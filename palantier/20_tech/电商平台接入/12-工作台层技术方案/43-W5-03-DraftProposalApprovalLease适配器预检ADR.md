# W5-03 Draft→Proposal→Approval→Lease 适配器预检 ADR

> 日期：2026-08-14（2026-08-25 于 `m1` 开始实施）
> 核查基线：`m1@f71c1ea`，authority `AOS-000237`
> 状态：`IMPLEMENTED_CODE_GREEN / EXPLICIT_DRAFT_AND_EXACT_APPROVAL_LEASE / EXTERNAL_RESERVATION_BLOCKED / NO_EXTERNAL_EFFECT / NO_RELEASE`
> 边界：只实现 additive authority、API、失败关闭测试和证据；不执行真实 migration，不读取账号/Secret，不发放真实 Approval/Lease，不调用 Provider，不做 canary/release

## 1. 结论

现有 AIP-3 已提供可复用的安全骨架：PostgreSQL Proposal/Draft/ApprovalEvent/ExecutionLease 真源，proposal hash/version、幂等锁、租户隔离，maker、approver、executor 三方隔离，以及批准、Lease、执行结果在 UI 中明确分层。后端 16 项、前端 8 项专项回归 GREEN。

但 W5-03 仍不能勾选。当前创建 Proposal 时同步产生一个已“等待审批”的 Draft，没有独立修改、冻结、提交步骤；审批资格只有宽泛角色，审批有效期可由调用者省略；`draftOnly=true` 没有被审批服务执行；Lease 也没有固化 W5-02 的 `actionBindingHash` 与账号、Adapter、预算 reservation。因此本 ADR 批准的是整改后的契约基线，不是编码完成。

## 2. 四段对象与状态

W5 外部 Action 使用明确的四段链，不能用页面按钮一次跨越：

```text
ActionDraftRevision(editable)
  --freeze/submit--> ActionProposal(immutable)
  --policy decisions--> ApprovalSet(exact)
  --atomic acquire--> ExecutionLease(single-use)
```

- `ActionDraftRevision`：允许人在 prepare 阶段修改 payload/diff/evidence/preview；每次保存产生新 revision，不覆盖旧快照。
- `ActionProposal`：submit 后不可修改，固化 draft ref、Preview ref、`actionBindingHash`、purpose、scope 与 expiry；变更必须由新 Draft 生成新 Proposal。
- `ApprovalSet`：由服务端 `ApprovalPolicyRevision` 解析所需 slot、顺序、人数、独立性与期限；单个 ApprovalEvent 不能代表整套审批已满足。
- `ExecutionLease`：只在 Proposal、ApprovalSet 和联合依赖仍有效时原子创建；它是外部副作用唯一执行凭证，不是 TaskRun start lease。

旧的一次 `create_proposal` 路径只允许历史回读或 `draft.internal`。属于 W5 allowlist 的外部 Action 必须经过显式 freeze/submit，不能用兼容路径直接进入审批。

## 3. 服务端审批策略

审批不能只判断 `admin/approver/aip_approver`。`ApprovalPolicyRevision` 至少定义：

- eligible principal/role slot、组织授权范围与 delegation revision；
- required slots、每槽人数、顺序或并行关系、maker/checker/executor 独立性；
- 风险、金额、批量、marking、账号与对象范围对应的审批下限；
- Proposal、Preview、dryValidate 和预算 reservation 的最大有效期；
- reject、expire、revoke、supersede 后的稳定状态和 reasonCode。

ApprovalEvent 固化 `proposalRef + actionBindingHash + policyRevision + slot + eligibilitySnapshotHash + expiresAt`。期限由服务端取各依赖最早到期时间，客户端只能请求更短时间，不能省略后获得永久批准。`draftOnly`、不在 allowlist、R4 或任一 unknown 必须在 submit/decide/acquire 三处失败关闭。

## 4. Lease adapter

Lease acquisition 在一个事务中锁定并复验：

