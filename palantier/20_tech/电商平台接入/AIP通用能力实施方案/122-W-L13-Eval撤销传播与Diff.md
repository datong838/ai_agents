# 122 · W-L13 Eval 撤销传播 + 语义 Diff

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L13** · 上游 W4-03 ADR 34  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l13-eval-revoke-diff/`  
> 边界：仅 `aos-platform-w1-aip`；不改 w2

## 1. 目标

1. Publication **按 `publication_id` 聚合**最新事件；`revoked` 后 EvalContract readiness blocked  
2. ImpactPreview / Start 复核递归 Eval 动态依赖（不只看合同行 hash）  
3. 服务端语义 Diff：`GET .../eval-contracts/{id}/diff?fromRevision=&toRevision=`

## 2. 不做（本波）

- `AipEvalRunner` 全面改为仅 contract-driven（另开；本波不伪造同版跑数 GREEN）  
- Workshop Diff UI / Badge  
- ReleaseGate invalidate 独立 command 改造

## 3. 落地

| 能力 | 位置 |
|---|---|
| 聚合最新 Publication | `aip_production_contract_store._eval_blockers` → `EVAL_PUBLICATION_REVOKED` |
| Preview/Start 动态就绪 | `_preview_dependency_state` 追加 `EvalContractDynamicReadiness` + blockers |
| 语义 Diff | `diff_eval_contract` + `GET .../eval-contracts/{id}/diff` |

## 4. 验收

- [x] 绑定 published 后 revoke 同 publication → blockers 含 `EVAL_PUBLICATION_REVOKED`  
- [x] Diff 返回中文变更项；同 revision 拒绝  
- [x] Preview 路径复用 `_eval_blockers`（有 exact Publication 绑定时）

## 5. 验证

`pytest tests/aip/test_w_l13_eval_revoke_diff.py` → **2 passed**

## 6. 风险

旧「event_id 仍是 published」假绿路径关闭——符合 W4-03。
