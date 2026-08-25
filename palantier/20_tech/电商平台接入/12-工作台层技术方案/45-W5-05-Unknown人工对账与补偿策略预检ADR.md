# W5-05 Unknown、人工对账与补偿策略预检 ADR

> 日期：2026-08-14
> 核查基线：Workshop `w2-workshop@a443532`，authority `AOS-000026`
> 状态：`IMPLEMENTATION_ACTIVE / W5_04_DEPENDENCY_GREEN / NO_EXTERNAL_EFFECT / NO_RELEASE`
> 边界：仅实施代码控制、迁移定义、专项测试与方案整改；不执行真实迁移，不读取真实账号/密钥，不调用外部 Provider，不触发租户业务写入或发布

## 1. 结论

现有控制骨架正确保留了三条原则：timeout 进入 unknown 且不自动补发；自动 reconcile 只读 Provider 并追加 Receipt；补偿创建新 Proposal 而不是改写历史。后端 10 项、前端 8 项专项测试 GREEN。

但当前实现把 Provider 最终 applied 和 failed 都包装成顶层 `reconciled`，补偿入口又把所有 reconciled Receipt 视为可补偿，存在对“确认未发生”的动作发起补偿的风险。没有 provider request id 时也没有人工对账 authority；页面所谓“手动只读对账”实际仍是自动 Adapter 回查。补偿 ActionType/payload 由调用者自由提供，未绑定受控逆操作策略。因此 W5-05 仍不能勾选。

## 2. Outcome 与 reconciliation 分轴

不要再用单个 `reconciled` 覆盖业务结果：

```text
providerOutcome: accepted | applied | failed | partial | unknown
reconciliationStatus: not_required | pending | automatic | manual | unresolved
settlementStatus: pending | settled | unknown | disputed
```

ReconcileReceipt 必须显式保存 `resolvedProviderOutcome`、quality、source、cutoff、原 Receipt/Attempt exact refs 和完整 hash。`automatic/manual` 说明结论如何取得，不代表 applied。补偿资格只读取 typed resolved outcome，禁止解析自由 payload 或凭顶层 reconciled 状态推断。

## 3. 自动对账

自动对账使用 durable `ReconcileAttempt`：固定原 Attempt/Receipt、Adapter revision、account、provider request/idempotency ref、request fingerprint、查询策略与 expiry。并发只允许一个 claim；进程崩溃后从 attempt 状态恢复，不重复创建结论。

- unknown 与 accepted 异步动作都可按 Adapter contract 进入 polling/callback reconcile；
- Provider 返回 applied/failed/partial 才追加终态 ReconcileReceipt；仍 pending 保持原 outcome，不伪装终态；
- 达到时限、查询不可用、结果冲突或缺稳定 ref 时转 ManualReconcileCase；
- 回查 API 本身有副作用或不支持稳定查询时，capability 必须标 manual/disabled。

## 4. ManualReconcileCase

人工对账不是让单个操作员填写“成功/失败”。Case 固化：

- 原 Proposal/Attempt/Receipt/actionBindingHash、账号、对象范围与预期 diff；
- Provider 工单、后台查询、业务对象读回、账单/消息/履约等受控 Evidence refs；
- required facts、marking、冲突/缺失项、最早/最晚事件时间；
- maker-checker、职责 slot、expiry 与 `confirmed_applied/confirmed_failed/confirmed_partial/unresolved` 决策。

人工结论产生 immutable ManualReconcileDecisionReceipt；证据不足保持 unresolved。紧急止损是新的独立 Action，不得把“先做反向动作”当作未知结果的补偿。

## 5. CompensationPolicy

补偿只针对 `confirmed_applied` 或可量化的 `confirmed_partial`。版本化 `CompensationPolicyRevision` 定义：

- original ActionType/outcome → allowed compensation ActionType/schema；
- 可逆范围、最大金额/数量、时间窗、账号与对象一致性；
- 已补偿量、剩余 effect、重复/叠加规则；
- 专用 ImpactPreview、风险下限、审批 slot、预算与 Adapter capability；
- 不可补偿时的人工 Case/告警路径。

Compensation Proposal 固定原 Proposal、Attempt、resolved outcome Receipt、policy revision、effect scope/delta 与 `actionBindingHash`，重新走 Preview→Approval→Lease→Receipt；调用者不能自由指定任意 ActionType/payload。原动作不改写为“没发生”，lineage 追加 `compensates` exact edge，并保留 residual effect。

