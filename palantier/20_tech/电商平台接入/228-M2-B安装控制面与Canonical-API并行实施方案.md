# 228-M2-B 安装控制面与 Canonical API 并行实施方案

> 状态：**v1.2 最终冻结，授权进入 M2-B0 共享底座**
> 日期：2026-08-03
> 上位方案：[228-M2 Resolver、Lock 与 Installation 公共契约冻结方案](228-M2-Resolver-Lock-Installation公共契约冻结方案.md)
> 代码基线：`aos-platform m1@a6e4d31`
> 分支基线：m1、W1、W2、W3、W4 均对齐 `a6e4d31`

---

## 0. 使用的 Rules

1. 先方案后编码；本文件冻结前不新增 M2-B 生产逻辑。
2. 只实现通用资产包 Composition/Installation 控制面，不实现具体电商平台 Connector、真实 Bundle 执行、migration apply 或 M3 页面。
3. 以 PostgreSQL、immutable lock/revision/decision/event 和持久化 receipt 为唯一真源；内存状态不得成为正确性前提。
4. 最小改动、失败关闭、租户隔离、强 CAS、持久化幂等和 maker-checker 优先；失败不得留下半条 revision/event/pointer/receipt。
5. 四个 Worker 按文件独占并行；共享错误、策略、路由聚合、CORS 和生成契约由总控独占。
6. 每小波先专项测试，再真实 PostgreSQL 并发/故障注入，再 M1+M2 累计回归；M2-B 全绿前不进入 M3。
7. 不修改用户已有 `AppShell.tsx` 和掘金文档改动；提交只包含本阶段明确文件。

---

## 1. 审计结论

M2-A 已提供可复用的严格 DTO、确定性 Resolver、Registry snapshot/release policy、composition/installation PostgreSQL 表、immutable/hash trigger、Store 读原语、CAS 行锁和 receipt-first 幂等。M2-B 不新增状态和表，也不改变 M2-A hash payload。

编码前审计同时发现以下真实缺口，本方案一次封口：

1. `CompositionStore.create_or_get()` 自行提交，无法与 command receipt 同事务；必须增加 caller-owned transaction 原语。
2. `InstallationStore` 只有 draft、get/list、receipt 和 CAS，没有 typed transition 写原语。
3. resolve baseline 必须从 active immutable revision 重建，不能信任客户端 current ref，也不能取 current revision 代替 active。
4. submit/approve/apply/verify 必须在同一 transition 事务中重验 exact selected releases；不能逐项另开事务或用全量 snapshot 排除结果代替精确失败。
5. 现有通用 marking helper 对 admin 放行，不符合 M2 “admin 不绕过 marking”。
6. marking 不足、Registry 持久化损坏、三类 server evidence 正文此前未精确定义。
7. FastAPI 必填 Header 会先走通用 validation，破坏 `IDEMPOTENCY_KEY_REQUIRED/PRECONDITION_REQUIRED`；必须显式解析单值 raw header。
8. 列表若分页后再隐藏 marking 不可见项，会泄露 total；必须在数据库分页/计数前过滤。
9. CORS 未暴露 `ETag`；浏览器虽可用 body `etagVersion`，但无法验证响应头契约。

结论：**M2-B 可开发，但必须按 B0→B1→B2→B3 四小波推进，不能直接先开 Router。**

交叉评审记录：v1.0 首轮由 W1/W2/W3 分别审查事务/baseline、状态机/revalidation/evidence、HTTP/OpenAPI/CORS；v1.1 关闭全部 P0/P1 后又进行两轮定点复核。最终三方均确认残余 P0/P1 为零，才形成 v1.2 冻结版。

---

## 2. 范围与非目标

### 2.1 本阶段交付

- Composition resolve/get lock Service 与 Canonical API；
- Installation create/list/detail、submit/approve/reject/apply/verify/rollback；
- immutable revision、decision、event、active/previous pointer 编排；
- receipt-first 幂等、强 ETag/If-Match、maker-checker、role/marking；
- exact selected release revalidation；
- dry-apply/verification/rollback server evidence；
- OpenAPI、router aggregate、CORS ETag 前置契约；
- 专项、真实 PostgreSQL 对抗、累计回归和证据文档。

### 2.2 明确不做

- 不执行 Bundle SQL/Python/HTTP、Connector 或任意外部调用；
- 不执行 migration plan，不写领域业务表；
- 不新增安装升级/替换 composition API，不新增 failed/blocked/upgrading 状态；
- 不做 M3 管理页面，不修改通用 Web API client 返回形状；
- 不手改 `domain_aggregates.py`、generated OpenAPI/inventory 或旧 `v1.yaml`；
- 不新增物理删除和 receipt TTL。

---

## 3. 冻结的权限与可见性

### 3.1 角色

| 操作 | 允许角色 |
|---|---|
| resolve composition | `admin/developer/asset-installer` |
| create/submit installation | `admin/developer/asset-installer` |
| approve/reject | `admin/asset-install-approver` |
| apply/verify/rollback | `admin/asset-installer` |
| GET lock、list/detail installation | `admin/developer/asset-installer/asset-install-approver` |

- 角色只从 verified Principal 获取；body/query/path 中注入 tenant、actor、roles、markings 一律拒绝。
- 角色不符沿用 M0 冻结的 `DUTY_SEPARATION_REQUIRED` 403。
- approve/reject 的 actor 必须不同于 immutable `requestedBy`；admin 也不得自批。

