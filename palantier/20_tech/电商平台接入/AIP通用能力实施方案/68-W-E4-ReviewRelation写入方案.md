# 68 · W-E4 Artifact Relation + Review Issue 写入波

> 状态：`GREEN` · 2026-08-20  
> 上位：59 D6/W-E4  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-e4-review-relation/`  
> 目标：Relation 与 ReviewIssue 表非空；空态消失；只绑现网 artifact / eval_report_revision exact hash

## 验收

- [x] `bootstrap_w_e4_review_relation.py` → relationCount≥1、issueCount≥1（`org-org/dev-project`）  
- [x] W2-C stage template fail-closed 码对齐 `STAGE_SOURCE_MISSING_OR_DRIFTED`（resolver 已接线）  
- [x] L14 return/attempt 回归通过  

## 产出

| 项 | 值 |
|---|---|
| relationId | `artifact-relation-8bf33b8b20f74b9bb3d4` |
| issueId | `review-issue-5a620b9e1c5141d4a0b2` |
