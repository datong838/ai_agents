# AOS HTML 页面 ↔ Palantir 截图映射表

> 用于驱动后续按截图重做页面的工作。每行：页面 → 主参考截图（本地路径） → 当前差距

截图根目录：`/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/images/foundry/`

---

## ✅ 已完成（按截图 1:1 复刻）

| HTML 页面 | 主参考截图 | 状态 |
|-----------|-----------|------|
| `aip-draft-inbox.html` | `ontologies/reviews.png` | ✅ 三栏审批台（左任务列表 / 中详情 / 右活动历史） |
| `ontology.html` | `ontology-manager/oma-discover-view.png` + `oma-fallback-sections.png` | ✅ OMA Discover 视图（收藏/最近/重要表格/群组） |
| `ontology-object.html` | `ontology-manager/oma-user-interface-object-type-view.png` + `oma-user-interface-overview-annotated.png` | ✅ Object Type View（左侧页面栏 + 右侧 6 section：元数据/属性/操作/链接图/数据/使用） |
| `pipeline.html` | `pipeline-builder/top-toolbar@2x.png` + `samplegraph@2x.png` + `outputs-sidebar@2x.png` | ✅ Pipeline Builder（顶部工具栏+画布+底部预览+右侧输出侧栏） |
| `data-connection.html` | `data-connection/data-connection-app-portal.png` | ✅ Data Connection 应用门户（左侧分类导航+统计条+应用卡片网格） |
| `lineage.html` | `data-lineage/data-lineage-ui-reference.png` | ✅ Data Lineage（左侧搜索/属性面板+中央沿袭图+节点详情条+图例+工具条） |

---

## 🔥 高优先级（有明确截图，功能核心）

### 本体 / Ontology
| HTML 页面 | 主参考截图 | 备注 |
|-----------|-----------|------|
| `ontology.html` | `ontology/ontology-overview-header.png` + `ontologies/topbar.png` | 本体总览，顶部 tab + 概览卡片 |
| `ontology-object.html` | `ontology-manager/oma-user-interface-object-type-view.png` + `object-explorer/home_object_type_preview.png` | 对象类型详情（属性表 + 关系图） |
| `ontology-property.html` | `ontology-manager/oma-user-interface-property-editor-v2.png` | 属性编辑器 |
| `ontology-link.html` | `ontology-manager/oma-user-interface-link-type.png` | Link 类型 |
| `ontology-action.html` | `ontology-manager/oma-user-interface-action-type.png` | Action 类型 |
| `ontology-function.html` | `ontology-manager/oma-user-interface-function-type.png` | Function 类型 |
| `ontology-branches.html` | `pipeline-builder/branches-new@2x.png` + `pipeline-builder/pb-branch-selector.png` | 分支管理 |
| `ontology-graph-health.html` | `object-explorer/home_object_type_graph_link.png` | 对象关系图 |
| `ontology-wiki.html` | `ontology/object-apps-slate-editor-view.png` | Wiki/文档 |
| `ontology-funnel.html` | `ontologies/proposal-overview.png` | 提案漏斗 |

### Object Explorer / 对象浏览
| HTML 页面 | 主参考截图 | 备注 |
|-----------|-----------|------|
| `workshop-object-view.html` | `object-explorer/admin_airline_exploration.png` | 对象探索主视图（表格 + 图表） |
| —（并入 object-view） | `object-explorer/results_view.png` | 结果表格 |
| — | `object-explorer/charts_histogram.png` + `charts_pie_chart.png` + `charts_cluster_map.png` | 图表面板 |
| — | `object-explorer/explore_search.png` + `results_column_configurator.png` | 搜索/列配置 |

### Pipeline Builder / 管道构建
| HTML 页面 | 主参考截图 | 备注 |
|-----------|-----------|------|
| `pipeline.html` | `pipeline-builder/pipeline-builder-gfx@2x.png` + `overview-flowchart@2x.png` | 管道画布（节点图） |
| `pipeline-list.html` | `pipeline-builder/file-tree-side-bar.png` | 管道列表 |
| `pipeline-proposals.html` | `pipeline-builder/proposals-tab@2x.png` + `pipeline-builder/new-proposal@2x.png` | 管道提案 |
| `pipeline-doc-intel.html` | `pipeline-builder/llm-doc-classification.png` + `llm-doc-entity-extract-prompt.png` | 文档智能（LLM） |
| `builds.html` | `pipeline-builder/health-build-status@2x.png` | 搭建状态 |
| `schedules.html` | `data-lineage/manage-schedules.png` + `manage-schedule-details.png` | 计划编辑器 |

