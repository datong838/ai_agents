# 118 · W-L9 EvidenceBundle Build Job + 服务端 coverage

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 / §10.4 **W-L9**  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l9-evidence-build-job/`  
> 代码：`aos-platform-w1-aip` · 分支 `w1-aip`（合入 `m1`）  
> 边界：仅 `aos-platform-w1-aip`；不改 w2

## 1. 目标（已兑现）

1. `POST /evidence-bundles/build`：服务端 Build Job 产出 EvidenceBundle
2. `requiredFactIds` ∩ Evidence `payload.factIds` → coverage/missing/freshness **服务端计算**
3. 客户端携带 `coverage`/`missing`/`freshness` → 校验拒绝（extra forbid）
4. 旧 `POST /evidence-bundles` 同契约（仅输入面，无客户端 coverage）

## 2. 不做

- 完整三层 Disclosure/Marking（W-L10）
- Mock Bundle 种子进权威租户

## 3. 算法

```text
provided = ∪ evidence.payload.factIds|facts
missing = requiredFactIds − provided
coverage = complete | partial | blocked
freshness = any(freshness_at < cutoffAt) → stale；blocked coverage → blocked
```

## 4. 改动面

| 路径 | 说明 |
|---|---|
| `aip_production_contracts.py` | `BuildEvidenceBundleRequest`；Create 去掉客户端 coverage |
| `aip_production_contract_store.py` | `build_evidence_bundle` + `_compute_evidence_bundle_coverage` |
| `routers/aip_production_contracts.py` | `/evidence-bundles/build` |
| `tests/test_w2a_*` | Build / 伪造拒绝 / complete 幂等 |

## 5. 验收

- pytest w2a store+api GREEN
- 直填 complete → 400/422
- 缺 fact → partial + missing

## 6. 风险

旧客户端直填 coverage 会 fail-closed——符合 W-L9。
