# W6-04 达人显式 Start、Partial、合同履约与关系链预检 ADR

> 日期：2026-08-14；施工复审：2026-08-25
> Authority：`AOS-000246`
> 代码基线：`m1@c2a1367`
> 证据：`.evidence/workshop/2026-08-14-w6-04-creator-start-partial-contract-relationship-preflight.json`
> 结论：`IMPLEMENTATION_AUTHORIZED / PLAN_FROZEN / EXTERNAL_EFFECT_OPERATIONAL_GATE_RETAINED / NO_RELEASE`

## 1. 初始审查结论（2026-08-14 历史基线）

通用 Action Proposal→Approval→ExecutionLease→Receipt→reconcile 骨架和前端状态呈现可复用，定向后端 6 项、前端 11 项通过。但 W6-03 领域批次 authority 未实现；四类达人 ActionType 与生产 Adapter 为 0；没有 batch start、item partial reducer、合同 Diff、履约或长期关系 authority。故 W6-04 当前不可编码、不可勾选、不可对真实达人触达。

## 2. 公共骨架与领域缺口

公共骨架已经做到：租户作用域、ActionType revision、maker/approver/executor 分离、审批过期、Lease、kill、基本预算/频率、单次执行 Receipt、timeout unknown 不盲重试、provider reread 和补偿 Proposal。

它尚不能替代达人领域闭环：

- Proposal 的 payload/diff 仍是任意字典，没有 OutreachBatch/item exact refs；
- Adapter 只返回单一 outcome，没有逐项 partial；
- production registry 没有私信、寄样、合同、佣金 Adapter；
- 执行前置事务会先 consume Lease 再调用 provider，存在 crash-without-Receipt 窗口；
- reconcile 的 applied/failed 只放在 payload，顶层为 reconciled，批次无法可靠聚合；
- `ContractRef/DeliveryRef/RelationshipRevision` 只是 Bundle 字符串。

## 3. 决策

1. W6-04 只消费 W6-03 frozen OutreachBatch，不允许从任意候选列表直接 start；
2. start 必须 CAS 并复验所有 frozen exact refs，形成不可变 `BatchStartDecision/Receipt`；
3. 每个 eligible item 和每个 ActionType 独立形成 Proposal/Impact/Approval/Lease/Receipt；一个批准不得跨私信、寄样、合同、佣金；
4. 引入 durable ExecutionAttempt/outbox，解决 consume-before-call crash 窗口；
5. partial reducer 保持 item 数量与状态守恒，accepted/unknown 不计完成；
6. unknown 只允许只读对账、Webhook 或人工 Case，resolved outcome 成为可机器聚合字段；
7. 合同 Diff、履约 Observation 和成熟后的 Relationship revision 共用合作 lineage，历史不可改写；
8. 先完成 W5 对应 capability 的 code-green，再经独立 operational-ready/真实授权门；本 ADR 不授权外部执行。

## 4. 初始阻断与解除条件（2026-08-14）

| ID | 当前事实 | 解除条件 |
|---|---|---|
| `DEP-W6-CREATOR-START-UPSTREAM` | 无 frozen OutreachBatch | W6-03 正式 GREEN |
| `DEP-W6-CREATOR-ACTION-TYPES` | 四类 ActionType 未发布、Module actionTypes 为空 | 四类 exact authority/Bundle refs GREEN |
| `DEP-W6-CREATOR-ACTION-INDEPENDENCE` | 无领域 compiler/policy 证明审批隔离 | 一 capability/账号/item-set/预算/Impact 一门测试 GREEN |
| `DEP-W6-CREATOR-EXPLICIT-START` | 无 start CAS/Decision/Receipt | exact revalidation 与重放/漂移测试 GREEN |
| `DEP-W6-CREATOR-BATCH-PARTIAL` | 只有单一 Adapter outcome | item Receipt reducer 与数量守恒 GREEN |
| `DEP-W6-CREATOR-PRODUCTION-ADAPTERS` | 生产 Adapter 为 0 | typed contract/conformance/account/usage/webhook GREEN |
| `DEP-W6-CREATOR-DURABLE-EXECUTION` | consume-before-call crash 窗口 | durable attempt/outbox/recovery GREEN |
| `DEP-W6-CREATOR-UNKNOWN-RECONCILE` | resolved outcome 不可直接聚合、无人工 Case | machine-readable outcome/manual Case/concurrency GREEN |
| `DEP-W6-CREATOR-CONTRACT-DELIVERY-RELATIONSHIP` | 三类领域 authority 为 0 | store/API/lineage/成熟窗口测试 GREEN |
| `DEP-W6-CREATOR-ACTION-READ-MODEL` | 无领域执行与关系视图 | item partial/unknown/合同 Diff/履约/a11y GREEN |
| `DEP-W6-CREATOR-W5-GATES` | W5-00～08 全未勾选 | 所需 capability 分项 code-green/operational-ready |

