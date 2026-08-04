# 228 · TI-5 AIP、分析模型与非数据库资源隔离实施方案

> 版本：v1.4 · 2026-08-04
> 状态：A1/A2/A3 GREEN，B1/B2 待实施
> 前置：TI-4 全域 GREEN；当前代码 `m1@68974ed`

## Rules

先处理已有租户字段和运行链，再处理未知历史归属；不得把历史测试数据、对象正文、ID 名称或创建时间当成客户归属证据。PostgreSQL 使用 canonical TenantScope、scoped transaction、复合 Contract 与 FORCE RLS；非数据库资源使用同一 tenant key/envelope。只验证本地 synthetic/测试组织，不连接真实商城、真实模型供应商或客户凭据。

## 1. 现状与范围

TI-0E 的冻结执行组在 TI-4 后剩余 TI-5：

- AIP 运行表：eval report、suite、logic graph、revision、run、run node、publication；已有 scope，但仍需运行链与 RLS/Contract 收口。
- `meta_aip_kv`：23 条历史记录，无完整 scope，先做 namespace 决策账本，未知归属进入维护隔离区。
- Analytics/模型目录：capacity、usage、catalog、provider、route、health、registered model；已有 dev scope，但仍是弱全局主键、无 RLS。
- `decision_lineage`：631 条无 scope 历史，与 `obj_instance` 直接匹配为 0，但只读 A3 precheck 已证明全部与唯一 Draft 父记录四重一致；必须以父 Draft 作为归属真源，不得仅因对象匹配为 0 就丢失可恢复归属。
- 非 PostgreSQL：对象前缀、向量、缓存、队列、离线产物和进程内引擎。

## 2. 分波

### TI-5 A1：AIP 已有 scope 运行链

- 全部 AIP Store/API/worker 显式传 TenantScope，删除 optional/default scope。
- scoped transaction 降权，冻结复合主键/父子 FK/NOT NULL，ENABLE/FORCE RLS。
- 同 ID 双 scope、无 GUC零可见、跨 scope mutation 拒绝。

实施结果：`d381578` 已完成 7 张 AIP 表 workspace FK、FORCE RLS、双 GUC policy，以及 Graph/Run/Eval/Publication Store scoped transaction；共享库可逆往返和 27 行守恒，83 项 AIP 专项与 181 项 Tenant Isolation 回归 GREEN。

### TI-5 A2：AIP KV 历史归属与 Contract

- nullable Expand 与 append-only ownership ledger 分离实施。
- 仅基于可审计 namespace/父资源关系作 ASSIGN；无法证明的记录 QUARANTINE。
- 回填/隔离可逆，业务 payload hash 与总数守恒；runtime 不得访问隔离表。

A2 实施冻结：当前共享非生产库 23 条 KV 均由本地测试流程产生，且用户已明确“现有应用作为测试组织、现有数据均为测试数据”，因此本批次以显式 key 清单和源库环境共同作为 `ASSIGN_TEST_ORG` 证据，归属 `dev-org/dev-project`；不使用更新时间或 payload 内容猜测。清单外的 NULL scope 历史一律 QUARANTINE。`meta_aip_kv` 收归 Alembic、主键改为 `(org_id, project_id, key)`、workspace FK/FORCE RLS；request dependency 在路由执行期间绑定 canonical ContextVar，KV 仍显式解析 `require_tenant_scope()`，无请求/无任务 envelope 时失败关闭。降级遇到跨 scope 同 key 冲突必须停止，不覆盖数据。

实施结果：`30137dd` 已完成 `228ti5a2kv` 迁移、23 条显式清单归属账本、workspace FK/FORCE RLS/复合主键、KV scoped transaction 和 request ContextVar 生命周期。共享库完成降级再升级往返，23 条 KV 与 23 条 ledger 守恒；A2 专项 5 passed、相关 API 29 passed、Provider 22 passed / 2 skipped、Tenant Isolation 186 passed / 11 skipped，同时 9,182 项全量测试收集 GREEN。

### TI-5 A3：Decision Lineage 历史归属

- 增加 TenantScope，以 `draft_dataset(org_id, project_id, id)` 作为执行上下文父记录；不按时间、payload 或对象 ID 名称猜测。
- A3 precheck 冻结基线：631/631 满足 `lineage.id = 'lin-' || draft_id`，631/631 唯一命中 Draft，631/631 的 action/object 字段与父 Draft 一致，父 Draft 均为 `dev-org/dev-project`，无 NULL scope、无一对多命中。因此本批次逐条 `ASSIGN_FROM_DRAFT`，而非默认认领。
- 任一四重证据不满足的旧行必须原样移入 `decision_lineage_orphan_quarantine`，记录 payload hash 与原因，runtime 不得访问；本次预期 quarantine=0，但不删除该安全网。
- 新写 lineage 必须从 Principal/执行 envelope 继承完整 scope，使用 scoped transaction，写入 `(org_id, project_id, id)` 且父 Draft scope 必须一致。
- 活跃表冻结 scope NOT NULL、workspace FK、父 Draft 复合 FK、复合主键与 FORCE RLS；Analytics/Quiver/Demo read 全部使用完整 scope。`ensure_lineage_schema()` 改为 migration-owned no-op，禁止请求期 DDL。
- 降级前若同 id 已跨 scope 共存则阻断，不静默合并；无冲突时将 quarantine 原样恢复并撤销 Contract。

