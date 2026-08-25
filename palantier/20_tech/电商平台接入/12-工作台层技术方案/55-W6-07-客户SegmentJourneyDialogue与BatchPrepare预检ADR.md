# W6-07 客户 Segment、Journey、Dialogue 与 Batch Prepare 预检 ADR

> 日期：2026-08-14  
> Authority：`AOS-000029`  
> 代码基线：`w2-workshop@bdcd36c5dd7ed29c056451c41c7d956054f45b4d`  
> 证据：`.evidence/workshop/2026-08-14-w6-07-customer-segment-journey-dialogue-batch-prepare-preflight.json`  
> 结论：`CUSTOMER_LITE_FOUNDATION_PARTIAL / CUSTOMER_DOMAIN_AND_BATCH_PREPARE_BLOCKED`

## 1. 审查结论

客户工作台已有 CustomerLite OT、Order Link、通用生产契约和统一 Shell，但没有 Segment/Journey/Dialogue/Consent/Batch 的领域 authority。前端 6 文件 18 项通过，只证明统一壳稳定；后端组合测试为 50 通过 1 失败，P08 专项为 27 通过 6 失败，客户隐私底座不能宣称 GREEN。W6-07 保持 `NOT_STARTED / IMPLEMENTATION_BLOCKED`。

## 2. 关键架构决策

1. CustomerLite 保持隐私最小化，不承载联系方式、Consent 或 Preference；
2. protected contact 只能在 W6-08 获批执行边界解析，W6-07 Batch item 只保存稳定 Customer ref；
3. Segment 存定义/query revision/cutoff/policy，不复制成员 PII 列表；
4. Journey 与 Dialogue 策略均 append-only revision，规则变化不改写历史；
5. Brief/Evidence/Eval/Responsibility 必须同版冻结，动态 Agent 编排不删除责任；
6. prepare/freeze 为零发送副作用，显式 start 属于 W6-08；
7. Consent、purpose、retention、k-anonymity、频控和 capability 任一 unknown 均失败关闭；
8. 不为让旧 P08 测试通过而恢复真实执行的 sample-input 回退，也不删除共享 canary 残留掩盖测试隔离问题。

## 3. PII 契约漂移

运行时 `ec_source_adapter.py` 对 `ns_member` 显式丢弃 mobile、OpenID、nickname、avatar、reg_address、last_login_ip、password、pay_password；CustomerLite 核心测试同样要求 PII 最小化。但 `p08-customer-lite.yaml` 仍列出 nickname、mobile、email、realName、address/fullAddress 等映射，并维护另一份排除清单。

在客户分群和触达进入编码前，必须收敛为单一可审查策略：Schema 允许字段、source drop、mapping manifest、日志/证据遮蔽和 protected contact resolver 的职责互不矛盾。不能把“源库里有字段”误写成“CustomerLite 可查询字段”。

## 4. 当前阻断与解除条件

