# W4-07 QueryJob、ResearchJob 与统一异步任务投影预检 ADR

> 状态：`AOS-000232_REVIEWED / IMPLEMENTATION_AUTHORIZED / CONSUMER_CLOSURE_IN_PROGRESS`
>
> 事实截面：AOS authority `AOS-000024`；证据 `.evidence/workshop/2026-08-14-w4-07-query-research-job-preflight.json`。

## 1. 审查结论

AOS 已有三套边界不同且各自合理的异步 authority：

- TaskRun/StepRun：AIP 内部执行，具备 Lease、Checkpoint、cancel/resume/unknown/reconcile；
- ResearchJob：C1 外部研究 Provider，具备 exact manifest/lineage、submission/event/artifact/delivery/reconcile Receipts；
- KnowledgePipelineRun：知识摄取管道，具备 partial、pause/resume、Checkpoint、Receipt 和 Candidate 输出。

三者不能因 UI 都显示“任务进度”就合并 Store。W4-07 的正确方向是“保留 authority + 统一只读投影 + 按类型提供受控命令”。

当前 ResearchJob 没有 partial、Checkpoint、resume/cancel command、list API、前端 SDK/恢复页面；虽然 Provider Protocol 定义了 cancel，生产服务也没有 adapter runtime 接线，默认 callback secret/artifact hash resolver 会失败关闭。KnowledgePipelineRun 不能冒充用户发起的长查询；TaskRun 也不能冒充外部 Provider ResearchJob。因此 W4-07 保持 `NOT_STARTED / IMPLEMENTATION_BLOCKED`。

## 2. Authority 与统一投影

新增只读 `AsyncJobProjection`，字段至少包括：

```text
jobRef(authority/type/id/version)
taskRef / subjectRefs / owner
status / progress / partialArtifactRefs
cancelability / resumability / reconcileRequired
checkpointRef / receiptRefs / lineageRef
startedAt / updatedAt / deadline / nextPollAt
blockedReasons / lastError / permissions
```

Projection 只汇聚 refs 和派生显示状态，不承接 command、不回写源 Store。状态映射保留原始 status 与 authority type，避免把 `partial`、`unknown`、`paused` 压成笼统“进行中”。

## 3. QueryJob 所有权

内部长查询优先复用 TaskRun/StepRun：当查询需要阶段、Lease、Checkpoint 和 Artifact 输出时，由 typed Query Stage/Capability 表达。只有在 TaskRun 无法表达独立排队、流式 partial 或查询调度语义时，才经 L0 评审新增 QueryJob authority；不得直接复制 ResearchJob 或 KnowledgePipeline 表。

外部多轮研究继续使用 ResearchJob。知识源周期摄取继续使用 KnowledgePipelineRun。产品统一的是用户观察和恢复入口，不是底层生命周期。

## 4. ResearchJob 必补接缝

1. 可信 Provider adapter runtime：submit/status/events/artifacts/cancel/health；
2. callback secret 与 artifact hash resolver 的生产 authority；
3. partial artifact/coverage receipt；
4. provider cursor/checkpoint 与 safe resume 或显式 retry-of-new-job；
5. cancel command、permission、idempotency 和 cancel outcome unknown/reconcile；
6. list/get、严格 SDK、refresh-by-job-ref UI；
7. deadline/timeout 后不盲重提，先 status/reconcile。

若 Provider 不支持 resume，UI 必须显示 `resumability=unsupported`；用户选择重试时创建新 Job 并引用 retryOf，不能伪装续跑原 Job。

## 5. UI 生命周期

统一 Job Drawer 根据 authority capability matrix 显示按钮。刷新只持有 scoped `jobRef`，从服务器恢复；partial Artifact 可查看但明确 incomplete/coverage。cancel 请求已受理不等于 Provider 已停止；timeout/unknown 显示 reconcile 状态和最后证据。

禁止客户端轮询失败后自动重新 submit。Watchdog/页面恢复只读取状态和触发经授权的 resume/reconcile command，不直接调用 Provider。

## 6. 验收门

- 三种 authority 的状态在 Projection 中无损映射，原始 refs、status、Receipt 可回读。
- ResearchJob Provider submit/callback/artifact/cancel 使用可信 resolver，nonce/signature/hash/tenant 负向门通过。
- partial 可持续追加且不冒充 succeeded；刷新能恢复 partial refs 和 checkpoint/cursor。
- cancel/reconcile 幂等；cancel timeout 进入 unknown，不重复提交外部副作用。
- 支持 resume 的 Provider 从 exact checkpoint 恢复；不支持者明确 retry-of 新 Job。
- 内部 Query Stage、外部 ResearchJob、KnowledgePipelineRun 的路由和命令不会交叉写 Store。
- 前端覆盖 loading/partial/paused/cancelled/unknown/reconcile/failed/succeeded 与无权限状态。

## 7. 明确废弃与禁止

- 废弃把 KnowledgePipelineRun 直接重命名成 QueryJob 的方案。
- 禁止创建覆盖三套生命周期的第二 AsyncJob authority。
- 禁止用 Provider Protocol 中“声明了 cancel”冒充 cancel 已生产接线。
- 禁止 callback secret/hash resolver 缺失时降级接受回调或 Artifact。
- 禁止页面断线后盲目重提 Job。

