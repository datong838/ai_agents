# W8-06 批量准备、显式启动、Partial/Unknown/Reconcile 预检 ADR

> 日期：2026-08-15  
> 决策：`NOT_STARTED / SCENARIO_CONTRACT_APPROVED / HARD_GATE_BLOCKED / NO_EXTERNAL_EFFECT`  
> 前置：产品正式封板；W4-08、W5-08、W6-10 当前 release 全 GREEN；共享批次 runtime 齐备

## 1. 当前事实

达人邀约、客户触达、内容生产、价格调研和 Wiki 资料吸收都需要“先准备、再显式启动”，但仓内只有通用 Action/reconcile、ResearchJob 或各领域零散合同，没有一个 canonical `BatchPreparationRevision + BatchStartDecision + child item outcome` authority。三个累计依赖均未 GREEN，产品也未封板。

因此本轮只冻结公共批次语义；不执行查询、触达、调价、发布、知识晋升或收费 Job，不拿任一领域的 Mock batch 冒充共享闭环。

## 2. 准备与启动绑定

exact `BatchPreparationRevision` 是场景根，`batchStartBindingHash` 至少覆盖：

1. QueryDefinition revision、cutoff、purpose 与 target snapshot hash；
2. candidates/originals 和 deterministic item keys；
3. dedupe、consent、license、marking、freshness、eligibility、required-facts policy；
4. included/excluded/blocked/unknown ItemPreparationDecision；
5. ImpactPreview、ProjectedCostRange 和 budget；
6. BatchStartDecision、actor、approval、expectedVersion 与 idempotency key；
7. parent TaskRun、child item、Attempt/Handoff；
8. Action/Receipt/Reconcile、Usage/Settlement/EffectReview 与 count-conservation refs。

prepare 期间外部调用、收费 Job、owner/target mutation 必须全为 0。prepared、previewed、approved、confirmed 都不等于 started。start 是独立幂等命令，服务端重验全部 exact refs；target、consent、license、policy、account、price、budget 或 capability 漂移即阻断。

## 3. Item 守恒与多轴结果

- start 前 `frozenTotal = included + excluded + blocked + unknown`；
- start 后每个 included item 仍有稳定 key、Attempt、Action 和 Receipt lineage；
- 业务 item、外部 Action、Usage settlement、Effect maturity、Handoff decision 分轴；
- sibling succeeded 不覆盖 failed/cancelled/blocked/unknown；整批只有全部满足目标合同才可 succeeded；
- unknown 保留频控、预算和副作用敞口，只允许原 fingerprint 的 reread/callback/reconcile；
- reconcile 追加 Receipt，不覆盖原 unknown；
- originals、candidate、event、material 和 target refs 不因聚合丢失；
- refresh/restart 重建相同 frozen total、item decisions 和 lineage。

## 4. 验收门

负向至少覆盖：duplicate item key、consent/license/marking/freshness/required facts 缺失或撤销、prepare/start 间 target/policy/account/price/budget/capability 漂移、同键同 payload 重放与同键漂移 payload、部分成功、timeout/gap/duplicate/late/out-of-order callback、Consent withdraw race、cancel before/after submit、刷新重启，以及跨租户 refs/受保护 payload。

正式正向只认 `org-org/dev-project`，`dev-org/dev-project` 只作隔离 canary。每种真实触达、调价、发布或 Wiki 晋升必须另有 capability 的 exact 授权，批次 start 不能借权。

## 5. 两轮审查

### 第一轮：用户确认与数量守恒

- prepare 与 start 严格分离，准备阶段零副作用；
- 用户能看到 included/excluded/blocked/unknown、缺口、影响和成本；
- frozen total 与 item key 可重建；
- prepared/approved/confirmed 不被误报为 started。

结论：`PASS`。

### 第二轮：Partial/Unknown 与执行资格

- 五条结果轴独立，部分成功不覆盖 sibling 失败或 unknown；
- unknown 仅 authoritative reconcile，原 Receipt 不覆盖；
- generic Action/ResearchJob/领域 batch 不替代共享 runtime 与跨域 E2E；
- 当前无真实批次、外部动作、租户或浏览器写入。

结论：`PASS_WITH_HARD_GATE_BLOCKED`。

## 6. 最终裁决

W8-06 批次生命周期合同可以作为未来施工和验收基线；当前不得运行或勾选。预检事实见 `.evidence/workshop/2026-08-15-w8-06-batch-prepare-explicit-start-partial-unknown-reconcile-preflight.json`。

