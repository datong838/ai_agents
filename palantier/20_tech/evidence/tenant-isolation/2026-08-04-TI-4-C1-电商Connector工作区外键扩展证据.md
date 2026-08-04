# TI-4 C1 电商 Connector 工作区外键扩展证据

> 日期：2026-08-04
> 结论：GREEN
> 代码：`aos-platform m1@ec0d7e7`
> Alembic：`228ti4c1expand`

## 1. 实施边界

本波只为 `ecom_ingest_receipt`、`ecom_link`、`ecom_object`、`ecom_sync_checkpoint`、`oauth_token_store` 增加 `(org_id, workspace_id) → twa_workspace(org_id, project_id)` 的 NOT VALID 外键。未连接任何真实电商平台，未读取凭据，未写客户数据，未启用 RLS，也未放开通用 Connector ingest。

## 2. 数据与结构结果

| 检查项 | 结果 |
|---|---|
| 共享库实施前行数 | 5 表均 0 |
| 共享库实施后行数 | 5 表均 0 |
| scope NOT NULL | 5/5 |
| TenantScope 复合主键 | 5/5 |
| workspace alias FK | 5/5 |
| FK validated | 0/5，符合 C1 Expand 门 |
| 业务 DML | 0 |

迁移仅新增或删除 5 个具名 FK；`workspace_id` 保持为 canonical `project_id` 的电商域字段别名，没有引入第三套租户身份。

## 3. 可逆性

- 备份：`/private/var/tmp/aos-ti4-c1.RBwlKq/aos-meta-before.dump`
- 大小：1,804,660 bytes；权限：0600
- SHA-256：`2f3ca029d3d926b430f46fa3ea31eb564d0eb8954b553aca7a80334894f7d258`
- `pg_restore -l`：GREEN
- 真实共享库：`upgrade head → downgrade 228ti3e7contract → upgrade head` GREEN
- 最终 revision：`228ti4c1expand`

## 4. 验证结果

| 验证 | 结果 |
|---|---|
| C1 专项 | 3 passed |
| Tenant Isolation 累计 | 126 passed、8 skipped、零失败 |
| schema lint | `ok=true`；无 invalid scope/PK/FK |
| 分支同步 | m1、w1、w2、w3、w4 均为 `ec0d7e7` |
| tree | `7ee529506caf2559b7a97a45899c2454a184d115` |

## 5. 未解除的门禁

4 个代码文件中的通用 Object ingest writer 仍丢失 scope，并因 Object Runtime RLS/Contract 失败关闭。C2 必须让 REST/File/MySQL/PostgreSQL/MSSQL 从 Router Principal 到数据库 transaction 全程携带 TenantScope，并把 conflict target 切到 scoped key；在此之前不得把 C1 描述为 Connector 已可接入。
