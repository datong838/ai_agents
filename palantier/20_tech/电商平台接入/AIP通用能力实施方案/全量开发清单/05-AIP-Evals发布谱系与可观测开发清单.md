# 05 AIP Evals、发布门、决策谱系与可观测开发清单

> 状态：**v2.8 · AIP-4 IMPLEMENTED_GREEN · E0A～E4C 全部封板（已获用户全量编码授权）**
> 上位依据：`../05-228-AIP-Evals发布门控决策谱系与可观测实施方案.md`
> 对应阶段：AIP-4、AIP-7 观测侧；前置：02、04 GREEN。

## 1. 工作包

| ID | 任务 | 文件边界 | 验收 |
|---|---|---|---|
| 05-01 | 冻结 EvalCase/Suite/Run/Report/ReleaseGate/Publication DTO | eval contracts | 全部绑定 exact revision/hash |
| 05-02 | 建 Eval/Publication/Lineage/Telemetry 表及 RLS | migrations/stores | 报告不可覆盖，撤回追加事件 |
| 05-03 | 实现六同事 EvalPack Registry | `aip_eval_*` | 每 Skill 正常/边界/负向/租户/故障齐备 |
| 05-04 | 实现 Eval runner、judge version、数据集来源/脱敏 | eval service | judge/数据变更使旧门失效 |
| 05-05 | 实现 ReleaseGate 与 Logic/Agent publication | publication store | 页面不能手工 GREEN |
| 05-06 | 实现 DecisionLineage 真实 run 事件聚合 | lineage store | 删除固定 6 段 trace |
| 05-07 | 接 OpenTelemetry spans 与 task/agent/logic 关联 | telemetry | 乱序/迟到/时钟偏差可处理 |
| 05-08 | 接真实 UsageReceipt、Token、成本、AdjustmentEvent | observability | 缺失为 unknown，不用估算过门 |
| 05-09 | Dashboard revision、Alert/Ack/Silence Receipt | observability UI/store | 无静态 widget 冒充持久化 |
| 05-10 | 外部 ResearchJob provider/artifact/delivery/reconcile 谱系 | lineage/evals | callback 重放、hash 错、漂移均阻断 |
| 05-11 | Lineage/Observability/Publication 页面真实化 | web pages/SDK | API 空/错/partial/unknown 诚实显示 |
| 05-12 | 建 37 Logic EvalCatalog 与发布门 | eval manifests/runner | 每条含正向、边界、缺字段、越权、下游失败、注入 |
| 05-13 | 建 SC01～SC09 组合 Eval 与 Handoff/EffectReview 回归 | scenario evals | 单 Logic 通过不代替场景通过 |
| 05-14 | 建 Wiki/FDE/Content 专项量化门 | eval packs | 冷启动/RAG、26 Reflection、14 Harness、视频/直播分别验收 |
| 05-15 | 建 G0～G6 累计发布与回滚门 | release policy | 上游未 GREEN、平台能力 unknown 或专项 deferred 时不可发布 |

## 1.1 实施子波与依赖裁决（2026-08-11）

| 子波 | 工作包 | 当前状态 | 退出门 |
|---|---|---|---|
| E0A | 05-01、05-02 的公共契约与 additive migration | `IMPLEMENTED_GREEN` | `2c02d1f`；26 passed；单 head/守恒/FORCE RLS/append-only 通过 |
| E0B1 | 05-02 tenant-scoped store + immutable semantics | `IMPLEMENTED_GREEN` | `4f9f471`；31 passed；双租户/幂等/冲突/重启回读通过 |
| E0B2 | 05-02 最小只读 API/OpenAPI + Publication 权限测试校正 | `IMPLEMENTED_GREEN` | `0996704`；55 passed + 2 subtests；真实租户与 canary 只读负向冒烟通过 |
| E1A | 05-03 Registry + 真实 Dataset manifest 门 | `IMPLEMENTED_GREEN` | `134b7e8`；20 passed；单 head `aip4_002`；双租户真实库空读 |
| E1B | 05-04 runner + 不可变 report | `IMPLEMENTED_GREEN` | `7e255ed`；28 passed；exact ref/content drift 全部失败关闭 |
| E1C | 旧 Logic Eval compatibility 收口 | `IMPLEMENTED_GREEN` | `f359534`；17 passed / 1 skipped；运行角色最小授权，未知租户 403 fail-closed |
| E2 | 05-05 | `IMPLEMENTED_GREEN` | `fb525cc`；gate 服务端推导、发布/撤销追加事件、撤销后阻断同 exact target 新 Run |
| E3A | 05-06 | `IMPLEMENTED_GREEN` | `16aed87`；权威源事件引用与真实 Lineage 投影；无固定六段 |
| E3B | 05-07、05-08 的 span/usage 基础 | `IMPLEMENTED_GREEN` | `ea1f1c5`；持久化 span；unknown quantity 为空；provider receipt 重放不重计 |
| E3C | 05-08 成本归因与 Capability Receipt | `IMPLEMENTED_GREEN` | `f7179ce`；分质量/币种归因、Adjustment 复算、exact capability receipt |
| E3D | 05-10 与 E3 总回归 | `IMPLEMENTED_GREEN` | `849f40d` + `e7542db` + `a88cad1`；118 passed；单 head `aip4_008`；真实租户零伪造 |
| E4 | 05-11 | `APPROVED_TO_IMPLEMENT` | 三页面唯一 SDK、无固定 trace/Mock/合成趋势 |
| E5 | 05-12～05-15 | `PENDING` | 37 Logic、场景和专项门在其真实资产存在后逐项封板 |