| ID | 当前事实 | 解除条件 |
|---|---|---|
| `DEP-W6-CUSTOMER-DOMAIN-AUTHORITY` | 仅 CustomerLite，八类客户领域对象为 0 | typed contract/store/API/RLS/CAS/Receipt GREEN |
| `DEP-W6-CUSTOMER-BUNDLE-CONTRACT` | Module exact refs 与 actionTypes 为空 | Bundle refs 指向已发布 authority 并通过安装门 |
| `DEP-W6-CUSTOMER-CONSENT-PURPOSE-AUTHORITY` | 无 Consent/Preference/purpose/retention authority | 版本化决策、撤回与 unknown 负向测试 GREEN |
| `DEP-W6-CUSTOMER-PII-CONTRACT-DRIFT` | P08 mapping 与 runtime drop/Schema 漂移 | 单一 PII 契约及资产一致性测试 GREEN |
| `DEP-W6-CUSTOMER-SEGMENT-AUTHORITY` | 无 query hash/cutoff/k-anonymity/member revision | Segment rebuild/漂移/小群体门 GREEN |
| `DEP-W6-CUSTOMER-JOURNEY-AUTHORITY` | 无阶段图、策略 revision 与停止条件 | Journey transition/exit/CAS GREEN |
| `DEP-W6-CUSTOMER-DIALOGUE-CONTRACT` | 无 Brief/Evidence/Eval/Strategy/originals | 同版冻结、独立评估、聚合守恒 GREEN |
| `DEP-W6-CUSTOMER-BATCH-PREPARE` | 无零副作用 prepare/freeze | item 守恒、去重、0 send、CAS/Receipt GREEN |
| `DEP-W6-CUSTOMER-READ-MODEL` | 仅通用 Shell | 分群/旅程/对话/批次披露与 a11y GREEN |
| `DEP-W6-CUSTOMER-P08-BASELINE-REGRESSION` | P08 专项 27 pass / 6 fail | 按当前 JDBC fail-closed 修正测试/实现契约并全绿 |
| `DEP-W6-CUSTOMER-TEST-ISOLATION` | canary 残留使空列表断言失败 | fixture 独立 scope/seed/cleanup 契约 GREEN |
| `DEP-W6-CUSTOMER-UPSTREAM-GATES` | W4-08、W6-01 未勾选 | 两项正式 GREEN |

## 5. 双轮审查记录

### 第一轮：隐私与权威边界

- PASS：CustomerLite、Consent、ProtectedContact、Segment/Journey 的真源职责分开；
- PASS：成员列表和联系方式不进入 Batch、URL、日志、Evidence 或分享视图；
- PASS：PII mapping 漂移被提升为 P0，不以运行时 drop 单点遮盖资产问题；
- 整改：原方案未明确 protected contact 解析时机、P08 基线失败与测试隔离，已补齐。

### 第二轮：零副作用与可干预生命周期

- PASS：prepare/freeze/start 严格分离，W6-07 不发送、不解析 contact；
- PASS：eligible/excluded/review/unknown/deduplicated 数量守恒，漂移必须重算；
- PASS：Brief/Evidence/Eval/Responsibility、Consent、频控、渠道 readiness 均可见可干预；
- PASS：每项阻断有稳定 ID 和退出条件，当前未错误勾选 W6-07。

## 6. 复审结论

W6-07 目标契约通过文档复审，当前实现未通过。正确入口是先恢复 P08/隐私契约的可信基线，再建设 Consent、Segment、Journey、Dialogue 和零副作用 Batch authority；禁止把 CustomerLite、legacy decision tags、静态 Widget 或通用 Shell 宣称为客户运营闭环。

## 7. 2026-08-25 施工复审与文件级子波

### 7.1 实时事实与旧阻断关闭

- Authority：`AOS-000250`；代码基线：`aos-platform/m1@58c8f7e`；唯一开发者在 `m1` 串行施工，不再把缺失实现转交或等待其他开发者。
- 当前重跑 P08 Pipeline、JDBC Source Adapter 与客户只读模型专项为 `25 passed`；2026-08-14 的 `27 passed / 6 failed` 与共享 canary 单测失败只保留为历史，不再阻断施工。
- 仍存在真实 PII 资产漂移：`p08-customer-lite.yaml` 继续声明 nickname、mobile、email、avatar、realName、address/fullAddress 等映射，而 runtime 已使用 `ns_member` allowlist、CustomerLite schema v2 和四字段最小投影。本波先把 YAML 收敛到同一公开契约，并增加资产一致性负向测试；不恢复 sample-input 回退，不读取或删除真实业务数据。
- W4-08、W6-01 已完成；现有 CustomerLite/read-only Shell 可作为基座。Consent/Preference、Segment、Journey、Dialogue、Batch authority 由本波直接补齐；W6-08 的 contact resolve/start/send 仍是独立后续门。

