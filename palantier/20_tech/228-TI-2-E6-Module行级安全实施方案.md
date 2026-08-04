# 228 · TI-2 E6 Module 行级安全实施方案

> 版本：v1.0 · 2026-08-04
> 状态：评审通过 / 执行中
> 前置：TI-2 E5 `8aee9f6` GREEN；共享库 Alembic `228ti2e4validate`

## Rules

先方案后代码；RLS 是显式 TenantScope 之后的数据库第二道边界，不替代 Router 鉴权、Store scope 或 E5 module_pk。只覆盖 TI-2 Module 实例族 11 张表；不扩展到全库，不改业务行、主键或 API。无租户 GUC 必须零可见/零可写；运行时不得以 table owner、superuser 或 BYPASSRLS 身份执行租户 DML。

## 现状判定

共享开发库当前连接角色 `aos_app` 同时是 table owner、superuser 且 `rolbypassrls=true`。仅执行 `ENABLE/FORCE ROW LEVEL SECURITY` 对该角色不构成真实边界。因此 E6 必须同时完成最小运行角色分离：

- Alembic/维护连接继续使用 owner 角色，负责 DDL、备份和经批准的离线操作；
- 带 `TenantScope` 的应用连接在事务内 `SET LOCAL ROLE aos_runtime`，再设置 `aos.org_id/aos.project_id`；
- `aos_runtime` 为 `NOLOGIN NOSUPERUSER NOBYPASSRLS`，不是表 owner，仅获 Module 族最小 DML 权限；
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

`aos_runtime` 只授予 `public` schema USAGE 以及上述 11 表的 SELECT/INSERT/UPDATE/DELETE；不授予 CREATE、TRUNCATE、REFERENCES、TRIGGER 或角色管理。E6 downgrade 删除 11 个 policy 并 DISABLE/FORCE OFF，但保留无登录运行角色及其最小 grant，避免全局角色 DROP 误伤其他数据库/并发会话；代码回滚同时撤销 scoped connection 的 `SET LOCAL ROLE`。E3 身份和 E4 FK 均不回退。

## 退出门

1. 真实 `aos_runtime` 为 NOSUPERUSER/NOBYPASSRLS/NOLOGIN，11 表 owner 均不是该角色。
2. 11/11 表 RLS enabled + forced，每表恰有目标 policy，USING/WITH CHECK 均引用正确 GUC。
3. scope A 只能读写 A；scope B 看不到 A；伪造 payload 中 B scope 被 WITH CHECK 拒绝。
4. 切到运行角色但不设 GUC时 11 表读取为 0、写入拒绝；事务结束后角色与 GUC 不泄漏。
5. `upgrade → downgrade → upgrade` 可逆，行数/身份 hash 不变，栖月汇 Module 0。
6. Tenant Isolation + Workshop 累计 GREEN，五分支同步后进入 E7 Contract；APP-04/05 仍不得提前标绿。
