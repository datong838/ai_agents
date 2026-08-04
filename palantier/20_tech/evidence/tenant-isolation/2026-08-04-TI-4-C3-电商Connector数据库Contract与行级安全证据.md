# TI-4 C3 电商 Connector 数据库 Contract 与行级安全证据

> 日期：2026-08-04  
> 结论：GREEN  
> 代码：`m1@6feb1cb`，tree `3bdf778af9a36c4e1c045afc29861ab74c088219`  
> 数据库：`228ti4c3contract`

## 1. 交付

- 迁移 `228ti4c3contract` 对 5 张电商真源表执行 orphan precheck、workspace FK Validate、ENABLE/FORCE RLS。
- 5 个 policy 同时使用 `org_id=aos.org_id` 与 `workspace_id=aos.project_id` 的 USING/WITH CHECK。
- `EcomConsistencyStore` 的 apply/get/checkpoint/link transaction 在 PostgreSQL 下使用 `aos_runtime` 和事务级双 GUC。
- `PostgresOAuthTokenStore` 的 get/put/delete/list_due 使用 canonical TenantScope；manager 到期刷新必须显式传入目标租户。

## 2. 数据库验证

| 验证项 | 结果 |
|---|---|
| Workspace FK | 5/5 存在且 validated |
| RLS | 5/5 ENABLE，5/5 FORCE |
| Policy | 5/5 名称、角色、双 GUC、USING/WITH CHECK 正确 |
| Runtime Role | 无 LOGIN、SUPERUSER、BYPASSRLS；不拥有目标表 |
| 负向门 | scope A/B 互不可见；无 GUC 零可见；伪造 scope 写入拒绝 |
| 业务行 | 5 张目标表均为 0；未写真实商城或客户数据 |

只读 schema report：`stage=TI-4-C3`、`ok=true`、`issues=[]`。

## 3. 可逆与备份

- 共享非生产执行 `228ti4d7contract → 228ti4c3contract → 228ti4d7contract → 228ti4c3contract`，最终回到 C3。
- downgrade 后 5 个 FK 恢复 NOT VALID，5 表 RLS/policy 撤销；upgrade 后完整恢复，逐表行数保持 0。
- Git 外备份：`/private/var/tmp/aos-ti4-c3.rc7XZr/aos-meta-before.dump`，1,888,983 bytes，权限 `0600`。
- SHA-256：`7fdfc36c4df2ae415c190c4e2a81a331676d7ae9ec9fee45bc6e4418aad03098`。

## 4. 回归

- C3/Ecom/OAuth/D7 定向：46 passed。
- Tenant Isolation + Ecom migration/store + OAuth：209 passed / 11 skipped。
- Ruff 与 diff check：GREEN。
- 既有 Phase5 seed 的历史环境问题不计入本波结论；本波未修改其业务逻辑。

## 5. 分支与结论

`m1`、w1、w2、w3、w4 本地与远端均指向 `6feb1cb`，tree 完全一致；四个 worker clean，主工作树仅保留用户 `docs/toutiao-series` 改动且未夹带。

TI-4 Data OS 与 Connector 已总收口。此结论只证明通用隔离底座，不代表已接入微信小店、微商城、抖音或任何真实平台；下一执行域为 TI-5。
