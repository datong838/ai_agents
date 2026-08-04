# 228 · TI-2 E3 Module 身份可逆回填实施方案

> 版本：v1.1 · 2026-08-04
> 状态：GREEN（代码 `8e57c8a`，共享非生产最终 batch 已 verify）
> 前置：TI-2 E1 `e95ae45`、E2 `472728e` GREEN；Alembic `228ti2e1expand`

## 0. Rules

先方案后代码；仅处理已有强 scope 的 Module 族；稳定身份必须可重复计算；无父 Module 的子记录不猜测、不删除，进入 quarantine；复用 TI-1 E3 append-only batch/decision/event/quarantine ledger；先备份和 dry-run，再由不同角色 approve/apply/verify；必须完成 rollback 演练后再执行最终非生产 apply；不改旧主键、不设 NOT NULL、不 Validate FK、不启用 RLS、不连接微商城。

## 1. 实库基线

2026-08-04 对共享非生产 PostgreSQL 只读实扫：

| 资源 | 总行 | module_pk=NULL | 精确父关联 |
|---|---:|---:|---:|
| `meta_module` | 160 | 160 | 160 |
| `module_canvas_config` | 9 | 9 | 9 |
| `module_deployment` | 29 | 29 | 29 |
| `module_events` | 262 | 262 | 260 |
| `module_interface` | 9 | 9 | 9 |
| `module_query` | 22 | 22 | 22 |
| `module_variable` | 25 | 25 | 25 |
| `module_widget_instance` | 108 | 108 | 108 |

`meta_module` 分布为 `dev-org/dev-project=159`、`dev-org/prj-ops=1`，栖月汇为 0。两条 `module_events`（legacy module_id=`order-mgmt`）找不到同 scope 父 Module，必须 quarantine。7 张子表合计 464 行，其中可确定回填集合为 462 行；因此本波 ASSIGN 总数为 160 个父 Module + 462 个子记录 = 622。E1 的 644 行总量还包含不使用 module_pk 的 Theme 3 行与 Widget Catalog 17 行，不得混入 E3 算术。

## 2. 稳定身份规则

- `module_id = meta_module.id`：仅兼容复制，不改旧 `id`。
- `module_pk = UUIDv5(FIXED_NAMESPACE, "org_id/project_id/legacy_module_id")`。
- 固定 namespace 写入代码常量并由测试冻结；相同输入跨进程得到相同 UUID，不使用随机 UUID。
- 子资源只允许通过 `(org_id, project_id, module_id) = (parent.org_id, parent.project_id, parent.id)` 精确继承父 `module_pk`。
- `template_id/template_version/installation_id` 不可由历史记录可靠推导，本波保持 NULL；不得把 module_id 冒充模板坐标。

## 3. Ledger 与执行状态机

复用 TI-1 E3 表：

- `tenant_backfill_batch`：TI-2 E3 batch，mode=`NON_PROD`。
- `tenant_ownership_decision`：每父 Module 和每子记录一项；可回填为 `ASSIGN/A`，孤儿为 `QUARANTINE/X`。
- `tenant_quarantine_record`：保存两条孤儿事件的脱敏 key hash，不保存业务内容。
- `tenant_backfill_batch_event` / `tenant_ownership_decision_event`：PLANNED → APPROVED → EXECUTING → COMPLETED，及 APPLIED/VERIFIED/ROLLED_BACK。

角色必须分离：PLANNER、APPROVER、EXECUTOR、VERIFIER 的 actor hash 不得复用。所有 key、before/after/evidence 均为 canonical hash。

## 4. 执行算法

### 4.1 Dry-run

1. 取 advisory transaction lock。
2. 冻结行数、scope 分布、旧 ID、NULL 状态和逐记录 before hash。
3. 计算 622 条 ASSIGN 决策（160+462）与 2 条 QUARANTINE 决策。
4. 检查 module_pk UUID 碰撞、父关联多义、非 NULL 冲突、栖月汇候选数；任一异常 BLOCKED。
5. 持久化 append-only ledger，输出脱敏 JSON 摘要。

### 4.2 Apply/Verify

