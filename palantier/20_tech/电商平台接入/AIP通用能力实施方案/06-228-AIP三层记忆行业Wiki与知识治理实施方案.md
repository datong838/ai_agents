# 228-AIP 三层运行记忆、行业 Wiki 与知识治理实施方案

> 状态：**IMPLEMENTING · v1.7 · 已获用户全量编码授权 · E0～E5 IMPLEMENTED_GREEN · E6 REVIEWED / APPROVED_FOR_IMPLEMENTATION_WITH_EXTERNAL_DATA_GATE**
> 对应阶段：AIP-5。
>
> 2026-08-11 补充：外部研究 Harness 的知识入口 v1.2 已评审通过。2026-08-12 对账：总控全量编码授权已取代历史“不授权编码”门，但每个子波仍需方案、检查点、测试、浏览器与安全提交。

## 1. 统一模型

旧“行业 Wiki 三层记忆”和 G4“四层多智能体记忆”统一解释为：

| 层 | 作用 | 真源 |
|---|---|---|
| Working | 当前 TaskRun 上下文、Selection、步骤产物 | Task/Checkpoint store |
| Episodic | 一次任务、结果、失败和效果观察 | Run/EffectReview/Evidence |
| Semantic | 经治理的行业知识、规则、概念和方法 | O1 Wiki/KnowledgeSubject |
| Procedural | 可执行方法，但不是第四套运行记忆库 | 版本化 Skill/Logic/Policy 资产及其 Eval/Receipt |
| Shared | 不是第四种存储；是经授权、脱敏、适用范围明确的 Semantic/Episodic 投影 | governed MemoryItem |

禁止再用 `aip_long_memory.py` singleton 形成另一套生产记忆。

## 2. 知识晋升链

```text
Task/Effect evidence
 -> MemoryCandidate
 -> PII/tenant/source/freshness check
 -> dedupe/conflict/applicability
 -> repeated evidence or controlled comparison
 -> Eval regression
 -> Draft approval
 -> MemoryItem/Wiki revision
 -> monitor/expire/revoke
```

一次成功、模型自述、竞品文案、其他租户明细不得直接晋升。

## 3. 七条知识管道的启用顺序

| 管道 | 首期策略 |
|---|---|
| 种子知识导入 | P0；只导入已授权文档，保留 source/hash/license |
| 运营实践自学习 | P1；先生成 Candidate，不自动入正式 Wiki |
| 网络学习 | P2；官方源优先，防提示注入与版权全文入库 |
| 竞品分析 | P2；只存事实摘要和引用，不存抓取全文 |
| 专业数据库 | P1；授权、版本和时效单独治理 |
| 客户数据反哺 | P1；组织内、最小化、聚合后才共享 |
| 人工经验注入 | P0；作者、适用范围、复审时间必填 |

### 3.1 外部研究 Harness 输入

- DeerFlow 等研究 Harness 的报告、网页事实和子任务结论只能生成 `Artifact`、`ReportDraft`、`InsightDraft` 或 `MemoryCandidate`，禁止直接写正式 Wiki/Memory。
- 每个 Candidate 必须携带 tenant/task/run、source URL 或 source ref、observed_at/freshness、license/usage policy、artifact hash、provider/version 与适用范围；缺失任一治理字段即隔离。
- 外部网页、MCP 返回和远程 Skill 一律按不可信输入处理：内容中的工具调用、系统指令、越权写入或凭据请求不得进入执行上下文。
- 外部 provider 的 checkpoint/memory 只用于恢复该次 Job，不能成为 AOS Working/Episodic/Semantic 真源；provider 停用不影响 canonical Memory/Wiki 可读性。
- 研究结论需经过去重、冲突、新鲜度、可信源和 Eval/Draft 门控，才可沿既有晋升链进入正式知识。

## 4. 检索与上下文装配

- 输入是 `KnowledgeQuery`：subject、task/skill、object refs、time cutoff、marking、max tokens。
- 输出是引用集合：Wiki revision、field/value、source、freshness、confidence、applicability。
- TAOR Think 按 Skill manifest 声明的知识依赖渐进加载。
- 过期、冲突、无权限、来源撤回时明确降级或阻断，不返回旧知识伪装新鲜。
- 向量库/全文索引只保存可重建索引和 scoped reference，不是授权、revision、source 或知识内容的权威真源。
- 公共行业包、组织知识和工作区运行记忆分别建 scope；“共享”必须显式发布投影，不能通过缺省查询跨 scope 命中。

### 4.1 E3 权威过滤与可重建索引裁决（2026-08-12）

- E3 的 `KnowledgeQuery` 是 subject/task/skill/object refs 驱动的渐进上下文装配，不是任意自由文本搜索。混合全文/向量召回、融合和重排仍属 E6，E3 不提前偷跑。
- 解析顺序固定为 `workspace -> organization -> public_package`；高优先级 scope 只能覆盖精确同 subject 且适用范围满足的低优先级条目。同 scope/同 subject 异 hash 为 conflict，不任选其一。
- 先从 PostgreSQL Memory/Wiki authority 执行 tenant、marking、status、time cutoff、source freshness、applicability 过滤，再允许索引 reference 参与排序；“先向量命中后补权限”禁止。
- token 预算按确定性 citation 优先级从高到低装配；单条超预算不截断成无法校验的半条知识，而是跳过并返回 degraded reason。
- 索引只存 `org/project + memory_item_id + revision + content_hash + searchable terms`；不存知识正文、不授权、不替代 revision/source。索引丢失时可从 PostgreSQL authority 重建，重建前可用 authority scan 诚实降级。
- O1 `wiki_page/wiki_page_version` 保持只读适配，不改已封板表与写路由。只有 Wiki body 内已含完整 governance envelope（source/hash/license/freshness/confidence/applicability/markings）的精确 revision 可转为 citation；历史缺字段页面返回 degraded/blocked，禁止填默认值伪装已治理。

