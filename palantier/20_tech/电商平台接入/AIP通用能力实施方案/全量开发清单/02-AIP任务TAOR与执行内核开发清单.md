# 02 AIP Task、TAOR 与执行内核开发清单

> 状态：**v1.2 · AIP-1 IMPLEMENTED_GREEN / AIP-2 PENDING（已获用户全量编码授权）**
> 上位依据：`../02-228-AIP任务编排TAOR与执行内核实施方案.md`
> 对应阶段：AIP-1、AIP-2；前置：01、14、15 GREEN。

## 0. 本轮实施基线与子波

- 当前基线 commit：`9bf5757`；分支：仅 `m1`；远端与本地一致。
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
| AIP-1B | `IMPLEMENTED_GREEN` | `1d7aeff`、`96df508`、`461c1a6` | canonical TAOR、四段证据、lease/heartbeat、checkpoint、控制幂等收据、C1 ResearchJob 契约及 legacy fail-closed；59 tests + 2 subtests GREEN |
| AIP-1C | `IMPLEMENTED_GREEN` | `9bf5757` | 唯一 SDK、权威 TaskRun 面板、服务端刷新恢复、七态控制、浏览器与跨租户 EvidencePack GREEN |

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

### AIP-1B 实施回写（2026-08-11）

- 02-05～02-06：`CanonicalTaorRunner` 只接受已批准的精确 PlanRevision；存在 capabilityRef 时必须绑定 revision。每个成功步骤均持久化 Think/Act/Verify/Observe 四段 Evidence，Observe 产物进入 `aip_artifact`，完成后生成 schema v1 Checkpoint。
- 02-07、02-12：真实组织 `org-org/dev-project` 的旧 `/v1/aip/logic/execute` 与内存 Automation 创建均失败关闭；Mock 仅在 `AIP_DEMO_MOCK_ENABLED=1 + dev-org` 时返回 `source=demo/nonAuthoritative=true`。旧 `get_controller()` 不再返回内存 TAOR 执行器。
- 02-08～02-09：StepRun 通过有期限 lease/heartbeat 领取；双 worker 只有一个成功。Act 前崩溃可安全重领，Act 后租约过期则 StepRun/TaskRun=`unknown`、Task=`paused`，等待 reconcile，禁止重复外部动作。start/pause/resume/cancel/rollback 使用 CAS，并在同 Run 的不可变 Evidence 内保存事务级幂等收据。
- 02-10：新增 C1 ResearchJob 公共 Adapter/Manifest/Event/Observation 契约；事件要求 execution id 一致、payload hash 正确、sequence 连续、event id 去重和终态单调。Callback 校验 timestamp、nonce、body hash、HMAC 和 replay window，回调只触发主动回读。
- 02-11：新增 5 个 Run 控制 API；OpenAPI 路由为 4083 rows / 4073 unique pairs / 2319 paths，AIP 路由无重复 owner。
- 验证：`tests/aip`、Task、legacy Logic、OpenAPI 与 router manifest 累计 `59 passed + 2 subtests`；真实正向测试范围为 `org-org/dev-project`，`dev-org` 只验证显式 demo/负向边界。

## 2. 前端工作包

- 02-F1：`apps/web/src/api/aipTasks/*` 生成/封装唯一 SDK，未知状态失败关闭。
- 02-F2：Logic Run Panel 绑定真实 TaskRun/timeline/checkpoint，不显示固定 trace。
- 02-F3：pause/resume/cancel/retry 显示 accepted 与最终状态差异；unknown 提供 reconcile 状态。
- 02-F4：刷新页面从服务端恢复，不以 localStorage 判完成。

### AIP-1C 编码顺序（已评审）

1. 后端补 `GET /v1/aip/task-runs?logic_graph_id=` 的 scoped discovery，只返回当前组织/工作区数据，并补 OpenAPI、路由真值和跨租户测试。
2. 建立 `apps/web/src/api/aipTasks/` 唯一 SDK，覆盖 Task、Plan、approve、Run、timeline、start/pause/resume/cancel/rollback；严格解析 DTO 与全部状态。
3. 在 Logic Canvas 增加权威 TaskRun 面板：可从当前已保存 Logic revision 创建 Task→Plan→批准→queued Run，并显示 accepted 后的服务端回读状态。
4. 控制按钮按服务端 Task/Run 版本进行 CAS；每次控制后回读 timeline。`unknown` 显示“结果待对账”并禁止重新执行动作。
5. 页面刷新按 Logic Graph ID 从服务端恢复最新 Run；失败/取消后的“重新执行”创建新 Task 链，不复活终态。
6. 完成 SDK/组件测试、TypeScript/build、真实租户浏览器点验、跨租户 canary 与 EvidencePack 后，才能把 AIP-1C 标为 GREEN。

## 3. 测试、证据与回滚

- 后端：状态机、CAS、幂等、双 worker lease、重启恢复、checkpoint 兼容、legacy fail-closed。
- 租户：缺 scope、错 scope、跨组织/工作区、对象引用越权均拒绝。
- ResearchJob：事件重复/乱序、callback 防重放、取消不确定、Artifact 损坏、provider 版本漂移。
- 浏览器：Task 创建→Plan→批准→运行→暂停→恢复→timeline；失败/unknown/取消均有可见证据。
- 回滚：切回兼容读路径并阻止新 Run；保留新表、Evidence、Receipt、Lineage，不反向删除历史。

## 4. 退出门

- [x] 重启后 AIP-1B canonical 资源可回读；真实范围默认 Mock 不可达。
- [x] 同幂等键不产生双 Task/Run/控制动作；双 worker 不重复执行。
- [x] 每个成功步骤都有四段证据，失败/unknown 不伪装成功。
- [x] AIP-0 contract hash、OpenAPI、迁移、前端 SDK、浏览器和 EvidencePack 全部对账。

### AIP-1C 实施回写（2026-08-11）

- 服务端新增按 `logic_graph_id` 的 scoped TaskRun discovery；`org-org/dev-project` 可回读当前 Graph 的 Run，`dev-org/dev-project` 对同一 Graph 返回空集合。
- `apps/web/src/api/aipTasks/` 成为 Task/Plan/Run/timeline/control 的唯一 SDK，未知状态和 Task/Plan/Run 引用不一致失败关闭。
- Logic Canvas 同时保留安全 Dry-Run 证据面板和权威 TaskRun 面板；两者明确分离。TaskRun 面板展示 queued/running/paused/succeeded/failed/cancelled/unknown，控制操作采用 Run/Task 双版本 CAS，并在 accepted 后回读 timeline。
- 真实浏览器在栖月汇租户创建 `logic-mso3quyh-2` 与 `run-4029db53c3b04c6c94ee`，点验 `queued → running → paused → running → cancelled`；页面刷新后仍恢复 cancelled，Evidence=4，浏览器控制台无错误。
- 验证：AIP 后端累计 60 tests（另有 2 个子进程确定性门）、前端定向 30 tests、TypeScript、Vite production build、OpenAPI 4084 rows / 4074 unique pairs / 2320 paths 全部通过。
