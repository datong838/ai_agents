# 220tech · W2-X · AIP 决策审计组（#84 / #85 / #87）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §6.4 #84/#85 + §6.5 #87
> - 产品方案 [07](../07-AIP引擎k-LLM与AgentStudio产品方案.md) §6.4（Decision Lineage/Insight Backfill）· [07b](../07b-Capability-Adapter重能力接入.md) §3（Capability Adapter）
> - 技术方案 [T07](./T07-AIP人工智能平台详细技术方案.md) §5（Insight）/ §6.5（Capability Adapter）
> - 上游 W2-W ProposalSubmission（审批产物）/ W2-V MaturityEngine（能力评估）
> **范围**：W2-X 收口 AIP 决策可审计与重能力接入三件 — Decision Lineage（完整决策记录）/ Insight Backfill（高置信结论沉淀）/ Capability Adapter 契约（Manifest + 运行时 API + Facade）
> **不替换底层**：本组是 AIP 决策侧的可观测与重能力契约层，不重写 Drafts/Wiki/MediaSet

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/decision_audit.py` + `aos_api/routers/decision_audit.py` + `tests/test_decision_audit.py`；`main.py` 加 2 行 |
| 不影响已有功能 | Decision Lineage 只增审计记录；Insight Backfill 只增 Insight Object；Capability Adapter 只增契约层 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 符合方案军规 | Decision Lineage 字段与 220w §6.4 一致；Insight 与 T07 §5 一致；Capability Adapter 分级 C0/C1/C2 与 07b §3 一致 |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| Decision Lineage | Drafts 有基础时间线；无完整决策记录字段；无溯源 API | 🔴 缺 |
| Insight Backfill | 无高置信结论沉淀机制；无 Insight Object + Link | 🔴 缺 |
| Capability Adapter | 仅前端 s2/aip.tsx 有工具面板分类；无 Manifest/运行时 API/Facade | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #84 Decision Lineage：8 字段决策记录 + 时间线查询 + 溯源 API
  - #85 Insight Backfill：高置信结论 → Insight Object + Link + 阈值控制
  - #87 Capability Adapter 契约：Manifest CRUD + C0/C1/C2 分级 + 运行时 API（invoke/submit/status/cancel/artifact）+ Facade
- ❌ 本组不做：
  - Drafts 实际写回（属 W1）
  - Insight Object 实际写回 Ontology（简化版仅记录 backfill 记录）
  - C2 Session 流事件（简化版仅状态机）
  - CAP-01~07 约束执行（属 W2-Y 后续）

---

## 2. 数据模型

### 2.1 #84 Decision Lineage

```python
class DecisionRecord(BaseModel):
    """决策记录。"""
    id: str
    timestamp: float
    logic_id: str
    proposal_id: str = ""             # 关联 W2-W ProposalSubmission
    model_id: str = ""                # 选用模型
    prompt_version: str = ""          # Prompt 版本
    object_refs: list[str] = []       # 读取的 Object 引用
    wiki_fields: list[str] = []       # 读取的 Wiki 字段
    cot: str = ""                     # CoT 思维链
    tool_calls: list[dict[str, Any]] = []  # Tool 调用序列
    draft_params: dict[str, Any] = {} # Draft 参数
    approval_result: str = ""         # 审批结果 approved/rejected/pending
    actor: str = ""
    metadata: dict[str, Any] = {}
```

### 2.2 #85 Insight Backfill

```python
class InsightObject(BaseModel):
    """Insight 对象。"""
    id: str
    title: str
    content: str
    confidence: float                 # 0~1
    source_decision_id: str           # 来源决策记录
    object_type: str = "Insight"
    object_id: str = ""
    links: list[str] = []             # 关联 Ontology 对象 RID
    created_at: float = 0.0
    backfill_status: str = "pending"  # pending / completed / failed


class BackfillConfig(BaseModel):
    """回填配置。"""
    confidence_threshold: float = 0.85  # 高置信阈值
    auto_backfill: bool = False         # 是否自动回填
    max_daily_backfill: int = 100       # 每日上限
```

### 2.3 #87 Capability Adapter

```python
class AdapterManifest(BaseModel):
    """Capability Adapter Manifest。"""
    id: str
    name: str
    capability_class: str             # C0 同步 / C1 异步 Job / C2 长会话
    version: str = "1.0.0"
    description: str = ""
    invoke_endpoint: str = ""         # C0 invoke 端点
    submit_endpoint: str = ""         # C1 submit 端点
    status_endpoint: str = ""         # C1 status 端点
    cancel_endpoint: str = ""         # C1 cancel 端点
    artifact_endpoint: str = ""       # C1 artifact 端点
    session_open_endpoint: str = ""   # C2 session.open 端点
    session_close_endpoint: str = ""  # C2 session.close 端点
    auth_type: str = "none"           # none / bearer / basic / hmac
    enabled: bool = True
    registered_at: float = 0.0


