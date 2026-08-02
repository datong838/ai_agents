# 228-电商增长参谋长 G6 受控生产 Action 与经营自动化实施方案

> 状态：方案稿 · C0.2 与 G0～G5 全部退出门关闭前禁止编码生产写回
> 版本：v1.0 · 2026-08-02
> 安全前置：[228-AIP 生产写回 C0 租户与审批安全闭环方案](../228-AIP生产写回C0租户与审批安全闭环方案.md)
> 上游：[G5 社交平台 Connector 与数字人直播](228-电商增长参谋长G5社交平台Connector与数字人直播实施方案.md)

---

## 0. 使用的 Rules

- GrowthPlan 批准不等于生产 Action 批准；每次外部副作用都必须形成独立 ActionProposal。
- Action 必须绑定不可变 plan/task/logic/tool/config/input revision 和 payload hash；批准后不得静默修改。
- 创建者、方案批准者、Action 批准者和高风险执行者按风险等级职责分离。
- 幂等、CAS、审计、配额、预算、补偿、kill switch、人工接管和状态查询先于任何正向写回。
- 外部超时是 `unknown`，不能盲目重试；先查远端状态再决定恢复。
- 先低风险、可逆、小流量、单租户灰度；支付、退款、库存、价格等高风险 Action 不纳入通用首波。
- Automation 只能引用已发布不可变对象与批准策略，不能运行任意脚本或绕过 Tool registry。

---

## 1. 目标与真实完成定义

G6 在 C0.2 完成后，把前五波的 Draft/人工流程升级为可控的生产执行：

```text
approved GrowthPlan revision
  → materialized AgentTask
  → approved Artifact/Draft
  → ActionProposal + exact payload hash
  → 风险评估与职责分离审批
  → reservation（预算/配额/幂等/并发）
  → trusted executor
  → provider receipt/status reconciliation
  → ExecutionObservation
  → EffectReview / compensation / incident
```

真实完成必须满足：

1. 未批准、批准过期、payload 改动、scope 不匹配或 C0.2 关闭时执行必然失败且无副作用。
2. 同一 Action 在客户端重试、队列重投和服务重启下最多产生一次外部语义效果。
3. 平台侧成功但本地超时可通过 reconcile 收敛，不重复执行。
4. 每次执行能还原 actor、审批、对象 revision、payload hash、adapter、回执、观察和复盘。
5. kill switch、预算/频控、人工接管和补偿均经过故障注入验证。
6. 首波只开放批准的低风险 Action；高风险类型保持拒绝并有负向测试。

---

## 2. 强制前置与当前阻断

编码正向执行前必须满足：

- [C0.2 生产写回安全闭环](../228-AIP生产写回C0租户与审批安全闭环方案.md)的租户、审批、幂等、审计与数据库真源门全部关闭。
- G0～G5 的 canonical 契约、Logic、Connector、Evals 和累计回归通过。
- trusted runtime adapter 显式注册，声明 side effect、风险、可逆性、超时和配额。
- router/OpenAPI 无重复路径/operationId；旧 Phase3 Draft 和内存路径已隔离。

当前代码中的 `aip_logic_engine` 自动构造 approved plan、进程内 idempotency、缺少租户的 Tool query、部分 L4 singleton 都不能进入生产执行链。

---

## 3. Action 风险分级

| 等级 | 示例 | 默认 | 审批/控制 |
|---|---|---|---|
| R0 | 读取状态、查询指标 | 可按现有只读策略 | 无生产副作用 |
| R1 | 创建平台 Draft、预约草稿 | 首批候选 | 单次 Action 审批、可撤回优先 |
| R2 | 正式发布内容、回复低风险评论 | 默认关闭，灰度 | 双人或策略审批、频控、reconcile |
| R3 | 私信/营销触达、直播播报 | 默认关闭 | consent、频控、实时接管、账号 kill switch |
| R4 | 价格、优惠券、库存、订单、退款、支付、赔付 | 通用 G6 禁止 | 后续专项、独立风控与业务授权 |

风险不是由前端或模型自行填报；服务端按注册的 ActionType policy 计算并取调用声明的更高值。

---

## 4. ActionProposal 契约

```yaml
action_proposal_id: ap_...
org_id: ...
project_id: ...
action_type: social.content.publish
risk_level: R2
plan_ref: {id: gp_..., revision: 3, hash: ...}
task_ref: {id: task_..., revision: 2}
logic_ref: {publication_id: ..., hash: ...}
artifact_ref: {id: asset_..., revision: 4, hash: ...}
connector_ref: {installation_id: ci_..., capability_snapshot_id: cap_...}
payload_hash: ...
requested_by: ...
expires_at: ...
status: draft|submitted|approved|reserved|executing|unknown|succeeded|failed|compensating|compensated|cancelled|expired
```