E0A 文件边界固定为：

- 新增 `services/aos-api/alembic/versions/aip4_001_eval_lineage_observability_contract.py`
- 新增 `services/aos-api/aos_api/aip_eval_contracts.py`
- 新增 `services/aos-api/tests/aip/test_aip4_contracts.py`
- 新增 `services/aos-api/tests/aip/test_aip4_migration.py`

E0A 不修改页面、不触发 Eval/Publication/外部 Adapter，不写真实业务记录。真实库基线计数必须保持 Suite=1、Report=2、Publication=1、历史 lineage=631。

E0B1 计划文件边界：

- 新增 `services/aos-api/aos_api/aip_eval_authority_store.py`
- 新增 `services/aos-api/tests/aip/test_aip_eval_authority_store.py`
- 如需对契约做兼容修正，仅允许修改 `aip_eval_contracts.py` 及其定向测试。

E0B1 只实现 Dataset revision、EvalRun/event、Gate decision、Publication/Lineage event、Usage/Adjustment 和 MetricDefinition 的 scoped persistence；不开放路由、不写 `org-org/dev-project` 验收数据。

E0B2 计划文件边界：

- 新增 `services/aos-api/aos_api/routers/aip_eval_authority.py`
- 新增 `services/aos-api/tests/aip/test_aip_eval_authority_api.py`
- 修改 `services/aos-api/aos_api/routers/domain_aggregates.py`
- 修改 `services/aos-api/tests/test_aip_logic_publication_api.py`，仅校正测试 principal/scope，不放宽生产鉴权。
- 如 route/OpenAPI inventory 为确定性快照，按实际新路由精确更新对应测试基线。

E0B2 仅允许 GET Dataset revision、GET EvalRun snapshot、GET Lineage events；不开放手工写 Gate/Publication/Usage 事实的 API。

E0B2 封板说明：

- OpenAPI 固定为 2332 paths、1562 schemas、4097 route rows、4087 unique operation pairs；domain manifest 固定为 514 routers。
- `org-org/dev-project` 与 `dev-org/dev-project` 对不存在的 Run 均返回 scoped 404、对不存在的 Lineage 均返回 scoped 空列表；没有写入 AIP-4 业务记录。
- 历史 `tests/test_evals_engine.py` API 夹具在当前 FORCE RLS 数据库下未设置 tenant GUC，独立扩展回归为 7 failed / 65 passed / 1 skipped / 2 subtests passed；该 RED 不属于 E0B2 只读路由回归，也不得隐藏，纳入 E1 旧引擎迁移与测试夹具收口。

E1A 文件边界和门禁：

- 新增 `aip4_002_eval_pack_registry.py`、`aip_eval_pack_registry.py` 及其迁移/store 测试；仅兼容扩展，不覆盖旧 Suite/Report。
- Registry 写入前必须验证同租户 Dataset revision 已存在；Suite/target/dataset/judge 全部绑定 exact revision/hash。
- Dataset manifest 禁止内联业务记录、明文 PII、`mock/synthetic/demo` 来源；必须包含 source reference/hash、字段 allowlist、redaction receipt/hash 和 case count。
- 六同事/37 Logic 等待 AIP-6 真实资产 revision，不生成占位目录。

E1B 计划边界：新增 `aip4_003_eval_report_revision.py`、`aip_eval_runner.py` 及定向测试；Report 只保存 case/result hash 和结构化 detail code，不保存业务明文。Runner 必须从 Registry 读取 Suite，并逐项复验 target/dataset/judge/artifact exact refs；任何漂移、解析失败或 judge 错误使 Run failed，不生成可过门报告。

