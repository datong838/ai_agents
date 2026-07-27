# 220tech · W2-T · k-LLM 路由编排组（#71 / #72 / #73）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §12 #71/#72/#73
> - 产品方案 [07](../07-AIP引擎k-LLM与AgentStudio产品方案.md) §2.1/§2.4/§6.2（场景化路由 / 热切换 / 数据出境）
> - 路由 UI 规整 [81](./81-模型路由可编辑与工具面板文案规整方案.md) §2 RouteRule 数据结构
> - 底层网关 `aos_api/llm_gateway.py` · `aos_api/llm_provider_registry.py`
> **范围**：W2-T 收口三件 — 智能路由（按请求特征自动选模）· 场景化路由（按任务类型/块级选模）· 熔断与热切换（主模失败自动切回退）
> **不替换底层**：本组是 `llm_gateway.chat()` 之上的**策略层编排**；最终调用仍走底层网关，不重写 provider 注册/密钥解析/sidecar 探测逻辑。

---

## 0. 使用的 Rules（按用户规则强制声明）

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/llm_routing.py` + `aos_api/routers/llm_routing.py` + `tests/test_llm_routing.py`；`main.py` 加 2 行（import + include_router）；不动 `llm_gateway.py` / `llm_provider_registry.py` / `gateway_default.py` |
| 不影响已有功能 | 路由编排层为可选前置；不修改 `chat()` 签名；现有调用方零感知 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 符合方案军规 | RouteRule 与 81 §2.1 数据结构对齐；egress 枚举与 07 §2.4 一致 |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| 底层调用 | `llm_gateway.chat(query, model=X)` 显式指定模型；未指定时走 `gateway_default` | ✅ 已有 |
| 默认路由 | 单一默认 text 模型；无按任务/上下文/安全等级选模 | 🔴 缺 |
| 场景化 | 无任务类型 → 模型映射；Logic 内 Block 无块级选模 | 🔴 缺 |
| 熔断 | 仅 `fallback_mode=mock` 兜底；无连续失败计数；无 half_open 探测；无主备自动切换 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：策略层决策（选哪个模型）+ 熔断器状态机 + 主备热切换
- ❌ 本组不做：模型能力评估（属 #78 Modeling Objectives）、数据出境策略（属 #74）、自定义 LLM 注册（属 #75）、UI 路由编辑（属 81 前端刀）
- ❌ 不替换：`llm_gateway.chat()` / `gateway_default` / `llm_provider_registry`

---

## 2. 数据模型

### 2.1 ModelCandidate（#71 智能路由候选）

```python
class ModelCandidate(BaseModel):
    id: str                        # 模型 id（与 llm_gateway 可路由 id 对齐）
    tier: Literal["low", "mid", "high"] = "mid"   # 能力档位
    max_context: int = 8192        # 最大上下文 token 数
    modalities: list[str] = ["text"]  # text/image/video/embed
    cost_per_1k: float = 0.0       # 单价（USD per 1k tokens）
    egress: Literal["allow", "restricted", "forbidden"] = "allow"
                                   # 出境策略：allow=可公网 / restricted=脱敏后可 / forbidden=仅私有
    tags: list[str] = []           # 业务标签（如 "code", "math", "vision"）
    enabled: bool = True
```

### 2.2 RoutingRequest（#71 选模请求）

```python
class RoutingRequest(BaseModel):
    query: str = ""
    context_length: int = 0        # 预估上下文 token 数
    complexity: int = 1            # 1-5，5 最复杂
    tools_required: list[str] = []
    security_label: Literal["public", "internal", "sensitive", "restricted"] = "internal"
    cost_budget: float | None = None  # 单次调用预算上限（USD）
    preferred_modalities: list[str] = ["text"]
    prefer_tags: list[str] = []
```

### 2.3 RouteRule（#72 场景化路由规则，对齐 81 §2.1）

```python
class RouteRule(BaseModel):
    id: str                        # summarize | wiki_qa | logic_long | chatbot | pii | provider_down | 自定义
    task: str                      # 展示名（中文）
    task_type: Literal[
        "chat", "code", "math", "vision",
        "extract", "summarize", "wiki_qa",
        "pii", "provider_down", "logic_long", "chatbot"
    ]
    primary: str                   # 模型 id 或 "—"
    fallback: str = ""             # 模型 id / "—" / ""
    egress: Literal[
        "禁公网", "审批后", "继承", "强制不出域", "fallback"
    ] = "继承"                       # 与 81 §2.1 egress 枚举对齐
    span: bool = False             # Provider 不可用行：首选跨列
    enabled: bool = True
