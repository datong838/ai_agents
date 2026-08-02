# 228-M2 Resolver、Lock 与 Installation 公共契约冻结方案

> 状态：**M2-A0 GREEN·M2-A1 已授权编码**
> 版本：v1.3 · 2026-08-03
> 上位方案：[228-M0 资产包注册、解析、安装与证据化接入案例实施方案](228-M0-资产包注册解析安装与证据化接入案例实施方案.md)
> 范围：通用 AOS 平台内核，不包含任何具体电商平台业务逻辑、生产连接器或生产数据

---

## 0. 使用的 Rules

| Rule | M2 约束 |
|---|---|
| 先方案后编码 | 本文件冻结后才允许 M2 编码；范围变化必须先回写本文件 |
| 真源唯一 | Registry snapshot、composition lock、installation revision、approval、event 和 idempotency receipt 只以 PostgreSQL 为真源 |
| 确定性优先 | 同一请求、Registry snapshot、resolver 版本和安装基线必须生成完全相同的 lock payload/hash |
| 失败关闭 | 歧义、缺证据、资源超限、锁完整性、租户、CAS、幂等或职责分离失败都不产生半成品状态 |
| 最小执行面 | M2 apply/verify 仅做 dry apply；不执行 Bundle SQL/Python、外部调用或具体电商逻辑 |
| 分阶段回归 | M2-A Core 与 M2-B Control Plane 各自通过专项和累计回归后才能进入下一阶段 |

---

## 1. 评审结论与边界

M0 v1.6 已冻结 M2 原则，但不足以让多个 Worker 无歧义并行。本文件补齐 DTO、hash、资源上限、状态机、CAS、幂等、DDL、错误和测试边界；属于已批准 M0 范围的实现细化，不扩大产品范围。

M2 只交付：

1. 单事务 Registry snapshot reader；
2. 确定性依赖/能力/贡献冲突解析和 immutable composition lock；
3. installation create → submit → approve/reject → dry apply → verify → active → rollback 控制面；
4. 事务内 CAS、持久化幂等、职责分离和 append-only 审计；
5. Canonical API 与专项/累计回归。

M2 不交付：

- Bundle migration 或 Bundle 自带代码执行；
- 生产环境外部调用、生产凭证或具体平台安装；
- FDE 页面切换（M3）；
- Evidence/接入案例投影（M4）；
- 电商包与栖月汇脱敏实例组合（M5）。

---

## 2. 统一命名、格式与公共常量

| 项 | 冻结值 |
|---|---|
| `lockSchemaVersion` | `aos.dev/composition-lock/v1alpha1` |
| `snapshotSchemaVersion` | `aos.dev/registry-snapshot/v1alpha1` |
| `resolverVersion` | `aos-resolver/1.0.0`；算法变化必须升版本 |
| hash | `sha256:` + 64 位小写十六进制 |
| composition/installation id | UUID；API 中使用规范小写字符串 |
| publisher/bundle id | 沿用 M1 `BUNDLE_ID_PATTERN` |
| SemVer | 沿用 M1 strict version 与 npm-compatible range；拒绝 coercion |
| environment | `dev`、`staging`、`prod` |
| Idempotency-Key | 1～160 个已 trim、无 NUL 的可打印字符 |
| ETag | 强 ETag，精确格式 `"<etagVersion>"`，例如 `"3"` |
| 时间 | UTC aware `TIMESTAMPTZ`；时间戳不进入 snapshot/lock hash |

全部公共 DTO 继承 strict、`extra=forbid`、camelCase alias、`populate_by_name=False` 和 assignment validation。请求不得携带 `orgId/projectId/actor/roles/markings`；这些只来自已验证 Principal。

---

## 3. Manifest 的签名贡献索引

M1 的 `exports` 仅包含 bundle-local 路径，不能证明 API/navigation/UI 资源键。M2 在 `BundleSpec` 增加向后兼容、默认空数组的 `contributions`；它属于 manifest，因而被 M1 content hash 与 Ed25519 签名覆盖。

### 3.1 ContributionClaim 判别联合

```json
[
  {"kind":"api","method":"POST","path":"/v1/orders/{orderId}:retry","operationId":"retryOrder","mode":"exclusive"},
  {"kind":"navigation","route":"/orders/:orderId","mode":"exclusive"},
  {"kind":"ui","slot":"order.detail.actions","id":"retry-order","mode":"shared"}
]
```

| kind | 精确字段 | 冲突主键 |
|---|---|---|
| `api` | method、path、operationId、mode=`exclusive` | `(method, normalizedPath)`；`operationId` 另做全局唯一键，不能拼进 path 主键绕过冲突 |
| `navigation` | route、mode | `normalizedRoute` |
| `ui` | slot、id、mode | `(slot,id)` |

