# TI-4 C2 通用 Connector 显式 TenantScope 证据

> 日期：2026-08-04
> 结论：GREEN
> 代码：`aos-platform m1@4ae0492`
> Alembic：保持 `228ti4c1expand`

## 1. 代码事实

| 能力 | 结果 |
|---|---|
| Router Principal | 继续传 `org_id/project_id` |
| REST/File handler | 显式构造 TenantScope，`connect(scope)` |
| MySQL/PostgreSQL/SQL Server | wrapper 到 module 透传同一 TenantScope |
| INSERT | `object_type, object_id, props, org_id, project_id` |
| Conflict target | `(org_id, project_id, object_type, object_id)` |
| 缺失/非法 scope | `TENANT_SCOPE_REQUIRED`，失败关闭 |
| TI-3 E5 deferred writer | 4 → 0 |

health/probe 没有业务写入，保持原行为；`autoCreateObjectType` 仍默认关闭。本波未新增平台 adapter、schema mapping 或真实 API 调用。

## 2. 隔离证明

- REST mock 固定 `rest-mock-1` 在两个 TenantScope 中同时存在，未互相覆盖。
- File mock 固定 `file-mock-a.txt` 在两个 TenantScope 中同时存在，未互相覆盖。
- PostgreSQL、SQL Server mock 与 MySQL synthetic sample 均只在传入 scope 可见。
- 三个 JDBC module 无 TenantScope 直调均被拒绝；REST/File 缺失或空白 scope 同样被拒绝。
- 既有 API Connector 测试补齐数据库父工作区夹具；运行时代码没有自动创建组织/工作区。

## 3. 验证结果

| 验证 | 结果 |
|---|---|
| C2 + TI-3 E5 专项 | 9 passed |
| Connector 相关回归 | 28 passed、1 skipped |
| Tenant Isolation 累计 | 132 passed、8 skipped |
| Ruff（排除文件既有 BLE001/SIM117） | GREEN |
| diff/compile | GREEN |

## 4. 共享开发库守恒

| 项 | 结果 |
|---|---|
| Alembic revision | `228ti4c1expand` |
| `obj_instance` | 0 |
| 5 张电商真源表 | 全部 0 |
| 本波 schema migration | 无 |
| 本波共享库业务 DML | 0 |

## 5. 分支与下一门

m1、w1、w2、w3、w4 本地/远端均为 `4ae0492`，tree `d25c6cea776fa764687172cefce1002eaf11b45d`。主工作树用户头条/掘金文档继续未暂存、未夹带。

下一门为 TI-4 D1：对 Data OS 的 Source/Pipeline/Dataset/History/Sync/Schedule/Graph 做 nullable TenantScope Expand 和父级 FK，不连接具体商城。