### 3.2 marking

- resolve 的结果、create、所有动作和详情读取都检查 `permissionDiff.target.markings` 全集，不只检查 added。
- `admin` 不绕过；不得复用带 admin bypass 的通用 `ensure_markings()`。
- mutation/resolve marking 不足返回新增稳定错误 `MARKING_ACCESS_DENIED` 403；details 不回显缺失 marking 名称。
- GET lock/detail marking 不足按隐藏资源策略返回 `NOT_FOUND` 404。
- list 必须在 SQL 计数、排序、limit/offset 前过滤不可见项，响应 total 不包含不可见安装。
- 角色在 command Store 前检查；receipt 命中后不读变化后的 Registry、current installation 或 ETag，但必须先校验 receipt body/ETag DTO，再从 receipt body 或其指向的 immutable composition lock 重验当前 Principal target markings。权限撤销返回 `MARKING_ACCESS_DENIED`，不创建新 receipt，也不得借 replay 读取旧响应。
- replay 中 receipt body/ETag 无法通过 DTO、引用的 immutable lock 不存在/损坏、receipt 与 lock 引用不一致，统一 `LOCK_INTEGRITY_CORRUPT` 500；不能降级成 404。resolve 可直接从 receipt 的 `StoredCompositionLock` 检查 marking；installation replay 只允许按 receipt body 的 `compositionId/lockRevision` 读取 immutable lock，禁止读取 current pointer/Registry。

### 3.3 baseline 环境

有 `currentInstallationRef` 时，新请求 `environment` 必须等于 active baseline lock 的 `request.environment`；不允许跨 dev/staging/prod 计算增量。环境不一致返回 `CURRENT_INSTALLATION_STALE` 409，且不回显服务端环境或 hash。

### 3.4 list 可见性 Store 契约

`InstallationStore.list_visible_installations(*, org_id, project_id, query, allowed_markings: Collection[str]) -> InstallationListResponse` 在一个 repeatable-read/read-only PostgreSQL 事务中完成：

1. tenant-safe join current revision → composition lock；
2. 先检查 current lock 的 permission diff JSON 结构和 `canonical_bundle_control_sha256(permission_diff_json) == permission_diff_hash`，任一损坏使整个请求 `LOCK_INTEGRITY_CORRUPT` 500，不能静默隐藏；
3. target markings 空集可见；否则仅 `target.markings ⊆ allowed_markings` 可见；admin 不增加隐式 marking；
4. 在同一可信快照内先过滤，再计算 total、稳定排序和 limit/offset；不得先分页后删项。

---

## 4. Composition Service 精确契约

### 4.1 API

```text
POST /v1/bundle-compositions:resolve
GET  /v1/bundle-compositions/{composition_id}/locks/{revision}
```

`CompositionService` 提供：

```python
resolve(
    *, request: CompositionRequest,
    org_id: str, project_id: str,
    actor: str, roles: Collection[str], markings: Collection[str],
    idempotency_key: str | None,
) -> CommandReceipt

get_lock(
    *, org_id: str, project_id: str,
    composition_id: str, revision: int,
    roles: Collection[str], markings: Collection[str],
) -> StoredCompositionLock
```

- resolve operation 固定为 `bundle_compositions.resolve`。
- 首次成功与 replay 均为 201，body 为完整 `StoredCompositionLock`，无 ETag。
- GET 为 200，无 Idempotency-Key、If-Match 和 ETag。
- command hash envelope 精确为 `subject/pathParams={}/body/ifMatch=null`；body 使用 camelCase canonical `CompositionRequest`，两个可选前置字段显式保留 null。
- roles、markings、server snapshot、当前时间和服务端读取状态不得进入 request hash。
- Router 负责缺失/重复/raw header 形状并保证失败时 Service 零调用；Service 仍以 `str | None` 防御性校验缺失和内容，统一映射 `IDEMPOTENCY_KEY_REQUIRED`。
- 构造签名固定为 `CompositionService(*, snapshot_reader, composition_store, command_store, baseline_reader, resolver=resolve)`；command_store 与 baseline_reader 可由同一个 `PostgresInstallationStore` 实现，但在 Protocol 上分离。

### 4.2 active baseline 共享 Protocol

B0 在 `control_protocols.py` 冻结以下跨 Worker 接口，W1 只依赖 Protocol，W2 提供 PostgreSQL 实现：

```python
class IdempotentCommandHandler(Protocol):
    def __call__(self, conn: Any) -> CommandResult: ...

class IdempotentCommandStore(Protocol):
    def execute_idempotent(
        self, *, org_id: str, project_id: str, operation: str,
        idempotency_key: str, subject: str, request_hash: str,
        handler: IdempotentCommandHandler,
    ) -> CommandReceipt: ...

class CompositionControl(Protocol):
    def resolve(
        self, *, request: CompositionRequest,
        org_id: str, project_id: str, actor: str,
        roles: Collection[str], markings: Collection[str],
        idempotency_key: str | None,
    ) -> CommandReceipt: ...
    def get_lock(
        self, *, org_id: str, project_id: str,
        composition_id: str, revision: int,
        roles: Collection[str], markings: Collection[str],
    ) -> StoredCompositionLock: ...

@dataclass(frozen=True, slots=True)
class ActiveInstallationBaseline:
    server_ref: CurrentInstallationRef
    lock: StoredCompositionLock

class ActiveBaselineReader(Protocol):
    def load_active_baseline_in_transaction(
        self,
        conn: Any,
        *,
        org_id: str,
        project_id: str,
        requested_ref: CurrentInstallationRef,
    ) -> ActiveInstallationBaseline: ...
```