三个 claim 都是 strict discriminated union，禁止携带其他 kind 的字段。公共 `mode` 只能是 `exclusive/shared`；API 只接受 exclusive。slot/id/operationId 长度 1～160，已 trim、无 NUL；operationId 符合 `^[A-Za-z][A-Za-z0-9_]*$`，slot/id 符合小写 `BUNDLE_ID_PATTERN`。

API normalization：method 转大写后只能是 `GET/POST/PUT/PATCH/DELETE/OPTIONS/HEAD`；path 必须以 `/` 开头，拒绝反斜杠、percent encoding、query、fragment、重复斜杠、`.`/`..` 段和空模板；除根路径外移除尾斜杠；`{合法参数名}` 统一折叠为 `{}` 参与冲突主键，因此 `{id}` 与 `{orderId}` 必然冲突。静态段大小写保留并按 PostgreSQL `C`/Unicode codepoint 排序。

Navigation normalization：route 必须以 `/` 开头，拒绝反斜杠、percent encoding、query、fragment、重复斜杠和 `.`/`..` 段；除根路径外移除尾斜杠，静态段转小写；`:合法参数名` 统一折叠为 `:`。UI 不拼接自由文本 key，直接以已校验的 `(slot,id)` 比较。

同一 manifest 内各冲突主键唯一。主键被多个 resolved bundle 声明且任一为 exclusive 时返回 contribution collision；仅当全部为 shared 才允许共存。API route 主键或 operationId 任一重复都冲突。

若 `exports.backend` 非空却没有 `api` claim，或 `exports.ui` 非空却没有 `navigation/ui` claim，解析失败关闭为 `MANIFEST_INVALID`，不得伪称路由/导航/UI 冲突检测通过。

---

## 4. Composition 与 Registry Snapshot DTO

### 4.1 RequestedBundle

| 字段 | 类型与约束 | 进入 lock hash |
|---|---|---|
| `publisher` | 必填 publisher id | 是 |
| `id` | 必填 bundle id | 是 |
| `version` | 必填 SemVer exact 或 range，1～256 | 是 |

`requested` 按 `(publisher,id,version)` canonical 排序，`(publisher,id)` 不得重复。publisher 必填，禁止在 M1 允许同 id 多 publisher 的前提下猜默认 publisher。

### 4.2 CurrentInstallationRef

```json
{
  "installationId": "8b09391f-9c91-4fb6-b086-0799a50f012b",
  "revision": 3,
  "lockHash": "sha256:...",
  "overlayRevision": "sha256:..."
}
```

客户端只能把它作为乐观前置条件提交。服务端必须按 Principal 的 `org_id + project_id + installation_id` 回读当前 `activeRevision`，并逐字核对 revision、lockHash、overlayRevision；diff 基线只使用该 active revision。不存在或跨租户统一 404；四项任一变化返回 `CURRENT_INSTALLATION_STALE`。服务端回读后的不可变副本进入 lock hash，客户端对象本身不能直接进入。

### 4.3 CompositionRequest

| 字段 | 约束 | null 语义 |
|---|---|---|
| `requested` | 1～64 个 `RequestedBundle` | 不可空 |
| `platformApiVersion` | strict exact SemVer | 不可空 |
| `platformRelease` | 1～160 已规范化字符串 | 不可空 |
| `environment` | `dev/staging/prod` | 不可空 |
| `registrySnapshotHash` | 可选 SHA-256 前置条件 | null 表示接受本次服务端 snapshot |
| `currentInstallationRef` | 可选 | null 表示无安装基线，diff 相对空集 |

服务端先在单个 PostgreSQL `REPEATABLE READ READ ONLY` 事务中生成 snapshot。客户端提供的 snapshot hash 不等于本次值时返回 `REGISTRY_SNAPSHOT_STALE`，不创建 composition/lock。

### 4.4 RegistrySnapshotCandidate

每个 candidate 必须包含并排序：

- `publisher/id/version/kind`；
- 完整 strict `manifest`；
- `contentHash`；
- 当前唯一 `signature_verification.artifactHash` 作为 `signatureFingerprint`；
- 五类 release evidence 最小快照的 `releaseEvidenceRevision`；
- 服务端派生的 required/optional dependency、conflict、capability、permission、migration 和 contribution 索引。

候选只来自 `published` version，且 M1 `REQUIRED_RELEASE_EVIDENCE` 每种都必须非空、该类型的**每一条**证据均为当前 valid、`observedAt <= transaction_timestamp()`、未过期、未 revoked；content-hash evidence 每一条都必须等于 version contentHash；signature evidence 必须唯一。内部 signature envelope、evidence artifactRef/metadata、actor、reason、snapshot 不进入 DTO，不经 API 泄露。

`releaseEvidenceRevision = canonical_sha256(sortedEvidence)`；每个最小 evidence 只含 `type/artifactHash/status/observedAt/expiresAt/revokedAt`，按 `(type,artifactHash,observedAt,expiresAt null-first)` 排序。它进入 RegistrySnapshotCandidate、ResolvedBundle 和 lock hash。submit/approve/apply/verify 重算后必须与 lock 完全一致；合法证据刷新也要求重新 resolve/approve，不能静默沿用旧安全证据集合。