## 5. 文件边界

```text
services/aos-api/alembic/versions/*_aip_memory_governance.py
services/aos-api/aos_api/aip_memory_store.py
services/aos-api/aos_api/aip_memory_retrieval.py
services/aos-api/aos_api/aip_memory_governance.py
services/aos-api/aos_api/aip_memory_pipeline_contracts.py
services/aos-api/aos_api/aip_memory_pipeline_store.py
services/aos-api/aos_api/aip_memory_pipeline_service.py
services/aos-api/aos_api/aip_taor_loop.py
services/aos-api/aos_api/ontology_wiki_engine.py
apps/web/src/api/aipMemory/*
apps/web/src/pages/s2/MemoryGovernancePage.tsx
apps/web/src/pages/ontology/Wiki*.tsx
```

新增候选为 Candidate store、retrieval 和 governance service；现有 `aip_long_memory.py`、`aip_taor_loop.py`、`ontology_wiki_engine.py` 为迁移/适配修改。不得直接改写已封板 O1 Wiki authority；新增能力通过其公共写契约或独立候选区接入。

## 6. 生命周期与失败语义

- Candidate 状态：`pending -> quarantined/rejected -> approved -> promoted`；MemoryItem 状态：`active -> stale -> revoked/expired`。
- source 撤回先停止新检索，再异步重建索引；索引尚未清理期间由权威状态在查询层 fail-closed。
- 用户删除/PII 撤回删除可删除 payload 和索引，历史 Lineage 仅保留最小审计哈希、删除事件和不可反查引用。
- 检索超时、索引缺失、来源冲突时按 Skill policy 返回 blocked/degraded，绝不静默改用其他租户或旧缓存。

## 7. 验收

1. 同一知识在不同 org/project 下不可见，除非是授权公共包。
2. 每个回答/决策可查看使用了哪些 Wiki revision 与 source。
3. stale/conflict/revoked 知识不能静默进入上下文。
4. Candidate 未经 Eval/Draft 不得成为正式共享知识。
5. 删除/撤回知识后，新运行不再使用；历史谱系仍保留不可变引用。
6. 公共包、组织知识、工作区记忆三类同名条目按适用范围和优先级稳定解析，并显示冲突。
7. 重建或清空向量索引不改变 canonical Wiki/Memory 状态，恢复后查询结果可复验。
8. 外部研究 provider 停用、断连或返回提示注入内容时不污染正式 Wiki/Memory，且对应 Candidate、阻断原因和来源证据可回读。

## 8. 实施分波与安全提交边界

| 子波 | 范围 | 主要文件 | 退出门 |
|---|---|---|---|
| E0 | 运行记忆/Procedural/Shared 裁决、公共契约、ADR、现状真值测试 | `aip_memory_contracts.py`、契约测试、ADR/清单 | 不建第四套运行记忆库；scope/source/license/freshness/applicability 字段冻结；无数据库变更 |
| E1A | Candidate/Item/Source/Revision authority schema、RLS/FORCE RLS、append-only event | migration、schema tests | 单一 Alembic head；无 GUC 零可见；同 ID 跨 scope 隔离；升降级可逆 |
| E1B | Candidate authority store 与状态转换 | `aip_memory_store.py`、store tests | pending→quarantined/rejected/approved/promoted 合法；非法跳转、CAS、跨租户失败关闭 |
| E2 | PII/source/license/freshness/dedupe/conflict/applicability 治理服务 | `aip_memory_governance.py` | 缺治理字段隔离；一次成功/模型自述不可晋升；Eval/Draft 引用精确 |
| E3 | KnowledgeQuery、渐进上下文与 O1 Wiki adapter | `aip_memory_retrieval.py`、`ontology_wiki_engine.py` adapter | 权限先于召回；stale/conflict/revoked 不返回；索引只存可重建 refs |
| E4 | Canonical API、OpenAPI、Memory Governance/Wiki 页面 | router、`apps/web/src/api/aipMemory/`、页面 | 唯一 SDK；真实 idle/loading/empty/error；无静态知识回填 |
| E5 | 七知识管道 Scheduler/Run/Receipt/checkpoint | ingestion/research/scheduler | 七条独立开关、幂等、重试、暂停、回读、告警；外部 Harness 只进 Candidate |
| E6 | 美妆冷启动知识包、检索融合/重排、50 查询 Eval | manifest/import/retrieval/evals | 数量、来源、许可和 Top-1 门达标；不以示例数据凑数 |
| E7 | 六同事个人记忆、共享投影、改进度量、撤回影响分析 | projection/evals/web | 最小披露；不跨租户共享业务明细；以 Eval/人工修改率证明改进 |

执行顺序固定 E0→E1A→E1B→E2→E3→E4→E5→E6→E7。每个子波完成后更新 `AOS项目开发上下文/01-当前项目状态.md`、`06-当前执行检查点.md`，形成代码与文档安全提交；若实时代码与本表冲突，以 PostgreSQL/O1 公共契约和代码真值为准，先修订方案再编码。

### 6.1 E3 实施结论（2026-08-12）