- Protocol 文件用 postponed annotations/`TYPE_CHECKING` 引用既有 `CommandResult/CommandReceipt`，避免 `installation_store ↔ control_protocols` 运行时循环；不搬迁既有 dataclass。
- `execute_idempotent` 的 handler 拥有调用方同一 connection/transaction；只有 handler 返回成功 CommandResult 后才插 receipt，Store 负责 advisory lock、receipt-first 和共同 commit。
- 实现对 installation identity 行取 `FOR SHARE` 并持有到 receipt 提交；按客户端 installationId 定位后，从 active immutable revision 重建 `server_ref` 并逐字段与 requested_ref 比较。
- 不存在/跨租户为 404；active null 或 revision/lockHash/overlayRevision 不符为 409 stale；revision 四 hash、composition lock 或 diff 损坏为 500 corrupt。
- `server_ref` 只能来自数据库；`lock` 必须通过完整性入口加载，W1 用 `lock.payload` 做 baseline diff 和 environment 门。

### 4.3 resolve 首请求顺序

1. Principal、strict DTO、角色和 Idempotency-Key 做无数据库校验；
2. `execute_idempotent` 取得 tenant/operation/key advisory transaction lock；
3. **先查 receipt**；同 hash 命中进入 immutable authorization 后原样回放，异 hash 返回 409；
4. receipt miss 时，若 current ref 非 null，锁定同租户 installation 行并从 `active_revision` 加载 baseline；
5. 资源存在后，服务端重建的 revision/lockHash/overlayRevision 与 client ref 任一不符或 active pointer 为空，返回 `CURRENT_INSTALLATION_STALE`；不存在/跨租户返回 `NOT_FOUND`；
6. 通过 composition Store 完整性入口读取 active historical lock，核对 installation revision 的四 hash，并从数据库值重建 effective current ref；
7. 校验 baseline environment；baseline 为 null 时完全不查 installation，三类 diff 相对空集；
8. 读取一次冻结 Registry snapshot，校验可选 `registrySnapshotHash`；
9. 用 effective request、同一 snapshot、baseline payload 调用纯 Resolver；
10. 检查 target markings；
11. 通过 `create_or_get_in_transaction(conn, ...)` 写 composition/lock；
12. 生成 201 CommandResult，写 receipt，与业务写同一事务提交。

任何异常回滚 composition、lock 和 receipt。不得先调用会自行 commit 的现有 `create_or_get()`。等价输入使用不同 key 可去重到同一 lock，但每个 command receipt 独立且仍返回 201。

### 4.4 baseline 精确语义

- baseline 只取 `active_revision`，不取 `current_revision`。M2-B 公共线性状态机首次 verify 前旧 active 必为 null，因而公共 API 不会产生 non-null previous；数据库为未来升级保留 non-null pointer 能力，受控 migration/Store fixture 可验证该前向兼容语义。若此类合法历史数据存在，rolled_back 后 active 指向的历史 revision 可继续作 baseline。
- active immutable revision 的 composition/lockRevision/lockHash/overlayRevision 必须与客户端四元组逐字一致。
- baseline payload 来自已验证历史 lock，不从当前 Registry 重建旧版本。
- 外层 installation 行至少 `FOR SHARE` 持有到 receipt 提交，防止并发 transition 改变 active pointer。
- 已持久化 baseline lock/diff/hash 损坏统一 `LOCK_INTEGRITY_CORRUPT` 500，响应不带正文、SQL 或 hash 差异。

---

## 5. Installation Service 精确契约

`control_protocols.py` 同时冻结 Router 与 W2 共用的 `InstallationControl` 调用面：

```python
create(*, request: CreateInstallationRequest,
       org_id: str, project_id: str, actor: str,
       roles: Collection[str], markings: Collection[str],
       idempotency_key: str | None) -> CommandReceipt
list(*, query: InstallationListQuery,
     org_id: str, project_id: str,
     roles: Collection[str], markings: Collection[str]) -> InstallationListResponse
get(*, installation_id: str,
    org_id: str, project_id: str,
    roles: Collection[str], markings: Collection[str]) -> InstallationResponse
submit(*, installation_id: str, request: EmptyInstallationActionRequest,
       org_id: str, project_id: str, actor: str,
       roles: Collection[str], markings: Collection[str],
       idempotency_key: str | None, if_match: str | None) -> CommandReceipt
approve(*, installation_id: str, request: ApproveInstallationRequest,
        org_id: str, project_id: str, actor: str,
        roles: Collection[str], markings: Collection[str],
        idempotency_key: str | None, if_match: str | None) -> CommandReceipt
reject(*, installation_id: str, request: RejectInstallationRequest,
       org_id: str, project_id: str, actor: str,
       roles: Collection[str], markings: Collection[str],
       idempotency_key: str | None, if_match: str | None) -> CommandReceipt
apply(*, installation_id: str, request: EmptyInstallationActionRequest,
      org_id: str, project_id: str, actor: str,
      roles: Collection[str], markings: Collection[str],
      idempotency_key: str | None, if_match: str | None) -> CommandReceipt
verify(*, installation_id: str, request: EmptyInstallationActionRequest,
       org_id: str, project_id: str, actor: str,
       roles: Collection[str], markings: Collection[str],
       idempotency_key: str | None, if_match: str | None) -> CommandReceipt
rollback(*, installation_id: str, request: RollbackInstallationRequest,
         org_id: str, project_id: str, actor: str,
         roles: Collection[str], markings: Collection[str],
         idempotency_key: str | None, if_match: str | None) -> CommandReceipt
```

