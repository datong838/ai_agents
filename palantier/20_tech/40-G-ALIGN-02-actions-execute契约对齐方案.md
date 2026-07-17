# 40 · G-ALIGN-02 `actions/execute` 契约对齐方案

> **版本**：v1.0 · 2026-07-17  
> **任务**：关闭 [31](31-波次交付结果台账.md) **G-ALIGN-02**  
> **对齐**：[T-API](T-API-aos-api稳定契约.md) §2.1 · [T08](T08-Workshop工作台详细技术方案.md) · OpenAPI `/actions/execute` · 既有 T3.4 approve  
> **工程**：`aos-platform/services/aos-api`  
> **硬规则**：生产写仍只经 Draft 批准；execute 是契约入口，不是旁路直写

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文通过后再改 router |
| 最小更改 | 抽取 approve 核心复用；不改 Draft 表语义 |
| 契约优先 | Idempotency-Key **必填**；OpenAPI 去 501 |

---

## 1. 目标 / 非目标

| 目标 | 非目标 |
| --- | --- |
| 实现 `POST /v1/actions/execute` | 绕过 Draft 直写 `obj_instance` |
| Idempotency-Key 缺失 → **400** | 改 UI 全量接入（可后置） |
| `draftId` → 等同 approve | 复杂工作流引擎 |
| 无 draft 时：validate → 建 Draft；`autoApprove=true` 则接着批准 | Scenario 沙箱 |

---

## 2. 行为

```
POST /v1/actions/execute
  Header: Idempotency-Key (required)
  Body:
    draftId? | (actionTypeId + payload [+ objectType/objectId])
    autoApprove?: bool = false
    (+ X-Allow-Conflicts 同 approve)
```

| 输入 | 结果 |
| --- | --- |
| `draftId` | 调用与 approve 同一写核 → `productionWritten=true` |
| `actionTypeId`+payload · `autoApprove=false` | 建 Draft → `status=proposed` · **不写生产** |
| 同上 · `autoApprove=true` | 建 Draft + 立即批准 → 写生产 |
| 无 Key | `400 MISSING_IDEMPOTENCY_KEY` |

响应字段与 approve 对齐，并加 `route: "actions.execute"`。

---

## 3. 代码落点

| 路径 | 动作 |
| --- | --- |
| `routers/runtime_write.py` | 抽 `apply_draft_approval`；加 `execute_action` |
| `packages/contracts/openapi/v1.yaml` | 补 requestBody；去 501 |
| `tests/test_actions_execute.py` | Key 必填 · draft 批准 · HITL 仅提案 · 幂等 |
| `26` / `31` / `00` | G-ALIGN-02 关闭 |

---

## 4. 自测

- 无 Key → 400  
- create draft → execute(draftId) → obj 可读  
- execute(autoApprove=false) → proposed、生产未写  
- 同 Key 重放 → `idempotentReplay`  

---

## 5. 完成判定

- [x] OpenAPI 与实现一致  
- [x] 单测绿  
- [x] G-ALIGN-02 关闭入台账  

---

*v1.0 · 契约入口 · 写核不旁路*