### 4.5 RegistrySnapshot

hash payload 精确为：

```json
{
  "schemaVersion": "aos.dev/registry-snapshot/v1alpha1",
  "candidates": []
}
```

对外/内部 DTO 精确为 `schemaVersion/candidates/snapshotHash/checkedAt`；`snapshotHash` 和 `checkedAt` 不进入上面的 hash payload，checkedAt 固定取同一 PostgreSQL 事务的 `transaction_timestamp()`。候选按 publisher/id 升序、SemVer precedence 升序，再按 version/contentHash 升序稳定排序。snapshot reader 必须单事务、单次候选集合读取，禁止 `list + N 次 get`。

---

## 5. Resolver 输出与解释契约

### 5.1 ResolvedBundle

`ResolvedBundle` 精确包含：

- `publisher/id/version/kind/contentHash/signatureFingerprint/releaseEvidenceRevision`；
- `dependencies/optionalDependencies`：`publisher/id/version` 约束 DTO，publisher 已服务端补全；
- `conflicts`：`publisher/id/version|null`，publisher 已服务端补全；
- `capabilities`：`provides/requires` 两个排序唯一字符串数组；
- `permissions`：完整目标 PermissionSet；
- `migration`：`planRef|null/downgradePolicy`；
- `contributions`：规范化后的判别联合数组；
- `selectionReason`：`requested` 或 `dependency`。

### 5.2 ResolvedEdge 与 CapabilityProvider

- Edge：`fromPublisher/fromId/fromVersion → toPublisher/toId/toVersion`、constraint、`optional`；按完整 tuple 排序。
- Provider：`capability → publisher/id/version`；按 capability 排序。一个 required capability 必须恰有一个 selected provider；0 个或多个都冲突。

### 5.3 稳定 ConflictDetail

`ConstraintPathNode` 精确字段为 `publisher/id/version|null/via`，via 是 `requested/dependency/optional`；`ConstraintRecord` 为 `sourcePublisher/sourceId/sourceVersion|null/targetPublisher/targetId/requirement/optional`；`CandidateRejection` 为 `publisher/id/version/reason`，reason 只能是 `platform_api/version_constraint/prerelease/conflict/resource_limit`；`ConflictResource` 为 `kind/key/owners`，owner 是 `publisher/id/version`。

`DEPENDENCY_CONFLICT.details` 固定为：

```json
{
  "subtype": "version_intersection_empty",
  "path": [],
  "constraints": [],
  "candidateRejections": [],
  "resource": null
}
```

`subtype` 只能是：`missing_dependency`、`version_intersection_empty`、`explicit_conflict`、`capability_missing`、`capability_multiple`、`contribution_collision`。path 从顶层 requested 到冲突节点；cycle 另用 `DEPENDENCY_CYCLE`，cycle 旋转到字典序最小节点并固定方向。所有 constraints/rejections/resource provider 列表 canonical 排序，禁止自由文本代替结构化 details。

`DEPENDENCY_CYCLE.details` 精确为 `{"cycle":[ConstraintPathNode...]}`；数组不重复首节点并保持真实有向依赖方向，只旋转到字典序最小 tuple 起点，不得反转成不存在的边。

### 5.4 确定性算法

1. 先校验平台 API，再收集顶层 requested 约束。
2. 依赖 publisher 缺省时继承声明者 publisher；顶层 publisher 永远不得缺省。
3. required dependency 全部参与；optional dependency 仅当其 `(publisher,id)` 同时是顶层 requested 时参与约束。
4. 多个范围不计算字符串交集，而是对 snapshot 中稳定候选逐项同时 match。
5. 优先最高 stable 版本；prerelease 只有顶层/依赖约束显式包含 prerelease 时可选。
6. 候选相同 SemVer precedence 时按 `(version,publisher,id,contentHash)` 升序排序并选第一项；conflict 的 publisher 缺省也与 dependency 一样继承声明者 publisher。
7. 采用全图 deterministic DFS/backtracking；输入、数据库行或 dict 顺序不得影响结果。
8. 选定后统一检查 cycle、explicit conflict、capability 与 contribution collision。

### 5.5 确定性资源预算

| 资源 | 上限 |
|---|---:|
| 顶层 requested | 64 |
| snapshot candidates | 4096 |
| resolved nodes | 512 |
| dependency edges | 4096 |
| dependency depth | 64 |
| backtracking states | 10000 |
| contribution claims | 10000 |
| canonical lock payload | 4 MiB |

任一超限返回 `RESOLUTION_LIMIT_EXCEEDED` 并在 details 中给出 `resource/limit/observed`。生产请求另设 2 秒 wall-clock 保护，但决定性 step budget 是主要边界；超时只允许失败，不允许返回可能因机器速度不同而变化的部分 lock。每一上限都做 max-1/max/max+1 测试。

