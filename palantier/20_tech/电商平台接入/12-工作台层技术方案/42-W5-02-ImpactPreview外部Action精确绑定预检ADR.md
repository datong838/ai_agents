# W5-02 ImpactPreview 外部 Action 精确绑定预检 ADR

> 日期：2026-08-14（2026-08-25 于 `m1` 开始实施）
> 核查基线：`m1@6185444`，authority `AOS-000236`
> 状态：`CODE_CONTROL_GREEN / EXACT_BINDING_PERSISTED / EXTERNAL_AUTHORITIES_BLOCKED / NO_RELEASE`
> 边界：已在 `m1` 完成模型、持久化、迁移资产与失败关闭回归；未对真实环境执行 migration，未读取真实账号或 Secret，未发放 Approval/Lease，未调用外部 Provider

## 1. 结论

W2-D 已形成可信的通用 Preview 基础：八维 impact 明确 measured/estimated/unknown，已知值必须带来源和 cutoff；Preview 冻结 exact Plan/Brief/Evidence/Eval/Responsibility/Stage refs，依赖快照在 freeze、approval、start 和 Action lease 前复验；W2-D3 strict SDK/UI 与真实租户空态失败关闭已经 GREEN。

但 W5-02 仍不能勾选。当前 `accountRef` 只完成 DTO，任何提供账号的 Preview 都以 `ACCOUNT_AUTHORITY_UNAVAILABLE` blocked；若省略 account/capability，Preview 又可能 ready。ActionProposal 只绑定 Preview ref，没有证明 ActionType、CapabilityBinding、账号、Adapter、风险和预算与 Preview 评估的是同一组 exact 依赖；历史兼容路径还允许无 Preview 的外部 Action 被审批和获取 Lease。

## 2. 两类门不能混用

- `ProductionStartDecision`：批准 canonical TaskRun 的受控创建；`started` 不等于 AgentRun、Provider 或外部 Action 已执行。
- `Action ExecutionLease`：在外部副作用前，批准某一 exact ActionProposal 使用同一账号、Adapter、预算与幂等 envelope 执行一次。

两者可以引用同一 Preview，但不能互相替代。启动 TaskRun 不授予外部发布、触达、履约或资金动作；获得 Action Lease 也不改变 Task/Run 编排真源。

## 3. W5 外部 Action 必需 Preview Profile

通用 Preview DTO 可保留 optional 字段以兼容无 Provider 的内部生产任务；W5 通过服务端 `ExternalActionPreviewProfileRevision` 收紧，不复制 Preview Store：

```text
requiredRefs:
  ActionTypeRevision
  CapabilityRevision + CapabilityBinding
  AccountBinding
  AdapterCapabilityRevision
  RiskPolicyRevision
  BudgetPolicyRevision
  KillPolicyRevision
  DryValidationReceipt
requiredDimensions:
  objectScope/channelScope/cost/budget/risks/
  reversibility/approvalChain/rateCapacityKill
```

ActionType family 在 W5 allowlist 中时，Proposal 创建、审批、Lease 与 execute 均强制 exact Preview；旧 proposal 的 NULL 兼容只允许历史回读或明确的 `draft.internal`，不能继续进入外部执行。

## 4. 联合一致性

Preview 生成一个服务端 `actionBindingHash`，至少覆盖：

```text
tenant + purpose + subject/object scope
ActionType revision/hash
Capability revision/hash + binding id/version/health
Account id/version/status
Adapter revision/hash
Risk/Budget/Kill policy revisions
DryValidation receipt hash
impact dimensions and source refs/cutoff
```

ActionProposal 固定 `previewRef + actionBindingHash`；Approval 只批准该 hash；ExecutionLease 再读所有 mutable authority 并锁定同一 hash。任何账号、Binding、Adapter、预算、kill、来源、许可、Eval 或 Preview expiry 漂移，都使旧 Proposal/Approval 失效，不允许静默重算后沿用审批。

