# 228 · TI-5 AIP、分析模型与非数据库资源隔离实施方案

> 版本：v1.12 · 2026-08-05
> 状态：A1/A2/A3/B1/B2/C1/C2/C3 GREEN，下一门 D
> 前置：TI-4 全域 GREEN；当前代码 `m1@56405f1`

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

### TI-5 B1：模型管理运行链与数据库 Contract

只读核查冻结基线：`capacity_limits=4`、`capacity_usage=30`、`model_catalog=12`、`model_provider=4`、`model_route=5`、`provider_health=4`、`registered_models=6`，共 65 行，全部明确位于测试组织 `dev-org/dev-project`。七表均已有非空 scope，但仍使用全局 `id` 主键、无 workspace/父子 FK、无 RLS；五个 Store 仍把 `_DEFAULT_ORG/_DEFAULT_PROJECT` 写死，四个管理 Router 未绑定 Principal。这些事实只能证明数据来自测试组织，不能证明现有运行链已隔离。

B1 冻结为一个可独立回滚的 PostgreSQL 波次：

- Router：`routers/model_catalog.py`、`routers/model_providers.py`、`routers/model_routes.py`、`routers/model_capacity.py` 全部依赖 `require_principal`，从 Principal 构造 canonical `TenantScope` 并显式传入 Store；客户端 `projectId` 仅可作为额度业务键，不得改写认证 scope。
- Store：`model_catalog.py`、`registered_models.py`、`model_providers.py`、`model_routes.py`、`model_capacity.py` 删除默认组织常量，公开读写均要求 `TenantScope`，所有连接使用 scoped transaction；请求期 `ensure_schema()` 改为 migration-owned no-op。
- Migration：七表冻结 `(org_id,project_id,id)` 复合主键、scope NOT NULL、workspace FK、ENABLE/FORCE RLS 与双 GUC policy；`provider_health` 增加同 scope provider 复合 FK，`registered_models` 增加同 scope catalog 复合 FK。`model_route.primary_model/fallback_model` 的旧数据目前是注册模型标识还是供应商模型名需用数据和调用契约判定，未证明前不得强加错误 FK。
- 历史：65 行均基于用户已确认的“现有测试数据”保持原 scope，不做内容猜测、不新建归属账本；迁移前后逐表 count/hash 守恒。若升级前出现 NULL scope、非 workspace scope 或父记录缺失，迁移必须失败，不自动认领或删除。
- 回滚：降级前检测跨 scope 同 `id` 冲突；存在冲突则阻断，避免退回全局主键时覆盖。无冲突才撤销 RLS/FK/复合主键，并恢复原全局主键结构。
- 验证：七表同 ID 双 scope、跨 scope read/update/delete、无 GUC零可见、错误父 scope 拒绝、认证 scope 不可被 query/body 覆盖；共享库真实 downgrade/upgrade 往返并校验 65 行 hash。

B1 预计文件边界：

- Migration：`services/aos-api/alembic/versions/228ti5b1_model_management_contract.py`
- Runtime：上述五个 Store、四个 Router及四个 demo seed 文件。
- Registry/lint：`tenant_resources.yaml`、`tenant_schema_lint.py`。
- Tests：`tests/tenant_isolation/test_ti5_b1_model_management_contract.py`，并更新 `test_model_management.py`、`test_phase5_regression.py` 的显式 scope 调用。

B1 实施结果：`044f5a5` 已完成 `228ti5b1models`。七表均为 `(org_id,project_id,id)` 主键、validated workspace FK、双 GUC FORCE RLS；Provider Health→Provider 与 Registered Model→Catalog 使用同 scope 复合 FK。四个 Router 从 Principal 取 scope，五个 Store 删除默认组织并使用 scoped transaction，demo seed 只在显式测试 scope 内执行。共享库 65 行完成真实降级/升级，七表逐表 count/hash 全部不变；模型管理 33 passed，B1 专项 4 passed，Tenant Isolation 199 passed / 7 skipped，9,191 项全量收集无错误。备份：`/private/var/tmp/aos-ti5-b1.0If0El/aos-meta-before.dump`，1,944,971 bytes，mode `0600`，SHA-256 `ebdcbe71e0b020465873a7f29fff96e031310e336ee449f22ed53479aa31b3f4`。