```

### 2.4 BlockRoute（#72 块级选模）

```python
class BlockRoute(BaseModel):
    block_id: str                  # Logic 内 Block 实例 id
    logic_id: str = ""             # 所属 Logic 图
    model_id: str                  # 绑定的模型 id
    task_type: str = ""            # 可选，关联 RouteRule.task_type
    inherit: bool = False          # True=继承 logic_id 级或全局默认
```

### 2.5 CircuitState（#73 熔断器状态）

```python
class CircuitState(BaseModel):
    model_id: str
    state: Literal["closed", "open", "half_open"] = "closed"
    consecutive_failures: int = 0
    last_failure_at: float = 0.0   # epoch seconds
    opened_at: float = 0.0         # 进入 open 的时间戳
    half_open_probes: int = 0      # half_open 状态下已发出探测数
```

熔断器配置（per-model 可覆盖）：

```python
class CircuitConfig(BaseModel):
    failure_threshold: int = 3       # 连续失败 ≥N 触发 open
    cooldown_seconds: float = 60.0   # open → half_open 冷却时间
    half_open_max_probes: int = 1    # half_open 最多并发探测
    success_threshold: int = 1       # half_open 连续成功 ≥N 关闭熔断
```

### 2.6 CallRecord（#73 调用记录，用于审计与决策）

```python
class CallRecord(BaseModel):
    id: str
    model_id: str
    route_source: Literal["smart", "scenario", "block", "explicit", "failover"]
    success: bool
    latency_ms: int = 0
    error: str = ""
    fallback_used: bool = False
    timestamp: float
```

---

## 3. 引擎设计

文件：`aos_api/llm_routing.py`（新增，3 个引擎 + 1 个统一 facade）

### 3.1 SmartRouter（#71）

```python
class SmartRouter:
    def register(self, candidate: ModelCandidate) -> ModelCandidate: ...
    def unregister(self, model_id: str) -> bool: ...
    def list(self, enabled_only: bool = False) -> list[ModelCandidate]: ...
    def choose(self, request: RoutingRequest) -> dict:
        """返回 { model_id, reason, alternatives, score_breakdown }"""
```

**评分算法**：

```
score = (
    w_capability * capability_match(tier, complexity)
  + w_context    * context_fit(max_context, context_length)
  + w_cost       * cost_score(cost_per_1k, cost_budget)
  + w_security   * security_match(egress, security_label)
  + w_tag        * tag_overlap(tags, prefer_tags)
)
```

权重默认：`w_capability=0.30, w_context=0.25, w_cost=0.15, w_security=0.20, w_tag=0.10`

**硬过滤**（不满足直接淘汰，不参与评分）：
- `enabled=False`
- `max_context < context_length`
- `preferred_modalities` 与 `modalities` 无交集
- `security_label=restricted` 且 `egress != forbidden`
- `cost_budget` 非 None 且 `cost_per_1k * context_length / 1000 > cost_budget`

**返回结构**：

```python
{
    "model_id": "agnes-text",
    "reason": "capability=high 复杂度5 / context=32k 满足 / security=forbidden 满足 restricted",
    "score": 0.91,
    "alternatives": [{"model_id": "deepseek-chat", "score": 0.78}, ...],
    "score_breakdown": {"capability": 0.30, "context": 0.25, ...}
}
```

无候选时抛 `RoutingError(code="NO_CANDIDATE")`。

### 3.2 ScenarioRouter（#72）

```python
class ScenarioRouter:
    def upsert_rule(self, rule: RouteRule) -> RouteRule: ...
    def get_rule(self, rule_id: str) -> RouteRule: ...
    def list_rules(self, task_type: str | None = None) -> list[RouteRule]: ...
    def delete_rule(self, rule_id: str) -> bool: ...
    def resolve(self, task_type: str, block_id: str | None = None) -> dict:
        """返回 { primary, fallback, egress, source: "block"|"scenario"|"default" }"""
