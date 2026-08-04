# TI-4 A1 Apollo 与调度异步 TenantScope 证据

> 日期：2026-08-04
> 结论：GREEN
> 方案：`228-TI-4-A1-Apollo与调度异步TenantScope实施方案.md`

## 1. 代码与数据库基线

- Scheduler scope 提交：`659b1ce`
- Apollo Contract 提交：`bbdbd2f`
- 最终 tree：`8e5721b121619b76c3504aead3c62be95ab15d23`
- 最终 Alembic：`228ti4a1apollo`
- 备份：`/private/var/tmp/aos-ti4-a1.Tp6Zb6/aos-meta-before.dump`
- 备份大小/权限：`1,890,415 bytes` / `0600`
- SHA-256：`883e668cbde3b2d0fa255fd51a6e598a8b6c243d6d4c31cdacb8d3d4f22ea7bd`

备份保留在 Git 外，仅用于本地共享非生产数据库的可逆验证。

## 2. Scheduler 隔离证明

- Schedule、ScheduledResource、ScheduleExecution 固定携带 org/project。
- create/list/get/update/delete/trigger/history/resource 均要求显式 TenantScope。
- 进程内索引键包含完整 scope；同一业务 ID 可跨工作区共存且互不可见。
- Router 与 Gantt 只从已认证 Principal 注入 scope；后台 executor 从 Schedule envelope 继承 scope。

## 3. Apollo 隔离证明

- `apollo_channel` 保持平台共享发布模板，不被错误复制到组织实例。
- `apollo_spoke` 主键为 `(org_id, project_id, id)`，scope 非空，workspace FK 已验证。
- 表启用 ENABLE/FORCE RLS，public policy 同时校验 `app.current_org_id` 和 `app.current_project_id`。
- runtime CRUD、heartbeat、apply、fleet 均使用 scoped transaction；无 scope 运行角色可见 0，伪造 scope 写入拒绝。
- 两条历史内置测试 Spoke 确定性归属 `dev-org/dev-project`；未使用名称或时间猜测客户归属。

## 4. 可逆演练

共享非生产库执行：

1. A1 前备份；
2. `228ti4a1apollo` 降级到 `228ti4c3contract`；
3. 验证 `project_id` 已撤销、Spoke 行数仍为 2；
4. 再升级到 `228ti4a1apollo`；
5. 验证 2 条 Spoke 均为 `dev-org/dev-project`，schema report `ok=true`。

最终记录：

- `dev-org/dev-project:spoke-local-dev`
- `dev-org/dev-project:spoke-full-stub`

## 5. 自动化验证

- A1 专项：5 passed。
- Apollo + Scheduler + Gantt 定向：42 passed / 13 skipped。
- Tenant Isolation 全量：176 passed / 11 skipped。
- Ruff 目标规则、`git diff --check`：GREEN。
- schema report：主键、workspace FK、RLS、policy、orphan 五项全部 GREEN。

跳过项来自既有条件化 Apollo 场景；专项真实 PostgreSQL 测试已覆盖同 ID 双 scope、无 scope fail-closed 和降级/升级守恒。

## 6. 分支与残余风险

- `m1` 与四个 Worker 本地/远端全部同步到 `bbdbd2f`，tree 一致。
- 主工作树 `docs/toutiao-series/*` 为用户改动，未暂存、未夹带。
- TI-4 冻结资源至此全量 GREEN；剩余风险进入 TI-5：AIP/Analytics/模型目录、向量、对象存储、缓存、队列、离线和其他进程内状态。
- 本证据不代表任何真实商城 API、凭据、数据或写回已经接入。