### TI-5 B2：平台模型模板与组织实例分离核验

- 当前 `model_catalog` 本身带组织/工作区 scope，语义上是“组织可发现目录快照”，不是平台全局模板；`registered_models`、provider、route、额度、usage、health 均是组织实例或运行状态。B1 不把它们提升成共享表，也不借隔离补强重新设计模型管理架构。
- B2 只核验所有平台级只读模型模板来源与组织实例的物化边界：共享模板不得携带客户凭据、启停、额度、健康或路由；组织套用模板后必须产生独立 scoped 实例，组织定制不能反写模板，也不能影响其他组织。
- 若代码中不存在独立平台模板存储，B2 以“能力缺口 + TI-6 上线阻断”登记，不在租户隔离波次凭空新建一套 catalog。只有现有产品/架构文档已有明确模板实体时，才补对应 Contract 与测试。
- B2 退出门是形成资源分类、调用证据和负向测试结论；不得把 B1 七表 GREEN 误报为平台模板能力已实现。

B2 代码/产品核查结论与验证边界冻结如下：

- 平台模板已有真实载体：`plugins/llm-providers/*/manifest.json` 由 `llm_provider_registry._scan_disk()` 只读扫描，包含 provider 类型、能力、默认模型和配置 Schema，不含客户凭据、启停、健康、额度或路由状态。
- 组织实例已有真实载体：安装状态、自定义插件、ready、组织配置与凭据槽分别落在 `meta_aip_kv` 的 `llm_provider_installs/custom/ready/configs/secrets`；A2 已使同 key 可跨 scope 共存并由 canonical ContextVar + RLS 隔离。
- B1 七表是组织的模型管理实例/可发现目录快照，不是平台模板；12 条 seed 只属于测试组织，不得展示给栖月汇空组织。
- `aip_model_catalog.ModelCatalogEngine` 是另一条进程内 Singleton CRUD，既不是只读 manifest，也未绑定 TenantScope；它归 TI-5 C 修复，不得用 B1 PostgreSQL GREEN 掩盖。
- B2 只新增契约测试：同一磁盘 manifest 对两 scope 均只读可见；A scope 安装/配置不得改变 B scope，也不得修改 manifest 文件 hash；不新增表、不改变产品三层栈式架构。

B2 实施结果：`7022ffe` 新增模板/实例负向契约测试并 GREEN。`moonshot` 磁盘 manifest 在两个 synthetic scope 中版本一致；A scope 安装后仅 A 的 scoped KV 状态变为 installed，B 仍为 false，manifest SHA-256 前后不变。平台 Provider manifest 与组织安装/配置实例分离得到代码证据；`aip_model_catalog` Singleton 明确转入 TI-5 C。

### TI-5 C：非 PostgreSQL 与进程内状态

- 统一 key：`org_id/project_id/resource_kind/resource_id`；队列 envelope 必含 TenantScope。
- Object Storage 仅允许受控 tenant prefix；列表、删除、重建和统计不能扫其他前缀。
- Vector namespace、cache key、offline output、dead-letter 和 retry key 均含完整 scope。
- Object/Delta/Stream indexing 等进程内单例的 key、列表、删除和统计按 scope 隔离。
- 未配置真实后端时只宣告契约与本地 fake GREEN，不冒充外部实盘验证。

### TI-5 C1：对象存储与向量 namespace

当前只读复核：MinIO `aos-media` 共 75 个对象，73 个位于 `dev-org/dev-project/` canonical prefix，2 个为历史 probe（`dev-probe.txt`、`dev-probes/...`）且无可证明客户归属；栖月汇 prefix 为 0。local vector 仅 1 条 `meta_aip_kv`，数据库 scope 为 `dev-org/dev-project`，key 中 collection 亦为 `dev-org__dev-project__demo-pipe-wo`，属于双重 scoped 测试数据。缓存未配置、离线 Store 未实现、消息队列仅进程内，不能虚报外部后端实盘。

C1 冻结：

