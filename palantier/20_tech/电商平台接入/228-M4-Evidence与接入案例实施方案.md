# 228-M4 Evidence 与接入案例实施方案

> 状态：**v1.4 · M4-3 GREEN · 允许进入 M4-4 降级、统计与浏览器闭环**
> 起始代码基线：`aos-platform m1@36b386e`
> 当前代码基线：`aos-platform m1@b2dc69b`（五分支与五远端同 HEAD/tree）
> 上位约束：M1、M2、M3 已最终 GREEN；本方案只细化 M0 已定义的 Evidence/Case 架构
> 后续门禁：M4 最终 GREEN 后方可进入 M5；M5 完成前不得进入具体电商平台接入

## 0. 使用的 Rules

1. 先复核 M0、M1～M3 既有契约、真实 PostgreSQL 模式与接入案例页，再冻结 M4。
2. M4 只实现领域无关的 Evidence、Case、服务端阶段投影、统计和真实页面，不导入电商业务模型或平台 API。
3. 现有 Registry Evidence 与 Installation Event Evidence 只能作为可信来源引用，不改变其 DTO、hash、状态机或披露边界。
4. 阶段、截止时间、有效状态、统计和阻塞项全部由服务端计算；客户端不能提交或推断这些事实。
5. Evidence、Snapshot、Stage Event 和实例修订历史不可变；过期、撤销、负向证据必须能够使阶段降级。
6. 租户、角色、marking、幂等、CAS、错误投影和数据库完整性沿用 M1～M3 已验证模式，`admin` 不绕过。
7. 先专项测试，再真实 PostgreSQL、API/Web、浏览器和平台累计回归；全部 GREEN 才进入下一波。

## 1. 当前审计结论

`m1@36b386e` 已具备 Registry、Resolver、Composition Lock、Installation、事件证据与安装管理 UI，但尚无通用 Integration Case 的 Router、Service、Store、迁移和 SDK。`IntegrationCasesPage.tsx` 仍以静态常量展示“9 个平台”“7 个已上线”“1.2M 行/日”以及 `live=生产运行`，这些不能作为事实继续保留。

M0 已冻结 Case 创建、服务端阶段计算、快照、时间线和 8 级阶段。为真正满足不可变历史、过期降级、幂等和真实统计，本方案在 M0 三张摘要表基础上细化 Evidence 真源、生命周期事件、实例修订、当前投影和命令回执；这是实现级展开，不改变 M0 架构方向。

## 2. 范围与非目标

### 2.1 本阶段交付

- 当前工作区 Case 与脱敏参考 Case 的严格隔离。
- Case/Instance 与精确 Installation revision、Composition lock、Overlay revision 绑定。
- 可信内部 Producer 写入的不可变 Evidence 与 append-only lifecycle。
- 服务端 Snapshot、连续阶段门、过期/撤销/负向证据降级和 Stage Event。
- 租户及 marking 过滤后的列表、详情、时间线和真实统计。
- `/apollo/cases` 从静态原型切换到真实 SDK/API，覆盖加载、空、错误、陈旧和刷新状态。
- 真实 PostgreSQL、API、前端、浏览器及累计回归证据。

### 2.2 明确不做

- 不开放“客户端上传 valid Evidence”的公共 HTTP API。
- 不执行外部平台连接、Pipeline、Ontology、Logic、Workshop 或生产 Action。
- 不把旧静态平台卡片迁移为生产数据或 seed 真源。
- 不扩宽 `BundleEvidence`、`InstallationEventEvidence` 或修改其 hash basis。
- 不存 Secret、PII、Evidence 大文件正文、原始事故原因或内部 actor。
- 不创建 M5 电商 Bundle，不开始 Niushop、微信小店、抖音等具体平台接入。

## 3. 核心架构与事实流

```text
可信平台 Producer
        │ EvidenceWriter（内部协议）
        ▼
immutable Integration Evidence ── append-only Lifecycle
        │
        │ Case row lock + DB cutoff + strict gate policy
        ▼
immutable Evidence Snapshot ── Stage Event
        │
        ▼
current Case Projection ── 授权后统计聚合
        │
        ▼
Canonical API ── Web SDK ── /apollo/cases
```