```

**解析顺序**（块级优先 → 场景 → 默认）：

1. 若 `block_id` 提供 且存在 `BlockRoute(block_id)` 且 `inherit=False` → 返回 `block.model_id`
2. 否则查 `RouteRule(task_type=...)` → 返回 `primary/fallback/egress`
3. 否则回落到默认模型（从 `gateway_default.get_gateway_default()` 读 `defaultModel`）

**与 81 协议对齐**：`GET/PUT /v1/aip/model-routes` 返回的 `items` 即 `RouteRule[]`，本引擎提供 `export_rules()` / `import_rules()` 给 81 路由调用。

### 3.3 FailoverEngine（#73）

```python
class FailoverEngine:
    def get_state(self, model_id: str) -> CircuitState: ...
    def set_config(self, model_id: str, config: CircuitConfig) -> CircuitConfig: ...
    def record_call(self, model_id: str, success: bool, error: str = "", latency_ms: int = 0) -> CallRecord: ...
    def can_call(self, model_id: str) -> bool:
        """closed/half_open(探测配额内) → True；open（冷却未到）→ False"""
    def call_with_failover(
        self,
        query: str,
        primary: str,
        fallback: str = "",
        route_source: str = "explicit",
    ) -> dict:
        """主模可调 → 调主模；失败或熔断 → 切 fallback；都失败抛 RoutingError"""
```

**状态机**：

```
CLOSED ──连续失败≥threshold──► OPEN
OPEN ──cooldown 到期──► HALF_OPEN
HALF_OPEN ──探测成功≥success_threshold──► CLOSED
HALF_OPEN ──探测失败──► OPEN（重置 cooldown 计时）
```

**call_with_failover 流程**：

1. 查 primary 熔断状态
   - `closed` / `half_open`（探测配额未满）→ 调用底层 `llm_gateway.chat(query, model=primary)`
   - `open` 或 `half_open` 配额满 → 跳过 primary，直接走 fallback
2. primary 调用结果记录到 `record_call`
   - 成功 → 返回结果（含 `fallback_used=False`）
   - 失败 → 进入 fallback 分支
3. fallback 分支
   - fallback 为空或 "—" → 抛 `RoutingError(code="PRIMARY_FAILED_NO_FALLBACK")`
   - fallback 模型熔断 `open` → 抛 `RoutingError(code="FALLBACK_OPEN")`
   - 否则调用底层 `llm_gateway.chat(query, model=fallback)`，记录 `record_call`
   - 成功 → 返回结果（含 `fallback_used=True`）
   - 失败 → 抛 `RoutingError(code="ALL_FAILED")`
4. 返回结构：`{ answer, model, fallback_used, route_source, call_record_id }`

### 3.4 LLMRoutingFacade（统一编排入口）

```python
class LLMRoutingFacade:
    """组合三引擎，提供端到端智能路由调用。"""
    def smart_route_and_call(self, request: RoutingRequest) -> dict:
        """SmartRouter.choose → ScenarioRouter 协同 → FailoverEngine.call_with_failover"""

    def scenario_route_and_call(self, task_type: str, query: str, block_id: str | None = None) -> dict:
        """ScenarioRouter.resolve → FailoverEngine.call_with_failover"""
```

### 3.5 单例与持久化

- 3 个引擎 + Facade 均用**双重检查锁单例**（与项目其他引擎一致：ActionLogEngine/SagaEngine 等）
- 持久化走 `aos_api.aip_kv_store.put_payload / get_payload`（与 `llm_provider_registry` 一致），key 前缀：
  - `llm_routing_candidates`（SmartRouter 注册表）
  - `llm_routing_rules`（ScenarioRouter 规则）
  - `llm_routing_blocks`（BlockRoute）
  - `llm_routing_circuits`（CircuitState per model）
  - `llm_routing_circuit_configs`（CircuitConfig per model）
  - `llm_routing_call_records`（最近 N 条 CallRecord，N=200）

---

## 4. API 设计

文件：`aos_api/routers/llm_routing.py`（新增）

### 4.1 Smart Router（#71）

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/smart-router/candidates` | 列出所有候选模型 |
| POST | `/v1/aip/smart-router/candidates` | 注册候选模型 |
| DELETE | `/v1/aip/smart-router/candidates/{model_id}` | 注销候选模型 |
| POST | `/v1/aip/smart-router/choose` | body=RoutingRequest，返回选模结果 |
| POST | `/v1/aip/smart-router/route-and-call` | 选模并调用底层网关 |

