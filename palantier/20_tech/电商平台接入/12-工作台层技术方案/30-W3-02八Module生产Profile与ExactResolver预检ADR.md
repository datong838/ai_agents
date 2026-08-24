# W3-02 八 Module 生产 Profile 与 Exact Resolver 预检 ADR

> 日期：2026-08-14
> 核查基线：`w2-workshop@740b979`；AIP 最新集成事实 `m1@79901df` / `AOS-000023`
> 状态：`PREFLIGHT_COMPLETED / IMPLEMENTATION_BLOCKED`
> 边界：只读审查与方案冻结；未修改 AIP、Bundle、数据库或真实租户

## 1. 结论先行

W3-02 的产品方向与四层边界成立，但当前还不能编码或宣称“发布八 Module profile”。AIP 已提供 `TaskBriefRevision`、`EvidenceBundleRevision`、`EvalContractRevision`、`ResponsibilityPlanRevision` 的 PostgreSQL authority、Canonical API 和唯一前端 SDK；缺口位于 L1 profile 的签名资产与 L0/L1 接缝：

1. 生产路由使用无参数 `AipProductionContractStore()`，`ResponsibilityTemplateResolver` 未装配；真实 ResponsibilityPlan create 必须以 `RESPONSIBILITY_TEMPLATE_AUTHORITY_UNAVAILABLE` 失败关闭。
2. 八个 Workshop contribution 的 `responsibilityTemplateRefs` 均为空；没有可由 installation lock + artifact hash 解析的 exact `ResponsibilityTemplateRevision`。
3. 六个 growth Module 仍引用 `content/evals/placeholder.json`；operations/customer 的旧 dry-run Eval 服务于历史 Logic，不等于 Operation/Dialogue 等生产 Profile 的同版 Eval。
4. 当前 Bundle 中没有八 Module typed Brief schema、Evidence selection profile 或统一 production-profile descriptor。
5. `TaskBrief.schemaRef`、`EvalContract.artifactSchemaRef` 目前是普通 `ResourceRef`；若没有已安装签名 Artifact resolver，前端或 BFF 可提交“看似有 ref、实际无 authority”的字符串。

故新增依赖门：`DEP-C0-PROFILE-RESOLVER`。它不是第二套业务 Store，而是 AIP Canonical service 对已安装签名 DomainPack/SolutionPack artifact 的 exact 解析器。该门与 W2 数据基座、W3-01 runtime-control API 均独立，任何一个未通过都不能启动 W3-03。

## 2. 当前事实

| 检查项 | 当前实现 | 判定 |
|---|---|---|
| Brief/Evidence/Eval/Responsibility authority | `aip_production_contracts.py`、`aip_production_contract_store.py`、Canonical router、`api/aipProductionContracts` | `CODE_CONTROL_GREEN` |
| Responsibility template 校验 | Store 接受可注入 resolver；生产 router `_STORE = AipProductionContractStore()` | `BLOCKED_UNWIRED` |
| Brief/Eval schema exact 解析 | DTO 接受 ResourceRef；未发现 production route 的安装 Artifact resolver | `BLOCKED_UNWIRED` |
| 八 Module responsibility refs | 8/8 空数组 | `MISSING` |
| 八 Module目标 Eval profile | 6 placeholder；2 旧 Logic dry-run | `MISSING` |
| 八 Module typed profile | 无公共 descriptor、无领域 schema/selection/template | `MISSING` |
| W3-02 业务副作用 | 本任务只应发布签名资产，不创建 Brief/Run/Action | `MUST_REMAIN_ZERO` |

## 3. 四层放置与唯一资产结构

### 3.1 L0 平台内核

保留现有四类 authority 与 Canonical API，不增加电商字段。只增加通用 `InstalledProductionProfileResolver` 接缝：

- 输入：TenantScope、installation exact lock、Artifact ResourceRef/ExactRevisionRef；
- 校验：已安装、当前/允许历史版本、artifact path、content hash、schema ID、撤销/rollback 状态；
- 输出：解析成功或稳定 blocker；不返回未授权 payload；
- 装配：生产 router 必须显式注入，禁止测试 lambda 进入真实运行时。

### 3.2 L1 `domain.ecommerce.core`

以新版本而非原地覆盖发布公共电商 envelope：

