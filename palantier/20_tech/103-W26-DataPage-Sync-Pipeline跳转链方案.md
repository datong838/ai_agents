# 103 · W26 DataPage Sync→Pipeline 跳转链

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[100](100-W23-Data连接Hub-Live指标与L1链路态方案.md) · [102](102-W25-蓝图审计P1收口与可演示冻结方案.md)  
> **约束**：最小 UX · 不改 API · 不深化 Apollo

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 先方案后编码 | 本文 → 3 文件 |
| 最小更改 | 只加跳转 · 可选 query 高亮 |
| 冻结期小改 | 增强 TB.8 彩排 L1 叙事 |

---

## 1. 问题

Hub 已有 `BpStagePipeline`，但 **② Sync → ③ Pipeline** 无法一键跳转；Source 详情 Sync 表与 Pipeline 列表 **断链**。

---

## 2. 方案

| 位置 | 变更 |
| --- | --- |
| `blueprintUi.tsx` | `BpStagePipeline` stage 可选 `href` |
| `DataPage.tsx` | Hub 阶段链 · Sync 表 action · Detail 关联 Pipeline |
| `s2/data.tsx` | `/data/pipelines?sourceId=` 过滤高亮 |

**链路语义：** `Sync.sourceId === Pipeline.sourceId === Source.id`

---

## 3. 涉及文件

```
apps/web/src/pages/s2/blueprintUi.tsx
apps/web/src/pages/DataPage.tsx
apps/web/src/pages/s2/data.tsx
```

---

## 4. 验收

1. Hub 点 ③ Pipeline → `/data/pipelines` ✅  
2. Hub 点 ② Sync → 锚点 `#data-syncs` ✅  
3. Source 详情 Sync 行 → `pipelines?sourceId=` ✅  
4. `npm test` 绿 ✅  

---

*v1.0*
