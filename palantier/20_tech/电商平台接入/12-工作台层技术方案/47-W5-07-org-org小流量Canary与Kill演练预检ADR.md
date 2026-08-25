# W5-07 `org-org/dev-project` 小流量 Canary 与 Kill 演练预检 ADR

> 日期：2026-08-14
> 核查基线：Workshop `w2-workshop@b37252d`，authority `AOS-000026`
> 状态：`PREFLIGHT_COMPLETED / PROTOCOL_BASELINE_APPROVED / REAL_CANARY_BLOCKED`
> 边界：只读代码、专项测试与协议整改；未读取或修改真实租户，未调用外部 Provider，未执行迁移或真实 Canary

## 1. 结论

现有 Action 底座已在 Lease 获取前和 Adapter 调用前复验通用 kill，并具备平台环境开关、组织/项目/ActionType guardrail 与跨租户失败关闭；两项专项测试 GREEN。但是 W5-00～W5-06 均未达到实现 GREEN，生产代码中没有任何 `ACTION_ADAPTERS.register`，也没有精确到账号、Adapter revision、CapabilityBinding、预算与时窗的用户授权。因此本波只批准 Canary 协议与 Kill 演练门禁设计，明确禁止真实执行。

`org-org/dev-project` 是唯一真实目标；`dev-org/dev-project` 只用于负向隔离验证，不能作为真实成功证据。

## 2. 开工硬门

真实 Canary 必须同时满足：

1. W5-00～W5-06 及所选 Adapter capability 分别 GREEN，不以累计测试或静态检查替代；
2. 用户单独批准一份不可歧义的 Canary Receipt，固定 ActionType revision、Capability/Binding、Account、Adapter revision、对象、最大数量、预算、时窗、操作者、审批人和停止条件；
3. 候选动作属于 allowlist 中可逆或无害的单对象 R2，批量、公开商业配置、退款、支付、库存、发货、调价持续 disabled；
4. `dryValidate → ImpactPreview → Proposal → Approval → Lease → Attempt → Receipt → Usage settlement → lineage → provider reread` 可在同一 `actionBindingHash` 上回读；
5. unknown、Webhook gap、签名失败、预算漂移、settlement 超时、lineage 冲突和补偿路径都有已演练的停止/处置规则。

缺任一项即 `blocked_dependency`，不得把“账号已登录”“接口 HTTP 2xx”“页面 toast”或旧环境成功当作放行依据。

## 3. Kill authority

Kill 不是一个可随意编辑的布尔值。发布 `KillPolicyRevision`，按平台、组织、项目、账号、Adapter revision、CapabilityBinding、ActionType 分层求最严格结果；变更必须 CAS、maker-checker、有效期与不可变 Receipt。执行链在 Preview、submit、Approval、Lease、dispatch 前分别固定或复验 exact policy revision。

`ActionExecutionAttempt` 在 Provider I/O 前持久化 dispatch fence。Kill 生效后：

- 尚未 dispatch 的新 Attempt 必须失败关闭并释放 reservation；
- 已 dispatch 的 Attempt 不声称已被撤销，进入 provider reread/reconcile；
- unknown 不盲重试，补偿只按 W5-05 的版本化 CompensationPolicy 重新审批；
- reset 需要新的双人审批和 Receipt，不覆盖原 Kill 事件。

## 4. 小流量 Canary 协议

CanaryPlan 固定唯一 `org-org/dev-project`、一个账号、一个 Adapter、一个 ActionType、一个对象或极小批次、最大预算与短时窗。执行前生成 EvidencePack，记录 capability conformance、Preview diff、账号权限、quota、recipient allowlist、无害测试对象、kill propagation 目标和补偿/对账责任人。

执行期间同时观察 Attempt/dispatch、provider outcome、Webhook backlog/gap、unknown age、Usage reservation/settlement、lineage projection、错误率和 kill propagation。任何 binding/policy drift、超预算、签名或顺序异常、unknown 超 SLA、跨租户可见性、无法回读最终事实立即停止扩大流量并进入处置。

Canary 成功只证明该 exact binding 在该时窗的低流量证据，不自动提升其他账号、Adapter、ActionType、批量规模或风险等级。

## 5. Kill 演练

`KillDrillPlan` 必须至少验证：