### 5.6 三类 Diff 精确 DTO

`PermissionSet` 精确为 `roles/markings/dataScopes/actionTypes` 四个排序唯一字符串数组。`PermissionDiff` 精确为 `baseline/target/added/removed/unchanged` 五个 PermissionSet；added/removed/unchanged 分别做逐集合差集/交集。无 current installation 时 baseline 四项全为空数组。职责分离中的 marking 门检查 `target.markings` 全集，不只检查 added。

`MigrationStep` 精确为 `publisher/id/version/planRef/downgradePolicy`，只收录 planRef 非 null 的 resolved bundle，按 `(publisher,id,version,planRef)` 排序。`MigrationChange` 精确为 `publisher/id/before/after`。`MigrationPlanDiff` 精确为 `baseline/target/added/removed/changed`：前四项为 MigrationStep 数组，changed 只包含同 bundle coordinate 但 step 不同的 before/after；无 current installation 时 baseline/removed/changed 为空。

`ContributionBinding` 精确为 `publisher/id/version/claim`，claim 为 §3 的规范化判别联合。`ContributionDiff` 精确为 `baseline/target/added/removed/unchanged` 五个 ContributionBinding 数组，按 `(claim.kind, conflictKey, publisher,id,version)` 排序。resolver 已在生成 diff 前拒绝 collision，因此 lock 内不保存“可能有冲突”的结果。

target 一律从本次 resolved bundles 聚合；baseline 一律从服务端验证后的 current active installation 所绑定的旧 lock payload 重建，禁止改用当前 Registry 中同版本的可变查询结果。Permission target 是所有 resolved permissions 的集合并集；migration/contribution 保留 owner coordinate，不能因文本相同丢失归属。

三个 diff 对象都以 strict DTO 的完整 canonical JSON 分别计算 `permissionDiffHash/migrationPlanHash/contributionDiffHash`；正文和 hash 同时落库并在 Store/Service/DB 三层重算。禁止只 hash added、只保存摘要或把空对象 `{}` 当成未定义算法。

---

## 6. Composition Lock 精确 hash payload

`CompositionLockPayload` 精确字段为：

```json
{
  "lockSchemaVersion": "aos.dev/composition-lock/v1alpha1",
  "resolverVersion": "aos-resolver/1.0.0",
  "request": {},
  "registrySnapshotHash": "sha256:...",
  "resolved": [],
  "edges": [],
  "capabilityProviders": [],
  "permissionDiff": {},
  "migrationPlan": {},
  "contributionDiff": {},
  "currentInstallationRef": null
}
```

规则：

- `request` 删除客户端的 `registrySnapshotHash/currentInstallationRef` 后，写入服务端规范化 request；两项使用 payload 顶层服务端值。
- `permissionDiff/migrationPlan/contributionDiff` 必须保存完整正文；各正文另计算 hash 并存储，但这些派生 hash 不重复进入 lock payload。
- `compositionId`、lock revision、actor、createdAt、computedAt、ETag 和 `lockHash` 自身不进入 hash。
- 空集合使用 `[]/{}`，语义可空字段使用 JSON `null`；禁止省略与 null 混用。
- `lockHash = canonical_sha256(CompositionLockPayload)`；Store/Service 每次回读都复验正文、三个 diff hash 和 lock hash。

`StoredCompositionLock` 在 payload 外增加 `compositionId/revision/lockHash/permissionDiffHash/migrationPlanHash/contributionDiffHash/createdAt`。相同 request hash + snapshot hash + resolverVersion + current ref hash 必须去重并回放同一 lock，不创建等价重复 revision。

---

## 7. Installation DTO 与状态机

### 7.1 创建和动作请求

| API | body | 额外头 |
|---|---|---|
| resolve | `CompositionRequest` | 必填 Idempotency-Key |
| create installation | `compositionId/lockRevision/overlayRevision/displayName` | 必填 Idempotency-Key |
| submit | 空 strict object | Idempotency-Key + If-Match |
| approve | `lockHash/permissionDiffHash/migrationPlanHash/contributionDiffHash` | Idempotency-Key + If-Match |
| reject | `reason` | Idempotency-Key + If-Match |
| apply | 空 strict object | Idempotency-Key + If-Match |
| verify | 空 strict object | Idempotency-Key + If-Match |
| rollback | `reason` | Idempotency-Key + If-Match |

所有成功 installation response 返回强 ETag。body 不提供 `expectedRevision`；若未来新增该字段，必须与 If-Match 一致，否则 400。create 时服务端按租户读取 lock 并固定 immutable installation revision 1；后续动作以 N+1 revision 记录状态，但 M2 不提供替换 composition lock/overlay 的安装计划升级 API。

### 7.2 状态机

