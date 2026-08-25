# W8-04 EffectReview→MemoryCandidate→Wiki 治理与撤销预检 ADR

> 日期：2026-08-15
> 决策：`NOT_STARTED / SCENARIO_CONTRACT_APPROVED / HARD_GATE_BLOCKED / NO_PROMOTION_OR_PUBLICATION`
> 前置：产品正式封板；W4-08、DEP-E7 当前 release 全 GREEN

## 1. 当前事实

w2 基线中的 Candidate、Pipeline、Store、治理晋升和 Search Eval 39 项测试通过。预检开始时 m1 authority 为 E7-4C；文档封口前 AIP 已 CAS 到 `AOS-000034 / E7-4D GREEN`，canonical read-only exposure/context API 已完成，当前只剩 E7-5 SDK/UI/browser seal。这个进展仍未补齐 canonical `EffectReviewRevision + EffectMaturityPolicy` runtime，不能证明一个经营效果具备学习资格。

因此本轮只冻结跨层合同；不创建、批准或晋升真实 Candidate，不发布或撤销 Wiki，不把通用 Memory 测试冒充 Workshop 学习闭环。

## 2. EffectReview 根与学习绑定

exact `EffectReviewRevision` 是场景根，`learningBindingHash` 至少覆盖：

1. TaskGraph/TaskRun/Attempt；
2. Action/Reconcile Receipt 与 Usage settlement；
3. Metric definition/value、cutoff、quality、baseline 和 cohort；
4. AttributionPolicy 与 EffectMaturityPolicy revision；
5. EvidenceBundle、Eval run、假设、反证和 uncertainty；
6. MemoryCandidate、GovernanceApproval 与 Promotion Receipt；
7. MemoryItem/Wiki revision、KnowledgeCitation 和 revocation impact refs。

成熟度不足、partial/unknown、对照缺失、证据 stale/revoked 或反证未处置时，只能显示 pending/blocked。EffectReview 不能自动 submit、approve、promote 或 publish；Working memory、自由模型输出、静态视觉稿样例也不能进入 Candidate pipeline。

## 3. 治理、晋升与撤销

- Candidate 的 pending/quarantined/rejected/approved/promoted 独立于知识项 active/stale/revoked/expired；
- 治理检查 PII、marking、license、freshness、applicability、conflict、quality 和 exact Eval evidence；
- approve 只产生治理证据，不发布知识；promote 是独立幂等命令；
- promote 生成不可变 MemoryItem/Wiki revision、exact Citation 和 Receipt，不覆盖 EffectReview 或旧 Wiki；
- 查询按 cutoff 复验 status、freshness、marking、applicability、purpose、content/source hash；
- source/projection/知识撤销只追加 revoke/impact 事实，保留历史 Citation/Exposure/Receipt；
- 撤销后的未来使用失败关闭，受影响 AgentRun、Decision 和 downstream Candidate 只生成 refs 供人工复核或重算，不静默回滚历史外部决策。

## 4. 验收门

负向至少覆盖：Effect immature/partial/unknown/无对照/反证未决，Working/free-form/untrusted source，PII/license/marking/applicability/freshness 拒绝，approve/promote 竞态与幂等漂移，source/governance/content hash 漂移，stale/revoked/expired 查询，已有 Exposure 后撤销，Wiki governance envelope/Citation/payload 不一致，冲突 Candidate shadow，以及跨租户 Candidate/Memory/Wiki/Exposure。

正式正向只认 `org-org/dev-project`，`dev-org/dev-project` 只作隔离 canary。必须证明 promotion 前后 exact lineage、撤销后查询立即 fail-closed、历史 Exposure 不丢失、受影响 refs 可回读；Mock 与内存 fixture 不能替代。

## 5. 两轮审查

### 第一轮：学习资格与治理职责

- EffectReview、成熟度、治理批准、晋升和知识有效性为独立轴；
- 用户能看到证据、假设、反证、不确定性和适用边界；
- approve 不等于 promote，所有晋升均有独立 Receipt；
- Working memory 与模型输出不能绕过 trusted pipeline。