1. 预先 arm 平台、租户、账号、Adapter 与 ActionType 多层 kill，并记录传播基线；
2. 触发一个精确 scope 的 kill 后，新 dispatch 全部被拒绝，UI 展示 reasonCode 与恢复路径；
3. 已在途 Attempt 被列入 reconcile，不被伪装成取消成功；
4. reservation、Usage、Webhook、lineage 和 ManualReconcileCase 完成守恒核对；
5. reset 经新审批恢复，旧 Proposal/Approval/Lease 不因 reset 自动复活。

演练产出不可变 KillDrillReceipt，固化 policy revisions、触发者/审批者、计划与实际传播时延、被阻断 Attempt、在途处置、最终对账和 reset refs。

## 6. 退出门

W5-07 只有在真实 Canary 获得单独授权并完成后才可勾选。GREEN 证据至少包括：

- W5-00～W5-06 独立 Delivery Receipts；
- exact CanaryPlan/Approval/Lease/Attempt/ActionReceipt/Usage/lineage/provider reread；
- KillDrillReceipt 与传播、在途、reset 证据；
- `dev-org/dev-project` 负向隔离 0 泄漏；
- 用户对 exact 结果与剩余风险的显式验收。

当前机器证据见 `.evidence/workshop/2026-08-14-w5-07-real-canary-kill-preflight.json`。它只冻结预检事实，不是执行授权。

## 7. 2026-08-25 零副作用控制面实施切片

本轮承接 `m1@ad26cd4` 与 authority `AOS-000241`。W5-00～W5-06 的代码控制面与独立 Delivery Receipt 已闭合，但真实 Adapter 注册、账号 Secret、独立 Canary 授权和外部动作仍不存在。因此本切片只关闭能够由代码与测试证明的 authority/dispatch-fence/drill-simulation 缺口；不会伪造真实 Canary GREEN，也不会以单开发者授权替代第 2、6 节的 exact 真实副作用门。

文件级清单：

- [ ] `services/aos-api/alembic/versions/w5_006_action_canary_kill_control.py`：新增 append-only `KillPolicyRevision`、mutable CAS head、maker-checker approval、immutable command receipt、exact `CanaryPlanRevision/Approval`、`KillDrillPlanRevision/Receipt`；所有 tenant 表 RLS，事实存在时降级失败关闭。
- [ ] `services/aos-api/aos_api/aip_action_canary_models.py` 与 `aip_action_canary_service.py`：Kill revision 只能通过 expected head version + idempotency 建议；另一主体审批后才生效；reset 必须是新 revision。按 platform/org/project/account/adapter/capability/action type 求最严格 exact policy，expiry 后不放大权限。
- [ ] `services/aos-api/aos_api/aip_action_execution.py`：在 exact binding 解析后、Attempt/outbox 持久化前复验 canonical Kill policy；被 kill 的新 dispatch 不创建 Attempt，已存在 dispatch_claimed/accepted/unknown 只进入 reconcile 处置，不声称取消或自动补偿。旧 `aip_action_guardrail` 与环境 kill 保持兼容，canonical policy 作为加法约束。
- [ ] `services/aos-api/aos_api/routers/aip_action_canary.py` 与 `routers/domain_aggregates.py`：提供 Principal-scoped Kill proposal/approval/effective read、Canary plan proposal/approval 和 zero-side-effect drill simulation；API 不提供“跳过审批”“真实执行 canary”或 Secret/Provider 参数。
- [ ] `services/aos-api/tests/aip/test_w5_07_action_canary_kill_control.py` 与迁移测试：覆盖 CAS、幂等漂移、maker-checker、reset 新 revision、多层最严格、exact binding mismatch、expiry、dispatch fence、in-flight reconcile、跨租户 0 可见及 simulation Receipt 守恒。
- [ ] `packages/contracts/openapi/v1.generated.json`、`v1.inventory.json` 与 `.evidence/workshop/2026-08-25-w5-07-action-canary-kill-control.json`：封存专项、W5 累计、compileall、Alembic、diff 与浏览器裁决；若不改页面，浏览器记 `N/A_NO_UI_CHANGE`，不得替代真实 Canary EvidencePack。

本切片完成后只能形成 `KILL_AUTHORITY_AND_ZERO_EFFECT_DRILL_CODE_GREEN / REAL_CANARY_BLOCKED`。只有第 6 节的 exact 真实链和用户结果验收完成，W5-07 主 Task 才能勾选；否则总清单必须把代码控制面进展与真实 Canary 缺口分轴记录。