1. immutable Proposal 与 Draft/Preview exact refs；
2. 完整、未过期、未撤销且 slot 满足的 ApprovalSet；
3. W5-02 `actionBindingHash` 对应的 CapabilityBinding、AccountBinding、Adapter、Risk/Budget/Kill policy 与 DryValidationReceipt；
4. 账号/capability health、Provider readiness、rate/capacity、marking、Evidence/Eval 传递撤销；
5. exact budget/quota reservation，而不是简单 `budget_units + 1`。

Lease 固化上述 refs/hash、owner、attempt、expiry、reservationRef 和 idempotency envelope。锁冲突、漂移或 unknown 一律 no-op/blocked。未消费 Lease 到期或被撤销时，由权威 transition 释放 reservation 并产生 Receipt；不能静默续期或换账号。执行前再次复验 kill 与可变依赖。

## 5. UI 投影

Draft Inbox 继续复用唯一 SDK，但按钮由服务端 command-readiness 投影驱动：显示 `eligible/disabledReasonCode/requiredSlots/satisfiedSlots/expiresAt/driftRefs`。用户必须能看到 Draft、Proposal、Impact、审批链、Lease 和 Receipt 的生命周期；没有资格或依赖漂移时按钮保持可聚焦并说明恢复动作。前端不自行推断角色，也不把 HTTP 接受当成批准或执行成功。

## 6. 兼容与迁移

- 保留历史 Proposal/Draft/Approval/Lease 只读解析；不回写或伪造缺失的 `actionBindingHash`。
- W5 external profile 对旧 NULL binding Proposal 标记 `legacy_non_executable`。
- 新表/字段采用 additive migration，先双读核对，再切换 W5 写入口；不改变 W2-D 内部无 Provider 生产任务。
- 当前生产 Adapter 注册为 0，真实正向 canary 仍不得开始。

## 7. 验收

1. Draft 多 revision、freeze/submit 幂等，提交后修改只能产生新 Proposal。
2. `draftOnly`、非 allowlist、R4、无 Preview 或缺联合 ref 均不能批准或取得 Lease。
3. 自批、自执行、同人占多个禁止 slot、无资格、过期、撤销和顺序错误失败关闭。
4. ApprovalSet、Proposal 与 Lease 固定同一 `actionBindingHash`；任一传递依赖 drift 使批准失效。
5. Lease 与预算/quota reservation 原子；并发只成功一次，过期/撤销可审计释放。
6. UI 展示稳定禁用原因并在 mutation 后重读 authority；Receipt 前不显示“已执行”。
7. `org-org/dev-project` 正向小流量必须等 W5-00～03 全部 GREEN 并另获 canary 授权。

机器证据见 `.evidence/workshop/2026-08-14-w5-03-draft-proposal-approval-lease-preflight.json`。

## 8. AOS-000237 实施决策

### 8.1 当前事实与兼容边界

1. W5-02 已把 external Action exact envelope 与 `actionBindingHash` 固定到 Preview/Proposal，但 external authorities 仍稳定 blocked；W5-03 不能用伪账号、伪预算或 fake ready Preview 制造正向运营证据。
2. 现有 `/action-proposals` 同步创建 Proposal 与兼容 Draft 投影，必须保留给内部/历史调用，避免既有功能倒退；W5 稳定 external family 继续禁止从该兼容入口绕过 explicit Draft。
3. 现有 decide 已有 maker/checker 隔离与 quorum，lease 已有 maker/approver/executor 隔离及并发单 attempt；本次在这些真源上追加 exact binding，不复制第二套执行状态机。
4. 当前启发式 risk policy 的 `draftOnly` 与宽泛角色不是 production ApprovalPolicy authority。新 explicit path 会保留服务器策略快照/hash并失败关闭，但 external operational GREEN 仍等待后续 exact policy/account/budget authorities。

### 8.2 最小 authority 设计

