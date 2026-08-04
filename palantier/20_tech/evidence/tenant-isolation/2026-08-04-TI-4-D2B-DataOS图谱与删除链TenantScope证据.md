# TI-4 D2-B · Data OS 图谱与删除链 TenantScope 证据

> 日期：2026-08-04
> 结论：GREEN
> 代码：`m1@7a05bd8`
> Tree：`ab11617deee2fdf326cef2afe8e531555bb2df79`
> Alembic：`228ti4d1expand`（本波无迁移）

## 1. 实施结论

- Phase5 Graph 保存、读取、删除均显式接收 canonical `TenantScope`，事务使用 `connect(scope)`。
- Graph nested node/edge ID 唯一检查限定在当前组织与工作区；遗留全局 `pipeline_id` 冲突在 D7 前失败关闭，不认领、不覆盖。
- Source、Pipeline、Dataset、Dataset History、Sync、Schedule、Graph 删除均同时约束资源 ID、`org_id`、`project_id`。
- 缺少 TenantScope 的 Graph/删除 direct call 返回 `TENANT_SCOPE_REQUIRED`。
- `boot_data_os` 只从运行时 surface 隐藏已知 demo ID，不再在无法证明归属时自动物理删除 PostgreSQL 行。
- 本波不回填、不迁移、不删除共享业务数据；D1 的 297 条 Data OS 历史记录保持原样。

## 2. 验证结果

| 验证面 | 结果 |
|---|---|
| D2-B + Phase5 专项 | 48 passed |
| Phase5/DataOS/Connector 相关回归 | 45 passed |
| Tenant Isolation 累计 | 155 passed / 8 skipped |
| Python compile | GREEN |
| Diff whitespace | GREEN |

负向测试覆盖：缺 scope 失败关闭、错租户删除不生效、Graph 同 ID 跨租户冲突不覆盖、不同租户 nested ID 可独立使用、非 scoped boot 零物理删除。

## 3. 共享数据库守恒

| 表 | 行数 |
|---|---:|
| `meta_source` | 4 |
| `meta_pipeline` | 2 |
| `meta_dataset` | 2 |
| `meta_dataset_history` | 212 |
| `meta_sync` | 76 |
| `meta_schedule` | 0 |
| `phase5_pipeline_graph` | 1 |
| 合计 | 297 |

最终 revision 仍为 `228ti4d1expand`。本波测试使用临时数据库，共享库行数与迁移版本未变化。

## 4. 分支状态

`m1` 与四个 worker 分支已推送至同一 `7a05bd8` / 同一 tree。四个 worker clean；主工作树仅保留用户自有 `docs/toutiao-series/*` 改动，未纳入本提交。

## 5. 未解除边界

D2 只完成新 mutation 与删除链。`load_all/boot_data_os` 仍为全局读取，293 条 Data OS 历史行缺少完整 TenantScope，主键仍为全局键，FK 仍为 NOT VALID，RLS 尚未启用。因此 D2-B GREEN 不等于 Data OS 全域隔离完成；下一门必须先执行 D3 历史归属账本与逻辑隔离。
