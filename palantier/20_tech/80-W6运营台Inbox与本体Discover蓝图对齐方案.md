# 80 · W6 运营台 Inbox 与本体 Discover 蓝图对齐方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[78](78-蓝图页面对齐差距台账与去演示Hub方案.md) §6 P1 · [79](79-W5概览与AIP-Draft-Lineage蓝图对齐方案.md)  
> **蓝图**：`workshop-module.html` · `ontology.html`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小 API | 复用 object-sets / objects / wiki / funnel / object-types |
| 禁 JSON 主面板 | Object View / Discover 用卡片与表格 |
| 保留已有能力 | Inbox Selection+Action；Ontology 创建 OT+分支 |

---

## 1. 范围

| 页 | 路径 | 蓝图区块 | 落地 |
| --- | --- | --- | --- |
| 运营台 | `/workshop/inbox` | 变量条 · Filter/Table/ObjectView 三栏 · Action | 重写 `InboxPage.tsx` |
| 本体主站 | `/ontology` | Discover 收藏/最近/表格 · OKF 横幅 · 浏览 | 重写 `OntologyPage.tsx` 结构 |

---

## 2. 组件

| 组件 | 文件 |
| --- | --- |
| `BpVarBar` · `BpWsGrid` · `BpObjectView` · `BpDiscoverCard` · `BpPropGrid` | `s2/blueprintUi.tsx` |
| 样式 | `styles.css` `.bp-ws-*` · `.bp-discover-*` |

---

## 3. 验收

1. Inbox 顶栏变量 chips + 三栏布局 ✅  
2. Object View 展示属性 + Wiki（有则显示）+ HITL Action ✅  
3. Ontology 首屏 Discover 区块 + 实例浏览（非 JSON 主面板）✅  
4. `npm test` 绿 ✅  

---

*v1.0*
