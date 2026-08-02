# 228-M2 Resolver、Lock 与 Installation 公共契约冻结方案

> 状态：**已补充冻结·等待 M1 最终累计回归门**
> 版本：v1.0 · 2026-08-03
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

### 3.1 ContributionClaim

```json
{
  "kind": "api",
  "key": "POST /v1/orders/{orderId}:retry",
  "mode": "exclusive"
}
```

| 字段 | 约束 |
|---|---|
| `kind` | `api`、`navigation`、`ui` |
| `key` | 1～512；已 trim、无 NUL、反斜杠、查询串或 fragment；必须是调用方预规范化后的稳定资源键 |
| `mode` | `exclusive` 或 `shared`；`api` 只允许 `exclusive` |

同一 manifest 内 `(kind,key)` 唯一。`api` key 固定为 `UPPER_METHOD + 空格 + normalized_path + 可选 ':' + operationId`；navigation key 固定为 normalized route；UI key 固定为 `slot/id`。同一 `(kind,key)` 被多个 resolved bundle 声明且任一为 `exclusive` 时返回 contribution collision；仅当全部为 `shared` 才允许共存。

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
- 服务端派生的 required/optional dependency、conflict、capability、permission、migration 和 contribution 索引。

候选只来自 `published` version，且 M1 `REQUIRED_RELEASE_EVIDENCE` 每种都必须非空、该类型的**每一条**证据均为当前 valid、`observedAt <= transaction_timestamp()`、未过期、未 revoked；content-hash evidence 每一条都必须等于 version contentHash；signature evidence 必须唯一。内部 signature envelope、evidence artifactRef/metadata、actor、reason、snapshot 不进入 DTO，不经 API 泄露。

### 4.5 RegistrySnapshot

hash payload 精确为：

```json
{
  "schemaVersion": "aos.dev/registry-snapshot/v1alpha1",
  "candidates": []
}
```

候选按 `(publisher,id,SemVer precedence,version,contentHash)` 稳定排序。`computedAt` 可作为存储元数据，但不进入 payload/hash。snapshot reader 必须单事务、单次候选集合读取，禁止 `list + N 次 get`。

---

## 5. Resolver 输出与解释契约

### 5.1 ResolvedBundle

`ResolvedBundle` 包含：

- `publisher/id/version/kind/contentHash/signatureFingerprint`；
- canonical required/optional dependency edges；
- conflicts、capabilities provides/requires；
- permissions、migration plan reference；
- signed contribution claims；
- `selectionReason`：`requested` 或 `dependency`。

### 5.2 ResolvedEdge 与 CapabilityProvider

- Edge：`fromPublisher/fromId/fromVersion → toPublisher/toId/toVersion`、constraint、`optional`；按完整 tuple 排序。
- Provider：`capability → publisher/id/version`；按 capability 排序。一个 required capability 必须恰有一个 selected provider；0 个或多个都冲突。

### 5.3 稳定 ConflictDetail

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

### 5.4 确定性算法

1. 先校验平台 API，再收集顶层 requested 约束。
2. 依赖 publisher 缺省时继承声明者 publisher；顶层 publisher 永远不得缺省。
3. required dependency 全部参与；optional dependency 仅当其 `(publisher,id)` 同时是顶层 requested 时参与约束。
4. 多个范围不计算字符串交集，而是对 snapshot 中稳定候选逐项同时 match。
5. 优先最高 stable 版本；prerelease 只有顶层/依赖约束显式包含 prerelease 时可选。
6. 候选相同 SemVer precedence 时按 `(version,publisher,id,contentHash)` 固定排序。
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
| approve | `lockHash/permissionDiffHash/migrationPlanHash` | Idempotency-Key + If-Match |
| reject | `reason` | Idempotency-Key + If-Match |
| apply | 空 strict object | Idempotency-Key + If-Match |
| verify | 空 strict object | Idempotency-Key + If-Match |
| rollback | `reason` | Idempotency-Key + If-Match |

所有成功 installation response 返回强 ETag。body 不提供 `expectedRevision`；若未来新增该字段，必须与 If-Match 一致，否则 400。create 时服务端按租户读取 lock 并固定 immutable installation revision 1；M2 不提供升级到 revision 2 的 API，但 schema 为后续 revision 留出空间。

### 7.2 状态机

| 操作 | from | to | 关键门禁 |
|---|---|---|---|
| create | 无 | `draft` | lock/diff/hash 完整，租户一致 |
| submit | `draft` | `submitted` | requester 与 revision requester 固定 |
| approve | `submitted` | `approved` | approver ≠ requester；三个 hash 精确匹配 |
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

每个 immutable revision 完整包含：`installationId/revision/parentRevision/state/compositionId/lockRevision/lockHash/permissionDiffHash/migrationPlanHash/contributionDiffHash/overlayRevision/requestedBy/createdAt`；approved revision 通过独立 approval DTO 关联 `decision/actor/approved hashes/reason/createdAt`，不得回写历史 revision。