- 新增 append-only `ActionDraftRevision` 与 mutable head：create/revise 每次追加 revision；submit 追加 submitted revision并在同一事务产生 immutable Proposal，Proposal 固定 source Draft exact ref。
- Proposal 固定 `approvalPolicyHash`；ApprovalEvent 固定 `actionBindingHash + approvalPolicyHash + slotId + eligibilitySnapshotHash + server expiresAt`。
- server approval expiry 为 `min(客户端请求的更短期限, Proposal expiry, policy max TTL)`；客户端省略时仍生成有限期限，不再产生永久 approval。
- decide/acquire 均执行 `draftOnly`、executionAllowed、W5 exact binding 与 policy/hash 漂移门；不改变历史已落库事实，只阻止其获得新的外部执行权限。
- ExecutionLease 固定 `actionBindingHash + approvalSetHash + reservationRef`。内部兼容 path 可保留现有 guardrail 计数；W5 external 在 exact ActionBudget reservation authority 未接入时稳定 blocked，不把 `budget_units + 1` 冒充 reservation。

### 8.3 文件级清单

- `services/aos-api/aos_api/aip_action_models.py`：explicit Draft create/revise/submit、Draft revision与 approval/lease binding 投影。
- `services/aos-api/aos_api/aip_action_store.py`：append-only Draft authority、原子 submit、server approval expiry/slot/eligibility/hash与三处 fail-closed。
- `services/aos-api/aos_api/aip_action_service.py`：复用唯一 schema/marking/submission/risk 入口准备 Draft facts。
- `services/aos-api/aos_api/aip_action_execution.py`：Lease 固定 approval set 与联合 binding；W5 exact reservation authority 缺失时拒绝。
- `services/aos-api/aos_api/routers/aip_actions.py`：新增唯一 SDK 对应的 Draft create/revise/submit routes，不开放 autoApprove/autoExecute。
- `services/aos-api/alembic/versions/w5_002_action_draft_approval_lease.py`：additive tables/nullable exact lineage fields、RLS、append-only trigger与有事实降级保护；不回填、不执行真实 migration。
- `services/aos-api/tests/aip/test_w5_03_draft_proposal_approval_lease.py` 与既有 Action/W2-D 回归：覆盖多 revision、CAS、submit replay、maker/checker/executor、有限 expiry、draftOnly、exact hash、并发单 lease与 external budget reservation blocked。
- `services/aos-api/tests/aip/test_w2d_store.py`、`services/aos-api/tests/test_w2a_production_contract_api.py`：修复累计回归夹具，使其不写非法空 Schema ref、不删除 append-only Evidence，并按资源不可见而非租户全库为空验证隔离。

### 8.4 验收与明确排除

- 代码验收包括 focused、累计 Action/W2-D/API、空库 Alembic head、compileall、diff 与方案一致性复核。
- 本项修改后端 route/authority，不修改 Workshop 页面或视觉稿；浏览器验收不适用，不能以 HTTP smoke 冒充 UI 验收。
- 不执行真实 migration、真实租户 write probe、真实 Approval/Lease/Action、账号/Secret 解析、Provider、canary 或 release。
- W5-03 只能在 explicit Draft 与 exact approval/lease code controls 闭合后标记 CODE GREEN；任何 external operational readiness 继续为 blocked。

## 9. AOS-000237 实施结果

实现已闭合：显式 Draft create/revise/submit 采用 owner + revision/contentHash CAS 与命令幂等，submit 在同一事务追加 submitted revision 并创建 immutable Proposal；Proposal、ApprovalEvent 和 ExecutionLease 分别固定 source Draft、`approvalPolicyHash`、`actionBindingHash`、slot/eligibility、`approvalSetHash` 与 nullable reservation ref。审批有效期由服务端限制，旧外部 Proposal 入口不能绕过显式 Draft。

验收结果：W5-03 专项 `4 passed`，相邻链 `32 passed`，累计 W5/AIP Action/W2-D/W2-A/W2-B `96 passed`；`compileall`、Alembic 单 head `w5_002`、`git diff --check` GREEN。该项未修改页面，因此内置浏览器验收不适用。

结论：`W5_03_EXPLICIT_DRAFT_EXACT_APPROVAL_LEASE_CODE_GREEN / INTERNAL_COMPATIBILITY_GREEN / EXTERNAL_RESERVATION_AUTHORITY_BLOCKED / NO_EXTERNAL_EFFECT / NO_RELEASE`。W5 external 仍不能获得 Lease；下一入口为 W5-04 durable Executor/Receipt/Usage/lineage 交付桥。
