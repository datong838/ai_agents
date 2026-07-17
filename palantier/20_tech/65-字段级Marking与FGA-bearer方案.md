# 65 · 字段级 Marking ↔ FGA bearer

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #3 — 字段级 Marking ↔ FGA bearer  
> **对齐**：[52](52-TX.4字段级Marking-MVP方案.md) · [63](63-OpenFGA与Markings组合判定方案.md) · [61](61-OpenFGA生产模型扩展.md)  
> **工程**：`aos_api/marking.py` · ontology/object_sets/写路径传 `conn` · 种子 · 单测  
> **硬规则**：与对象级同一开关 `AOS_AUTHZ_MARKING_BEARER`；无 conn / 关开关 → 行为 = [52] JWT-only；admin 旁路

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | 扩 `can_see_field` / `ensure_field_writes`；调用方传 conn |
| 不影响主路径 | 无 bearer 时脱敏/写拒与今相同 |
| 诚实 | 字段级 OR bearer；非 UI 逐格产品 |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| 读脱敏：`can_see_field` = JWT ∪ FGA `marking#bearer` | 改 OpenFGA 模型 |
| 写校验：`ensure_field_writes` 传 conn → 走 [63] `ensure_markings` | 字段审计 UI |
| 种子 `user:field-bearer#bearer@marking:secret` → 可见 `internalCost` | 强制每人起 OpenFGA |
| 关 `AOS_AUTHZ_MARKING_BEARER=0` → 字段仍仅 JWT | 对象级公式变更 |

---

## 2. 公式

```
field_ok(labels) =
  admin
  OR ∀ m ∈ labels: m ∈ JWT.markings OR (BEARER=1 ∧ bearer(m))

读：!field_ok → 剔除字段 + _redactedFields
写：proposed 含受限字段且 !field_ok → 403
```

与 [63] 共用开关与 `user_has_marking_bearer`。

---

## 3. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../65-*.md` | 本文 |
| `marking.py` | `can_see_field`/`redact`/`apply`/`ensure_field_writes` + `conn` |
| `ontology.py` · `object_sets.py` | 传 conn |
| `actions`/`drafts`/`runtime_write` | 传 conn |
| `db.py` | field-bearer 种子 |
| `tests/test_field_marking_fga.py` | 组合测 |
| 26/31/00/27 | 回写 |

---

## 4. 自测

- [x] 无 secret JWT → internalCost 仍 redact（回归）  
- [x] field-bearer + JWT public → 可见 internalCost  
- [x] BEARER=0 → field-bearer 仍 redact  
- [x] 写路径 bearer 可写 / 无关则 403  
- [x] test_field_marking 既有绿  

---

*v1.0*