- `file-object-store` probe 必须接收认证 Principal 的 `TenantScope`，只列 `tenant_key_prefix(scope)`，不得再使用空 prefix 扫全 bucket；返回 sample 只能是本 scope key。
- 业务对象读写/删除必须先 `assert_object_key_tenant`；workspace clear 只能删除本 scope prefix。底层管理员 adapter 可保留 raw key 能力，但不得直接暴露给租户 API。
- 两个无 canonical prefix 的 probe 对象只做可逆维护隔离：先本地安全备份 bytes/hash 和 manifest，再复制到 `_maintenance/quarantine/unowned/`，验证后删除旧 key；不得认领给测试组织或客户组织。维护 prefix 永不出现在租户 list/probe。
- local vector 继续复用 A2 scoped KV + `scoped_collection_name`；补同逻辑 collection 双 scope 与 foreign prefix 拒绝测试。Qdrant 未配置，只验证 collection namespace 契约并保留 `EXTERNAL_BACKEND_UNVERIFIED`。

C1 实施结果：`bb0773c` 将 `file-object-store` probe 改为必须接收认证 Principal 的完整 TenantScope，只能列 `tenant_key_prefix(scope)`；无 scope 失败关闭。新增对象/向量 namespace 专项 3 passed，相关 Connector 回归 18 passed。MinIO 两个无归属历史 probe 已先备份到 `/private/var/tmp/aos-ti5-c1-bzbep_4o`，再复制到 `_maintenance/quarantine/unowned/<sha256>` 并完成读回 hash 校验后删除旧 key；总对象数仍为 75，其中测试组织 canonical prefix 73、维护隔离 2、栖月汇 prefix 0。local vector 唯一 KV 同时具备数据库 scope 与 scoped collection name；Qdrant 未配置，状态保持 `EXTERNAL_BACKEND_UNVERIFIED`，不宣称外部实盘 GREEN。

### TI-5 C2：关键进程内 Singleton

- 首批必须处理已证实的可变租户数据链：`aip_model_catalog.ModelCatalogEngine`、`phase5_pipeline_engine` 的 Dataset/Build/Health/SyncConfig、`wave_ext` Demo Dataset/Media bytes，以及直接关联的 analytics/read 路径。
- 引擎 key 必须含 `(org_id,project_id,resource_id)`，Router 从 Principal 显式传 `TenantScope`；列表、详情、更新、删除、统计、reset 均只作用当前 scope。同 ID 双 scope不能覆盖。
- 832 条静态 finding 不是 832 个租户缺口：常量 set/dict、只读 registry、平台模板先排除；可变 Singleton 必须按 Router 可达性和业务数据语义形成机器清单，未分类项阻断 TI-5 D，不凭文件名批量改造。

C2 按可独立验证、可独立回滚的两个子波实施，避免一次改动整个进程态：

- **C2-A Model Catalog + Phase5 Dataset 链**：`aip_model_catalog.ModelCatalogEngine` 的 CRUD 改为 `(scope.key,item_id)`；`phase5_pipeline_engine` 仅将 Dataset/Build/Health/SyncConfig 四组容器改为 scoped key，Pipeline/Node/Schedule 等其他状态不在本子波扩张。两个 Router 全部依赖 `require_principal`，且每个 engine 调用显式传 `TenantScope`。
- C2-A 容量上限按 scope 计算；list/detail/update/delete/preview/build/health/sync-config 均只见当前 scope。同 ID 双 scope 可共存；A scope 的 reset 不能清 B scope。仅测试基础设施允许命名明确的 `reset_all_for_tests()`，生产路由不得调用。
- C2-A demo seed 必须显式接收 scope，禁止把示例 Dataset 隐式灌入全局空间；既有直接 engine 测试改为显式 `TEST_SCOPE`，不得引入默认组织常量。
- **C2-B Wave Ext Demo Dataset/Media**：在 C2-A GREEN 后单独处理 `wave_ext` 的 `_datasets/_media/_media_bytes` 及关联 analytics/read；按 scope 分桶并补跨 scope 同 RID、bytes、list、delete/clear 负向门。
- C2-A 文件边界：`aip_model_catalog.py`、`aip_model_catalog_router.py`、`phase5_pipeline_engine.py`、`routers/phase5_datasets.py`、`demo/seed_phase5_pipeline.py`，以及对应既有测试和 `tests/tenant_isolation/test_ti5_c2a_singleton_scope.py`。不新增数据库表，不改变公开响应 DTO。
- C2-A 退出门：专项同 ID 双 scope、跨 scope 404/不可见、scope reset、容量分租户、无鉴权拒绝；既有 AIP Catalog、Phase5 Dataset 与 Router 回归全部通过。若发现其他调用者无法安全获得 scope，则失败关闭并登记到 C2-B/后续清单，不以默认 scope 兼容。

