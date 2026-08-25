# W8-05 FULL 短视频生产与故障恢复预检 ADR

> 日期：2026-08-15  
> 决策：历史预检为 `NOT_STARTED / SCENARIO_CONTRACT_APPROVED / HARD_GATE_BLOCKED`；2026-08-26 工程裁决为 `CODE_CONTRACT_BROWSER_GREEN / OPERATIONAL_FAIL_CLOSED / NO_PROVIDER_OR_PUBLISH_EFFECT / NO_RELEASE`
> 前置：产品正式封板；W7-11、DEP-M9 当前 release 全 GREEN；签名 FULL 模板和生产 Adapter 齐备

## 1. 当前事实

媒体技术方案已完整定义八类影视专业责任、自适应 Stage、Artifact family、四门同版评估、返工、Provider、成本和发布边界。八类责任不是八个固定 Agent；实际任务可协调人、数字同事、共享 Agent、工具和 Provider，但任何职责、独立审核和治理责任都不能被合并掉。

W7-11 已确认十个 W7 实现均未 GREEN；从 W7-11 基线 `5c3ca93` 到本轮预检，`services/apps/packages/bundles` 无业务源码变化。AIP-9、签名 FULL 模板、媒体 executor、生产 Provider Adapter、正向浏览器和故障注入证据均不存在。因此不重复运行同一组 generic 测试，不用 Mock 或静态页面冒充 FULL 生产。

## 2. FULL 生产绑定

exact `MediaProductionBriefRevision + TaskRun` 是场景根，`fullProductionBindingHash` 至少覆盖：

1. EvidenceBundle、EvalContract、ProfileRecommendation/Confirmation；
2. StageTemplate、ResponsibilityPlan、MergePolicy；
3. Plan/Step/Attempt、Capability/AgentInstance、Provider/ModelRoute/RuntimePolicy/Price/License；
4. Stage Lease、fenceToken、Checkpoint 和 dependency snapshot；
5. CreativeDirection、Script、ArtPack、Storyboard/ShotList、RawAsset、Master、Variant 与 ArtifactRelation；
6. MediaGateSet、ReviewIssue、ReturnDecision 与 Approval；
7. Capacity/Budget Reservation、Usage、Settlement/Reconcile；
8. PublishCandidate、Impact、Action/Receipt 与 EffectReview。

FULL 表示八专业责任与全部治理门覆盖，不表示固定执行人数、自动执行或无限预算。compiler 只物化 Plan，start 独立复验后只创建一个 canonical TaskRun。

## 3. 故障恢复合同

- crash before submit：无提交 Receipt，不伪造 Provider 请求；
- crash after submit before Receipt：使用原 request fingerprint 查询，不换 Provider/账号/幂等键；
- lease loss/takeover：新 fence 生效，旧 owner 的延迟写入一律拒绝；
- duplicate/out-of-order/late webhook：归并到原 attempt，不双建 Artifact/Usage；
- timeout/cancel/late result：CancelIntent、Adapter 响应、Provider 最终态、Usage 和 late Artifact 分轴；
- Checkpoint corruption/drift：按 exact input/template/capability/policy/provider/license 计算 invalidation，不能盲目恢复；
- capacity/budget race：预留、提交、outbox 原子边界，unknown exposure 不提前释放；
- partial/malicious Artifact：保持 quarantine，未通过 hash/MIME/malware/license/肖像/商标/prompt-injection 门不得登记；
- DB/API/worker restart 与网络分区：从 durable authority 重建，不依赖进程内状态。

## 4. 验收门

同一新 Artifact 的事实、品牌、版权、平台四门必须 4/4；ReturnDecision 产生新 attempt，旧 Attempt/Artifact/Usage/Issue 不覆盖。发布、交付、Usage settlement、lineage 与 Effect maturity 分轴，任一 unknown 不得被其他成功吞并。

正式正向只认 `org-org/dev-project`，`dev-org/dev-project` 只作隔离 canary。必须具备当前 release 的 contract、service、restart、RLS、双租户 browser、安全、fault injection、Provider、publish canary 和 operational readiness 独立 Receipt。

## 5. 两轮审查

### 第一轮：职责、生产与用户干预

- 八责任全部保留但不固定 Agent/人数；
- Brief→Stage→Artifact→四门→返工→发布→复盘全链 exact；
- pause/resume/takeover/cancel/return/reconcile 都有用户可见状态与 Receipt；
- FULL 不被解释为自动运行或绕过预算、审核和发布批准。

结论：`PASS`。

### 第二轮：故障语义与执行资格

