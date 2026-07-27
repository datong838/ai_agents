# 220tech · W2-W · L4 自动化收尾组（#82 / #83 / #86）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §6 #82/#83/#86 + §10（L4 熔断/模型预热/三种提案通道）
> - 技术方案 [T07](./T07-AIP人工智能平台详细技术方案.md) §3.3（模型预热）· §6.1（L4 熔断）
> - 产品方案 [07](../07-AIP引擎k-LLM与AgentStudio产品方案.md) §6.4（提案通道）· §6.3（L4）
> - 上游 W2-T FailoverEngine · W2-V MaturityEngine/AutomateEngine
> **范围**：W2-W 收口 L4 全自动态三件 — L4 熔断降级（失败率>5%）· 模型预热（warm-up/冷启动）· 三种提案通道（同步/异步 Automate/异步管道）
> **不替换底层**：本组复用 W2-T FailoverEngine 的 CallRecord 与 W2-V MaturityEngine 的等级定义，仅扩展 L4 监控与提案分发

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/l4_automation.py` + `aos_api/routers/l4_automation.py` + `tests/test_l4_automation.py`；`main.py` 加 2 行 |
| 不影响已有功能 | L4 熔断只读 W2-T CallRecord；模型预热只增预热状态；提案通道只增分发路由 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 符合方案军规 | 失败率>5% 降级 L3 与 T07 §6.1 一致；预热状态与 T07 §3.3 一致；三通道与 220w §6.3 一致 |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| L4 熔断 | W2-T FailoverEngine 有 closed/open/half_open 单链路熔断；无跨链路失败率监控与 L4→L3 降级 | 🔴 缺 |
| 模型预热 | LLM 网关冷启动直接调用；无 warm-up；无 UI 预热状态 | 🔴 缺 |
| 提案通道 | W2-V Automate 有 proposal_id 关联；Drafts 基础通道已有；无三通道分发与默认暂存策略 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #82 L4 熔断：滑动窗口失败率监控 + 自动降级 L3 + 停 auto_apply + Lineage 告警
  - #83 模型预热：模型预热状态机（cold/warming/ready/failed）+ warm-up 探测 + UI 状态查询
  - #86 三种提案通道：sync / async_automate / async_pipeline 三通道 + 默认暂存 + 审批台查询 + 24h 安全窗口
- ❌ 本组不做：
  - FailoverEngine 本身（属 W2-T）
  - LLM 网关真实 warm-up 调用（简化版仅状态机）
  - Drafts 实际写回（属 W1）
  - Lineage 实际入库（仅 emit 事件记录）

---

## 2. 数据模型

### 2.1 #82 L4 熔断

```python
class L4CircuitConfig(BaseModel):
    """L4 熔断配置。"""
    window_size: int = 100           # 滑动窗口大小
    failure_threshold: float = 0.05  # 失败率阈值 5%
    cooldown_seconds: float = 60.0   # 降级后冷却期
    auto_degrade_to: str = "L3"      # 降级目标等级


class L4CircuitState(BaseModel):
    """L4 熔断状态。"""
    current_level: str = "L4"        # L4 / L3
    window_failures: int = 0
    window_total: int = 0
    failure_rate: float = 0.0
    last_degraded_at: float = 0.0
    last_recovered_at: float = 0.0
    degraded: bool = False


class L4Alert(BaseModel):
    """L4 告警记录（替代 Lineage 入库）。"""
    id: str
    timestamp: float
    type: str                        # degrade / recover / threshold_exceeded
    message: str
    failure_rate: float = 0.0
    level: str = "L4"
```

### 2.2 #83 模型预热

```python
class WarmupState(BaseModel):
    """模型预热状态。"""
    model_id: str
    state: str = "cold"              # cold / warming / ready / failed
    last_warmup_at: float = 0.0
    last_ready_at: float = 0.0
    last_failed_at: float = 0.0
    failure_count: int = 0
    cooldown_until: float = 0.0
    metadata: dict[str, Any] = {}


class WarmupProbeResult(BaseModel):
    """预热探测结果。"""
    model_id: str
    success: bool
    duration_ms: int = 0
    error: str = ""
    timestamp: float = 0.0
```

### 2.3 #86 三种提案通道

```python
class ProposalChannel(BaseModel):
    """提案通道定义。"""
    type: str                        # sync / async_automate / async_pipeline
    name: str
    description: str = ""
    enabled: bool = True


