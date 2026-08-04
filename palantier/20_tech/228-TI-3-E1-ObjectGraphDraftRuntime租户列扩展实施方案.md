# 228 · TI-3 E1 Object/Graph/Draft Runtime 租户列扩展实施方案

> 版本：v1.0 · 2026-08-04
> 状态：连续执行授权下评审通过 / 待实施
> 前置：TI-2 E1～E7 GREEN；代码 `m1@4004170`；共享库 `228ti2e7contract`

## Rules

先 Expand、后双写/回填/读切换/RLS/Contract。E1 只增加 nullable TenantScope 列、NOT VALID 关系和只读 lint，不推断历史归属，不改运行时 SQL，不把既有对象默认认领给测试组织或栖月汇。平台模板 `meta_action_type/meta_link_type/meta_object_type` 保持共享，不加租户列。

## 唯一资源范围

范围只来自 `tenant_resources.yaml.executionPlan` 的三个 TI-3 group：

1. `ti3-ontology-templates`：3 张平台模板表，仅复核、不迁移。
2. `ti3-object-graph`：`funnel_status`、`graph_edge`、`meta_branch`、`obj_branch_overlay`、`obj_instance`、`object_lifecycle`。
3. `ti3-draft-wiki`：`draft_dataset`、`wiki_page`、`wiki_page_version`。

当前 9 张租户资源实库行数为：Draft 925、Funnel 1、Graph 2、Branch 3、Overlay 0、Object 31、Lifecycle 2、Wiki 1、Wiki Version 65。前 5 张及 `obj_instance` 没有 TenantScope；后三张 Draft/Wiki 与 Lifecycle 已有 scope，但主键仍未包含 scope。

## E1 变更

- 对 `funnel_status/graph_edge/meta_branch/obj_branch_overlay/obj_instance` 增加 nullable `org_id/project_id`。
- 9 张租户资源均增加 `(org_id, project_id) → twa_workspace(org_id, project_id)` 的 NOT VALID FK；现有行不回填、不 Validate。
- 保留全部旧主键、唯一约束、默认值和运行路径；不启用 RLS。
- 将资源注册表现状更新为 E1 Expand：新增列存在，但 PK 状态仍为 WEAK_PK；不得宣称运行隔离完成。
- 新增 TI-3 E1 schema lint：revision、列、nullable 规则、9 个 FK 存在且未验证、模板表无租户列、行数守恒。

## 文件范围

| 文件 | 动作 |
|---|---|
| `alembic/versions/228ti3e1_object_expand.py` | 5 表 nullable scope、9 个 NOT VALID FK、可逆 downgrade |
| `aos_api/tenant_resources.yaml` | 5 个 NO_TENANT 资源更新为带列 WEAK_PK；executionPlan 不变 |
| `aos_api/tenant_schema_lint.py` | TI-3 E1 只读报告 |
| `tests/tenant_isolation/test_ti3_e1_object_expand.py` | 迁移、实库 lint、模板不变、行数守恒与升降级门 |

## 备份与 Precheck

升级前使用 PostgreSQL 16 匹配版本完整备份，记录大小/SHA-256/权限。记录 9 表行数、列、主键、现有 FK、scope 分布与三张模板表结构；任何未登记表、同名迁移 head 或 DDL 漂移均阻断。

## 回滚

E1 downgrade 先删除 9 个 NOT VALID FK，再删除 5 表新增 nullable 列。因 E1 不写历史 scope、不切运行路径，降级应保持所有行和旧主键不变。若后续波次已写入这些列，降级必须由 Alembic 顺序先退回 E1，禁止直接删列。

## 退出门

1. 9 张租户资源行数逐表守恒，3 张模板表结构不变。
2. 5 张原无租户表新增 nullable org/project；Draft/Wiki/Lifecycle 既有 NOT NULL scope 不放宽。
3. 9 个 FK 均存在且 `convalidated=false`；RLS 不新增。
4. Alembic `upgrade → downgrade → upgrade` GREEN，最终 revision `228ti3e1expand`。
5. TI-3 E1 专项、既有 Tenant Isolation、Object/Graph/Draft/Wiki 回归 GREEN。
6. 五分支同步后才进入 TI-3 E2 显式 TenantScope；E1 不授权历史回填或具体商城接入。
