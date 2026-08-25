# W7-02 Profile 建议、成本区间与用户确认预检 ADR

> 日期：2026-08-15；2026-08-25 唯一开发者串行复核并开工
> 状态：`COMPLETED_CODE_CONTRACT_BROWSER_GREEN / NO_EXTERNAL_EFFECT / NO_RELEASE`
> 范围：W7-02 Profile 建议、预计成本区间、用户确认与只读贡献视图；只新增迁移定义，不 apply 数据库，不操作真实租户。

## 1. 结论

本节记录 2026-08-15 预检时的历史结论：当时 W7-01 尚未实现，且 ProfileRecommendation、ProfileConfirmation、MergePolicy、ProjectedCost 与对应 UI authority 均不存在，因此不能编码。该结论已由第 8 节 2026-08-25 独立复核解除，不代表当前状态。

本 ADR 冻结目标合同，使后续实现不以自由文本档位、静态前端报价、本地确认状态或预计成本覆盖实际费用。

## 2. Recommendation 唯一合同

`ProfileRecommendationRevision` 是租户域不可变 revision，至少固定：

- Brief/Evidence/Eval、ResponsibilityTemplate、MergePolicy、组织 Policy、ProviderPrice exact refs；
- `LITE | STANDARD | FULL` 稳定 profile key、policy floor、推荐理由与风险提升规则；
- required/optional/merge-candidate responsibilities、coverage 与职责分离结论；
- `ProjectedCostRange[]`、`ProjectedDurationRange`、assumptions、confidence、unknown、createdAt/expiresAt；
- recommendationId、revision、contentHash、readiness、blockers 与 staleReasons。

相同 frozen 输入、策略和价目表必须产生相同 content hash。LLM 可以生成解释，但不能决定未受 Policy authority 约束的档位、价格或降档。

## 3. 成本权威边界

`ProjectedCostRange` 按币种保存 ProviderPrice exact ref、Stage 数量假设、单价、税费/平台费、许可证费用、重试/冗余预留、lower/upper、unknown、confidence 与 expiry。

- 不同币种不自动折算或相加；需要折算时必须引用 exact FX source/policy；
- 缺单价、数量上界、许可证费或 Provider readiness 时保留 unknown，不显示为 0；
- projected/estimated 不可直接扣减 hard budget；
- 实际费用唯一来自 UsageReceipt → Attribution → Adjustment/Reconcile，并继续区分 measured/estimated/unknown；
- UI 同时展示预计区间、已发生费用与差异原因，任何一方不得覆盖另一方。

## 4. 用户确认合同

`ProfileConfirmationReceipt` 固定 recommendation exact ref/hash、选择结果、actor/reason、policy decision、确认前后职责/成本差异、ETag/CAS、Idempotency-Key 与 createdAt。

确认只表达“接受此版本方案和预算区间”，不 freeze ResponsibilityPlan、不启动 TaskRun、不调用 Provider、不发布外部内容。降档不得低于 policy floor；升档与合法降档都先产生新 Recommendation。网络结果 unknown 时查询并按原 command envelope 恢复，不能生成第二个不同确认。

Brief、Evidence、Eval、template、MergePolicy、Policy、ProviderPrice、license、budget 或 readiness 漂移后，Recommendation 与 Confirmation 一并 stale；必须重算并重新确认。

## 5. 现场事实与缺口

机器证据：`.evidence/workshop/2026-08-15-w7-02-profile-cost-confirmation-preflight.json`。

已验证基础：generic ResponsibilityPlan/StageTemplate DTO/store 存在；事后成本归因能区分 measured/estimated/unknown，并在 unknown/estimated 时拒绝 hard-budget eligibility；前端 Usage parser 保留质量与币种不变量；媒体 Module 声明十项 canonical Capability。

阻断项共 13 项：W7-01 未 GREEN；Recommendation、Confirmation、MergePolicy、ProjectedCost authority 缺失；profile 非 exact enum；价目/数量/币种/税费/许可证/expiry 模型缺失；policy floor 缺失；确认 CAS/幂等缺失；漂移失效链缺失；Module 模板 refs 为空且 Eval placeholder；UI/SDK 缺失；租户隔离未证明。

## 6. 实施顺序与测试门

