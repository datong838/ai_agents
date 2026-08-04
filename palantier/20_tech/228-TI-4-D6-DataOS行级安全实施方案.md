# 228 · TI-4 D6 Data OS 行级安全实施方案

> 版本：v1.0 · 2026-08-04
> 状态：评审授权链内，待执行
> 前置：TI-4 D5 GREEN；代码 `m1@2b81a1b`；Alembic `228ti4d4validate`

## Rules

复用既有降权角色 `aos_runtime` 与 transaction-local `aos.org_id/aos.project_id`。7 表统一 `FOR ALL ... USING ... WITH CHECK`，ENABLE + FORCE；不为迁移创建新角色，不改 297 条业务行，不授予 runtime 对 D3 控制账本或隔离记录的访问。

## 1. 范围

`meta_source`、`meta_pipeline`、`meta_dataset`、`meta_dataset_history`、`meta_sync`、`meta_schedule`、`phase5_pipeline_graph`。

新 revision `228ti4d6rls`，down revision `228ti4d4validate`。每表 policy 名 `tenant_scope_<table>_ti4`，表达式精确匹配两个 GUC。Downgrade 只 drop policy、NO FORCE、DISABLE RLS。

## 2. 验证

- runtime role + scope A 只能读写 A；scope B 看不到 A。
- `connect()` 后手动 `SET LOCAL ROLE aos_runtime` 且无 GUC 时 7 表零可见，写入失败。
- WITH CHECK 阻止 scope A transaction 写 scope B 或 NULL。
- 连接归还后 role/GUC 不泄漏。
- 真实 `D4 → D6 → D4 → D6` 往返，7/7 policy 与 ENABLE/FORCE 状态可逆；297/293/293 守恒。

## 3. 退出门

- 7/7 表 ENABLE + FORCE；7 个 policy 定义、角色和 USING/WITH CHECK 正确。
- `aos_runtime` 非 superuser、非 bypassrls、不是目标表 owner。
- 无 GUC零可见；跨 scope 与伪造写失败关闭；quarantine 默认不可见。
- D6 专项与 Tenant Isolation 累计 GREEN；五分支、证据和上下文同步。

## 4. 后续边界

D6 后仍有全局主键、nullable scope 和 runtime bootstrap DDL。下一门 D7 必须把 293 条未知历史从活跃表物理移入不可变维护隔离区，随后冻结 scope NOT NULL、复合主键/唯一与父子复合 FK，并把 Data OS 建表真源收归 Alembic。完成 D7 前不得开始具体微商城 Connector。
