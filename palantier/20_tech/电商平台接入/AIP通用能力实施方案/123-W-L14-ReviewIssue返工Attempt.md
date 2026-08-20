# 123 · W-L14 ReviewIssue 返工 Attempt 不被跳过

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L14** · 上游 W4-04 ADR 35  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l14-review-return-attempt/`  
> 边界：仅 `aos-platform-w1-aip`；不改 w2

## 1. 目标（本波近场）

1. **latest-attempt 执行语义**：`complete_run` 只认每个 `stepKey` 的**最高 attempt** 是否 `succeeded`  
2. **return → attempt N+1 可认领**：attempt 1 succeeded 后 return，`claim_step` 认领 N+1  
3. **新 attempt exact 输入**：追加 Issue / ReturnDecision / Artifact exact refs  
4. **ReturnDecision 可读**：`GET .../return-decisions` list/get

## 2. 不做（本波）

- 完整 InvalidationSet / ReuseDecision DAG  
- ruleRef / resolution 全量校验与 event payload 可读化  
- 独立 review 权限门  
- LineageSourceKind 新枚举迁移

## 3. 落地

| 能力 | 位置 |
|---|---|
| latest-attempt complete | `aip_task_store.complete_run` |
| repair input_refs | `return_review_issue` |
| Decision 读模型 | `list_return_decisions` / `get_return_decision` + router |

## 4. 验收

- [x] succeeded → return → attempt 2 queued；claim 得到 attempt=2  
- [x] complete_run 在 latest=queued 时失败关闭  
- [x] 新 attempt `input_refs` 含 ReviewIssue + ReturnDecision + Artifact  
- [x] ReturnDecision list/get 可用

## 5. 验证

`pytest test_w_l14_review_return_attempt.py` + w2c return → **2 passed**
