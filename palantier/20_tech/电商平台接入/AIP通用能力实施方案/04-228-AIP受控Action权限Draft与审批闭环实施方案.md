# 228-AIP 受控 Action、权限、Draft 与审批闭环实施方案

> 状态：**待评审 · 不授权编码**
> 对应阶段：AIP-3。

## 1. 目标

把 Tool 请求、Ontology Action、外部 Connector 和人工审批统一为：

```text
ActionType policy
 -> ActionProposal
 -> server-side risk classification
 -> Draft
 -> maker-checker approval
 -> ExecutionLease
 -> Adapter call
 -> Receipt / UnknownExternalState
 -> reconcile / compensate
```

## 2. 风险分层

| 等级 | 示例 | 默认 |
|---|---|---|
| R0 | 本体/Wiki/公开证据只读查询 | 可执行，完整留痕 |
| R1 | 内容、回复、报告、活动草稿 | 自动生成 Draft，不外发 |
| R2 | 单次低影响发布/触达 | 指定角色批准后执行 |
| R3 | 批量触达、价格/优惠、公开直播 | maker-checker + 预算/频控 |
| R4 | 支付、退款、库存扣减、权限、不可逆 | 默认禁止，专项安全评审 |

客户端的 `risk_level` 只是提示，服务端策略必须抬高风险，不得降低。

## 3. Canonical 对象

- `ActionTypeRevision`：input schema、side effect、risk floor、permission、adapter、receipt schema、compensation。
- `ActionProposal`：task/run/actor/object refs、expected revision、idempotency key、expires_at。
- `Draft`：proposal snapshot、diff、evidence、approval policy。
- `ApprovalEvent`：maker/checker、decision、bound revision/hash。
- `ExecutionLease`：单次执行租约、截止时间、attempt。
- `ActionReceipt`：provider request id、accepted/applied/failed/unknown、reread evidence。

## 4. 六层防线的现代化映射

旧“六层权限”不再堆 Prompt 规则，映射为：

1. Capability/ActionType allowlist。
2. 服务端风险下限与 Policy Engine。
3. AuthZ、租户、字段 marking、purpose check。
4. Draft 与职责分离。
5. Adapter 网络/密钥/预算/频控/kill switch。
6. Receipt 回读、对账、补偿与事故审计。

## 5. 现有映射与文件

复用 O1 Action/Draft/Receipt、现有 DraftInbox、tenant isolation、decision lineage。禁止继续扩展 `aip_drafts_engine` singleton 为生产真源。

```text
services/aos-api/alembic/versions/*_aip_action_control.py
services/aos-api/aos_api/aip_action_policy.py
services/aos-api/aos_api/aip_action_proposal_service.py
services/aos-api/aos_api/aip_action_execution_service.py
services/aos-api/aos_api/routers/aip_actions.py
apps/web/src/api/aipActions/*
apps/web/src/pages/DraftInboxPage.tsx
apps/web/src/pages/s2/LogicRunPanel.tsx
```

## 6. 验收

1. 无批准时所有 R2+ Adapter 不可达。
2. 修改 proposal 后旧批准失效。
3. 重复请求只产生一个外部动作或进入明确 unknown/reconcile。
4. 超时不能直接标失败并重试；必须先按 provider request id 对账。
5. 跨租户、越权字段、过期批准、预算耗尽、kill switch 均失败关闭。
6. UI 的“批准”不等于已执行；只有 Receipt 回读才能显示已应用。
