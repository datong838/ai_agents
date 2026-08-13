# 06 AIP 三层运行记忆、行业 Wiki 与知识治理开发清单

> 状态：**v2.0 · 已获用户全量编码授权 · E0～E5 IMPLEMENTED_GREEN · E6 REVIEWED / APPROVED_FOR_IMPLEMENTATION_WITH_EXTERNAL_DATA_GATE**
> 上位依据：`../06-228-AIP三层记忆行业Wiki与知识治理实施方案.md`
> 对应阶段：AIP-5；前置：02、04、05 GREEN。

## 1. 工作包

| ID | 任务 | 文件边界 | 验收 |
|---|---|---|---|
| 06-01 | 冻结 Working/Episodic/Semantic、Shared 投影和 Procedural 资产边界 | contracts/ADR | 不建第四套运行记忆库 |
| 06-02 | 建 MemoryCandidate/MemoryItem/source/revision/governance 表与 RLS | migration/store | scope、状态、来源、新鲜度完整 |
| 06-03 | 实现 Candidate 提交、隔离、拒绝、批准、晋升 | governance service | 未经 Eval/Draft 不进正式 Wiki |
| 06-04 | 实现 PII/tenant/source/license/freshness/dedupe/conflict/applicability 门 | governance | 一次成功/模型自述不可晋升 |
| 06-05 | 实现 KnowledgeQuery 与渐进上下文装配 | retrieval | token 预算、marking、time cutoff 生效 |
| 06-06 | 复用 O1 Wiki/KnowledgeSubject authority | ontology wiki adapter | 不直接改写封板 authority |
| 06-07 | 建全文/向量可重建索引与 scoped refs | index adapters | 清空索引不改变 canonical 状态 |
| 06-08 | 启用种子导入与人工经验 P0 管道 | ingestion jobs | source/hash/license/复审时间完整 |
| 06-09 | 启用运营反哺/客户聚合/专业库 P1 管道 | candidate jobs | 组织内最小化，跨组织只发布投影 |
| 06-10 | 启用网络/竞品 P2 管道 | research adapter | 防提示注入，不存未授权全文 |
| 06-11 | 外部 DeerFlow 研究只接 Artifact/Draft/Candidate | research input | provider memory 不成为 AOS 真源 |
| 06-12 | Memory Governance/Wiki 页面与引用解释 | API/web | stale/conflict/revoked 可见且阻断 |
| 06-13 | 管道1 种子知识导入 | ingestion/manifest | 方案、SOP、平台规则均有 source/hash/license |
| 06-14 | 管道2 运营实践自学习 | task completion candidate job | 只生成 Candidate，一次成功不能晋升 |
| 06-15 | 管道3 网络学习 | scheduled ResearchJob | 防注入、限量、引用、时效、L4 门控 |
| 06-16 | 管道4 竞品分析 | scheduled ResearchJob | 只存允许摘要/事实，不复制未授权全文 |
| 06-17 | 管道5 专业知识库 | professional adapter | CosDNA/NMPA 等来源先过授权、许可与版本核验 |
| 06-18 | 管道6 客户反哺、管道7 人工经验 | event/manual candidate jobs | 聚合/去敏；人工经验也需冲突与适用范围治理 |
| 06-19 | 建七管道 Scheduler、Run、Receipt、checkpoint 和状态看板 | scheduler/API/web | 七条独立开关、重试、暂停、回读、告警 |
| 06-20 | 建美妆 VerticalPack manifest、来源清单、Candidate 导入与回滚 | vertical knowledge bundle | 先通过逐条 source/license/hash 门；目标量不足时 DATA_BLOCKED，不用示例凑数 |
| 06-21 | 建审核制金标集、检索质量和六角色语义依赖 Eval | evals/retrieval | ≥50 条已审核 gold 才计算 Top-1≥80%；不足时 EVAL_BLOCKED |
| 06-22 | 实现全文召回、可选向量、RRF/重排和引用装配 | retrieval adapters | 权限先于召回；lane 独立报 capability；空/坏/缺依赖诚实降级 |
| 06-23 | 建个人记忆、共享投影和跨角色最小披露 | memory projection | 不共享工作记忆/敏感会话；共享项有治理 revision |
| 06-24 | 建记忆改进度量与撤回影响分析 | evals/governance | 用 Eval/人工修改率/事实率证明改进，不以文本量代替 |

