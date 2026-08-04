# 228 · TI-4 D2 Data OS 显式 TenantScope 写链实施方案

> 版本：v1.0 · 2026-08-04
> 状态：评审通过 / D2-A 执行中
> 授权：用户已授权连续完成微商城接入前置；本波不连接具体商城
> 前置：TI-4 D1 GREEN；代码 `m1@8e49b68`；Alembic `228ti4d1expand`

## Rules

先方案后代码；复用 canonical `TenantScope` 和 `connect(scope)`，不从 item props、ID 或默认值推断 scope。D2 只收口新 mutation，不回填 297 条历史行、不切换全局 load/boot、不启用 RLS、不改主键。跨 scope 的既有全局 ID 冲突必须失败关闭，禁止更新另一租户的 scope 列。

## 一、分波

### D2-A：Wave API 六类持久化

- `persist_source`
- `persist_pipeline`
- `persist_dataset`
- `persist_dataset_history`
- `persist_sync`
- `persist_schedule`

Router 从 Principal 构造一个 TenantScope，所有关联写入复用同一 scope。Sync 只允许更新当前 scope 的 Dataset/History；patch/run 必须先验证内存对象属于当前 scope。

### D2-B：Graph 与删除 mutation

- `persist_phase5_pipeline_graph` 内部查询、upsert 与 nested ID 唯一检查按 scope；
- Source/Pipeline/Dataset/History/Sync/Schedule/Graph 删除显式 scope；
- 所有 direct call 缺 scope 失败关闭；
- `boot_data_os` 的 demo 清理不得无 scope 扫删，改为只处理显式测试 scope 或停止自动物理删除。

D2-A GREEN 后立即进入 D2-B，不提前进入 D3。

## 二、写入 Contract

1. Store 函数签名首参为 `TenantScope`；不接受 `None`，不读取 context fallback。
2. 所有 transaction 使用 `connect(scope)`，并显式写 `org_id/project_id`。
3. 现有全局主键阶段，upsert 只在 `existing.org_id/project_id == EXCLUDED` 时更新；跨 scope 或 NULL 历史冲突返回失败，不认领、不覆盖。
4. Dataset History 的替换删除和插入均绑定 `(dataset_rid, org_id, project_id)`。
5. Router item 中的 `orgId/projectId` 只是返回/内存投影，数据库授权边界来自传入 TenantScope。
6. `_persist_safe` 不得吞掉 TenantScope 安全冲突并返回成功；安全错误向请求方失败关闭。非安全可用性错误是否继续兼容，须有测试证明。

## 三、文件范围

| 文件 | 变更 |
|---|---|
| `aos_api/data_os_store.py` | D2-A 六类 scoped persist；D2-B graph/delete scoped mutation |
| `aos_api/routers/wave_ext.py` | Principal→TenantScope、同 scope 关联写、内存对象 ownership gate |
| `aos_api/phase5_pipeline_engine.py` | D2-B graph scope 透传 |
| `tests/tenant_isolation/test_ti4_d2_data_os_write_scope.py` | 缺 scope、跨 scope、同 ID、防覆盖、history/sync 联动 |
| 既有 Data OS/API tests | 显式测试 scope 和父工作区夹具 |

## 四、退出门

1. D2-A 六类新写全部显式 scope；静态扫描无默认 `dev-org/dev-project` persist。
2. D2-B graph 与 delete mutation 全部显式 scope；无 scope direct call 失败关闭。
3. 两 TenantScope 同时使用不同 ID 时互不可见；全局键未 Contract 前，同 ID 跨 scope 明确冲突而非覆盖。
4. Dataset History 的 delete+insert 只影响当前 scope；Sync 不更新其他 scope Dataset。
5. 共享库 297 条历史行、5 张电商表和 Object 行数不变；Alembic 保持 `228ti4d1expand`。
6. Data OS 专项、API 相关回归、Tenant Isolation 累计 GREEN。
7. 五分支同 HEAD/tree，证据与上下文同步。

## 五、后续边界

D2 后仍保留全局主键、全局 `load_all/boot_data_os` 和 297 条未决历史，因此不能宣告 Data OS 已隔离。D3 建逐记录 ownership/quarantine ledger；D4 Validate；D5 才切 scoped read/boot；D6 RLS；D7 复合 Contract 与 runtime DDL 收归 migration。