### 7.2 163/164 组合落位

客户工作台使用既有原子能力，不创建一个大而全 Skill：

1. `build-evidence-pack`；
2. `segment-entities`；
3. `consent-and-purpose-check`；
4. `needs-discovery`；
5. `customer-journey-plan`；
6. `response-or-outreach-draft`；
7. `verify-claims`；
8. `review-outcomes`。

它们由 `ecommerce-customer-relationship` Logic exact 编排；`私域管家`主责，`内容官`、`客服专员`、`导购顾问`与`数据参谋`协作。工作台只呈现 Skill 贡献、Logic 编排、数字同事责任、领域 exact refs、数量守恒与 blocker；不复制 AIP Skill 实现，也不把 Draft/prepare 显示成已触达。

### 7.3 authority 与恒定安全边界

本波建立 append-only、tenant-scoped、version/hash CAS 的 `CustomerConsentPolicyRevision`、`CustomerSegmentRevision`、`CustomerJourneyRevision`、`CustomerDialogueStrategyRevision` 与 `CustomerDialogueBatchRevision`：

- Consent policy 固定 purpose/channel/marking/retention 与 granted/withdrawn/unknown 判定合同，不保存联系方式；
- Segment 固定 definition/query/schema/source/policy/cutoff/k-anonymity hashes，只保存稳定 Customer refs 和资格结果，不导出 PII 成员表；
- Journey/Dialogue 固定阶段、停止条件、Brief/Evidence/Eval/Responsibility/strategy exact refs；
- Batch prepare/freeze 固定 target/item hashes，并满足 `input = eligible + excluded + needs_review + unknown + deduplicated`；item 不包含 mobile/OpenID/email/address/raw message/provider payload；
- 不发布 resolve-contact/start/send/provider 路由；`contact_resolution_count = action_count = provider_call_count = send_count = external_effect_count = 0`。

### 7.4 子波与具体文件

| 子波 | 最小改动文件 | 验收 |
|---|---|---|
| `W6-07A` | 本 ADR、`17-客户关系技术方案.md`、D-waves、Task Receipt/Lease | 实时基线、PII 单一契约、组合落位与零触达边界一致 |
| `W6-07B` | `bundles/platforms/ecommerce-niushop/content/mappings/p08-customer-lite.yaml`、P08 资产一致性测试 | YAML 只声明 allowlist/CustomerLite v2 字段；禁止 PII 回流 |
| `W6-07C` | `ecommerce_workshop_customer_lifecycle.py`、`ecommerce_workshop_customer_lifecycle_store.py` | Consent policy、Segment、Journey、Dialogue、Batch prepare/freeze；tenant/CAS/append-only/数量守恒 |
| `W6-07D` | `routers/ecommerce_workshop.py`、OpenAPI 基线与测试 | 仅内部 authority 命令和贡献 GET；无 contact/start/send route |
| `W6-07E` | `alembic/versions/w6_007_customer_lifecycle.py` 与迁移测试 | additive、RLS/FORCE RLS、唯一 head；只验证不 apply |
| `W6-07F` | Web contracts/parser/client、`CustomerPage.tsx`、样式与测试 | Skill→Logic→数字同事→贡献视图、五桶守恒、prepare 0 触达、无 PII/动作控件 |
| `W6-07G` | 专项＋W6 累计回归、build、内置浏览器、diff/方案复审、Evidence/Receipt/CAS/Prime | 能力不倒退；证据闭合后才勾选 W6-07 |

### 7.5 关闭口径

W6-07 的代码 GREEN 只证明隐私最小化资产、客户领域 authority、零副作用 Batch 与工作台贡献视图闭合。ProtectedContact 解析、真实 Consent 运营数据、渠道账号/capability、start、频控 reservation、撤回竞态、发送、Provider、Effect、迁移 apply 与 release 均不在本波伪造；它们由 W6-08 重新核验并逐门开启。
