# W6-09 三 Module Partial、Usage、效果成熟与 Handoff 预检 ADR

> 日期：2026-08-14  
> Authority：`AOS-000029`  
> 代码基线：`w2-workshop@13b88b5e5bab52ce93d0e92ac181192e24adfd3b`  
> 证据：`.evidence/workshop/2026-08-14-w6-09-three-module-partial-usage-effect-handoff-preflight.json`  
> 结论：`GENERIC_USAGE_AND_HANDOFF_AUTHORITIES_GREEN / THREE_MODULE_EFFECT_CLOSURE_BLOCKED`

## 1. 审查结论

AIP one-time Handoff 与 Usage Receipt authority 是可信基础，定向后端 18 项、前端 20 项通过；但达人、价格、客户 W6-03～08 均未 GREEN，三领域 partial reducer、Usage 自动绑定、EffectReview runtime/成熟窗口、Module bridge/业务决定与业务 read model 为 0。W6-09 保持 `NOT_STARTED / IMPLEMENTATION_BLOCKED`。

## 2. 公共契约决策

1. partial 由 item outcome 集计算，不允许调用者直接写 batch success/partial；
2. 领域状态映射保留 original status/Observation，公共 algebra 不覆盖领域真源；
3. Usage provider receipt 自动桥接，measured/estimated/unknown 分开，unknown 不造 0；
4. Usage exact Attribution 同时覆盖 Module、Batch/item、run、capability、account 与 budget，Adjustment append-only；
5. EffectReview 是版本化 authority，不是 EffectReviewRef 字符串或前端卡片；
6. 成熟窗口按 event time/cutoff/late data/min sample/baseline-control/attribution policy 裁决，未到窗保持 immature；
7. Handoff 复用平台 envelope，但必须由唯一 Module compiler 建立 canonical TaskRun 与最小 refs；
8. consume 只证明 token 被正确接收，业务 accept/reject/request-more/return 另有决定 Receipt；
9. item outcome、Action outcome、Usage settlement、Effect maturity、Handoff decision 五轴独立，不互相冒充完成。

## 3. 当前阻断与解除条件

| ID | 当前事实 | 解除条件 |
|---|---|---|
| `DEP-W6-THREE-MODULE-UPSTREAM` | W6-03～08 全未勾选 | 三领域前置正式 GREEN |
| `DEP-W6-THREE-MODULE-PARTIAL-CONTRACT` | 无公共 algebra/reducer/数量守恒 | typed mapping、重建与冲突测试 GREEN |
| `DEP-W6-THREE-MODULE-USAGE-BRIDGE` | Usage 仅部分 provider path 自动接入 | Research/Action/Channel receipt bridge GREEN |
| `DEP-W6-THREE-MODULE-USAGE-ATTRIBUTION` | 无三领域多维绑定政策 | exact Attribution/Adjustment/settlement GREEN |
| `DEP-W6-EFFECT-REVIEW-AUTHORITY` | 仅 Schema/ref 声明 | contract/store/API/RLS/CAS/Receipt GREEN |
| `DEP-W6-EFFECT-MATURITY-POLICY` | 无成熟窗口 runtime | event-time/late/sample/re-eval/invalidation GREEN |
| `DEP-W6-EFFECT-EVIDENCE-ATTRIBUTION` | 无 originals/指标/基线/归因 compiler | Evidence/Impact/Outcome 联合 binding GREEN |
| `DEP-W6-MODULE-HANDOFF-BRIDGE` | generic Handoff 只认 Agent/TaskRun | 唯一 Module compiler 与最小披露 GREEN |
| `DEP-W6-MODULE-HANDOFF-DECISIONS` | 仅 issue/consume/revoke/expire | accept/reject/request-more/return Receipt GREEN |
| `DEP-W6-THREE-MODULE-CLOSURE-READ-MODEL` | 无五轴业务视图 | partial/usage/maturity/handoff/a11y GREEN |
| `DEP-W6-THREE-MODULE-CLOSURE-GATES` | W5/W6 前置、Adapter、真实 cohort 缺失 | code-green/operational-ready 与成熟样本满足 |

## 4. 双轮审查记录

### 第一轮：真源与状态守恒

- PASS：领域 original status 与公共 item algebra 分离；
- PASS：Usage authority 可复用但不能冒充已自动绑定；
- PASS：EffectReview Schema 声明与 runtime authority 分离；
- 整改：原方案未定义五轴独立状态、成熟窗口和 Handoff consume/accept 差异，已补齐。

### 第二轮：跨域最小披露与经验回流

- PASS：Module compiler 只传最小 refs，request-more 由来源重新授权；
- PASS：EffectReview immature/insufficient/unknown 不生成可晋升经验；
- PASS：每项阻断有稳定 ID 与退出条件，三领域前置未 GREEN 时不越门；
- PASS：当前结论为 `NOT_STARTED / IMPLEMENTATION_BLOCKED / NO_EXTERNAL_EFFECT`。

