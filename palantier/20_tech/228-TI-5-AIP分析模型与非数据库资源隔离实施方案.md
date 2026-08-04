# 228 · TI-5 AIP、分析模型与非数据库资源隔离实施方案

> 版本：v1.1 · 2026-08-04
> 状态：A1 GREEN，A2 待实施
> 前置：TI-4 全域 GREEN；当前代码 `m1@d381578`

## Rules

先处理已有租户字段和运行链，再处理未知历史归属；不得把历史测试数据、对象正文、ID 名称或创建时间当成客户归属证据。PostgreSQL 使用 canonical TenantScope、scoped transaction、复合 Contract 与 FORCE RLS；非数据库资源使用同一 tenant key/envelope。只验证本地 synthetic/测试组织，不连接真实商城、真实模型供应商或客户凭据。

## 1. 现状与范围

TI-0E 的冻结执行组在 TI-4 后剩余 TI-5：

- AIP 运行表：eval report、suite、logic graph、revision、run、run node、publication；已有 scope，但仍需运行链与 RLS/Contract 收口。
- `meta_aip_kv`：23 条历史记录，无完整 scope，先做 namespace 决策账本，未知归属进入维护隔离区。
- Analytics/模型目录：capacity、usage、catalog、provider、route、health、registered model；已有 dev scope，但仍是弱全局主键、无 RLS。
- `decision_lineage`：631 条无 scope 历史，当前与对象引用匹配为 0；禁止默认认领，先逐记录决策并可逆隔离。
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

### TI-5 A3：Decision Lineage 历史归属

- 增加 TenantScope 与输入/输出/执行上下文证据列，不按 ID 或时间猜测。
- 当前 631 条引用无法证明时全部进入可逆维护隔离，不伪造测试组织归属。
- 新写 lineage 必须从 Principal/执行 envelope 继承完整 scope。

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