Case 的 `planned` 事实来自精确 Installation revision 与 Composition lock；其余阶段只由有效 Evidence head 满足连续门后产生。读取发现 `nextProjectionAt` 到期时必须先重投影；失败时返回安全错误，不能继续显示旧的高阶段。

## 4. 冻结的数据模型

所有租户真源使用 `(org_id, project_id, internal_pk)` 复合键/外键；公共 ID 为服务端生成的 canonical lowercase UUID。历史表禁止 UPDATE、DELETE、TRUNCATE。

| 表 | 责任 | 核心约束 |
|---|---|---|
| `integration_case` | Case 身份与作用域 | `current` / `reference`；reference 是单独脱敏副本，不由 tenant 行原地转换 |
| `integration_instance` | 实例根、当前 revision/ETag | 绑定 Case；N+1 指针原子推进 |
| `integration_instance_revision` | 精确安装/Overlay 快照 | exact FK 到 Installation revision；正文 insert-only |
| `integration_evidence` | 逻辑 Evidence 的 append-only revision | type/subject/artifact 身份不变；纠错、负向、撤销均新增 revision |
| `integration_evidence_snapshot` | cutoff 时的完整 canonical Evidence envelopes | insert-only；稳定排序、唯一、canonical hash；服务端 stage |
| `integration_stage_event` | 阶段升降历史 | append-only；old 等于上一投影，new 等于 snapshot stage；阶段未变不写 |
| `integration_case_projection` | 当前阶段、有效期、阻塞和可聚合指标 | 仅与 snapshot/event 同事务推进；到期前有效 |
| `integration_case_command` | POST 幂等回执 | operation/key/request hash/subject/status/body/ETag 持久化 |

`integration_evidence` 保存受限的 typed claims、ref/hash/status/time/expiry/revocation/markings，不保存 Secret、PII 或任意自由正文。Snapshot 必须锁定 Evidence 的精确 revision 和完整 canonical envelope，不能只保存可变引用。

统计不另建第二事实表；从授权过滤后的 Projection 聚合。reference 永远不计入 current/production 统计。

### 4.1 迁移规则

- 新迁移：`228asset2_integration_cases.py`，`down_revision = 228assetinstall`，保持单 head。
- 顺序：表/复合键 → 索引 → canonical/stage 函数 → immutable/consistency trigger → 聚合 view。
- 新建域专属 canonical wrapper，复用但不改名或改变已有 canonical 函数。
- downgrade 仅在全部 M4 表为空时允许；不得删除 `pgcrypto` 或旧域函数。
- 必测 upgrade → API/Store 回读 → 有数据 downgrade 阻断 → 空库 downgrade → upgrade。

## 5. Evidence 严格契约

### 5.1 通用 envelope

每条 Evidence 包含：

- `evidenceId`、`revision`、`evidenceType`、`seriesKey`；
- `subjectRef`、`artifactRef`、`artifactHash`；
- `outcome`：`valid | invalid | revoked`；
- `observedAt`、`expiresAt`、`revokedAt`；
- `requiredMarkings`、`producer`、严格 typed `claims`；
- `evidenceHash`、`recordedAt`。

同一 `(producer, seriesKey)` 只取最新 revision；最新 invalid/revoked 不得回退旧 valid。有效性同时要求：

1. `observedAt <= cutoff`；
2. `outcome == valid`；
3. `expiresAt IS NULL OR cutoff < expiresAt`；
4. cutoff 前未撤销；
5. hash、Case/subject binding、Producer 和 marking 均有效。

`expiresAt == cutoff` 按 expired 处理。cutoff 只取数据库控制时钟，HTTP body 不接受时间。

### 5.2 Evidence type 与 typed claims