## 6. UI

页面分别展示原 Provider outcome、自动/人工对账状态、证据充分性、补偿资格与 residual effect。缺 provider ref 时提供“创建人工对账 Case”，不是永久禁用；对账按钮显示自动查询或人工 Case，不能混称。只有服务端 `compensationReadiness=eligible` 才显示补偿入口，并先展示 policy、Impact 和审批链。

## 7. 验收

1. reconciled-applied 与 reconciled-failed typed outcome 不混淆；failed 绝不能补偿。
2. accepted/unknown 自动 polling、callback、并发与 crash 恢复均幂等，不重复 Provider 查询副作用。
3. 缺 provider ref、查询冲突、超期会创建 ManualReconcileCase；单人断言不能形成终态。
4. Evidence 不足保持 unresolved，未知期间无补发、无自动补偿。
5. CompensationType/payload/scope 由 exact policy 生成，重新经过完整 Action 安全链。
6. partial compensation 记录 applied delta、compensated delta 和 residual effect；重复申请失败关闭。
7. lineage 可追溯原动作、对账证据、结论、补偿 Proposal/Receipt 与残余影响。

机器证据见 `.evidence/workshop/2026-08-14-w5-05-unknown-reconcile-compensation-preflight.json`。

## 8. 2026-08-25 实施切片与文件级清单

本轮在 `m1@ecf3417`、authority `AOS-000239` 上承接 W5-04 durable Attempt/Receipt，保持既有内部 AIP-3B Action API 兼容，同时对 W5 external family 关闭自由补偿绕过。实现继续遵循“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图”：对账与补偿是 Action Logic 的受控后续步骤，其 Case、Evidence、Decision、Policy、Proposal 与 Receipt 都作为同一贡献链的 exact facts，不新增第二套业务 authority。

- [ ] `services/aos-api/alembic/versions/w5_004_action_reconcile_compensation.py`：新增 tenant-scoped `ReconcileAttempt`、`ManualReconcileCase`、immutable `ManualReconcileDecisionReceipt`、versioned `CompensationPolicyRevision` 与补偿 exact refs；所有结论、策略与历史 Receipt append-only，存在事实时降级失败关闭。
- [ ] `services/aos-api/aos_api/aip_action_execution.py`：unknown/accepted 只通过 durable reconcile claim 查询；applied/failed/partial 与 automatic/manual 分轴；缺稳定 ref、查询不可用/冲突/超期转 Manual Case，绝不补发原动作。
- [ ] `services/aos-api/aos_api/aip_action_models.py` 与 `routers/aip_actions.py`：公开 typed reconcile/manual case/decision/compensation readiness；人工结论要求 maker-checker、CAS、受控 Evidence，证据不足保持 unresolved。
- [ ] `services/aos-api/aos_api/aip_action_execution.py`：external compensation 只消费 exact policy revision，校验原 ActionType/outcome/effect scope、重复/残余量和联合 binding；由策略生成逆操作 Draft/Proposal，再走 Preview→Approval→Lease→Receipt，不接受调用者自由 ActionType/payload。
- [ ] `services/aos-api/tests/aip/test_w5_05_action_reconcile_compensation.py` 与迁移/相邻回归：覆盖 reconciled failed 不可补偿、accepted/unknown 并发幂等、无 provider ref 转 Case、单人断言拒绝、Evidence 不足 unresolved、exact policy/hash/outcome/scope、partial residual 与跨租户失败关闭。
- [ ] `packages/contracts/openapi/v1.generated.json`、`v1.inventory.json` 与 `.evidence/workshop/2026-08-25-w5-05-unknown-reconcile-compensation.json`：确定性导出并封存专项、累计、编译、Alembic、diff 证据；若本波无页面变化，浏览器明确记 `N/A_NO_UI_CHANGE`，不得以此代替后续 W5 累计页面验收。

本波代码 GREEN 仍不等于 operational GREEN：production Adapter/账号/预算 reservation、真实迁移、Canary、外部副作用与 release 保持 blocked。任何 provider 结果不确定、人工证据不足、policy/exact binding 漂移或 residual 不守恒都失败关闭。