全部参数为 keyword-only，不允许 positional 或额外自由参数。Service 校验 header 内容；Router 负责 raw header 的缺失/重复前置。operation 常量精确为：

```text
bundle_compositions.resolve
bundle_installations.create
bundle_installations.submit
bundle_installations.approve
bundle_installations.reject
bundle_installations.apply
bundle_installations.verify
bundle_installations.rollback
```

resolve/create command 的 `pathParams={}`；六个 action 的 command pathParams 精确为 `{"installationId":"<canonical-lowercase-uuid>"}`。GET/list 不产生 command receipt。

构造签名固定为 `InstallationService(*, store, composition_store, revalidator)`；`revalidator.revalidate_in_transaction(conn, *, lock) -> RevalidationResult(checked_at)` 返回锁后读取的统一时钟，Service 以该 checked_at 生成 evidence。create/reject/rollback 不调用 revalidator；rollback 在 CAS/marking 后通过 Store `read_control_clock_in_transaction(conn) -> datetime` 单独读取一次 `clock_timestamp()`，create/reject 无 evidence，可使用 Store 既有事务时间。

### 5.1 状态与 pointer

| 操作 | from→to | decision | evidence | pointer |
|---|---|---|---|---|
| create | 无→draft r1 | null | null | active/previous=null |
| submit | draft→submitted | null | null | 不变 |
| approve | submitted→approved | 新 approved decision | null | 不变 |
| reject | submitted→rejected | 新 rejected decision | null | 不变，终态 |
| apply | approved→applied | 继承 approved id | dry_apply/valid | 不变 |
| verify | applied→active | 继承 approved id | verification/valid | previous=旧 active；active=N+1 |
| rollback | active→rolled_back | 继承 approved id | rollback/valid | active=旧 previous；previous 保持该值，可 null |

- 每次成功动作只插 N+1 immutable revision 和 sequence=N+1 event，再受控更新 current/pointers/etag。
- `etag_version == current_revision`，create 为 1，每次成功动作 +1。
- rejected/rolled_back 终态；任何非法边统一 `INSTALLATION_STATE_CONFLICT`，零写入。
- rollback 不因 Registry revoke/evidence expiry 阻断，M2 不返回 `ROLLBACK_BLOCKED`。

### 5.2 事务 Store 原语

新增内部 `LockedInstallation`，至少包含 tenant、installation_pk、完整 current record；保留既有 `lock_for_cas()` 兼容读原语，新增 `lock_for_transition_in_transaction(...) -> LockedInstallation`。Store 不开放自由 `targetState/pointers/decisionType/evidenceType`，只开放六个窄方法：

```python
append_submit_in_transaction(conn, *, locked, actor) -> InstallationRecord
append_approval_in_transaction(conn, *, locked, actor, request) -> InstallationRecord
append_rejection_in_transaction(conn, *, locked, actor, reason) -> InstallationRecord
append_apply_in_transaction(conn, *, locked, actor, evidence) -> InstallationRecord
append_verify_in_transaction(conn, *, locked, actor, evidence) -> InstallationRecord
append_rollback_in_transaction(conn, *, locked, actor, reason, evidence) -> InstallationRecord
```

每个窄方法从 locked current 唯一派生 toState、decision、evidence type、reason 规则和 pointer：

1. 可选 decision；
2. N+1 revision，完整复制固定 plan/overlay/requester/decision lineage；
3. N+1 event 与可选 evidence；
4. current/active/previous/etag/updated_at；
5. `SET CONSTRAINTS ALL IMMEDIATE`；
6. 完整 record 回读。

Service 不拼 transition SQL。Store 必须拒绝 submit/approve/reject 携带 evidence、apply/verify/rollback 的 evidence type 错配、approve/reject decision 错配、空/多余 reason 和任何非法边。所有 mutation 都在 `execute_idempotent` handler 的同一连接内完成。`SET CONSTRAINTS ALL IMMEDIATE` 可沿用，但该 handler 事务只能写本 installation/composition command 相关表，不混入其他领域写。

### 5.3 mutation 精确顺序

1. Principal、DTO、operation role、Idempotency-Key、If-Match 语法；
2. canonical request hash；
3. tenant/operation/key advisory lock；
4. receipt-first；命中后先把 body 校验为 `InstallationResponse`、核对 `response_etag == f'"{body.etagVersion}"'`，再按 body current revision 指向的 immutable lock 做 marking authorization，最后原 status/body/ETag 回放；不得读取 current installation/Registry；
5. 首请求 `FOR UPDATE` installation + CAS + current state；
6. load/verify stored lock、decision lineage、target markings；
7. submit/approve/apply/verify 做 exact release revalidation；reject/rollback 不做；
8. approve 校验 body 四 hash等于当前 immutable plan，并创建唯一 decision；apply/verify 逐字复验继承的 approved decision；
9. 生成 server evidence（如适用）；
10. typed transition 写 revision/decision/event/pointer/etag，立即检查 deferred constraints；
11. record body `etagVersion` 与强 ETag `"N"` 一致；
12. receipt 与业务写共同提交。

