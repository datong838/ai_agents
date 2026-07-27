# 220tech · W2-V · AIP 智能层扩展组（#78 / #79 / #80）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §12 #78/#79/#80
> - 产品方案 [07](../07-AIP引擎k-LLM与AgentStudio产品方案.md) §4.4（调试器）· §5（Automate）· §6.1（四层成熟度）
> - 上游 W1-2 Logic 引擎 / W2-T LLMRoutingFacade / W2-U EgressPolicyEngine
> **范围**：W2-V 收口三件 — 调试器（CoT 步进 + 提议预览）· Automate 集成（条件触发 + 提案）· 四层成熟度（L1/L2/L3/L4 楼梯）
> **不替换底层**：本组是 AIP 智能层的可观测性与自动化能力补充，不重写 Logic 引擎与 LLM 网关

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/aip_extras.py` + `aos_api/routers/aip_extras.py` + `tests/test_aip_extras.py`；`main.py` 加 2 行 |
| 不影响已有功能 | 调试器是 Logic 引擎的可观测层；Automate 是 Logic 之上的触发器；四层成熟度是 AIP 整体评估 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 符合方案军规 | L1/L2/L3/L4 与 07 §6.1 一致；Automate 与 07 §5 一致；调试器与 07 §4.4 一致 |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| 调试器 | Logic 引擎可执行但无 CoT 步进；无提议预览 | 🔴 缺 |
| Automate | Logic 引擎可手动触发；无事件订阅 + 自动触发 | 🔴 缺 |
| 四层成熟度 | 无整体 AIP 能力评估 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #78 调试器：CoT 步进执行 + 中间变量快照 + 提议预览（不应用）
  - #79 Automate：事件触发器 CRUD + 触发评估 + 自动调用 Logic 生成提案
  - #80 四层成熟度：L1/L2/L3/L4 评估 + 升级降级 + 看板
- ❌ 本组不做：
  - Logic 引擎本身（属 W1-2）
  - LLM 网关调用（属 W2-T）
  - 自动化部署（属运维层）

---

## 2. 数据模型

### 2.1 #78 调试器

```python
class DebugSession(BaseModel):
    """调试会话。"""
    id: str
    logic_id: str
    inputs: dict[str, Any] = {}
    status: Literal["pending", "running", "paused", "completed", "failed"] = "pending"
    current_step: int = 0
    steps: list[DebugStep] = []
    started_at: float = 0.0
    ended_at: float = 0.0
    error: str = ""


class DebugStep(BaseModel):
    """调试步骤。"""
    index: int
    block_id: str
    block_type: str                # input / create_var / get_attr / use_llm / transform / apply_action / execute
    inputs: dict[str, Any] = {}    # 步骤输入快照
    outputs: dict[str, Any] = {}   # 步骤输出快照
    variables_after: dict[str, Any] = {}  # 执行后变量上下文
    status: Literal["pending", "running", "completed", "failed", "skipped"] = "pending"
    error: str = ""
    started_at: float = 0.0
    duration_ms: int = 0


class ProposalPreview(BaseModel):
    """提议预览。"""
    id: str
    logic_id: str
    debug_session_id: str
    proposed_changes: list[ProposedChange] = []
    applied: bool = False          # 预览默认不应用


class ProposedChange(BaseModel):
    """单条提议变更。"""
    object_type: str
    object_id: str
    field_path: str
    old_value: Any = None
    new_value: Any = None
    change_type: Literal["create", "update", "delete"] = "update"
    rationale: str = ""            # LLM 推理理由
```

### 2.2 #79 Automate

```python
class AutomateTrigger(BaseModel):
    """自动化触发器。"""
    id: str
    name: str
    logic_id: str                  # 触发后调用的 Logic
    event_type: Literal[
        "object_changed", "schedule", "manual", "webhook", "threshold"
    ] = "manual"
    condition: dict[str, Any] = {}  # 条件树（与 CriteriaEngine 对齐）
    enabled: bool = True
    cooldown_seconds: float = 0.0   # 冷却期，防止抖动
    last_triggered_at: float = 0.0
    trigger_count: int = 0
    description: str = ""


class AutomateRun(BaseModel):
    """自动化执行记录。"""
    id: str
    trigger_id: str
    logic_id: str
    trigger_event: str = ""
    status: Literal["pending", "running", "completed", "failed", "skipped"] = "pending"
    proposal_id: str = ""          # 生成的提议 id（待人工审批）
    started_at: float = 0.0
    ended_at: float = 0.0
    error: str = ""