1. W7-01 实现并发布可安装的 exact templates；
2. 建立 Recommendation/ProjectedCost/MergePolicy revision authority 与确定性 hash；
3. 建立无副作用 Confirmation command、CAS/幂等/unknown recovery；
4. 将确认 ref 纳入 ResponsibilityPlan freeze/start 组合门并实现 drift invalidation；
5. 建立 SDK/UI，展示理由、policy floor、职责、预计/实际成本、unknown、expiry 和修复动作；
6. 覆盖确定性、过期、升降档、unknown、多币种、价格漂移、重放、跨租户和 `org-org/dev-project` 正向证据。

## 7. 双轮复审

### 第一轮：业务与产品边界

- 建议不替用户决策，确认不暗中启动：通过；
- 预计成本与实际费用不混淆：通过；
- unknown、假设、置信度和有效期对用户可见：通过；
- 降档不突破 policy floor：通过。

### 第二轮：技术与安全边界

- exact refs、不可变 revision、CAS/幂等和漂移失效完整：通过；
- 多币种、price/license unknown、hard-budget fail-closed 完整：通过；
- 当前 13 项缺口与依赖保留，未误写为实现完成：通过；
- 未改代码、数据库、真实租户或外部系统：通过。

结论：W7-02 **合同基线通过**，实现仍保持未开始。

## 8. 2026-08-25 独立复核与实施裁决

本次不沿用 2026-08-15 的历史阻断结论，而按当前代码、W7-01 Receipt 与 active authority 重新核验：

1. W7-01 已在 `AOS-000255` 形成 LITE/STANDARD/FULL Stage/Responsibility signed-installable candidate 资产、八责任/十 Capability exact mapping 与 active-installation typed resolver，代码/合同/浏览器切片 GREEN；Candidate 仍不冒充已发布或已安装。
2. W6-02 已提前建立 `ResponsibilityProfile` exact enum、`MergePolicyRevision`、`ProfileRecommendationRevision`、`ProfileConfirmationReceipt`、租户表/RLS 与 ResponsibilityPlan freeze 组合门；因此不重建第二套 Recommendation/Confirmation 真源。
3. 当前真实缺口收敛为：Recommendation 尚未冻结 Brief/Evidence/Eval/Stage/Responsibility/ProviderPrice/license 等完整 exact 输入；尚无结构化 `ProjectedCostRange`、duration、assumptions/confidence/unknown；Confirmation 缺 expected ETag/CAS 与明确幂等 command envelope；前端仅展示计划已有 ref，不能读取建议、预计成本和确认差异。
4. 实际 Usage/Attribution 现有权威保持不变。W7-02 只新增预计成本 authority 与只读/确认入口，unknown 不得显示为 0，预计值不得扣减 hard budget，也不得自动 freeze/start。
5. 163/164 的分层继续适用：成本估算和方案比较属于原子 Skill 输出，Profile 选择由 Logic + Policy 编排，数字同事只绑定责任，工作台只展示建议、假设、证据、贡献和阻断；Tool/Provider/外部发布门不下沉到 Skill。

历史十三项阻断中，W7-01、exact profile/merge/confirmation 基座、Module Stage/Responsibility refs 与租户隔离已解除；其余缺口由本波直接实现，不等待外部开发者。数据库 migration 仅形成定义与测试，不在本波 apply。

## 9. 2026-08-25 文件级施工清单

1. 扩展唯一 profile authority 合同：增加预计成本币种分组、数量/单价/税费/平台费/许可证/冗余、lower/upper、unknown、confidence、expiry、duration、assumptions 与完整 exact dependency refs；不同币种禁止自动合并。
2. 扩展 store：确定性 snapshot/content hash；exact price/template/policy 校验；过期、缺价、unknown 与 drift 失败关闭；Confirmation 增加 expected recommendation hash、expected revision/ETag 和 Idempotency-Key，重放返回同一 Receipt，冲突拒绝。
3. 新增只读 list/get Recommendation/Confirmation API，并使写命令显式消费幂等键；不在确认成功后 freeze ResponsibilityPlan、创建 TaskRun 或调用 Provider。
4. 新增 `w7_001` 迁移定义，为现有 append-only Recommendation/Confirmation 表补充预计成本、完整依赖快照和 command envelope 列及约束/RLS 兼容；只验证单头与 migration contract，不执行 apply。
5. 给媒体 Bundle candidate 增加预计成本合同资产并回填 `impactCalculatorRefs`；它只描述 schema/边界，不携带真实价格或租户数据。
6. 扩展 Web SDK/parser 与生产合同页：读取建议、policy floor、预计区间、unknown、假设、有效期、确认差异；确认按钮仅对服务端返回的当前 Recommendation 开放，网络 unknown 后刷新权威，不本地伪造成功。
7. 覆盖确定性、多币种、unknown、过期、升降档、价格/模板漂移、CAS、幂等重放/冲突、跨租户、UI 失败关闭和迁移 RLS；再执行累计后端、Web 全量/build、OpenAPI/Router、安全和内置浏览器三视口验收。
8. 形成 Evidence、Delivery Receipt、安全提交、authority CAS 与 Prime 回读后自动进入 W7-03。