## 2. 七条知识管道冻结表

| 管道 | 触发 | 默认级别 | 当前清单状态 |
|---|---|---|---|
| 种子知识 | 手动冷启动 | P0/L1 | REQUIRED |
| 运营实践自学习 | Task 完成事件 | P2/L3 | REQUIRED，先 Candidate |
| 网络学习 | 定时 ResearchJob | P2/L4 | REQUIRED，来源未核验则 blocked |
| 竞品分析 | 定时 ResearchJob | P3/L4 | REQUIRED，外部全文受限 |
| 专业知识库 | 定时/版本事件 | P0/L1-L2 | REQUIRED，适配器/许可未就绪则 blocked |
| 客户数据反哺 | 订单/评价/服务事件 | P1/L3 | REQUIRED，只允许聚合去敏事实 |
| 人工经验 | 人工提交 | P0/L2 | REQUIRED，不能绕过治理 |

原 06-08～06-10 的 P0/P1/P2 分组只是优先级视图，本表才是七条管道的完整交付目录。

## 3. 三层运行记忆与 Procedural 裁决

- Working：任务级 TTL，上下文和中间结果。
- Episodic：有条件、结果、EffectReview 的经历，可过期/撤回。
- Semantic：稳定事实和经验证知识，版本化治理。
- Procedural：Skill/Logic/Policy/Playbook 的版本化发布资产；不创建第四套运行时 Memory store。

所有跨角色共享只发布经治理的最小投影；跨租户最多复用脱敏、抽象、获授权的方法资产，不复用租户业务数据。

## 4. 删除、撤回与失败语义

- source 撤回先阻止新检索，再重建索引；payload 删除只保留最小不可反查审计哈希。
- 检索超时、索引缺失、来源冲突返回 blocked/degraded，不跨租户或静默用旧缓存。
- provider 临时 memory/checkpoint 有 TTL 和清理 Receipt，不影响 canonical Wiki/Memory。

## 5. 退出门

- [ ] 每次回答可查看 Wiki revision、source、freshness、confidence、applicability。
- [ ] 同名公共包/组织知识/工作区记忆解析稳定并显示冲突。
- [ ] stale/revoked/撤回来源不进入新上下文；向量索引不是授权真源。
- [ ] 外部研究、客户数据、人工经验均经过统一 Candidate 晋升链。
- [ ] 七条管道分别具有 Schedule/Run/Receipt/checkpoint、状态页和失败/恢复证据。
- [ ] 美妆冷启动达到量化门；来源和许可证不满足时保持 blocked，不用示例知识凑数。
- [ ] 检索 Eval 包含关键词、语义、混合、重排、权限、新鲜度、冲突和引用正确性。
- [ ] 六数字同事各有个人记忆策略，共享投影不暴露另一同事的工作记忆或客户敏感会话。

## 6. 当前执行顺序