E1C 禁止通过删除旧测试、关闭 FORCE RLS 或恢复进程内 Suite/Report 真源消红。优先将旧夹具的 scoped connection 设置 tenant GUC，使兼容 API 在当前 RLS 军规下恢复；随后明确旧 API 仅为 compatibility surface，新写链进入 E1 Registry/Runner。

E1C 实施结论：隔离 schema 明确授予 `aos_runtime` USAGE 与表级最小 DML 权限，并在连接内设置 transaction-local tenant GUC；未修改生产表策略。旧文件 17 passed / 1 个需显式 Agnes 配置的集成项 skipped；组合范围共收集 80 项并退出码 0。跨租户 header 伪造在 Store 前由 Auth 以 `403 AUTH_TENANT_UNKNOWN` 拒绝，符合 fail-closed 边界。

E2 编码清单已冻结：

- [x] 建立唯一 `aip_release_publication_service.py`，在同一 scoped transaction 内复验 Report hash、Run succeeded、Suite threshold 与 target/dataset/judge exact refs。
- [x] Gate 状态仅由服务端推导；请求 DTO 不允许传入 passed/GREEN/status。
- [x] 首期只允许 `logic_graph` exact revision/hash 发布；Agent/Skill 等 registry 未落地类型明确失败关闭。
- [x] `published/revoked` 仅追加 `aip_publication_event`；重复撤销拒绝，历史事实禁止 UPDATE/DELETE。
- [x] canonical API、OpenAPI、认证权限、幂等回放/冲突与错误码定向测试完成。
- [x] 隔离 PostgreSQL 覆盖跨租户、报告/资产漂移、失败报告、同键异载荷、append-only；真实 `org-org/dev-project` 与 canary 不写业务事实。

E2 实施结论：代码 `fb525cc`；新增 3 个 canonical API，不产生 AIP 重复路由；OpenAPI 更新为 2335 paths、1569 schemas、4100 route rows、4090 unique operation pairs。AIP-4 E0A～E2 合并回归 95 passed / 1 skipped / 2 subtests passed；真实库单 head `aip4_003`，两个既定租户的新 Suite/Report/Gate/Event 计数均为 0。下一门为 E3 真实 LineageEvent、Telemetry、UsageReceipt/Adjustment 与成本口径。

E3A 编码清单已冻结：

- [x] additive migration 为 `aip_lineage_event` 增加权威 `source_kind/source_id/source_hash`，建立租户内同源唯一约束并保持 append-only、RLS/FORCE RLS。
- [x] 建立唯一 `aip_lineage_service.py`，仅从真实 TaskRun/Action/Eval/Publication 表读取和投影；事件 id/sequence/hash 确定性且可重放。
- [x] 投影只落 exact 引用、类型、时间和哈希，不复制业务 payload、模型 prompt、对象字段或 PII。
- [x] canonical 查询返回持久化真实事件；空谱系诚实返回空，不使用 `aip_lineage_engine.py` 固定六段回退。
- [x] 对账投影写入口只授予受信运行角色；请求只选择 root，不允许提交 event_type、quality、payload_hash 或手工 source。
- [x] 覆盖同源重放、同源 hash 冲突、源事实不存在、跨租户、Action unknown/reconcile、Publication revoke、Eval failed 与 append-only 负向测试。
- [x] disposable PostgreSQL 从全量基线迁移到 `aip4_004`，downgrade SQL 静态复核、OpenAPI/路由唯一性、真实租户/canary 只读零写入与 E0A-E2 回归通过，进入 E3B。

E3A 实施结论：代码 `16aed87`；累计 107 tests collected 并以退出码 0 完成，ruff、compileall、OpenAPI exporter 和路由固定契约通过。OpenAPI 为 2337 paths、1570 schemas、4102 route rows、4092 unique operation pairs；开发库单 head `aip4_004`。真实租户和 canary 的 canonical lineage 新记录均为 0，本波只增加权威投影能力，未生成假谱系。

E3B 实施清单：

- [x] additive migration 建立 tenant-scoped persistent span authority，区分 producer 时间、ingest 时间和 observed 时间，并保留乱序/迟到事实。
- [x] 调整 `UsageReceipt`：`quality=unknown` 时 quantity 必须为空；measured/estimated 必须有非负 quantity，成本仍要求 currency。
- [x] provider receipt 以 scope + provider + provider_receipt_id 唯一；同载荷重放幂等，异载荷冲突，不把重复回调重复计费。
- [x] `AdjustmentEvent` 仅追加、引用原 Receipt；原收据不得 UPDATE/DELETE，聚合按 Adjustment 复算。
- [x] span/usage canonical 写入口只授予受信运行角色，并绑定既有 lineage/root；不接收页面手工 GREEN、估算趋势或 PII attribute。
- [x] 覆盖乱序、迟到、时钟偏差、unknown、重复 provider receipt、adjustment 重放/冲突、跨租户与 append-only 负向门。

