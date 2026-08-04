# TI-4 D2-A Data OS 显式 TenantScope 写链证据

> 日期：2026-08-04
> 结论：GREEN
> 代码：`aos-platform m1@5155d9b`
> Alembic：保持 `228ti4d1expand`

## 结果

- Source/Pipeline/Dataset/History/Sync/Schedule 的 Store 首参均为显式 TenantScope，transaction 使用 `connect(scope)`，scope 写入数据库列。
- 全局主键尚未 Contract 的阶段，upsert 仅允许相同 scope 更新；跨 scope 或 NULL 历史冲突返回 `TENANT_SCOPE_CONFLICT`，不覆盖 org/project。
- Dataset History 的 delete+insert 同时约束 dataset_rid 和 scope；另一 scope 的同 rid history 保留。
- Router 从 Principal 构造 scope，Source/Pipeline/Dataset/Schedule mutation 做 ownership gate；Sync 只联动当前 scope Dataset。
- `_persist_safe` 不再吞掉安全 ApiError；普通可用性异常仍按既有兼容路径记录日志。

## 验证

| 验证 | 结果 |
|---|---|
| D2-A + Data OS 专项 | 12 passed |
| Tenant Isolation 累计 | 144 passed、8 skipped |
| 缺 scope 六类负向 | 全部失败关闭 |
| 跨 scope 全局 ID | 409，原 owner/status 不变 |
| 共享库 | revision `228ti4d1expand`；7 表仍 297 行 |
| 五分支 | `5155d9b`；tree `b9890d897cf973dc6c3100f61f2558b204d16e0d` |

## 未完成

Graph persist/load/delete、六类 delete mutation、boot demo 物理清理仍需 D2-B；全局 load/read 与 297 行历史归属仍未切换。