这些废弃项不削弱统一体验；它们通过统一投影保持体验一致，同时保存每种任务的真实语义和副作用边界。

## 8. AOS-000232 实施前复审（2026-08-25）

### 8.1 后续实现已覆盖的旧缺口

旧预检晚于当前代码事实。AIP W-L17 已交付 ResearchJob list/cancel/retry、QueryJob list 和只读 AsyncJobProjection：

1. ResearchJob 已有 PostgreSQL authority、list/get、cancel command receipt、`cancelRequested`、unknown/reconcile、retryOf 新 Job 与 `resumability=unsupported`；不把 retry 冒充 resume。
2. QueryJob 已有独立 append-only authority、list/get、start/result/cancel/timeout/fail/reconcile；不与 ResearchJob 共 Store。
3. AsyncJobProjection 已保留 `authorityType`，但当前只汇聚 ResearchJob 与 QueryJob，字段不足且没有 Web strict SDK/工作台消费。
4. KnowledgePipelineRun 已独立具备 queued/running/paused/partial/unknown、Checkpoint、Receipt 与 list/get；旧投影尚未把它纳入只读观察面。

因此本波不重建三套 Store，不新增第四套 AsyncJob authority，也不为了“resume”伪造 Provider checkpoint。真实 Provider adapter、callback secret 和 artifact resolver 缺失时继续显式 blocker；submitted cancel 只记录 intent 并进入 unknown，绝不宣称 Provider 已停止。

### 8.2 当前真实缺口与裁决

- 统一投影缺 KnowledgePipelineRun，且缺 raw/display status 分离、progress、partial refs、checkpoint、receipt refs、更新时间、权限与 blocker。
- ResearchJob 已有 Artifact/Delivery/Command receipts，可从 authority 派生 partial 与 receipt refs；没有可信 checkpoint 时 `checkpointRef=null`、`resumability=unsupported`。
- QueryJob 以 latest event sequence 和 result revision 形成 exact 只读 refs；不能冒充 ResearchJob 或 KnowledgePipeline。
- Workshop 只消费统一投影并按“原子 Skill → Logic 编排 → 数字同事 → 工作台贡献视图”披露上下文；不复制命令状态机、不自动 submit/retry/reconcile。

### 8.3 文件级实施清单

| 顺序 | 文件 | 最小改动 |
|---|---|---|
| 1 | `services/aos-api/aos_api/aip_research_job_store.py` | 增加只读 projection facts 查询，返回已有 Artifact/Delivery/Command receipt refs 与 authority 更新时间；不写新 Store。 |
| 2 | `services/aos-api/aos_api/aip_async_job_projection.py` | 将 ResearchJob、QueryJob、KnowledgePipelineRun 无损汇聚为丰富只读投影；保留 raw status、authority type、partial/checkpoint/receipt 与 blocker。 |
| 3 | `services/aos-api/aos_api/routers/aip_async_jobs.py` | 传入 Principal 角色，仅派生权限矩阵；不新增统一 command endpoint。 |
| 4 | `services/aos-api/tests/aip/test_w_l17_async_jobs.py` | 补三 authority 映射、partial/checkpoint/receipt、权限、unknown 与不交叉写 Store 测试。 |
| 5 | `apps/web/src/api/aipAsyncJobs.ts` 与测试 | 新增 strict parser/authoritative GET；拒绝租户、计数、状态、exact ref、权限矩阵漂移，不使用离线快照。 |
| 6 | `apps/web/src/components/workshop/AsyncJobDrawer.tsx` 与测试 | 新增统一 Job Drawer，诚实展示 partial/paused/unknown/reconcile/unsupported；刷新只读且不自动重提。 |
| 7 | `apps/web/src/components/workshop/AnalystPage.tsx` 及测试 | 在经营参谋贡献视图挂载 Drawer；未有 exact Skill/Logic/AgentRun 时保持 unknown，不把 Job authority 冒充数字同事。 |
| 8 | `scripts/export_openapi.py`、`packages/contracts/openapi/v1.generated.json`、`v1.inventory.json`、`services/aos-api/tests/test_openapi_contract.py` | 仅在结构计数实际变化时同步确定性合同守卫。 |
| 9 | `.evidence/workshop/2026-08-25-w4-07-query-research-job-lifecycle.json` | 记录专项、累计、内置浏览器与安全边界；不包含 Secret、Provider payload 或真实业务数据。 |

### 8.4 验收与副作用边界

- 后端专项同时证明三 authority 无损映射、租户隔离、partial 不冒充 succeeded、unknown 必须 reconcile、unsupported 不出现 resume。
- Web 覆盖 loading/empty/partial/paused/cancelled/unknown/failed/succeeded、刷新、严格漂移拒绝和键盘操作；涉及页面必须用内置浏览器对照既有 Workshop Analyst 视觉语言。
- 本波不 live apply migration、不注册/调用真实 Provider、不提交/取消/重试真实 Job、不发布、不写真实业务数据。
- 若真实 Provider runtime 未装配，代码与页面以 blocker/unsupported/unknown 关闭，不把外部缺口变成停工理由，也不伪造 operational GREEN。