`InstallationRecord` 包含：identity/displayName、由 current revision 派生的 state、`currentRevision/activeRevision/previousActiveRevision/etagVersion`、current immutable revision、可选 approval、按 sequence 排序的事件和 created/updated 时间。列表 API 只返回 identity/displayName/state/pointers/etag/times；详情和动作返回完整 record。所有动作响应中的 body `etagVersion` 必须与 HTTP `ETag` 一致；事件 evidence 只返回服务端生成的脱敏 ref/hash/status，不返回秘密或 Bundle 原始内容。

---

## 8. CAS 与持久化幂等

### 8.1 CAS

`bundle_installation.etag_version` 从 1 开始，每次成功 state/pointer 变化加 1。If-Match 缺失返回 `PRECONDITION_REQUIRED`，格式非法返回 `PRECONDITION_INVALID`，值不等返回 `REVISION_CONFLICT`。CAS 检查、state/pointer 更新、approval/evidence/event、ETag 增长和 idempotency receipt 必须在同一事务。

### 8.2 幂等

唯一键固定为 `(org_id, project_id, operation, idempotency_key)`。request hash 覆盖 canonical body、path identity、If-Match 和服务端固定的资源 revision，不覆盖 actor 时间戳。

- 同 key + 同 request hash：回放原 HTTP status、response body 和 ETag；
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
| `bundle_installation_approval` | tenant、installation/revision、decision、actor、三个 approved hash、reason/time | 每 revision 最多一个决定；insert-only；actor≠requester trigger |
| `bundle_installation_event` | tenant、installation、sequence、revision、from/to、actor、reason、evidence_json/hash、created_at | append-only；sequence 连续；事件尾与 installation state 同事务一致 |
| `bundle_installation_command` | tenant、operation、key、request_hash、HTTP status、response_json、etag、created_at | 复合 PK；insert-only；只允许 2xx receipt；JSON object |

### 9.2 关系与 trigger

- 所有 tenant-owned 表都保留 `org_id + project_id` 并使用包含 tenant 的复合 FK，禁止只靠 Service 过滤。
- FK 全部 `ON DELETE RESTRICT`；M2 不提供物理删除。
- lock/revision/approval/event/command 使用 UPDATE/DELETE/TRUNCATE 拒绝 trigger。
- installation identity/tenant 不允许任意直接修改；current/active/previous pointer 与 etag 只能通过受控 transition trigger，且 commit 时必须同时存在 N+1 immutable revision 和连续 event。
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
| 400 | `IDEMPOTENCY_KEY_REQUIRED` | M2 POST 缺少或非法幂等键 |
| 428 | `PRECONDITION_REQUIRED` | mutation 缺少 If-Match |
| 400 | `PRECONDITION_INVALID` | If-Match 不是冻结的强 ETag 格式 |

跨租户资源统一 `NOT_FOUND`，不得泄露资源存在性。旧批准 hash 重放使用 `APPROVAL_STALE`；自批使用 `DUTY_SEPARATION_REQUIRED`。

---

## 11. 分阶段文件所有权

### M2-A：Core（可并行）

- W1：新增 `composition_contracts.py`、`release_policy.py`、`registry_snapshot.py`、`dependency_graph.py`、`diff_service.py`、`resolver.py` 及纯算法/属性测试；只在总控窗口修改 `contracts.py/__init__.py`。M1 Service 与 snapshot reader 共用 release policy，禁止跨模块调用下划线私有函数。
- W2：新增 M2 migration、`composition_store.py`、`installation_store.py` 及 PostgreSQL/迁移/并发测试。
- W3：独立安全与契约测试，先不修改共享 router/main。
- 总控：冻结公共导出、审查 hash/DDL，集成后运行 M1+M2-A 专项和累计回归。

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
| 自批或旧批准重放 | P0 | immutable approval hashes + maker-checker + CAS |
| 幂等只在内存 | P0 | PostgreSQL receipt + advisory lock + unique constraint |
| route/nav/UI 假检测 | P0 | manifest signed contribution claims；索引缺失失败关闭 |
| M2 破坏 M1 | P1 | 新模块/新表为主，两阶段累计回归；不改旧 Apollo 真源 |

回滚优先通过 revert M2 router/service 开关保留新表；有 M2 数据时 schema downgrade 失败关闭，禁止为“回滚成功”静默删除 lock、approval、event 或 receipt。

---

## 14. 冻结结论

M2 只有在 M1 最新提交累计回归 GREEN、本文件已提交、四个 worker 分支对齐同一 m1 基线后才允许进入 M2-A 编码。M2-A 未通过专项与累计回归，不进入 M2-B；M2-B 未通过不进入 M3。