- 父表采用 compare-and-set：仅当 `module_pk IS NULL AND module_id IS NULL` 且 before hash 匹配时填写。
- 子表仅当 `module_pk IS NULL` 且精确父关联及 before hash 匹配时填写。
- 两条孤儿事件保持原行和 NULL module_pk，不创建假父记录。
- Apply 全部在一个事务内；任一冲突不做部分提交。
- Verify 对 622 个 APPLIED after hash、父子 module_pk 一致性、总行数守恒、栖月汇 0、quarantine 2 逐项检查。

### 4.3 Rollback 演练

- 仅回滚本 batch 的 APPLIED 行，且当前 after hash 与 ledger 完全一致。
- 父恢复 `module_pk=NULL,module_id=NULL`；子恢复 `module_pk=NULL`。
- 行数和非身份字段 hash 必须与 dry-run 前一致。
- 先在恢复库执行完整 apply/verify/rollback；共享非生产先完成真实备份，再执行一次 apply/verify/rollback 演练，最后使用新 batch 做最终 apply/verify。

## 5. 文件范围

| 文件 | 动作 |
|---|---|
| `aos_api/module_identity_backfill.py` | planner、ledger、角色分离、apply/verify/rollback |
| `scripts/tenant_module_identity_backfill.py` | dry-run/approve/apply/verify/rollback CLI |
| `tests/tenant_isolation/test_ti2_e3_module_identity_backfill.py` | 确定性、孤儿 quarantine、冲突失败关闭、可逆性 |
| `tenant_schema_lint.py` | E3 只读数据状态报告；不改变 E1 DDL 断言 |

本波不修改 Router、Web、Module API DTO、旧 PK/FK、Overlay/Profile/Preference，也不增加平台 Connector。

## 6. 退出门

1. dry-run 精确得到 ASSIGN=622、QUARANTINE=2，栖月汇候选=0。
2. 备份文件 Git 外、权限 600、记录 SHA256；恢复库演练 GREEN。
3. 共享非生产 apply/verify/rollback 后 identity NULL 计数回到基线；最终新 batch apply/verify 后父 160、子 462 非 NULL，孤儿 2 仍 NULL。
4. 8 张表总行数逐表不变；非身份字段聚合 hash 不变。
5. 所有 TI-2 FK 仍 NOT VALID；Alembic 仍为 `228ti2e1expand`；RLS 仍为 0。
6. 租户隔离、Module/Workshop 累计测试 GREEN；五分支同 HEAD。

## 7. E3 后边界

E3 只建立可验证身份，不切读、不解除旧全局 PK。因此 APP-04 同 module_id 双租户共存和 APP-05 卸载继续未完成。下一门为 E4 Validate：仅在 quarantine 不属于 FK 目标或被明确排除后验证可验证约束；随后 E5 才允许按 module_pk 读切换。

## 8. 完成记录

- 只读 dry-run：parent=160、child=464、ASSIGN=622、QUARANTINE=2、BLOCKED=0；栖月汇候选 0。
- Git 外备份：`/private/var/tmp/aos-ti2-e3.uN6mtv/aos-meta-before.dump`，899051 bytes，mode 600，SHA256 `8510931ac59ee84dc98c82e015507a8118f682f88741b98f4fb9ec0ac99bb4e8`。
- 恢复库首次 rollback 暴露父先于子导致 FK 拦截；代码 `9502acf` 改为子先父后并新增有子记录回归。重跑 apply/verify/rollback 均为 622 GREEN，临时恢复库已删除。
- 共享非生产 drill batch `5932fb43-2ff8-50e9-ba4b-92e1b4d53f7e` 完成 622/622/622，回滚后身份计数归零。
- 最终 batch `f3edf8d9-8cbf-5b5f-8f3c-4a541f240cdd` 完成 apply=622、verify=622；父 160、子 462 非 NULL，2 个 orphan Event 保持 NULL/quarantine。
- 新写持续性：Module 与 7 类子资源在存在父实例时写入同一稳定 module_pk；124 项租户/Workshop 累计 GREEN。
- 详细证据：`evidence/tenant-isolation/2026-08-04-TI-2-E3-Module身份可逆回填证据.md`。