### 4.2 Scenario Router（#72）

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/scenario-router/rules` | 列出 RouteRule（可按 task_type 过滤） |
| GET | `/v1/aip/scenario-router/rules/{rule_id}` | 单条 |
| POST | `/v1/aip/scenario-router/rules` | 新增/更新 RouteRule |
| DELETE | `/v1/aip/scenario-router/rules/{rule_id}` | 删除 |
| POST | `/v1/aip/scenario-router/resolve` | body={task_type, block_id?}，返回 primary/fallback |
| GET | `/v1/aip/scenario-router/blocks` | 列出 BlockRoute |
| POST | `/v1/aip/scenario-router/blocks` | 新增/更新 BlockRoute |
| DELETE | `/v1/aip/scenario-router/blocks/{block_id}` | 删除 |
| POST | `/v1/aip/scenario-router/route-and-call` | 场景路由并调用 |

### 4.3 Failover Engine（#73）

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/failover/circuits` | 列出所有模型熔断状态 |
| GET | `/v1/aip/failover/circuits/{model_id}` | 单模型熔断状态 |
| POST | `/v1/aip/failover/circuits/{model_id}/reset` | 强制重置为 closed |
| PUT | `/v1/aip/failover/circuits/{model_id}/config` | 更新 CircuitConfig |
| POST | `/v1/aip/failover/call` | body={query, primary, fallback?}，主备热切换调用 |
| GET | `/v1/aip/failover/call-records` | 最近调用记录（可按 model_id 过滤） |
| POST | `/v1/aip/failover/circuit-drill` | 熔断演练（与 81 §2.1 对齐，不改生产路由） |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
# aos_api/routers/__init__.py 与 main.py 同步添加 llm_routing
from aos_api.routers import (..., llm_routing, ...)
application.include_router(llm_routing.router)
```

### 5.2 与底层网关的调用契约

- `FailoverEngine.call_with_failover` 内部调用 `from aos_api.llm_gateway import chat`
- 调用签名固定为 `chat(query, model=model_id)`，不修改 `chat` 任何参数
- `llm_gateway.chat` 抛 `RuntimeError` 时，FailoverEngine 捕获并记录 `CallRecord(success=False, error=str(exc))`

### 5.3 与 81 路由编辑 UI 的对接

- `GET /v1/aip/scenario-router/rules` 与 81 §2.1 `GET /v1/aip/model-routes` 数据结构对齐（id/task/primary/fallback/egress/span）
- 81 前端 PUT `/v1/aip/model-routes` 时，后端可调用 `ScenarioRouter.import_rules(items)` 持久化
- `POST /v1/aip/failover/circuit-drill` 与 81 §2.1 熔断演练端点对齐

---

## 6. 测试计划

文件：`tests/test_llm_routing.py`（新增，约 42 个用例）

### 6.1 SmartRouter（12）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register 候选 | 返回带 id 的候选 |
| 2 | unregister | 注销后 list 不含 |
| 3 | list enabled_only | 过滤 enabled=False |
| 4 | choose 基础 | 返回最高分模型 |
| 5 | choose 上下文超限 | 该候选被淘汰 |
| 6 | choose 模态不匹配 | 该候选被淘汰 |
| 7 | choose 安全等级 restricted | 仅 egress=forbidden 候选入选 |
| 8 | choose 成本预算 | 超预算候选淘汰 |
| 9 | choose 无候选 | 抛 NO_CANDIDATE |
| 10 | choose 复杂度与 tier 匹配 | high 复杂度优先 high tier |
| 11 | choose tag 加分 | prefer_tags 命中加分 |
| 12 | choose 返回 alternatives | 包含次优候选列表 |

### 6.2 ScenarioRouter（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | upsert_rule 新增 | 返回带 id 的 rule |
| 2 | upsert_rule 更新 | 同 id 覆盖 |
| 3 | get_rule 未找到 | 抛 NOT_FOUND |
| 4 | list_rules 按 task_type 过滤 | 仅返回匹配项 |
| 5 | delete_rule | 删除后 get 抛 NOT_FOUND |
| 6 | resolve 块级优先 | block_id 命中时返回 block.model_id |
| 7 | resolve 块级 inherit=True | 跳过 block，走 scenario |
| 8 | resolve 场景命中 | 返回 primary/fallback |
| 9 | resolve 场景未命中 | 回落默认 source=default |
| 10 | BlockRoute CRUD | 增/查/改/删 |
| 11 | BlockRoute 删除保护 | 不影响 scenario rule |
| 12 | export_rules | 与 81 RouteRule 结构对齐 |
| 13 | import_rules | 批量导入并覆盖 |

### 6.3 FailoverEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | get_state 初始 | closed, failures=0 |
| 2 | record_call 失败计数 | 连续失败递增 |
| 3 | record_call 成功重置 | 连续失败归零 |
| 4 | 熔断触发 | 连续失败≥3 → open |
| 5 | 冷却未到 can_call | False |
| 6 | 冷却到期 → half_open | can_call True（探测配额内） |
| 7 | half_open 探测成功 → closed | state=closed |
| 8 | half_open 探测失败 → open | 重置 cooldown |
| 9 | call_with_failover 主模成功 | fallback_used=False |
| 10 | call_with_failover 主模失败 → 切 fallback | fallback_used=True |
| 11 | call_with_failover 主模 open → 跳过直走 fallback | 不调用主模 |
| 12 | call_with_failover 无 fallback | 抛 PRIMARY_FAILED_NO_FALLBACK |
| 13 | call_with_failover fallback 也失败 | 抛 ALL_FAILED |
| 14 | reset 强制重置 | state=closed, failures=0 |

### 6.4 集成（3）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | smart_route_and_call 端到端 | 选模 → 调用 → 返回 answer |
| 2 | scenario_route_and_call 端到端 | 任务路由 → 调用 → 返回 answer |
| 3 | call_with_failover 与 llm_gateway mock 协同 | 主模 mock-llm 调用成功 |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 路由层与底层网关重复造轮子 | 严格只调用 `chat(query, model=X)`；不重写 provider 解析/密钥解析/sidecar 探测 |
| 熔断器状态丢失 | 持久化到 `aip_kv_store`；进程重启后从 kv 恢复 |
| 评分权重不公 | 权重作为常量集中定义，便于后续调参；提供 `score_breakdown` 透明可审计 |
| 与 81 UI 不一致 | RouteRule 字段对齐 81 §2.1；export/import 双向兼容 |
| 默认候选为空 | `SmartRouter` 启动时自动从 `llm_gateway.models_payload()` 同步一份默认候选（lazy） |
| 熔断演练误改生产 | `circuit-drill` 仅返回推演结果，不调用 `record_call` |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-t-llm-routing.md` | 新建 | 本文档 |
| `aos-platform/services/aos-api/aos_api/llm_routing.py` | 新建 | 3 引擎 + Facade + 单例 |
| `aos-platform/services/aos-api/aos_api/routers/llm_routing.py` | 新建 | ~20 个端点 |
| `aos-platform/services/aos-api/tests/test_llm_routing.py` | 新建 | ~42 测试 |
| `aos-platform/services/aos-api/aos_api/main.py` | 修改 2 行 | import + include_router |
| `docs/palantier/20_tech/220plan-分阶段开发与里程碑计划.md` | 更新 | v3.2 → v3.3，标记 #71/#72/#73 ✅ |

---

## 9. 验收标准

1. ✅ 所有 42 个单测全绿
2. ✅ 全量回归无新增失败（pre-existing wiki flaky 不计）
3. ✅ `main.py` 启动无报错，新路由 `/v1/aip/smart-router/*` `/v1/aip/scenario-router/*` `/v1/aip/failover/*` 可访问
4. ✅ 方案文档与代码字段一致（RouteRule/CircuitState/CallRecord 等）
5. ✅ 看板进度从 41/166 → 44/166，全局 87 → 90 / 259