- [x] E0：冻结公共契约与 ADR；复核 `aip_long_memory.py`/TAOR/O1 Wiki 现状，证明没有平行生产真源。代码 `bb84fc3`；新旧兼容记忆回归 15 passed，compile/diff check GREEN。
- [x] E1A：Candidate/Item/Source/Revision/Event authority migration、RLS/FORCE RLS、升降级与隔离测试。代码 `07c974e`；20 passed；单 head `aip5_001`。
- [x] E1B：Candidate store、CAS 和合法状态机。代码 `2692f1e`；AIP-5 与邻接 AIP-4 Store 33 passed。
- [x] E2：七类治理门与统一晋升服务。代码 `ab7b8aa`；累计 41 tests passed。
- [x] E3：KnowledgeQuery、渐进上下文、O1 Wiki adapter 和可重建索引。代码 `81c5f82`；8 个专项、累计 50 tests passed。
- [x] E4：Canonical API/SDK/治理页面与浏览器验收。
- [x] E5：七知识管道的 Schedule/Run/Receipt/checkpoint；E5A～E5D 代码、自动化、真实 API 与内置浏览器证据已封板。
- [ ] E6：美妆 VerticalPack、全文/可选向量检索与量化 Eval；方案已通过，外部数据门独立阻断。
- [ ] E7：六同事个人记忆/共享投影、撤回影响与改进度量。

本清单中的全量授权不允许跨波偷跑；每个子波必须更新 `01-当前项目状态.md` 和 `06-当前执行检查点.md` 并形成安全提交。

E0 实施结论：运行层只允许 Working/Episodic/Semantic；Procedural 继续作为版本化 Skill/Logic/Policy/Playbook，Shared 只作治理投影。Working 不进入 Candidate 晋升链；写请求 DTO 不接受租户字段；Semantic Candidate 必须保留精确来源、hash、新鲜度、适用范围，并在批准/晋升前绑定 Eval report、Draft 和 ApprovalEvent。旧 `aip_long_memory.py` 与 `ontology_wiki_engine.py` singleton 明确降级为兼容层，不是生产权威。

E1A 实施结论：新增 SourceRevision、Candidate、CandidateEvent、Item、ItemRevision 五张 additive authority 表；全部 FORCE RLS。Source/Event/Revision 追加不可变，Candidate/Item 为后续 CAS 状态载体；Candidate 外键绑定同租户 Task/Run，Item.current_revision 精确绑定自己的 Revision。disposable PostgreSQL 验证正向 `org-org/dev-project`、负向 `dev-org/dev-project`、无 scope 零可见/禁止写、迁移降升级与既有权威表行数守恒；本波未注册 API、未写真实业务记录。

E1B 实施结论：新增唯一 `AipMemoryStore`，实现 SourceRevision 与 Candidate 精确幂等、Candidate 事件时间线、expected-version CAS、合法状态迁移、治理证据绑定及 Candidate→Item+Revision 原子晋升。网络重试可精确回读同一晋升结果；Working 禁止持久化；跨租户、旧版本、来源漂移、非法状态和绕过 Item 的直接 promoted 均失败关闭。Store 重建后仍从 PostgreSQL 回读；本波仍未注册 API。

### 6.1 E2 统一治理服务冻结（2026-08-12）

E2 不新增审批、Eval、PII 或许可证真源，而是在 `AipMemoryStore` 之上新增唯一 Governance Service：

1. `tenant`：仅使用服务端 `TenantScope`，Candidate/Task/Run/Source/Memory 全部由 RLS 和 scoped query 回读；缺失或跨租户按不可见失败关闭。
2. `source`：受信 Artifact Inspector 必须返回与 Candidate payload 完全一致的 `artifact_id/revision/content_hash`；不接受调用方自报的哈希或脱敏结果。
3. `PII`：Inspector 只允许 `clear` 或有精确脱敏证据的 `redacted`；`contains_pii/unknown`均隔离。
4. `license`：由受信 License Policy Resolver 核验 SourceRevision 的 `license_id + usage_policy`；`denied/unknown`均隔离。
5. `freshness`：审批和晋升两个时点均检查 `freshness_expires_at > now`，防止审批后过期仍晋升。
6. `dedupe/conflict`：在同租户、同 subject 的正式 Memory authority 中查询；同 hash 是 duplicate，异 hash 是 conflict，均不默认覆盖。
7. `applicability`：请求的适用目标必须是 SourceRevision `applicability` 的子集；缺失、空值或越界均隔离。

