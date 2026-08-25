# W8-01 洞察→GrowthPlan→内容/达人/媒体→发布→复盘同链预检 ADR

> 日期：2026-08-15
> 决策：`NOT_STARTED / SCENARIO_CONTRACT_APPROVED / HARD_GATE_BLOCKED / NO_EXTERNAL_EFFECT`
> 前置：产品正式封板；W2-10、W3-14、W4-08、W5-08、W6-10、W7-11、DEP-A8 当前 release 全 GREEN

## 1. 当前事实

技术基线已正式审查封板，用户也已授权 W1～W8 连续开发；但产品状态仍为 `SUBSTANTIALLY_COMPLETE_DRAFT / FORMAL_REVIEW_PENDING / NOT_FROZEN`。W8-01 的七个技术/累计依赖全部未 GREEN：八页数据/浏览器、公共编排/领域 authority、Evidence/Eval/Wiki、外部 Action、内容/达人闭环、多媒体累计门和 AIP-8 均未闭合。

因此本轮只能收敛可执行 E2E 合同，不能用 fixture、Mock Provider、静态页面或手工拼接 refs 运行“成功场景”。连续开发授权不等于真实发布、租户写入或 release 授权。

## 2. 同链合同

一个 approved exact `GrowthPlanRevision` 是场景根，`scenarioBindingHash` 覆盖：

1. MetricDefinition/Observation quality 与 cutoff；
2. AnalysisBrief/EvidenceBundle/EvalContract；
3. InsightRevision/DecisionSummary 的证据、归因、假设、反证和不确定性；
4. GrowthPlan 目标、约束、预算、预期、停止条件与 Approval；
5. canonical TaskGraph 与每个 HandoffDecision；
6. Campaign/Content Brief、Creator collaboration、Media Responsibility/Run/Artifact/GateSet；
7. PublishCandidate/Impact/Action/Approval/Lease/Receipt/reconcile；
8. Usage/Settlement、EffectReview 与 MemoryCandidate。

跨 Module 只传 scoped refs、purpose 和 requestedOutcome，不复制正文、客户/达人资料或媒体 payload。任何页面切换、刷新或重启都从同一 binding 恢复，不选择“最新记录”补洞。

## 3. 守恒与多轴状态

- GrowthPlan materialize 的 Task 数、Handoff 子任务、批次 item 与最终 outcome 可对账；
- offered/accepted/rejected/request-more/returned 分别有 Receipt，accept 不等于完成；
- Campaign 批准、Artifact 四门/批准、发布 Action 批准相互独立；
- Provider applied、Usage settled、Effect mature、Candidate governed/promoted 是四个独立轴；
- stale/revoked/conflict/partial/forbidden/unknown/kill/budget 只允许受权的下一步；
- 不存模型私有思维链，只存决策摘要、证据链、归因路径、关键假设和不确定性；
- EffectReview 不成熟或证据不足时不得产出“已验证经验”或自动晋升 Wiki。

## 4. 正式 EvidencePack

必须包含当前 release 的全部依赖 Receipt、真实 HTTP 浏览器跨 analyst/content/creator/media/total-control/review 链、`org-org/dev-project` 正向 authority 对账、`dev-org/dev-project` 负向隔离、DOM/network/console/database/lineage 证据，以及 stale metric、revoked evidence、missing capability、rejected Handoff、provider unknown、kill 和 revision conflict 负向旅程。真实发布 canary 另需 exact target/account/budget/time/stop 条件的独立授权。

## 5. 两轮审查

### 第一轮：业务闭环与信息守恒

- 洞察、计划、内容、达人、媒体、发布和复盘均从一个 GrowthPlan 根可达；
- Handoff、Task、Artifact、Action、Usage、Effect 与 Candidate 状态不互相冒充；
- 跨 Module 最小披露与数量守恒清晰；
- 决策可解释但不保存私有思维链。

结论：`PASS`。

### 第二轮：执行资格与副作用

- 产品封板和七个依赖均为硬门；
- Mock/fixture/静态视觉不构成正向 E2E；
- continuous development authorization 不替代 publish canary/release authorization；
- 当前不创建租户数据、不启浏览器写路径、不调用 Provider。

结论：`PASS_WITH_HARD_GATE_BLOCKED`。

## 6. 最终裁决

W8-01 场景合同可作为未来 E2E 施工与验收基线；当前不得运行或勾选。预检事实见 `.evidence/workshop/2026-08-15-w8-01-insight-growthplan-content-creator-media-publish-review-preflight.json`。

## 7. 2026-08-26 串行施工更新（编码前方案）

### 7.1 基线复核与实施裁决

当前 authority 为 `AOS-000267`。W2～W7 的工程代码/合同/浏览器清单已闭合，但 W7-11 明确保留 Provider Adapter、publish canary、operational-ready 三个外部门，因此 W8-01 不运行真实发布 E2E，也不创建租户业务事实。本波先完成可独立验收的 GET-only 场景贡献：以 exact `GrowthPlanRevision` 为唯一场景根，把洞察、内容、达人、媒体、发布、Usage/Settlement、EffectReview、MemoryCandidate 作为同一个 `scenarioBindingHash` 下的独立阶段和独立结果轴；缺根、跨租户、跨 cutoff、跨 binding、数量不守恒或外部状态不确定时失败关闭。

### 7.2 163/164 分层落位

