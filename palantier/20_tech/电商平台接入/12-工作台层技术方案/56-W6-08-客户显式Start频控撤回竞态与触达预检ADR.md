# W6-08 客户显式 Start、频控、撤回竞态与触达预检 ADR

> 日期：2026-08-14
> Authority：`AOS-000029`
> 代码基线：`w2-workshop@e3d7c2398fc66e426f48a439de7b6befc8a5c3da`
> 证据：`.evidence/workshop/2026-08-14-w6-08-customer-start-frequency-revocation-contact-preflight.json`
> 结论：`GENERIC_ACTION_SAFETY_SKELETON_GREEN / CUSTOMER_CONTACT_EXECUTION_BLOCKED`

## 1. 审查结论

通用 Action 的 Proposal/Approval/Lease/Receipt/unknown/reconcile 骨架定向后端 29 项、前端 11 项通过。但 W6-07 没有 frozen customer Batch，客户 ActionType、显式 start、Consent 竞态、客户级频控、ProtectedContact、生产 Adapter、durable Attempt、partial reducer 和业务 read model 均为 0。W6-08 保持 `NOT_STARTED / IMPLEMENTATION_BLOCKED`，本次未触达任何客户。

## 2. Start 与撤回的线性化决策

“发送前再查一次 Consent”不足以解决竞态，因为查询后到 provider 调用前仍有窗口。采用可审计线性化：

1. 每项 start 在 Consent authority 串行化边界内锁定最新 Consent/Preference；
2. 同时固定 Batch item、purpose、content、channel/account/capability、频控、Impact 与策略 hashes；
3. 创建 durable `DispatchAttempt`、frequency reservation 与一次性 `ContactExecutionPermit`，记录 sequence；
4. 撤回 sequence 在前则永不解析 contact；Attempt sequence 在前则本次授权成立，撤回阻断其余未获 permit item 和未来消息；
5. Adapter dispatch 前兑换短 TTL opaque handle，resolver 再验证 permit；raw contact 不返回 Workshop；
6. provider 结果通过 Receipt/Webhook/reread 追加，unknown 不自动重发。

这个规则明确竞态先后，不承诺物理世界的“同时撤回必然阻止已发消息”。用户界面必须展示授权 sequence、撤回 sequence 与当前 item 状态。

## 3. 频控不是通用 rate limit

现有 guardrail 仅按 ActionType 的 minute/day 计数。客户触达还需 `FrequencyPolicyRevision`，至少覆盖 customer、channel、purpose、Journey/campaign、quiet hours、rolling windows、timezone 与例外。reservation 需跨批次 CAS：accepted/applied 结算，dispatch 前失败可按政策释放，unknown/accepted_pending 保持占用直到对账，禁止因 timeout 腾出额度后重复发送。

## 4. 当前阻断与解除条件

