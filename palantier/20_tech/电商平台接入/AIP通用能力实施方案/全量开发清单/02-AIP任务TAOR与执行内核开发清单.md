# 02 AIP Task、TAOR 与执行内核开发清单

> 状态：**v1.1 · IMPLEMENTING（已获用户全量编码授权）**
> 上位依据：`../02-228-AIP任务编排TAOR与执行内核实施方案.md`
> 对应阶段：AIP-1、AIP-2；前置：01、14、15 GREEN。

## 0. 本轮实施基线与子波

- 基线 commit：`8a01222`；分支：仅 `m1`；远端与本地一致。
- 迁移 head：`o1ux2_001`；正向范围：仅 `org-org/dev-project`；`dev-org` 仅负向 canary。
- 既有无关未跟踪文件不纳入提交：`scripts/browser-pilot-verification/` 与三份历史 D5 evidence JSON。
- AIP-1A：02-01～02-04、02-11 的 Task/Plan/Run 基础 API；先完成迁移、FORCE RLS、scoped store、CAS/幂等、状态转换和路由替换。
- AIP-1B：02-05～02-10、02-12；接入精确 revision、四段证据、lease/heartbeat、checkpoint/pause/resume/rollback 与 ResearchJob 公共契约。
- AIP-1C：02-F1～02-F4；唯一 SDK、Logic Run Panel、七态交互、刷新恢复、浏览器与 EvidencePack。

停止条件：迁移出现第二 head、真实租户数据需破坏性回填、AIP-0 contract hash 漂移、跨租户可见、或必须重写 O1 公共契约时，立即停止当前子波。

### 实施状态

| 子波 | 状态 | 代码提交 | 当前证据 |
|---|---|---|---|
| AIP-1A | `IMPLEMENTED_GREEN` | `0077055` | 单 head `aip1_001`；Task/Plan/Run PostgreSQL authority；30 tests + 2 subtests GREEN |
| AIP-1B | `IN_PROGRESS` | — | TAOR/Observe/lease/checkpoint/recovery 待实施 |
| AIP-1C | `PENDING` | — | SDK/页面/浏览器/EvidencePack 待实施 |

## 1. 后端与数据工作包

| ID | 任务 | 主要文件边界 | 验收 |
|---|---|---|---|
| 02-01 | 冻结 Task/PlanRevision/TaskRun/StepRun/Checkpoint/Artifact/Evidence DTO 与状态机 | `aip_contracts.py`、OpenAPI | hash 与 AIP-0 一致，无第二枚举 |
| 02-02 | 设计并评审 PostgreSQL 表、组合唯一键、FK、FORCE RLS | `alembic/versions/*_aip_task_runtime.py` | expand 迁移、单 head、跨租户不可见 |
| 02-03 | 实现 scoped store、CAS、idempotency | `aip_task_store.py` | 并发创建/迁移只有一个成功 |
| 02-04 | 实现 Task/Plan/Run 服务及状态转换 | `aip_task_service.py` | 终态单调，旧批准不覆盖新 revision |
| 02-05 | TAOR 绑定精确 Logic/Agent/Skill/Model/Policy revision | `aip_taor_loop.py` | Run 可完整重放和解释 |
| 02-06 | 将 Observe 接入成功/失败/暂停主循环 | `aip_taor_loop.py`、hooks | 每步 Think/Act/Verify/Observe 有证据 |
| 02-07 | 默认关闭真实范围 Mock/fallback | `aip_logic_engine.py` | 未注册 adapter 明确失败 |
| 02-08 | 实现 worker lease/heartbeat/claim/重领 | runtime worker | 崩溃恢复不重复外部动作 |
| 02-09 | 实现 checkpoint/pause/resume/retry/rollback | checkpoint service | 重启恢复、schema version 兼容 |
| 02-10 | 实现 C1 ResearchJob 公共 Adapter 契约 | research adapter/reconciler | 幂等、乱序、callback 重放、unknown |
| 02-11 | 发布 `/v1/aip/tasks`、runs、timeline API | `routers/aip_tasks.py` | 统一错误/分页/receipt |
| 02-12 | 迁移 legacy 内存 Task/TAOR | compatibility/backfill | demo 可丢、配置可导出、伪业务不迁移 |

## 2. 前端工作包

- 02-F1：`apps/web/src/api/aipTasks/*` 生成/封装唯一 SDK，未知状态失败关闭。
- 02-F2：Logic Run Panel 绑定真实 TaskRun/timeline/checkpoint，不显示固定 trace。
- 02-F3：pause/resume/cancel/retry 显示 accepted 与最终状态差异；unknown 提供 reconcile 状态。
- 02-F4：刷新页面从服务端恢复，不以 localStorage 判完成。

## 3. 测试、证据与回滚

- 后端：状态机、CAS、幂等、双 worker lease、重启恢复、checkpoint 兼容、legacy fail-closed。
- 租户：缺 scope、错 scope、跨组织/工作区、对象引用越权均拒绝。
- ResearchJob：事件重复/乱序、callback 防重放、取消不确定、Artifact 损坏、provider 版本漂移。
- 浏览器：Task 创建→Plan→批准→运行→暂停→恢复→timeline；失败/unknown/取消均有可见证据。
- 回滚：切回兼容读路径并阻止新 Run；保留新表、Evidence、Receipt、Lineage，不反向删除历史。

## 4. 退出门

- [ ] 重启后全部 canonical 资源可回读；真实范围默认 Mock 不可达。
- [ ] 同幂等键不产生双 Task/Run；双 worker 不重复执行。
- [ ] 每个成功步骤都有四段证据，失败/unknown 不伪装成功。
- [ ] AIP-0 contract hash、OpenAPI、迁移、前端 SDK、浏览器和 EvidencePack 全部对账。