| 类型 | 必需 claims 摘要 | 支持阶段 |
|---|---|---|
| `source_connection` | connectionRef、authMode、readProbe、tenantBinding | connection |
| `tenant_isolation` | positiveTenant、negativeTenant、crossTenantDenied | connection/data |
| `pipeline_run` | pipelineRef、runId、result、input/output revision | data |
| `dataset_revision` | datasetRef、revision、schemaHash、rowCount（可空） | data/metrics |
| `data_quality` | datasetRef、checkSetHash、requiredPassed、failedChecks | data |
| `ontology_revision` | ontologyRef、revision、schemaHash | ontology |
| `mapping_validation` | mappingRef、coverage、linkValidationPassed；v1 要求 coverage=1.0 | ontology |
| `logic_publication` | logicRef、immutableRevision、publicationHash | logic |
| `logic_eval` | logicRef、evalSuiteHash、requiredPassed | logic |
| `workshop_validation` | workshopRef、realSource、empty/permission/mainFlowPassed | workshop |
| `action_safety` | actionRef、approval/rollback/idempotency controls | production_ready |
| `operations_readiness` | runbook/alert/owner refs、requiredChecksPassed | production_ready |
| `security_validation` | policySetHash、requiredChecksPassed | production_ready |
| `runtime_health` | deploymentRef、runId、healthy、latencyMs（可空） | production_active/metrics |

Registry/Installation 已有 evidence 类型可由可信 Producer 转换为上述 envelope 的来源引用，但不得直接改变原证据。每种 claims 使用独立 strict DTO；禁止以自由 metadata 决定阶段。

## 6. 阶段投影策略 v1

阶段固定为：

```text
planned
  → connection_verified
  → data_verified
  → ontology_verified
  → logic_verified
  → workshop_verified
  → production_ready
  → production_active
```

| stage | 必须连续满足的新增门 |
|---|---|
| `planned` | exact Instance revision、Installation active revision、Composition lock/hash 均完整有效 |
| `connection_verified` | `source_connection` + `tenant_isolation.crossTenantDenied=true` + 权限/marking 检查 |
| `data_verified` | 成功 `pipeline_run` + `dataset_revision` + `data_quality.requiredPassed=true` + tenant negative gate |
| `ontology_verified` | `ontology_revision` + `mapping_validation.linkValidationPassed=true` |
| `logic_verified` | immutable `logic_publication` + `logic_eval.requiredPassed=true` |
| `workshop_verified` | `workshop_validation` 的 realSource、empty、permission、mainFlow 全通过 |
| `production_ready` | action safety、operations readiness、security validation 全通过，安装 apply/verify 与 rollback 能力可引用 |
| `production_active` | 新鲜 `runtime_health.healthy=true`，无开放 blocker，且此前所有门仍有效 |

算法只返回最高连续通过阶段，允许一次升降多级。Evidence 新增、最新负向、撤销和过期均触发新 Snapshot；stage 变化时在同事务写唯一 Stage Event。`nextProjectionAt` 为当前参与门禁 Evidence 的最早到期时间。

PG trigger 至少复验 snapshot refs/hash、连续 stage 和 projection 尾；Python 使用同一 policy version 交叉验证。任何完整性损坏失败关闭为 `EVIDENCE_INTEGRITY_CORRUPT`。

## 7. Canonical API

只实现 M0 已声明的五个端点：

| Method | Path | operationId |
|---|---|---|
| GET | `/v1/integration-cases` | `list_integration_cases` |
| POST | `/v1/integration-cases` | `create_integration_case` |
| GET | `/v1/integration-cases/{case_id}` | `get_integration_case` |
| POST | `/v1/integration-cases/{case_id}/evidence-snapshots` | `create_integration_evidence_snapshot` |
| GET | `/v1/integration-cases/{case_id}/timeline` | `list_integration_case_timeline` |

### 7.1 写请求

`CreateIntegrationCaseRequest` 只允许：

```text
installationId
overlayRevision
displayName
```

org/project/owner/markings/scope 从验证 Principal 与绑定资源派生。禁止 body 注入 caseId、stage、evidence、cutoff、metrics、producer 或权限字段。

Snapshot POST body 严格为 `{}`。它只对服务端已有 canonical Evidence 生成快照；Evidence 写入/撤销通过内部 `EvidenceWriter` Protocol，由可信 Producer 调用。

