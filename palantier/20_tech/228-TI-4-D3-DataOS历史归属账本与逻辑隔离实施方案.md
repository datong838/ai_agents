# 228 · TI-4 D3 Data OS 历史归属账本与逻辑隔离实施方案

> 版本：v1.0 · 2026-08-04
> 状态：评审授权链内，待执行
> 前置：TI-4 D2 GREEN；代码 `m1@7a05bd8`；Alembic `228ti4d1expand`
> 边界：本波只建逐记录决策账本和逻辑隔离事实，不回填、不搬迁、不物理删除业务行

## Rules

先冻结共享非生产源快照，再生成确定性逐记录决策。只接受双向可证明的现有 TenantScope；缺列、半空、父工作区不存在、父子归属冲突或断链全部 `QUARANTINE`。禁止按默认组织、ID 前缀、当前登录身份、测试习惯或 props 单证据猜测归属。本波业务 DML 必须为 0。

## 1. 当前基线

| 表 | 总数 | 完整 scope | scope 缺失 |
|---|---:|---:|---:|
| `meta_source` | 4 | 4 | 0 |
| `meta_pipeline` | 2 | 0 | 2 |
| `meta_dataset` | 2 | 0 | 2 |
| `meta_dataset_history` | 212 | 0 | 212 |
| `meta_sync` | 76 | 0 | 76 |
| `meta_schedule` | 0 | 0 | 0 |
| `phase5_pipeline_graph` | 1 | 0 | 1 |
| 合计 | 297 | 4 | 293 |

上述 293 条记录在 D3 不得默认归给测试组织或栖月汇。4 条完整 scope 也必须验证 `twa_workspace` 父记录存在，才允许判为 `NO_ACTION`。

## 2. 决策模型

复用 TI-1 的 append-only 控制面表：`tenant_backfill_batch`、`tenant_backfill_batch_event`、`tenant_ownership_decision`、`tenant_quarantine_record`，不新增另一套账本。

| 条件 | 决策 | 证据等级 | 动作 |
|---|---|---|---|
| org/project 完整且 `twa_workspace` 父存在 | `NO_ACTION` | A | 保持原行 |
| 任一 scope 为空 | `QUARANTINE` | X | 只写控制面逻辑隔离记录 |
| scope 完整但父工作区不存在 | `QUARANTINE` | X | 只写控制面逻辑隔离记录 |
| 父子链 scope 冲突或断链 | `QUARANTINE` | X | 只写控制面逻辑隔离记录 |
| 可证明唯一目标但需改写 | 本波不接受 | - | D3 gate BLOCKED，另行评审物理回填 |

## 3. 记录身份与守恒

- 每表冻结稳定业务键：Source/Pipeline/Sync/Schedule 用 `id`，Dataset 用 `rid`，History 用数据库 `id`，Graph 用 `pipeline_id`。
- `key_hash` 包含 stage、表名、原始 scope 与稳定业务键；`before_hash` 基于完整行 canonical JSON。
- `source_snapshot_hash` 覆盖逐表数量、逐记录决策及行 hash；重复 plan 必须得到同一 batch ID。
- Apply 前重新构建快照；任何新增、删除或内容漂移均失败关闭。
- `NO_ACTION + QUARANTINE = 297`，`ASSIGN = 0`，业务表 INSERT/UPDATE/DELETE = 0。

## 4. 角色与状态机

沿用 Planner、Approver、Executor、Verifier 职责分离与 actor hash 去标识化。状态按 `PLANNED → APPROVED → EXECUTING → COMPLETED → VERIFIED` 追加；rollback 只追加 `ROLLED_BACK` 证据，不删除历史事件。重复 persist/verify 必须幂等。

## 5. 文件范围

| 文件 | 变更 |
|---|---|
| `aos_api/data_os_ownership.py` | D3 决策计划、账本、apply/verify/rollback；零业务 DML |
| `scripts/tenant_data_os_ownership.py` | 非生产受控 CLI |
| `tests/tenant_isolation/test_ti4_d3_data_os_ownership.py` | 决策、守恒、漂移、职责分离、零 DML |
| evidence / AOS 项目开发上下文 | 共享库最终快照、batch、分支和下一门 |

## 6. 执行顺序

1. 在临时数据库验证确定性、未知归属逻辑隔离、漂移门、角色分离和 rollback。
2. 对共享非生产库只读 plan，核对 297 条逐记录守恒。
3. 先做逻辑备份并记录校验值，再 persist/approve/apply/verify；apply 必须报告 `businessRowsUpdated=0`。
4. 再次核对 7 表行数、逐表 hash、Alembic revision 均未变化。
5. 同步 m1 与四 worker，输出 evidence；进入 D4 前不改 FK 状态。

## 7. 退出门

- 297 条当前记录都有且只有一个逐记录 decision。
- `ASSIGN=0`；未知/断链全部逻辑 `QUARANTINE`，没有静默归属。
- 决策、事件、隔离记录 append-only；角色不可复用；源快照漂移失败关闭。
- 共享库业务表 297 行及内容 hash 守恒，业务 DML=0，revision 保持 `228ti4d1expand`。
- D3 专项与 Tenant Isolation 累计 GREEN；五分支同 HEAD/tree；上下文同步。

## 8. 后续边界

D3 GREEN 后，D4 只可验证非 NULL 行的 workspace FK；293 条逻辑隔离记录仍存在于活跃表时，不得把 FK 验证写成“历史数据已归属”。若 PostgreSQL NOT VALID FK 对 NULL 行天然放行，D4 必须同时证明非 NULL orphan=0，并明确 NULL 仍由 D3 逻辑隔离而非数据库 FK 保护。物理隔离留给 D7 Contract，不在 D3 执行。
