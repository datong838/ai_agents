# 228 · TI-4 C3 电商 Connector 数据库 Contract 与行级安全实施方案

> 版本：v1.0 · 2026-08-04
> 状态：GREEN（2026-08-04）
> 前置：TI-4 C1/C2、D1～D7 GREEN；代码 `m1@c890a7a`；Alembic `228ti4d7contract`

## Rules

不新增具体商城字段、API 或业务映射，只收口现有通用电商 Connector 真源表。保持 5 表既有 scoped 主键、对象关系、幂等/CAS 与 OAuth 加密契约；先验证空表和 workspace FK，再启用 FORCE RLS。所有 SQLAlchemy、psycopg 与后台 refresh 路径必须在事务内显式 TenantScope、降权角色与双 GUC，禁止 owner 全表扫描。

## 1. 范围与现状

目标表：`ecom_ingest_receipt`、`ecom_link`、`ecom_object`、`ecom_sync_checkpoint`、`oauth_token_store`。

- 5 表均为 0 行，`org_id/workspace_id` 非空且主键已包含完整 scope。
- C1 已建 5 个 `NOT VALID` workspace alias FK；当前均未 Validate。
- 5 表当前 RLS/Force 均关闭。
- `EcomConsistencyStore` 查询本身带 scope，但 SQLAlchemy transaction 仍以 owner 执行，未设置 GUC/降权角色。
- `PostgresOAuthTokenStore` 使用无 scope `connect()`；`list_due(before)` 是全表扫描，无法在 RLS 后安全运行。

## 2. 目标 Contract

1. 5 个 workspace FK 全部 Validate；空表 orphan=0。
2. 5 表分别建立 `tenant_scope_<table>_ti4c3`，谓词为 `org_id=aos.org_id AND workspace_id=aos.project_id`，同时 `USING/WITH CHECK`、ENABLE/FORCE。
3. `EcomConsistencyStore` 每个 read/write transaction 在执行首条业务 SQL 前 `SET LOCAL ROLE aos_runtime` 并设置双 GUC；scope 来源只能是 BatchCommand、StorageIdentity 或显式 list 参数。
4. `PostgresOAuthTokenStore` 的 get/put/delete 使用 `TenantScope.from_workspace()`；`list_due` 改为显式 scope，`OAuthTokenManager.refresh_due` 同样要求 scope，后台调度必须按租户 fan-out，不允许全表 refresh。
5. In-memory OAuth Store 保持同一接口并按 scope 筛选，避免测试环境掩盖生产边界。

## 3. 实施拆分

### C3-A Migration

- 新 revision `228ti4c3contract`，down revision `228ti4d7contract`。
- 对 5 个 workspace FK 做 orphan precheck 后 Validate。
- 创建 5 个 policy 并 ENABLE/FORCE；downgrade 撤销 policy/RLS，并以 drop/re-add `NOT VALID` 的方式恢复 C1 前态，业务行不变。

### C3-B Runtime transaction

- 为 SQLAlchemy Connection 增加最小 transaction-local scope helper，不改 Store 业务算法。
- apply/get/checkpoint/list links 全路径调用 helper；无 scope 参数的入口不存在。
- OAuth psycopg 路径改用 canonical TenantScope；due refresh 改成 scope-required。

### C3-C 验证

- scope A/B 同 external ID 共存，读写互不可见；伪造 scope、无 GUC写入失败。
- 5/5 FK validated，5/5 policy、ENABLE/FORCE 生效。
- OAuth scope A 的 get/list_due/delete 不影响 B；manager refresh 只处理目标 scope。
- 真实 `D7→C3→D7→C3` 往返，5 表行数 0 守恒。
- Ecom/OAuth/Connector/Tenant Isolation 累计回归 GREEN，五分支同步。

## 4. 退出门与风险

- 运行角色不是表 owner、无 BYPASSRLS；无 GUC零可见，WITH CHECK 拒绝伪造。
- 不存在 owner 业务 transaction 或全局 OAuth due scan。
- 既有幂等、checkpoint CAS、对象/Link FK、token version/encryption 语义不变。
- 本波仍不调用微信小店、微商城、抖音等真实 API，不读取真实凭据。
- C3 GREEN 后 TI-4 才可总收口；下一执行域为 TI-5 AIP/Analytics 与非数据库资源隔离。

## 5. 实施结论

- 代码提交：`6feb1cb`；Alembic 最终 revision：`228ti4c3contract`。
- 5/5 workspace FK 已验证，5/5 表均 ENABLE/FORCE RLS，运行角色安全且不拥有表。
- SQLAlchemy 一致性存储、PostgreSQL OAuth Store 与到期刷新均已显式绑定 TenantScope；无 GUC 零可见，跨 scope 写失败关闭。
- 专项定向 46 passed；Tenant Isolation + Ecom/OAuth 累计 209 passed / 11 skipped。
- 共享库 `D7→C3→D7→C3` 往返、5 表 0 行守恒；五个代码分支本地/远端均指向 `6feb1cb`，tree `3bdf778a...`。
- 未接入任何具体商城、未使用真实凭据或客户数据；Data OS/Connector 收口，TI-4 全域还需完成注册表中的 `ti4-async-runtime`。