reason codes 冻结为：`tenant_scope_invalid`、`source_artifact_unverified`、`source_hash_mismatch`、`pii_detected`、`pii_status_unknown`、`license_denied`、`license_status_unknown`、`source_stale`、`duplicate_memory`、`memory_conflict`、`applicability_missing`、`applicability_mismatch`、`eval_authority_invalid`、`draft_authority_invalid`、`approval_authority_invalid`。

统一入口执行 `pending/quarantined -> approved`；任一门失败或未知时原子转为 `quarantined` 并写 CandidateEvent。只有全门通过且 PostgreSQL 精确回读 Eval report `gate_passed=true`、Draft `status=approved`、ApprovalEvent `decision=approved` 且三者 proposal version/hash 自洽时才允许 approved。晋升入口在调用 Store 原子晋升前重检时效、Artifact/PII/许可和去重冲突；调用方不得直接将 Candidate 写为 approved/promoted。

E2 实施结论：`AipMemoryGovernanceService` 已成为唯一治理决策入口；精确 Artifact Inspection 与 redaction Receipt、License Resolver、时效、适用范围、同 subject 去重/冲突、PostgreSQL Eval/Draft/Approval authority 全部 fail closed。审批失败写入 quarantined CandidateEvent；晋升前重做时效与治理检查。新增 14 个 PostgreSQL 集成用例，与 E0/E1A/E1B、AIP-3/AIP-4 相邻权威累计 41 tests passed；compileall 和 diff check GREEN。

E3 实施结论：`AipMemoryRetrieval` 只从 tenant-scoped PostgreSQL authority 解析正式 Memory，按 workspace/organization/public_package 优先级装配主 subject 与 object refs。授权 markings、applicability、time cutoff、freshness、revoked/conflict 在正文解析前失败关闭；payload 与 citation 精确 hash 绑定，token 预算不截断 chunk。O1 Wiki 只读 adapter 仅接收完整治理 envelope，legacy 或正文/payload hash 漂移 blocked。reference-only 索引可清空重建，unavailable 时诚实回源并标记 degraded。全文/向量混合检索仍属 E6。代码 `81c5f82`；8 个专项、累计 50 tests passed。

### 6.3 E4 执行拆分

- [x] E4A：新增 `/v1/aip/memory-authority` Canonical API；候选/事件/正式 Memory 列表与详情，approve/promote，KnowledgeQuery；认证租户与角色矩阵、错误映射、OpenAPI 和 `extra=forbid` 测试。代码 `17817db`；AIP-5 相关 38 tests passed，路由聚合 520 项一致。
- [x] E4B：新增唯一 `apps/web/src/api/aipMemory/` contracts/client；严格解析 tenant、revision/hash/source/freshness/applicability/citation，不接受缺字段成功响应。代码 `cc8f216`；SDK/AIP client 6 tests、TypeScript GREEN。
- [x] E4C：新增 `MemoryGovernancePage` 并接导航；候选、正式 Memory、Knowledge Query 三视图覆盖 idle/loading/empty/error/blocked/degraded/complete；O1 Wiki 只增加治理入口和引用解释，不改变 Draft 写链。代码 `038b9da`。
- [x] E4D：后端累计回归、前端定向/全量、TypeScript/build、`org-org/dev-project` 内置浏览器逐项点击；`dev-org` 仅 API 负向 canary；更新上下文、记忆与安全提交。

E4D 实施结论：E4B 复审补强 `8b08792`，深层严格解析 tenant/source/governance/Event/Item/Revision/Citation 并补齐 events/approve/promote SDK；E4C 页面 `038b9da`，三视图、导航、O1 Wiki 治理入口与交互诚实清单完成。后端 38 passed；前端定向 21、全量 2053 tests、TypeScript、Vite build（274 modules）与 diff check GREEN。内置浏览器只使用 `org-org/dev-project`，验证导航、三视图、必填阻断、API 500 错误态、Wiki 入口和控制台错误 0；不把环境 500 冒充正向回包。按用户要求暂停于 E5 前。

