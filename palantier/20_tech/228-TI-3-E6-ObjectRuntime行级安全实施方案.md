# 228 · TI-3 E6 Object Runtime 行级安全实施方案

> 版本：v1.0 · 2026-08-04
> 状态：执行中
> 前置：TI-3 E5 `3d53105` GREEN；共享库 `228ti3e4validate`；1,030/37/0 守恒

## Rules

复用 TI-2 已建立的 `aos_runtime` 降权角色和 transaction-local `aos.org_id/aos.project_id`，不创建第二套租户角色。E6 只为 9 张 Object Runtime 工作区表建立 `FOR ALL` RLS policy 并 ENABLE/FORCE；不改业务行、主键、NULL quarantine、API 或 OpenAPI。无 GUC 零可见/零可写，WITH CHECK 对伪造 scope 失败关闭。

## RLS 清单

- `funnel_status`
- `graph_edge`
- `meta_branch`
- `obj_branch_overlay`
- `obj_instance`
- `object_lifecycle`
- `draft_dataset`
- `wiki_page`
- `wiki_page_version`

每表 policy 名为 `tenant_scope_{table}_ti3`，表达式同时要求：

```sql
org_id = current_setting('aos.org_id', true)
AND project_id = current_setting('aos.project_id', true)
```

## 边界与已知阻断

- `connect(TenantScope)` 已由 TI-2 E6 先 `SET LOCAL ROLE aos_runtime` 再设置 GUC，E6 直接复用。
- 37 条 NULL scope 行在运行角色下自然不可见，也不能被 scope 写回；维护 owner 仅用于审批后的离线治理。
- 4 个 Connector writer 仍通过无 scope owner 连接写 `obj_instance`，属于 TI-4 明确阻断项；E6 不把它们冒充受 RLS 保护，也不解除真实平台连接暂停。
- Platform template 表不启用租户 RLS；`decision_lineage` 等 TI-5 资源不在本波扩大范围。

## 实现范围

| 文件 | 动作 |
|---|---|
| `alembic/versions/228ti3e6_object_runtime_rls.py` | 9 表 policy、ENABLE/FORCE、可逆 downgrade |
| `aos_api/tenant_schema_lint.py` | E6 revision、角色/表/policy 只读报告 |
| `tests/tenant_isolation/test_ti3_e6_object_runtime_rls.py` | DDL、跨 scope、WITH CHECK、无 GUC、上下文不泄漏 |
| `tests/tenant_isolation/test_ti3_e4_object_runtime_fk_validate.py` | 历史 E4 往返后恢复最新 head，保持累计门稳定 |

## 回滚

`downgrade` 逐表 DROP TI-3 policy、NO FORCE、DISABLE RLS；保留共享 `aos_runtime` 角色及 TI-2 policy，避免破坏其他资源族。E4 validated FK 与业务数据不回退。真实库执行前备份，完成 upgrade/downgrade/upgrade 与行数/hash 守恒。

## 退出门

1. `aos_runtime` 仍为 NOLOGIN/NOSUPERUSER/NOBYPASSRLS，且不是 9 表 owner。
2. 9/9 表 ENABLE+FORCE，每表恰有目标 policy，USING/WITH CHECK 均含双 GUC。
3. scope A 只能读写 A；B 看不到 A；伪造 B payload 被 WITH CHECK 拒绝。
4. 运行角色无 GUC 时 9 表可见 0、写入拒绝；事务后 role/GUC 不泄漏。
5. 37 条 quarantine 在 runtime 零可见；共享库 upgrade/downgrade/upgrade 后 1,030/37/0 守恒。
6. Tenant Isolation 累计 GREEN，五分支同步；下一门 TI-3 E7 Contract。
7. E6 GREEN 不代表 4 个 Connector writer 或真实微商城已可接入。