class ProposalSubmission(BaseModel):
    """提案提交记录。"""
    id: str
    channel: str                     # sync / async_automate / async_pipeline
    logic_id: str
    payload: dict[str, Any] = {}
    status: str = "pending"          # pending / running / completed / failed / cancelled
    submitted_by: str = ""
    submitted_at: float = 0.0
    completed_at: float = 0.0
    visible_until: float = 0.0       # 24h 安全窗口截止时间
    approval_status: str = "pending" # pending / approved / rejected
    approved_by: str = ""
    approved_at: float = 0.0
    error: str = ""


DEFAULT_CHANNELS = {
    "sync": ProposalChannel(
        type="sync", name="同步通道",
        description="Logic 直接嵌 Workshop，结果即时回写",
    ),
    "async_automate": ProposalChannel(
        type="async_automate", name="异步 Automate 通道",
        description="Automate 触发，结果入 Draft 待审批",
    ),
    "async_pipeline": ProposalChannel(
        type="async_pipeline", name="异步管道通道",
        description="Pipeline 批处理，结果入 Draft 待审批",
    ),
}
```

---

## 3. 引擎设计

文件：`aos_api/l4_automation.py`（新增，3 个引擎）

### 3.1 L4CircuitEngine（#82）

```python
class L4CircuitEngine:
    def get_config(self) -> L4CircuitConfig: ...
    def update_config(self, cfg: L4CircuitConfig) -> L4CircuitConfig: ...
    def get_state(self) -> L4CircuitState: ...
    def record_call(self, success: bool) -> L4CircuitState: ...
    """记录一次调用结果，更新滑动窗口，触发降级/恢复评估"""
    def force_degrade(self, reason: str = "manual") -> L4Alert: ...
    """手动强制降级（演练用）"""
    def force_recover(self) -> L4Alert: ...
    """手动恢复"""
    def list_alerts(self, limit: int = 50) -> list[L4Alert]: ...
    def reset(self) -> None: ...
```

**record_call 流程**：
1. 把 success 推入滑动窗口（保留最近 window_size 条）
2. 计算 failure_rate = failures / total
3. 若 failure_rate > threshold 且未降级 → 触发 degrade：current_level=L3，停 auto_apply，emit L4Alert(type=degrade)
4. 若 failure_rate <= threshold/2（滞回）且已降级且 cooldown 已过 → 触发 recover：current_level=L4，emit L4Alert(type=recover)

### 3.2 ModelWarmupEngine（#83）

```python
class ModelWarmupEngine:
    def register_model(self, model_id: str, metadata: dict[str, Any] = {}) -> WarmupState: ...
    def get_state(self, model_id: str) -> WarmupState: ...
    def list_states(self) -> list[WarmupState]: ...
    def warmup(self, model_id: str, probe_callable: Callable[[], bool] | None = None) -> WarmupProbeResult: ...
    """执行预热探测：cold→warming→ready/failed；失败累计 cooldown"""
    def mark_ready(self, model_id: str) -> WarmupState: ...
    """直接标记就绪（外部探测器）"""
    def mark_failed(self, model_id: str, error: str = "") -> WarmupState: ...
    def remove_model(self, model_id: str) -> bool: ...
    def list_probe_results(self, model_id: str | None = None, limit: int = 50) -> list[WarmupProbeResult]: ...
```

**warmup 流程**：
1. 取模型状态，若 cooldown 未过抛 `IN_COOLDOWN`
2. 状态转 warming
3. 调用 probe_callable（默认返回 True，可注入真实 LLM 探测）
4. 成功 → state=ready，记录 last_ready_at
5. 失败 → state=failed，failure_count++，cooldown_until = now + 退避（5s × count）

### 3.3 ProposalChannelEngine（#86）

```python
class ProposalChannelEngine:
    def list_channels(self) -> list[ProposalChannel]: ...
    def get_channel(self, channel_type: str) -> ProposalChannel: ...
    def upsert_channel(self, channel: ProposalChannel) -> ProposalChannel: ...
    def submit(
        self, channel: str, logic_id: str, payload: dict[str, Any],
        submitted_by: str = "", visibility_hours: float = 24.0,
    ) -> ProposalSubmission: ...
    """提交提案到指定通道：sync 立即 completed；async_* 入 pending（待审批）"""
    def get_submission(self, submission_id: str) -> ProposalSubmission: ...
    def list_submissions(
        self, channel: str | None = None, status: str | None = None,
        approval_status: str | None = None, include_expired: bool = False,
    ) -> list[ProposalSubmission]: ...
    def approve(self, submission_id: str, approver: str) -> ProposalSubmission: ...
    def reject(self, submission_id: str, approver: str, reason: str = "") -> ProposalSubmission: ...
    def cancel(self, submission_id: str) -> ProposalSubmission: ...
    def cleanup_expired(self) -> int: ...
    """清理 visible_until 已过且未审批的提案（标记 cancelled）"""
