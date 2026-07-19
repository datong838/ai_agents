# 108 · W31 Schedules Cron 可视化蓝图对齐

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[85](85-P1数据WorkshopStudio蓝图对齐方案.md) · `foundry/html/schedules.html` · [107](107-W30-Canvas-widget密度蓝图对齐方案.md)  
> **约束**：纯 UI · 不改 `/v1/schedules` 契约

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文 |
| 先方案后编码 | 本文 → dataSchedules + CSS |
| 最小更改 | Cron 五段分解 · 预设高亮 · 下次运行卡 |
| 停车场收口 | 78/84 schedules cron 最后一项 cosmetic |

---

## 1. 问题

85 已有 Cron 预设与 Tab，但 **无五段字段可视化**、预设无选中态、「下次运行」仅 Banner 一行。

---

## 2. 方案

| 文件 | 变更 |
| --- | --- |
| `s2/dataSchedules.tsx` | `parseCronFields` · 字段网格 · 预设 active · 下次运行卡 |
| `styles.css` | `bp-cron-*` 样式 |

---

## 3. 验收

1. `/data/schedules` 五段 Cron 可见 ✅  
2. 预设按钮选中高亮 ✅  
3. `npm test` 绿 ✅  

---

*v1.0*