- create：`Idempotency-Key`；
- snapshot：`Idempotency-Key + If-Match`；
- 两个 POST 成功均回复 `201 Created`，幂等 replay 保持原 status/body/ETag；
- detail/mutation 返回强 ETag；
- Snapshot 返回不可变历史响应，调用方随后 GET 当前 Case；
- 同 key 同 envelope replay 原结果；不同 body/If-Match 返回 409；同 ETag 并发只允许一个成功。

### 7.2 读取投影

- List item：case/scope/display/owner/installation/overlay/computedStage/snapshot revision/cutoff/blocker/ETag/time。
- Detail：增加 composition/lock、stage gates、脱敏 latest evidence、nextProjectionAt、统计可用性。
- Timeline：sequence/snapshot revision/old/new stage/stable cause/reason refs/time，分页返回。
- 不返回 raw claims/metadata、Secret、PII、内部 actor 或事故自由文本。

读取前按 org/project/scope/marking 过滤；list 的 total、分页和聚合在授权过滤后计算。detail 不可见统一 404，避免跨租户和 marking 侧信道。

## 8. 统计真实性

- current 与 reference 独立查询；reference 不进入 current 统计。
- Case/stage 数来自 live projection。
- connector/pipeline 按有效 Evidence 的唯一 `subjectRef` 去重。
- dataset rows 按 `(subjectRef, datasetRevision)` 去重，防止多 Case 重复累计。
- latency v1 固定取有效 runtime sample 的 `max`，不平均多个 p95。
- 每个指标返回 `value | null`、aggregation、measuredCaseCount、eligibleCaseCount、cutoffAt。
- 无有效测量为 `null`，前端显示 `—`；只有有效 Evidence 明确测得零才显示 `0`。
- expired/invalid/revoked 不计成功统计，但进入 blocker/latest failure。

## 9. 权限、并发与错误

- `HTTPBearer(auto_error=False)` + `require_principal`；Principal 只能来自已验证身份。
- current Case 创建需要 `integration-case-maker`，Snapshot 需要 `integration-case-projector`；reference 只读且不可执行当前租户操作。
- required markings 为 Case、Instance、参与 Evidence marking 的并集；`admin` 不绕过。
- 同 Case mutation 用 row lock/advisory lock 串行；Evidence/lifecycle 与 Snapshot 不产生半投影。
- expiry projector 可用 `FOR UPDATE SKIP LOCKED`，重复执行不重复 Stage Event。

复用既有错误：`VALIDATION`、`AUTH_REQUIRED`、`IDEMPOTENCY_KEY_REQUIRED`、`PRECONDITION_REQUIRED`、`PRECONDITION_INVALID`、`REVISION_CONFLICT`、`IDEMPOTENCY_CONFLICT`、`MARKING_ACCESS_DENIED`、`NOT_FOUND`。

M4 仅新增：

| HTTP | code | 场景 |
|---:|---|---|
| 422 | `EVIDENCE_REFERENCE_INVALID` | Producer、Case/subject binding 或 gate Evidence 不合法 |
| 500 | `EVIDENCE_INTEGRITY_CORRUPT` | 已持久化 Evidence/Snapshot/Timeline 完整性损坏 |

## 10. Web 映射

保留 `/apollo/cases` 路由，按现有仓库约定新增：

```text
apps/web/src/api/integrationCases/
  types.ts
  parsers.ts
  operations.ts
  client.ts
  *.test.ts

apps/web/src/pages/s2/integrationCases/
  model.ts
  readHooks.ts
  IntegrationCaseStats.tsx
  IntegrationCaseCatalog.tsx
  IntegrationCaseDetail.tsx
  EvidenceTimeline.tsx
  *.test.tsx
```

`IntegrationCasesPage.tsx` 变成只负责 scope、筛选、选择、刷新和组件组合的薄页面。删除运行路径中的 `STATS`、`PLATFORM_CASES`、静态 G1～G10 阻塞、全绿步骤和 `live=生产运行`。

