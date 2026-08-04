# TI-1 E2 Authz 双写与差异 Ledger 证据

> 日期：2026-08-04  
> 结论：GREEN（仅限 E2 授权范围）  
> 代码：`aos-platform m1@a7df658`

## 1. 范围与不变项

E2 仅为 `authz_tuple` 新写增加可关闭的 TenantScope 双写和差异证据。默认开关为 `off`；既有 check/list/delete 仍走 legacy 读路径。本波未执行历史回填、归属修复、读切换、RLS、删除或客户数据迁移。

## 2. 实现证据

| 证据面 | 结果 |
|---|---|
| Feature flag | `AOS_TENANT_DUAL_WRITE_AUTHZ=off|shadow|enforce`，默认 `off`，非法值失败关闭 |
| Scope 来源 | Router 只从已认证 `Principal` 构造 `TenantScope`，请求 body 不接收 org/project |
| 冲突语义 | `ON CONFLICT DO NOTHING`，不更新既有 NULL/异租户行；SHADOW 记 MISMATCH，ENFORCE 返回 `TENANT_DUAL_WRITE_CONFLICT` |
| Ledger 最小化 | 只保存 resource/operation/SHA-256 hash/请求 scope/观察 scope/status/time，无 tuple 原文、Token 和 payload |
| 回滚 | 运行第一回滚点为开关切 `off`；本地无审计数据时 migration 可降级 |

## 3. 真实 PostgreSQL 验证

- Alembic `228ti1e1expand → 228ti1e2dual → 228ti1e1expand → 228ti1e2dual` 成功，最终单一 head/current 为 `228ti1e2dual`。
- Schema lint GREEN：`authz_tuple` 两个租户列仍 nullable，7 个 E1 FK 仍 NOT VALID，RLS 启用/强制均为 0；ledger 10 列和必填约束齐全。
- 事务内探针：SHADOW 新 tuple 产生 MATCH；既有 NULL tuple 产生 MISMATCH 且原行不变；ENFORCE 对 mismatch 失败关闭。事务回滚后 tuple 和 ledger 都无残留。
- 实扫 coverage：87 张 PostgreSQL 表、94 个总资源，100% 登记；STRONG_PK/WEAK_PK/NO_TENANT = 32/28/27。

## 4. 测试和质量门

| 门 | 结果 |
|---|---|
| E2 专项 | 26 passed，7 个既有 warning |
| 租户隔离 + migration 累计 | 74 passed，7 个既有 warning |
| Authz 相关 | 15 项全部通过（最后 1 项单独复核） |
| Ruff / compile / diff | GREEN |
| TWA 共享库累计 | 43 passed / 3 failed；失败为固定 ID 残留、成员残留与 E1 FK 下的非幂等测试构造，在未含 E2 的 worker 基线也可复现；未删除数据规避 |

TWA 失败不经过 E2 双写路径，因此不是 E2 回归；但它们是真实的测试隔离债务，不应记为全量 GREEN。后续应使用独立数据库/schema 或随机化租户/ID，不在 E2 中扩大修改。

## 5. 实扫文件

- `ti1-e2-2026-08-04/ti1-e2-coverage.json`
- `ti1-e2-2026-08-04/ti1-e2-schema-lint.json`
- `ti1-e2-2026-08-04/precheck/` 四份 TI-0D 刷新账本
- `ti1-e2-2026-08-04/plan/` TI-0E 刷新计划

## 6. 下一波建议

进入 TI-1 E3 之前先单独评审“历史归属 + quarantine ledger + 备份/恢复”方案。E3 会修改历史数据，必须在独立演练库先证明可逆，并解决本机缺少 `pg_dump/psql` 的生产备份恢复硬门；未单独授权前不执行 E3。