E3 已以代码 `81c5f82` 实现权威 `KnowledgeQuery`、渐进上下文、O1 Wiki 只读适配器与可清空重建的 reference-only 索引。检索按 `workspace → organization → public_package` 稳定解析；服务端授权 markings、applicability、time cutoff、Memory 状态、source freshness 均在 payload 解析和上下文组装前过滤。请求 markings 不能扩大服务端授权，同层异 hash 冲突、撤回、未来生效、过期来源、跨租户、payload/hash 漂移均失败关闭。

上下文按主 subject 后接去重的 `object_refs` 渐进装配，token 预算只允许完整 chunk，不截断半条知识；每个 chunk 与 citation 一一对应且 token 总数由契约复核。索引只保存 `memory_item_id/revision/content_hash/subject_key`，不保存知识正文；索引 unavailable 时显式降级为 PostgreSQL authority scan，清空或重建不改变 canonical Memory。

O1 Wiki adapter 不改写既有 `wiki_page`，只有具备完整 governance envelope、精确 source/freshness/license/applicability/markings、正文 hash 与 payload hash 一致的页面才可读取；历史 legacy 页面继续 blocked。E3 8 个专项 PostgreSQL 场景、AIP-5 全链及相邻 AIP-3/AIP-4 累计 50 tests passed，compileall 与 diff check GREEN。全文/向量召回、融合与重排仍留在 E6，没有在 E3 伪装完成。

### 6.2 E4 Canonical API、SDK 与页面冻结（2026-08-12）

现状核查确认 `/v1/ontology/wikis` 仍由历史 in-memory `ontology_wiki_engine` 驱动，`/v1/wiki/*` 与 `/ontology/wiki` 属于 O1 对象 Wiki/Draft 链；两者都不得改名或包装成 AIP-5 Memory authority。E4 新增独立 `/v1/aip/memory-authority`，只暴露 E1～E3 已存在的 PostgreSQL authority、Governance Service 与 KnowledgeQuery，不修改 O1 写路由。

Canonical operations 冻结如下：

- `GET /candidates`、`GET /candidates/{id}`、`GET /candidates/{id}/events`：租户范围内治理候选、详情和不可变事件；支持服务端枚举状态过滤与有界 limit。
- `POST /candidates/{id}/approve`、`POST /candidates/{id}/promote`：仅 `admin/reviewer`；调用唯一 Governance Service，客户端只提交 expected version、精确 Governance refs、适用范围和目标 item ID，不提交 org/project、PII 或许可证结论。
- `GET /memories`、`GET /memories/{id}`：租户范围内正式 Memory 与精确 current revision；无权或跨租户统一不可见。
- `POST /knowledge-queries`：仅 `admin/reviewer/executor/aip_executor/developer`；authorized markings 只取认证 Principal，客户端 `markings` 只是请求约束，不能授权自己；payload resolver 未配置或 hash 漂移时返回契约内 blocked/degraded，不生成静态正文。

错误映射冻结：not found=404、CAS/conflict=409、治理/状态/授权门=422、角色不足=403、authority/payload resolver unavailable=503；未知异常不回显内部 SQL。OpenAPI DTO 必须 camelCase 且 `extra=forbid`。

前端唯一入口为 `apps/web/src/api/aipMemory/`，严禁页面散落 `apiGet/apiPost` 或继续调用 in-memory Wiki API 冒充治理。新增 `MemoryGovernancePage` 作为候选/正式 Memory/Knowledge Query 三视图；O1 `WikiPage` 保持原职责，并增加“治理权威”入口与 citation/blocked 解释。页面必须真实覆盖 idle/loading/empty/error/blocked/degraded/complete；没有权威数据时显示空态或阻断原因，禁止 MOCK、默认知识和示例命中。浏览器验收只使用 `org-org/dev-project`，`dev-org` 只作 API 负向 canary。

### 6.3 E4 实施结论（2026-08-12）

E4 已完成并封板：Canonical `/v1/aip/memory-authority` API、唯一 `apps/web/src/api/aipMemory/` SDK、`MemoryGovernancePage`、AIP 导航和 O1 Wiki 治理/Citation 入口均已落地。SDK 复审补强为深层严格解析 tenant、Candidate request/source/governance、不可变 Event、Item/Revision、payload hash 与 Citation/Chunk 一一对应；事件、审批、晋升、检索全部复用唯一 AIP client。代码提交依次为 `17817db`、`cc8f216`、`8b08792`、`038b9da`。

页面包含 Candidate、正式 Memory、Knowledge Query 三视图；真实空列表不注入示例，blocked/degraded/complete 与错误分别显示。批准/晋升没有用不完整表单开放：缺精确 Eval report、Draft、ApprovalEvent 时必须继续由服务端 Governance Service 失败关闭。O1 Wiki 原 Draft 写链未改，仅新增治理入口和 Agent 读取前的 scope/freshness/applicability/marking/Citation 说明。

验证结果：AIP-5 后端 contracts/store/governance/retrieval/API 累计 38 passed；前端定向 4 文件 21 tests、全量 174 文件 2053 tests、TypeScript、Vite production build（274 modules）和 diff check 全部 GREEN。内置浏览器确认 `org-org/dev-project`、新导航、三视图、客户端必填阻断、API 异常诚实展示、Wiki 双向跳转及控制台错误 0。当前本机 `aos-api health HTTP 500`，因此只声明 UI/失败关闭浏览器 GREEN，不伪称真实正向回包 GREEN。按用户要求，本波结束后暂停，不自动进入 E5。

### 6.4 E5 七知识管道控制面冻结（2026-08-12）

