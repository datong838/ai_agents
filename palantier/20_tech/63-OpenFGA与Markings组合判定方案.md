# 63 · OpenFGA ↔ Markings 组合判定深化

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #2 — OpenFGA ↔ Markings 组合判定深化  
> **对齐**：[55](55-TX.4-Marking继承与OpenFGA-Facade方案.md) · [61](61-OpenFGA生产模型扩展.md) · [T-CROSS](T-CROSS-横切能力详细技术方案.md) §2 · [52](52-TX.4字段级Marking-MVP方案.md)  
> **工程**：`aos_api/marking.py` · `aos_api/openfga.py` · 种子 · 单测  
> **硬规则**：对象读仍 **AND**（Markings 过关 ∧ 有元组则 viewer）；Marking 标签可用 **JWT ∪ FGA bearer**；admin 旁路；字段脱敏默认仍仅 JWT（本刀不扩）

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | 仅深化 `ensure_markings` 的 bearer OR；不改 UI |
| 不影响主路径 | 无 bearer 元组时 = 今日 JWT-only；有 JWT marking 仍过 |
| 诚实 | 组合 = 标签 OR 关系化 bearer；非完整 ABAC 产品 |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| 对象读：`markings_ok ∧ viewer_ok` 写清并测 | 替换 Markings 引擎 |
| `markings_ok`：∀ m ∈ effective → m∈JWT **或** `user#bearer@marking:m` | 字段级 redact 走 FGA（后置） |
| 开关 `AOS_AUTHZ_MARKING_BEARER`（默认 **1**） | UI 策略编辑器 |
| 种子：`user:bearer-only` 仅 JWT public + bearer(restricted) 可进 wo-1003 | JWT 自动写 bearer 元组 |
| `GET /v1/authz/status` 增 `markingBearer` | 改 OpenFGA 模型 DSL |

---

## 2. 判定公式

```
effective = type ∪ instance ∪ 1-hop inherit   // [55]

markings_ok(m) =
  admin
  OR m ∈ principal.markings
  OR (AOS_AUTHZ_MARKING_BEARER=1 AND check(user, bearer, marking:m))

viewer_ok =
  无 object 元组
  OR admin
  OR check(user, viewer, object:Type:id)   // editor/owner 蕴含见 [61]

READ allow = markings_ok(all effective) AND viewer_ok
```

```
JWT markings ──┐
               ├─ OR ──► markings_ok ──┐
FGA bearer ────┘                       ├─ AND ──► allow
Object viewer (optional tuples) ───────┘
```

---

## 3. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../63-*.md` | 本文 |
| `marking.py` | `ensure_markings(..., conn=)` · bearer OR |
| `openfga.py` | `check_marking_bearer` · status 字段 |
| `db.py` 种子 | `user:bearer-only#bearer@marking:restricted` |
| 单测 | `test_marking_fga_combine.py` |
| 26/31/00/27 | 回写 |

---

## 4. 自测

- [x] JWT 有 restricted → wo-1003 仍 200（回归）  
- [x] JWT 仅 public、无 bearer → 403  
- [x] JWT 仅 public + bearer 元组 → 200（组合）  
- [x] `AOS_AUTHZ_MARKING_BEARER=0` → bearer 不生效  
- [x] wo-fga-demo 仍需 viewer（AND 不变）  
- [x] 与 [55]/[61] 交叉一致（combine+inherit 13 绿）

---

## 5. 风险

| 风险 | 缓解 |
| --- | --- |
| 过宽放行 | 默认仅补齐缺的 label；须显式 bearer 元组 |
| 远程 FGA 延迟 | 沿用 check 本地/远程回落策略 |

---

*v1.0*
