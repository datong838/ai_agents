# 107 · W30 Canvas widget 密度蓝图对齐

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[102](102-W25-蓝图审计P1收口与可演示冻结方案.md) · `foundry/html/workshop-canvas.html`  
> **约束**：纯 UI · 不改 Module API · 预览区保留

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文 |
| 先方案后编码 | 本文 → CanvasPage + CSS |
| 最小更改 | Section 内 widget 示意 · 网格底纹 |
| 蓝图 | 对齐 dashed Section + 内嵌 Widget 块 |

---

## 1. 问题

78/84 停车场：**Canvas widget 密度** cosmetic。画布 Section 仅有操作按钮，缺 blueprint 内 **Filter/Table/Buddy/Overlay 示意块** 与 grid 底纹。

---

## 2. 方案

| 文件 | 变更 |
| --- | --- |
| `CanvasPage.tsx` | `WidgetPreview` · Section 中文标签 · Layout 树友好名 |
| `styles.css` | 画布 grid 底纹 · `bp-canvas-widget*` 密度块 |

---

## 3. 验收

1. `/workshop/canvas` Section 内可见 widget 示意 ✅  
2. 保存/拖拽/预览行为不变 ✅  
3. `npm test` 绿 ✅  

---

*v1.0*