读取状态至少覆盖 `idle/loading/ready/empty/forbidden/not_visible_or_missing/error/stale/refreshing`。详情与时间线独立维护状态；刷新失败可保留旧事实但必须显式标注 stale。切换 scope、tenant 或筛选时清除旧选择。

## 11. 开发分波与四 Worker 所有权

### M4-0：契约与 Policy 冻结

**实施结果（2026-08-03）：GREEN。**

- W1 冻结 14 类 strict typed claims、current/reference 判别 DTO、Snapshot 与 Timeline。
- W2 冻结 8 级最高连续 Policy、latest series head、expiry/revoke/negative 和 `null`/`0`。
- W3 冻结五端点 Web types/parser/fixture；W4 冻结 maker/projector、scope 与 marking 安全门。
- 总控完成后端/Web canonical 对拍、DTO→Policy 直接执行、结构化 blocker、UTC/统计/错误收口。
- 后端累计 131 passed；Web 全量 140 files / 1950 passed；TypeScript 与 production build GREEN。
- 五代码分支与五远端同步到 `c10d5ee`，ahead/behind `0/0`，五工作树 clean。
- 完整证据：[M4-0 契约与阶段策略冻结证据](../evidence/m0/m4-evidence-case/2026-08-03-M4-0契约与阶段策略冻结证据.md)。

- W1：`integration_contracts.py` 与 strict DTO/fixture。
- W2：`integration_stage_policy.py` 与连续门/expiry/revoke 算法。
- W3：Web DTO/parser/operation fixture。
- W4：M4 API、错误、角色、marking、OpenAPI 契约测试。

退出门：字段、claims、stage policy、五端点和错误矩阵全部通过；不改 DB，不改页面。**已满足。**

### M4-1：PostgreSQL 真源

- W1：唯一迁移 `228asset2_integration_cases.py` 与真实 PG migration 测试。
- W2：`integration_store.py`、canonical snapshot、receipt、并发/重启测试。
- W3：Web SDK client 与错误映射。
- W4：Store 对抗、跨租户/marking/corruption 测试；重启回读必须复验 current instance、最新 snapshot 和 projection 的 revision/ETag/stage/policy/cutoff/gates 镜像及 marking 绑定，命令回执写入失败必须连同 handler 产生的业务写入整体回滚。

迁移全项目只允许 W1 写；公共导出和错误表由总控单写。

**完成状态（2026-08-04）：GREEN。** W1 完成唯一 `228assetintegration` 迁移与 8 表数据库真源；W2 完成 Store、canonical snapshot、receipt、CAS、重启和并发保障；W3 完成五端点 Web SDK 与错误归一；W4 补齐重启时 current instance/latest snapshot/projection/marking 镜像复验与 handler/receipt 整体回滚。最终代码基线 `m1@14311e2`，五分支与五远端同 HEAD/tree、ahead/behind `0/0`、工作树 clean。详见 [M4-1 PostgreSQL 真源与 SDK 回归证据](../evidence/m0/m4-evidence-case/2026-08-04-M4-1PostgreSQL真源与SDK回归证据.md)。

### M4-2：Service、Projection 与 API

- W1：`integration_projection.py`、expiry projector 与算法交叉测试。
- W2：`integration_service.py`、内部 `EvidenceWriter` 与幂等/CAS。
- W3：`routers/integration_cases.py`、Protocol/wiring。
- W4：API E2E、双租户、role/marking、OpenAPI/header 契约。

共享 `domain_manifest.json`、聚合 Router、生成物与 operation 总数由总控收口。

M4-2 生产接线还必须由总控单写 PostgreSQL Reader 与 Marking Resolver：Reader 在 org/project/scope/marking 过滤后再计算 total、分页与统计，读取 current 列表前处理本租户已到期投影；由于 M2 Installation 尚无独立 marking 字段，v1 创建 Case 时保守地将已验证 Principal 的 marking 集合固化为 Case/Instance required markings，不允许 body 自报或降级。