```

**submit 流程**：
1. 校验 channel 存在且 enabled，否则抛 `INVALID_CHANNEL` / `CHANNEL_DISABLED`
2. 校验 logic_id 非空，否则抛 `INVALID_LOGIC_ID`
3. 创建 ProposalSubmission，visible_until = now + visibility_hours*3600
4. 若 channel=sync → status=completed, approval_status=approved, completed_at=now（同步通道即时完成）
5. 若 channel=async_* → status=pending, approval_status=pending（待审批台处理）

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，200 条上限防膨胀（alerts/probe_results/submissions）

---

## 4. API 设计

文件：`aos_api/routers/l4_automation.py`（新增）

### 4.1 #82 L4 熔断

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/l4-circuit/config` | 获取配置 |
| POST | `/v1/aip/l4-circuit/config` | 更新配置 |
| GET | `/v1/aip/l4-circuit/state` | 当前状态 |
| POST | `/v1/aip/l4-circuit/record-call` | 记录一次调用结果 |
| POST | `/v1/aip/l4-circuit/force-degrade` | 手动降级（演练） |
| POST | `/v1/aip/l4-circuit/force-recover` | 手动恢复 |
| GET | `/v1/aip/l4-circuit/alerts` | 告警历史 |

### 4.2 #83 模型预热

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/aip/warmup/models` | 注册模型 |
| GET | `/v1/aip/warmup/models` | 列出预热状态 |
| GET | `/v1/aip/warmup/models/{model_id}` | 单条状态 |
| POST | `/v1/aip/warmup/models/{model_id}/warmup` | 执行预热探测 |
| POST | `/v1/aip/warmup/models/{model_id}/mark-ready` | 标记就绪 |
| POST | `/v1/aip/warmup/models/{model_id}/mark-failed` | 标记失败 |
| DELETE | `/v1/aip/warmup/models/{model_id}` | 移除模型 |
| GET | `/v1/aip/warmup/probe-results` | 探测历史 |

### 4.3 #86 三种提案通道

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/proposal-channels` | 列出通道 |
| GET | `/v1/aip/proposal-channels/{type}` | 单条通道 |
| POST | `/v1/aip/proposal-channels` | 新增/更新通道 |
| POST | `/v1/aip/proposals` | 提交提案 |
| GET | `/v1/aip/proposals` | 列表（支持 channel/status/approval 过滤） |
| GET | `/v1/aip/proposals/{id}` | 单条提案 |
| POST | `/v1/aip/proposals/{id}/approve` | 审批通过 |
| POST | `/v1/aip/proposals/{id}/reject` | 审批驳回 |
| POST | `/v1/aip/proposals/{id}/cancel` | 取消 |
| POST | `/v1/aip/proposals/cleanup-expired` | 清理过期提案 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., l4_automation, ...)
application.include_router(l4_automation.router)
```

### 5.2 与 W2-T/W2-V 协同

- `L4CircuitEngine` 与 W2-T `FailoverEngine` 互补：FailoverEngine 管单链路熔断；L4CircuitEngine 管跨链路失败率与 L4→L3 降级
- `L4CircuitEngine.force_degrade` 与 W2-V `MaturityEngine.set_target_level` 联动：降级时 current_level=L3，可同步 register_capability("auto_apply", False)
- `ProposalChannelEngine` 与 W2-V `AutomateEngine.fire` 互补：Automate 触发产生提案后，可走 async_automate 通道提交到审批台

### 5.3 与 T-API 对齐

- 失败率>5% 返回 `CIRCUIT_OPEN` 503（T-API §1）
- L4 降级徽标在 aip-maturity.html 显示（前端联动，本组仅提供 API）

---

## 6. 测试计划

文件：`tests/test_l4_automation.py`（新增，约 42 个用例）

### 6.1 L4CircuitEngine（15）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | get_config 默认 | window_size=100, threshold=0.05 |
| 2 | update_config | 修改后 get 返回新值 |
| 3 | get_state 初始 | current_level=L4, degraded=False |
| 4 | record_call 单次成功 | total=1, failures=0, rate=0.0 |
| 5 | record_call 单次失败 | failures=1, rate=1.0 |
| 6 | record_call 滑动窗口溢出 | 保留最近 N 条 |
| 7 | 触发降级（>5%） | current_level=L3, degraded=True, alert type=degrade |
| 8 | 降级后稳定 | 持续失败不再 emit 重复 degrade alert |
| 9 | 滞回恢复（rate<=2.5% 且 cooldown 过） | current_level=L4, alert type=recover |
| 10 | 滞回未过 cooldown | 不恢复 |
| 11 | 滞回未达阈值 | 不恢复 |
| 12 | force_degrade | 立即降级 |
| 13 | force_recover | 立即恢复 |
| 14 | list_alerts | 列表非空 |
| 15 | reset | 清空状态 |

### 6.2 ModelWarmupEngine（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register_model | 返回 cold 状态 |
| 2 | get_state 未注册 | 抛 NOT_FOUND |
| 3 | list_states | 列表 |
| 4 | warmup 成功（默认 probe） | state=ready |
| 5 | warmup 失败（注入 probe=False） | state=failed, failure_count=1 |
| 6 | warmup 失败后 cooldown | IN_COOLDOWN |
| 7 | warmup 多次失败累加 | cooldown_until 增长 |
| 8 | mark_ready | 直接就绪 |
| 9 | mark_failed | 直接失败 |
| 10 | remove_model | 移除成功 |
| 11 | remove_model 未注册 | NOT_FOUND |
| 12 | list_probe_results | 列表 |
| 13 | warmup 未注册模型 | NOT_FOUND |

### 6.3 ProposalChannelEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | list_channels 默认 3 个 | sync / async_automate / async_pipeline |
| 2 | get_channel async_automate | 返回定义 |
| 3 | get_channel 未找到 | NOT_FOUND |
| 4 | upsert_channel 禁用 | enabled=False |
| 5 | submit sync 通道 | status=completed, approval=approved |
| 6 | submit async_automate | status=pending, approval=pending |
| 7 | submit async_pipeline | status=pending |
| 8 | submit 禁用通道 | CHANNEL_DISABLED |
| 9 | submit 未知通道 | INVALID_CHANNEL |
| 10 | submit logic_id 空 | INVALID_LOGIC_ID |
| 11 | approve | approval_status=approved |
| 12 | reject | approval_status=rejected |
| 13 | cancel | status=cancelled |
| 14 | cleanup_expired | 过期未审批的标记 cancelled |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| L4 熔断误触发 | 滞回阈值（rate<=2.5%）+ cooldown 60s 防抖动 |
| warmup 探测阻塞主流程 | probe_callable 可注入异步实现；默认同步返回 True |
| 提案审批台数据膨胀 | cleanup_expired 定期清理；submissions 保留 200 条 |
| 同步通道无审批风险 | sync 通道默认 approval=approved 即时完成；可选 disabled 关闭 |
| 24h 安全窗口跨时区 | visible_until 用 epoch 秒，UTC 一致 |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-w-l4-automation.md` | 新建 | 本文档 |
| `aos-platform/services/aos-api/aos_api/l4_automation.py` | 新建 | 3 引擎 + 单例 |
| `aos-platform/services/aos-api/aos_api/routers/l4_automation.py` | 新建 | ~24 个端点 |
| `aos-platform/services/aos-api/tests/test_l4_automation.py` | 新建 | ~42 测试 |
| `aos-platform/services/aos-api/aos_api/main.py` | 修改 2 行 | import + include_router |
| `docs/palantier/20_tech/220plan-分阶段开发与里程碑计划.md` | 更新 | v3.5 → v3.6，标记 #82/#83/#86 ✅ |

---

## 9. 验收标准

1. ✅ 所有 ~42 个单测全绿
2. ✅ 全量回归无新增失败（pre-existing wiki flaky 不计）
3. ✅ `main.py` 启动无报错，新路由 `/v1/aip/l4-circuit/*` `/v1/aip/warmup/*` `/v1/aip/proposal-channels/*` `/v1/aip/proposals/*` 可访问
4. ✅ 方案文档与代码字段一致
5. ✅ 看板进度从 50/166 → 53/166，全局 96 → 99 / 259