E5 只建设知识摄取控制面，不复制 AIP-1/2 的 `Task/Plan/Run/Checkpoint` 业务执行真源，也不把历史 `meta_schedule_run` 包装成 AIP-5 权威。知识管道 Run 必须精确绑定同租户既有 `aip_task + aip_task_run`；其 checkpoint 仅表示外部来源游标，不能代替 Task checkpoint 或 Memory revision。

#### 6.4.1 七管道与默认策略

| kind | 中文名 | 允许触发 | 默认状态 | 首期输出约束 |
|---|---|---|---|---|
| `seed_import` | 种子知识导入 | manual | paused | 已授权文档；只生成 Candidate |
| `operational_learning` | 运营实践自学习 | task_event | paused | 绑定 Effect/Evidence；一次成功不得晋升 |
| `network_learning` | 网络学习 | scheduled/manual | disabled | 未配置可信来源/许可/防注入 Harness 时保持 disabled |
| `competitor_analysis` | 竞品分析 | scheduled/manual | disabled | 只允许事实摘要和引用，不保存未授权全文 |
| `professional_database` | 专业数据库 | scheduled/version_event | disabled | 适配器、许可和来源版本缺一即 blocked |
| `customer_feedback` | 客户数据反哺 | domain_event/scheduled | paused | 只允许组织内聚合去敏事实 |
| `human_experience` | 人工经验注入 | manual | paused | 作者、适用范围、复审时间齐全；仍走统一治理 |

`disabled` 表示依赖尚未具备，不能触发；`paused` 表示配置存在但不接受自动触发，允许有权限的人工单次运行；`active` 才接受声明的自动触发。安装/迁移不得创建真实租户 schedule 或自动拉取外部数据，真实启用必须由 Canonical API 产生 Receipt。

#### 6.4.2 权威模型与不变量

1. `PipelineSchedule`：租户内独立配置，保存 kind、触发类型、规范化 schedule spec、配置 ArtifactRef、状态、next run、expected-version CAS 与当前外部游标版本；不保存凭据。
2. `PipelineRun`：绑定 schedule、AIP Task/Run、trigger、attempt、idempotency key/request hash 和状态；同 scope + idempotency key 只能对应完全相同请求。
3. `PipelineReceipt`：每次 terminal Run 唯一、追加不可变，记录结果、输入/输出 hash、Candidate refs、checkpoint 前后版本、计数、错误码与 receipt hash；不得包含外部全文、PII 或密钥。
4. `PipelineCheckpointRevision`：追加不可变；只有成功或诚实的部分成功 Receipt 可在同一事务以 expected-version CAS 推进，失败、unknown、暂停和重放不得推进。
5. `PipelineAlert`：由失败、重试耗尽、source blocked、checkpoint conflict 生成追加不可变告警；ack/silence 通过新 Event/Receipt 表达，不覆盖历史事实。
6. 所有权威表具备 `org_id + project_id` 主键前缀、RLS + FORCE RLS；无 scope 零可见/禁止写，`dev-org/dev-project` 仅作负向 canary。
7. Run 输出的每个 Candidate 必须已存在于同租户 `aip_memory_candidate`，且其 `task_id/run_id` 与 Pipeline Run 绑定一致；外部 DeerFlow/Harness 结果只能先成为 Artifact/Research receipt，再由可信适配器提交 Candidate。
8. `PipelineScheduleEvent`：Schedule create/transition 每次写入一条追加不可变事件，记录 from/to status、version、actor、reason和 dependency review；可变 Schedule 行不能单独充当启停证据。
9. `PipelineRunEvent`：Run enqueue/claim/pause/resume/terminal/lease-expired 每次写入追加不可变事件；状态、version、actor、reason 和 lease owner 必须精确绑定，不能接收 `reasonCode` 后丢弃。
10. idempotency key 由可信请求头/服务参数传入，request hash 必须由服务端对严格 DTO 规范化后生成；写 DTO 不接受调用方自报 request hash，防止伪造幂等证据。

#### 6.4.3 状态机与恢复

- Schedule：`active <-> paused`，`active/paused -> disabled`；disabled 只能在依赖复核和 expected-version CAS 后恢复为 paused，不能直接 active。
- Run：`queued -> running -> succeeded/partial/failed/cancelled`；`running -> paused -> queued` 仅用于可恢复内部执行。terminal 状态不可重开，重试创建新 attempt/new run，并通过 `retry_of_run_id` 关联。
- worker 领取运行必须使用短租约；租约超时只能把结果标记 unknown/告警，不能假定未执行并重复写外部系统。
- 相同 idempotency key + request hash 精确回读；同 key 异 hash 返回 conflict。服务重启后从 PostgreSQL 回读 schedule/run/receipt/checkpoint，不依赖进程内字典。
- Schedule 状态变更必须在同一事务中推进 expected-version 并写入追加不可变 `PipelineScheduleEvent`；事件写入失败时 Schedule 变更整体回滚。
- Run 的所有状态变更必须与 `PipelineRunEvent` 同事务提交；terminal Receipt/Alert 与 terminal RunEvent 精确共享同一版本事实。
- checkpoint 冲突、Candidate 漂移、来源许可/新鲜度 unknown、AIP Task/Run 不匹配全部 fail closed；不得静默跳过或跨租户回退。

#### 6.4.4 Canonical API 与页面边界

