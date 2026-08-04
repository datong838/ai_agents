# 228 · TI-4 A1 Apollo 与调度异步 TenantScope 实施方案

> 版本：v1.1 · 2026-08-04
> 状态：GREEN
> 前置：TI-4 Data OS/Connector GREEN；最终代码 `m1@bbdbd2f`

## Rules

复用 canonical `TenantScope`，不改变 Channel 平台模板语义；Spoke 实例与调度任务、资源、执行记录必须按组织和工作区隔离。先锁定历史与兼容边界，再做最小代码修改；不默认认领无法证明的历史 Spoke，不连接真实商城或外部调度后端。

## 1. 对账结论

`tenant_resources.yaml.executionPlan` 仍有唯一冻结组 `ti4-async-runtime`：`apollo_channel`、`apollo_spoke`、`tenant-scheduler-jobs`。C3 只收口 Connector，不能覆盖该组。

- `apollo_channel` 是平台共享发布通道，保持 SYSTEM_GLOBAL。
- `apollo_spoke` 是 tenant-owned 部署实例，当前只有 org scope、全局主键和无 RLS；目标为完整 TenantScope。
- `SchedulingEngine` 是进程级单例，Schedule、Resource、Execution 无 TenantScope，Router 虽有统一鉴权门但未把 Principal 传入 Engine。
- 本波把异步任务 Envelope 固定为 `TenantScope + resource_id`；不把业务 ID 名称、默认 org 或时间作为历史归属证据。

## 2. 实施拆分

### A1-A Scheduler memory boundary

- Schedule、ScheduledResource、ScheduleExecution 增加 org_id/project_id，创建时只能从 Principal scope 注入。
- Engine 的 create/list/get/update/delete/trigger/history/resource 操作全部显式 TenantScope；同 ID 跨工作区互不影响，无 scope direct call 失败关闭。
- executor 接收的 Schedule 自带不可变 scope，作为后续真实队列 Envelope 的最小契约。

### A1-B Apollo Spoke boundary

- Channel 保持全局模板；Spoke API 从 Principal 传入完整 TenantScope，不再只按 org。
- 为 `apollo_spoke` 增加 `project_id` 与 workspace FK；能由现有测试环境确定的 seed 使用测试工作区，无法证明的 synthetic Spoke 进入维护隔离区，不默认认领。
- 冻结 scoped 主键、NOT NULL、ENABLE/FORCE RLS；运行时 transaction 使用 `connect(scope)`。
- Apollo runtime DDL 收归 Alembic；seed 只能写明确 scope，不能覆盖其他租户实例。

### A1-C 验证与回滚

- 同 ID 双 scope、跨 scope 读写删除失败关闭；无 GUC零可见。
- Channel 在两个 scope 下读取一致，Spoke/调度状态互不可见。
- 共享库真实升降级、行数守恒、隔离记录 hash 守恒。
- Tenant Isolation、Apollo、Scheduling 累计回归 GREEN；五分支同步。

## 3. 退出门

- `ti4-async-runtime` 三个资源均有明确边界；Scheduler 不再使用全局 key，Spoke 不再只按 org。
- 运行时无请求期建表、owner tenant transaction 或无 scope 后台扫描。
- 完成后才允许宣告 TI-4 全域 GREEN并进入 TI-5。

## 4. 实施结果

- A1-A 已由 `659b1ce` 完成：Schedule、Resource、Execution 均携带 TenantScope，Engine key 和全部读写删/触发/历史 API 按 scope 隔离。
- A1-B 已由 `bbdbd2f` 完成：`apollo_channel` 保持平台全局模板；`apollo_spoke` 使用 `(org_id, project_id, id)` 主键、workspace FK、FORCE RLS 和 scoped transaction。
- Alembic 最终 revision 为 `228ti4a1apollo`；共享非生产库完成 C3→A1→C3→A1 可逆往返，2 条内置测试 Spoke 行数与归属守恒。
- 定向 Scheduler/Apollo/A1 回归 42 passed / 13 skipped；全量 Tenant Isolation 176 passed / 11 skipped；静态检查和 schema report GREEN。
- `m1` 与四个 Worker 本地/远端最终同一提交 `bbdbd2f`、同一 tree `8e5721b121619b76c3504aead3c62be95ab15d23`。

TI-4 全域至此 GREEN。下一执行域为 TI-5 AIP/Analytics/模型目录与非数据库资源，不授权真实微商城连接。