```

### 2.3 #80 四层成熟度

```python
class MaturityLevel(BaseModel):
    """成熟度等级定义。"""
    level: Literal["L1", "L2", "L3", "L4"]
    name: str
    description: str
    required_capabilities: list[str] = []  # 必备能力标签


class MaturityAssessment(BaseModel):
    """成熟度评估结果。"""
    id: str
    timestamp: float
    current_level: str             # L1 / L2 / L3 / L4
    target_level: str = "L4"
    capabilities: dict[str, bool] = {}  # capability → 满足与否
    score: float = 0.0             # 0~1
    gaps: list[str] = []           # 缺失能力列表
    recommendation: str = ""


# L1/L2/L3/L4 默认定义
DEFAULT_LEVELS = {
    "L1": MaturityLevel(
        level="L1", name="基础",
        description="规则驱动 + 人工调用",
        required_capabilities=["rule_engine", "manual_call"],
    ),
    "L2": MaturityLevel(
        level="L2", name="辅助",
        description="LLM 辅助 + 人工审核",
        required_capabilities=["llm_gateway", "prompt_engineering", "evals"],
    ),
    "L3": MaturityLevel(
        level="L3", name="半自动",
        description="Logic 编排 + 自动触发 + 人工审批",
        required_capabilities=["logic_engine", "automate", "debugger", "proposal_preview"],
    ),
    "L4": MaturityLevel(
        level="L4", name="全自动",
        description="端到端自动 + 熔断 + 自愈",
        required_capabilities=["failover", "circuit_breaker", "auto_apply", "monitoring"],
    ),
}
```

---

## 3. 引擎设计

文件：`aos_api/aip_extras.py`（新增，3 个引擎）

### 3.1 DebuggerEngine（#78）

```python
class DebuggerEngine:
    def create_session(self, logic_id: str, inputs: dict[str, Any]) -> DebugSession: ...
    def get_session(self, session_id: str) -> DebugSession: ...
    def list_sessions(self, logic_id: str | None = None) -> list[DebugSession]: ...
    def step_forward(self, session_id: str) -> DebugStep: ...
    """前进一步：执行下一未完成步骤，记录输入/输出/变量快照"""
    def step_backward(self, session_id: str) -> DebugStep: ...
    """后退一步：回到上一已完成步骤，恢复变量上下文"""
    def run_to_completion(self, session_id: str) -> DebugSession: ...
    """连续 step_forward 直到完成或失败"""
    def preview_proposal(
        self, session_id: str, changes: list[ProposedChange],
    ) -> ProposalPreview: ...
    """生成提议预览（不应用）"""
    def list_proposals(self, session_id: str | None = None) -> list[ProposalPreview]: ...
    def apply_proposal(self, proposal_id: str) -> ProposalPreview: ...
    """应用提议（标记 applied=True；实际写回走 writeback 模块）"""
```

**step_forward 流程**：
1. 取 session，若 status != paused/pending 抛错
2. 取 `current_step` 索引，若越界标记 completed
3. 模拟执行 block（这里做简化：不实际调用 LLM，只记录变量流转）
4. 记录 step.inputs / step.outputs / step.variables_after
5. current_step += 1，status=paused（除非已是最后一步→completed）

### 3.2 AutomateEngine（#79）

```python
class AutomateEngine:
    def upsert_trigger(self, trigger: AutomateTrigger) -> AutomateTrigger: ...
    def get_trigger(self, trigger_id: str) -> AutomateTrigger: ...
    def list_triggers(self, enabled_only: bool = False) -> list[AutomateTrigger]: ...
    def delete_trigger(self, trigger_id: str) -> bool: ...
    def evaluate(
        self, trigger_id: str, event: dict[str, Any],
    ) -> bool: ...
    """评估触发条件是否满足（condition 树评估）"""
    def fire(
        self, trigger_id: str, event: dict[str, Any] = {},
    ) -> AutomateRun: ...
    """触发：检查 cooldown → evaluate → 调用 Logic → 生成 Proposal"""
    def list_runs(
        self, trigger_id: str | None = None, limit: int = 50,
    ) -> list[AutomateRun]: ...
    def get_run(self, run_id: str) -> AutomateRun: ...
