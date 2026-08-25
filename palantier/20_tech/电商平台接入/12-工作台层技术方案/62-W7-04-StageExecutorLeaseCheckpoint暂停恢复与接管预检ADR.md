# W7-04 StageExecutor、Lease、Checkpoint、暂停恢复与接管预检 ADR

> 日期：2026-08-15；2026-08-25 现状复核并进入实施  
> 状态：`IN_PROGRESS / CANONICAL_RUNTIME_REUSE / NO_EXTERNAL_EFFECT / NO_RELEASE`

## 1. 决策

W7-04 只扩展 AIP canonical TaskRun/StepRun/Checkpoint，不建立媒体专用 StageRun 真源。执行权以 `TaskRun + stepKey + attempt` 唯一定位；每次 claim 或合法接管分配单调递增 fence。所有 heartbeat、阶段写、Checkpoint、完成和失败写同时校验 owner、lease expiry 与 fence，防止旧 worker 在接管后回写。

`TakeoverDecisionReceipt` 是追加事实，固定旧/新 owner、旧/新 fence、lease/heartbeat 健康证据、策略 exact ref、actor/reason、受影响 Stage/Artifact 与时间。接管不删除旧 lease、Checkpoint、attempt 或事件。

## 2. Checkpoint 与暂停恢复

Checkpoint 固定 Plan/Stage/attempt exact refs、输入 hash、已验证 Artifact refs、Provider request fingerprint、Usage/Receipt refs、checkpoint policy 与依赖快照，不保存大媒体正文，也不等于 Stage 成功。

暂停采用 `running → pausing → paused`：只有抵达模板声明的安全点，或已把可能发生的外部结果标为 unknown 并进入 reconcile，才能进入 paused。恢复与接管重新验证 template、Capability/assignee、Provider、Policy、license、budget、readiness 和输入 hash，生成不可变 reuse/invalidation decision；Checkpoint 存在不能自动证明可复用。

## 3. Provider 与竞态边界

Provider request fingerprint 由 run/step/attempt/input hash 确定。lease 在请求前过期可安全重取；请求后缺可信 Receipt 则进入 unknown/reconcile，禁止换 owner、换账号或换幂等键盲发。Capacity reservation、Usage 与 lease/attempt 通过 exact refs 关联，但继续使用各自 canonical authority。

## 4. 2026-08-25 独立现状复核

W7-03 已以 `d0851ad5` 完成并由 authority `AOS-000258` 投影为 GREEN，原“W7-03 未 GREEN”阻断已解除。当前仓库已具备两组必须复用、不得复制的 canonical authority：

1. AIP-1 `aip_task_run / aip_step_run / aip_checkpoint` 是唯一执行与断点真源；
2. W3-07 `aip_takeover_request / aip_takeover_decision_revision / aip_execution_assignment_head` 是唯一接管、审批、owner、lease 与 fence 真源。

现状缺口不是等待其他人交付，而是两组既有 authority 尚未闭合：普通 `claim_step` 未创建/推进 assignment head，TAOR 后续写只校验字符串 owner 与过期时间、不校验 fence；pause/resume 仍直接翻转 Task 状态；Checkpoint 只保存 `{stepRunId, stepKey, status}`；恢复没有 exact dependency/input hash 的不可变 reuse/invalidation 判定；Task Cockpit 也没有展示 owner/fence/safe-point/reconcile/Checkpoint 复用事实。

本波不提前实现 W7-07 Provider adapter，也不发真实 Provider 请求；`DEP-M9` 在本波按“可插拔 provider fingerprint + unknown/reconcile 边界”收敛为执行器合同，不再作为等待外部开发的停工理由。

## 5. 文件级实施清单

1. 新增 `w7_002` 迁移：在 canonical TaskRun/StepRun/Checkpoint 上增加暂停、fence、输入摘要、Provider fingerprint 与恢复快照字段；新增 append-only `aip_run_resume_decision_revision`，不新建 StageRun/媒体执行表。
2. 扩展 AIP 合同与 TaskStore：首次 claim 和安全重取均推进 assignment head 的单调 fence；heartbeat、TAOR phase、Checkpoint、complete/fail 必须携带并核验 fence；稳定 request fingerprint 由 run/step/attempt/input hash 派生。
3. 暂停采用 `running → pausing → paused`：无活跃 step 可直接 paused；存在活跃 step 时只登记 pausing，worker 到 checkpoint 才完成暂停；Provider outcome unknown 时维持 reconcile 失败关闭。
4. resume 复算 approved Plan、PlanStep、依赖与 input hash，写不可变 reuse/invalidation decision；漂移时拒绝恢复且不改运行状态。
5. W3-07 接管审批继续写唯一 assignment head，并同步 canonical StepRun 的 owner/lease/fence；旧 owner 的任何后续写因 fence 不匹配失败。
6. Task Cockpit 只读投影补 owner、fence、lease、safe-point、input hash、Provider fingerprint、Checkpoint reuse/reconcile 摘要；页面不暴露 Provider secret，不提供绕过审批的执行按钮。
7. 补齐专项、竞态、双租户、累计回归、OpenAPI/Router/Alembic、安全与内置浏览器三视口证据；不 apply migration、不调用 Provider、不产生外部副作用。

## 6. 兼容策略与验收门

- 旧调用方仅通过 `StepLease` 获得新 fence；本仓所有 canonical 调用点同波升级，不保留无 fence 写通道。
- 历史行的新字段允许兼容空值，但新 claim/checkpoint/resume 必须形成完整 v2 事实；UI 对历史空值显示“未建立”，不得显示为 0/健康。
- 继续保持“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图”：executor 执行 PlanStep 已绑定的 capability/assignee，不把 worker、Provider 或 Tool 重新命名为 Skill。
- 验收必须覆盖：旧 worker 接管后写入失败、活跃 lease 暂停进入 pausing、安全点落盘后 paused、resume 漂移失败关闭、unknown 不盲重试、Checkpoint hash 可复算、`org-org/dev-project` 正向与 `dev-org/dev-project` 隔离。

## 7. 历史预检事实

机器证据：`.evidence/workshop/2026-08-15-w7-04-stage-executor-lease-checkpoint-takeover-preflight.json`。

已有基础包括 TaskRun/StepRun、pause/resume、限时 lease、heartbeat、owner 校验、Checkpoint DTO/存储，以及“外部动作后 lease 过期转 unknown/reconcile”；generic Task runtime 12 项测试通过。

当时记录的 13 项缺口保留为历史基线；2026-08-25 复核后，W7-03、接管 Receipt 与 assignment head 已具备，其余缺口转为本波实施项，不再写作外部等待依赖。

## 8. 双轮复审

第一轮业务与生命周期：暂停不伪造静止、接管不抹除历史、unknown 不盲重试、用户可见 owner/fence/checkpoint/reconcile，`PASS`。

第二轮技术与安全：单一 runtime authority、attempt scope、fencing、CAS/幂等、不可变 Checkpoint、漂移复验与 fail-closed 完整；13 项缺口未误写为完成，无代码/迁移/真实租户/Provider 变更，`PASS`。

2026-08-25 第二轮复审结论：实施范围与 163/164、W7 上位方案一致；采用已有 W3-07 authority 可避免双真源，允许登记 Task Receipt/Lease 后开始最小实现。