C2-A 实施结果：`a302544` 已将 AIP Model Catalog CRUD/容量/reset 与 Phase5 Dataset/Build/Health/SyncConfig 全链改为显式 TenantScope 和 scoped key；两个 Router 均从认证 Principal 构造 scope，demo seed 也必须显式传 scope。专项及相关回归 77 passed，Tenant Isolation 206 passed / 8 skipped，全量 9,199 项收集无错误；五条代码分支同步到同一 HEAD/tree。复核同时确认 `/v1/datasets` GET 与 `wave_ext` 存在既有重复路由，当前有效 GET 由已做 metadata scope 过滤的 wave_ext 响应；该路由真源冲突与 `_datasets/_media/_media_bytes` 全链必须在 C2-B 收口，因此 C2 总门尚未 GREEN。

C2-B 编码边界进一步冻结如下：

- `_datasets`、`_dataset_history`、`_media`、`_media_bytes` 统一使用 `(org_id,project_id,rid)` key；所有 get/list/enrich/parse/reference/docintel、pipeline create/patch、sync history 与 hydrate 都先由 Principal/显式 TenantScope 生成 key，禁止“全局 rid 命中后再看 metadata”的兼容路径。
- `data_os_store.load_all(scope)` 仍返回本 scope 的 RID 映射，但 `wave_ext._hydrate_data_os_scope` 必须逐项转换为 scoped key；boot 只清运行缓存。demo seed 改为显式 `scope`，不再生成无归属 Dataset/History。
- Analytics 的 dataset lookup/ontology rail 必须接收 Principal scope，只读取该 scope 的 wave_ext Dataset；测试直接注入内存数据也必须使用 scoped helper，不得写裸 RID key。
- Media bytes 与 metadata 必须使用同一个 scoped key。parser/docintel 通过 `mediaRid` 读 bytes 前必须先命中本 scope metadata；即便 A/B 使用相同 RID，也只能解析各自 bytes。对象存储 key 继续由 C1 tenant prefix 保护。
- `/v1/datasets` GET 的运行时真源按现有 Router 注册顺序认定为 `wave_ext` Data OS；Phase5 同名 GET 定义登记为 `NOT_REACHABLE_DUPLICATE`，本波不改变已冻结 route manifest/operationId。其存储已在 C2-A scoped，不作为绕过路径；后续 API 去重须单独兼容性评审。
- C2-B 文件边界：`routers/wave_ext.py`、`routers/analytics.py`、`data_os_store.py`、`demo/demo_story.py`，对应既有测试及 `tests/tenant_isolation/test_ti5_c2b_wave_ext_scope.py`。退出门包含同 RID 双 scope Dataset/History、Media metadata/bytes/parse、hydrate、analytics rail/preview、demo seed 显式 scope与现有 Data OS/Media 回归。

C2-B 实施结果：`4e5d069` 已将 `_datasets/_dataset_history/_media/_media_bytes` 统一为 `(org_id,project_id,rid)` key；hydrate、analytics lookup、demo seed、purge 与 parser/docintel 均显式 TenantScope。`b249a2d` 补齐 Parser registry 直接单测的显式 ContextVar scope。`GET /v1/datasets` 运行时真源冻结为 wave_ext Data OS；Phase5 同名 GET 登记为 `NOT_REACHABLE_DUPLICATE`（manifest 仍 2 条，本波不改 route 契约）。相关回归 80 passed / 1 skipped，Parser 7 passed，Tenant Isolation 211 passed / 8 skipped，全量 9,204 项收集无错误；五分支同 HEAD/tree。C2 总门 GREEN；下一门 C3。

### TI-5 C3：缓存、队列、离线与剩余进程态收口