| 操作 | from | to | 关键门禁 |
|---|---|---|---|
| create | 无 | `draft` | lock/diff/hash 完整，租户一致 |
| submit | `draft` | `submitted` | requester 与 revision requester 固定 |
| approve | `submitted` | `approved` | approver ≠ requester；四个 hash 精确匹配 |
| reject | `submitted` | `rejected` | reviewer ≠ requester；reason 非空 |
| apply | `approved` | `applied` | 只生成 dry-apply evidence，不执行 Bundle |
| verify | `applied` | `active` | lock/Registry refs/evidence 复验；原 active 保存为 previous |
| rollback | `active` | `rolled_back` | active 恢复为 previous；previous 可为 null，表示回到未安装基线 |

M2 不定义 `upgrading/deactivating/blocked/failed`；非法边统一 `INSTALLATION_STATE_CONFLICT`。rejected、rolled_back 为本 revision 终态。动作失败不得改变 state、pointer、ETag 或成功事件。

状态历史采用**全量 immutable revision**：create 插入 revision 1，此后每个成功动作插入 revision N+1，完整复制固定的 composition lock/overlay/requester 并写入新的 state；历史 revision 永不 UPDATE。`bundle_installation.current_revision` 只原子指向最新 revision，`active_revision/previous_active_revision` 指向对应 immutable revision。event 记录 `fromRevision/toRevision`，因此 revision insert-only 与状态机不再冲突。

submit、approve、apply、verify 在同一事务内按 lock 中精确 `publisher/id/version/contentHash/signatureFingerprint` 重新验证所选版本仍为 published、M1 五类 release evidence 仍全部 current，且当前 trust root 仍接受签名。旧 lock 可以保留作审计，但不能穿越 bundle revoke、evidence expiry 或 trust-root revoke 进入 active。

### 7.3 职责分离与角色

- create/submit：`admin/developer/asset-installer`；
- approve/reject：`admin/asset-install-approver`，且 actor 必须不同于 requester；
- apply/verify/rollback：`admin/asset-installer`；
- 普通 `admin` 仍受 maker-checker，不因角色绕过主体分离；
- Principal `markings` 必须覆盖 lock permission diff 中全部目标 marking；`admin` 不绕过 marking；
- 所有角色只取 Principal，不信任 body。

### 7.4 InstallationRevision 与响应

每个 immutable revision 完整包含：`installationId/revision/parentRevision/state/compositionId/lockRevision/lockHash/permissionDiffHash/migrationPlanHash/contributionDiffHash/overlayRevision/requestedBy/decisionId|null/createdAt`。approve/reject 创建 immutable `decisionId`；approved revision 写入该 id，apply/verify/active/rolled_back 后继 revision 必须原样继承，禁止替换或清空。rejected revision 关联 rejected decision；draft/submitted 必须为 null。

`InstallationDecision` 精确为 `decisionId/installationId/submittedRevision/decision/actor/lockHash/permissionDiffHash/migrationPlanHash/contributionDiffHash/reason|null/createdAt`，decision 只能 `approved/rejected`。apply/verify 通过 current revision 的 decisionId 读取同一批准对象，逐字核对四个 hash、decision=approved、actor≠requestedBy；不通过“当前 revision 恰好没有 approval”或仅按 lock hash 猜批准对象。

`InstallationRecord` 包含：identity/displayName、由 current revision 派生的 state、`currentRevision/activeRevision/previousActiveRevision/etagVersion`、current immutable revision、由 decisionId 精确关联的可选 decision、按 sequence 排序的事件和 created/updated 时间。列表 API 只返回 identity/displayName/state/pointers/etag/times；详情和动作返回完整 record。所有动作响应中的 body `etagVersion` 必须与 HTTP `ETag` 一致；事件 evidence 只返回服务端生成的脱敏 ref/hash/status，不返回秘密或 Bundle 原始内容。

### 7.5 API 字段、列表和状态码

- `CreateInstallationRequest`：compositionId UUID、lockRevision integer≥1、overlayRevision 1～160 规范化字符串、displayName 1～240 规范化字符串。
- `ApproveRequest`：四个 SHA-256 hash；`RejectRequest/RollbackRequest`：reason 1～2000 规范化字符串；submit/apply/verify body 必须是严格空对象 `{}`。
- `InstallationEvent`：`sequence/fromRevision|null/toRevision/fromState|null/toState/actor/reason|null/evidence|null/createdAt`；evidence 精确为 `type/evidenceRef/evidenceHash/status/observedAt`，type 为 `dry_apply/verification/rollback`，status 为 `valid/invalid`。
- list query：可选 state filter，`limit` 默认 50、范围 1～100，`offset` 默认 0、范围 0～10000；稳定排序 `createdAt DESC, installationId ASC`；响应 envelope 为 `items/total/limit/offset`。
- resolve 与 create installation 首次成功返回 201；submit/approve/reject/apply/verify/rollback 返回 200；所有 GET 返回 200；幂等回放返回原始状态码而不是改成 200。

---

## 8. CAS 与持久化幂等

### 8.1 CAS

