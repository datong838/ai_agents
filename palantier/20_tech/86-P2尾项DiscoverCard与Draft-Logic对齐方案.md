# 86 · P2 尾项 DiscoverCard + Draft 分栏 + Logic 节点对齐方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[84](84-蓝图与实现全面审计台账.md) §7 P2 尾项  
> **蓝图**：`ontology.html` · `aip-capabilities` · `aip-draft-inbox` · `aip-logic`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 先方案后编码 | 本文 → 改组件/页 |
| 最小更改 | 扩展 `BpDiscoverCard` 支持 button 模式 |
| 禁 JSON 主面板 | Draft 预览 / Logic Debug 用 PropGrid + `<details>` |

---

## 1. 范围

| 项 | 文件 | 落地 |
| --- | --- | --- |
| BpDiscoverCard 复用 | `blueprintUi.tsx` + Ontology/Capability | onClick 模式 |
| Draft 左右分栏 | `DraftInboxPage.tsx` | 队列 + 详情 |
| Logic 节点样式 | `LogicPage.tsx` + `styles.css` | kind 色带 + Debug 折叠 |
| pipeline-doc-intel | — | 标注永久后置（84） |

---

## 2. 验收

1. Ontology 收藏 / Capability 卡片统一组件 ✅  
2. Draft 选中详情无 JSON 主预览 ✅  
3. Logic Debug 折叠 ✅  
4. `npm test` 绿 ✅  

---

*v1.0*