A3 预计文件边界：

- Migration：`services/aos-api/alembic/versions/228ti5a3_decision_lineage_contract.py`
- Runtime：`services/aos-api/aos_api/routers/runtime_write.py`、`routers/analytics.py`、`demo/demo_story.py`、`demo/seed.py`
- Schema report：`services/aos-api/aos_api/tenant_schema_lint.py`
- Tests：`services/aos-api/tests/tenant_isolation/test_ti5_a3_decision_lineage_contract.py` 及被 Contract 影响的既有 lineage/analytics/demo 用例。

A3 前置备份：`/private/var/tmp/aos-ti5-a3.OAHNwn/aos-meta-before.dump`，1,907,663 bytes，mode `0600`，SHA-256 `3c6ed2195abc836cbede6c8e809a73cb7fb8bd20cf95d95281694157d78b9b0a`。基线 lineage 行数 631，聚合 hash `e0e211357213b2211e7c27c0032e7c4a`。

实施结果：`68974ed` 已完成 `228ti5a3lineage`。631 条 `ASSIGN_FROM_DRAFT` 账本、可逆 quarantine 安全网、workspace/Draft 复合 FK、复合主键、FORCE RLS 及 lineage/analytics/demo scoped read/write。共享库降级到 A2 时 631 行与原始 hash `e0e211357213b2211e7c27c0032e7c4a` 完全恢复，再升级后 631 活跃、631 ledger、0 quarantine、0 orphan。A3/Action/Draft/Analytics 核心 32 passed，Tenant Isolation 195 passed / 7 skipped，9,204 项全量收集 GREEN。同时将 Action/Draft 建表从请求期下沉到 bootstrap，修复 A2 ContextVar 下同步路由的降权 DDL 回归。

### TI-5 B1/B2：Analytics 与模型目录

- B1：Provider/Model/Route/Usage/Capacity/Health 全链显式 TenantScope 与 scoped transaction。
- B2：workspace FK Validate、复合主键/父子 FK、scope NOT NULL、FORCE RLS；平台模型模板与组织实例配置保持分离。
- 组织级供应商启停、路由、额度和健康状态互不影响；不得把共享 catalog 模板误变成租户实例。

### TI-5 C：非 PostgreSQL 与进程内状态

- 统一 key：`org_id/project_id/resource_kind/resource_id`；队列 envelope 必含 TenantScope。
- Object Storage 仅允许受控 tenant prefix；列表、删除、重建和统计不能扫其他前缀。
- Vector namespace、cache key、offline output、dead-letter 和 retry key 均含完整 scope。
- Object/Delta/Stream indexing 等进程内单例的 key、列表、删除和统计按 scope 隔离。
- 未配置真实后端时只宣告契约与本地 fake GREEN，不冒充外部实盘验证。

### TI-5 D：总收口

- 全量 schema/resource lint、同 ID 双 scope、跨 scope 负向、无 scope fail-closed。
- PostgreSQL 真实备份、降级、升级与行数/hash 守恒。
- Tenant Isolation 累计回归、五分支同 HEAD/tree、上下文与证据更新。

## 3. 文件边界

- Migration：`services/aos-api/alembic/versions/228ti5*.py`
- Scope/Schema report：`services/aos-api/aos_api/tenant_scope.py`、`tenant_schema_lint.py`
- AIP/Analytics/Model Store 与 Router：只修改实际命中的 Store/API/worker 文件。
- 非表资源：对象、向量、缓存、队列、离线与 indexing engine 的实际实现文件。
- Tests：`services/aos-api/tests/tenant_isolation/test_ti5_*.py` 及现有专项回归。

每个子波编码前必须先以代码检索确认真实文件清单；禁止按文件名猜测或大范围重构。

## 4. 退出门

- TI-0E 登记的 TI-5 资源全部有执行结果，无遗漏、无重复。
- 栖月汇业务数据仍为 0；测试数据只在“测试组织”scope 或维护隔离区。
- 组织/工作区之间 AIP、分析模型配置、额度、对象、向量、缓存、队列和内存状态互不可见、互不覆盖。
- 未知历史可审计、可逆、运行时不可见；不得通过伪造归属换取空阻断表。
- TI-5 GREEN 后进入 TI-6 生产前门禁；仍不得开始真实微商城 Connector。

## 5. 回滚与风险

- 每个数据库子波先做 Git 外备份，提供 downgrade，并核对活跃+隔离总量与 hash。
- 非表资源只做前缀/namespace/key 级迁移，不读取业务正文猜租户；无可信归属时冻结旧 namespace。
- 生产外部后端未配置时保留 `EXTERNAL_BACKEND_UNVERIFIED`，由 TI-6 作为上线阻断，不虚报 GREEN。
- `decision_lineage` 与 `meta_aip_kv` 是当前最大历史风险；先隔离、后凭证恢复，禁止不可逆删除。
