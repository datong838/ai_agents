# 120 · W-L11 ProductionContextRevision 四合同 CAS 冻结

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L11** · 上游 W3-04 / 93 ADR / W-L9/L10  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l11-production-context-freeze/`  
> 边界：仅 `aos-platform-w1-aip`；不改 w2 Workshop `ecommerceWorkshopFreeze` 适配器  
> 代码 HEAD：`c509541`（w1-aip）

## 1. 目标

1. AIP L0 新增 append-only `ProductionContextRevision`：一次事务复验并冻结四 exact refs  
   - TaskBriefRevision（frozen）  
   - EvidenceBundleRevision（complete + fresh，且未 revoke）  
   - EvalContractRevision（frozen）  
   - ResponsibilityPlanRevision（frozen exact；assignee 运营就绪留给 W-L4/Start）  
2. API：`POST .../production-contexts/freeze` · `GET` · `list`；幂等 CAS；不复制四对象 payload  
3. `ProductionStart` **必须**携带同一 `productionContextRef`，并与 Preview 内四合同 refs 对齐

## 2. 不做

- Workshop module freeze command / BFF  
- Plan compile 消费 Context（留给 W3-05 / 后续）  
- preparation/profile/installation provenance 全量（本波允许空 provenance stub 字段）  
- Responsibility assignee SkillBinding 运营就绪复验（沿用 W-L4 / Start；本波只验 frozen exact）

## 3. 验收（已 GREEN）

- 缺任一 ref / lifecycle 不符 / Bundle revoked / coverage≠complete / freshness≠fresh → 不写 Context  
- 同 Idempotency-Key + 同 hash 重放同一 Context；异 hash → conflict  
- Start 缺 Context 或 Context 与 Preview 四合同漂移 → blocked

## 4. 风险

强制 Start 带 Context 会打破旧仅 Preview 的启动路径——符合 W3-04 顺序，属预期 fail-closed。