class AdapterInvocation(BaseModel):
    """Capability Adapter 调用记录。"""
    id: str
    adapter_id: str
    capability_class: str             # C0 / C1 / C2
    operation: str                    # invoke / submit / status / cancel / artifact / session.open / session.close
    inputs: dict[str, Any] = {}
    outputs: dict[str, Any] = {}
    job_id: str = ""                  # C1 异步 Job ID
    session_id: str = ""              # C2 Session ID
    status: str = "pending"           # pending / running / completed / failed / cancelled
    started_at: float = 0.0
    ended_at: float = 0.0
    error: str = ""


_VALID_CAPABILITY_CLASSES = {"C0", "C1", "C2"}
_VALID_AUTH_TYPES = {"none", "bearer", "basic", "hmac"}
_VALID_OPERATIONS = {
    "invoke", "submit", "status", "cancel", "artifact",
    "session.open", "session.close",
}
_OPERATION_BY_CLASS = {
    "C0": {"invoke"},
    "C1": {"submit", "status", "cancel", "artifact"},
    "C2": {"session.open", "session.close"},
}
```

---

## 3. 引擎设计

文件：`aos_api/decision_audit.py`（新增，3 个引擎）

### 3.1 DecisionLineageEngine（#84）

```python
class DecisionLineageEngine:
    def record(self, rec: DecisionRecord) -> DecisionRecord: ...
    def get(self, decision_id: str) -> DecisionRecord: ...
    def list(
        self, logic_id: str | None = None, proposal_id: str | None = None,
        actor: str | None = None, limit: int = 50,
    ) -> list[DecisionRecord]: ...
    def get_timeline(self, decision_id: str) -> dict[str, Any]: ...
    """返回决策时间线（按时间排序的 Tool 调用 + 审批事件）"""
    def trace(self, proposal_id: str) -> list[DecisionRecord]: ...
    """按提案溯源（一个提案可能多条决策记录）"""
```

### 3.2 InsightBackfillEngine（#85）

```python
class InsightBackfillEngine:
    def get_config(self) -> BackfillConfig: ...
    def update_config(self, cfg: BackfillConfig) -> BackfillConfig: ...
    def register_insight(self, ins: InsightObject) -> InsightObject: ...
    def get_insight(self, insight_id: str) -> InsightObject: ...
    def list_insights(
        self, source_decision_id: str | None = None,
        backfill_status: str | None = None, min_confidence: float = 0.0,
        limit: int = 50,
    ) -> list[InsightObject]: ...
    def backfill(self, insight_id: str) -> InsightObject: ...
    """执行回填：标记 backfill_status=completed；简化版不实际写回 Ontology"""
    def evaluate_and_register(
        self, decision_id: str, title: str, content: str,
        confidence: float, links: list[str] | None = None,
    ) -> InsightObject: ...
    """评估置信度并注册 Insight（>= threshold 才注册）"""
    def list_pending(self, limit: int = 50) -> list[InsightObject]: ...
    def cleanup(self) -> int: ...
    """清理 backfill_status=failed 的旧记录"""
```

### 3.3 CapabilityAdapterEngine（#87）

```python
class CapabilityAdapterEngine:
    def register(self, manifest: AdapterManifest) -> AdapterManifest: ...
    def get(self, adapter_id: str) -> AdapterManifest: ...
    def list(self, capability_class: str | None = None, enabled_only: bool = False) -> list[AdapterManifest]: ...
    def update(self, adapter_id: str, updates: dict[str, Any]) -> AdapterManifest: ...
    def delete(self, adapter_id: str) -> bool: ...
    def invoke(
        self, adapter_id: str, inputs: dict[str, Any],
        invoke_callable: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    ) -> AdapterInvocation: ...
    """C0 同步调用：立即返回结果"""
    def submit(
        self, adapter_id: str, inputs: dict[str, Any],
        submit_callable: Callable[[dict[str, Any]], str] | None = None,
    ) -> AdapterInvocation: ...
    """C1 异步提交：返回 job_id"""
    def status(self, adapter_id: str, job_id: str,
               status_callable: Callable[[str], str] | None = None) -> AdapterInvocation: ...
    """C1 查询 job 状态"""
    def cancel(self, adapter_id: str, job_id: str) -> AdapterInvocation: ...
    """C1 取消 job"""
    def artifact(self, adapter_id: str, job_id: str,
                 artifact_callable: Callable[[str], dict[str, Any]] | None = None) -> AdapterInvocation: ...
    """C1 获取 job 产物"""
    def session_open(self, adapter_id: str, inputs: dict[str, Any] = {},
                     open_callable: Callable[[dict[str, Any]], str] | None = None) -> AdapterInvocation: ...
    """C2 开启会话"""
    def session_close(self, adapter_id: str, session_id: str) -> AdapterInvocation: ...
    """C2 关闭会话"""
    def list_invocations(
        self, adapter_id: str | None = None, job_id: str | None = None,
        session_id: str | None = None, limit: int = 50,
    ) -> list[AdapterInvocation]: ...