- 未配置 Redis/队列/离线后端时建立 canonical key/envelope contract、本地 fake 负向测试和启动状态 `NOT_CONFIGURED`；不得宣称生产后端 GREEN。
- 对实际可达的 retry/dead-letter/job/offline output，envelope 缺 TenantScope 必须失败关闭；管理统计不得跨 scope 聚合明细。
- 完成 mutable finding 分类表：`TENANT_OWNED_FIXED`、`PLATFORM_TEMPLATE`、`CONSTANT`、`NOT_REACHABLE`、`EXTERNAL_UNVERIFIED`，每项带代码证据。

C3 按真实路由可达性拆成三个最小子波，禁止用静态命中数量驱动大范围重构：

- **C3-A Job / DLQ envelope**：只处理 `wave_ext` 中实际可达的 capability job、DLQ、docintel failure 与 demo purge。`_jobs`、`_dlq` 使用完整 `(org_id,project_id,rid)` key；返回 envelope 固化 `orgId/projectId`。list/status/retry 只能访问当前 scope，同 ID 双 scope 可共存，跨 scope 必须 404/不可见。`_capabilities` 是平台级开发能力模板，登记为 `PLATFORM_TEMPLATE`，但由模板产生的 job 必须属于调用 scope。
- **C3-B Phase5 剩余进程态**：对 `Pipeline/Node/Edge/Proposal/History/Schedule/ScheduleRun` 的实际可达 Router 与 Engine 调用逐项加 TenantScope，统一 scoped key，并保证父子查找、执行回调、历史、文件树、预览和 schedule run 不跨 scope。与 `wave_ext` 重复且被注册顺序遮蔽的路由只登记 `NOT_REACHABLE_DUPLICATE`，不借 C3 改公开 route manifest。
- **C3-C 外部后端与机器分类**：机器生成剩余 finding 清单并逐项归类。未配置 Redis、外部队列、离线结果存储时，运行状态明确为 `NOT_CONFIGURED` / `EXTERNAL_UNVERIFIED`；本地 fake 只验证 key/envelope 合同和缺 scope fail-closed，不能替代生产后端验证。进程内执行局部 `queue.Queue` 若不跨请求持久化，登记为 `CONSTANT_EXECUTION_LOCAL`。

C3-A 编码边界冻结为 `routers/wave_ext.py`、`data_os_store.py`、受影响 demo/现有测试以及新增 `tests/tenant_isolation/test_ti5_c3a_job_dlq_scope.py`；不得修改 Phase5 Engine、数据库迁移或公开 DTO 结构。退出门为 capability job 同 ID 双 scope、status 跨 scope 404、DLQ 同 ID双 scope、list/retry 隔离、docintel failure scope envelope、demo purge 不误删其他 scope，并通过相关既有回归。

C3-A 实施结果：`b96eaf2` 已将 capability job 与 DLQ 统一改为 `(org_id,project_id,rid)` key，返回 envelope 固化 `orgId/projectId`；status/list/retry、docintel failure 与 demo seed/purge 均按调用 scope 工作。能力定义继续作为 `PLATFORM_TEMPLATE`。新增 3 个专项场景，相关 19 项通过，Tenant Isolation 222 项收集并全套通过；五分支同 HEAD `b96eaf2` / tree `724edafa...`。C3-A GREEN，下一门 C3-B。

C3-B 代码复核后再拆为两个原子子波：

- **C3-B1 Pipeline Graph/Node/Proposal/History**：`phase5_pipeline_engine.py` 中上述七类容器先处理 Pipeline、Node、Edge、Proposal、History；Engine 所有相关公开方法必须显式接收 TenantScope，Router 每个 handler 必须显式注入 Principal，不以 `APIRouter.dependencies` 代替传 scope。持久化 graph 的 scope 与内存 hydrate key 必须一致；同 pipeline/node/proposal ID 双 scope 可共存。`/v1/pipelines` 的 list/post/detail 等若被 wave_ext 同方法同路径遮蔽，登记为 `NOT_REACHABLE_DUPLICATE`，但 Engine 直接调用和 graph/files/node/proposal/history 等可达子路径仍须完成隔离。
- **C3-B2 Schedule/ScheduleRun/dispatch**：随后处理 Schedule 与 ScheduleRun；给当前无鉴权的 Phase5 schedule Router 增加 Principal 门并传 scope。schedule 只能运行同 scope pipeline；run/history 使用同 scope key。executor 注册表与 evidence resolver 是平台级运行能力，登记 `PLATFORM_TEMPLATE`；本地 `queue.Queue` 是单次 dispatch 局部对象，登记 `CONSTANT_EXECUTION_LOCAL`，但 executor callback 的 pipeline/node 快照必须来自当前 scope。

