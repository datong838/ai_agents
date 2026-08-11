# 228-AIP 任务编排、TAOR 与执行内核实施方案

> 状态：**IMPLEMENTING · v1.1 实时基线（已获用户全量编码授权）**
> 对应阶段：AIP-1、AIP-2。
>
> 2026-08-11 补充：外部 ResearchJob 契约 v1.2 已评审通过，不改变当前编码门禁。
>
> 2026-08-11 实施门更新：AIP-0 已以 `8a01222` 封板；用户随后明确授权清单内全部编码并要求串行 Loop。授权不取消租户、安全、证据和逐波复审门。

## 0.1 2026-08-11 实时代码裁决

- 当前 `/v1/aip/tasks` 仍由 `routers/phase3_aip_logic.py` 的进程内 `_tasks` 提供，且该组遗留 Task 路由没有 `require_principal`；它不是可保留的生产真源。
- `aip_taor_loop.py` 已具备 Think/Act/Verify 函数，但成功路径没有调用 `_observe`，Checkpoint 也只存在于 Task 内存对象。
- 已封板的 `aip_logic_graph_store.py`、`aip_logic_run_store.py` 是本阶段 PostgreSQL、scope、CAS、幂等和恢复实现的直接范式；不另建 ORM 或 Redis 真源。
- Alembic 当前唯一 head 为 `o1ux2_001`；AIP-1 迁移必须从该 head 线性展开，禁止生成并行 migration head。
- AIP-1 按三个可独立回退的子波串行实施：AIP-1A 数据模型/store/service/canonical API；AIP-1B TAOR/Observe/lease/checkpoint/recovery；AIP-1C SDK/页面/浏览器/EvidencePack。

## 0. 目标与非目标

目标是把现有 Task/TAOR/Logic 从“进程对象 + 可选 Harness + 旧 Mock”收敛为唯一可重放、可暂停、可审计的执行主链。非目标是不重做 Logic Canvas，不引入第二套 LangGraph 真源，不开放生产写回。

## 1. 现有能力映射

- 复用 `aip_logic_graph_store.py`、`aip_logic_run_store.py`、`aip_logic_publication_store.py` 的 revision/hash/CAS/证据模式。
- 复用 `aip_logic_dry_run_executor.py` 和 runtime adapters。
- 校正 `aip_task_model.py`、`aip_taor_loop.py`、`aip_hooks.py`、`aip_verify_skills.py`。
- 逐步淘汰 `aip_logic_engine.py` 的默认 Mock 和未持久化 flow/automation。

## 2. Canonical 模型

所有持久化记录必须包含 `org_id`、`project_id`；它们从认证上下文写入，API 不接受客户端覆盖。可变聚合包含 `revision`、`updated_at`，不可变事件包含 `event_id`、`payload_hash`、`created_at`、`created_by`。

| 对象 | 关键字段 |
|---|---|
| Task | id/type/title/status/goal/selection_ref/policy_revision/idempotency_key |
| PlanRevision | task_id/revision/steps/dependencies/risk/approval/status/hash |
| TaskRun | task_id/plan_revision/logic_graph_id/logic_revision/run_status/started/ended |
| Checkpoint | run_id/step_id/state_snapshot_ref/artifact_refs/resume_token |
| Artifact | type/content_ref/schema/source/evidence_refs/marking |
| Evidence | source_type/source_ref/observed_at/freshness/hash/redaction |
| StepRun | attempt/think_ref/action_ref/verify_ref/observe_ref/token/cost/error |

状态迁移必须由服务端 CAS 执行；Task status 与 Plan/Run status 分离。

## 3. 运行语义

```text
Create Task
 -> Generate PlanRevision
 -> Approve exact revision/hash
 -> Resolve Agent/Skill/Logic revision
 -> Think
 -> Act(read-only or ActionProposal)
 -> Verify
 -> Observe (必须执行并持久化)
 -> Checkpoint
 -> next / pause / fail / compensate
```

- 默认执行路径禁止 `_execute_mock`；开发演示只能在 `dev-org` 明确 feature flag 下运行并标 `source=demo`。
- LLM、Tool、Ontology Query、ActionProposal 统一走注册 Adapter；未注册即失败关闭。
- Think 只接收按需装配的 Wiki/Memory 引用，不注入全量文本。
- Observe 必须写入 StepRun、Artifact/Evidence refs 和下一步上下文；不能只改内存字典。

### 3.1 外部长任务 ResearchJob

外部研究/长任务统一作为 C1 Job Adapter 接入。AOS 先创建 `TaskRun` 与不可变执行清单，再提交外部任务；禁止外部系统事后反向补建 AOS Task，或把外部 checkpoint 当成第二套 Task store。

```text
AOS TaskRun
 -> submit(manifest_hash, idempotency_key, budget, scoped refs)
 -> external_execution_id
 -> status/events(cursor)
 -> artifacts + delivery receipt
 -> verify/hash/lineage
 -> complete | failed | cancelled | unknown/reconcile
```

Adapter 最小契约为 `submit/status/events/artifacts/cancel/health`，并满足：

- 提交以 `TaskRun + manifest_hash + idempotency_key` 幂等；同键不得产生两个有效外部执行。
- AOS worker lease、heartbeat 和预算仍是控制权威；外部状态只作为受验证的执行事实回传。
- 超时、断连或取消结果不确定时进入 `unknown/reconcile`，不得盲重试；产生外部副作用的步骤继续受 AIP-3 Receipt 对账约束。
- Checkpoint 只保存 provider、external execution id、event cursor、artifact refs 与 provider version，不保存外部凭据或不可验证内存对象。
- DeerFlow 是该契约的首个候选 provider，不是 AIP-1/AIP-2 的强制依赖；未安装或停用时 canonical Task/Run 历史仍可完整回读。
- 外部事件使用 `provider_execution_id + monotonic sequence/event_id` 去重；重复、乱序、迟到事件不得回退 canonical 终态。
- Callback 只触发主动回读，必须校验签名、时间戳、nonce、body hash 与 replay window；不直接相信 callback body 的 succeeded/artifact 信息。
- 输出 schema/hash、provider/binding version、traceparent 和 deadline 必须写入不可变 manifest；版本不兼容时阻止提交。