### Data Connection / 数据连接
| HTML 页面 | 主参考截图 | 备注 |
|-----------|-----------|------|
| `data-connection.html` | `data-connection/data-connection-app-portal.png` | 应用门户（应用卡片网格） |
| `source-new.html` | `data-connection/data-connection-new-source-page.png` | 新建数据源 |
| `source-detail.html` | `data-connection/db-explorer.png` | 数据库浏览器（三栏：表树/数据/属性） |
| `data-connection-agents.html` | `data-connection/agent-metrics.png` + `agent-requirements.png` | 边缘代理 |
| `sync.html` | `data-connection/data-connection-batch-sync-s3.png` + `incremental-jdbc-sync.png` | 同步任务 |
| `sync-routing.html` | `data-connection/data-connection-source-capabilities.png` | 同步路由 |

### Workshop / 工作台
| HTML 页面 | 主参考截图 | 备注 |
|-----------|-----------|------|
| `workshop.html` | `ontology/object-apps-workshop-module.png` + `Workshop-createnewmodule.png`(若存在) | Workshop 模块（暗色主题！） |
| `workshop-canvas.html` | `ontology/object-apps-slate-editor-view.png` | Slate/画布编辑器 |
| `workshop-module.html` | `ontology/object-apps-workshop-editor-view.png` | 模块编辑器 |

### Data Lineage / 数据沿袭
| HTML 页面 | 主参考截图 | 备注 |
|-----------|-----------|------|
| `lineage.html` | `data-lineage/data-lineage-ui-reference.png` + `data-lineage-expand-all.png` | 沿袭图 |
| `health.html` | `data-lineage/data-lineage-icon-issues-reported.png` + `view-histogram.png` | 数据健康 |

---

## 🟡 中优先级（有截图，可复刻）

| HTML 页面 | 主参考截图 | 备注 |
|-----------|-----------|------|
| `dataset.html` | `data-lineage/dataset-preview.png` | 数据集预览 |
| `code-repositories.html` | `code-repositories/`(目录) | 代码仓库 |
| `media-sets.html` | `media-sets-advanced-formats/`(目录) | 媒体集 |
| `agents.html` | `functions/`(目录) 或 `interfaces/`(目录) | Agent/Chatbot |
| `aip-logic.html` | `logic/`(目录) | AIP 逻辑画布 |
| `aip-tools.html` | `functions/`(目录) | Agent 工具 |
| `aip-evals.html` | `pipeline-builder/unit-test-pass-fail.png` | Evals 门控 |
| `aip-decision-lineage.html` | `data-lineage/data-lineage-ui-reference.png` | 决策谱系 |
| `aip-maturity.html` | —（无直接截图，自定义） | 成熟度楼梯 |
| `aip-model-providers.html` | `pipeline-builder/llm-doc-model-configs.png` | 模型供应商 |
| `aip-model-router.html` | —（自定义） | 模型路由 |
| `aip-capabilities.html` | —（自定义） | 重能力接入 |

---

## 🟢 低优先级（Apollo / 入口 / 自定义）

| HTML 页面 | 主参考截图 | 备注 |
|-----------|-----------|------|
| `index.html` | `data-connection/data-connection-app-portal.png` | 入口页（应用网格） |
| `funnel.html` / `okf-funnel.html` | —（自定义业务） | 业务漏斗 |
| `apollo-*.html` (7个) | —（AOS 自有概念） | Apollo 舰队 |
| `workshop-aip-chat.html` | —（自定义） | Buddy 助手 |
| `workshop-cop.html` | —（自定义） | 态势大屏 |
| `workshop-events.html` | —（自定义） | 事件配置 |
| `workshop-module-interface.html` | —（自定义） | 模块接口 |
| `workshop-publish.html` | —（自定义） | 发布入口 |

---

## 工作方法

1. **每次重做一个页面前**：先 Read 对应截图，把布局、组件、配色、字号、间距精确提取
2. **保持 Palantir 全局壳**：`p-app` + `p-nav-global` + `p-sidebar` + `p-header` + `p-content`
3. **页面内容按截图重做**：用 `p-card` / `p-table` / `p-badge` / `p-btn` / `p-tabs` 等已有组件类
4. **特殊布局**：如三栏审批台、画布、对象图等，追加专用 CSS 块到 `demo.css` 末尾
5. **每个页面重做完**：本地服务器预览验证，再标记完成