C3-B1 文件边界冻结为 `phase5_pipeline_engine.py`、`routers/phase5_pipelines.py`、Phase5 pipeline 既有测试和新增 `tests/tenant_isolation/test_ti5_c3b1_phase5_pipeline_scope.py`。不处理 Schedule、Dataset、公开 route manifest 或数据库结构。退出门为五类对象同 ID 双 scope、跨 scope 404/不可见、graph persistence 与内存一致、reset 只清当前 scope、相关既有 Phase5 回归通过。

C3-B 实施时确认 Schedule dispatch 与 Pipeline/Node 快照存在同一调用链，B1 与 B2 不能形成可独立运行的中间版本，因此在一个编译波内共同收口。`bb795dc` 已将七类容器统一为 scoped key，所有 Engine 调用显式 TenantScope，Schedule Router 补 Principal，dispatch 只复制当前 scope 节点；新增 3 个跨 scope 场景。Phase5/执行回归 71 passed，Tenant Isolation 全套通过，全量 9,210 项收集无错误；五分支同 HEAD/tree。C3-B GREEN，下一门 C3-C。

C3-C 文件边界冻结为新增 `tenant_non_postgres_classification.yaml`、对应只读 loader/validator、`tenant_precheck.py` 的未配置状态纠正和专项测试。分类文件必须覆盖 7 个 TI-5 非表资源以及本轮确认的平台模板、重复路由和局部执行队列；每项只允许 `TENANT_OWNED_FIXED/PLATFORM_TEMPLATE/CONSTANT/NOT_REACHABLE/EXTERNAL_UNVERIFIED`，并带代码证据。当前没有 Redis/broker/tenant offline backend 配置时必须分别记录 `NOT_CONFIGURED`，不得启动或连接外部服务；Object/Vector 已有 C1 证据，Scheduler/Process Memory 已有 TI-4/C2/C3 证据。退出门为机器分类 validator、无 scope 合同负向、既有 precheck/registry/migration plan 与 Tenant Isolation 回归通过。

C3-C 实施结果：`56405f1` 新增 12 项机器分类，完整覆盖 7 类 TI-5 非表资源以及 capability/executor 平台模板、局部 dispatch queue 和重复路由；Redis、broker、租户离线存储均明确 `NOT_CONFIGURED`。分类/预检/registry/plan 16 passed，Tenant Isolation 227 项收集并全套通过，全量 9,212 项收集无错误；五分支同 HEAD/tree。外部对象/向量后端继续保留 `EXTERNAL_UNVERIFIED`，不影响本地合同门 GREEN，但仍是 TI-6 生产部署条件。C3 与 TI-5 实施子波全部 GREEN，下一门 D 总收口。

### TI-5 D：总收口

- 全量 schema/resource lint、同 ID 双 scope、跨 scope 负向、无 scope fail-closed。
- PostgreSQL 真实备份、降级、升级与行数/hash 守恒。
- Tenant Isolation 累计回归、五分支同 HEAD/tree、上下文与证据更新。

D 仅做收口验证与机器对账，不再新增业务架构：D1 运行 schema/resource/classification lint、同 ID 双 scope 和无 scope 失败关闭累计门；D2 对 TI-5 PostgreSQL 迁移链执行真实临时库 upgrade/downgrade/upgrade 与共享非生产库只读行数/hash 核对，禁止改写业务数据；D3 执行 Tenant Isolation、全量 collection、必要的 Phase5/AIP 直接回归、五分支同步和文档总对账。若外部后端未配置，只保留生产条件阻断，不得把“未配置”误判为本地合同失败。

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
