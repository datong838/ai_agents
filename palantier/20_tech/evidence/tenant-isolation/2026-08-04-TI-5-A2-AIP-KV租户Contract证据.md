# TI-5 A2 AIP KV 租户 Contract 证据

> 日期：2026-08-04
> 结论：GREEN
> 代码：`30137dd`，tree `3a7fe1f15be1a208205376bd89221405d665eecc`

## 1. 实施结果

- `228ti5a2kv` 将 `meta_aip_kv` 收归 Alembic，冻结 `(org_id, project_id, key)` 复合主键、workspace FK、scope NOT NULL 和 ENABLE/FORCE RLS。
- 共享非生产库的 23 条历史 KV 仅按冻结 key 清单与用户明确的测试数据定性归属 `dev-org/dev-project`；未读取 payload 猜测。
- `aip_kv_ownership_ledger` 只保存 key 及 payload hash 等审计信息，不复制业务 payload；清单外的无 scope 数据失败关闭。
- KV Store 生产连接使用 `db_connect(TenantScope)`，路由 Principal 在整个请求生命周期绑定 canonical ContextVar；无请求或无任务 envelope 时失败关闭。
- 降级遇到跨 scope 同 key 时会阻断，不允许静默覆盖。

## 2. 数据库与可逆性

- 前置 Git 外备份：`/private/var/tmp/aos-ti4-a1.Tp6Zb6/aos-meta-before.dump`，SHA-256 `883e668cbde3b2d0fa255fd51a6e598a8b6c243d6d4c31cdacb8d3d4f22ea7bd`。
- 共享库执行 `228ti5a1aip → 228ti5a2kv → 228ti5a1aip → 228ti5a2kv`。
- 往返前后 `meta_aip_kv=23`，最终 ownership ledger=23，全部为 `dev-org/dev-project`，NULL scope=0，orphan=0。
- 最终 schema report：`stage=TI-5-A2`、`ok=true`、`alembicRevision=228ti5a2kv`。

## 3. 验证

- TI-5 A2 专项：5 passed。
- Model Router、Apollo、Auth 相关：29 passed。
- Provider Credential/Security/Call Log：22 passed / 2 skipped。
- Tenant Isolation：186 passed / 11 skipped。
- 后端全量收集：9,182 tests collected，零 collection error。
- 回归中发现并恢复 TWA9 纯函数兼容接口；持久化链仍必须使用完整 scope。最终 smoke 3 passed、diff check GREEN。
- 五分支与五远端均为 `30137dd`，tree 一致；用户 `docs/toutiao-series/*` 未夹带。

## 4. 边界与下一门

本波不处理 `decision_lineage`、Analytics/模型目录或非 PostgreSQL 资源。下一门 TI-5 A3 必须将 631 条无法证明归属的 lineage 原样进入可逆维护隔离，不得沿用 A2 的测试数据例外。本波未连接真实商城、真实模型供应商或客户凭据。