ActionProposal 不存 Secret；运行参数由 canonical refs 装配并重新计算 hash。批准事件保存批准人、scope、decision、reason、policy version、proposal revision/hash、时间和到期时间。

---

## 5. 审批与职责分离

```text
proposal submit
  → 服务端 risk/policy evaluation
  → required approver set
  → exact revision/hash approval
  → expiry + prerequisite recheck
  → reservation
```

- 创建人不能批准自己的 R2/R3；R3 至少需要业务 owner 与安全/运营授权组合。
- GrowthPlan approval 证明方向获批，不替代具体内容、账号、时间和 payload 的 Action approval。
- 批准后任何 payload、账号、capability、Logic publication、素材或 consent 变化都使批准失效。
- 批量 Action 每项保留独立 hash/状态；不能用一次模糊批准覆盖无限目标。
- 紧急停用无需原批准人同意；恢复必须有新审批和事件复盘。

---

## 6. 幂等、并发与状态对账

### 6.1 本地幂等

唯一键包含 `org/project/action_type/idempotency_key`；幂等记录持久化并保存 request hash、proposal ref、result ref、状态和 TTL。相同 key 不同 hash 返回冲突。

### 6.2 执行租约

worker 通过数据库 CAS 从 `approved` 获取 reservation/lease；lease 有 owner、epoch、expires_at 和 heartbeat。只有当前 epoch 可提交结果，避免旧 worker 覆盖。

### 6.3 外部未知态

```text
invoke timeout/network break
  → mark unknown
  → query provider by request token/idempotency token
  → confirmed success / confirmed absence / still unknown
  → only confirmed absence may retry under same semantic key
```

没有可靠查询/幂等能力的平台写操作不得自动重试，只能转人工核验。

---

## 7. Tool/Connector 执行门

每个生产 adapter 注册：

```yaml
action_type: social.content.publish
side_effect: true
read_only: false
risk_level: R2
reversible: conditional
supports_idempotency: true|false
supports_status_query: true|false
supports_compensation: true|false
timeout_ms: ...
max_concurrency: ...
budget_bucket: ...
```

Runtime 只接受 ActionExecutionToken，不接受前端直接传 `approved=true`。Token 由服务端短期签发，绑定 tenant、proposal revision/hash、adapter、attempt、deadline 和 nonce，并只能使用一次。

---

## 8. 预算、配额、频控与 kill switch

- 全局、租户、项目、账号、ActionType、campaign、customer purpose 多层预算/频控取最严格值。
- reservation 在执行前扣占，确定失败释放，成功结算，unknown 保持占用直到对账/过期人工处理。
- kill switch 层级：全平台、provider、connector installation、ActionType、tenant/project、campaign/live session。
- kill switch 检查必须在 proposal、reserve、invoke 三个阶段执行；队列中已批准任务也会被阻断。
- 超阈值错误、投诉、撤回、延迟或未知态自动开闸停止新 Action，并通知人工。

---

## 9. 补偿、撤回与事故

- 补偿是独立 ActionProposal，不是假装数据库回滚能撤销外部世界。
- 内容撤回、删除、纠正、停播等只有 provider 支持且经审批才执行。
- 不可逆 Action 失败时记录 incident、影响范围、人工处置和客户补救，不伪造 compensated。
- 原 Action 与 compensation 双向引用；补偿失败继续保持 incident open。
- 事故证据脱敏，保留外部回执、时间线、policy/adapter version 和 operator 决策。

---

## 10. Automation 安全模型

Automation 只允许绑定：

- immutable GrowthPlan/Logic publication/ActionPolicy revision；
- 明确 trigger、时间窗、输入 schema、最大运行次数、预算和 expiry；
- 允许的 Task/ActionType 白名单；
- 每次 Action 是否仍需人工审批；
- kill switch、人工 owner、回滚/补偿与观测指标。

禁止：任意 Python/SQL/Shell、动态下载代码、自动扩大 scope、自动批准自己、从记忆内容生成新权限、无限循环和无预算触达。

Automation 状态为 `draft → evaluated → approved → active → paused|expired|revoked`；版本变化必须重新评测和批准。

---

## 11. API 建议