```

**fire 流程**：
1. 取 trigger，若 disabled 抛 `AUTOMATE_DISABLED`
2. 若 `cooldown_seconds > 0` 且 `now - last_triggered_at < cooldown` 抛 `IN_COOLDOWN`
3. 调用 `evaluate(trigger_id, event)`，若不满足抛 `CONDITION_NOT_MET`
4. 创建 AutomateRun(status=running)
5. 模拟调用 Logic（简化：不实际执行，标记 completed）
6. 更新 trigger.last_triggered_at 与 trigger_count
7. 返回 AutomateRun

### 3.3 MaturityEngine（#80）

```python
class MaturityEngine:
    def list_levels(self) -> list[MaturityLevel]: ...
    def get_level(self, level: str) -> MaturityLevel: ...
    def upsert_level(self, level: MaturityLevel) -> MaturityLevel: ...
    """更新等级定义（管理员）"""
    def register_capability(self, name: str, satisfied: bool) -> None: ...
    """注册能力满足情况"""
    def list_capabilities(self) -> dict[str, bool]: ...
    def assess(self) -> MaturityAssessment: ...
    """评估当前成熟度：找最高满足等级"""
    def list_assessments(self, limit: int = 20) -> list[MaturityAssessment]: ...
    def set_target_level(self, level: str) -> None: ...
    def get_target_level(self) -> str: ...
```

**assess 流程**：
1. 取所有 level 定义（L1→L4）
2. 对每个 level，检查 `required_capabilities` 是否全部满足
3. 找最高满足的 level 作为 `current_level`
4. 计算 `score = satisfied_count / total_count`
5. `gaps` = 当前 level 到 target_level 之间缺失的能力
6. `recommendation` 文案：如"当前 L2，目标 L4，需补齐 automate/debugger/failover 等能力"

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 持久化走 `aip_kv_store`，key 前缀：
  - `aip_extras_debug_sessions`
  - `aip_extras_proposals`
  - `aip_extras_automate_triggers`
  - `aip_extras_automate_runs`
  - `aip_extras_maturity_levels`
  - `aip_extras_maturity_capabilities`
  - `aip_extras_maturity_assessments`
  - `aip_extras_maturity_target`

---

## 4. API 设计

文件：`aos_api/routers/aip_extras.py`（新增）

### 4.1 #78 调试器

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/aip/debugger/sessions` | 创建调试会话 |
| GET | `/v1/aip/debugger/sessions` | 列出会话 |
| GET | `/v1/aip/debugger/sessions/{session_id}` | 单条会话 |
| POST | `/v1/aip/debugger/sessions/{session_id}/step-forward` | 前进一步 |
| POST | `/v1/aip/debugger/sessions/{session_id}/step-backward` | 后退一步 |
| POST | `/v1/aip/debugger/sessions/{session_id}/run` | 连续执行到完成 |
| POST | `/v1/aip/debugger/sessions/{session_id}/preview` | 生成提议预览 |
| GET | `/v1/aip/debugger/proposals` | 列出提议 |
| POST | `/v1/aip/debugger/proposals/{proposal_id}/apply` | 应用提议 |