- `/v1/aip/memory-authority/pipelines/schedules`：列出/创建；`/{id}` 回读；`/{id}/transitions` 执行 CAS pause/resume/disable。
- `/v1/aip/memory-authority/pipelines/runs`：列出/创建人工或事件运行；`/{id}`、`/{id}/receipts`、`/{id}/alerts` 回读。首期 API 不直接执行外部抓取，只登记/驱动已注册 adapter。
- `/v1/aip/memory-authority/pipelines/runs/{id}/complete`：可信内部 executor 写 terminal Receipt、Candidate refs 和 checkpoint；普通前端用户不可调用。
- Memory Governance 页面增加“知识管道”只读/受控操作视图，覆盖 loading/empty/error/disabled/paused/active/running/failed/blocked；按钮必须有真实 API 或明确禁用原因。

SDK 契约以服务端 `AipContractModel` 的 Canonical JSON 为准：`ResourceRef` 必须包含 `resourceType/resourceId/authority`，`ArtifactRef` 必须包含 `artifactType/artifactId/revision/contentHash`。Checkpoint 与 Receipt 尚未产生时仍返回对象信封 `{checkpoint:null}` / `{receipt:null}`，避免公共 client 把合法空值误判为无效成功响应；未知枚举、缺 authority、缺 revision/hash 或 tenant 漂移全部失败关闭。

E5D 角色矩阵冻结：所有 GET 仍由认证 Principal 的租户 scope + RLS 限制；Schedule 创建/状态变更只允许 `admin/reviewer`；Run 登记只允许 `admin/executor/aip_executor`，paused 人工单次运行还必须显式声明授权；`claim/complete/lease-expire` 不暴露给普通页面，complete 首期仅 `executor/aip_executor` 且必须提交当前 lease owner。API 不接受 caller 自报 tenant、request hash、依赖结果或 adapter ready 状态。

#### 6.4.5 E5 子门与退出证据

| 子门 | 范围 | 退出门 |
|---|---|---|
| E5A | 契约、migration、RLS/FK/append-only | disposable PostgreSQL upgrade/downgrade；单 head；无 scope 零可见；既有行数守恒 |
| E5B | Store、幂等/CAS、ScheduleEvent/RunEvent、checkpoint/Receipt/Alert | 服务端哈希、重启回读、同 key 重放、异 hash conflict、所有状态事件不可变、失败不推进 checkpoint、跨租户不可见 |
| E5C | Service、七管道策略、adapter registry | 七 kind 独立开关；依赖未知 fail closed；Task/Run/Candidate 精确绑定；无真实外部抓取 |
| E5D | Canonical API、SDK/页面、累计回归与浏览器 | 角色矩阵、严格 DTO、真实状态/禁用原因、`org-org/dev-project` 浏览器验收、canary 负向证据 |

E5 不导入美妆知识，不启用网络/竞品/专业库真实抓取，不实现 E6 的全文/向量融合，也不实现 E7 的六同事共享投影。上述能力不得用 seed、Mock 或静态页面提前冒充完成。

#### 6.4.6 E5C 策略与可信适配边界

E5C 的依赖判断使用服务端生成的 `PipelineDependencySnapshot`，每个依赖只能是 `available/unavailable/unknown`，并绑定精确 PostgreSQL `aip.eval_report`。缺项、unknown、过期或依赖集合与管道策略不一致都失败关闭；前端或 provider 自报 `ready=true` 不构成启用依据。七类策略冻结如下：

| kind | 必需依赖（除公共 `task_run_authority/memory_governance/license/freshness`） | 允许的权威输入 Receipt | 默认状态 |
|---|---|---|---|
| `seed_import` | `authorized_source` | `aip.artifact_receipt` | paused |
| `operational_learning` | `effect_evidence` | `aip.effect_receipt` | paused |
| `network_learning` | `trusted_adapter/source_allowlist/prompt_injection_guard` | `aip.research_artifact_receipt` | disabled |
| `competitor_analysis` | `trusted_adapter/source_allowlist/summary_only/prompt_injection_guard` | `aip.research_artifact_receipt` | disabled |
| `professional_database` | `trusted_adapter/source_version` | `aip.research_artifact_receipt` | disabled |
| `customer_feedback` | `aggregate_redaction` | `aip.customer_aggregate_receipt` | paused |
| `human_experience` | `author/applicability/review_due` | `aip.artifact_receipt` | paused |

可信 adapter registry 只注册 `adapter_id + revision + contract_hash + 允许 kind + 允许 Receipt 类型`，默认注册表为空且不保存密钥。adapter 只能接收由服务端 Receipt resolver 回读的精确 `ResourceRef + ArtifactRef`，返回严格 `SubmitMemoryCandidateRequest`；Service 必须再次校验 receipt、kind、Task/Run、SourceKind、source_ref、许可和 freshness，再经 `AipMemoryStore` 登记 Source revision 与 Candidate。adapter 不得直接写 Memory、checkpoint 或 Receipt，也不得执行外部抓取；provider checkpoint/memory、裸 URL、未版本化 Artifact 和调用方自报 Candidate ref 全部拒绝。

paused 管道不接受自动触发；仅当该 kind 明确允许 `manual` 且调用方具有权限时才能人工单次运行，其余 kind 需依赖复核后先激活；disabled 一律不能启动。Schedule 创建状态必须等于该 kind 的默认状态，恢复或激活必须重新通过完整依赖快照，不能只凭一个非结构化“复核通过”引用。

#### 6.4.7 E5A 实施结论（2026-08-12）