`bundle_installation.etag_version` 从 1 开始，每次成功 state/pointer 变化加 1。If-Match 缺失返回 `PRECONDITION_REQUIRED`，格式非法返回 `PRECONDITION_INVALID`，值不等返回 `REVISION_CONFLICT`。CAS 检查、state/pointer 更新、approval/evidence/event、ETag 增长和 idempotency receipt 必须在同一事务。

### 8.2 幂等

唯一键固定为 `(org_id, project_id, operation, idempotency_key)`。事务取得 advisory lock 后**先查 receipt，再读取任何当前 Registry/installation 状态**。request hash 只覆盖 canonical client command envelope：`subject/pathParams/body/ifMatch`；subject 是已验证 Principal subject，body 包含客户端实际提交的 snapshot/current-ref 前置条件。不得把本次服务端读取的 snapshot、current resource revision/ETag、角色、markings 或时间放入 request hash。

- 已有 receipt 时先用原 command envelope 重算 hash；同 key + 同 request hash 直接回放原 HTTP status、response body 和 ETag，不再次 resolve、重验当前 ETag 或读取变化后的 Registry；
- 同 key + 不同 request hash：`IDEMPOTENCY_CONFLICT`；
- 不同租户或 operation 可安全复用相同 key；
- M2 不设 TTL，不允许 key 过期后表达另一请求；
- 使用 tenant/operation/key advisory transaction lock 串行首请求，并由唯一约束兜底；
- 只持久化与业务事务共同提交的 2xx 结果；认证、校验、CAS、domain failure 或进程崩溃均不留下成功 receipt。

---

## 9. PostgreSQL 真源与硬约束

### 9.1 表

| 表 | 关键列 | 硬约束 |
|---|---|---|
| `bundle_composition` | tenant、composition_id、request_json/hash、snapshot_json/hash、current_ref_json/hash、resolver_version、actor/time | tenant+id 唯一；JSON object；hash 格式；等价输入唯一去重 |
| `bundle_composition_lock` | tenant、composition_pk、revision、payload/hash、三个 diff 正文/hash、created_at | tenant-safe FK；revision≥1；JSON object；insert-only；lock hash 唯一于 composition |
| `bundle_installation` | tenant、installation_id/pk、display_name、current_revision、active_revision、previous_active_revision、etag_version、actor/time | tenant+id 唯一；etag≥1；identity/tenant immutable；业务 state 从 current immutable revision 读取 |
| `bundle_installation_revision` | tenant、installation_pk/revision、parent_revision、state、composition_pk/lock_revision/hash、overlay_revision、requested_by/time | 每个成功动作插入 N+1；复合 PK/FK；insert-only；parent=N-1；lock 三 hash 由 trigger 核对 |
| `bundle_installation_decision` | tenant、decision_id、installation/submitted_revision、decision、actor、四个 approved hash、reason/time | 每 submitted revision 最多一个决定；insert-only；actor≠requester trigger |
| `bundle_installation_event` | tenant、installation、sequence、from/to revision/state、actor、reason、evidence_json/hash、created_at | append-only；sequence 连续；事件尾与 installation current revision 同事务一致 |
| `bundle_installation_command` | tenant、operation、key、request_hash、HTTP status、response_json、etag、created_at | 复合 PK；insert-only；只允许 2xx receipt；JSON object |

### 9.2 精确列、主键和 null

所有 `org_id/project_id/actor/operation/key/display_name/overlay_revision/resolver_version` 为 TEXT，并做非空白、无 NUL 与本文件长度 CHECK；所有 hash 为 TEXT + SHA256_PATTERN CHECK；所有时间为 `TIMESTAMPTZ NOT NULL DEFAULT NOW()`；所有 JSONB 同时做 object/array CHECK。

1. `bundle_composition`
   - `org_id, project_id, composition_pk UUID, composition_id UUID, request_json JSONB(object), request_hash, registry_snapshot_json JSONB(object), registry_snapshot_hash, current_installation_ref_json JSONB(object) NULL, current_installation_ref_hash NULL, resolver_version, created_by, created_at`。
   - PK `(org_id,project_id,composition_pk)`；UNIQUE `(org_id,project_id,composition_id)`；等价去重 unique index 为 `(org_id,project_id,request_hash,registry_snapshot_hash,resolver_version,COALESCE(current_installation_ref_hash,''))`。
2. `bundle_composition_lock`
   - `org_id, project_id, composition_pk, revision BIGINT, lock_payload JSONB(object), lock_hash, permission_diff_json JSONB(object), permission_diff_hash, migration_plan_json JSONB(object), migration_plan_hash, contribution_diff_json JSONB(object), contribution_diff_hash, created_by, created_at`。
   - PK `(org_id,project_id,composition_pk,revision)`；revision≥1；复合 FK 到 composition；UNIQUE `(org_id,project_id,composition_pk,lock_hash)`。