## 7. 2026-08-26 串行施工方案（AOS-000275）

### 7.1 新鲜事实与本波裁决

W4、W5、W6 和 W8-01～W8-05 已在 `m1` 形成 Evidence、受控 Action、达人/客户批次、Usage/Effect/Handoff 与六场景的工程合同和浏览器证据，因此第 1 节“依赖均未 GREEN”的 2026-08-15 历史快照不能继续作为 GET-only 工程施工的停工依据。

仓内仍没有一个可替代各领域 authority 的共享可写 Batch runtime。本波不创建第二套 `batch_store`、不迁移 Creator/Customer 历史批次、不把任一领域 batch 冒充公共权威；只新增 canonical reader 端口上的 **GET-only、exact-bound、fail-closed 场景投影**，验证公共语义、数量守恒、partial/unknown/reconcile 诚实表达和 163/164 产品落位。所有命令与外部副作用继续关闭。

### 7.2 合同与产品形态

1. exact 根固定为 `BatchPreparationRevision + BatchStartDecision`，`batchStartBindingHash` 确定性覆盖根、原子 Skill、Logic、数字同事责任绑定、ItemPreparationDecision、child outcome、五结果轴和 reconcile Receipt；任一 ref/revision/hash、scope 或 cutoff 漂移即整体失败关闭。
2. prepare 决策固定为 `included/excluded/blocked/unknown`，item key 必须唯一；`frozenTotal = included + excluded + blocked + unknown`，不得用 candidate 数量、页面数量或“已准备”文案替代。
3. 七阶段固定为 `prepare_root`、`impact_cost_preview`、`explicit_start`、`child_dispatch`、`partial_outcomes`、`unknown_reconcile`、`restart_rebuild`；非 ready 阶段必须有独立 blocker 且不得保留可信 exact refs。
4. 五结果轴固定分为 `business_item`、`external_action`、`usage_settlement`、`effect_maturity`、`handoff_decision`；partial/succeeded 不覆盖 sibling failed/cancelled/blocked/unknown。
5. unknown 只允许同 fingerprint 的 authoritative reread/callback/reconcile；reconcile 作为 append-only Receipt 可见，不能覆盖原 unknown 事实或触发自动重试。
6. composition 显式展示“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图”；批次生命周期是 Logic，不是大 Skill，调用外部系统是 Tool/Capability，不是 Skill。
7. `prepare/start/cancel/reconcile = false`，`automaticRetryAllowed=false`，`externalEffectsAllowed=false`，`releaseAllowed=false`；页面不生成相应写按钮。

### 7.3 文件级施工清单

| 切面 | 文件 | 最小改动 |
| --- | --- | --- |
| 后端合同 | `services/aos-api/aos_api/ecommerce_workshop_batch_scenario_contracts.py` | 新增 strict roots、四层 composition、Item decisions、七阶段、五结果轴、ledger、append-only reconcile refs 与全 false 命令守恒 |
| 后端组装 | `services/aos-api/aos_api/ecommerce_workshop_batch_scenario.py` | 新增 canonical reader 端口、binding hash 重算与 tenant/cutoff/root/item/ledger 漂移失败关闭；不新增 store |
| HTTP/OpenAPI | `services/aos-api/aos_api/routers/ecommerce_workshop.py`、`services/aos-api/tests/test_ecommerce_workshop_api.py`、`services/aos-api/tests/test_openapi_contract.py`、`scripts/export_openapi.py`、`packages/contracts/openapi/v1.*.json` | 新增 `GET /v1/ecommerce-workshop/views/task-cockpit/batch-scenario`，拒绝未知 query，不增写 operation |
| 后端测试 | `services/aos-api/tests/test_ecommerce_workshop_batch_scenario.py` | 证明无 root 失败关闭、exact binding/数量守恒可读，以及重复 key、跨租户、cutoff、hash、root、ledger、unknown/reconcile 漂移被拒绝 |
| Web SDK | `apps/web/src/api/ecommerceWorkshop/contracts.ts`、`parser.ts`、`client.ts`、`batchScenarioParser.test.ts` | 增加 strict parser、精确 GET client、字段/数量/命令漂移拒绝 |
| Task Cockpit UI | `apps/web/src/components/workshop/TaskCockpitPage.tsx`、`TaskCockpitPage.test.tsx`、`apps/web/src/styles/45-ecommerce-workshop.css` | 增加批次准备/显式启动/partial/unknown/reconcile 四层贡献、数量 ledger、七阶段、Item 与五轴；保持现有 W8-03 和任务明细功能不倒退 |
| 证据/上下文 | `.evidence/workshop/2026-08-26-w8-06-batch-prepare-start-reconcile-scenario.json`、本 ADR、D-waves 总清单、Task/Delivery Receipt、authority/Prime 投影 | 记录专项/累计测试、内置浏览器、安全扫描、commit 和 `NO_RELEASE` 边界 |