### 4.2 #79 Automate

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/automate/triggers` | 列出触发器 |
| POST | `/v1/aip/automate/triggers` | 新增/更新 |
| GET | `/v1/aip/automate/triggers/{trigger_id}` | 单条 |
| DELETE | `/v1/aip/automate/triggers/{trigger_id}` | 删除 |
| POST | `/v1/aip/automate/triggers/{trigger_id}/evaluate` | 评估触发条件 |
| POST | `/v1/aip/automate/triggers/{trigger_id}/fire` | 触发执行 |
| GET | `/v1/aip/automate/runs` | 列出执行记录 |
| GET | `/v1/aip/automate/runs/{run_id}` | 单条执行记录 |

### 4.3 #80 四层成熟度

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/maturity/levels` | 列出 L1~L4 定义 |
| GET | `/v1/aip/maturity/levels/{level}` | 单条等级 |
| POST | `/v1/aip/maturity/levels` | 更新等级定义 |
| GET | `/v1/aip/maturity/capabilities` | 列出能力满足情况 |
| POST | `/v1/aip/maturity/capabilities` | 注册/更新能力 |
| POST | `/v1/aip/maturity/assess` | 触发评估 |
| GET | `/v1/aip/maturity/assessments` | 历史评估 |
| GET | `/v1/aip/maturity/target` | 当前目标等级 |
| POST | `/v1/aip/maturity/target` | 设置目标等级 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., aip_extras, ...)
application.include_router(aip_extras.router)
```

### 5.2 与 Logic 引擎协同

- `DebuggerEngine.step_forward` 简化版不实际调用 Logic 引擎；后续可扩展为真实调用
- `AutomateEngine.fire` 简化版不实际执行 Logic；后续可扩展

### 5.3 与 W2-T/W2-U 协同

- `MaturityEngine` 的能力清单可包括：`llm_gateway`（W2-T）、`prompt_engineering`（W2-U）、`failover`/`circuit_breaker`（W2-T）等

---

## 6. 测试计划

文件：`tests/test_aip_extras.py`（新增，约 40 个用例）

### 6.1 DebuggerEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | create_session | 返回带 id 的会话 |
| 2 | get_session 未找到 | 抛 NOT_FOUND |
| 3 | list_sessions 按 logic_id 过滤 | 仅返回匹配项 |
| 4 | step_forward 第一步 | current_step=1，step.completed |
| 5 | step_forward 到末尾 | session.status=completed |
| 6 | step_forward 已完成会话 | 抛 SESSION_COMPLETED |
| 7 | step_backward | current_step 减 1 |
| 8 | step_backward 已在开头 | 抛 AT_BEGINNING |
| 9 | run_to_completion | status=completed |
| 10 | preview_proposal | 返回 ProposalPreview，applied=False |
| 11 | list_proposals | 列表 |
| 12 | apply_proposal | applied=True |
| 13 | apply_proposal 已应用 | 抛 ALREADY_APPLIED |
| 14 | preview 多条变更 | changes 列表完整 |

### 6.2 AutomateEngine（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | upsert_trigger 新增 | 返回带 id |
| 2 | get_trigger 未找到 | 抛 NOT_FOUND |
| 3 | list_triggers enabled_only | 过滤 disabled |
| 4 | delete_trigger | 删除成功 |
| 5 | evaluate 条件满足 | True |
| 6 | evaluate 条件不满足 | False |
| 7 | fire 成功 | status=completed，trigger_count+1 |
| 8 | fire disabled | 抛 AUTOMATE_DISABLED |
| 9 | fire cooldown 中 | 抛 IN_COOLDOWN |
| 10 | fire 条件不满足 | 抛 CONDITION_NOT_MET |
| 11 | list_runs | 列表 |
| 12 | get_run 未找到 | 抛 NOT_FOUND |
| 13 | fire 多次 trigger_count 累计 | 计数正确 |

### 6.3 MaturityEngine（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | list_levels | 返回 L1~L4 |
| 2 | get_level L2 | 返回 L2 定义 |
| 3 | get_level 未找到 | 抛 NOT_FOUND |
| 4 | upsert_level 更新 | 修改后 get 返回新值 |
| 5 | register_capability | capabilities 含新能力 |
| 6 | list_capabilities | 返回字典 |
| 7 | assess 全部满足 → L4 | current_level=L4 |
| 8 | assess 仅 L1 满足 | current_level=L1 |
| 9 | assess 部分 | current_level=最高满足 |
| 10 | assess gaps | 包含缺失能力 |
| 11 | assess recommendation | 文案非空 |
| 12 | set_target_level + get_target_level | 读写一致 |
| 13 | list_assessments | 历史评估列表 |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 调试器不实际调用 Logic | 简化版仅记录变量流转；真实调用留作扩展 |
| Automate fire 失败影响生产 | 简化版不实际执行 Logic；返回 AutomateRun 记录便于审计 |
| 成熟度评估主观 | 基于 capability 清单客观计算；capability 可由管理员注册 |
| 持久化数据膨胀 | CallRecord/AutomateRun/MaturityAssessment 各保留最近 200 条 |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-v-aip-extras.md` | 新建 | 本文档 |
| `aos-platform/services/aos-api/aos_api/aip_extras.py` | 新建 | 3 引擎 + 单例 |
| `aos-platform/services/aos-api/aos_api/routers/aip_extras.py` | 新建 | ~26 个端点 |
| `aos-platform/services/aos-api/tests/test_aip_extras.py` | 新建 | ~40 测试 |
| `aos-platform/services/aos-api/aos_api/main.py` | 修改 2 行 | import + include_router |
| `docs/palantier/20_tech/220plan-分阶段开发与里程碑计划.md` | 更新 | v3.4 → v3.5，标记 #78/#79/#80 ✅ |

---

## 9. 验收标准

1. ✅ 所有 ~40 个单测全绿
2. ✅ 全量回归无新增失败（pre-existing wiki flaky 不计）
3. ✅ `main.py` 启动无报错，新路由 `/v1/aip/debugger/*` `/v1/aip/automate/*` `/v1/aip/maturity/*` 可访问
4. ✅ 方案文档与代码字段一致
5. ✅ 看板进度从 47/166 → 50/166，全局 93 → 96 / 259
