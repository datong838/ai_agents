# 124 · W-L15 KnowledgeQuery 生产装配 + Memory 成熟度桥

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L15** · 上游 W4-05 ADR 37  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l15-knowledge-memory-factory/`  
> 边界：仅 `aos-platform-w1-aip`；不改 w2

## 1. 落地

| 能力 | 位置 |
|---|---|
| 生产 factory | `aip_memory_production_factory.py` |
| Router 装配 | `get_aip_memory_{governance,retrieval,search}_service` ≠ None |
| 成熟度桥 | `MaturityPage` → `/aip/memory-governance?view=candidates\|readiness` |

## 2. 验收

- [x] production getters ≠ None  
- [x] missing artifact / payload → LookupError / UNKNOWN PII（失败关闭）  
- [x] Explicit None override 仍 503；角色门 403 先于 provider  
- [x] 成熟度页深链 Memory 治理  

## 3. 验证

专项 pytest GREEN（factory + 503 override + role）
