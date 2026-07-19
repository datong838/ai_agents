# 108 · Metric Card 真组件方案

> 状态：✅ 已落地（方案先行）  
> 前置：[`106`](./106-Graph与ActionForm真组件方案.md) · [`102`](./102-Widget运行时挂载方案.md) · T08  
> 索引：[`00`](./00-技术方案索引.md) v1.0.77

---

## 1. 目标

将 `metric-card` 从 stub 升为 **真指标卡**：读 `POST /v1/object-sets/query` 行数，展示总数 + 按字段分桶（默认 `status`）。

| pluginId | canvasKind | runtime |
| --- | --- | --- |
| `metric-card` | `metric` | `inproc` |

---

## 2. 规则

1. 配置：`objectType`（默认 WorkOrder）· `groupBy`（默认 status）· 可选 `site` 过滤（与 Filter 对齐时可手填）。  
2. 旧 Layout：`kind=stub` + `pluginId=metric-card` → `resolveRenderKind` → `metric`。  
3. **不做**时序图 / COP 真推送；诚实标注 `source=object-sets`。  
4. 不改 action/graph/P0 四种 widget。

---

## 3. 助手（可单测）

```ts
summarizeMetricRows(rows, groupBy) → { total, buckets: [{ label, count }] }
```

---

## 4. 自测

- install → palette `kind=metric` · `runtime=inproc` · `stub=false`  
- vitest：分桶合计 = total；resolveRenderKind  
- object-sets query 契约仍绿  

---

## 5. 明确不做

- 真 COP 订阅 / WebSocket 指标流  
- 自定义 SQL 指标  
