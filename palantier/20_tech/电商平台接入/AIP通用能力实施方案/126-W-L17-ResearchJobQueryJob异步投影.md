# 126 · W-L17 ResearchJob/QueryJob list + cancel + Async 投影

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L17** · 上游 W4-07 ADR 38  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l17-async-jobs/`  
> 边界：仅 `aos-platform-w1-aip`；不合并三套 Store

## 1. 目标

1. ResearchJob **list** + **cancel**（幂等 command receipt；未提交可直接 cancelled；已提交 cancelRequested≠已停）  
2. **resumability=unsupported** 明示；retry = 新建 Job 并挂 `retryOf`（不伪装续跑）  
3. QueryJob **list**  
4. 只读 **AsyncJobProjection** 汇聚 ResearchJob + QueryJob（不回写）  
5. 工具面板不得把本地 query 冒充 ResearchJob（投影 `authorityType` + `query_job_is_not_research_job`）

## 2. 不做

- 完整 Provider adapter cancel 接线（无 adapter 时 cancel 进 unknown/reconcile 语义）  
- KnowledgePipeline 并入投影写命令  
- 新 AsyncJob 权威表替代三套生命周期

## 3. 实现要点

- Migration `aip11_001`：`aip_research_job_command_receipt`；**放宽** `UNIQUE(run_id,step_key)` 以允许 retry 同 step 多 Job  
- API：`GET /v1/aip/research-authority/jobs`、`POST .../cancel`、`POST .../retry`  
- API：`GET /v1/aip/analyst/query-jobs`  
- API：`GET /v1/aip/async-jobs` 只读投影

## 4. 验收

- [x] GET research jobs list / POST cancel / POST retry  
- [x] GET query-jobs list  
- [x] GET async-jobs 投影只读  
- [x] pytest GREEN（`test_w_l17_async_jobs.py` + research/query 回归）
