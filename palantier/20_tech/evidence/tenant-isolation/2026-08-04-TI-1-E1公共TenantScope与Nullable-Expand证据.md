# 228 · TI-1 E1 公共 TenantScope 与 Nullable Expand 证据

> 日期：2026-08-04
> 代码提交：`621a1bb`
> 状态：TI-1 E1 GREEN；未授权且未执行 E2 双写、E3 回填、E5 读切换、E6 RLS 或 E7 Contract

## 1. 本波交付

- 冻结不可变 `TenantScope(org_id, project_id)`，严格拒绝空值、首尾空白、控制字符和超过 160 字符的值。
- 电商 `workspace_id` 只在适配边界映射为 canonical `project_id`，没有形成第三套 Scope。
- `db.connect(scope=...)` 可显式或通过 ContextVar 设置 transaction-local `aos.org_id/aos.project_id`；未传 scope 的旧调用行为不变。
- Alembic 新增单一 head `228ti1e1expand`。
- `authz_tuple` 增加 nullable `org_id/project_id` 和部分索引；9 条历史数据保持两列 NULL。
- 新增 7 个 `NOT VALID` 复合外键；没有执行 `VALIDATE CONSTRAINT`，没有启用 RLS。
- 新增只读 schema lint，防止 E1 提前进入 NOT NULL、FK validate 或 RLS。

## 2. 真实迁移验证

执行顺序：

1. `228assetintegration → 228ti1e1expand`
2. schema lint 和租户数据核验
3. `228ti1e1expand → 228assetintegration`
4. 确认新增列数量恢复为 0
5. 再次升级到 `228ti1e1expand`

最终 Alembic `heads/current` 均为唯一 `228ti1e1expand`。升级前 TI-0D 与升级后逐表精确对账均为 86 表、2,854 行，逐表差异为 0。

`authz_tuple`：总数 9、两列均 NULL 9、已归属 0。没有把历史授权记录自动归给测试组织或栖月汇。

## 3. Schema lint

| 检查 | 结果 |
|---|---|
| authz nullable tenant columns | 2/2 |
| 新增 FK | 7/7 |
| 已 validate 的新增 FK | 0 |
| RLS enabled/forced 表 | 0 |
| Alembic revision | `228ti1e1expand` |
| 总体 | GREEN |

事务 GUC 实测：scope 连接内为 `dev-org/dev-project`，事务结束后的新连接为 `null/null`，没有 session 泄漏。

## 4. 新暴露的历史断链

`NOT VALID` 外键使结构可以安全展开，同时只读 precheck 暴露了 3 张表、64 行历史断链：

| 子表 | 孤儿行 | 父表 |
|---|---:|---|
| `meta_membership` | 57 | `meta_workspace` |
| `twa_ws_member` | 4 | `twa_workspace` |
| `twa_audit` | 3 | `twa_workspace` |

这些记录不是 E1 新产生的，本波没有补父记录、改租户或删除。它们阻断对应 FK validate 和后续 E3，但不阻断 nullable expand 收口。

## 5. 重新实扫结论

- PostgreSQL coverage：86/86，drift/unregistered/stale 均为 0。
- 结构状态：STRONG_PK 31、WEAK_PK 28、NO_TENANT 27。
- 未知归属仍为 993 行；其中 `authz_tuple` 的 9 行由“缺列未知”变为“nullable 空值未知”。
- 栖月汇 BUSINESS_DATA=0、CONTROL_PLANE=5，`isProvenEmpty=false`。
- 栖月汇阻断新增 `BLANK_TENANT_VALUES`，没有因 expand 被错误判为已隔离。
- MinIO、Vector、Cache、Queue、Offline 和 Process-memory 结论与 TI-0D 一致。

## 6. 测试结果

- TI-1 E1、TI-0B～TI-0E 和迁移控制面累计：`65 passed`，7 个既有 warning。
- 组织/工作区/TWA 专项：GREEN。
- Ruff：GREEN。
- Python compileall：GREEN。
- Alembic upgrade → downgrade → upgrade：GREEN。
- 三轮 schema/ledger/plan JSON：格式与敏感信息检查 GREEN。

## 7. 未完成门禁

本机缺少 `pg_dump/psql` 客户端，因此未声称完成 PostgreSQL 逻辑备份恢复演练。进入任何生产库、客户库或不可逆阶段前，必须安装匹配服务端版本的 PostgreSQL 客户端并完成可恢复备份验证。

下一步只能进入 TI-1 E2 方案评审：确定哪些 Store 首批双写、feature flag、差异 ledger、历史孤儿 quarantine 策略和回滚方式。未经新授权，不执行双写或历史回填。
