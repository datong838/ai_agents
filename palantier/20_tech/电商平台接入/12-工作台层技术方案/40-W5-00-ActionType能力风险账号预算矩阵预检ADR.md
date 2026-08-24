# W5-00 ActionType、能力、风险、账号与预算矩阵预检 ADR

> 日期：2026-08-14（2026-08-25 于 `m1` 实时复审并冻结）  
> 核查基线：`m1@90c0365`，项目 authority `AOS-000234`  
> 状态：`MATRIX_CONTRACT_FROZEN_GREEN / ALL_EXTERNAL_ROWS_BLOCKED / NO_RELEASE`  
> 边界：只读代码审查、测试与方案收敛；未修改源代码、迁移、数据库、真实租户、外部账号或静态视觉稿

## 1. 结论

AIP 已有 Proposal→Approval→ExecutionLease→Receipt→Reconcile 的通用安全骨架，27 项 Action/Capability 定向测试通过；但它还不是工作台可用的电商 Action 矩阵：ActionType 读取可变 `meta_action_type`，风险靠关键词启发式推断，Proposal/Lease 未绑定 exact Capability、租户账号、Adapter revision 或 BudgetPolicy，生产 Adapter 注册数为 0。

因此本 ADR 冻结目标矩阵与禁区，不开启执行。`AOS-000025` 新增 W2-D3 strict SDK/UI/browser GREEN，不会自动关闭 W4-08、Adapter 或真实账号门。

## 2. 联合主键与有效风险

每一行受控动作的唯一身份不是一个菜单按钮，而是：

```text
ActionTypeRevisionRef
  + CapabilityRevisionRef
  + CapabilityBindingRef
  + AccountRef
  + AdapterRevisionRef
  + RiskPolicyRevisionRef
  + BudgetPolicyRevisionRef
  + KillPolicyRevisionRef
  + TenantScope / purpose / markings
```

任一 exact ref 缺失、漂移、撤销、过期或 readiness 非 `available`，该行即 `blocked`。有效风险取 ActionType、Capability、账号、批量规模、数据敏感度、可逆性、金额/费用与组织策略下限的最大值；alias、客户端 hint 和租户 Overlay 只能升高，不能降低。

Action 的 `R0～R4` 与 Capability 的 `low/medium/high/critical` 只允许通过服务端签名映射：`low→不低于 R1`、`medium→不低于 R2`、`high→不低于 R3`、`critical→R4`。查询不进入副作用 Action 链；真正只读能力由 Query capability 执行。

## 3. 电商 Action family 基线

以下是稳定 family 与最低风险，不代表当前存在可执行实例。具体 provider ActionType ID 由签名 PlatformAdapterPack 发布并映射到 family，不能由页面自行造 ID。

| Action family | 典型动作 | 最低风险 | W5 初始策略 |
|---|---|---:|---|
| `draft.internal` | 保存 Draft、Proposal、计划、人工 Handoff | R1 | 仅 AOS 内部真源；不得伪装外部完成 |
| `order.remark` | 写订单内部备注 | R2 | 可作为小流量候选；需账号、dryValidate、单对象和 Receipt |
| `price.alert` | 发送价格异常告警，不改价 | R2 | 可作为小流量候选；目标与渠道 allowlist |
| `creator.invite` | 单达人邀请/消息 | R2 | 可作为候选；同意、频控、撤回竞态与证据齐备 |
| `customer.service-message` | 单客户服务消息 | R2 | 可作为候选；身份、consent、purpose、频控严格通过 |
| `content.publish` | 单内容/单渠道发布或撤回 | R2 | 分渠道专项门；必须绑定 exact Variant 与可验证撤回能力 |
| `campaign.schedule` | 活动/直播排期或公开配置 | R3 | 默认 disabled；专项双审批、容量与回滚演练后另行开门 |
| `bulk.contact` | 批量达人/客户触达 | R3 | 默认 disabled；不得由多次 R2 调用拆单绕过 |
| `creator.contract` | 合同、佣金或履约承诺 | R3/R4 | 默认 disabled；含资金承诺即 R4 |
| `price.update` | 商品改价、优惠、佣金调整 | R4 | 本阶段禁止执行 |
| `inventory.update` | 库存数量/可售状态修改 | R4 | 本阶段禁止执行 |
| `order.fulfill` | 发货、取消、售后状态推进 | R4 | 本阶段禁止执行 |
| `refund.payment` | 退款、支付、赔付或资金补偿 | R4 | 本阶段禁止执行 |

R2 “候选”仍不是授权：只有对应 contract suite、真实账号 readiness、预算、kill、canary 和用户批准全部 GREEN 后，才允许逐行开放。所有未列出的 ActionType 默认 disabled。

## 4. 账号与 Adapter 规则

- `AccountRef` 是租户受控的 opaque ref，绑定 provider、店铺/渠道、用途、marking、状态和 exact revision；Secret 只在受控执行环境解析。
- Proposal/ImpactPreview/Approval/Lease 必须固定同一 AccountRef 与 CapabilityBinding；执行前再次回读 health、quota、network policy、account status 与 Adapter revision。
- Adapter 先 `dryValidate`，返回权限、对象范围、预计费用、限流、容量、可逆性、reconcile 模式和稳定 blocker；不能在 execute 内临时选账号。
- timeout/断流为 `unknown`，只按同一 provider request ref reconcile；禁止换账号、换 Adapter 或新幂等键盲发。
- Provider 无可靠查询时必须声明 `reconcile=manual` 并提高风险，不得把人工推测写成 applied。

## 5. 预算模型

现有 `daily_budget/budget_units` 只统计 Lease 获取次数，不能作为业务预算。目标 BudgetPolicy 至少包含：

