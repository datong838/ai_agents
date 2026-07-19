# 184m · TTL / 遗忘归档作业

> **版本**：v1.2 · 2026-07-19  
> **状态**：✅ 方案定稿 · **已编码**（M1-W2a）  
> **计划**：[180m](180m-M1后置闭环开发计划.md)  
> **对齐**：[25](25-LLM-Wiki启示与L2演进补丁.md) §4.3 · 179 ② T2.12  
> **实现**：`ttl_job.py` + `retention_jobs.py` · `/v1/ops/ttl/*` · `tests/test_retention_184m.py`

## 行为摘要

- Insight 内存店按 `AOS_INSIGHT_TTL_DAYS`（默认 90）软归档  
- `POST /v1/ops/ttl/run` 支持 dryRun；同步写 `object_lifecycle`（有 objectType/id 时）  
- 另扫 `obj_instance` 上 `retentionCandidate` / Insight* / `lifecycle.ttlDays`  
- 核心类型禁 `forgotten`  
- `graph_health.archiveCandidates` 读真实候选

## 自检

- [x] dry-run / archive / graph-health / forget deny

---

*v1.2 · 184m*