任一步失败，state/pointer/ETag/revision/decision/event/receipt 全不变。

### 5.4 exact release revalidation

新增 `installation_revalidation.py`，使用 caller-owned transition connection：

- installation/CAS 锁定并完成 state/marking 门后，先取得 Registry projection advisory lock `pg_advisory_xact_lock(228, 1)`，与 M1 publish/deprecate/revoke 串行；
- advisory lock 到手后先取得一次 frozen trust-root snapshot，再执行一次 `SELECT clock_timestamp()` 得到 `checked_at`；禁止使用 `transaction_timestamp()/now()`，因为它们返回 receipt/transition 事务开始时间。外部 trust-root 的线性化点为 snapshot 成功时刻，允许并发旋转落在线性化点之前或之后，但禁止在等待数据库锁前长期预取旧 snapshot；
- 按 lock.resolved 已 canonical 的 `publisher/id/version` 顺序，用一次批量 SQL 读取并锁定完整 version、artifacts、五类 evidence 行集；不得 N+1 查询；
- 复用公共 `ReleasePolicy.evaluate()`，逐项核对 status=published、contentHash、signatureFingerprint、releaseEvidenceRevision 和当前 trust root；
- 使用下表做 transport-neutral 翻译，不直接透传 `ReleasePolicy` 的客户端向错误。

| 原因 | 稳定结果 |
|---|---|
| exact version 缺失、status 不再 published、五类 evidence 缺失/expired/revoked、合法 evidence refresh 导致 revision 变化 | `REGISTRY_SNAPSHOT_STALE` 409 |
| 当前 trust root 不再存在/已 revoke/合法 rotate 后旧签名不再被接受、当前 root 尚未到 notBefore 或已过 notAfter、policy evidence revision 与 lock 不同 | `REGISTRY_SNAPSHOT_STALE` 409 |
| trust-root provider snapshot/read outage 或返回不可用视图 | `TRUST_ROOT_UNAVAILABLE` 503 |
| exact version 的 persisted contentHash 与 immutable lock 不同，或 descriptor canonical hash 与 persisted contentHash 不同 | `REGISTRY_INTEGRITY_CORRUPT` 500 |
| evidence observedAt 晚于锁后 checked_at、malformed persisted JSON、重复/越界关联、同一 current root 下 fingerprint/密码学验证不一致 | `REGISTRY_INTEGRITY_CORRUPT` 500 |
| PostgreSQL connection/deadlock/serialization/未知内部异常 | 保留脱敏 persistence exception，由全局映射固定 `INTERNAL_ERROR` 500，不伪装成 stale/corrupt |

translation 必须根据 revalidator 已分类的 cause 映射，禁止匹配异常 message。submit、approve、apply、verify 必做；reject、rollback 不做。不得调用 RegistryService 下划线私有函数，不得逐项另开事务。

### 5.5 server evidence

evidenceRef 固定：

```text
evidence://bundle-installations/{installationId}/revisions/{toRevision}/{type}
```

其中 type 为 `dry_apply/verification/rollback`。内层 `evidenceHash` 为以下 canonical JSON（不含 evidenceHash 本身）的 SHA-256：

```json
{
  "schemaVersion": "m2-installation-evidence/v1",
  "type": "dry_apply|verification|rollback",
  "evidenceRef": "...",
  "installationId": "...",
  "fromRevision": 3,
  "toRevision": 4,
  "fromState": "approved",
  "toState": "applied",
  "lockHash": "sha256:...",
  "permissionDiffHash": "sha256:...",
  "migrationPlanHash": "sha256:...",
  "contributionDiffHash": "sha256:...",
  "decisionId": "...",
  "status": "valid",
  "observedAt": "2026-08-03T12:34:56.12345+00:00"
}
```

- basis 只使用可永久重建的 immutable identity、event、to revision 和 decision 字段，不把后续会变化的 pointer 放入 hash。`fromState/toState` 与 evidence type 映射固定为 approved→applied/dry_apply、applied→active/verification、active→rolled_back/rollback。
- 新增 `installation_evidence.py`，唯一提供 `format_evidence_timestamp/build_evidence_basis/build_event_evidence/verify_event_evidence`；Service 写入前和 Store 每次完整 record 回读都必须从 installation identity + immutable event + to revision + decision 重建 basis 并复算 inner hash。inner 错、outer 对也返回 `LOCK_INTEGRITY_CORRUPT` 500。
- 外层数据库 `bundle_installation_event.evidence_hash` 继续对完整公开 `InstallationEventEvidence` envelope 做 canonical hash，与内层 basis hash 分工，不递归。
- 数据库 trigger 诚实只保证 outer envelope hash；直接 SQL 伪造 inner+正确 outer 可能落库，但任何 Store/API 回读都会按 immutable 列复算并失败关闭，不能进入可用状态。M2-B 不为此修改既有 migration/表。
- `observedAt` 必须等于 Registry advisory lock 后读取的一次 `clock_timestamp()`（rollback 为 CAS/marking 后单独读取的一次），revision/event created_at 显式写同一值。hash 前先转 UTC，固定 `+00:00`，微秒末尾 0 裁掉，全 0 省略小数点：`0→2026-08-03T12:34:56+00:00`、`100000→...56.1+00:00`、`123450→...56.12345+00:00`、`123456→...56.123456+00:00`；禁止 `Z` 和固定六位尾零。公开 DTO 回读若使用等价 offset，复算前必须先规范成该文本。
- evidenceRef、hash、status、observedAt 全由服务端生成；客户端不能提交或覆盖。
- M2 只有在所有门通过后生成 valid evidence；失败不持久化 invalid 事件。

