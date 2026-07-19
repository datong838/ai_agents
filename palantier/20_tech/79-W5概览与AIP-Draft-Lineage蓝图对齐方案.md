# 79 · W5 概览与 AIP Draft/Lineage 蓝图对齐方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[78](78-蓝图页面对齐差距台账与去演示Hub方案.md) §6 P0  
> **蓝图**：`foundry/html/index.html` · `aip-draft-inbox.html` · `aip-decision-lineage.html`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小 API | 复用 `/v1/aip/drafts` · `/v1/aip/lineage/{id}` · `/v1/demo/governance` |
| 禁 JSON 主面板 | Draft/Lineage 主区用 bp-ui 卡片/时间线 |
| 蓝图双对齐 | 区块顺序跟 HTML |

---

## 1. 范围

| 页 | 路径 | 蓝图要点 | 落地 |
| --- | --- | --- | --- |
| 概览 | `/` | 四域色带 panel + index tile grid | `OverviewDomainGrid` + 保留 StoryChain |
| Draft | `/aip/drafts` | 隔离 banner + 卡片队列 + 批准/驳回 | 重写 `DraftInboxPage` |
| Lineage | `/aip/lineage` | Trace 头 + 左竖线时间线 + 治理 + 链 | 重写 `DecisionLineagePage` |

---

## 2. 组件落点

| 文件 | 新增/改 |
| --- | --- |
| `s2/blueprintUi.tsx` | `BpDraftCard` · `BpLineageTimeline` · `BpDomainPanel` · `BpIndexTile` |
| `components/OverviewDomainGrid.tsx` | index 四域静态链 |
| `pages/DraftInboxPage.tsx` | 蓝图 Draft 队列 |
| `pages/s2/aip.tsx` | DecisionLineage 时间线 |
| `styles.css` | `.bp-domain-*` · `.bp-draft-*` · `.bp-lineage-*` |

---

## 3. 验收

1. `/aip/drafts` 无 `<pre>` JSON 主面板 ✅  
2. `/aip/lineage` 谱系以时间线展示 steps ✅  
3. `/` 含 Workshop/AIP/Ontology/数据/Apollo 色带域 ✅  
4. `npm test` 绿 ✅  

---

## 变更日志

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-18 | W5 P0 方案 |

---

*v1.0*
