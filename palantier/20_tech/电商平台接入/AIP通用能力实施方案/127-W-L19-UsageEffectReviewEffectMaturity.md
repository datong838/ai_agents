# 127 · W-L19 Usage / EffectReview / EffectMaturity 可消费权威

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L19** · 上游 W6-09 ADR 57、方案 03/18  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l19-effect-review/`  
> 边界：仅 `aos-platform-w1-aip`；不宣称三领域 Module 闭环；不改 w2-workshop

## 1. 目标（本波近场切片）

1. **EffectReviewRevision** 版本化权威（非 Schema 字符串 / 非前端卡片）  
2. **EffectMaturity** 裁决：未到窗 → `immature`；禁止把 immature 当成 completed  
3. **accepted ≠ completed** 分轴：业务 accept 与效果 completed 独立字段  
4. **五轴独立投影**：item_outcome / action_outcome / usage_settlement / effect_maturity / handoff_decision 互不冒充  
5. 复用既有 Usage Receipt 只读挂载；本波不重做三 Module Usage bridge

## 2. 不做

- 达人/价格/客户 Module partial reducer 与领域 Usage 自动绑定（仍属 W6 阻断）  
- ModuleHandoffCompiler / accept-reject Receipt 全套（Handoff 已有 L12；本波只投影引用）  
- 用 UI 壳或 EffectReviewRef 字符串冒充 runtime authority

## 3. 数据与 API

- Migration `aip12_001`：`aip_effect_review_head` / `aip_effect_review_revision` / `aip_effect_maturity_decision`  
- `POST/GET /v1/aip/effect-authority/reviews`  
- `POST /v1/aip/effect-authority/maturity`  
- `GET /v1/aip/effect-authority/axes/{subjectId}` 五轴只读投影

## 4. 验收

- [x] 创建 EffectReview → 可读 revision；CAS 冲突 409  
- [x] Maturity 未满足样本/窗口 → immature，且 `completed=false`  
- [x] accept 记录不自动置 `effectCompleted`  
- [x] 五轴投影字段独立；pytest GREEN
