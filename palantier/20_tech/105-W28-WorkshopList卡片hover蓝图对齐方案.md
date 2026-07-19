# 105 · W28 WorkshopList 卡片 hover 蓝图对齐

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[102](102-W25-蓝图审计P1收口与可演示冻结方案.md) · `foundry/html/workshop.html`  
> **约束**：纯 CSS · 不改 API · 全局 `bp-discover-*` 复用

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文 |
| 先方案后编码 | 本文 → `styles.css` |
| 最小更改 | 仅 discover 卡片 hover |
| 蓝图 | 对齐 workshop.html `group-hover` 边框/标题变亮 |

---

## 1. 问题

78/84 停车场：**WorkshopList 卡片 hover** cosmetic。`WorkshopListPage` 用 `<Link class="bp-discover-card">`，但 hover 仅覆盖 `button`，且缺 `bp-discover-muted` 底色与标题/CTA 动效。

---

## 2. 方案

| 文件 | 变更 |
| --- | --- |
| `apps/web/src/styles.css` | `bp-discover-muted` 底色 · `a.bp-discover-card:hover` 抬升+标题/CTA · 与 violet 一致 |

受益页：`WorkshopListPage` · `DataPage` 向导 · `remainder` Discover 区。

---

## 3. 验收

1. `/workshop` 卡片 hover 边框变亮、轻微上浮 ✅  
2. 不影响 Inbox/Buddy 功能 ✅  
3. `npm test` 绿 ✅  

---

*v1.0*