预计代码范围：

- `services/aos-api/aos_api/aip_responsibility_profile.py`
- `services/aos-api/aos_api/aip_responsibility_profile_store.py`
- `services/aos-api/aos_api/routers/aip_production_contracts.py`
- `services/aos-api/aos_api/routers/domain_manifest.json`
- `services/aos-api/alembic/versions/w7_001_profile_projected_cost_confirmation.py`
- `services/aos-api/tests/aip/test_w7_02_profile_cost_confirmation.py`
- `services/aos-api/tests/aip/test_w7_02_profile_cost_confirmation_migration.py`
- `services/aos-api/tests/aip/test_w6_02_responsibility_profiles.py`
- `apps/web/src/api/aipProductionContracts/contracts.ts`
- `apps/web/src/api/aipProductionContracts/parser.ts`
- `apps/web/src/api/aipProductionContracts/index.ts`
- `apps/web/src/api/aipProductionContracts/index.test.ts`
- `apps/web/src/pages/s2/ProductionContractsPage.tsx`
- `apps/web/src/pages/s2/ProductionContractsPage.test.tsx`
- `bundles/candidates/ecommerce/solution.ecommerce.growth/1.4.0/**`
- `.evidence/workshop/2026-08-25-w7-02-profile-cost-confirmation.json`

若实现中必须扩大范围，先回写本 ADR 与 Task Lease，再改代码。

## 10. 2026-08-25 实施与验收封板

W7-02 已按第 8/9 节完成，且没有新建第二套 Profile 真源：

1. 在现有 `ProfileRecommendationRevision`、`ProfileConfirmationReceipt` 与 `MergePolicyRevision` 上补齐 TaskBrief/Evidence/Eval/Stage/Responsibility/Policy/ProviderPrice exact dependency snapshot、按币种分组的 `ProjectedCostRange`、`ProjectedDurationRange`、assumptions/confidence/unknown/expiry 与确定性 hash。
2. Recommendation 对模板、Policy、价目有效期和 exact hash 漂移失败关闭；不同币种不相加，缺价保持 unknown 且不能伪装为 0。
3. Confirmation 使用 `If-Match` CAS 与 `Idempotency-Key`，同键同命令返回同一 Receipt，同键异命令拒绝；确认不 freeze ResponsibilityPlan、不创建 TaskRun、不调用 Provider、不扣 hard budget。
4. 媒体 Candidate 新增 fail-closed 成本投影合同并由 Module exact 路径引用；工作台展示 LITE/STANDARD/FULL 建议、预计区间、unknown、时长、假设和确认入口。
5. 分层保持 163/164：原子 Skill 产出成本/时长事实，Logic + Policy 选择 Profile，数字同事只绑定职责，工作台只展示建议、证据、假设、贡献与阻断。

验证结果：

- 专项与邻接后端 `11 passed`；OpenAPI/Router `22 passed + 2 subtests`；迁移单头 `w7_001`，未 apply 真实数据库。
- Web 专项 `2 files / 23 tests`，累计 `232 files / 2132 tests`，生产构建 `344 modules`。
- 定向安全扫描 `15 files / critical=0 / warning=0`；Python 编译、Candidate JSON 与 `git diff --check` GREEN。
- 内置浏览器 `768/1440/1920` 三视口无横向溢出，STANDARD 建议、CNY 已知区间、FULL `LIVE_VIDEO_PRICE_UNKNOWN`、预计时长与确认入口可见，console error 0；未点击确认，未产生业务写入。

证据：`.evidence/workshop/2026-08-25-w7-02-profile-cost-confirmation.json`。结论：`W7_02_PROFILE_PROJECTED_COST_CONFIRMATION_CODE_CONTRACT_BROWSER_GREEN_NO_EXTERNAL_EFFECT_NO_RELEASE`，自动进入 W7-03。
