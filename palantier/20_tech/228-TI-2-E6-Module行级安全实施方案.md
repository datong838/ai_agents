# 228 · TI-2 E6 Module 行级安全实施方案

> 版本：v1.1 · 2026-08-04
> 状态：GREEN
> 前置：TI-2 E5 `8aee9f6` GREEN；共享库 Alembic `228ti2e4validate`

## Rules

先方案后代码；RLS 是显式 TenantScope 之后的数据库第二道边界，不替代 Router 鉴权、Store scope 或 E5 module_pk。只覆盖 TI-2 Module 实例族 11 张表；不扩展到全库，不改业务行、主键或 API。无租户 GUC 必须零可见/零可写；运行时不得以 table owner、superuser 或 BYPASSRLS 身份执行租户 DML。

## 现状判定

共享开发库当前连接角色 `aos_app` 同时是 table owner、superuser 且 `rolbypassrls=true`。仅执行 `ENABLE/FORCE ROW LEVEL SECURITY` 对该角色不构成真实边界。因此 E6 必须同时完成最小运行角色分离：

- Alembic/维护连接继续使用 owner 角色，负责 DDL、备份和经批准的离线操作；
- 带 `TenantScope` 的应用连接在事务内 `SET LOCAL ROLE aos_runtime`，再设置 `aos.org_id/aos.project_id`；
- `aos_runtime` 为 `NOLOGIN NOSUPERUSER NOBYPASSRLS`，不是表 owner；因当前所有已隔离 Store 统一复用 `connect(scope)`，且部分 legacy `ensure_schema()` 会在迁移后动态建表，它获得 public 表普通 DML 与 sequence 使用权及同类默认权限，但没有 DDL、TRUNCATE、REFERENCES、TRIGGER或角色管理；
- 无 scope 的连接不自动切运行角色，不得作为 HTTP 业务路径使用。

## RLS 清单

工作区级 10 表使用 `(org_id, project_id)` policy：

- `meta_module`
- `module_canvas_config`
- `module_deployment`
- `module_events`
- `module_interface`
- `module_query`
- `module_variable`
- `module_widget_instance`
- `module_instance_overlay`
- `module_user_view_preference`

组织级 `module_organization_profile` 只比较 `org_id`。所有 policy 均为 `FOR ALL`，同时定义 `USING` 与 `WITH CHECK`；`current_setting(..., true)` 缺失时返回 NULL，表达式不成立并失败关闭。11 表均 `ENABLE` 且 `FORCE ROW LEVEL SECURITY`。

## 实现范围

| 文件 | 变更 |
|---|---|
| `alembic/versions/228ti2e6_module_rls.py` | 创建/授权最小运行角色；11 表 policy；ENABLE/FORCE；可逆 downgrade |
| `aos_api/tenant_scope.py` | scoped transaction 先 `SET LOCAL ROLE aos_runtime`，再写 transaction-local GUC |
| `aos_api/tenant_schema_lint.py` | E6 schema report：角色属性、11 表 ENABLE/FORCE、policy 形态与最终 revision |
| `tests/tenant_isolation/test_ti2_e6_module_rls.py` | DDL 静态门、真实角色切换、无 GUC/跨租户/写入负向、降级形态 |
| `tests/conftest.py` | 测试身份准备使用明确 scope，避免无 GUC 维护 DML冒充业务路径 |

## 权限与回滚

`aos_runtime` 授予 `public` schema USAGE、表 SELECT/INSERT/UPDATE/DELETE 与 sequence USAGE/SELECT；同样的 `ALTER DEFAULT PRIVILEGES` 只由迁移 owner 配置，以兼容 Theme/Widget 等迁移后动态建表。运行角色自身不拥有 ALTER DEFAULT PRIVILEGES、CREATE、TRUNCATE、REFERENCES、TRIGGER 或角色管理能力。默认 DML grant 不是默认隔离证明：任何新 tenant-owned 表仍必须注册、显式 TenantScope 并在对应 E6 波加入 RLS policy，否则资源覆盖门不得 GREEN。E6 仅对上述 11 张 Module 表建立 policy。downgrade 删除 11 个 policy 并 DISABLE/FORCE OFF，但保留无登录运行角色及其 grant，避免全局角色 DROP 误伤其他数据库/并发会话；代码回滚同时撤销 scoped connection 的 `SET LOCAL ROLE`。E3 身份和 E4 FK 均不回退。

## 退出门

1. 真实 `aos_runtime` 为 NOSUPERUSER/NOBYPASSRLS/NOLOGIN，11 表 owner 均不是该角色。
2. 11/11 表 RLS enabled + forced，每表恰有目标 policy，USING/WITH CHECK 均引用正确 GUC。
3. scope A 只能读写 A；scope B 看不到 A；伪造 payload 中 B scope 被 WITH CHECK 拒绝。
4. 切到运行角色但不设 GUC时 11 表读取为 0、写入拒绝；事务结束后角色与 GUC 不泄漏。
5. `upgrade → downgrade → upgrade` 可逆，行数/身份 hash 不变，栖月汇 Module 0。
6. Tenant Isolation + Workshop 累计 GREEN，五分支同步后进入 E7 Contract；APP-04/05 仍不得提前标绿。

## 执行结果

- 代码 `846b49a`；m1 与四 Worker 本地/远端同步。
- 新增 `aos_runtime`：NOLOGIN/NOSUPERUSER/NOBYPASSRLS/非 owner；scoped transaction 先 `SET LOCAL ROLE` 再设置 GUC。
- 11 张 Module 实例表全部 ENABLE+FORCE RLS，每表一个 `FOR ALL` USING/WITH CHECK policy；10 表 org+project，Profile 仅 org。
- 为兼容迁移后动态 `ensure_schema()`，迁移 owner 给现有及未来 public 表/sequence 配置普通运行 DML 默认 grant；运行角色无 DDL/角色能力，新 tenant 表仍必须另过注册/RLS门。
- 共享库完成 upgrade/downgrade/upgrade 多轮演练；降级 policy/RLS=0，最终 Alembic `228ti2e6rls`。
- 无 GUC运行角色可见 0；测试工作区可见 159，owner 总量 160；跨 scope 与 WITH CHECK 负向 GREEN。
- 专项 12 passed；Tenant Isolation + Workshop 累计 134 passed，7 个既有 warning。
- 备份：`/private/var/tmp/aos-ti2-e6.WHDDpN/aos-meta-before.dump`，1,615,403 bytes，mode 600，SHA-256 `91c573644ce17a6c25f57db4dc697c5e0dd29c482cc38a960cdcfdb9f24ea4a3`。
