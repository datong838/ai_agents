# 228 · TI-0D 归属 Precheck 与栖月汇空数据基线证据

> 日期：2026-08-04  
> 方案：`228-组织与工作区租户隔离全量补强实施方案.md` v1.5  
> 代码基线：`aos-platform m1@504a639`  
> 结论：TI-0D 扫描 GREEN；栖月汇业务数据为 0，但全资源空数据证明为 YELLOW；未执行任何数据写入

## 1. 新增能力

- `aos_api/tenant_precheck.py`：在 PostgreSQL 只读事务中生成行数、租户空值、租户聚合、现有 FK 孤儿、JSON 租户标记和迁移阻断项。
- `scripts/tenant_isolation_precheck.py`：生成 precheck、migration ledger、栖月汇 baseline、非 PostgreSQL inventory 四份脱敏 JSON。
- `tenant_resources.yaml` 增加 `BUSINESS_DATA/CONTROL_PLANE` 基线范围，避免把组织目录必需行误报成客户业务数据。
- MinIO 只统计 Bucket/租户前缀，不读取或输出完整对象键和正文；Vector、内存、Queue、Cache 同样不输出内容。

## 2. PostgreSQL 结果

| 指标 | 结果 |
|---|---:|
| 注册表/成功扫描表 | 86 / 86 |
| 全表总行数 | 2,854 |
| 已归测试组织 TENANT_OWNED 行 | 1,749 |
| 栖月汇 BUSINESS_DATA 行 | 0 |
| 栖月汇 CONTROL_PLANE 行 | 5 |
| 未知归属行 | 993，分布于 12 张表 |
| 空/空字符串租户行 | 0 |
| 现有 FK 孤儿 | 0 |

栖月汇 5 行控制面数据来自 `meta_workspace=1`、`meta_membership=1`、`twa_audit=3`，是组织/工作区存在与审计所需记录，不属于订单、Module、对象、AIP 或电商业务数据。

未知归属主要包括 `decision_lineage=631`、`meta_dataset_history=212`、`meta_sync=76`、`obj_instance=31`、`meta_aip_kv=23`，以及 `authz_tuple/graph_edge/meta_branch/meta_dataset/meta_pipeline/funnel_status/phase5_pipeline_graph`。TI-0D 未猜测其归属。

## 3. 非 PostgreSQL 结果

| 资源 | 状态 | 结果 |
|---|---|---|
| MinIO | PROBED | 70 个对象；测试前缀 68、栖月汇 0、未知前缀 2 |
| Vector | PROBED | `meta_aip_kv` 1 个未分租户记录；未读取向量 |
| Scheduler | PROBED | `meta_schedule` 0；栖月汇 0 |
| Cache | NOT_CONFIGURED | 当前无 Redis tenant backend，不能按空处理 |
| Message Queue | NOT_CONFIGURED | 当前仅发现进程内路径，不能按空处理 |
| Offline Storage | NOT_IMPLEMENTED | 未识别 tenant-owned offline store |
| Process Memory | STATIC_ONLY | 832 个可变全局/单例候选，AST 解析错误 0；未读取运行时值 |

## 4. Migration Ledger

| 阻断项 | 资源数 |
|---|---:|
| TENANT_COLUMNS_MISSING | 13 |
| TENANT_COLUMNS_NOT_IN_PRIMARY_KEY | 27 |
| TENANT_COMPOSITE_FOREIGN_KEY_MISSING | 53 |
| UNATTRIBUTED_ROWS | 12 |

共 53 个资源为 `REQUIRES_REMEDIATION`。该 ledger 只给出迁移动作与波次，不包含、也不会执行 SQL。

## 5. 栖月汇结论

`targetBusinessRowCount=0`，但 `isProvenEmpty=false`。当前三个阻断原因：

1. 993 行 PostgreSQL 数据无法证明属于测试组织或其他组织。
2. MinIO 仍有 2 个未知前缀对象，Vector 有 1 个未分租户记录。
3. Cache、Queue、Offline、Process-memory 尚无完整运行时租户探测。

因此可以确认“当前已识别业务表中没有栖月汇业务数据”，不能确认“栖月汇全域资源已经严格为空”。

## 6. 证据文件

- [`ti0d-precheck.json`](ti0d-2026-08-04/ti0d-precheck.json)
- [`ti0d-migration-ledger.json`](ti0d-2026-08-04/ti0d-migration-ledger.json)
- [`ti0d-qiyue-baseline.json`](ti0d-2026-08-04/ti0d-qiyue-baseline.json)
- [`ti0d-non-postgres-inventory.json`](ti0d-2026-08-04/ti0d-non-postgres-inventory.json)

四份 JSON 已执行敏感值扫描，未包含开发密码、Bearer、API Key、对象正文或业务行内容。