---

## 6. Canonical HTTP 契约

### 6.1 端点表

| Method/Path | body/query | headers | success |
|---|---|---|---|
| POST `/v1/bundle-compositions:resolve` | CompositionRequest | Idempotency-Key | 201 StoredCompositionLock，无 ETag |
| GET `/v1/bundle-compositions/{composition_id}/locks/{revision}` | — | — | 200 StoredCompositionLock |
| POST `/v1/bundle-installations` | CreateInstallationRequest | Idempotency-Key | 201 InstallationResponse + ETag |
| GET `/v1/bundle-installations` | state?/limit/offset | — | 200 InstallationListResponse |
| GET `/v1/bundle-installations/{installation_id}` | — | — | 200 InstallationResponse + ETag |
| POST `.../{installation_id}/submit` | strict `{}` | Idempotency-Key + If-Match | 200 InstallationResponse + ETag |
| POST `.../{installation_id}/approve` | 四 hash | 同上 | 200 InstallationResponse + ETag |
| POST `.../{installation_id}/reject` | reason | 同上 | 200 InstallationResponse + ETag |
| POST `.../{installation_id}/apply` | strict `{}` | 同上 | 200 InstallationResponse + ETag |
| POST `.../{installation_id}/verify` | strict `{}` | 同上 | 200 InstallationResponse + ETag |
| POST `.../{installation_id}/rollback` | reason | 同上 | 200 InstallationResponse + ETag |

共新增 11 operations、10 unique paths。create/detail/action 的 HTTP ETag 必须等于 body `etagVersion`；不增加 Location 或 expectedRevision。

11 个显式稳定 operationId 固定为：`resolve_bundle_composition/get_bundle_composition_lock/create_bundle_installation/list_bundle_installations/get_bundle_installation/submit_bundle_installation/approve_bundle_installation/reject_bundle_installation/apply_bundle_installation/verify_bundle_installation/rollback_bundle_installation`。禁止依赖函数名自动生成。

### 6.2 Header 解析

- 所有 M2 POST 要求 **恰好一个** `Idempotency-Key`：1～160、trim 后不变、无 NUL/控制字符；缺失、重复或非法统一 `IDEMPOTENCY_KEY_REQUIRED` 400。
- 六个 action 要求 **恰好一个** If-Match，格式严格 `"[1-9][0-9]*"`；缺失 428，弱 ETag、`*`、列表、无引号、0、前导零或重复均 `PRECONDITION_INVALID` 400。
- Router 从 raw ASGI headers 计数并显式调用领域错误；不能把 Header 声明为 FastAPI required 后交给通用 validation。
- request hash 保存客户端规范化的 raw If-Match；不存在时 resolve/create 为 null。

### 6.3 Auth、错误与响应

- runtime 继续以 `require_principal` 为唯一认证/tenant 真源；M2 routes 额外用 `HTTPBearer(auto_error=False)` 仅声明 OpenAPI Bearer security，不替代认证。
- JWT claim 与 tenant header 不一致沿用 `AUTH_TENANT_MISMATCH` 403；生产缺 tenant claim 401；跨租户资源 404。
- `AssetRegistryError` 统一映射 ApiError envelope；PostgreSQL/credential/path/secret 不进入 message/details。
- Pydantic/body/query/path validation 的 runtime 仍由全局 handler 统一为 400；M2 OpenAPI 显式声明 400 ErrorBody，不在 worker 内局部移除 framework 422。
- replay response 必须重新通过对应 DTO 校验并核对 ETag/body，不用绕过 validation 的裸 JSONResponse。

### 6.4 新增稳定错误

| HTTP | code | 场景 |
|---:|---|---|
| 403 | `MARKING_ACCESS_DENIED` | mutation/resolve 的 target marking 不足，admin 也不绕过 |
| 500 | `REGISTRY_INTEGRITY_CORRUPT` | 已持久化 Registry descriptor/evidence/关联损坏 |

读取场景 marking 不足不返回新错误，统一隐藏为 `NOT_FOUND`。其余错误沿用 M2 上位方案。

---

## 7. Router aggregate、OpenAPI 与浏览器前置

### 7.1 聚合和生成物

- 总控在 `domain_manifest.json` 末尾追加 infra order 509/510；
- 运行 `scripts/generate_domain_aggregates.py` 生成，不手改 `domain_aggregates.py` 或 `main.py` import；
- 预计 manifest 509→511、infra 21→23；routeRows 4027→4038、unique operation pairs 4008→4019、runtime routes 4031→4042、OpenAPI paths 2267→2277；
- 上述 route 数在集成后由脚本实测冻结，schema component 数和 route hash不预猜；known duplicate 列表不得增加；
- 连续两个 clean process export 必须 byte-identical；更新 generated JSON/inventory，旧 `v1.yaml` 不在本波手补。

### 7.2 CORS 与 Web 边界