### 7.4 验收与回退

- 专项：后端 scenario/API/OpenAPI、Web parser/page；累计：Workshop 后端集、Web 全量、production build。
- 安全：只接受 tenant-bound exact refs；禁止 secret/PII/provider payload；不解析受保护联系方式；无请求时 DDL；无 Provider/Action/publish/reconcile 执行。
- 浏览器：内置浏览器新鲜页签验证四层贡献、frozen total、四类准备决定、七阶段、partial/unknown、append-only reconcile、五结果轴、命令全 false、无新增写按钮、窄屏无横向溢出和 console error。
- 回退只移除本波 scenario 合同/路由/SDK/UI 贡献；不修改 canonical Batch/TaskRun/Action/Receipt/Usage/Effect authority，因此不需要数据回滚或 migration。

## 8. 2026-08-26 实施、一致性复审与验收结论

### 8.1 实施结果

- 新增 strict `BatchScenarioContribution` 与 canonical reader；exact `BatchPreparationRevision + BatchStartDecision`、`batchStartBindingHash`、四层 composition、四类 item decision、七阶段、五结果轴、child outcome 与 reconcile Receipt 任一漂移均整体失败关闭。
- 新增 `GET /v1/ecommerce-workshop/views/task-cockpit/batch-scenario`；未知 query 被拒绝，未增加 POST/PUT/PATCH/DELETE operation，不新增 Batch store 或 migration。
- Task Cockpit 增加“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”视图，显示 `included/excluded/blocked/unknown` 和 frozen-total 守恒、partial/unknown/reconciled 分离及 append-only reconcile。
- `prepare/start/cancel/reconcile` 全部 false，`automaticRetryAllowed=false`、`externalEffectsAllowed=false`、`releaseAllowed=false`；页面只有“重新读取”，不生成批次命令按钮。

代码提交为 `aos-platform/m1@34a6cdf0`，浏览器证据提交为 `aos-platform/m1@4959e000`。

### 8.2 新鲜验证

- 后端专项/API/OpenAPI：`25 passed`；Workshop 后端累计：`198 passed / 7 warnings`。
- Web parser/page 专项：`14 passed`；Web 全量：`241 files / 2180 tests`；production build：`344 modules`。
- OpenAPI 确定性检查 PASS：`2670 paths / 2456 schemas / 4447 unique operations`，exporter `4457 rows`。
- 内置浏览器桌面 `1440×1000`：7 阶段、5 结果轴、4 类准备决定与四层贡献可见，命令按钮 0，console error/warning 0。
- 内置浏览器窄屏 `720×900`：`body/root scrollWidth=714 <= innerWidth=720`，stage/axis 折为单列，无水平溢出，命令按钮 0。

结构化证据：`.evidence/workshop/2026-08-26-w8-06-batch-prepare-start-reconcile-scenario.json`；截图：`.evidence/workshop/2026-08-26-w8-06-browser/batch-scenario-desktop.png` 与 `batch-scenario-narrow.png`。

### 8.3 方案—代码一致性与风险复审

第二轮复审结论为 `PASS`：文件级清单全部落位；root/binding/item/ledger 守恒、unknown/reconcile 语义、命令边界和 163/164 四层贡献与第 7 节一致；原有 Task Cockpit 任务明细与 W8-03 贡献未被移除，累计测试无倒退。

本波只证明工程产品合同和 GET-only 失败关闭，不证明可写 shared Batch runtime 、真实批次或 operational readiness。未 apply 迁移、未写真实租户、未 prepare/start/cancel/reconcile 批次、未自动重试、未调用 Provider/Action、未产生外部副作用或 release，故最终裁决为：

`W8_06_BATCH_PREPARE_START_PARTIAL_UNKNOWN_RECONCILE_EXACT_BINDING_CODE_CONTRACT_BROWSER_GREEN_SECURITY_SCOPED_GREEN_OPERATIONAL_FAIL_CLOSED_NO_EXTERNAL_EFFECT_NO_RELEASE`
