# 228 · TI-3 E3 Object/Graph/Draft/Wiki 历史归属隔离实施方案

> 版本：v1.0 · 2026-08-04
> 状态：GREEN（代码 `21f8803`，共享非生产最终 batch 已 verify）
> 前置：TI-3 E1/E2 GREEN；代码 `m1@5e58768`；Alembic `228ti3e1expand`

## 0. Rules

先方案后代码；历史归属只接受现存强 scope 或可复核的一对一证据；NULL scope 不按默认组织、ID、创建时间、Demo 名称或对象关系猜测。复用 TI-1 E3 append-only batch/decision/event/quarantine ledger；先只读 dry-run，再备份与恢复库演练，最后才允许共享非生产 apply/verify。不得删除业务行、不得把未知行写给栖月汇、不得连接具体商城。

## 1. 只读基线

2026-08-04 共享非生产实扫：

| 资源 | 总行 | 已有完整 scope | NULL/不完整 scope | E3 决策 |
|---|---:|---:|---:|---|
| `draft_dataset` | 925 | 925 | 0 | NO_ACTION |
| `funnel_status` | 1 | 0 | 1 | QUARANTINE |
| `graph_edge` | 2 | 0 | 2 | QUARANTINE |
| `meta_branch` | 3 | 0 | 3 | QUARANTINE |
| `obj_branch_overlay` | 0 | 0 | 0 | - |
| `obj_instance` | 31 | 0 | 31 | QUARANTINE |
| `object_lifecycle` | 2 | 2 | 0 | NO_ACTION |
| `wiki_page` | 1 | 1 | 0 | NO_ACTION |
| `wiki_page_version` | 65 | 65 | 0 | NO_ACTION |
| 合计 | 1,030 | 993 | 37 | NO_ACTION=993，QUARANTINE=37 |

“已有完整 scope”只表示本波不修改该行，并不追溯证明早期默认值的原始来源；E3 必须记录其当前 scope 与 before hash，后续 E5 对读和 TI-6 空组织证明仍需独立验证。

## 2. 归属策略

1. org/project 均非 NULL 且工作区父记录存在：`NO_ACTION/A`，冻结当前归属与行 hash，不做 DML。
2. 任一 scope 为 NULL：`QUARANTINE/X`，写入脱敏 key hash、before hash、reason=`TENANT_SCOPE_UNPROVEN`；原业务行保持不变。
3. scope 非 NULL 但工作区父记录不存在：`QUARANTINE/X`，reason=`WORKSPACE_PARENT_NOT_FOUND`。
4. 不存在 `ASSIGN` 规则；若后续取得外部权威证据，必须新建独立 batch，不修改本 batch 决策。
5. E2 已使 NULL 行不进入正常租户读取，因此 ledger quarantine 与运行时不可见共同形成逻辑隔离。

## 3. 状态机与职责分离

- `tenant_backfill_batch`：mode=`NON_PROD`，stage=`TI-3-E3`。
- `tenant_ownership_decision`：1,030 条逐记录决策；key、before、evidence 仅保存 canonical hash。
- `tenant_quarantine_record`：37 条未知归属记录。
- Planner、Approver、Executor、Verifier actor hash 必须两两不同。
- PLANNED → APPROVED → EXECUTING → COMPLETED；本波 apply 只落决策/隔离账本，不修改 9 张业务表，所以 verify 的业务 DML 数必须为 0。

## 4. 执行与回滚

1. Dry-run：逐表按稳定主键排序，计算 1,030 个 key/before hash、scope 分布与决策摘要。
2. Persist：append-only 写 batch、decision、quarantine 和 event；重复 batch ID 幂等回放。
3. Apply：再次核对 1,030 行当前 hash 与 dry-run 一致；若漂移则整批 BLOCKED。确认 ASSIGN=0 后只追加执行事件。
4. Verify：行数、业务表聚合 hash、NULL 计数均与基线一致；quarantine=37；栖月汇候选/业务行不得增加。
5. Rollback 演练：仅回滚本 batch 的 ledger 执行状态，不删除 append-only历史；由于业务 DML=0，业务表必须天然保持原 hash。

## 5. 文件范围

| 文件 | 动作 |
|---|---|
| `aos_api/object_runtime_ownership.py` | 只读 planner、持久化、approve/apply/verify；禁止 ASSIGN |
| `scripts/tenant_object_runtime_ownership.py` | dry-run/plan/approve/apply/verify CLI |
| `tests/tenant_isolation/test_ti3_e3_object_runtime_ownership.py` | 决策计数、漂移阻断、职责分离、零业务 DML |
| `tenant_schema_lint.py` | 增加 E3 决策/隔离计数只读报告 |

## 6. 退出门

1. 实库 dry-run 精确得到 total=1,030、NO_ACTION=993、QUARANTINE=37、ASSIGN=0、BLOCKED=0。
2. 备份在 Git 外，mode 600，记录大小/SHA256；恢复库 plan/apply/verify GREEN。
3. 共享非生产最终 batch 完成职责分离；9 表逐表行数、业务 hash、scope NULL 计数零变化。
4. 37 条未知归属全部进入 append-only quarantine，正常租户读取继续不可见。
5. Alembic 仍为 `228ti3e1expand`；FK 仍 NOT VALID；RLS 未开启；三张 Ontology 模板无变化。
6. Tenant Isolation 与 Object/Graph/Draft/Wiki 累计 GREEN；五分支同步。

## 7. 下一门

E3 GREEN 后进入 E4：只验证不会被 37 条 NULL scope 阻断的工作区 FK（NULL 对 FK 合法），同时单独证明 993 条完整 scope 无父断链。不得以 E4 Validate 冒充历史归属已恢复。之后 E5 才做全面 Read Switch，E6 RLS，E7 Contract。

## 8. 完成记录

- 共享实盘 dry-run：total=1,030、NO_ACTION=993、QUARANTINE=37、ASSIGN/BLOCKED=0；source snapshot `efbc1fc7…fcde`。
- Git 外备份：`/private/var/tmp/aos-ti3-e3.ZH8MTl/aos-meta-before.dump`，1,656,851 bytes，mode 600，SHA256 `5ed0331c02b3181faabdd7dde17656945fe05479a05eb1626ea66c62cf108915`。
- 恢复库 batch `75da9e3e-601e-590a-acb2-13487d2c636e`：approve/apply/verify/rollback GREEN，verified=1,030、quarantine=37、businessRowsUpdated=0；临时恢复库已删除。
- 共享最终 batch `7c82803d-1b18-5df0-9a52-46b8f831f376`：Planner/Approver/Executor/Verifier 分离，apply/verify GREEN，verified=1,030、quarantine=37、businessRowsUpdated=0。
- 专项 2 passed；Tenant Isolation 109 passed、7 skipped；五分支同步至 `21f8803`。
