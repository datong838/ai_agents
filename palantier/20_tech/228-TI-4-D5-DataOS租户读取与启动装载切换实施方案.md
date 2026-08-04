# 228 · TI-4 D5 Data OS 租户读取与启动装载切换实施方案

> 版本：v1.0 · 2026-08-04
> 状态：GREEN
> 前置：TI-4 D4 GREEN；代码 `m1@176bdf5`；Alembic `228ti4d4validate`

## Rules

所有 Data OS 读取必须来自请求 Principal 转换出的 canonical TenantScope。NULL/半空/其他 scope 数据默认不可见；不得保留“无标签历史对当前组织可见”兼容。进程启动没有请求 scope，因此禁止全库装载到共享内存。改动只触及 Data OS surface，其他 wave_ext 能力保持不变。

## 1. 分波

### D5-A：Store 与启动边界

- `load_all(scope)` 必须显式 TenantScope，7 表所有 SELECT 同时约束 org/project，History 只装载当前 scope Dataset。
- 缺 scope direct call 失败关闭；两个工作区的读取结果互斥；293 条 quarantine/NULL 不可见。
- `boot_data_os` 不再执行全库 `SELECT *`，只清空 Data OS 运行时缓存并记录 lazy scoped load；不物理删除任何行。

### D5-B：Router 与内存投影

- Source/Sync/Dataset/History/Pipeline/Build/Schedule 的 list/detail/mutation 入口先按当前 scope hydrate。
- 可见性从 org-only 改为严格 `(orgId, projectId)`；无标签条目不可见。
- detail、patch、run、embed 的资源 ownership gate 统一返回跨租户不可见/失败关闭。
- 现有全局业务 ID 阶段，不同 scope 的同 ID 仍按 D2 Contract 冲突；D7 后再切 scope 复合键。

## 2. 缓存策略

在不重构其他 wave_ext surface 的前提下，Data OS 缓存使用“按 scope 懒加载 + 带 scope stamp”的过渡策略：

1. App startup 清空 Data OS 六类 map 和已加载 scope 集合。
2. 首次请求调用 `load_all(scope)`，只合并当前 scope 项；同 scope 后续新写直接更新当前投影。
3. Reload 时只移除当前 scope 的旧投影，不触碰其他 scope；所有读取仍二次执行严格 scope 过滤。
4. 293 条 NULL 历史永不进入 runtime map。

该策略不是最终复合 key；D7 前用全局 ID 冲突失败关闭保证不同 scope 不能拥有同一 ID。

## 3. 文件与测试

| 文件 | 变更 |
|---|---|
| `aos_api/data_os_store.py` | scoped `load_all`、无全库 startup boot |
| `aos_api/routers/wave_ext.py` | lazy hydrate、严格 scope list/detail/mutation |
| `aos_api/main.py` | 保留 boot hook，但其行为变为零数据库读取的 cache reset |
| `tests/tenant_isolation/test_ti4_d5_data_os_read_scope.py` | 两 scope、NULL quarantine、detail/patch/run、boot 零全局装载 |
| 既有 Data OS/API tests | 适配 lazy scoped restore |

## 4. 退出门

- `load_all/boot_data_os` 全局业务 SELECT 静态命中为 0；无 scope load 失败关闭。
- Source/Sync/Dataset/History/Pipeline/Build/Schedule 两工作区 list/detail 互不可见。
- 293 条 NULL 历史在 Store 和 API 均不可见，且数据库行/hash 不变。
- startup 不加载任一租户业务数据，不执行物理删除。
- 相关 API、Data OS 专项、Tenant Isolation 累计 GREEN；共享库 297/293 与 D3 账本守恒；五分支同步。

## 5. 后续边界

D5 后数据库仍无 Data OS RLS，任何未来漏 scope SQL 仍可能越界。下一门 D6 为 7 表 ENABLE/FORCE RLS 与双 GUC policy；D7 才处理复合主键、NOT NULL、物理隔离和 runtime DDL 收归 migration。

## 6. 执行结果

代码 `2b81a1b` 完成 scoped `load_all`、零全库 startup boot、按 scope 懒加载和七类 API 严格工作区读取。相关 45 passed / 22 skipped，Tenant Isolation 162 passed / 8 skipped；共享 297/293/293 与 `228ti4d4validate` 守恒。下一门 D6。
