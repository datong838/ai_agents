# 121 · W-L12 HandoffDecisionRevision 与 Envelope 分层

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L12** · 上游 W-L3 / W3-06 ADR 94  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l12-handoff-decision/`  
> 边界：仅 `aos-platform-w1-aip`；不改 w2 ModuleHandoffCompiler / Workshop BFF  
> 代码 HEAD：`974d692`（w1-aip）

## 1. 目标

1. 在 Envelope `consumed` 之后，追加独立 append-only `HandoffDecisionRevision`  
   - `accepted` / `rejected` / `request_more` / `returned`  
2. Decision **不改写** Envelope 传输状态；consume 仍是一次性终态  
3. API：`POST/GET /v1/aip/handoffs/{handoffId}/decisions` · `GET .../decisions/{decisionId}`  
4. 幂等 CAS；`rejected` 不取消来源 Task；`accepted` 不冒充下游已执行

## 2. 不做

- ModuleHandoffCompiler / 八 Module BFF  
- request_more 自动签发新 Envelope（只记录决定 + gapCodes；新 Envelope 仍走既有 issue）  
- 前端 Drawer 时间线 UI

## 3. 门禁（已 GREEN）

- Envelope 非 `consumed` → 422  
- 终态决定（accepted/rejected/returned）后再写 → 409（幂等重放除外）  
- `request_more` 后仅允许 `returned`

## 4. 验收

- issue→consume→accepted；Envelope.status 仍为 consumed  
- request_more→returned；跨租户 404  
- pytest W-L12 + handoff API 通过