### 6.4 E5 执行拆分（2026-08-12 复审通过）

#### E5A：契约与 PostgreSQL authority（IMPLEMENTED_GREEN · `0f40442`）

- [x] `aip_memory_pipeline_contracts.py`：冻结七种 `pipelineKind`、Schedule/Run/Receipt/Checkpoint/Alert DTO 与状态机；写 DTO 不接受 org/project、凭据或任意 provider payload。
- [x] `aip5_002_memory_pipeline_control.py`：新增 schedule/run/receipt/receipt-candidate/checkpoint revision/alert 六类 authority；全部 RLS + FORCE RLS。
- [x] Schedule/Run 使用 expected-version 和 idempotency key/request hash；Receipt、ReceiptCandidate、Checkpoint revision、Alert 追加不可变。
- [x] Run 外键精确绑定同租户 `aip_task/aip_task_run`；每个输出 Candidate 由独立关联表在同 scope 做 FK 约束。
- [x] disposable PostgreSQL 验证 upgrade/downgrade、单 Alembic head、无 scope、`org-org/dev-project`、`dev-org/dev-project` canary 和既有表行数守恒；12 targeted / 55 cumulative passed，compileall/diff/敏感词 GREEN，Ruff unavailable。

#### E5B：Store、CAS 与恢复（IMPLEMENTED_GREEN · `25ada61`）

- [x] `aip_memory_pipeline_store.py`：Schedule create/read/list/transition；Run enqueue/claim/read/list/transition；terminal Receipt、Alert 和 checkpoint 原子提交。
- [x] idempotency key 仅从可信请求头/服务参数进入，request hash 由服务端对 actor + 严格 DTO 生成；同 scope + key + hash 精确重放，异 hash conflict。
- [x] Schedule create/transition 与追加不可变 `PipelineScheduleEvent` 同事务提交；变更失败不留可变行脏状态。
- [x] Run enqueue/claim/pause/resume/terminal/lease-expired 与追加不可变 `PipelineRunEvent` 同事务提交；非终态 `reasonCode` 不丢弃。
- [x] 服务重建后 PostgreSQL 回读 Schedule/Run/Receipt/checkpoint/ScheduleEvent/RunEvent 一致，不使用进程内字典。
- [x] 失败/取消/unknown/暂停不推进 checkpoint；成功/partial 仅可 expected-version CAS 前进，不能回退。
- [x] Candidate 的 tenant/task/run/revision 必须与 Pipeline Run 一致；漂移或跨租户失败关闭并留 Alert。
- [x] retry 创建新 run/attempt 并绑定 `retryOfRunId`；terminal run 不重开；租约过期仅原子转 unknown。
- [x] E5A–E5B 专项 21 tests / 累计 AIP-5 64 tests passed；单 head `aip5_003`，compileall/diff/敏感信息 GREEN，Ruff unavailable。

#### E5C：七管道策略与可信适配器门

- [x] `aip_memory_pipeline_service.py`：七 kind 各自 trigger allowlist、默认状态、依赖门、source/license/freshness policy。
- [x] 冻结 `PipelineDependencySnapshot`：服务端生成、精确绑定 PostgreSQL `aip.eval_report`；缺项/unknown/过期/集合漂移均 fail closed。
- [x] `seed_import/human_experience` 首期 paused；`operational_learning/customer_feedback` paused；`network_learning/competitor_analysis/professional_database` 在真实适配器和许可未就绪时 disabled。
- [x] 外部 DeerFlow/Harness 只提交 Artifact/Research receipt，再经可信 adapter 产生 Candidate；provider checkpoint/memory 不成为 AOS 真源。
- [x] adapter registry 默认空，只登记版本化 contract/kind/Receipt allowlist；Service 回读 Receipt 后二次校验 Task/Run/SourceKind/source_ref/license/freshness，再经 `AipMemoryStore` 写 Source revision 与 Candidate。
- [x] paused 不接受自动 trigger；仅允许 manual 的 kind 可授权人工单次 Run；disabled 全部阻断；Schedule 创建状态必须等于 kind 默认状态。
- [x] 本子门只实现 adapter registry/调用边界和 fake adapter 单元测试；未拉真实外部数据，未导入示例知识。代码 `c0282d4`；E5C 17 tests / AIP-5 累计 75 tests GREEN。

