# 228 · TI-4 C1 电商 Connector 工作区外键扩展实施方案

> 版本：v1.1 · 2026-08-04
> 状态：GREEN
> 授权：用户已明确授权连续执行至具备接入微商城的前期条件；本波仍不连接具体商城
> 前置：TI-3 E1～E7 GREEN；代码 `m1@fd2a124`；Alembic `228ti3e7contract`

## Rules

先方案后代码；严格按 `tenant_resources.yaml.executionPlan` 的 `ti4-connectors → ti4-data-os → ti4-async-runtime` 顺序执行。C1 只补齐现有通用电商 Connector 数据面的 workspace 关系，不重设计 `EcomConsistencyStore`，不调用真实平台 API，不写客户数据，不启用 RLS，不修改 4 个 Object ingest writer。`workspace_id` 继续是电商域对 canonical `project_id` 的字段别名，禁止复制第三套租户身份。

## 一、现状

`ecom_object`、`ecom_link`、`ecom_sync_checkpoint`、`ecom_ingest_receipt`、`oauth_token_store` 已具备：

- `org_id/workspace_id` NOT NULL；
- TenantScope 复合主键；
- Store 查询和 mutation 显式约束 `org_id/workspace_id`；
- 当前共享开发库 5 表均为 0 行。

但 5 表尚未建立到 `twa_workspace(org_id, project_id)` 的父关系，也未启用 RLS。`workspace_id` 目前只有代码语义，没有数据库父级完整性门。另有 `connector_runtime.py`、`mysql_connector.py`、`pg_connector.py`、`mssql_connector.py` 的 Object ingest 虽已从 Router 收到 `org_id/project_id`，下游 handler 仍丢弃 scope，并使用旧全局 conflict target；它们由 C2 显式 TenantScope 波处理，C1 不混做。

## 二、目标

1. 为以下 5 表新增 NOT VALID workspace FK：

```text
(org_id, workspace_id)
  -> twa_workspace(org_id, project_id)
```

2. FK 名称固定为 `fk_<table>_workspace_ti4`，便于后续 Validate、lint 和回滚。
3. 只执行结构 Expand，不修改业务行、不启用/强制 RLS、不改变主键和外部 DTO。
4. schema lint 明确报告 5 表 scope、复合 PK、workspace alias FK 和当前未 Validate 状态。
5. 为 C2 冻结边界：4 个通用 Object ingest writer 仍必须失败关闭，下一波才把 Router Principal scope 传到底层 transaction。

## 三、文件范围

| 文件 | 变更 |
|---|---|
| `alembic/versions/228ti4c1_ecom_workspace_expand.py` | 5 个 NOT VALID workspace alias FK，可逆 downgrade |
| `aos_api/tenant_schema_lint.py` | TI-4 C1 revision、PK/scope/FK/validated 状态报告 |
| `tests/tenant_isolation/test_ti4_c1_ecom_workspace_expand.py` | migration 静态边界、实库 lint、行数守恒、升降级 |
| 总方案、证据、AOS 上下文 | 完成后记录状态、验证、分支和下一波 |

## 四、迁移与回滚

升级仅执行 5 条 `ALTER TABLE ... ADD CONSTRAINT ... NOT VALID`。由于共享库 5 表为空，不存在业务 DML；仍保持 NOT VALID，以遵守 E1→E4 分门规则。降级只删除这 5 个具名 FK，不删除表、索引、token、对象、receipt 或 checkpoint。

任何表缺少目标复合 PK、scope 非空列或 `twa_workspace` 唯一父键时，precheck/schema lint 失败，不自动修复。`workspace_id` 不改名，避免破坏现有 Ecom DTO 与 OAuth Store；映射关系只由 FK 和 TenantScope adapter 固化。

## 五、退出门

1. 共享库 precheck：5 表总行数 0，scope NOT NULL 5/5，目标复合 PK 5/5。
2. 迁移 `upgrade → downgrade → upgrade` GREEN，5 表行数与 schema hash 守恒。
3. 最终 5 个 `fk_*_workspace_ti4` 存在且 `validated=false`；Alembic `228ti4c1expand`。
4. Tenant Isolation 累计 GREEN；不新增共享库测试数据。
5. 五分支同 HEAD/tree，证据与 AOS 项目开发上下文同步。
6. C1 GREEN 不代表 Connector 可 ingest；4 writer 继续失败关闭，下一波为 C2 Connector 显式 TenantScope 与 scoped transaction。

## 六、风险

| 风险 | 等级 | 控制 |
|---|---|---|
| 把 `workspace_id` 当独立租户层 | P0 | 固定映射到 `twa_workspace.project_id`，不新增身份真源 |
| 空表直接 Validate/RLS 越级 | P1 | C1 只 NOT VALID Expand，后续逐门验证 |
| 误把 Strong PK 等同全隔离 | P0 | 状态明确 RLS=0、parent FK 缺失、writer scope 丢失 |
| 提前连接微商城 | P0 | 不读取凭据、不调用 API、不新增平台 adapter/业务 schema |

## 七、实施结果

- 代码基线由 `fd2a124` 前移至 `ec0d7e7`；最终 Alembic revision 为 `228ti4c1expand`。
- 5 张电商表均已建立具名 NOT VALID workspace alias FK，最终 `validated=false` 5/5；原有 TenantScope 复合主键与 NOT NULL 未改变。
- 共享开发库 5 表实施前后均为 0 行；本波业务 DML=0，未写入 token、对象、receipt 或 checkpoint。
- 已完成真实 `upgrade → downgrade 228ti3e7contract → upgrade` 往返；备份可列举恢复，迁移可逆。
- 专项测试 3 passed；Tenant Isolation 累计 126 passed、8 skipped、零失败。
- 五个代码分支和远端均同步到 `ec0d7e7`，tree `7ee529506caf2559b7a97a45899c2454a184d115`。
- C1 仅完成结构 Expand。Connector ingest 仍失败关闭；下一波为 C2，把 Principal TenantScope 传到 REST/File/MySQL/PostgreSQL/MSSQL 的 Object transaction。