## 4. API 草案

```text
POST   /v1/aip/tasks
GET    /v1/aip/tasks/{taskId}
POST   /v1/aip/tasks/{taskId}/plans
POST   /v1/aip/tasks/{taskId}/plans/{revision}/approve
POST   /v1/aip/tasks/{taskId}/runs
POST   /v1/aip/task-runs/{runId}/pause
POST   /v1/aip/task-runs/{runId}/resume
POST   /v1/aip/task-runs/{runId}/rollback
GET    /v1/aip/task-runs/{runId}/timeline
```

写请求必须带 `Idempotency-Key`、预期 revision；响应返回 canonical receipt 与最新状态链接。

统一错误语义：`400 schema_invalid`、`401 unauthenticated`、`403 scope_or_policy_denied`、`404 not_found_in_scope`、`409 revision_or_idempotency_conflict`、`422 transition_blocked`、`429 budget_or_capacity_exceeded`、`503 dependency_unavailable`。跨租户资源不得通过错误差异泄漏是否存在。

## 5. 计划修改文件

```text
services/aos-api/alembic/versions/*_aip_task_runtime.py
services/aos-api/aos_api/aip_task_models.py
services/aos-api/aos_api/aip_task_store.py
services/aos-api/aos_api/aip_task_service.py
services/aos-api/aos_api/aip_taor_loop.py
services/aos-api/aos_api/aip_logic_engine.py
services/aos-api/aos_api/routers/aip_tasks.py
services/aos-api/tests/test_aip_task_*.py
services/aos-api/tests/tenant_isolation/test_aip_task_scope.py
apps/web/src/api/aipTasks/*
apps/web/src/pages/s2/LogicRunPanel.tsx
```

## 6. 开发拆分

- T0：OpenAPI/DTO/状态机/错误码冻结。
- T1：表、RLS、store、CAS/idempotency。
- T2：TAOR 接 canonical store，补 Observe，移除真实范围默认 Mock。
- T3：pause/resume/checkpoint/rollback，回滚只作用于本 run 资源。
- T4：Logic Canvas 绑定 TaskRun 与 timeline。
- T5：累计回归、跨租户 canary、重启恢复和浏览器验收。

## 7. 存储、并发与回滚

- `Task(org_id, project_id, id)`、`PlanRevision(task_id, revision)`、`TaskRun(task_id, idempotency_key)` 使用租户内唯一约束；所有查询同时受 RLS 和服务层 scope guard 约束。
- Worker 通过有期限 lease 领取 StepRun；心跳丢失只能重新领取未产生外部副作用的步骤，副作用步骤必须先按 ActionReceipt 对账。
- Checkpoint 保存 schema version 与引用，不序列化凭据、数据库连接或不可验证的内存对象。
- 迁移按 expand/backfill/compare/cutover/contract 执行；旧单例只读迁移，不能双写成第二真源。
- rollback 默认暂停新 run、切回上一兼容读路径并保留新表；禁止删除已生成的 Evidence、Receipt 和历史 Lineage。

## 8. 验收

1. 同一 idempotency key 不产生两个 Task/Run。
2. 重启后 Task、Plan、Run、Checkpoint、Artifact 可回读。
3. 批准 plan revision A 后修改为 B，A 的批准不覆盖 B。
4. 每个成功步骤均有 Think/Act/Verify/Observe 四段证据。
5. 未注册模型/工具、超时、撤权、旧 revision、跨租户均失败关闭。
6. `org-org` 真实数据不进入 `dev-org`，反向同样不可见。
7. 两个 worker 竞争同一步骤时只有一个 lease 生效；崩溃恢复不重复外部动作。
8. 旧 `/api/aip/*`、phase3 与 `/v1/aip/*` 的保留/转发/下线路由表有唯一 owner 和删除门。
9. 外部 Job 重复提交、断连、取消、超时与迟到回执均可收敛到唯一 TaskRun，且 provider 停用后历史 Artifact/Lineage 仍可解释。

## 9. 实施状态回写（2026-08-11）

- AIP-1A `IMPLEMENTED_GREEN`：提交 `0077055`，完成 PostgreSQL authority、FORCE RLS、Task/Plan/Run API、精确 hash 审批、CAS 与创建幂等。
- AIP-1B `IMPLEMENTED_GREEN`：提交 `1d7aeff`、`96df508`、`461c1a6`，完成 canonical TAOR、四段 Evidence、Artifact、Checkpoint、lease/heartbeat、控制幂等收据、unknown/reconcile fail-closed 以及 C1 ResearchJob 公共契约。
- legacy 收口：`org-org/dev-project` 不可再进入旧 Mock 或内存 Automation 创建；仅 `dev-org + AIP_DEMO_MOCK_ENABLED=1` 保留明确标记为非权威的兼容演示。
- 累计验证：59 tests + 2 subtests GREEN；OpenAPI、AIP contract 与 route inventory 已重新生成并通过双进程确定性检查。
- 尚未封板 AIP-1：AIP-1C SDK、Logic Run Panel、七态/unknown 交互、刷新恢复、浏览器验收与 EvidencePack 仍待完成。