**完成状态（2026-08-04）：GREEN。** W1 完成统一数据库 cutoff、租户限定和失败隔离的 expiry projector；W2 完成五用例 Service、receipt-first 幂等、Snapshot CAS 与仅供可信 Producer 使用的内部 `EvidenceWriter`；W3 完成五个 Canonical Router、严格 body/query/header、角色/marking 与统一错误映射；总控完成 PostgreSQL Reader、Marking Resolver、真实 JWT + 隔离 PostgreSQL HTTP 闭环、路由清单和 OpenAPI 确定性收口。公共 HTTP 未开放 Evidence 写入/撤销通道，current 读取在返回前处理本租户到期投影并失败关闭。最终代码基线 `m1@483dd0f`，五分支与五远端同 HEAD/tree、ahead/behind `0/0`、工作树 clean。详见 [M4-2 Service、Projection 与 Canonical API 回归证据](../evidence/m0/m4-evidence-case/2026-08-04-M4-2Service-Projection与Canonical-API回归证据.md)。

### M4-3：真实 Case 页面

- W1：Web read model/hooks 和竞态/刷新测试。
- W2：stats/catalog 组件。
- W3：detail/timeline 组件。
- W4：薄页面、scope/选择/错误态集成与静态伪事实清除。

**实施冻结（2026-08-04）：** M4-3 只消费 M4-1 已交付的 `apps/web/src/api/integrationCases/` 五端点 SDK 和 M4-2 已验证的真实响应，不修改后端 DTO、Policy、Store、Service、Router、数据库或 OpenAPI。页面运行路径必须移除 `STATS`、`PLATFORM_CASES` 及“7 已上线”“1.2M 行/日”“live=生产运行”等静态伪事实；测试夹具只能注入组件或 hook，不能作为失败回退数据。

M4-3 读取与交互契约：

- W1 在 `apps/web/src/pages/s2/integrationCases/` 建立单一 read model/hooks；列表、详情和时间线使用独立 request token/abort 或等价世代门，旧 scope/旧 Case 响应不得覆盖新选择。
- 列表状态覆盖 `idle/loading/ready/empty/forbidden/not_visible_or_missing/error/stale/refreshing`；详情和时间线独立失败，列表仍可用。手动刷新失败可保留最后一次服务端事实，但必须显示 stale，不能静默伪装为最新。
- scope 只允许 `current/reference`；切换 scope、tenant 或筛选必须清空旧选择、详情、时间线和陈旧错误。reference 不显示 current 专属 owner/Installation/Overlay/Lock，不显示 current stats。
- W2 的统计卡与目录卡只格式化服务端 `stats/items`；`null` 显示 `—`，明确 `0` 显示 `0`，不得在浏览器重算 eligible/production/connector/pipeline 等聚合。
- W3 的详情、8 门阶段和时间线只展示服务端 `computedStage`、`stageGates`、`blockers`、Evidence 元数据与 Stage Event；不得由图标、步骤序号、Evidence 数量或文档名称推断阶段。
- W4 保持 `IntegrationCasesPage.tsx` 为 scope、筛选、选择、刷新和组件组合的薄页面；本波默认只读，不增加创建 Case 或生成 Snapshot 的 UI mutation，避免在浏览器端引入幂等/CAS/未知结果的新状态面。
- 授权隐藏与不存在继续统一为非披露状态；403、完整性错误、网络错误必须诚实区分。任何错误态都不回退到静态平台数据。

M4-3 退出门：新增组件与 hook 专项测试、原 IntegrationCasesPage 测试、`integrationCases` SDK 累计测试、Web 全量、TypeScript 和 production build 全部 GREEN；运行路径搜索确认静态伪事实清零；浏览器证据留到 M4-4 完成真实后端场景闭环。

