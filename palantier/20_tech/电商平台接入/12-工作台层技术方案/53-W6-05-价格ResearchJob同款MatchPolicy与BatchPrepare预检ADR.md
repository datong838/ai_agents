# W6-05 价格 ResearchJob、同款 Match、Policy 与 Batch Prepare 预检 ADR

> 日期：2026-08-14  
> Authority：`AOS-000027`  
> 代码基线：`w2-workshop@0e480b18f6c286484fbff631149fc604cca742e6`  
> 证据：`.evidence/workshop/2026-08-14-w6-05-price-research-match-policy-batch-prepare-preflight.json`  
> 结论：`GENERIC_FOUNDATIONS_GREEN / PRICE_DOMAIN_AND_BATCH_PREPARE_BLOCKED`

## 1. 审查结论

通用 ResearchJob、TaskBrief/Evidence/Eval/Impact 与安装 Shell 可复用，定向后端 22 项、前端 18 项通过。但当前没有 PriceObservation、同款 Match Decision、MonitoringPolicy、PriceCase、聚合 originals 或 PriceResearchBatch authority；Module 四类 exact refs 为空、Eval placeholder。故 W6-05 不能勾选，也不能把对象名清单或通用采集底座冒充价格治理。

## 2. 关键边界

- external Artifact 是来源事实，不覆盖 Product/ProductSku 价格真源；
- ComparisonSnapshot/趋势是可重建投影，每个值必须可达 originals；
- Match Observation 与人工/政策 Decision 分离，低置信度保持 PRELIMINARY；
- MonitoringPolicy 是版本化 authority，不是前端阈值或任意 JSON；
- batch prepare/freeze 为零 provider/零通知/零调价副作用，start 另行授权；
- 调研 capability 与通知、建议、调价 capability 独立。

## 3. 决策

1. 冻结 PriceResearchProfile、Observation Schema、required-facts、Match feature/policy、MonitoringPolicy 与 Batch Schema；
2. 建立 tenant-scoped 领域 authority、RLS/append-only/CAS/Receipt；
3. 以 canonical ResearchJob Artifact 进入受控 Normalizer，显式价格口径并保留 originals；
4. 实现 Match Observation/Decision/PRELIMINARY 与漂移 invalidation；
5. 实现 Policy/Eval 驱动的 PriceCase，不把聚合投影当事实；
6. 实现 side-effect-free batch prepare/freeze、item 数量守恒和 rate/capacity/budget；
7. 更新 Bundle exact refs、Module API/SDK/三视图；
8. 累计 contract/store/API/frontend/security 验收，W6-06 外部动作不得提前。

## 4. 当前阻断与解除条件

| ID | 当前事实 | 解除条件 |
|---|---|---|
| `DEP-W6-PRICE-DOMAIN-AUTHORITY` | 领域 contract/store/service/API 为 0 | additive authority 与 tenant/CAS/Receipt GREEN |
| `DEP-W6-PRICE-BUNDLE-CONTRACT` | exact refs 为空、Eval placeholder、actionTypes 空 | 发布锁定 refs 并移除 placeholder |
| `DEP-W6-PRICE-RESEARCH-PROFILE` | 无来源/URL/许可/口径/rate profile | 签名 profile 与 Adapter contract GREEN |
| `DEP-W6-PRICE-OBSERVATION-NORMALIZATION` | 无规范化/原始证据映射 | 多口径、unknown/not-comparable、hash 测试 GREEN |
| `DEP-W6-PRICE-EVIDENCE-SELECTION` | coverage/freshness/license 由调用方自报 | price required-facts BuildJob GREEN |
| `DEP-W6-PRICE-MATCH-AUTHORITY` | 无 Observation/Decision/PRELIMINARY | 同版 feature/model/policy/evidence GREEN |
| `DEP-W6-PRICE-POLICY-AUTHORITY` | 无 MonitoringPolicy revision | scope/basis/threshold/freshness/Eval authority GREEN |
| `DEP-W6-PRICE-BATCH-PREPARE` | 无 prepare/freeze/CAS/零副作用 | 数量守恒、幂等、0 ResearchJob/Action 测试 GREEN |
| `DEP-W6-PRICE-AGGREGATION-ORIGINALS` | 无 originals reachability/rebuild | 去重、迟到、单位/币种、重建对账 GREEN |
| `DEP-W6-PRICE-READ-MODEL` | 只有公共 Shell | 三视图、Match/Policy Diff/Batch/a11y GREEN |
| `DEP-W6-PRICE-UPSTREAM-GATES` | W4-08、W6-01 未勾选 | 两项正式 GREEN 后重新核验 |

## 5. 双轮审查记录

### 第一轮：事实、口径与真源

- PASS：Product/ProductSku 与外部 Observation/聚合投影边界明确；
- PASS：币种、单位、优惠、税费、运费与 not-comparable 进入规范化契约；
- PASS：Match Observation/Decision 与 Policy/Eval exact refs 分离；
- 整改：原方案未定义 originals 守恒、批次数量守恒和手动导入门，已补齐。

### 第二轮：可施工性与动作隔离

- PASS：每个 P0 缺口有稳定 ID 和解除条件；
- PASS：prepare 0 provider/通知/调价，调研可用不点亮调价；
- PASS：unknown/reconcile、漂移、可重建聚合与三视图均可验；
- PASS：当前保持 `NOT_STARTED / IMPLEMENTATION_BLOCKED`，未越过 W6-06/W5。

## 6. 复审结论

