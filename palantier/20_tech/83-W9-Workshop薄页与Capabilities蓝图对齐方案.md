# 83 · W9 Workshop 薄页与 Capabilities 蓝图对齐方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[78](78-蓝图页面对齐差距台账与去演示Hub方案.md) · [82](82-W8-COP-ModelRouter-ObjectType7Tab蓝图对齐方案.md)  
> **蓝图**：`workshop-object-view` · `workshop-module-interface` · `workshop-events` · `aip-capabilities`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI 文案 |
| 先方案后编码 | 本文 → 再改 `apps/web` |
| 最小更改 | 复用 neighbors/wiki/webhooks/capabilities API |
| 禁 JSON 主面板 | 图谱/表格/卡片；调试 JSON 仅 `<details>` |

---

## 1. 范围

| 页 | 路径 | 蓝图要点 | API | 落地 |
| --- | --- | --- | --- | --- |
| 知识图谱 | `/workshop/graph` | Graph + Object View + Wiki | objects/neighbors/wiki | `GraphExplorerPage` |
| 模块接口 | `/workshop/module-interface` | I/O 契约 + 嵌套 Loop | modules/runtime | `ModuleInterfacePage` |
| 事件配置 | `/workshop/events` | 触发器表 + 幂等护栏 | actions/webhooks | `EventsPage` |
| 重能力 | `/aip/capabilities` | 能力卡片 + Session | capabilities/* | `CapabilityPage` |

---

## 2. 设计摘要

### 2.1 Graph（workshop-object-view）
- 左：邻接 1-hop 节点图（中心=选中实例，外圈=neighbors）
- 右：Object View + Wiki 摘要 + Action 链 Draft + @Buddy
- 禁 `JsonBlock` 主面板

### 2.2 Module Interface
- 从 module `widgets` 推导 input/output 表
- 嵌套 Loop 示意（Inbox 行 → 详情侧栏）

### 2.3 Events
- `BpTable`：蓝图 3 行 + API webhooks 合并展示
- 幂等护栏 `BpBanner`

### 2.4 Capabilities
- 已登记能力卡片（GET `/v1/aip/capabilities`）
- C2 Session 区（POST `session/open`）
- Job/一镜结果折叠 JSON

---

## 3. 代码落点

| 文件 | 变更 |
| --- | --- |
| `apps/web/src/pages/s2/workshop.tsx` | Graph + Events |
| `apps/web/src/pages/s2/extras.tsx` | ModuleInterfacePage |
| `apps/web/src/pages/CapabilityPage.tsx` | 卡片 + Session |
| `apps/web/src/styles.css` | `.bp-graph-*` |
| [78](78-蓝图页面对齐差距台账与去演示Hub方案.md) §6 | W9 行 |
| [00-技术方案索引](00-技术方案索引.md) | 挂 83 |

---

## 4. 验收

1. 上述四路径主区无大块 JSON ✅  
2. TB.9 业务一镜仍可用 ✅  
3. `npm test` 绿 ✅  

---

*v1.0*