**完成状态（2026-08-04）：GREEN。** W1 完成单一 read model、九态读取、三路独立 generation gate、tenant/scope/filter 清选与 stale 保留；W2 完成仅格式化服务端统计和目录的 current/reference 组件；W3 完成详情、8 门、Blocker、受限 Evidence 与 Stage Event 时间线组件；总控将 `IntegrationCasesPage.tsx` 收薄为 scope、筛选、选择、刷新和组件组合，并监听租户切换。旧 `STATS`、`PLATFORM_CASES`、`BLOCKERS`、`E2E_STEPS` 以及平台名、1.2M、G1～G10 等静态伪事实已从运行路径清零。最终代码基线 `m1@b2dc69b`，五分支与五远端同 HEAD/tree、ahead/behind `0/0`、工作树 clean。详见 [M4-3 真实 Case 页面回归证据](../evidence/m0/m4-evidence-case/2026-08-04-M4-3真实Case页面回归证据.md)。

### M4-4：降级、统计与浏览器闭环

- 覆盖 Evidence 新增、最新负向、expiry、revoke、续期、重复 projector。
- 覆盖 reference 排除、marking 后聚合、`null` 与 `0`、去重和统一 cutoff。
- 浏览器验证空、错误、current/reference、详情、timeline、过期降级和刷新。

### M4-5：累计回归与证据收口

- 后端 M1～M4 专项与累计回归。
- Web/Desktop/Ontology SDK 测试、typecheck、production build。
- OpenAPI 确定性生成与唯一 operationId。
- 五分支同 HEAD/tree、ahead/behind 0/0、clean 并推远端。
- 更新总计划、228 路线、M0 状态与 AOS 开发上下文。

## 12. 验收矩阵

| 类别 | 必验场景 |
|---|---|
| Strict contract | extra/snake_case/coercion/非法 UUID/hash/naive time/body 注入全部失败且零写 |
| 租户与 marking | 双租户同 ID、跨租户统一 404、admin 不绕过、隐藏 Case 不进入 total/metrics |
| 阶段 | 缺前门不跳级、乱序确定性、最新 negative 覆盖旧 valid、过期边界、撤销降级 |
| 历史与完整性 | append-only、hash/sequence/stage 伪造被 PG 拒绝、PG/Python canonical 交叉一致 |
| 并发幂等 | 同 key replay、不同 envelope 冲突、同 ETag 仅一方成功、无半 snapshot/event/receipt |
| 统计 | reference 排除、重复 Dataset 去重、无测量 `null`、明确零 `0`、统一 cutoff |
| API | 5 路由、ETag/header/error、重启回读、OpenAPI 唯一且确定性 |
| Web | loading/empty/401/403/404/409/5xx/stale/refresh，详情与 timeline 独立错误 |
| 反伪事实 | “7 已上线”“1.2M”、`STATUS_META.live`、`PLATFORM_CASES` 不参与运行 |

## 13. 退出门与风险

M4 只有同时满足以下条件才 GREEN：

- body 伪造 stage/cutoff/metrics/evidence 无效；公共 HTTP 无 Evidence 自证通道。
- PostgreSQL 真源、不可变历史、hash、幂等、CAS 和双租户测试 GREEN。
- expiry/revoke/latest negative 会重投影、降级并只写一个 Stage Event。
- 统计、列表和详情均在授权过滤后计算；reference 永不污染 current。
- `/apollo/cases` 全面切真实 API，静态生产事实退出运行路径。
- 浏览器与累计回归 GREEN，五分支/远端同一最新基线。

主要风险及控制：

- **自由 claims 伪造阶段**：每类 Evidence 使用 strict typed claims，Stage Policy 只识别固定字段。
- **到期后假生产**：`nextProjectionAt` + projector；读取到期时同步重投影或失败关闭。
- **历史随引用变化**：Snapshot 保存 exact revision/full canonical envelope。
- **reference 泄漏**：只允许独立脱敏副本；不保留 tenant/source/owner 原值。
- **统计侧信道**：先授权过滤再 total/分页/聚合，不共享跨 Principal 缓存。
- **SQL/Python 漂移**：canonical 与 stage 使用代表性样本双实现交叉验证。

## 14. 当前裁决

M4 方案已冻结。允许从 `m1@36b386e` 开始 M4-0；不得提前修改数据库、页面或启动 M5。M4-0 的唯一目标是让后端 strict DTO、Stage Policy、Web fixture 和五端点安全契约形成同一可执行真源。