```text
currency / unit
estimatedCost / maxCost / measuredCost / unknownCost
org/project/account/actionType limits
daily and rolling-window limits
reservationId / reservedAt / expiresAt
release or settlement Receipt
UsageReceipt refs / reconciliation status
```

unknown cost 按风险预算占用，不按 0；Lease 获取只创建 reservation，执行终态由 UsageReceipt 结算，过期/失败按策略释放。预算修改使用 CAS、审批和不可变 Receipt，不能直接更新表后静默生效。

## 6. 现有实现需保留与需替换

保留：maker-checker-executor 分离、proposal expiry、单 attempt Lease、幂等、租户隔离、append-only Receipt、unknown/reconcile、kill 与 R4 默认禁止。

替换或补齐：

1. 将关键词风险分类器降为保守兼容兜底；正式决策来自 exact RiskPolicy，未知一律取更高风险并 blocked。
2. 建立 versioned ActionType authority，并通过 installation lock 解析；禁止直接把可变 `meta_action_type` 当正式发布真源。
3. Proposal/Preview/Lease 加入 exact Capability/Binding/Account/Adapter/Budget/Kill refs，并做传递漂移复验。
4. 增加签名 allowlist 与逐行 readiness；R2/R3 不能仅凭通用审批人数自动执行。
5. Adapter contract 增加 dryValidate、capability metadata、usage 和可核验 reconcile；生产 Registry 为空时继续 503 fail-closed。
6. Guardrail 管理增加 version/CAS/审批/Receipt；不删除现有强制检查。

## 7. 两级退出门（2026-08-25 纠偏）

### 7.1 W5-00 矩阵合同退出门

- 电商 Action family、最低风险、默认策略和 exact 联合主键已冻结；
- R4、R3 与 unlisted 行默认 disabled，R2 行仅是候选而非授权，批量不可拆单降级；
- 所有外部行在 exact refs 未齐备时统一返回稳定 blocker，不产生可执行 Proposal/Lease；
- Secret、Cookie、Token、完整 PII 不进入 Proposal、Preview、Receipt、日志或共享记忆；
- W4-08 已在 `AOS-000234` 闭环，可进入 W5-01 实现 contract suite。

### 7.2 单行运营可用门

以下条件不是 W5-00 文档任务的循环前置，而是每个真实外部 Action 行在 W5-01～W5-07 逐项关闭的运营门：

- versioned ActionType 和 RiskPolicy 有唯一 authority；
- Capability/Binding/Account/Adapter/ActionBudget/Kill exact refs 可回读且同一截止面 GREEN；
- 生产 Adapter revision 通过 contract suite，账号 readiness、网络、配额和签名 allowlist 均 GREEN；
- dryValidate、ImpactPreview、Approval、Lease、Receipt、Usage、unknown/reconcile 与 kill 联合链闭环；
- W5-07 另有独立 canary 授权、精确账号/对象/预算/时窗/停止条件和浏览器证据。

## 8. AOS-000234 实时复审结论

1. 现有 `ActionAdapter` 仍只有 `execute/reconcile`，`ACTION_ADAPTERS` 仍是进程内注册；不存在生产 Adapter revision authority。
2. 现有 `ActionTypeRevisionRef` 只固定 action type id/hash/object type，执行时仍回读可变 `meta_action_type`；不能冒充签名发布真源。
3. 现有 `BudgetPolicyRevision` 属于模型运行治理，不是外部业务 Action 的费用 reservation/settlement authority；严禁同名误用。
4. Proposal/Lease 尚未绑定完整联合主键，所以本次只冻结矩阵和失败关闭规则，所有外部行继续 blocked。
5. `draft.internal` 仅允许保存 AOS 内部 Draft/Proposal 真源，不得伪装 Provider 已成功。

### 8.1 稳定 blocker

| 范围 | blocker | 解除责任 |
|---|---|---|
| 全部外部行 | `ACTION_EXACT_BINDING_INCOMPLETE` | W5-01～W5-05 |
| 未发布 Adapter revision | `ADAPTER_CAPABILITY_REVISION_UNAVAILABLE` | W5-01 |
| 未绑定账号/密钥 | `AUTHORIZED_ACCOUNT_UNAVAILABLE` | W5-01/W5-02 |
| 未实现 Action 业务预算 | `ACTION_BUDGET_POLICY_UNAVAILABLE` | W5-03 |
| R3/R4/unlisted | `ACTION_FAMILY_DISABLED_BY_BASELINE` | 后续专项方案，非 W5 默认开放 |
| 真实 canary | `CANARY_EXPLICIT_AUTHORIZATION_REQUIRED` | W5-07 |

### 8.2 W5-01 文件级入口

- `services/aos-api/aos_api/aip_action_adapters.py`：增加不可变 Adapter capability 合同与严格 registry 边界，保留旧 fake adapter 测试兼容。
- `services/aos-api/aos_api/aip_adapter_contracts.py`：新增 exact refs、dry validation、状态、usage 和支持性声明的纯合同。
- `services/aos-api/aos_api/aip_adapter_conformance.py`：新增零外部副作用的参数化合规评估，不连接生产 Provider。
- `services/aos-api/tests/aip/test_w5_01_adapter_capability_contracts.py`：覆盖定义、hash/drift、账号、dryValidate、幂等、unknown/reconcile、usage 和不支持能力的失败关闭。
- 本次 W5-01 不增加迁移、HTTP 写路由、真实账号解析或 Provider 调用；持久发布真源与联合绑定按 W5-02 后续闭环。

历史预检证据见 `.evidence/workshop/2026-08-14-w5-00-action-risk-matrix-preflight.json`；实时冻结证据见 `.evidence/workshop/2026-08-25-w5-00-action-risk-matrix-freeze.json`。