结论：`PASS`。

### 第二轮：撤销传播与执行资格

- revoke 保留历史 Exposure/Receipt，未来查询 fail-closed；
- 影响传播以 refs 发起复核/重算，不自动改写历史决策；
- E7-4D GREEN 仍不等于 DEP-E7 全 GREEN，通用 39 项测试不等于 Workshop E2E；
- 当前没有 Candidate、Wiki、真实租户或浏览器写入。

结论：`PASS_WITH_HARD_GATE_BLOCKED`。

## 6. 最终裁决

W8-04 场景合同可以作为未来施工和验收基线；当前不得运行或勾选。预检事实见 `.evidence/workshop/2026-08-15-w8-04-effectreview-memorycandidate-wiki-governance-revocation-preflight.json`。

## 7. 2026-08-26 串行施工方案（AOS-000273）

依据 163/164 分层约束，W8-04 只建立“EffectReview 学习资格 → Candidate 治理 → 不可变知识 revision → 查询复验 → 撤销影响”的 GET-only 贡献视图，不把整条学习闭环包装成大 Skill，也不让经营参谋页面直接 submit、approve、promote、publish 或 revoke。投影必须 exact 绑定可复用原子 `SkillRevision`、跨步骤 `LogicRevision`、`AgentTemplate/AgentInstance + SkillBinding`，并把成熟度、治理批准、晋升、知识有效性和撤销影响保留为独立结果轴。

文件级最小施工清单：

1. 新增 `services/aos-api/aos_api/ecommerce_workshop_learning_scenario_contracts.py` 和 `ecommerce_workshop_learning_scenario.py`，定义 exact `EffectReviewRevision + EffectMaturityPolicyRevision` 根、`learningBindingHash`、7 段学习/治理/查询/撤销链、Skill/Logic/数字同事绑定、Candidate/Memory/Wiki/Exposure/impact 数量守恒、5 独立结果轴和全 false Command 合同。
2. 在 `services/aos-api/aos_api/routers/ecommerce_workshop.py` 新增独立 GET-only Analyst learning-scenario 路由；默认 canonical reader 缺失时返回结构化 blocked，不创建 Candidate、KnowledgeCitation、Wiki revision 或 revoke/impact 事实。
3. 新增后端场景专项测试，并扩充 router/OpenAPI 合同测试；覆盖 tenant/cutoff/root/binding/分层/成熟度、Candidate 与知识状态轴混淆、approve/promote 混淆、历史 Exposure 丢失、撤销后未来查询仍可用、ledger 漂移及伪 operational-ready。
4. 扩充 `apps/web/src/api/ecommerceWorkshop/{contracts,parser,client}.ts` 及 parser 专项测试，严格拒绝 Evidence/Wiki 正文、PII、Provider Secret、完整查询文本或受保护对象正文进入列表合同。
5. 最小扩充 `apps/web/src/components/workshop/AnalystPage.tsx` 及 CSS/组件测试，独立展示 7 阶段、5 结果轴、原子 Skill/Logic/数字同事贡献、Candidate 与知识状态分离、撤销影响和全部关闭的治理命令；场景读取失败不影响现有 Analyst v2。
6. 重生 OpenAPI generated/inventory，执行专项与累计后端、全量 Web、typecheck/build、OpenAPI 确定性、scoped security 和内置浏览器验收；最后形成 EvidencePack、Delivery Receipt、安全提交、authority CAS 和 Prime 独立长记忆事实。

兼容与安全边界：复用现有 `aip_effect_review` 与 `aip_memory_*` 合同语义但不调用其写服务；不修改旧 Analyst v2 字段；不 apply 共享迁移；不写 `org-org/dev-project`；不提交/批准/晋升 Candidate，不创建/发布/撤销 Wiki，不展开知识或 Evidence 正文，不调用 Provider、Action 或 release。
