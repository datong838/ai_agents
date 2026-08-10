# 228-AIP 任务编排、TAOR 与执行内核实施方案

> 状态：**评审通过 · v1.0 方案基线（仍不授权编码）**
> 对应阶段：AIP-1、AIP-2。

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
