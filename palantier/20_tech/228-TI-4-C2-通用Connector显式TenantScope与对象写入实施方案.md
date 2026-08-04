# 228 · TI-4 C2 通用 Connector 显式 TenantScope 与对象写入实施方案

> 版本：v1.0 · 2026-08-04
> 状态：评审通过 / 执行中
> 授权：用户已授权连续完成微商城接入前置；本波不连接具体商城
> 前置：TI-4 C1 GREEN；代码 `m1@ec0d7e7`；Alembic `228ti4c1expand`

## Rules

先方案后代码；复用 TI-1 `TenantScope` 与 `db.connect(scope)`，不另造 Connector 租户模型。只收口现有 REST、File、MySQL、PostgreSQL、SQL Server 通用 ingest 的 scope 传递和 `obj_instance` 写事务，不改变 probe/health，不调用真实平台 API，不回填历史数据，不放宽 Object Runtime RLS，不把客户 scope 塞入 props 冒充数据库隔离。

## 一、现状与根因

Router `POST /v1/connectors/{plugin_id}/ingest` 已从 `Principal` 取得 `org_id/project_id` 并传给 dispatch，但 scope 在下游被丢失：

| 链路 | 当前问题 |
|---|---|
| `rest-generic` / `file-local` | handler 以 `**_` 吞掉 scope，使用 `connect()` owner 路径和旧三列 INSERT |
| `jdbc-postgres` / `jdbc-sqlserver` | runtime wrapper 不向 connector module 透传 scope；mock/live 两条写路径均无 scope |
| `jdbc-mysql` | 只把 org/project 写入 props 标记，数据库连接、列和 conflict target 仍是全局键 |
| 全部 ingest | `ON CONFLICT (object_type, object_id)` 与 TI-3 E7 scoped Contract 不一致 |

TI-3 E6/E7 后，这些 writer 在降权/RLS 下应失败关闭，不能通过 owner/BYPASSRLS 绕过。C2 的目标是让合法带 Principal 的 ingest 恢复为 scoped transaction，同时无 scope 的内部直调继续失败关闭。

## 二、目标 Contract

1. ingest handler 必须显式接收 `org_id/project_id`，立即构造 `TenantScope`；任一缺失、空白或非法值都失败关闭，不使用 `dev-org/dev-project` 默认值。
2. REST/File 在 `connect(scope)` 内写入 `org_id/project_id`；MySQL/PostgreSQL/SQL Server wrapper 把同一个 scope 传到 module。
3. 所有 `obj_instance` 写入固定为五列：`object_type, object_id, props, org_id, project_id`。
4. 所有 upsert 固定使用 `ON CONFLICT (org_id, project_id, object_type, object_id)`；更新只发生在当前 scope。
5. 返回体可以继续提供 `orgId/projectId` 供审计，但 props 不再承担隔离职责；MySQL 既有 `_aosOrgId/_aosProjectId` 仅作兼容审计，不视为授权边界。
6. health/probe 无业务写入，保持现有签名与行为；不强制它们建立数据库 TenantScope。
7. `autoCreateObjectType` 保持默认关闭；C2 不把租户输入自动晋升为平台级 Object Type 模板。

## 三、文件范围

| 文件 | 最小变更 |
|---|---|
| `aos_api/connector_runtime.py` | 统一 scope 构造；REST/File scoped write；向 3 个 JDBC module 透传 scope |
| `aos_api/mysql_connector.py` | require scope；scoped transaction/columns/conflict target |
| `aos_api/pg_connector.py` | mock/live require scope；scoped transaction/columns/conflict target |
| `aos_api/mssql_connector.py` | mock/live require scope；scoped transaction/columns/conflict target |
| `tests/tenant_isolation/test_ti4_c2_connector_scope.py` | 缺 scope 失败关闭、双租户同 ID、5 plugin 路由/静态门 |
| `tests/tenant_isolation/test_ti3_e5_object_runtime_read_switch.py` | deferred writer 集合由 4 收口为 0 |

不新增数据库 migration；C2 复用 TI-3 E7 已冻结的 `obj_instance` Contract。

## 四、验证与退出门

1. 静态扫描 `aos_api` 中 Object Runtime 无 scope writer 为 0；不得只改字符串逃避门禁。
2. REST/File mock 通过 HTTP Principal 写入当前 scope；同 object ID 可在两个 TenantScope 共存，跨 scope 不覆盖。
3. MySQL/PostgreSQL/SQL Server module 直调缺 scope 均失败关闭；mock/live SQL 都包含 scope 列与 scoped conflict target。
4. 运行角色 transaction 设置双 GUC，写后只在当前 scope 可见；无 GUC仍为 0 可见。
5. 既有 Connector 测试、Tenant Isolation 累计测试和相关 API 回归 GREEN。
6. 共享开发库不调用真实上游、不新增业务数据；本波 schema/Alembic revision 保持 `228ti4c1expand`。
7. 五分支同 HEAD/tree，方案、证据、AOS 接续上下文同步。

## 五、回滚

C2 无 schema 迁移。代码回滚恢复为失败关闭的旧 writer，不删除任何对象或外部数据。若验证中写入 synthetic 测试对象，只允许在临时测试数据库中创建和销毁；共享开发库行数必须保持不变。

## 六、风险控制

| 风险 | 等级 | 控制 |
|---|---|---|
| 把 props 中 scope 当安全边界 | P0 | 数据库列、RLS GUC、复合 conflict target 三者同时生效 |
| wrapper 透传但 module 丢失 | P0 | 5 plugin 路由测试 + module 缺 scope 负向测试 |
| 同 ID 跨租户覆盖 | P0 | 固定 scoped conflict target，并做同 ID 双租户断言 |
| owner 绕过 RLS | P0 | 所有业务写事务使用 `connect(scope)`；不得改 `db.connect` 降权规则 |
| 测试误连真实上游 | P0 | 只用 mock/patch；不读取客户 endpoint 或凭据 |
| 自动创建全局 Object Type | P1 | `autoCreateObjectType` 默认关闭；模板治理留给既定 TI-5 边界 |