| ID | 当前事实 | 解除条件 |
|---|---|---|
| `DEP-W6-CUSTOMER-CONTACT-UPSTREAM` | W6-07 无 frozen Batch | W6-07 正式 GREEN |
| `DEP-W6-CUSTOMER-ACTION-TYPES` | Module actionTypes 为空 | 客户 typed Action/Draft authority GREEN |
| `DEP-W6-CUSTOMER-EXPLICIT-START` | 无 batch start/CAS/item Receipt | 显式 start、重放、0 implicit start GREEN |
| `DEP-W6-CUSTOMER-CONSENT-REVOCATION-RACE` | acquire/execute 不绑定或复验 Consent | sequence/permit/撤回并发负向测试 GREEN |
| `DEP-W6-CUSTOMER-FREQUENCY-POLICY` | 只有 ActionType rate limit | 客户多维 policy/reservation/settlement GREEN |
| `DEP-W6-CUSTOMER-PROTECTED-CONTACT` | generic adapter 直收 payload | opaque permit/resolver/日志无 contact GREEN |
| `DEP-W6-CUSTOMER-IMPACT-ACTION-BINDING` | 无 item/Consent/频控/账号联合 hash | Proposal/Approval/Lease 漂移 fail-closed GREEN |
| `DEP-W6-CUSTOMER-PRODUCTION-ADAPTERS` | typed channel Adapter 为 0 | account/schema/idempotency/webhook/conformance GREEN |
| `DEP-W6-CUSTOMER-DURABLE-EXECUTION` | consume-before-call crash 窗口 | durable Attempt/outbox/recovery GREEN |
| `DEP-W6-CUSTOMER-BATCH-PARTIAL` | 无 item reducer/数量守恒 | partial/cancel/unknown aggregate GREEN |
| `DEP-W6-CUSTOMER-UNKNOWN-OPTOUT-RECONCILE` | 无直接 outcome、人工 Case、退订事件 reducer | signed webhook/reread/manual Case/Consent update GREEN |
| `DEP-W6-CUSTOMER-CONTACT-READ-MODEL` | 仅通用 Inbox/Shell | start/频控/撤回/partial/unknown/a11y GREEN |
| `DEP-W6-CUSTOMER-CONTACT-GATES` | W5 与 W6-07 未 GREEN，Adapter 0 | 对应 capability code-green/operational-ready |

## 5. 双轮审查记录

### 第一轮：授权与隐私竞态

- PASS：start 的线性化点、Consent 撤回先后和用户可见语义明确；
- PASS：ProtectedContact 只在一次性 Permit 兑换边界出现，Workshop 无 raw contact；
- PASS：通用 rate limit 与客户级 frequency reservation 分离；
- 整改：原方案只有“执行前复验”，未定义查询后竞态窗口和 unknown 的额度占用，已补齐。

### 第二轮：故障恢复与数量守恒

- PASS：durable Attempt 先于 provider，避免 consume-without-Receipt 无法判定；
- PASS：partial/item reducer、取消边界、unknown/reread/Webhook/人工 Case 完整；
- PASS：每项 P0 有稳定 ID 与退出条件，W5/W6-07 未 GREEN 时不触达；
- PASS：当前结论为 `NOT_STARTED / IMPLEMENTATION_BLOCKED / NO_EXTERNAL_EFFECT`。

## 6. 复审结论

W6-08 目标契约通过文档复审，当前实现未通过。安全入口是先完成 W6-07 与 W5，再建设客户 ActionType、Consent 线性化、频控 authority、ProtectedContact resolver、durable Attempt 和 item reducer；禁止把通用 Action 测试、Draft Inbox 或 ActionType rate limit 宣称为客户触达闭环。

## 7. 2026-08-25 施工复审与文件级子波

### 7.1 实时事实与阻断重分类

- Authority：`AOS-000251`；代码基线：`aos-platform/m1@c85501c2`。W6-07 已交付 frozen Dialogue Batch、Consent policy、Segment/Journey/Dialogue authority 与五桶守恒，Prime 强一致入口均 CURRENT，因此 `DEP-W6-CUSTOMER-CONTACT-UPSTREAM` 的代码施工前置已经解除。
- W5 已具备 Proposal/Approval/Lease/Attempt/outbox/Receipt/unknown/reconcile 的公共代码合同；W6-04 已验证“显式 start 只编译治理决策、不调用 Provider”的领域组合模式。W6-08 直接复用公共 authority，不复制执行器，也不接受调用方自报账号、capability、Approval 或 Receipt。
- 真实客户联系方式、Consent 运营数据、渠道账号/capability、Provider 与外部 Effect 仍没有可伪造的 operational authority。它们不阻断客户 start/frequency/withdrawal/permit/attempt/partial 的 typed authority、RLS/CAS、内部 API 和只读贡献视图施工，但继续阻断 permit 兑换、contact resolve、Provider dispatch、发送、Canary 与 release。
- 单开发者串行负责所需四层代码，不再以“等待其他开发者交付”停工；涉及真实租户数据、外部副作用、迁移 apply 或发布时仍逐门失败关闭。

