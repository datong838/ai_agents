# 91 · W14 Workshop 运行态链路对齐方案（Apollo 延后）

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **蓝图**：`workshop-module` · `workshop.html` · `index` 主链  
> **约束**：**Apollo 子页不深化** · 仅保留导航/诚实后置文案

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 先方案后编码 | 本文 → Inbox/Buddy/列表/主链 |
| 最小更改 | 不改 API · 不碰 Apollo 页逻辑 |
| Apollo 延后 | 概览/发布仅标注后置，不新开 Apollo 刀 |

---

## 1. 范围

| 项 | 文件 | 落地 |
| --- | --- | --- |
| Inbox 顶栏 + Module 框 | `InboxPage.tsx` | BpToolbar · bp-module-frame |
| Inbox→Buddy 上下文 | `InboxPage` + `BuddyPage` | `?order=&assist=1` |
| 应用列表入口感 | `WorkshopListPage.tsx` | BpHeroLink |
| 主链步骤卡片化 | `StoryChainPanel.tsx` | BpDiscoverCard |
| Apollo 诚实后置 | `OverviewDomainGrid` · `PublishPage` | hint 文案 |

---

## 2. 验收

1. Inbox 选中行 → Buddy 带 Selection ✅  
2. `npm test` 绿 ✅  

---

*v1.0*
