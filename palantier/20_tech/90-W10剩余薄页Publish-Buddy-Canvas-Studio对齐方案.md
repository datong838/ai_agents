# 90 · W10 剩余薄页 Publish/Buddy/Canvas/Studio 蓝图对齐方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **蓝图**：`workshop-publish` · `workshop-aip-chat` · `workshop-canvas` · `agents`  
> **前置**：[84](84-蓝图与实现全面审计台账.md) · [85](85-P1数据WorkshopStudio蓝图对齐方案.md)

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 先方案后编码 | 本文 → 4 页 |
| 最小更改 | 只加深 UI 壳；不改 API |
| 禁 JSON 主面板 | 保持 PropGrid / 折叠 |

---

## 1. 缺口（用户截图）

| 页 | 缺口 | 落地 |
| --- | --- | --- |
| `/workshop/publish` | UI 浅 | 居中卡片 + 2×2 通道链接格 |
| `/workshop/buddy` | 缺 Module 嵌入框 | 表格 Module 框 + Assist 浮层 |
| `/workshop/canvas` | widget 密度 | 三栏壳 + Widget 调色板 |
| `/aip/studio` | UI 中 | 4 Tab + L2 门控 + Prompt chips |

---

## 2. 文件

| 文件 | 变更 |
| --- | --- |
| `PublishPage.tsx` | bp-publish-shell |
| `BuddyPage.tsx` | bp-module-frame + assist popover |
| `CanvasPage.tsx` | bp-canvas-shell + palette |
| `StudioPage.tsx` | BpTabs 四 Tab |
| `styles.css` | publish / module / canvas 样式 |

---

## 3. 验收

1. 四页主区对齐蓝图结构 ✅  
2. `npm test` 绿 ✅  

---

*v1.0*