- `aos.ecommerce-production-profile/v1`；
- `aos.ecommerce-brief-spec/v1`；
- `aos.ecommerce-evidence-selection/v1`；
- `aos.ecommerce-eval-profile/v1`；
- `aos.ecommerce-responsibility-template/v1`。

DomainPack 只规定字段、收紧规则与扩展点，不包含具体平台账号、真实客户数据、六个固定 Agent 编制或执行状态。

### 3.3 L1 SolutionPack

`solution.ecommerce.operations-base` 与 `solution.ecommerce.growth` 分别发布自己拥有的 Module profile。已签名的 `1.1.0/1.3.0` 不覆盖；新版本通过标准 publish/install/rollback 链进入 installation lock。每个 Module contribution 必须把 `productionContractRefs`、`evalPackRefs`、`responsibilityTemplateRefs` 指向本版本真实 artifact，禁止 placeholder。

### 3.4 L2/L3

- L2 Adapter 只贡献来源、平台规则和 capability readiness，不裁决 Brief/Eval/职责模板。
- L3 租户 overlay 只允许在 schema 约束内设置默认 profile、预算和 assignee 建议；不能删除事实、独立审核、批准、Receipt 等硬门。

## 4. 八 Module 唯一映射

| Module | Brief profile | Evidence/Eval 重点 | Responsibility 规则 |
|---|---|---|---|
| `ecommerce.task-cockpit` | `reference-only-task-summary`，只投影来源 Module frozen Brief | readiness、阻塞、职责覆盖、审批；不另建总控 Brief 真源 | 保留来源职责槽；仅允许 canonical reassign/Handoff |
| `ecommerce.content-campaign` | `campaign-content` | 人群、商品、Offer、预算、品牌/平台规则、素材许可 | 策划/内容 owner、独立审核、Handoff、批准/Receipt |
| `ecommerce.operations` | `operation-decision` | 原始订单/库存/履约事件、政策、SLA、金额和影响 | case owner、maker-checker、执行、reconcile |
| `ecommerce.creator-growth` | `creator-recruitment-negotiation` | 来源许可、身份/匹配、频控、合同 revision、履约标准 | discovery、谈判、合规/审核、外部触达批准 |
| `ecommerce.media-studio` | `media-production` | 素材/肖像/版权、品牌、事实、平台四门同版 Eval | LITE/STANDARD/FULL；八类影视职责可合并但不可消失 |
| `ecommerce.analyst` | `analysis-decision` | 指标口径、cutoff、归因证据、反证、假设和不确定性 | 分析、独立复核、计划 owner、效果复盘 |
| `ecommerce.price-governance` | `price-research-decision` | 同款依据、报价 originals、freshness、许可、策略/影响 | 采集、匹配、策略、审核；调价批准独立 |
| `ecommerce.customer` | `dialogue-journey` | identity、purpose、consent、retention、语气/禁词/频控 | 分群/旅程、文案、合规审核、发送批准、reconcile |

所有 profile descriptor 均引用同一四类公共 authority，不创建 ModuleBrief/ModuleEval/ModuleResponsibility Store。一个 Agent 可承担多个槽，但独立审核、合规、外部动作批准和结果对账不得被 merge 吞掉。

## 5. 精确实施包

### 5.1 允许修改

1. `bundles/domains/ecommerce-core/`：公共 envelope schema、新版本与 bundle evidence；
2. `bundles/solutions/ecommerce-operations-base/`：operations profile、真实 Eval/Responsibility artifact、新不可变版本；
3. `bundles/solutions/ecommerce-growth/`：其余七 Module profile、真实 Eval/Responsibility artifact、新不可变版本；
4. Asset Registry/AIP production service 的通用 installed-artifact resolver 与装配；不得含电商分支判断；
5. Bundle/schema/resolver/production-contract 邻接测试和本波 EvidencePack。

### 5.2 禁止修改

- 不新建 TaskBrief/Evidence/Eval/Responsibility 数据表；
- 不把 Bundle path、显示名、角色名或前端常量当运行 identity；
- 不复制 AIP DTO/Store 到 Workshop BFF；
- 不创建 Task/Run/Action，不安装真实租户，不执行外部副作用；
- 不以旧 dry-run Eval 或 placeholder 通过 8/8 门。

## 6. Red→Green 与退出门