W6-05 目标契约通过文档复审，当前实现未通过。安全入口是在 W4-08/W6-01 GREEN 后按第 3 节建立领域 authority；禁止先抓外部页面、先写调价按钮或用 placeholder/mock 构造价格异常。

## 7. 2026-08-25 施工复审与文件级子波

### 7.1 实时前置重核

- Authority：`AOS-000248`；施工代码基线：`aos-platform/m1@1aad7b6`；唯一开发者在 `m1` 串行施工。
- `W4-08` 已闭合跨 Bundle/Eval/Wiki/ResearchJob 累计代码与浏览器门，`W6-01` 已闭合 exact capability/assignee/readiness，`W2-07` 已提供严格只读价格视图。因此本 ADR 第 4 节的 `DEP-W6-PRICE-UPSTREAM-GATES` 已解除，领域施工入口成立。
- 通用 ResearchJob、SkillRevision、LogicPublicationRevision、AgentBindingRevision 仅作为 exact authority 引用；W6-05 不创建 ResearchJob、不调用 Provider，不把通用 authority 冒充价格事实。
- 真实租户仍只认 `org-org/dev-project`，`dev-org/dev-project` 仅作隔离负向；本波不 apply migration、不修改真实业务数据、不触发通知、调价、Canary 或发布。

### 7.2 163/164 组合落位

W6-05 按“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图”施工，不新增大而全的价格 Skill：

1. 原子 Skill：`discover-price-sources`、`normalize-price-observations`、`match-comparable-products`、`evaluate-price-policy`、`prepare-price-research-batch`；
2. Logic：`ecommerce-price-governance`，只绑定 exact Skill revisions，不在工作台复制 AIP 编排器；
3. 数字同事：`数据参谋`主责，`活动策划师`与`导购顾问`协作；binding 漂移即 contribution/readiness 失败关闭；
4. 工作台：只展示贡献链、Price authority、批次守恒与 blocker；本波不提供 start/notify/reprice 按钮。

### 7.3 子波与文件级清单

| 子波 | 最小改动 | 验收 |
|---|---|---|
| `W6-05A` | 本 ADR、`16-价格治理技术方案.md`、D-waves 总清单 | 方案、边界、exact refs 与施工顺序一致 |
| `W6-05B` | `ecommerce_workshop_price_research.py`、`ecommerce_workshop_price_research_store.py` | Profile、Normalizer、Match Observation/Decision、Policy、prepare/freeze 严格合同；append-only/CAS/租户隔离 |
| `W6-05C` | `routers/ecommerce_workshop.py`、`scripts/export_openapi.py`、`packages/contracts/openapi/v1.generated.json`、`v1.inventory.json` 与 OpenAPI 测试 | 内部 authority 命令与贡献只读 API；8 个新增操作进入确定性合同基线；typed error；零 Provider/ResearchJob/Action |
| `W6-05D` | `alembic/versions/w6_005_price_research.py` 与迁移合同测试 | additive、RLS/FORCE RLS、唯一 head；只验证、不 apply |
| `W6-05E` | Web contracts/parser/client、`PriceGovernancePage.tsx` 及测试 | strict contribution view；失败关闭；无外部动作控件 |
| `W6-05F` | 专项＋W6 累计回归、build、内置浏览器、diff/方案复审、Evidence/Receipt/CAS/Prime | 能力不倒退，代码/合同/浏览器闭合后才勾选 W6-05 |

### 7.4 本波关闭口径

`prepare/freeze` 只能固化输入、exact refs、逐项处置和数量台账；`provider_call_count = research_job_count = notification_count = action_proposal_count = repricing_count = external_effect_count = 0`。任何许可、original、口径、Match、Policy/Eval、Skill/Logic/Agent binding、rate/capacity/budget 漂移均使批次 stale 或阻断。W6-05 GREEN 仅表示价格领域代码/合同/浏览器 prepare 门闭合，不授予 W6-06 外部通知或调价权限。

## 8. 2026-08-25 实施与验收封存

- 实现提交：`aos-platform/m1@de8eaf4`。已新增 tenant-scoped append-only Profile、Observation、Match Observation/Decision、MonitoringPolicy 与 PriceResearchBatch prepare/freeze authority；exact ref、content hash、version/CAS、数量守恒及零副作用计数均进入强类型合同。
- 公共合同：新增 8 个内部 authority/贡献操作；确定性 OpenAPI 为 `2616 paths / 2248 schemas / 4395 route rows / 4385 unique operations`，双清洁进程导出 GREEN，未删除或放宽旧合同断言。
- 测试：W6 与 API/OpenAPI 累计 `56 passed`；前端专项 `2 files / 6 tests passed`，全量累计 `227 files / 2115 tests passed`；生产 build `343 modules`，compileall、diff check、`w6_005` 唯一 head GREEN。迁移仅验证，未 apply。
- 浏览器：内置浏览器在 `org-org/dev-project` 的 `/workshop/price-governance` 验证贡献链、数据参谋主责、协作同事、可信空 batch、零 Provider/ResearchJob/external effect、无 start/notify/reprice 控件；P01/P03/P07/P09/P11 当前失败事实保持可见，未被页面提升。
- 安全结论：未读写真实业务数据，未创建 ResearchJob，未调用 Provider，未发送通知，未创建 Action/调价 Proposal，未发布。

结论：`W6_05_CODE_CONTRACT_BROWSER_GREEN / NO_PROVIDER / NO_RESEARCH_JOB / NO_EXTERNAL_EFFECT / NO_RELEASE`。W6-05 可以勾选；下一串行任务为 W6-06，仍须独立建立通知、建议、Handoff 与调价分门，不能借 W6-05 GREEN 点亮外部动作。