- crash、fence、webhook、cancel、Checkpoint、预算和重启矩阵完整；
- provider unknown 只 reconcile，不盲重试或伪造取消/退款；
- 无业务源码变化时不重复累计 generic 测试冒充实现推进；
- 当前无 Provider、媒体、真实租户、浏览器或发布副作用。

结论：`PASS_WITH_HARD_GATE_BLOCKED`。

## 6. 最终裁决

W8-05 FULL 生产与故障恢复合同可以作为未来施工和验收基线；当前不得运行或勾选。预检事实见 `.evidence/workshop/2026-08-15-w8-05-full-video-production-fault-recovery-preflight.json`，其 Delivery Receipt 中误写的符号 `HEAD` 由 `.evidence/workshop/2026-08-15-w8-05-preflight-receipt-commit-correction.json` 追加纠正为 immutable SHA。

## 7. 2026-08-26 串行施工方案（AOS-000274）

### 7.1 新鲜事实与本波裁决

W7 已形成 Media Studio 七节点生命周期、八责任槽、Stage/Artifact/Issue、Provider Job 贡献、Capacity/Budget/Usage/Settlement、发布贡献与十一栏累计门的工程基座；W8-01～W8-04 也已在 `m1` 串行完成只读场景合同、前端贡献视图、浏览器验收与 authority/Prime 回读。因此，本 ADR 第 1 节中“W7 未实现”的历史快照已不能作为停工依据。

本波允许实现一个 **GET-only、exact-bound、fail-closed** 的 FULL 短视频生产/故障恢复贡献场景，用于验证合同、数量守恒、故障语义和工作台产品表达。Provider Adapter、publish canary 与 operational readiness 仍保留为独立阻断；本波不调用 Provider、不启动/恢复/接管 TaskRun、不发布、不结算、不产生真实租户业务写入，不宣称 release GREEN。

### 7.2 合同与产品形态

1. 场景根固定为 exact `MediaProductionBriefRevision + TaskRun`，`fullProductionBindingHash` 确定性覆盖 composition、八责任、Stage/Attempt、Artifact/Gate/Issue、Usage/Settlement 和故障恢复观测；任一 ref、revision 或 hash 漂移即整体失败关闭。
2. composition 显式区分“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”；不把八责任、整条流程或 Provider 动作冒充为单个 Skill。
3. 七个生产阶段固定为 `brief_profile`、`compile_start`、`script_art`、`storyboard_capture`、`post_review`、`publish_delivery`、`settlement_effect`；每阶段只能是 `ready/blocked/unknown`，非 ready 必须带独立 blocker，不伪造 exact refs。
4. 八责任槽必须 8/8 可见，但不假定八个固定 Agent；合并执行人不得吞掉独立审核、证据和 Receipt。
5. 故障矩阵固定覆盖 submit 前崩溃、submit 后 Receipt 前崩溃、Lease/fence 丢失、webhook 重复/乱序/迟到、timeout/cancel/late result、Checkpoint 损坏/依赖漂移、capacity/budget 竞态、重启/网络分区、恶意 Artifact 隔离；每项显示 recovery decision 与 authority ref 或 blocker。
6. 命令面固定返回 `prepare/start/resume/takeover/cancel/reconcile/publish/settle = false`；前端不生成对应写按钮。

### 7.3 文件级施工清单

| 切面 | 文件 | 最小改动 |
| --- | --- | --- |
| 后端合同 | `services/aos-api/aos_api/ecommerce_workshop_full_video_scenario_contracts.py` | 新增 strict exact refs、composition、七阶段、八责任、故障矩阵、ledger、命令全 false 与守恒校验 |
| 后端组装 | `services/aos-api/aos_api/ecommerce_workshop_full_video_scenario.py` | 新增 canonical reader 端口、binding hash 重算与 scope/cutoff/root/fault 一致性失败关闭 |
| HTTP/OpenAPI | `services/aos-api/aos_api/routers/ecommerce_workshop.py`、`services/aos-api/tests/test_ecommerce_workshop_api.py`、`services/aos-api/tests/test_openapi_contract.py`、`scripts/export_openapi.py`、`packages/contracts/openapi/v1.*.json` | 新增 `GET /v1/ecommerce-workshop/views/media-studio/full-production-scenario`，禁止未知 query，不增写 operation |
| 后端测试 | `services/aos-api/tests/test_ecommerce_workshop_full_video_scenario.py` | 先证明无 root 失败关闭，再证明 exact binding、8/8 责任、七阶段、故障语义、漂移/跨租户/数量伪造被拒绝 |
| Web SDK | `apps/web/src/api/ecommerceWorkshop/contracts.ts`、`parser.ts`、`client.ts`、`fullVideoScenarioParser.test.ts` | 增加 strict parser、精确 GET client 和漂移拒绝测试 |
| Media Studio UI | `apps/web/src/components/workshop/MediaStudioPage.tsx`、`MediaStudioPage.test.tsx`、`apps/web/src/styles/45-ecommerce-workshop.css` | 在现有页面增加 FULL 场景四层贡献、七阶段、8 责任、故障矩阵与命令全 false 视图；不改现有三 Tab 数据契约 |
| 证据/上下文 | `.evidence/workshop/2026-08-26-w8-05-full-video-fault-recovery-scenario.json`、本 ADR、D-waves 总清单、Task/Delivery Receipt、authority/Prime 投影 | 记录新鲜测试、内置浏览器、安全扫描、commit 与 `NO_RELEASE` 边界 |