- 总控唯一允许修改 `services/aos-api/aos_api/main.py` 的内容：`expose_headers` 从 `X-Trace-Id` 扩为 `X-Trace-Id, ETag`，并加专项测试；allow headers 已为 `*`，浏览器可发 Idempotency-Key/If-Match。
- M2-B 不修改通用 `apps/web/src/api/client.ts` 返回类型，避免影响 1,000+ 既有调用；M3 安装管理 UI 可使用 body `etagVersion` 构造 If-Match，或新增独立 metadata helper。
- M2-B 浏览器前置用 raw fetch 验证 ETag 可读、preflight、错误 envelope 和刷新回读，不制作页面。

---

## 8. 四 Worker 文件所有权与波次

### M2-B0：总控共享底座

总控独占：

- `services/aos-api/aos_api/asset_registry/errors.py`
- `services/aos-api/aos_api/asset_registry/control_policy.py`（新）
- `services/aos-api/aos_api/asset_registry/control_protocols.py`（新）
- `services/aos-api/aos_api/asset_registry/control_wiring.py`（新）
- `services/aos-api/aos_api/routers/asset_bundles.py`（仅把既有 Registry factory 委托给共享 wiring，API/行为不变）
- `services/aos-api/tests/asset_registry/test_m2_control_policy.py`（新）
- `services/aos-api/tests/asset_registry/test_control_wiring.py`（新）

冻结并测试新增错误、operation role、no-admin-bypass marking、read-hide/mutation-deny、Protocol 和统一生产 wiring。`control_wiring.py` 公开 `build_asset_registry_service() -> RegistryService`、`build_composition_service() -> CompositionControl`、`build_installation_service() -> InstallationControl`；后两者在函数体内 lazy import B1 concrete Service，W3 Router 只依赖 builder/Protocol。可信根和 allowlist 配置只在 wiring 定义一次，旧 `get_asset_registry_service()` 保留原 dependency 名称和 cache，只委托 builder。B0 只验证配置、旧 Registry 行为和 lazy seam；B1 合入后 W4/B3 必须调用两个 control builder 做真实装配测试。B0 提交后五分支重新对齐，Worker 才开始 B1。

### M2-B1：三路并行

**W1 Composition** 独占：

- `services/aos-api/aos_api/asset_registry/composition_service.py`（新）
- `services/aos-api/aos_api/asset_registry/composition_store.py`
- `services/aos-api/tests/asset_registry/test_composition_service.py`（新）
- `services/aos-api/tests/asset_registry/test_composition_store.py`

W1 通过 Protocol 依赖 baseline reader；不修改 installation Store。

**W2 Installation** 独占：

- `services/aos-api/aos_api/asset_registry/installation_service.py`（新）
- `services/aos-api/aos_api/asset_registry/installation_revalidation.py`（新）
- `services/aos-api/aos_api/asset_registry/installation_evidence.py`（新）
- `services/aos-api/aos_api/asset_registry/installation_store.py`
- `services/aos-api/tests/asset_registry/test_installation_service.py`（新）
- `services/aos-api/tests/asset_registry/test_installation_revalidation.py`（新）
- `services/aos-api/tests/asset_registry/test_installation_store.py`

W2 提供 W1 所需的 active baseline reader 实现，并保持 Protocol 兼容。

**W3 Router/API** 独占：

- `services/aos-api/aos_api/routers/asset_control_headers.py`（新）
- `services/aos-api/aos_api/routers/bundle_compositions.py`（新）
- `services/aos-api/aos_api/routers/bundle_installations.py`（新）
- `services/aos-api/tests/asset_registry/test_composition_api.py`（新）
- `services/aos-api/tests/asset_registry/test_installation_api.py`（新）

W3 只调 Service，不接触 Store/SQL；dependency factory 可 lazy import 具体 Service，API 单测用 dependency override，从而可与 W1/W2 并行。

### M2-B2：W4 独立对抗

W4 独占：

- `services/aos-api/tests/asset_registry/test_m2_control_plane_adversarial.py`（新）
- `services/aos-api/tests/asset_registry/test_m2_control_plane_integration.py`（新）

W4 不修改生产文件；以合入 W1/W2/W3 后的基线写真实 PostgreSQL 并发、故障注入、tenant/auth/header/marking/receipt-first 对抗测试。发现问题退回原 owner 修复。

### M2-B3：总控集成和生成

总控独占：

- `services/aos-api/aos_api/routers/domain_manifest.json`
- `services/aos-api/aos_api/routers/domain_aggregates.py`（仅脚本生成）
- `services/aos-api/aos_api/main.py`（仅 CORS ETag）
- `scripts/export_openapi.py`
- `services/aos-api/tests/test_domain_router_manifest.py`
- `services/aos-api/tests/test_openapi_contract.py`
- `packages/contracts/openapi/v1.generated.json`（仅脚本生成）
- `packages/contracts/openapi/v1.inventory.json`（仅脚本生成）
- M2-B 证据文档和上位状态文档。

`composition_contracts.py`、migration、resolver、registry_snapshot、release_policy 和 public `asset_registry/__init__.py` 原则上不改；两个新增稳定错误只要求从 `asset_registry.errors` 使用，不扩大五项公共 package 导出。旧 asset_bundles Router 只允许 B0 的 factory wiring 委托，路由/DTO/API 行为不得变化；其他修改必须先重开方案并由总控裁决。

---

## 9. 测试矩阵

### 9.1 P0 Service/Store