#### E5D：Canonical API、SDK/页面与封板

- [x] 在 `/v1/aip/memory-authority/pipelines` 增 schedule/run/receipt/checkpoint/alert 的 tenant-scoped API；内部 complete 接口只允许受信 executor。代码 `db27919`。
- [x] 角色矩阵：GET=认证租户；Schedule 写=admin/reviewer；Run 登记=admin/executor/aip_executor；complete=executor/aip_executor + 当前 lease owner；不接收 caller 自报 tenant/hash/dependency-ready。
- [x] `apps/web/src/api/aipMemory/` 扩展唯一严格 SDK；未知枚举/缺失 hash/version/tenant 失败关闭。代码 `3492970`。
- [x] `MemoryGovernancePage` 增“知识管道”视图，覆盖 loading/empty/error/disabled/paused/active/running/failed/blocked；每个操作有真实 API 或明确禁用理由。
- [x] SDK 严格对齐 Canonical `ResourceRef.authority` 与 `ArtifactRef.artifactType/artifactId/revision/contentHash`；可空 Receipt/Checkpoint 使用对象信封，未知枚举/缺 hash/tenant 漂移失败关闭。
- [x] 后端累计 74、前端定向 12、前端全量 174 files / 2057 tests、TypeScript、Vite build、OpenAPI 六路由、diff check、真实 API 7/0/0 与 `org-org/dev-project` 内置浏览器验收；`dev-org` 只作 API/测试负向 canary。
- [x] 更新 `01-当前项目状态.md`、`06-当前执行检查点.md`、Prime/shared-memory 投影并形成代码/文档安全提交。

E5 统一边界：不复制 AIP Task/Run/Checkpoint，不以 `meta_schedule_run` 冒充 AIP-5 控制面，不保存外部全文/PII/密钥，不在 migration 创建真实租户 schedule，不提前执行 E6 冷启动或 E7 个人/共享记忆。

### 6.5 E6 执行拆分（2026-08-13 复审通过）

- [x] E6A：为 `VerticalPack` 冻结知识出口、package manifest/source inventory/hash/回滚契约；未知许可、路径穿越和 hash 漂移失败关闭。代码 `f3415a9`；212 回归、compileall、diff check GREEN。
- [ ] E6B：实现可信 bundle seed adapter，只经 E5 Receipt + Candidate 链导入；重放幂等，异 hash 冲突，失败不推进 checkpoint。
- [ ] E6C：实现 tenant-scoped 全文 reference index 与 capability registry；RLS/FORCE，索引可重建且不存正文/PII。
- [ ] E6D：新增自然语言 `KnowledgeSearch`，保留 E3 精确 `KnowledgeQuery`；授权先行，全文/向量/重排独立 capability，Citation 必填。
- [ ] E6E：实现 gold-set schema、Eval runner 和六角色语义依赖检查；未审核或少于 50 条时禁止生成 Top-1 GREEN。
- [ ] E6F：控制面展示知识包、来源门、检索 lane、Eval 与阻断原因；完成 `org-org/dev-project` 内置浏览器验收。

E6 外部数据门：CosDNA 许可未知，保持 disabled；NMPA 需登记当前动态清单版本与使用政策；旧方案 353 条只作目标，不是资产；当前无 pgvector，向量 lane 必须 degraded。详见 `AOS项目开发上下文/50-2026-08-13-AIP-5-E6美妆知识包与混合检索评审清单.md`。
