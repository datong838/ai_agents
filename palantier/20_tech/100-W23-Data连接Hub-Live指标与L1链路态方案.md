# 100 · W23 Data 连接 Hub Live 指标与 L1 链路态

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[85](85-W6运营台Inbox与本体Discover蓝图对齐方案.md) · [97](97-W20-概览四域Live指标与控制面加深方案.md)  
> **约束**：只读 API · 不改 BFF · Apollo 不深化

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 先方案后代码 | 本文 → `DataPage.tsx` |
| 最小更改 | Hub Tab 增指标 · refresh 扩 fetch |
| 与概览一致 | WorkOrder 数来自 `/v1/demo/story` |

---

## 1. 范围

| API | Hub 指标 |
| --- | --- |
| `/v1/sources` · `/v1/syncs` | Source / Sync 计数 |
| `/v1/pipelines` · `/v1/media-sets` | Pipeline / Media 计数 |
| `/v1/datasets` · `/v1/builds` · `/v1/dlq` | L1 产物计数 |
| `/v1/demo/story` | WorkOrder 实例 · 种子态 |
| sync-routing | 保持现有探测 UI |

UI：`BpMetricGrid` + `BpStagePipeline`（① Connector → ④ Ontology 映射态）

---

## 2. 验收

1. ensure-seed 后 Hub 指标全 >0 ✅  
2. 无种子时 Banner 提示 ✅  
3. `npm test` 绿 ✅  

---

*v1.0*