1. Red：生产 router 无 resolver 时真实 ResponsibilityPlan create 稳定 blocked；伪 artifact、错误 hash、未安装版本、rollback 后旧 current ref 均拒绝。
2. Green：唯一 resolver 对已安装签名 artifact exact readback；跨租户、未知 path/hash、撤销/回滚失败关闭。
3. 8/8 descriptor 通过 DomainPack schema；Module ID、brief mode、required facts、Eval gates、slots、merge/handoff/return policy 完整。
4. 8/8 contribution refs 非空且引用本 Bundle 可用 path；placeholder 命中 0；旧 Logic Eval 不冒充生产 Eval。
5. 版本发布、签名、Resolver、Installation、rollback 邻接回归 GREEN；旧 active 版本和历史 refs 可读。
6. 前后 Task/Run/Action/真实租户业务行均为 0；本波只证明 profile 资产可被 exact 解析。

## 7. 开工判断

- `DEP-C0` 公共 authority：现有 code/control 可复用；
- `DEP-C0-PROFILE-RESOLVER`：`RED`；
- W2 全波退出门：未通过；
- W3-02：`NOT_STARTED / IMPLEMENTATION_BLOCKED`。

安全下一步是先由 AIP/Asset Registry owner 评审并实现通用 installed-production-profile resolver，随后在 W2 GREEN 后按第 5 节发布三组新 Bundle revision。W3-02 可以与 W3-01 做方案/红测准备，但不能绕过 W3 总开工门提前发布或安装。

## 8. AOS-000038 刷新与两轮复审

2026-08-15 按 `AOS-000038 / BIND1_1_CONTRACT_ADDITIVE_MIGRATION_GREEN_WITH_WARNINGS` 重新核验。BIND-1 的 additive contracts/migration 不发布 Module profile、不解析签名 Artifact、不补 Responsibility/Eval refs，也不使 Agent runnable；下一门仍是 BIND1_2 readiness，W2 退出门也未关闭。

第一轮复审重新清点八 Module：`viewRefs`、`productionContractRefs`、`responsibilityTemplateRefs` 均为 8/8 空；六个 Eval 为 placeholder，operations/customer 两个为历史 dry-run。整改继续冻结 profile envelope、exact artifact hash、active installation lock、signature/publisher/runtime/permission/marking/purpose/revocation 校验，以及“职责保留、执行者与 Agent 数量不固定”。结论 `PASS_AFTER_REMEDIATION`。

第二轮反查通用 Production Contract authority：TaskBrief/EvidenceBundle/EvalContract/ResponsibilityPlan Store/API/SDK 基础仍可复用，但 installed signed production-profile exact resolver、Responsibility template resolver 和 Module profile publication 均不存在。W3-02 只能贡献 immutable L1 profile artifact，不得新建公共 authority；task-cockpit 继续 reference-only。只有 W2 GREEN、resolver 全链 GREEN、8/8 non-placeholder exact refs、Bundle publish/install/rollback/revoke EvidencePack 与正负租户证据齐备后才可发布。结论 `PASS_AFTER_REMEDIATION`。

刷新证据：`.evidence/workshop/2026-08-15-w3-02-production-profile-resolver-refresh-preflight.json` 与 `.evidence/workshop/2026-08-15-w3-02-production-profile-resolver-refresh-doc-ledger.json`。最终状态保持 `NOT_STARTED / PREPARATION_REFRESHED_GREEN / HARD_GATE_BLOCKED / NO_EXTERNAL_EFFECT`。

提交前 authority 又推进至 `AOS-000039 / BIND1_2_CAPABILITY_READINESS_SERVICE_GREEN_WITH_WARNINGS`：exact CapabilityBinding readiness 与 activation revalidation 已完成，但真实 CapabilityBinding 仍为 0、Agent 仍不可运行，下一门为 BIND1_3 Skill publication/binding readiness。该进展没有生成八 Module profile refs 或 installed profile resolver，故本 ADR 的 W3-02 阻断结论不变；账本以 AOS-000039 完成闭合。

## 9. AOS-000041 / BIND1-3～4 差量复审

截至 AOS-000041，AIP 已完成 immutable Skill publication、SkillBinding readiness 及 CapabilityBinding/SkillBinding Canonical API/OpenAPI。这些能力为将来展示 assignee/binding readiness 提供了公共底座，但没有发布或解析八 Module 的 Brief/Evidence/Eval/Responsibility 生产 Profile。

