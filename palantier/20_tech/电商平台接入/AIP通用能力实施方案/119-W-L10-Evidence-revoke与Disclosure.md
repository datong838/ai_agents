# 119 · W-L10 Evidence 不可变/revoke + Disclosure/Marking

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L10** · 上游 W-L9 / W4-02  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l10-evidence-revoke-disclosure/`  
> 边界：仅 `aos-platform-w1-aip`；不改 w2  
> 代码 HEAD：`6aea0d1`（w1-aip）

## 1. 目标

1. EvidenceBundle **不可变**；revoke 走 append-only 事件，不改历史 revision 行
2. 三层 Disclosure 执行 API：`resolve` / `get`（L1 摘要 · L2 片段 · L3 scoped ref）
3. Bundle list/get 按 `principal.markings` fail-closed（get 缺 marking → 404 不泄露）
4. revoke 后 ImpactPreview 引用 / Disclosure 新裁决 → blocked

## 2. 不做

- Workshop Drawer UI
- 完整 license 策略引擎 / KnowledgeCitation 混用

## 3. 表

- `aip_evidence_bundle_revoke_event`（UNIQUE bundle+revision+hash）
- `aip_evidence_disclosure_decision`

## 4. API

```text
POST /v1/aip/production-contracts/evidence-bundles/{bundleId}/revoke
POST /v1/aip/evidence/disclosures/resolve
GET  /v1/aip/evidence/disclosures/{decisionId}
```

## 5. 验收（已 GREEN）

- revoke 后 GET 仍可读元数据且 `revoked=true`；新 disclosure blocked（`EVIDENCE_BUNDLE_REVOKED`）
- `marking=["secret"]` Bundle：Bearer dev list 过滤、get 404
- L1/L2（dev 有 public+restricted）allowed；L3 缺 secret → blocked
- 客户端不可自填 decision；幂等 replay 同 decisionId

## 6. 风险

旧「有 itemRefs 就能读正文」路径关闭——符合 W4-02。