### 7.2 163/164 组合落位

W6-08 不新建“客户触达大 Skill”。客户判断与文案继续由 W6-07 的 8 个原子 Skill 和 `ecommerce-customer-relationship` Logic 编排；显式 start、频控 reservation、Consent withdrawal、opaque permit、durable attempt/outbox、Receipt reconcile 均属于受控 Tool/Capability/Action authority。`私域管家`主责，`内容官`、`客服专员`、`导购顾问`与`数据参谋`协作；工作台展示每项贡献和门，不把受控动作伪装成 Skill 成果。

### 7.3 本波可达状态与恒定边界

本波实现 `FrequencyPolicyRevision`、`CustomerConsentWithdrawalObservation`、`CustomerBatchStartDecisionRevision`、`CustomerFrequencyReservationRevision`、`CustomerContactExecutionPermitRevision`、`CustomerDispatchAttemptRevision`、`CustomerDispatchObservation` 与守恒 read model。start 必须绑定 frozen Batch、item hash、Consent/Preference/purpose/retention、frequency/channel/account/capability/content/Impact/Approval exact refs；所有 resolver 均从 canonical store 读取，不信任页面 payload。

当前可达的 start 是 `governance_prepared`：创建 durable attempt/outbox intent、frequency reservation 和不可兑换的 opaque permit authority，记录 Consent/start sequence，`contact_resolution_count = provider_call_count = send_count = external_effect_count = 0`。不发布 permit redeem、raw contact、provider dispatch 或 send 路由；真实 authority 缺失时保留 stable operational blockers。withdrawal sequence 在前的 item 进入 `skipped_withdrawn`，start sequence 在前只证明治理授权先后，不声称消息已发；unknown 保持 reservation，占用不得因 timeout 自动释放或重试。

### 7.4 子波与具体文件

| 子波 | 最小改动文件 | 验收 |
|---|---|---|
| `W6-08A` | 本 ADR、`17-客户关系技术方案.md`、D-waves、Task Receipt/Lease | 实时基线、Skill/Logic/Action 分层、线性化与零发送边界一致 |
| `W6-08B` | `ecommerce_workshop_customer_contact.py`、`ecommerce_workshop_customer_contact_store.py` | Frequency/withdrawal/start/reservation/permit/attempt/observation；tenant/CAS/append-only/状态守恒 |
| `W6-08C` | `routers/ecommerce_workshop.py`、OpenAPI 基线与测试 | 仅内部 governance authority 命令和贡献 GET；无 redeem/contact/provider/send route |
| `W6-08D` | `alembic/versions/w6_008_customer_contact.py` 与迁移测试 | additive、RLS/FORCE RLS、唯一 head；只验证不 apply |
| `W6-08E` | Web contracts/parser/client、`CustomerPage.tsx`、样式与测试 | sequence、频控、partial/unknown、operational blockers 可见；无 raw contact/发送控件 |
| `W6-08F` | 专项负向矩阵 | 非 frozen/漂移/跨租户/撤回竞态/频控超限/重复 start/Receipt binding/unknown 不释放失败关闭 |
| `W6-08G` | W6 累计回归、build、内置浏览器、方案复审、Evidence/Receipt/CAS/Prime | 能力不倒退；证据闭合后才勾选 W6-08 |

### 7.5 关闭口径

W6-08 的代码 GREEN 只证明客户触达治理 authority、竞态顺序、频控 reservation、durable attempt/outbox intent、partial/unknown/reconcile 与工作台贡献视图闭合。真实 permit 兑换、ProtectedContact 解析、账号/capability、Provider dispatch、发送、真实 Consent 数据、迁移 apply、Canary、外部 Effect 和 release 必须由当时的 exact operational authority 独立裁决，不能由本波测试或开发授权替代。