E3B 实施结论：代码 `ea1f1c5`；39 项定向测试与 95 项 `tests/aip` 累计回归退出码 0，ruff、compileall、OpenAPI/路由固定契约通过。OpenAPI 为 2343 paths、1579 schemas、4108 route rows、4098 unique operation pairs；开发库单 head `aip4_005`，真实租户和 canary 的 span/usage/adjustment 均为 0。

E3C 实施清单：

- [x] additive migration 新增 append-only `aip_usage_attribution` 与 `aip_capability_receipt`，保持 RLS/FORCE RLS、truncate guard 和租户复合键。
- [x] UsageAttribution 引用原 Receipt 与同一 lineage；按 model/tool/capability/task/agent 维度保存 exact subject ref、quality、weight/source hash，不复制业务 payload。
- [x] CapabilityReceipt 绑定同租户 TaskRun、PlanRevision、PlanStep 和 exact `capabilityRef.revision`；lineage root/run 不一致、未批准计划或 binding 漂移必须失败关闭。
- [x] 成本汇总按 currency 与 measured/estimated/unknown 分桶；Adjustment 继承原 Receipt quality 并复算，结果不得为负，原 Receipt 不修改。
- [x] 只有 measured cost + measured attribution + 单一币种 + 无未知缺口可形成 hard-budget eligible 读模型；其余明确 unknown/estimated。
- [x] AIP-6/AIP-7 权威 registry 未落地的 model/tool/agent measured attribution 失败关闭，不以 legacy 内存目录补真值。
- [x] canonical 写入口仅授予受信运行角色，覆盖跨租户、幂等/冲突、未知收据、权重超配、负数复算与 append-only 负向门。

E3C 实施结论：代码 `f7179ce`；20 项 E3C/路由定向测试与 105 项 `tests/aip` 累计回归完成，ruff、compileall、OpenAPI exporter 和固定路由契约通过。OpenAPI 为 2347 paths、1586 schemas、4112 route rows、4102 unique operation pairs；开发库单 head `aip4_006`，真实租户与 canary 的 attribution/capability receipt 均为 0。

E3D 下一波清单：

- [x] 复核已评审 ResearchJob v1.2、`aip_research_job.py` 与 TAOR 现有 Job 事件链，裁决唯一兼容真源，禁止平行内存实现。
- [x] 建租户范围、版本化 Provider authority；disabled/unregistered/revision drift 均在提交前失败关闭。
- [x] ResearchJob 提交绑定 exact provider、capability、PlanStep、TaskRun 与 lineage；外部 job id 只由受信 Adapter Receipt 回写。
- [x] callback 验签、nonce 防重放、provider event id 幂等且 sequence 单调；gap/乱序保留并进入 reconcile，不伪装完成。
- [x] Artifact/Delivery Receipt 保存 immutable URI/hash/media type/exact capability；交付前复验内容 hash 与当前绑定。
- [x] timeout/断网/外部未知状态进入 unknown；禁止盲重试副作用，只有 Reconcile Receipt 可推进最终状态。
- [x] 完成 E3A～E3D 累计回归、双租户负向、OpenAPI/路由唯一性、迁移单 head 与真实租户零伪造证据。

E3D 代码实况与文件边界：

- 保留 `aip_research_job.py` 的 v1.2 DTO、事件单调合并和 HMAC 回调验签；其当前 nonce `set` 不是可重启真值。
- 唯一 Task/Run 真源继续是 `aip_task_run/aip_plan_revision`；唯一产物真源继续是 `aip_artifact`。
- 新增 `aip4_007_research_job_authority.py`、`aip_research_job_store.py`、`aip_research_job_service.py`、`routers/aip_research_jobs.py` 和 migration/store/API 定向测试。
- 只追加 ProviderRevision、JobManifest、Submission、Event、CallbackNonce、Artifact、Delivery/Reconcile Receipt；当前状态由 Receipt 推导，不写第二套 Task 状态。
- Provider exact revision 必须是租户内当前最高且 enabled；sequence gap 持久保留但不能完成；callback body 只作唤醒信号；Artifact hash/capability 漂移或 unknown 均阻断 delivery。

E3D 最终复审补强：