E5A 已以代码 `0f40442` 实现七知识管道公共契约和 `aip5_002` PostgreSQL authority。新增 Schedule/Run/Receipt/ReceiptCandidate/CheckpointRevision/Alert 六表；全部 RLS + FORCE RLS，Receipt/ReceiptCandidate/CheckpointRevision/Alert 追加不可变。Schedule/Run 具备租户内 idempotency key、request hash 和 version/CAS 字段；Run 精确外键绑定 AIP Task/Run，每个 Receipt 输出 Candidate 通过独立关联表绑定同租户 `aip_memory_candidate`，没有只靠 JSON 声明引用。

迁移未创建真实租户 Schedule，未复用 `meta_schedule_run`，未注册 API 或拉取外部数据。disposable PostgreSQL 覆盖 upgrade/downgrade、单 head `aip5_002`、无 scope 零可见/禁止写、`org-org/dev-project` 与 `dev-org/dev-project` 隔离、追加不可变触发器和既有 AIP authority 行数守恒；E5A 12 tests、累计 AIP-5 55 tests、compileall、diff/敏感词检查 GREEN。当前 venv 未安装 Ruff，故不声明 Ruff 结果。下一门为 E5B Store/CAS/恢复。

#### 6.4.8 E5B 实施结论（2026-08-13）

E5B 已以代码 `25ada61` 实现 tenant-scoped `AipMemoryPipelineStore`。Schedule 和 Run 写 DTO 不接受调用方自报 idempotency key/request hash；Store 以可信服务参数接收 key，并将 actor 与规范化严格 DTO 一起服务端哈希。同 scope + key + hash 精确重放，异 hash 失败冲突；Schedule/Run 通过 expected-version CAS 变更。

`aip5_003` 新增追加不可变 ScheduleEvent/RunEvent，create、transition、enqueue、claim、pause/resume、terminal 和 lease-expired 都在同一事务留痕。Run 精确绑定 AIP Task/Run 和 Candidate revision；过期租约只能原子转 `unknown + Receipt + Alert`，不假定外部未执行。成功/如实 partial 才能以 checkpoint expected-version 前进；失败、unknown、Candidate 漂移和 checkpoint 冲突失败关闭，且不产生虚假 terminal Receipt。

disposable PostgreSQL 验证了重启回读、服务端哈希重放/冲突、CAS、审计原子性、事件不可变、租约超时、retry attempt、Candidate/Task/Run 精确绑定、checkpoint 成功/失败和跨租户零可见。E5A–E5B 专项 21 tests、累计 AIP-5 64 tests、Alembic 单 head `aip5_003`、compileall、diff/敏感信息检查 GREEN；Ruff 仍 unavailable。未写真实租户 Schedule，未拉取外部数据。下一门为 E5C 七管道策略与可信 adapter 门。

#### 6.4.9 E5C 实施结论（2026-08-13）

E5C 已以代码 `c0282d4` 落地七类独立策略、服务端依赖快照和默认空的版本化可信 adapter registry。Schedule 创建只能使用 kind 的允许 trigger 与默认状态；paused 不接受自动 trigger，仅允许 manual 的 kind 可经授权人工单次运行；disabled 全部阻断。恢复/激活由 Service 回读完整 `PipelineDependencySnapshot`，缺项、unknown、过期、kind/集合漂移或未注册 adapter 均失败关闭。

外部结果只允许以精确 PostgreSQL Receipt + Artifact 进入。Service 在 adapter 调用前复核租户、Task/Run、Receipt 类型、SourceKind、source_ref、许可和 freshness；adapter 输出再次经严格 DTO 解析，并由 Service 绑定原 Receipt 的 Artifact/Source 后调用 `AipMemoryStore` 创建 Source revision 与 Candidate。adapter 无权直写 Memory、Receipt 或 checkpoint。没有注册真实 adapter、没有外部抓取、没有导入 seed/示例知识，也没有创建真实租户 Schedule。

E5C 专项 17 tests、AIP-5 累计 75 tests、compileall、diff/敏感信息检查 GREEN；现有 Pydantic/Starlette warnings 不属于本波，Ruff 仍 unavailable。下一门为 E5D Canonical API、严格 SDK、知识管道页面和浏览器封板。

#### 6.4.10 E5D 实施结论（2026-08-13）

E5D 已由代码提交 `db27919`、`3492970` 完成 Canonical API、唯一严格 SDK 与 Memory Governance“知识管道”控制面。API 覆盖七类 Policy、Schedule 创建/迁移、Run 登记、Receipt、Checkpoint 与 Alert 回读；GET 只依赖认证 Principal 的 tenant scope，Schedule 写只允许 `admin/reviewer`，Run 登记只允许 `admin/executor/aip_executor`。写 DTO 不接受调用方自报租户、request hash、依赖 ready 或 adapter ready；页面只展示 PostgreSQL 权威状态，没有 Schedule 时显示诚实空态和禁用理由，不生成示例 Schedule。

前端 SDK 已严格对齐 `ResourceRef.authority` 与 `ArtifactRef.artifactType/artifactId/revision/contentHash`；可空 Receipt/Checkpoint 使用对象信封，未知枚举、缺 hash/version、tenant 漂移全部失败关闭。后端 AIP-5 累计 74 tests、前端定向 12 tests、前端全量 174 files / 2057 tests、TypeScript、Vite production build、OpenAPI 六条必需路由和 diff check 均 GREEN。开发库已从 `aip4_008` 升级到单 head `aip5_003`；`org-org/dev-project` 真实 API 验证 Policy 7 条、Schedule 空集合 200，未写入业务数据。