```

**invoke 流程**：
1. 取 manifest，校验 capability_class=C0 + enabled，否则抛 `INVALID_CLASS`/`ADAPTER_DISABLED`
2. 创建 AdapterInvocation(operation=invoke, status=running)
3. 调用 invoke_callable（默认返回 echo inputs）
4. 成功 → status=completed, outputs=结果
5. 失败 → status=failed, error
6. 200 条上限

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，200 条上限（records/insights/invocations）

---

## 4. API 设计

文件：`aos_api/routers/decision_audit.py`（新增）

### 4.1 #84 Decision Lineage

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/aip/decisions` | 记录决策 |
| GET | `/v1/aip/decisions` | 列表（支持 logic_id/proposal_id/actor 过滤） |
| GET | `/v1/aip/decisions/{decision_id}` | 单条决策 |
| GET | `/v1/aip/decisions/{decision_id}/timeline` | 决策时间线 |
| GET | `/v1/aip/decisions/by-proposal/{proposal_id}` | 按提案溯源 |

### 4.2 #85 Insight Backfill

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/insights/config` | 获取配置 |
| POST | `/v1/aip/insights/config` | 更新配置 |
| POST | `/v1/aip/insights` | 注册 Insight |
| GET | `/v1/aip/insights` | 列表 |
| GET | `/v1/aip/insights/{insight_id}` | 单条 |
| POST | `/v1/aip/insights/{insight_id}/backfill` | 执行回填 |
| POST | `/v1/aip/insights/evaluate` | 评估并注册 |
| GET | `/v1/aip/insights/pending` | 待回填列表 |
| POST | `/v1/aip/insights/cleanup` | 清理失败记录 |

### 4.3 #87 Capability Adapter

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/aip/capabilities/adapters` | 注册 Adapter |
| GET | `/v1/aip/capabilities/adapters` | 列表 |
| GET | `/v1/aip/capabilities/adapters/{adapter_id}` | 单条 |
| PUT | `/v1/aip/capabilities/adapters/{adapter_id}` | 更新 |
| DELETE | `/v1/aip/capabilities/adapters/{adapter_id}` | 删除 |
| POST | `/v1/aip/capabilities/adapters/{adapter_id}/invoke` | C0 同步调用 |
| POST | `/v1/aip/capabilities/adapters/{adapter_id}/submit` | C1 异步提交 |
| GET | `/v1/aip/capabilities/adapters/{adapter_id}/jobs/{job_id}/status` | C1 状态 |
| POST | `/v1/aip/capabilities/adapters/{adapter_id}/jobs/{job_id}/cancel` | C1 取消 |
| GET | `/v1/aip/capabilities/adapters/{adapter_id}/jobs/{job_id}/artifact` | C1 产物 |
| POST | `/v1/aip/capabilities/adapters/{adapter_id}/sessions/open` | C2 开会话 |
| POST | `/v1/aip/capabilities/adapters/{adapter_id}/sessions/{session_id}/close` | C2 关会话 |
| GET | `/v1/aip/capabilities/invocations` | 调用记录列表 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., decision_audit, ...)
application.include_router(decision_audit.router)
```

### 5.2 与 W2-W/W2-V 协同

- `DecisionLineageEngine.record` 可关联 W2-W `ProposalSubmission.id` 作为 proposal_id
- `InsightBackfillEngine.evaluate_and_register` 可消费 W2-X DecisionRecord 的 confidence 字段
- `CapabilityAdapterEngine.invoke` 可作为 W2-V `MaturityEngine` 的能力注册数据源（C0/C1/C2 接入即满足 `external_capability`）

### 5.3 与 07b §3 对齐

- C0 invoke 即时返回；C1 submit→jobId→status→artifact→MediaSet；C2 session.open→sessionId→流事件→session.close
- 简化版 C2 不实现流事件，仅状态机

---

## 6. 测试计划

文件：`tests/test_decision_audit.py`（新增，约 42 个用例）

### 6.1 DecisionLineageEngine（12）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | record | 返回带 id |
| 2 | get 未找到 | 抛 NOT_FOUND |
| 3 | list 默认 | 列表 |
| 4 | list 按 logic_id 过滤 | 仅返回匹配 |
| 5 | list 按 proposal_id 过滤 | 仅返回匹配 |
| 6 | list 按 actor 过滤 | 仅返回匹配 |
| 7 | get_timeline | 返回时间线 |
| 8 | trace by proposal | 返回溯源 |
| 9 | record 含完整 8 字段 | 字段保留 |
| 10 | list limit | 截断 |
| 11 | 200 条上限 | 旧记录被淘汰 |
| 12 | get 单条 | 返回详情 |

### 6.2 InsightBackfillEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | get_config 默认 | threshold=0.85, auto=False |
| 2 | update_config | 修改后 get 返回新值 |
| 3 | register_insight | 返回带 id |
| 4 | get_insight 未找到 | NOT_FOUND |
| 5 | list_insights 默认 | 列表 |
| 6 | list_insights min_confidence | 过滤低置信 |
| 7 | list_insights source_decision_id | 过滤 |
| 8 | list_insights backfill_status | 过滤 |
| 9 | backfill 成功 | status=completed |
| 10 | evaluate_and_register 高置信 | 注册成功 |
| 11 | evaluate_and_register 低置信 | 抛 BELOW_THRESHOLD |
| 12 | list_pending | 仅 pending |
| 13 | cleanup 清理 failed | 返回数量 |
| 14 | backfill 已 completed | 抛 ALREADY_BACKFILLED |

### 6.3 CapabilityAdapterEngine（16）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register C0 Adapter | 返回带 id |
| 2 | register 未知 class | 抛 INVALID_CLASS |
| 3 | register 未知 auth | 抛 INVALID_AUTH_TYPE |
| 4 | get 未找到 | NOT_FOUND |
| 5 | list 默认 | 列表 |
| 6 | list 按 class 过滤 | 仅 C0 |
| 7 | list enabled_only | 过滤禁用 |
| 8 | update | 修改后 get 返回新值 |
| 9 | delete | 删除成功 |
| 10 | invoke C0 成功 | status=completed |
| 11 | invoke C1 抛 INVALID_CLASS | 错误 |
| 12 | invoke 禁用 Adapter | ADAPTER_DISABLED |
| 13 | submit C1 | 返回 job_id |
| 14 | status C1 | 返回状态 |
| 15 | cancel C1 | status=cancelled |
| 16 | session_open + session_close C2 | 状态正确 |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| Decision Lineage 字段过多导致写入慢 | 字段全部可选；200 条上限防膨胀 |
| Insight 误回填 | 阈值 0.85 + auto_backfill 默认关闭 |
| Capability Adapter 调用阻塞 | invoke_callable/submit_callable 可注入异步实现 |
| C2 流事件未实现 | 简化版仅状态机；后续扩展 |
| Manifest 端点暴露 | auth_type 强制 + enabled 默认 false → 注册后显式开启 |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-x-decision-audit.md` | 新建 | 本文档 |
| `aos-platform/services/aos-api/aos_api/decision_audit.py` | 新建 | 3 引擎 + 单例 |
| `aos-platform/services/aos-api/aos_api/routers/decision_audit.py` | 新建 | ~28 个端点 |
| `aos-platform/services/aos-api/tests/test_decision_audit.py` | 新建 | ~42 测试 |
| `aos-platform/services/aos-api/aos_api/main.py` | 修改 2 行 | import + include_router |
| `docs/palantier/20_tech/220plan-分阶段开发与里程碑计划.md` | 更新 | v3.6 → v3.7，标记 #84/#85/#87 ✅ |

---

## 9. 验收标准

1. ✅ 所有 ~42 个单测全绿
2. ✅ 全量回归无新增失败（pre-existing wiki flaky 不计）
3. ✅ `main.py` 启动无报错，新路由 `/v1/aip/decisions/*` `/v1/aip/insights/*` `/v1/aip/capabilities/*` 可访问
4. ✅ 方案文档与代码字段一致
5. ✅ 看板进度从 53/166 → 56/166，全局 99 → 102 / 259