1. resolve 同 key 同请求双线程仅一次 snapshot/resolve/write；同 key异 body/subject 冲突；跨 tenant/operation 可复用。
2. receipt 成功后让 snapshot/resolver/current Registry 全部抛错，replay 仍原 201/200/body/ETag；但 immutable role/marking 撤销仍阻止读取。
3. composition/lock 写后 receipt 前、decision/revision/event/pointer/receipt 各点故障，事务全部回滚。
4. current ref 四字段逐项 stale、active null、跨租户、environment mismatch、并发 transition；baseline 必须取 active historical lock。
5. 六条合法状态边和非法边笛卡尔；operation/evidence/decision/reason 错配全部零写；rejected/rolled_back 终态；pointer/decision/event/evidence/etag 精确。
6. approve/reject、apply/verify/rollback 双线程同 ETag 只有一个成功；输家无 receipt。
7. submit/approve/apply/verify 与 revoke/evidence expire/delete/refresh/trust-root revoke 并发；事务开始后等待 global lock 跨过 evidence/root expiry 必须按锁后 `clock_timestamp()` stale，等待期间 rotate root 后不得使用等待前旧 root；多个 release 同时变化仍为一次 canonical batch/单一事务视图，成功 evidence/revision/event 三个时间逐字相等且不早于锁释放。
8. role 矩阵、admin 自批、admin marking 不足、只有 unchanged target marking 不足；全部零写。
9. rollback 在 Registry 已 revoke 时仍成功；公共 API 路径恢复 null previous，受控 forward-compat fixture 验证 non-null previous；无 Bundle executor/network/migration 调用。
10. persisted lock/decision/event/receipt/Registry 任一篡改失败关闭并脱敏；inner 错 outer 对、outer 错 inner 对均失败，apply→verify→rollback 每条历史 evidence 重启后可复算。
11. `ReleasePolicy` 每类异常按 cause translation matrix 精确归类，覆盖 contentHash drift、root notBefore/notAfter、future observedAt；禁止异常 message 匹配；DB Check/Unique/deadlock/serialization 与 `SET CONSTRAINTS` 失败脱敏、零 receipt。
12. observedAt 的 0/100000/123450/123456 golden 文本、Python/PG、多时区和重启回读一致。

### 9.2 P0 HTTP/OpenAPI

1. 11 routes 未认证 401且 Service 零调用；tenant header 伪造 403；跨租户 404。
2. body 注入 tenant/actor/roles/markings、snake_case、coercion、extra 字段全部 400。
3. Idempotency-Key 缺失/空白/NUL/控制/161字符/重复；If-Match 所有非法形状/重复/旧值。
4. 首次与 replay status/body/ETag 完全一致；body etagVersion 与 response ETag 一致。
5. list marking SQL 前过滤、total 不泄露；detail/lock marking 不足 404。
6. OpenAPI 两次 byte-identical、11 个显式 operationId 精确集合、10 paths/参数名完整、header required/security/status/response header 正确、duplicates 不增加。
7. aggregate 生成无漂移；旧 asset Registry API 契约不变。
8. OPTIONS 与 raw browser fetch 可发送两个控制 header、读取 ETag 和错误 traceId。

### 9.3 累计门

- changed-file Ruff/format；
- M1 Registry + M2-A + M2-B asset_registry 全专项；
- migration head/current 和 downgrade blocker；
- OpenAPI/aggregate 两次生成；
- 后端全量；
- SDK、Web、Desktop tests；
- Web/Desktop typecheck/build；
- source/build security scan；
- 真实 PostgreSQL 双线程并发与跨租户矩阵。

每个 B0/B1/B2 小波至少跑自己的专项和 M1+M2 累计；B3 才跑全平台最终门。任何阶段红灯都停在当前小波，不带红进入下一波。

---

## 10. 风险与回滚

| 风险 | 等级 | 控制 |
|---|---:|---|
| receipt 与业务写不同事务 | P0 | caller-owned Store + handler 同连接 + 故障注入 |
| replay 绕过权限撤销 | P0 | receipt-first 后只读 immutable lock 做 role/marking 门 |
| exact release 与 transition 混合视图 | P0 | projection advisory lock + caller-owned transaction + frozen trust root |
| admin marking 绕过 | P0 | M2 专用 control policy，正反测试 |
| list total 泄密 | P0 | SQL 分页/计数前 marking filter |
| evidence hash 自引用或不可复算 | P0 | inner basis 只取 immutable 列，写前与每次回读重算；outer envelope 由 DB 另验 |
| Router header 先被框架拦截 | P1 | raw 单值解析 + OpenAPI 手工 required |
| CORS 读不到 ETag | P1 | 总控仅增加 exposed ETag |
| W1/W2/W3 共享文件冲突 | P1 | B0 后对齐，B1 文件独占，W4 只写测试 |

回滚优先 revert Router/Service/manifest/CORS，不删除 M2 数据。存在 composition/installation/command 数据时 migration downgrade 继续失败关闭；不得为回滚静默清理审计历史。

---

## 11. 进入编码结论

M2-A 最终 GREEN，五分支已对齐 `a6e4d31`。本文件 v1.2 已根据三组交叉评审补齐事务、baseline、跨 Worker Protocol、typed transition、exact revalidation、role/marking、可复算 evidence、header、OpenAPI、CORS 和文件所有权；最终复核残余 P0/P1 为零，正式授权 B0。

**下一步固定为 M2-B0：总控先交付新增稳定错误、control policy/protocol/wiring；专项通过并同步五分支后，W1/W2/W3 并行进入 B1。不得跳过 B0 直接写 Router。**