- [x] 追加 `aip4_008_research_job_lineage_binding.py`，不改写已执行的 `aip4_007`；JobManifest 固化 exact `lineage_id/sequence/event_id`。
- [x] `lineageRef` 必须指向当前 TaskRun 根的最新 lineage event；跨 run、跨租户、旧 sequence 和无 lineage 均失败关闭。
- [x] `aip4_008` 对既有 ResearchJob 行拒绝猜测式回填；完成专项测试后重新执行累计回归、迁移与零伪造证据。

E3D 实施结论：代码 `849f40d`、`e7542db`、`a88cad1`；13 项 migration/store/API 补强门与 118 项 AIP 累计回归通过。OpenAPI 确定性导出、Ruff、compile 通过；开发库单 head/current=`aip4_008`。真实租户和 canary 七表均为 0；各表 RLS/FORCE RLS/双 guard 有效。下一门 E4 只做三页面对唯一 SDK 与真实权威读模型的消费，不在前端构造固定 trace、Mock 或趋势。

E4 编码清单已冻结：

- [x] E4A：建立唯一 `apps/web/src/api/aipEvidence/` SDK 基座，强类型解析 LineageEvent 并预注册 Telemetry canonical operations；禁止谱系组件自行拼接 canonical path。
- [x] E4A：决策谱系页以 root type + root id 查询权威事件；删除固定 Trace ID、固定标题与 `defaultSteps`；空、错、partial 和 unknown 诚实展示。
- [x] E4B：可观测页改为按 lineage ID 查询真实 spans/usage；Overview 只由返回事实聚合，quantity 缺失显示 unknown，不把 estimated 合并成 measured。
- [x] E4B：删除生产路径 `MOCK_KPIS/MOCK_TREND/MOCK_TRACES/MOCK_SPANS/MOCK_METRICS/MOCK_WIDGETS`、`request_count × 230` 展示和合成趋势；删除无权威后端的 Dashboard/Alerts 演示能力。
- [x] E4C：Evals 门控与现有 Logic Publication 严格 revision/hash/readback 通过同一 AIP client/SDK 消费；不新增手工 GREEN，不重写正常 Publication 写链。
- [x] E4C：更新交互诚实清单、定向测试、TypeScript、前端全量测试和构建；内置浏览器以 `org-org/dev-project` 验收三页失败关闭。API health=500，正向真实回包明确留作环境补证。

E4 三页面裁决：导航页为 Evals 门控、决策谱系、可观测性；Publication 写动作继续由 Logic Canvas/Publication Panel 承担，Evals 页承载发布前 Gate/Report 证据，不创建平行发布页。

E4A 实施结论：代码 `84dac50`；9 项 SDK/页面定向测试与 TypeScript 通过。内置浏览器确认 `org-org/dev-project`、root 类型下拉、空输入说明和 API 失败关闭态，固定示例命中 0。因本机 API health=500，本子步未宣称真实事件正向浏览器证据 GREEN；该项随 E4C 服务恢复后补齐。下一门 E4B。

E4B 实施结论：代码 `9fcd203`；3 文件 14 tests、TypeScript、diff check 通过。Telemetry/Usage 契约对跨 lineage、重复 provider receipt、quantity/quality 和 currency/usageKind 不一致失败关闭；内置浏览器确认真实组织/工作区、idle/error 诚实展示，伪 Token 和 Dashboard 命中 0。API health=500 的正向浏览器证据保留至 E4C。

E4C 实施结论：代码 `43f5f82`；6 文件 44 tests、前端全量 172 文件/2044 tests、TypeScript、Vite production build 全部 GREEN。内置浏览器确认 Evals 权威 Run 只读入口、Lineage 无示例、Observability 无 Mock，三页 API 异常均失败关闭；Publication POST→GET exact readback 回归保持。AIP-4 全部封板，下一阶段 AIP-5。

## 2. 退出门

- [ ] 任一 Agent/Skill/Logic/Model/Policy revision 变化，旧 ReleaseGate 自动失效。
- [ ] fallback、工具失败、Draft 驳回、unknown、reconcile、撤回出现在同一谱系。
- [ ] measured/estimated/unknown 不混算；重复 usage 不重复成本。
- [ ] 37/37 Logic 均有独立 EvalPack 和 exact revision 绑定；工具未注册/数据过期必须失败关闭。
- [ ] SC01～SC09、G0～G6、七管道、26 Reflection、14 Harness 和直播 L0～L5 可分别查看通过/阻断/延期证据。
- [ ] 沙箱、Draft、Proposal、平台真实执行四种结果在发布门和谱系中不会混淆。
- [ ] 双租户查询/导出隔离，PII 不进 span；历史发布与撤回可复验。
