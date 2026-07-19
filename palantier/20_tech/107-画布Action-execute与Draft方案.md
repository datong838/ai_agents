# 107 · 画布 Action execute + Draft 方案

> 状态：✅ 已落地（方案先行）  
> 前置：[`106`](./106-Graph与ActionForm真组件方案.md) · T-API `POST /v1/actions/execute` · Draft HITL  
> 索引：[`00`](./00-技术方案索引.md) v1.0.76

---

## 1. 目标

在 Canvas **Action Form** 上补「提交 Draft」：走既有 `POST /v1/actions/execute`，**强制 Idempotency-Key**，默认 **HITL**（`autoApprove=false`），生产写仍须审批台批准。

| 按钮 | 行为 |
| --- | --- |
| 试跑校验 | 106 已有 · `POST /v1/actions/validate` |
| 提交 Draft | `execute` + `Idempotency-Key` · 创建 `proposed` Draft · **不**写 `obj_instance` |

---

## 2. 规则

1. 缺 `Idempotency-Key` → API 400（Host 已有）；前端每次提交生成新 key（`canvas-af-…`）。  
2. 画布默认 **禁止** `autoApprove=true`（防误写生产）；高级开关不做。  
3. 须带 `objectType` / `objectId`（配置面板可改；默认 `WorkOrder` + 可空则由后端生成）。  
4. 成功提示含 `draftId` + 链到 `/aip/drafts`。  
5. 不改 execute 后端语义；不改 Graph / metric-card。

---

## 3. 前端契约助手（可单测）

```ts
buildActionExecuteBody({ actionTypeId, objectType, objectId, payload, autoApprove?: false })
newCanvasIdempotencyKey()
```

---

## 4. 自测

- pytest：canvas 风格 execute → `productionWritten=false` · `status=proposed`  
- vitest：body 默认 `autoApprove=false` · key 非空唯一前缀  
- 缺 key 仍 400（既有回归）

---

## 5. 明确不做

- 画布内一键批准写生产  
- metric-card 真组件 → 见 [`108`](./108-MetricCard真组件方案.md)