3. `bundle_installation`
   - `org_id, project_id, installation_pk UUID, installation_id UUID, display_name, current_revision BIGINT, active_revision BIGINT NULL, previous_active_revision BIGINT NULL, etag_version BIGINT, created_by, created_at, updated_at`。
   - PK `(org_id,project_id,installation_pk)`；UNIQUE `(org_id,project_id,installation_id)`；current_revision/etag≥1；三个 pointer 使用 `DEFERRABLE INITIALLY DEFERRED` 复合 FK 到本 installation revision。
4. `bundle_installation_revision`
   - `org_id, project_id, installation_pk, revision BIGINT, parent_revision BIGINT NULL, state, composition_pk, lock_revision BIGINT, lock_hash, permission_diff_hash, migration_plan_hash, contribution_diff_hash, overlay_revision, requested_by, decision_id UUID NULL, created_at`。
   - PK `(org_id,project_id,installation_pk,revision)`；revision≥1；revision=1 时 parent NULL，否则 parent=revision-1；state CHECK `draft/submitted/approved/rejected/applied/active/rolled_back`；复合 FK 到 installation、parent revision、composition lock 和可选 decision。
5. `bundle_installation_decision`
   - `org_id, project_id, decision_id UUID, installation_pk, submitted_revision BIGINT, decision, actor, lock_hash, permission_diff_hash, migration_plan_hash, contribution_diff_hash, reason TEXT NULL, created_at`。
   - PK `(org_id,project_id,decision_id)`；UNIQUE `(org_id,project_id,installation_pk,submitted_revision)`；decision CHECK `approved/rejected`；approved reason 可 null，rejected reason 必填；FK 到 submitted immutable revision。revision→decision FK 为 deferred，以便 decision 与 N+1 revision 同事务插入。
6. `bundle_installation_event`
   - `org_id, project_id, installation_pk, sequence BIGINT, from_revision BIGINT NULL, to_revision BIGINT, from_state TEXT NULL, to_state TEXT, actor, reason TEXT NULL, evidence_json JSONB(object) NULL, evidence_hash TEXT NULL, created_at`。
   - PK `(org_id,project_id,installation_pk,sequence)`；sequence≥1；evidence_json/hash 必须同 null 或同非 null；复合 FK 到 from/to revision；to_state 必须等于 to revision state。
7. `bundle_installation_command`
   - `org_id, project_id, operation, idempotency_key, subject, request_hash, status_code SMALLINT, response_json JSONB(object), response_etag TEXT NULL, created_at`。
   - PK `(org_id,project_id,operation,idempotency_key)`；status_code 200～299；response ETag 必须为 null 或冻结的强 ETag 格式；M2 无 expires_at/TTL。

### 9.3 关系与 trigger

- 所有 tenant-owned 表都保留 `org_id + project_id` 并使用包含 tenant 的复合 FK，禁止只靠 Service 过滤。
- FK 全部 `ON DELETE RESTRICT`；M2 不提供物理删除。
- lock/revision/decision/event/command 使用 UPDATE/DELETE/TRUNCATE 拒绝 trigger。
- installation identity/tenant 不允许任意直接修改；current/active/previous pointer 与 etag 只能通过受控 transition trigger，且 commit 时必须同时存在 N+1 immutable revision 和连续 event。
- decision trigger 要求 submitted source 的 requester 与 decision actor 不同、四个 hash 等于固定 lock；approved 及其所有后继 revision 必须继承同一 approved decisionId，rejected 只能引用 rejected decision。
- lock insert trigger 重新计算 canonical lock、permission、migration、contribution hash；直接 SQL 伪造正文/hash 必须失败关闭。
- event evidence 正文与 hash 在数据库层强绑定，采用 M1 已冻结的 canonical JSONB + pgcrypto profile。
- 非空 lock、installation 或 command 数据存在时，M2 downgrade 失败关闭；空库允许 downgrade。

---

## 10. Canonical API 与错误

沿用 M0 §9.2 API。新增稳定错误：

| HTTP | code | 场景 |
|---:|---|---|
| 409 | `REGISTRY_SNAPSHOT_STALE` | 客户端 snapshot 前置条件已变化 |
| 409 | `CURRENT_INSTALLATION_STALE` | current installation 四元组已变化 |
| 422 | `RESOLUTION_LIMIT_EXCEEDED` | 任一决定性解析预算超限 |
| 409 | `INSTALLATION_STATE_CONFLICT` | 非法状态边或 terminal revision 重放 |
| 409 | `LOCK_INTEGRITY_INVALID` | lock/diff 正文与 hash 不一致 |
| 500 | `LOCK_INTEGRITY_CORRUPT` | 服务端回读已持久化 lock/diff 发现损坏；响应不得带原始内容 |
| 400 | `IDEMPOTENCY_KEY_REQUIRED` | M2 POST 缺少或非法幂等键 |
| 428 | `PRECONDITION_REQUIRED` | mutation 缺少 If-Match |
| 400 | `PRECONDITION_INVALID` | If-Match 不是冻结的强 ETag 格式 |