```text
POST   /v1/growth/actions
GET    /v1/growth/actions/{id}
POST   /v1/growth/actions/{id}/submit
POST   /v1/growth/actions/{id}/approve
POST   /v1/growth/actions/{id}/reject
POST   /v1/growth/actions/{id}/cancel
POST   /v1/growth/actions/{id}/reconcile
POST   /v1/growth/actions/{id}/compensations
POST   /v1/growth/action-policies
POST   /v1/growth/automations
POST   /v1/growth/automations/{id}/evaluate
POST   /v1/growth/automations/{id}/approve
POST   /v1/growth/automations/{id}/activate
POST   /v1/growth/automations/{id}/pause
POST   /v1/growth/kill-switches
DELETE /v1/growth/kill-switches/{id}
```

Action/Automation/kill switch 均须 Principal、roles、markings、幂等、revision/hash 与审计。解除 kill switch 是高权限写操作，不能用普通 DELETE 无条件执行，API 实现需提交解除理由和 expected revision。

---

## 12. 计划新增/修改文件

```text
services/aos-api/aos_api/actions/
  contracts.py
  policy_registry.py
  proposal_store.py
  approval_service.py
  idempotency_store.py
  reservation_service.py
  execution_token.py
  executor.py
  reconciliation_service.py
  compensation_service.py
  kill_switch_service.py
services/aos-api/aos_api/automation/
  contracts.py
  store.py
  evaluator.py
  scheduler.py
services/aos-api/aos_api/routers/
  growth_actions.py
  growth_automations.py
  growth_kill_switches.py

services/aos-api/alembic/versions/
  228growth6_actions_automation.py

apps/web/src/pages/s2/growth/actions/
  ActionApprovalQueue.tsx
  ActionDetailPage.tsx
  ActionReconciliationPanel.tsx
  KillSwitchConsole.tsx
apps/web/src/pages/s2/growth/automation/
  AutomationEditor.tsx
  AutomationRunHistory.tsx
```

Action 核心、Automation、前端审批/控制台和 provider adapter 可并行，但公共 contract、policy registry、迁移 head 和 OpenAPI 由单一集成 owner 管理。

---

## 13. 分小波实施

| 小波 | 内容 | 退出门 |
|---|---|---|
| G6.0 | C0.2 回读、威胁建模、ActionType 清单 | 所有前置证据齐全，高风险明确禁止 |
| G6.1 | Proposal/approval/persistent idempotency/audit | 双租户、职责分离、hash/expiry/CAS 通过 |
| G6.2 | reservation/executor/reconcile/kill switch | 重启、重复、断网、unknown、开闸故障注入通过 |
| G6.3 | R1 单租户 canary | 最多一次语义效果、回执、撤回/补偿通过 |
| G6.4 | 获批 R2 小流量 | 预算/频控/投诉门、人工接管、事故演练通过 |
| G6.5 | Automation（仍按 Action 门） | trigger/revision/预算/暂停/过期/重放通过 |

R3 及以上不因 G6.5 自动开放，必须有独立专项方案、平台能力和业务授权。

---

## 14. 测试、灰度与回滚

必须测试：

- 状态机、hash、expiry、policy、职责分离、幂等冲突、lease epoch、预算结算。
- 双租户同 ID、越权批准、marking、撤回 approval、kill switch 竞态。
- worker 崩溃、服务重启、队列重复、429/5xx、超时 unknown、平台成功本地失败。
- provider 不支持幂等/查询/补偿时的人工恢复。
- 浏览器：proposal → diff/风险 → 审批 → 执行 → 回执 → reconcile → review/incident。
- G0～G6 API/Web/OpenAPI/Logic/Evals/Connector 累计回归。
- R4 高风险类型必须持续返回 policy denial，外部调用计数为 0。

灰度顺序：内部测试租户 → 单账号 R1 → 单一 R2 ActionType 小流量 → 扩租户；每步设错误率、unknown、投诉、重复、延迟和预算阈值。任一越线自动关闭相应 kill switch。

回滚先停新 Action，再 reconcile in-flight/unknown，最后关闭功能；不能删除审计、批准、回执和 incident。数据库 downgrade 只有在无 Action/Automation 数据且无后续迁移时允许。

---

## 15. 最终退出门

G6 及整个通用电商增长闭环完成，需要同时满足：

1. C0.2 和 G0～G5 所有退出门有可回读证据。
2. 方案审批与 Action 审批真正分离，精确 revision/hash 不可绕过。
3. 幂等、unknown 对账、kill switch、补偿和人工接管通过故障注入。
4. 首批允许 Action 清单与禁止清单已冻结；R4 保持禁用。
5. 每阶段专项测试、累计回归和浏览器主链路全部通过。
6. 执行、结果、复盘和记忆候选形成闭环，但任何学习都不自动扩大权限。

未满足任一项，都只能保持 Draft/人工执行模式，不能宣称经营自动化已完成。