## 5. Server-owned Impact

来源引用并不能让客户端提交的数值自动成为权威。八维结果必须由领域 calculator 与 Adapter `dryValidate` 共同生成：

- 领域 calculator：对象/渠道范围、Evidence/Eval/策略风险、业务可逆性；
- Adapter：账号权限、Provider 限制、quota/rate/capacity、预计成本、Provider 可逆性、reconcile 模式；
- Budget authority：remaining/reservation/max/unknown cost；
- Approval policy：有效审批链、职责分离、expiry；
- Kill authority：平台/组织/项目/账号/ActionType 多级状态。

每个值标质量、来源、cutoff 和 calculator/Adapter revision。unknown 对 W5 必需维度一律 blocked；不允许用默认 0、默认可逆或默认账号补齐。

## 6. 传递撤销与并发

freeze 保存 direct + transitive dependency snapshot。除版本/hash 外，至少重新计算 Capability/Account health、Adapter publication、DryValidation expiry、预算 reservation、kill、Evidence license/revoke 与 Eval publication/release gate 当前态。W4-03 的 Eval 撤销传播缺口必须先关闭。

Approval 与 Lease 必须串行化 mutable dependencies；锁不到或状态 unknown 就 no-op/blocked。Preview 过期后只能创建新 revision 和新 Proposal，不延长旧审批。

## 7. 验收

1. W2-D 通用内部生产任务在没有 external profile 时保持兼容，不被 W5 规则误伤。
2. allowlisted W5 Action 无 Preview、缺任一 required ref、hash 不一致、账号/Binding/预算/kill 漂移均失败关闭。
3. ActionProposal、Approval、Lease、Receipt 与 Lineage 可回到同一 actionBindingHash 和 Preview exact ref。
4. server calculator 与 dryValidate 输出不可由客户端覆盖；unknown 不伪 0。
5. ProductionStart 与 Action execution 两类门分别测试，互不授予对方权限。
6. `org-org/dev-project` 只有在 W5-00/01 GREEN 且存在受控账号后才做正向小流量；当前 0 Preview/0 StartDecision 维持诚实空态。

## 8. AOS-000236 实施决策

### 8.1 实时事实

1. W2-D 已有 server-owned `actionBindingHash`，但它仅覆盖 Preview exact ref、dependency snapshot、binding/capability/account 和 expiry，并且只存在 Draft snapshot，尚未作为 Proposal 显式字段持久。
2. Preview 还没有一个不可分裂的 external Action profile；ActionType/Adapter/Risk/ActionBudget/Kill/DryValidation 无法证明与同一 Preview 对齐。
3. `accountRef` 的 `ACCOUNT_AUTHORITY_UNAVAILABLE` 是真实失败关闭证据，不得为了制造正向测试而删除。
4. W5-01 只交付了 pure Adapter contract/conformance，没有 production publication authority；所以 W5-02 将交付 exact binding schema、持久和漂移复验，但 external profile 仍会因未实现 authority 而 blocked。

### 8.2 最小数据模型

在通用 Preview 上增加可选 `ExternalActionPreviewBinding`，用于 W5 外部动作专用 profile：

```text
purpose
ActionTypeRevision
CapabilityRevision
CapabilityBindingRevision
AccountBindingRevision
AdapterCapabilityRevision
RiskPolicyRevision
ActionBudgetPolicyRevision
KillPolicyRevision
DryValidationReceiptRevision
```

该对象所有 ref 都为 `id + revision + contentHash`，且 Capability/CapabilityBinding/Account 必须与 Preview 现有字段一致。内部生产任务不提供该对象时完全兼容。

### 8.3 文件级清单

