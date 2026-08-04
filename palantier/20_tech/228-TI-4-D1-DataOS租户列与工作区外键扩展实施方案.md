# 228 · TI-4 D1 Data OS 租户列与工作区外键扩展实施方案

> 版本：v1.0 · 2026-08-04
> 状态：评审通过 / 执行中
> 授权：用户已授权连续完成微商城接入前置；本波不连接具体商城
> 前置：TI-4 C1/C2 GREEN；代码 `m1@4ae0492`；Alembic `228ti4c1expand`

## Rules

先方案后代码；D1 只做 Expand，不回填、不切换 Data OS 读写、不启用 RLS、不修改进程内缓存行为。历史 `props`、默认 `dev-org/dev-project` 和 ID 命名都不能直接作为可信归属；所有既有行先原样冻结，归属决策留给 D3。新增列允许 NULL，新增 workspace FK 全部 NOT VALID，迁移必须可逆。

## 一、只读基线

| 表 | 行数 | 当前 scope | 当前主键 |
|---|---:|---|---|
| `meta_source` | 4 | `org_id/project_id` NOT NULL，但带历史默认值 | `(id)` |
| `meta_pipeline` | 2 | 无列；部分身份可能仅在 props | `(id)` |
| `meta_dataset` | 2 | 无列；部分身份可能仅在 props | `(rid)` |
| `meta_dataset_history` | 212 | 无列 | `(id)` |
| `meta_sync` | 76 | 无列 | `(id)` |
| `meta_schedule` | 0 | nullable `org_id/project_id` | `(id)` |
| `phase5_pipeline_graph` | 1 | 无列 | `(pipeline_id)` |

总计 297 行。`data_os_store.py` 当前还会用默认 scope、props scope 和全局 ID 读写，属于 D2/D5 范围，D1 不混做。

## 二、目标

1. 为 `meta_pipeline`、`meta_dataset`、`meta_dataset_history`、`meta_sync`、`phase5_pipeline_graph` 新增 nullable `org_id/project_id`。
2. `meta_source` 与 `meta_schedule` 保留现有列形态，不在 D1 改写历史 default 或 nullable 状态。
3. 为 7 表新增具名 NOT VALID FK：

```text
(org_id, project_id) -> twa_workspace(org_id, project_id)
```

4. FK 名固定为 `fk_<table>_workspace_ti4d1`。
5. 不修改 297 条历史行；升级前后行数、payload 和主键不变。
6. schema lint 报告 10 个新增列、7 个 NOT VALID FK、逐表行数与 revision。

## 三、文件范围

| 文件 | 变更 |
|---|---|
| `alembic/versions/228ti4d1_data_os_expand.py` | 5 表新增 scope 列、7 表 NOT VALID workspace FK、可逆 downgrade |
| `aos_api/tenant_schema_lint.py` | D1 revision 与 Data OS Expand 报告 |
| `tests/tenant_isolation/test_ti4_d1_data_os_expand.py` | 静态边界、实库 lint、数据守恒、真实升降级 |
| 历史 C1 lint/tests | 允许合法后继 revision，不降低 C1 断言 |
| 总方案、证据、AOS 上下文 | 收口后对账 |

## 四、迁移与回滚

升级顺序：先给 5 表增加两个 nullable TEXT 列，再给 7 表增加 NOT VALID FK。降级逆序删除 7 个 FK，再删除本波新增的 10 个列；`meta_source/meta_schedule` 原有列绝不删除。

任何目标表缺失、父级复合唯一键缺失、目标列类型冲突或 Alembic 非预期 head，均失败关闭。共享库迁移前必须生成本机外部逻辑备份并通过 `pg_restore -l`。

## 五、退出门

1. 7 表总行数升级前后均为 297，逐表差异 0；业务 DML=0。
2. 新增列 10/10 且 nullable；workspace FK 7/7 且 `validated=false`。
3. 真实 `C1 → D1 → C1 → D1` 往返 GREEN，最终 revision `228ti4d1expand`。
4. D1 专项、Tenant Isolation 累计、lint/compile/diff check GREEN。
5. 五分支同 HEAD/tree，证据和 AOS 上下文同步。
6. D1 GREEN 只表示结构可承载 scope；Data OS 仍不得用于多租户生产，下一波 D2 显式 TenantScope 写链。

## 六、风险

| 风险 | 等级 | 控制 |
|---|---|---|
| 把 source 默认 dev scope 当可信归属 | P0 | D1 零 DML；D3 逐记录 ledger 决策 |
| props 中 scope 被误认为列隔离 | P0 | D2 必须显式列写；D5 才切读 |
| history 子表先丢失父 scope | P0 | D2 写入时从同一 TenantScope 传递，D4 再验证父关系 |
| 运行期 DDL 覆盖 migration | P1 | 后续 D2 同步更新 schema 声明；D1 先以 Alembic 为真源 |
| 提前启用 RLS 导致全链中断 | P0 | D1 禁止 RLS；按 D2→D3→D4→D5→D6→D7 顺序 |