跨租户资源统一 `NOT_FOUND`，不得泄露资源存在性。旧批准 hash 重放使用 `APPROVAL_STALE`；自批使用 `DUTY_SEPARATION_REQUIRED`。

`LOCK_INTEGRITY_INVALID` 只用于客户端引用/hash 与 canonical lock 不一致；数据库已持久化内容自身无法通过重算时必须使用 `LOCK_INTEGRITY_CORRUPT` 并告警。M2 的 rollback 从 active 恢复 previous（previous 可 null）原则上总是允许；`ROLLBACK_BLOCKED` 保留给后续存在下游引用或法律保留门的阶段，M2 不凭空返回该错误。

---

## 11. 分阶段文件所有权

### M2-A：Core（可并行）

- M2-A0 已完成：W1 冻结 composition DTO/contribution claims，W2 落地 migration/数据库不变量，W3 冻结请求 Schema/稳定错误，总控冻结五个公共导出并完成累计回归。
- M2-A1 按 [228-M2-A1 核心解析与持久化并行实施方案](228-M2-A1核心解析与持久化并行实施方案.md) 执行：W1 负责 release policy/snapshot，W2 负责 composition/installation store，W3 负责 dependency graph/diff/resolver，W4 负责独立对抗与跨模块集成测试。
- M1 Service 与 snapshot reader 共用 release policy，禁止跨模块调用下划线私有函数。
- 总控独占共享导出和既有契约文件，审查 hash/DDL，集成后运行 M1+M2-A 专项和累计回归。

### M2-B：Control Plane（M2-A GREEN 后）

- W1：`composition_service.py`；
- W2：`installation_service.py`；
- W3：`routers/bundle_compositions.py`、`routers/bundle_installations.py`、API/OpenAPI 测试；
- 总控：修改 `aos_api/routers/domain_manifest.json` 并重新生成 `domain_aggregates.py`，不得直接手改生成文件或 `main.py`；同时负责错误映射、集成/安全/浏览器前置契约。

任何 Worker 不提前修改别人的共享文件；跨模块接口以本文件 DTO/Protocol 为准。

---

## 12. 退出门

### M2-A

- 同 id 不同 publisher、exact/range、pre-release、optional 显式启用、缺依赖、菱形、cycle、冲突、capability 和 contribution 全通过。
- 至少 100 组输入/候选 permutation 不改变 snapshot/lock hash。
- 每项资源预算 max-1/max/max+1。
- snapshot 读取期间并发 revoke/expire 不产生跨事务混合快照。
- lock 正文/三个 diff/hash 回读复验；直接 SQL 篡改全部失败。
- migration empty upgrade/downgrade/upgrade、非空 downgrade blocker 通过。
- M1 Registry 专项与后端累计回归通过。

### M2-B

- 所有合法/非法状态边通过；rejected/rolled_back 终态成立。
- 双线程 CAS 只有一个成功；失败请求无半写 pointer/event/receipt。
- 同 key 同请求并发只有一份数据且回放完全一致；同 key 不同请求冲突；双租户隔离。
- 自批、stale approval/current ref/snapshot、跨租户、旧 If-Match 全部失败关闭。
- apply/verify/rollback 不执行 Bundle 代码或外部调用；active → rollback 原子恢复 previous active（可为 null）。
- OpenAPI 两次生成 byte-identical、无重复 operationId。
- M1+M2 全专项、后端全量、Web/Desktop test/typecheck/build 全绿，并形成阶段证据文档。

---

## 13. 风险与回滚

| 风险 | 等级 | 控制 |
|---|---:|---|
| 解析器指数爆炸 | P0 | 决定性 step budget + 节点/边/深度上限 |
| 同 id 多 publisher 歧义 | P0 | 顶层 publisher 必填；依赖缺省只继承声明者 |
| lock 看似不可变但 hash 可伪造 | P0 | Store/Service/DB 三层重算，insert-only trigger |
| 自批或旧批准重放 | P0 | immutable decision hashes + maker-checker + CAS |
| 幂等只在内存 | P0 | PostgreSQL receipt + advisory lock + unique constraint |
| route/nav/UI 假检测 | P0 | manifest signed contribution claims；索引缺失失败关闭 |
| M2 破坏 M1 | P1 | 新模块/新表为主，两阶段累计回归；不改旧 Apollo 真源 |

回滚优先通过 revert M2 router/service 开关保留新表；有 M2 数据时 schema downgrade 失败关闭，禁止为“回滚成功”静默删除 lock、decision、event 或 receipt。

---

## 14. 冻结结论

M2-A0 已在 `m1@cc78e01` 完成公共契约、数据库底座与最终累计回归，证据见 [M2-A0 公共契约与数据库底座回归证据](../evidence/m0/m2-control/2026-08-03-M2-A0公共契约与数据库底座回归证据.md)。M2-A1 编码门现已打开；M2-A1 未通过专项与累计回归，不进入 M2-B，M2-B 未通过不进入 M3。