## 5. 双轮审查记录

### 第一轮：副作用与职责隔离

- PASS：prepare/freeze 与 start 完全分离；
- PASS：四类动作独立审批、Lease、Receipt，不共享授权；
- PASS：unknown 不重放、partial 不掩盖 item、真实执行需另行授权；
- 整改：原方案未定义 start 数量守恒和 crash 窗口，已补充 durable attempt 与逐项 reducer。

### 第二轮：领域生命周期与可恢复性

- PASS：合同 Diff、佣金 maker-checker、履约乱序与 Relationship 成熟窗口已明确；
- PASS：历史只追加 revision/compensation，不把回滚理解为数据库回滚；
- PASS：每项阻断有稳定 ID 和可验证解除条件；
- PASS：W6-03/W5 未 GREEN 时仍 `NOT_STARTED / IMPLEMENTATION_BLOCKED`。

## 6. 初始复审结论（2026-08-14）

W6-04 目标契约通过文档复审，当前实现未通过。安全入口是先解除 W6-03 与 W5 对应门，再从领域 ActionType/Adapter/ExecutionAttempt 开始；禁止先接真实账号、先造批量发送按钮或将 generic Draft Inbox 冒充达人闭环。

## 7. 2026-08-25 施工复审

### 7.1 实时依赖结论

- W6-03 已以 `m1@c2a1367` 交付 CreatorBatch prepare/freeze、exact refs、数量守恒和零副作用边界；`AOS-000246` 已将 W6-04 设为唯一下一串行入口。
- W5-01～W5-08 已有 exact AdapterCapability、Impact binding、Draft→Proposal→Approval→Lease、durable Attempt/outbox、typed reconcile、Webhook 与 kill 代码控制面；原 consume-before-call 窗口与不可聚合 reconcile 已不是代码缺口。
- 生产 Adapter/Account/Secret、实时预算和真实外部授权仍非 operational GREEN；本波用可回读的内部 StartDecision 与 action lane 关闭代码链，但不调用 Provider，不制造真实触达事实。

### 7.2 163/164 产品落位

W6-04 沿用 W6-03 的“原子 Skill → `ecommerce-creator-match` Logic → 导购顾问主责 → 达人工作台贡献”，不创建领域大 Skill。显式 start 只将 frozen batch 编译为四条相互独立的 canonical Action 治理 lane：

```text
outreach-message | sample-shipment | contract-signature | commission-change
每条 lane = ActionType + Impact + AdapterCapability + Account + Budget + ApprovalPolicy exact refs
```

一条 lane 的 approval/lease/receipt 不得授权另一条 lane。工作台只展示领域生命周期贡献、partial/unknown 和 exact lineage，不在前端拼接 W5 API，不提供绕过 operational gate 的“批量发送”。

### 7.3 串行子波与文件级清单

1. `W6-04A` frozen item 兼容：扩展 `ecommerce_workshop_creator_prepare.py`，保存可消费 item exact refs；旧 batch 默认空 items 仅可读且 start blocked。
2. `W6-04B` start authority：新增 `ecommerce_workshop_creator_lifecycle.py` 与 store，实现 BatchStartDecision/Receipt、四 action lane 独立 binding hash、expected version/hash CAS、幂等和零 Provider call。
3. `W6-04C` partial/reconcile：保存 item/lane Receipt exact refs，聚合 prepared/accepted/applied/failed/unknown/disputed；accepted/unknown 不计 completed，resolved outcome 为顶层机器可读字段。
4. `W6-04D` 领域生命周期：新增 ContractRevision/Diff、DeliveryObservation 与 RelationshipRevision，共用 collaboration lineage，只追加且成熟窗口失败关闭。
5. `W6-04E` 对外契约与界面：扩展现有 ecommerce Workshop router、OpenAPI、strict SDK/parser、`CreatorGrowthPage.tsx` 与样式；仅提供受控内部命令和读模型。
6. `W6-04F` 验收：新增 `w6_004_creator_lifecycle.py`，只验证 RLS/FORCE RLS/唯一 head 不 apply；运行专项、W6 累计、OpenAPI、TypeScript/build、内置浏览器、一致性复审、EvidencePack、Receipt、authority CAS 和 Prime 回读。

### 7.4 不回退与不越门条款

- 旧 W6-03 batch 与 W2-04 read model 必须保持可读；缺 item exact refs 时显式 legacy blocked，不回填、不推断。
- StartDecision 只表示用户显式进入 Action 治理，不表示 Proposal approved、Lease issued、Provider called 或 Effect applied。
- 本波不 apply migration，不修改真实业务数据，不连接真实达人账号，不触达、寄样、签约、改佣金、做 Canary 或发布。