第一轮差量复审逐项反证替代关系：published SkillRevision 不是 ProductionProfile artifact；SkillBinding/CapabilityBinding 不是 ResponsibilityTemplateRevision；zero-binding API 不是 installed signed artifact resolver；BIND1-5 strict SDK/UI 也不负责补齐领域 profile 内容。故 `DEP-C0-PROFILE-RESOLVER`、八 Module immutable descriptors、8/8 production/responsibility refs、六 placeholder 与两 legacy dry-run Eval 替换仍全部 RED。

第二轮复审冻结后续所有权：AIP/Asset Registry 提供通用 installed signed artifact exact resolver 与 strict SDK；Workshop DomainPack/SolutionPack 只在该 resolver 和 W2 门 GREEN 后，以新不可变 Bundle revision 贡献 profile artifacts。两者不能互相代替，也不得从当前 BIND1-4 API 推断 profile operational。差量证据见 `.evidence/workshop/2026-08-15-w3-01-02-bind1-4-dependency-refresh.json`。

结论保持 `NOT_STARTED / PREPARATION_REFRESHED_GREEN / HARD_GATE_BLOCKED / NO_EXTERNAL_EFFECT`；下一次重核触发点为 BIND1-5 Delivery Receipt、profile resolver 独立交付或 W2 数据/Registry 门变化。

## 10. AOS-000211 实施刷新与文件级清单

2026-08-24 在 `m1@0337370 / AOS-000211` 重新核验后，本 ADR 的历史阻断需要分拆：

1. “生产 router 未装配 resolver”已不再成立；`routers/aip_production_contracts.py` 已显式注入 `resolve_responsibility_template`。
2. 真实缺口仍在：当前 `aip_responsibility_template_authority.py` 只是共享静态 allowlist，不读取租户 active installation、composition lock、Registry published release 与 artifact digest，不能作为生产 exact authority。
3. 八个 Module 仍没有同版 typed Brief/Evidence/Eval/Responsibility profile；六个 placeholder 与两个 legacy dry-run 不得被冒充为生产 Eval profile。
4. W3-01 已交付只读 AgentRun/Handoff SDK 与 `原子 Skill → Logic exact ref → SkillBinding/数字同事 → Workshop blocker` 投影；W3-02 不复制该 authority，只提供 Logic/数字同事绑定前可解析的领域生产约束。

本波调整为两个串行最小切片，不等待外部开发者：

- `W3-02A`：用通用 `InstalledProductionProfileResolver` 替代静态 allowlist，必须同时匹配 tenant scope、active installation revision、exact composition lock、published signed release 与 artifact digest；未安装、跨租户、错误 hash、非 active/回滚旧 revision 和非发布版本全部失败关闭。Resolver 只返回布尔裁决，不返回 artifact payload，不新建生命周期 Store。
- `W3-02B`：为 DomainPack 和两个 SolutionPack 生成新的源 Bundle revision，以公共 strict schema 校验八份 production profile，将八个 Workshop contribution 的 `productionContractRefs`、`evalPackRefs`、`responsibilityTemplateRefs` 替换为本 Bundle 真实 artifact ref。旧签名 release 目录保持不变。

### 10.1 先方案后编码文件级清单

| 切片 | 文件 | 最小改动 |
|---|---|---|
| W3-02A | `services/aos-api/aos_api/aip_responsibility_template_authority.py` | 从静态 allowlist 收敛为安装态 exact artifact resolver，保持现有 Store callable 签名 |
| W3-02A | `services/aos-api/tests/aip/test_aip_responsibility_template_authority.py` | 覆盖正向 exact match 及跨租户、错 hash、未安装、回滚旧 revision、未发布负向 |
| W3-02B | `services/aos-api/aos_api/aip_production_profile_contracts.py` 与合同测试 | 定义不含电商执行分支的 strict production-profile envelope |
| W3-02B | `bundles/domains/ecommerce-core/` | 提升新源版本，新增 Brief/Evidence/Eval/Responsibility 公共 schema |
| W3-02B | `bundles/solutions/ecommerce-growth/` | 提升新源版本，新增 task/content/creator/media/analyst/price 六份 profile 并刷新 contribution refs |
| W3-02B | `bundles/solutions/ecommerce-operations-base/` | 提升新源版本，新增 operations/customer 两份 profile 并刷新 contribution refs |
| 累计门 | `services/aos-api/tests/asset_registry/test_workshop_module_contracts.py` 与 Bundle 邻接测试 | 8/8 refs 存在、0 placeholder、0 legacy dry-run 冒充、schema/Bundle-local ref 一致 |
| 证据 | `.evidence/workshop/2026-08-24-w3-02-production-profiles-exact-resolver.json` | 记录文件、测试、负向、副作用与 NO_RELEASE 边界 |