内置浏览器已补采 `org-org/dev-project` 的“知识管道”页签、7 条权威策略、0 Schedule/Run、7 个禁用动作、刷新与控制台 0 error；证据为 `AOS项目开发上下文/evidence/2026-08-13-AIP5-E5D-knowledge-pipelines-org-org.png`。因此 E5D 与 E5 总门均为 `IMPLEMENTED_GREEN`。

## 7. E6 美妆 VerticalPack、混合检索与量化 Eval 冻结（2026-08-13）

E6 以 `AOS项目开发上下文/50-2026-08-13-AIP-5-E6美妆知识包与混合检索评审清单.md` 为唯一执行清单。14-Wiki 系列中与下列规则冲突的历史段落只保留背景价值，不再授权实现：

1. 美妆知识必须作为可安装、可卸载、可回滚的 `VerticalPack` 交付，核心 AOS 不内置行业正文；组织/工作区实例可独立安装和定制。
2. bundle/source inventory/Receipt/Task/Run/source/license/freshness/hash 全部自洽后，可信 adapter 才能批量提交 Candidate；任何入口都不得直写 Semantic/Wiki。
3. 自然语言 `KnowledgeSearch` 是 E3 `KnowledgeQuery` 的增量能力，不替换精确 subject 解析；授权和治理过滤先于索引召回和 payload 解析。
4. 全文、向量、重排是独立 capability。当前环境无 pgvector 时必须返回 `degraded_vector_unavailable`，不能把全文命中称为混合检索 GREEN。
5. 353 条种子和 50 条金标均为目标门，不是已有数据。缺逐条授权 Receipt 或专家审核时分别保持 `DATA_BLOCKED` 与 `EVAL_BLOCKED`。
6. CosDNA 等来源在许可未知时保持 disabled；NMPA 等官方来源也必须登记当前版本、时效和使用政策，不能因“官方”绕过来源门。

E6 拆为 E6A 知识包契约、E6B Candidate 导入、E6C 全文 reference index、E6D 检索融合/Citation、E6E Eval runner、E6F 控制面与浏览器验收。只有各子门的代码、真实数据和 Eval 证据分别成立后，才允许宣告 E6 完成。

### 7.1 E6A 实施结论（2026-08-13）

E6A 已以代码 `f3415a9` 冻结 `VerticalPack` 专属 `knowledge` export、严格 KnowledgePackage/source inventory/entry/rollback DTO 和共享 JSON Schema。serialized loader 拒绝重复 JSON key；路径穿越、绝对/Windows/URL payload path、非 HTTPS 或带凭据/fragment 的 source URI、未知字段、hash 漂移、孤立 source、重复 entry/path 和无 Receipt rollback 全部失败关闭。非 VerticalPack 不得声明知识出口。

readiness 只返回稳定 `license_unknown/license_denied/source_stale` blocker，不修改 bundle authority。当前未创建美妆 bundle、未导入正文、未注册 adapter、未写租户数据。专项与 asset-registry 邻接回归 212 passed，compileall 与 diff check GREEN；venv 无 Ruff，不声明 Ruff。下一门为 E6B 可信 bundle seed adapter 与 Candidate 批量导入。

### 7.2 E6B 导入边界冻结

KnowledgePackage 只组织批量目录；每个 entry 必须有独立 subject、confidence、payload path/hash 和 source。E5 的 `KnowledgePipelineInputReceipt` 仍保持“一条 Receipt 对应一个精确 Artifact”，因此 E6B adapter 每次只把一个 entry Receipt 转换为一个确定性 Candidate Draft，批量由多个 Receipt 组成。禁止把整包 Artifact 复用为多条 Candidate payload，也禁止 adapter 直接写 Candidate、checkpoint 或正式 Wiki。

E6B 已以代码 `67cf0a8` 实现 `VerticalPackSeedAdapter`。adapter 只允许 `seed_import + authorized_document + aip.artifact_receipt`，每次把一个精确 entry Receipt 映射为一个确定性 Semantic Candidate Draft；entry id、payload hash、许可、usage policy、provider/version、observed/freshness 和 applicability 任一漂移均失败关闭。`PUBLIC_PACKAGE` 仍不允许由租户 adapter 直接发布，需另行 release authority。

E6A/E6B/Pipeline 专项 43 passed，compileall 与 diff check GREEN。包含更大邻接集合时 246 passed，另有 1 个既有签名时间 ISO 尾随零文本断言漂移（时间值相同），不属于本波逻辑。未注册生产 adapter、未创建真实租户 Candidate、未导入知识正文。下一门为 E6C tenant-scoped 全文 reference index 与 capability registry。

### 7.3 E6C reference index 与 capability registry 冻结

E6C 将 E3 的进程内 reference cache 升级为 PostgreSQL 可重建投影，但不替换 E3 的 canonical authority 查询。`aip_memory_search_reference` 仅保存同租户 Memory revision 的 id/revision/hash、subject/source reference、受限 search terms、markings/applicability/freshness；严禁 payload reference、正文、embedding 和 PII。`aip_memory_search_capability` 仅保存 fulltext/vector/rerank lane 的状态、原因、provider/revision、CAS version 和观测时间，不承担授权。

两表均启用并强制 RLS；无 scope 零可见。reference 清空/重建不修改 Source/Candidate/Memory；capability 更新必须 CAS。当前 PostgreSQL 只使用内建 `simple` 全文索引，不安装扩展；vector 明确为 `degraded_vector_unavailable`，rerank 未配置为 `unbuilt`。E6C 不返回知识正文，权限先行、融合、重排和 Citation 装配留在 E6D。

