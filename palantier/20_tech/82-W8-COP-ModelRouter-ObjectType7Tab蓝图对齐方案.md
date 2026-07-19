# 82 · W8 COP + Model Router + Object Type 7 Tab 蓝图对齐方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[78](78-蓝图页面对齐差距台账与去演示Hub方案.md) §3 · [26 §12](26-AOS目标态开发计划.md)  
> **蓝图**：`workshop-cop.html` · `aip-model-router.html` · `ontology-object.html`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI 文案 |
| 先方案后编码 | 本文 → 再改 `apps/web` |
| 最小更改 | 复用现有 API；不增后端 |
| 禁 JSON 主面板 | KPI/表格/Tab；调试 JSON 仅 `<details>` |
| 诚实占位 | Usage 30 天指标 API 未有时标注「引擎后置」 |

---

## 1. 范围

| 页 | 路径 | 蓝图要点 | API | 落地 |
| --- | --- | --- | --- | --- |
| 态势大屏 | `/workshop/cop` | 4 KPI + Map/Graph + 钻取侧栏 | graph-health · metrics · evals · objects | `CopPage` → `BpMetricGrid` + 布局 |
| 模型路由 | `/aip/model-router` | 路由规则表 + 预热 + 试聊 | models · providers · warmup · chat | `ModelRouterPage` → `BpTable` + 卡片 |
| Object Type | `/ontology` | 7 Tab 详情 | object-types · link-types · actions/types · modules · funnel | `ObjectTypeDetailPanel` |

---

## 2. 设计

### 2.1 COP（workshop-cop）

| KPI（蓝图） | API 映射 |
| --- | --- |
| 在途订单 | `graph-health.metrics.instances` |
| 缺货 SKU | `graph-health.metrics.orphanInstances` |
| 周转天数 | `metrics.totals.p95Ms` → 展示为 API 延迟 p95（ms） |
| 风险工厂 | Eval 未绿或 `metrics.totals.errors > 0` |

主区：`bp-cop-map` 网格占位 + 可点 Object Type 节点；右侧钻取 Object View + 链 Inbox。

### 2.2 Model Router（aip-model-router）

- **路由规则表**：6 行任务类型 × 从 `/v1/aip/models` 推导首选/回退（无持久化策略 API）
- **预热**：`GET /v1/aip/models/warmup` → 状态条
- **试聊**：`POST /v1/aip/chat` · 主区展示 `answer` 文本；原始 JSON 折叠

### 2.3 Object Type 7 Tab（ontology-object）

选中 Object Type 后展示 Tab：

| Tab | 内容 | API |
| --- | --- | --- |
| Overview | 元数据 + 子卡片预览 | type row + funnel |
| Properties | 属性表 | `properties` on object-types |
| Action types | 过滤 actions/types | `objectType` match |
| Link type graph | 关联 link-types | src/dst filter |
| Dependents | Module 依赖 | `/v1/modules` · `objectType` |
| Data | 实例列表 + Funnel | objects + funnel/status |
| Usage | 读/写/活跃（metrics 诚实推导） | `/v1/metrics` totals |

---

## 3. 代码落点

| 文件 | 变更 |
| --- | --- |
| `apps/web/src/pages/s2/extras.tsx` | `CopPage` 蓝图布局 |
| `apps/web/src/pages/s2/aip.tsx` | `ModelRouterPage` 路由表 + 预热 |
| `apps/web/src/pages/s2/objectTypeDetail.tsx` | **新增** · 7 Tab 面板 |
| `apps/web/src/pages/OntologyPage.tsx` | 选中 OT 挂 7 Tab |
| `apps/web/src/styles.css` | `.bp-cop-map` 等 |
| [78](78-蓝图页面对齐差距台账与去演示Hub方案.md) §6 | W8 行 |
| [00-技术方案索引](00-技术方案索引.md) | 挂 82 |

---

## 4. 验收

1. `/workshop/cop` · `/aip/model-router` · `/ontology`（选中 OT）主区无大块 JSON ✅  
2. API 真值驱动 KPI / 路由模型 / Tab 内容 ✅  
3. `npm test` 绿 ✅  

---

*v1.0*