### 10.2 本波边界与退出门

- 只修改源 Bundle 与通用解析代码；不修改已冻结签名 release 目录，不真实 publish/install/rollback/revoke。
- 不新增 migration，不创建 Brief/Run/Action/Handoff，不发起 Provider 或业务副作用。
- `task-cockpit` 仍为 `reference-only`；必须保留来源 Module 的 frozen Brief 与职责 identity，不新建总控真源。
- 代码门要求 contract/resolver/Bundle/Workshop module 专项、API 累计回归、静态类型和差异复审全部 GREEN。本任务只可签发 `CODE_CONTROL_GREEN / NO_RELEASE`；真实运行仍必须消费后续的 publish/sign/install 与租户门证据。

状态更新为 `IN_PROGRESS / W3-02A_STARTED / NO_RELEASE / NO_EXTERNAL_EFFECT`。

### 10.3 累计回归否决与不倒退整改

W3-02B 首轮尝试直接将现有 `bundles/domains/ecommerce-core`、`bundles/solutions/ecommerce-growth`、`bundles/solutions/ecommerce-operations-base` author root 前移版本。Asset Registry 累计回归得到 `861 passed / 11 failed`：其中 10 项精确指向 M5 冻结 author/release 镜像、四 Bundle 依赖图与安装生命周期回归，证明“在原目录原地升版”违反不可变性；另 1 项为本波之前已存在的知识文档 PII 扫描失败，与 W3-02 差异无关。

整改决定：

1. 原样恢复现有三个 author root、`1.3.0` AIP publisher/version lock、历史 query template 与 M5 dependency range，不改旧测试来掩盖回归。
2. 新版改放在 `bundles/candidates/ecommerce/<bundle-id>/<version>/`，每个 candidate 是上一不可变版本的完整 successor 副本，再叠加 schema/profile/contribution refs；不写入 `bundles/releases/`。
3. candidate 单独通过 ManifestLoader、profile strict contract、8/8 ref 与“旧资产集合不减少”测试；只标记 `AUTHORING_CANDIDATE_GREEN / NO_RELEASE`。
4. 只有后续真实 publish/sign/install 门才能把 candidate 转成 Registry release；本波不执行该过程。

文件级清单据此修正：第 10.1 节的三个 Bundle 目标改为上述 `bundles/candidates/ecommerce/...` versioned 目录，现有 author root 仅作为差异基线，不在写 scope 内。

### 10.4 实施结论与验收

W3-02A/B 已按整改后路径闭合：

1. `InstalledProductionProfileResolver` 已收紧为 tenant active installation、active revision、composition lock、Registry published signed artifact 与 exact digest 的联合裁决；未安装、跨租户、错 hash、旧 revision、未发布/未签名与存储异常全部失败关闭。
2. `domain.ecommerce.core@1.1.0`、`solution.ecommerce.growth@1.4.0`、`solution.ecommerce.operations-base@1.2.0` 以 versioned candidate 形式交付；8/8 Module 的 production/Eval/responsibility ref 均指向同 Bundle 的 strict profile，新增 5 类共享 schema，并保证历史资产集合不减少。
3. 专项回归 `28 passed`，AIP/Registry 邻接回归 `18 passed`，Python compile GREEN；Asset Registry 累计回归 `843 passed / 3 failed`，3 项均精确定位为 W3-02 差异之外的既有 author-root 基线问题，而三个历史 author root 的 Git 差异为 0。
4. 内置浏览器验收 `/workshop`：API 不可用时页面明确显示离线、目录读取失败与 0 active installation，没有把 candidate 伪装成已安装或可运行。

结论为 `W3_02_INSTALLED_EXACT_RESOLVER_AND_8_PROFILE_CANDIDATES_CODE_GREEN_NO_RELEASE`。本结论只关闭代码/候选资产门，不授权 publish/sign/install，不产生 Provider、Action 或真实业务副作用。详细证据见 `.evidence/workshop/2026-08-24-w3-02-production-profiles-exact-resolver.json`；下一任务为 `W3-03` prepare 聚合。