E6C 已以代码 `e581a99` 实现并复审通过。migration `aip5_004` 可逆升级且保持唯一 head；两张投影表 RLS/FORCE、同 scope FK、无 payload/正文/embedding 字段。Store 在写 reference 前逐项复核 canonical subject/hash/source/markings/applicability/freshness，terms 拒绝手机号、身份证、邮箱和 URL；vector 在数据库未安装 pgvector 时禁止写成 ready。6 项专项、32 项邻接、downgrade/upgrade、compileall、diff check GREEN；真实租户投影仍为空。下一门为 E6D `KnowledgeSearch` 与 Citation 装配。

### 7.4 E6D KnowledgeSearch 冻结

E6D 只增量新增自然语言 `KnowledgeSearch`，不改变 E3 精确 `KnowledgeQuery`。tenant RLS 与请求 marking 先约束 reference 候选；全文索引只给出 id/revision/hash/score，随后必须回查 canonical Item/Revision/Source 的 active、time window、freshness、markings、applicability、revision/hash，全部通过后才解析 payload。每条正文必须与 Citation 同序一一绑定。

响应按 fulltext/vector/rerank lane 明示状态和 reason；只有 ready lane 参与。所有 lane 不可用时 blocked 空结果；部分 lane 不可用时 degraded。当前真实租户 0 reference/0 capability，因此不得返回知识正文；vector/rerank 不得以假实现参与融合。E6D 首期排序仅采用 PostgreSQL fulltext rank + stable id tie-break，RRF 只有两个以上 ready lane 时才启用。

E6D 已以代码 `9bfec8c` 实现 `KnowledgeSearch` DTO、reference fulltext rank、lane 状态、canonical authority 二次过滤、payload 延迟解析、Citation 一一绑定和 `/knowledge-searches` 路由。2 项新 API、21 项核心邻接、compileall/diff check GREEN；默认 trusted resolver 未装配、真实租户 capability/reference 为空，所以只宣告 `CODE_GREEN / PROVIDER_BLOCKED / DATA_BLOCKED`。RRF 因只有零个 ready lane 未执行，不得宣告混合检索 GREEN。

### 7.5 E6E GoldSet 与 Eval runner 冻结

GoldSet 需要稳定 id/revision/hash、reviewer/approvedAt；每条至少包含自然语言、Skill、六角色依赖、精确 gold Memory/revision/hash/Citation 和负向期望。少于 50、未审核、六角色语义覆盖不全、重复 query/citation 或结果缺失时，runner 只能返回 `EVAL_BLOCKED` 且不计算指标。

Top-1 采用实际首条 Citation 的 Memory/revision/hash 精确匹配；另计 Citation coverage 和权限/stale/revoked/conflict 负向保护。任一负向泄露总门 RED。runner 是纯计算器，不生成 gold、不调用 LLM 补答案、不写 Memory/Index；当前真实金标计数仍为 0。

E6E 已以代码 `3d3ee69` 实现严格 GoldSet、Observation、Report 与纯计算 runner。正样本 Top-1/Citation coverage 和负样本泄漏分别计量，正确空返回的负样本不稀释正样本指标；全负样本也不得计算指标。未审核、少于 50、六角色覆盖缺口、重复或不完整结果均失败关闭。12 项专项、26 项 E6C-E6E 邻接、compileall、diff check GREEN；真实审核 GoldSet 仍为 0，故保持 `CODE_GREEN / EVAL_BLOCKED`。下一门为 E6F 控制面与 `org-org/dev-project` 内置浏览器验收。

### 7.6 E6F 只读控制面冻结

E6F 使用后端单一 `KnowledgeReadiness` 聚合，禁止前端跨 Source/Index/Installation/Eval 自行推断。Source/license/usage/freshness、reference 数和三 lane 来自当前租户 PostgreSQL 真值；未登记 lane 只可补成 `unbuilt/capability_not_registered`。当前尚无 KnowledgePackage installation identity 映射和 GoldSet registry，因此 package/Eval 两块返回 `authority_unavailable` 与空计数，不得显示猜测的 0。页面新增“冷启动与检索”视图，真实空态、provider 未装配、许可与 capability blocker 均可见；API 失败时失败关闭。浏览器正向验收只认 `org-org/dev-project`，`dev-org/dev-project` 仅作隔离 canary。

E6F 已以代码 `7e76886` 实现并通过复审。后端新增 tenant-scoped 只读 `KnowledgeReadiness` API；package/Eval 权威缺失保持空计数，Source/reference/capability 读取 PostgreSQL 真值，三 lane 缺失补为明确 `unbuilt`，存储失败映射 503。前端通过唯一严格 SDK 增加“冷启动与检索”视图，不从多接口自行推断。11 项后端邻接、14 项前端定向、TypeScript、Vite 274 modules、compileall、diff check 和内置浏览器 GREEN；`org-org/dev-project` 真实空态及全部阻断原因可见，`dev-org/dev-project` 独立 canary 无串租户。浏览器发现的嵌套 snake_case 契约漂移与 blocker 文本溢出均已修复。

因此 E6 当前结论为：**E6A～E6F CODE/CONTROL_IMPLEMENTED_GREEN；真实知识包、外部知识正文、可信检索 provider、向量能力和专家 GoldSet 仍分别 DATA/PROVIDER/EVAL_BLOCKED。** 这不是 operational hybrid search 或检索效果 GREEN；不得跳过外部门控宣告 E6 全量业务完成。