## 5. 复审结论

W6-09 目标契约通过文档复审，当前实现未通过。安全入口是先完成 W6-03～08 和 W5，再建设公共 item reducer、Usage bridge/Attribution、EffectReview/maturity authority 与 ModuleHandoffCompiler；禁止把 AsyncState partial、Usage API、EffectReviewRef 或 generic Handoff consume 宣称为三领域效果闭环。

## 6. 2026-08-25 施工复审与文件级子波

### 6.1 实时事实与阻断重分类

- Authority 已推进到 `AOS-000252`；代码基线为 `aos-platform/m1@f3573f83`。W6-03～W6-08 已逐项形成代码/合同/浏览器证据，旧 `DEP-W6-THREE-MODULE-UPSTREAM` 已解除。
- 公共 Usage authority 已具备 measured/estimated/unknown、Adjustment 与 Attribution 合同；`aip_effect_review.py` / store 已具备 EffectReviewRevision、成熟度决策和五轴 snapshot；Handoff service 已具备 consumed 后的 accepted/rejected/request_more/returned 决定与 CAS Receipt。因此旧文中的“EffectReview runtime 与业务决定为 0”只保留为历史，不复制第二套公共 authority。
- 当前真实缺口是达人、价格、客户三领域 original outcome 到公共 algebra 的 canonical mapping，Provider Usage Receipt 到领域 exact Attribution 的受控桥，EffectReview/成熟度与领域 Evidence/Impact/Outcome 的 exact binding，Module Handoff compiler，以及三页面五轴贡献视图。
- 真实 Provider、账号/capability、实际 cohort、外部 Effect、迁移 apply、Canary 与 release authority 仍不存在。它们不阻断 typed bridge、RLS/CAS、API、只读贡献视图和负向合同施工，但继续阻断任何真实 Action、自动发送、业务写入与“成熟有效经验”声明。

### 6.2 163/164 组合落位

W6-09 不把 partial、Usage、EffectReview 或 Handoff 包装成新的角色大 Skill。达人、价格、客户继续消费各自原子 Skill 与领域 Logic；本波只把其产物、Observation、Action Receipt 和 EffectReview 通过受控 Tool/Capability authority 连接到五轴 closure。页面分别展示主责数字同事、协作者、atomic Skill/Logic exact refs 与 Workshop contribution，明确 `item outcome ≠ action outcome ≠ usage settlement ≠ effect maturity ≠ handoff decision`。

### 6.3 文件级子波

| 子波 | 最小改动文件 | 验收 |
|---|---|---|
| `W6-09A` | 本 ADR、三领域方案、D-waves、Task Receipt/Lease | 实时基线、五轴真源、163/164 分层和零副作用边界一致 |
| `W6-09B` | `ecommerce_workshop_three_module_closure.py`、`ecommerce_workshop_three_module_closure_store.py` | typed item algebra、领域 mapping、Usage Attribution、Effect binding、Handoff compilation；tenant/CAS/append-only |
| `W6-09C` | `routers/ecommerce_workshop.py`、OpenAPI 与测试 | internal compiler/observation command + 三领域贡献 GET；调用方不得自报聚合成功或成熟 |
| `W6-09D` | `alembic/versions/w6_009_three_module_closure.py` 与迁移测试 | additive、RLS/FORCE RLS、唯一 head；只验证不 apply |
| `W6-09E` | Web contract/parser/client、`CreatorGrowthPage.tsx`、`PriceGovernancePage.tsx`、`CustomerPage.tsx` 与测试 | 五轴独立、partial/unknown/immature/request-more 可见；无真实动作控件 |
| `W6-09F` | 专项负向矩阵 | 跨租户、original/ref 漂移、数量不守恒、unknown 造 0、未成熟造成功、Handoff 扩披露全部失败关闭 |
| `W6-09G` | W6 累计回归、build、内置浏览器、方案复审、Evidence/Receipt/CAS/Prime | 能力不倒退，证据闭合后才勾选 W6-09 |

### 6.4 可达状态与恒定边界

本波可达状态是 `THREE_MODULE_CLOSURE_CODE_CONTRACT_BROWSER_GREEN`：能够从 canonical 三领域 authority 重建 partial，绑定已有 Usage/EffectReview/Handoff exact refs，并展示 immature/insufficient/unknown 与业务决定。没有真实 Observation 或成熟样本时必须诚实为空或 blocked；测试 fixture 只能证明合同，不得写入真实业务数据，也不得晋升 MemoryCandidate。

本波不 apply migration，不触发 Provider、ProtectedContact、通知、邀约、调价、发送、Handoff token consume、真实业务 mutation、Canary、外部 Effect 或 release。任何 operational authority 缺失仍逐门失败关闭，不能由单开发者全栈授权替代。