- 原子 Skill：每个阶段只消费租户内 exact Capability/Skill/Evidence ref，不复制能力真源；
- Logic 编排：`GrowthPlanRevision` 与 `TaskGraphRevision`、Handoff、Campaign/Media/Action refs 共同参与 binding，不选择“最新记录”补洞；
- 数字同事绑定：只展示可验证 Binding/AgentRun ref；没有 exact ref 时保持 unknown，不按岗位名称伪造运行主体；
- 工作台贡献：Analyst v2 展示 GrowthPlan 根、八阶段同链、任务/Handoff/Outcome 守恒和 Provider/Usage/Effect/Memory 四轴，仍保持写入口 0。

### 7.3 文件级实施清单

后端：

1. 新增 `services/aos-api/aos_api/ecommerce_workshop_growth_scenario_contracts.py`，冻结场景根、阶段、exact refs、守恒 ledger、四结果轴、blocker 和全部禁用命令；
2. 新增 `services/aos-api/aos_api/ecommerce_workshop_growth_scenario.py`，定义 bounded canonical reader 组合边界；无可信 observation 时返回结构化 blocked，不制造 GrowthPlan 或业务结果；
3. additive 扩展 `ecommerce_workshop_analyst_contracts.py`、`ecommerce_workshop_analyst.py` 与现有 GET router，使 Analyst v2 返回场景贡献；v1 保持可读；
4. 新增专项测试并扩展 Analyst/OpenAPI 回归，覆盖同链、跨租户/cutoff/binding、缺阶段、数量不守恒、provider unknown、effect immature、MemoryCandidate 不自动晋升。

前端：

1. additive 扩展 `apps/web/src/api/ecommerceWorkshop/contracts.ts` 与 `parser.ts`，严格解析 v2 exact binding、八阶段、守恒 ledger 与四轴，拒绝任何可执行命令或成功伪状态；
2. 新增 parser 测试，扩展 `AnalystPage.tsx` 与测试，在视觉上呈现“洞察 → GrowthPlan → 内容 → 达人 → 媒体 → 发布 → 复盘”同链和“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”；
3. 更新 OpenAPI 生成物，完成专项/累计/Web 全量/TypeScript/build/security，再用内置浏览器验证 1280/1440/1920、七 Tab 键盘、刷新、无溢出、无写入口。

证据与记忆：形成独立 evidence、Delivery Receipt 和安全提交；最后才串行 CAS 更新 authority、01/06 与 Prime，并自动进入 W8-02。

### 7.4 不变式、回滚与明确不做

- 不 apply 共享迁移，不写 `org-org/dev-project`，`dev-org/dev-project` 只作负向合同；
- 不调用 Provider，不 execute/reconcile/retry/publish，不运行真实 canary，不 release；
- accepted 不等于 completed，Provider applied、Usage settled、Effect mature、MemoryCandidate governed/promoted 四轴不互相推导；
- 页面只存决策摘要、证据链、归因路径、关键假设和不确定性，不存私有思维链；
- 回滚只移除 Analyst v2 场景字段和对应 UI，现有 Analyst v1 七视图与 W2～W7 读模型保持不变。

## 8. 2026-08-26 实施、复审与验收结论

W8-01 已完成 GET-only Analyst v2 同链贡献实现。新增严格的 `GrowthScenarioContribution`，固定八阶段顺序，并把 Provider applied、Usage settled、Effect mature、Memory governed 保持为四个独立结果轴；`GrowthPlanRevision` 必须与 `growth_plan` 阶段 exact ref 完全一致，binding、租户或 cutoff 漂移均返回不含可信 refs 的结构化 blocked。全部阶段与结果轴均 ready 时也不会被解释为运营放行，而是稳定降级为 `GROWTH_SCENARIO_OPERATIONAL_AUTHORIZATION_REQUIRED`。

验收事实：

- 后端场景、Analyst、Workshop API 与 OpenAPI 回归 `32 passed / 7 warnings`；OpenAPI 保持 `2666 paths`，schema 增至 `2398`；
- Web 专项 `2 files / 6 tests`，全量 `236 files / 2156 tests`，TypeScript 与 production build `344 modules` 通过；
- sensitive scanner 自测 `9 passed`，本任务 `15 files / 0 critical / 0 warning`；全仓既有安全基线仍为 RED，因此不宣称 release GREEN；
- 内置浏览器通过 1280/1440/1920，确认 8 阶段、4 结果轴、7 语义 Tab、方向键实际切换、`GROWTH_PLAN_EXACT_ROOT_REQUIRED` 失败关闭状态，以及业务写按钮为 0；
- 页面和合同持续采用“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”，没有把岗位名称、fixture 或页面可见冒充 exact AgentRun/Binding；
- 未 apply 共享迁移、未写真实租户、未调用 Provider、未物化/派发计划、未发布、未晋升 Memory/Wiki、无外部副作用、无 release。

代码提交 `89f6fbe5`，证据提交 `eac191f9`；证据包为 `.evidence/workshop/2026-08-26-w8-01-growth-scenario-exact-binding.json`，浏览器图为 `.evidence/workshop/2026-08-26-w8-01-browser/analyst-growth-scenario-1920.jpg`。工程退出裁决：`W8_01_GROWTH_SCENARIO_EXACT_BINDING_CODE_CONTRACT_BROWSER_GREEN_SECURITY_SCOPED_GREEN_OPERATIONAL_FAIL_CLOSED_NO_EXTERNAL_EFFECT_NO_RELEASE`。这只关闭 W8-01 的工程清单，不解除真实 Provider、Canary、Action、发布或 release 门；下一串行入口为 W8-02。
