# 228-AIP 三层运行记忆、行业 Wiki 与知识治理实施方案

> 状态：**IMPLEMENTING · v1.5 · 已获用户全量编码授权 · E0～E4 IMPLEMENTED_GREEN · E5 REVIEWED_APPROVED_TO_IMPLEMENT**
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

#### 6.4.3 状态机与恢复

- Schedule：`active <-> paused`，`active/paused -> disabled`；disabled 只能在依赖复核和 expected-version CAS 后恢复为 paused，不能直接 active。
- Run：`queued -> running -> succeeded/partial/failed/cancelled`；`running -> paused -> queued` 仅用于可恢复内部执行。terminal 状态不可重开，重试创建新 attempt/new run，并通过 `retry_of_run_id` 关联。
- worker 领取运行必须使用短租约；租约超时只能把结果标记 unknown/告警，不能假定未执行并重复写外部系统。
- 相同 idempotency key + request hash 精确回读；同 key 异 hash 返回 conflict。服务重启后从 PostgreSQL 回读 schedule/run/receipt/checkpoint，不依赖进程内字典。
- checkpoint 冲突、Candidate 漂移、来源许可/新鲜度 unknown、AIP Task/Run 不匹配全部 fail closed；不得静默跳过或跨租户回退。

#### 6.4.4 Canonical API 与页面边界

- `/v1/aip/memory-authority/pipelines/schedules`：列出/创建；`/{id}` 回读；`/{id}/transitions` 执行 CAS pause/resume/disable。
- `/v1/aip/memory-authority/pipelines/runs`：列出/创建人工或事件运行；`/{id}`、`/{id}/receipts`、`/{id}/alerts` 回读。首期 API 不直接执行外部抓取，只登记/驱动已注册 adapter。
- `/v1/aip/memory-authority/pipelines/runs/{id}/complete`：可信内部 executor 写 terminal Receipt、Candidate refs 和 checkpoint；普通前端用户不可调用。
- Memory Governance 页面增加“知识管道”只读/受控操作视图，覆盖 loading/empty/error/disabled/paused/active/running/failed/blocked；按钮必须有真实 API 或明确禁用原因。

#### 6.4.5 E5 子门与退出证据

| 子门 | 范围 | 退出门 |
|---|---|---|
| E5A | 契约、migration、RLS/FK/append-only | disposable PostgreSQL upgrade/downgrade；单 head；无 scope 零可见；既有行数守恒 |
| E5B | Store、幂等/CAS、checkpoint/Receipt/Alert | 重启回读、同 key 重放、异 hash conflict、失败不推进 checkpoint、跨租户不可见 |
| E5C | Service、七管道策略、adapter registry | 七 kind 独立开关；依赖未知 fail closed；Task/Run/Candidate 精确绑定；无真实外部抓取 |
| E5D | Canonical API、SDK/页面、累计回归与浏览器 | 角色矩阵、严格 DTO、真实状态/禁用原因、`org-org/dev-project` 浏览器验收、canary 负向证据 |

E5 不导入美妆知识，不启用网络/竞品/专业库真实抓取，不实现 E6 的全文/向量融合，也不实现 E7 的六同事共享投影。上述能力不得用 seed、Mock 或静态页面提前冒充完成。