- `services/aos-api/aos_api/aip_production_contracts.py`：新增 strict `ExternalActionPreviewBinding`，并在 `CreateImpactPreviewRequest` 中校验联合一致性。
- `services/aos-api/aos_api/aip_production_contract_store.py`：持久/回读 external binding，纳入 content/dependency/action binding hash，对尚无 authority 的 exact ref 生成稳定 blocker。
- `services/aos-api/aos_api/aip_action_models.py`：Proposal 投影增加显式 `actionBindingHash`。
- `services/aos-api/aos_api/aip_action_store.py`：对 W5 稳定 family 强制 external Preview，创建 Proposal 时校验 ActionType/purpose 并持久 hash，approval/lease/execute 重算漂移。
- `services/aos-api/aos_api/aip_action_execution.py`：Receipt payload 保留 `actionBindingHash`，不改变 Provider payload 状态机。
- `services/aos-api/alembic/versions/w5_001_impact_action_binding.py`：只增加 nullable JSONB/hash 字段和结构约束，不回填旧数据。
- `services/aos-api/tests/aip/test_w5_02_impact_preview_exact_binding.py` 及现有 W2-D/Action 回归：覆盖 strict refs、联合不一致、序列化/hash、稳定 blocker、W5 无 Preview 拒绝、内部兼容和迁移约束。

### 8.4 失败关闭与排除

- external binding 的 Adapter/Risk/ActionBudget/Kill/DryValidation authority 在后续任务完成前返回 `*_AUTHORITY_UNAVAILABLE`，因此不会冻结为 ready Preview；
- W5 稳定 family 无 exact Preview 时在 Proposal 创建前拒绝；不依赖客户端 risk hint 判断；
- 本次只创建迁移文件并做 upgrade/downgrade 测试，不对真实环境执行 migration；
- 不注册生产 Adapter，不解析账号/Secret，不发放 Approval/Lease，不执行 Action/Provider/canary/release。

历史预检证据见 `.evidence/workshop/2026-08-14-w5-02-impact-preview-exact-binding-preflight.json`；实施证据将写入 `.evidence/workshop/2026-08-25-w5-02-impact-preview-exact-binding.json`。

## 9. AOS-000236 实施结果

1. `ExternalActionPreviewBinding` 已把 purpose、ActionType、Capability、CapabilityBinding、Account、AdapterCapability、Risk、ActionBudget、Kill 与 DryValidation 十项 exact 事实作为不可分裂 envelope 纳入 Preview。
2. W5 稳定外部 Action family 在 Proposal 写入前强制 exact Preview；ActionType hash 与 purpose 必须同 Preview 一致。通用内部 Preview 不提供 external binding 时保持兼容。
3. `actionBindingHash` 已从 Draft-only 快照提升为 Proposal 显式持久事实，并在 approval/lease/start 前按当前 Preview 重算；Proposal 与 Draft 快照相互漂移同样失败关闭。Receipt 只追加该 hash 作为 lineage，不改变 Provider payload 或状态机。
4. `w5_001` 仅新增 nullable JSONB/hash 字段与约束，不回填旧事实；降级在已存在新事实时拒绝。测试数据库从空库升级到 `w5_001 (head)` GREEN，真实环境未执行 migration。
5. 专项回归 `28 passed`；累计 Action/W2-D/API 回归 `112 passed`；compileall、Alembic head 与 `git diff --check` GREEN。既有 warning 为历史 schema/operation-id warning，不属于本次新增失败。
6. 本项没有 route、组件或页面变化，浏览器验收不适用；没有用浏览器 smoke 替代后端合同证据。
7. Adapter/Risk/ActionBudget/Kill/DryValidation 等 production authority 尚未实现时返回稳定 `*_AUTHORITY_UNAVAILABLE` blocker；因此外部 Preview 不能 freeze 为 ready，更不产生真实 Action、Provider、canary 或 release。

结论：`W5_02_EXACT_BINDING_CODE_GREEN / INTERNAL_COMPATIBILITY_GREEN / EXTERNAL_AUTHORITIES_BLOCKED / NO_EXTERNAL_EFFECT / NO_RELEASE`。下一入口为 W5-03；W5-02 的 CODE GREEN 不代表任何 Action family operational GREEN。