### 7.4 验收与回退

- 专项：后端 scenario/API/OpenAPI，Web parser/page；累计：Workshop 后端集、Web 全量与 production build。
- 安全：仅 GET、严格租户、无 secret/PII/media payload、无 Provider/Action/publish 执行、无请求时 DDL。
- 浏览器：使用内置浏览器在新鲜页签核对不新增重复 H1、四层贡献、七阶段、八责任、故障矩阵、全 false 命令、无横向溢出和 console error。
- 回退粒度是本波新增 scenario 合同/路由/SDK/UI 贡献；不修改 canonical TaskRun/Artifact/Provider/Usage authority，因而不需要数据回滚或 migration。

## 8. 2026-08-26 实施、一致性复审与验收结论

### 8.1 实施结果

- 新增 strict `FullVideoScenarioContribution` 与 canonical reader；exact `MediaProductionBriefRevision + TaskRun`、`fullProductionBindingHash`、composition、八责任、七阶段、九故障轴与数量 ledger 任一漂移均整体失败关闭。
- 新增 `GET /v1/ecommerce-workshop/views/media-studio/full-production-scenario`；未知 query 被拒绝，未增加 POST/PUT/PATCH/DELETE operation。
- Media Studio v7 在原三 Tab 之前增加 FULL 场景贡献区，明确展示“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”；八责任不等于八个固定 Agent。
- `prepare/start/resume/takeover/cancel/reconcile/publish/settle` 八项均为 false；前端只存在“重新读取 + 三个只读 Tab”四个按钮，不生成命令按钮。

代码提交为 `aos-platform/m1@604ca9b4`，浏览器证据提交为 `aos-platform/m1@874321dd`。

### 8.2 新鲜验证

- 后端专项 scenario/API：`10 passed / 7 warnings`；Workshop/OpenAPI 累计：`209 passed / 7 warnings`。
- Web parser/page 专项：`2 files / 11 tests`；Web 全量：`240 files / 2177 tests`；production build：`344 modules`。
- OpenAPI：`2669 paths / 2442 schemas / 4446 unique operations`，exporter `4456 rows`。
- security scanner unit：`9 passed`；本波 14 文件 scoped security：`critical=0 / warning=0`。
- 内置浏览器桌面 `1440×1000`：七阶段、八责任、九故障轴、八个不可执行命令完整可见，console error/warning 为 0；切换“职责与执行”Tab 后场景仍在且按钮仍为 4。
- 内置浏览器窄屏 `720×900`：`bodyScrollWidth=714 <= innerWidth=720`，阶段/责任/故障网格均折为单列，无横向溢出。

结构化证据：`.evidence/workshop/2026-08-26-w8-05-full-video-fault-recovery-scenario.json`；关键截图：`.evidence/workshop/2026-08-26-w8-05-browser/full-video-scenario-viewport.jpg` 与 `full-video-fault-command-viewport.jpg`。

### 8.3 方案—代码一致性与风险复审

第二轮复审结论为 `PASS`：文件级清单全部落位；合同数量、root 绑定、命令边界和 163/164 四层贡献均与第 7 节一致；既有 Media Studio 三 Tab、Provider/Finance/Lifecycle/Publish/Cumulative 贡献未被移除，累计测试无倒退。

剩余风险保持显式：测试夹具只证明工程产品合同，不是 Provider Adapter、真实发布 canary 或 operational readiness。未 apply 共享迁移、未写真实租户、未启动/恢复/接管 TaskRun、未自动重试、未调用 Provider/Action、未发布、未结算、未产生外部副作用，故最终裁决为：

`W8_05_FULL_VIDEO_RECOVERY_EXACT_BINDING_CODE_CONTRACT_BROWSER_GREEN_SECURITY_SCOPED_GREEN_OPERATIONAL_FAIL_CLOSED_NO_RELEASE`
