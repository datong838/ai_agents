# 全量页面功能组件差距盘点：视觉稿 vs 系统实现

> 文档版本：v1.0（2026-07-26）
> 范围：全站 10 个分区，约 73 个视觉稿文件
> 原则：**视觉稿有的 → 必须对齐；系统多出的 → 保留不动**
> 状态码：✅ 一致 | ⚠️ 部分差距 | 🔴 缺失 | 🟡 系统多出保留

---

## 0. 全局汇总表

| 分区 | 视觉稿数 | 系统页面数 | 完全一致 | 部分差距 | 缺失页面 | 缺失组件 |
|---|---|---|---|---|---|---|
| 概览 | 1 | 1 | 1 | 0 | 0 | 0 |
| 工作台 | 6 | 8 | 0 | 6 | 0 | 多 |
| 应用程序构建工具 | 7 | 4 | 0 | 4 | 3 | 多 |
| AIP 决策引擎 | 14 | 14 | 0 | 12 | 0 | 多 |
| 模型管理 | 4 | 4 | 0 | 4 | 0 | 多 |
| 本体·数字孪生 | 9+7=16 | 9 | 0 | 9 | 7 | 多 |
| 管道与数据治理 | 9 | 9 | 0 | 9 | 0 | 多 |
| 数据源与同步 | 6+2=8 | 6 | 0 | 6 | 2 | 多 |
| 运维交付 Apollo | 8 | 11 | 0 | 8 | 0 | 多 |
| **合计** | **~73** | **65** | **1** | **58** | **12** | **大量** |

---

## 1. 概览（`index.html`）

| 组件 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 顶部标题区 | h1 + 描述（13px） | ✅ 有 | ✅ 一致 | |
| 工作台 Panel | 标题 + 说明 + 应用列表入口 + 3 个模块卡片 + 快捷链接 | ✅ 有 | ✅ 一致 | |
| AIP 平台介绍条 | aos-footer-bar + 4 个卡片（Studio/Logic/Tools/Capabilities）+ 快捷链接 | ✅ 有 | ✅ 一致 | |

---

## 2. 工作台（6 页）

### 2.1 应用列表（`workshop.html`）

| 组件 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 顶部标题区 | h1"应用列表"（13px）+ 描述 + 绿色"新建 Module"按钮 | ✅ 有 | ✅ 已对齐 | 刚完成改造 |
| 最近使用 Panel | .aos-panel + grid 3列 + 卡片双链接（打开运行态/编辑画布） | ✅ 有 | ✅ 已对齐 | |
| 全部应用 Panel | .aos-panel + 4 Tab（全部/运营/分析/AI助手）+ grid 3列 | ✅ 有 | ✅ 已对齐 | |
| 卡片样式 | eyebrow（11px多色）+ 应用名（13px）+ 描述（11px）+ 双链接 | ✅ 有 | ✅ 已对齐 | |

### 2.2 创建应用（`workshop-create.html`）

| 组件 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 左侧垂直步骤导航 | 高亮绿 `#0F6E56` + 对勾已完成态 + 蓝色提示框 | 🔴 缺失 | 🔴 缺失 | |
| Step1 基本信息 | 模块名称 / 模块标识（slug自动生成）/ 6个图标选择器 / 业务域chip | ⚠️ 部分 | 缺图标选择器、slug自动生成、业务域chip | |
| Step2 数据绑定 | 对象类型树（左）+ 属性chips（右）+ 权限提示 | 🔴 缺失 | |
| Step3 模板选择 | 2×2模板卡（空白/表格列表/仪表盘/对象探索）+ 预览缩略图 | 🔴 缺失 | |
| Step4 确认创建 | 信息汇总表 + "创建后自动执行"清单 | 🔴 缺失 | |

### 2.3 风险告警管理（`workshop-module.html`）

| 组件 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| Top bar | 模块名 + 版本徽章 + "编辑模块/返回列表" | ⚠️ 部分 | 缺版本徽章和编辑模块按钮 | |
| 左 Filter | 状态/优先级/日期三组 checkbox + Object Set Filter | ⚠️ 部分 | 缺优先级和日期分组 | |
| 中 Table | 订单号/问题/店铺/等级，选中行左蓝边 | ⚠️ 部分 | 列头未对齐 | |
| 右 Object View | 风控分大数字 + 属性grid + Wiki黄底卡 + Actions + 活动日志时间线 | ⚠️ 部分 | 缺活动日志时间线 | |

### 2.4 订单管理（`workshop-app-order.html`）⭐ 重点

| 组件 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 暗色主题 | `#1A1A2E` + `p-ws-dark` | 🔴 缺失 | 当前是浅色运行态，需改为暗色画布编辑器 | |
| 三栏布局 | 左280px「模块接口/参数/事件处理/函数」面板 + 中画布 + 右「属性面板」 | 🔴 缺失 | 当前是单栏列表 | |
| Topbar | 模块/预览切换 + 保存/发布按钮 | 🔴 缺失 | |
| 工具栏 + 4个pop-panel | 添加微件grid（12个widget）、布局、变量、事件 | 🔴 缺失 | |
| 中画布 | 4统计卡片 + 订单表格 + 趋势SVG + 详情卡（动态渲染） | ⚠️ 部分 | 有表格，但非动态渲染 | |

### 2.5 态势大屏 COP（`workshop-cop.html`）

| 组件 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| KPI行 | 在途订单/缺货SKU/周转天数/风险工厂 | ⚠️ 部分 | KPI偏技术，需业务化 | |
| 主体 | 左SVG供应链网络 + 右钻取侧栏 | ⚠️ 部分 | SVG地图未对齐 | |
| 底部 | 风险工厂详情 + 实时事件 | ⚠️ 部分 | 事件列表仍mock | |

### 2.6 Buddy智能助手（`workshop-aip-chat.html`）

| 组件 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 表格列 | 订单号/状态/风控分💡/选中标记 | ⚠️ 部分 | 缺风控分列 | |
| Assist popover | 流程内提问 + 上下文说明 + AI回答 | ⚠️ 部分 | |
| 右Buddy侧栏 | Context chips + 对话log + 输入框 | ⚠️ 部分 | 布局基本对齐 | |

---

## 3. 应用程序构建工具（7页）

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 画布编辑 | `workshop-canvas.html`（145KB） | `/workshop/canvas` | ⚠️ 部分 | 视觉稿最复杂，现状基础版 |
| 组件注册表 | `workshop-widget-registry.html` | — | 🔴 缺失 | 需补：路由+占位页+nav项 |
| 变量管理器 | `workshop-variables.html` | — | 🔴 缺失 | 需补：路由+占位页+nav项 |
| 主题与样式 | `workshop-styles.html` | — | 🔴 缺失 | 需补：路由+占位页+nav项 |
| 模块接口 | `workshop-module-interface.html` | `/workshop/module-interface` | ⚠️ 部分 | |
| 事件配置 | `workshop-events.html` | `/workshop/events` | ⚠️ 部分 | |
| 发布入口 | `workshop-publish.html` | `/workshop/publish` | ⚠️ 部分 | |

### 3.1 画布编辑器（`workshop-canvas.html`）详细差距

| 组件 | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 顶部工具栏 | 保存/撤销/重做/预览/发布 | ⚠️ 部分 | 缺部分按钮 |
| 左侧组件面板 | 12个widget分类（数据/布局/表单/图表/AI/其他） | ⚠️ 部分 | |
| 中间画布 | 自由布局网格 + 拖拽组件 + 选中高亮 | ⚠️ 部分 | |
| 右侧属性面板 | 组件属性配置 + 样式配置 + 数据源配置 | 🔴 缺失 | |
| 底部状态栏 | 画布尺寸/选中组件/对齐提示 | 🔴 缺失 | |

---

## 4. AIP 决策引擎（14页）

### 4.1 应用层

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| AIP助手 | `aip-assist.html` | `/aip/assist` | 🔴 缺失 | 路由未注册，点击跳首页 |
| 对话机器人 | `agents.html` | `/aip/studio` | ⚠️ 部分 | 名字差异（Chatbot Studio） |
| AIP分析师 | `aip-analyst.html` | `/aip/analyst` | 🔴 缺失 | 路由未注册，点击跳首页 |

### 4.2 逻辑编排层

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| AIP逻辑画布 | `aip-logic.html` | `/aip/logic` | ⚠️ 部分 | |
| Agent工具面板 | `aip-tools.html` | `/aip/tools` | ⚠️ 部分 | |
| 成熟度楼梯 | `aip-maturity.html` | `/aip/maturity` | ⚠️ 部分 | |

### 4.3 智能体

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 智能体目录 | `agent-registry.html` | `/aip/agent-registry` | ⚠️ 部分 | 名字差异（智能体注册表） |
| 智能体插件 | `aip-capabilities.html` | `/aip/capabilities` | ⚠️ 部分 | |
| 智能体导入 | `aip-agent-import.html` | `/aip/agent-import` | ⚠️ 部分 | 系统多出，视觉稿存在 |
| 能力导入 | `aip-capability-import.html` | `/aip/capability-import` | ⚠️ 部分 | 系统多出，视觉稿存在 |

### 4.4 评测与治理

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| Evals门控 | `aip-evals.html` | `/aip/evals` | ⚠️ 部分 | |
| Draft审批台 | `aip-draft-inbox.html` | `/aip/drafts` | ⚠️ 部分 | |

### 4.5 决策谱系

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 决策谱系 | `aip-decision-lineage.html` | `/aip/lineage` | ⚠️ 部分 | |
| 可观测性 | `aip-observability.html` | `/aip/observability` | ⚠️ 部分 | |

---

## 5. 模型管理（4页）

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 模型目录 | `aip-model-catalog.html` | `/aip/model-catalog` | 🔴 缺失 | 路由未注册 |
| 模型供应商 | `aip-model-providers.html` | `/aip/model-providers` | ⚠️ 部分 | |
| 模型路由 | `aip-model-router.html` | `/aip/model-router` | ⚠️ 部分 | |
| 容量管理 | `aip-capacity-management.html` | `/aip/capacity` | 🔴 缺失 | 路由未注册 |

---

## 6. 本体·数字孪生（9+7=16页）

### 6.1 一级页面（9页）

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 本体管理 | `ontology.html` | `/ontology` | ⚠️ 部分 | |
| 对象探索 | `workshop-object-view.html` | `/workshop/graph` | ⚠️ 部分 | |
| 本体提案 | `ontology-funnel.html` | `/ontology/funnel` | ⚠️ 部分 | 名字差异（漏斗管道） |
| 图谱健康度 | `ontology-graph-health.html` | `/ontology/graph-health` | ⚠️ 部分 | |
| 活知识Wiki | `ontology-wiki-index.html` | `/ontology/wiki` | ⚠️ 部分 | |
| OKF funnel | `funnel.html` | `/ontology/okf-funnel` | ⚠️ 部分 | 名字差异（OKF行业漏斗） |
| OKF概览 | `okf-funnel.html` | `/ontology/okf-overview` | ⚠️ 部分 | |
| 分支管理 | `ontology-branches.html` | `/ontology/branches` | ⚠️ 部分 | |

### 6.2 二级详情页（7页）— 全部缺失

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 对象类型详情 | `ontology-object.html` | `/ontology/object-types/:typeId` | ✅ 有 | |
| 链接类型详情 | `ontology-link.html` | `/ontology/link-types/:linkId` | ✅ 有 | |
| 属性类型详情 | `ontology-property.html` | — | 🔴 缺失 | |
| Action详情 | `ontology-action.html` | `/ontology/action-types/:actionId` | ✅ 有 | |
| Function详情 | `ontology-function.html` | — | 🔴 缺失 | |
| Wiki详情 | `ontology-wiki.html` | — | 🔴 缺失 | |
| Wiki差异 | `ontology-wiki-diff.html` | — | 🔴 缺失 | |

---

## 7. 管道与数据治理（9页）

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 管道构建 | `pipeline-list.html` | `/data/pipelines` | ⚠️ 部分 | |
| 管道提案 | `pipeline-proposals.html` | `/data/pipeline-proposals` | ⚠️ 部分 | |
| 计划编辑器 | `schedules.html` | `/data/schedules` | ⚠️ 部分 | |
| 搭建 | `builds.html` | `/data/builds` | ⚠️ 部分 | |
| 数据集预览 | `dataset.html` | `/data/datasets` | ⚠️ 部分 | |
| 代码库 | `code-repositories.html` | `/data/code-repos` | ⚠️ 部分 | |
| 数据沿袭 | `lineage.html` | `/data/lineage` | ⚠️ 部分 | |
| 数据健康 | `health.html` | `/data/health` | ⚠️ 部分 | |
| 管道画布 | `pipeline.html` | `/data/pipelines/:pipelineId` | ⚠️ 部分 | |
| DocIntel管道 | `pipeline-doc-intel.html` | — | 🔴 缺失 | |

---

## 8. 数据源与同步（6+2=8页）

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| 数据链接器 | `data-connection.html` | `/data` | ⚠️ 部分 | |
| 边缘代理 | `data-connection-agents.html` | `/data/agents` | ⚠️ 部分 | |
| 同步配置 | `sync.html` | `/data/sync-config` | ⚠️ 部分 | |
| 同步路由 | `sync-routing.html` | `/data/sync-routes` | ⚠️ 部分 | |
| 媒体集 | `media-sets.html` | `/data/media-sets` | ⚠️ 部分 | |
| 文档智能 | `document-intelligence.html` | `/aip/doc-intelligence` | 🔴 缺失 | 路由未注册 |
| 数据源新建 | `source-new.html` | — | 🔴 缺失 | |
| 数据源详情 | `source-detail.html` | `/data/sources/:sourceId` | ✅ 有 | |

---

## 9. 运维交付 Apollo（8页）

| 页面 | 视觉稿 | 系统 | 状态 | 详情 |
|---|---|---|---|---|
| Hub舰队 | `apollo-hub.html` | `/apollo` | ⚠️ 部分 | |
| Release通道 | `apollo-release.html` | `/apollo/release` | ⚠️ 部分 | |
| Spoke详情 | `apollo-spoke.html` | `/apollo/spoke` | ⚠️ 部分 | |
| Ferry摆渡 | `apollo-ferry.html` | `/apollo/ferry` | ⚠️ 部分 | |
| FDE资产包 | `apollo-assets.html` | `/apollo/assets` | ⚠️ 部分 | |
| 变更审批 | `apollo-change-mgmt.html` | `/apollo/change` | ⚠️ 部分 | |
| 配置与密钥 | `apollo-config.html` | `/apollo/config` | ⚠️ 部分 | |
| 接入案例 | `integration-cases.html` | `/apollo/cases` | ⚠️ 部分 | |

---

## 10. 缺失页面汇总（共12页）

| # | 页面 | 视觉稿文件 | 所属分区 | 优先级 |
|---|---|---|---|---|
| 1 | 组件注册表 | `workshop-widget-registry.html` | 应用程序构建工具 | **P0** |
| 2 | 变量管理器 | `workshop-variables.html` | 应用程序构建工具 | **P0** |
| 3 | 主题与样式 | `workshop-styles.html` | 应用程序构建工具 | **P0** |
| 4 | AIP助手 | `aip-assist.html` | AIP决策引擎 | **P0** |
| 5 | AIP分析师 | `aip-analyst.html` | AIP决策引擎 | **P0** |
| 6 | 模型目录 | `aip-model-catalog.html` | 模型管理 | **P0** |
| 7 | 容量管理 | `aip-capacity-management.html` | 模型管理 | **P0** |
| 8 | 文档智能 | `document-intelligence.html` | 数据源与同步 | **P0** |
| 9 | 属性类型详情 | `ontology-property.html` | 本体·数字孪生 | **P1** |
| 10 | Function详情 | `ontology-function.html` | 本体·数字孪生 | **P1** |
| 11 | Wiki详情 | `ontology-wiki.html` | 本体·数字孪生 | **P1** |
| 12 | Wiki差异 | `ontology-wiki-diff.html` | 本体·数字孪生 | **P1** |
| 13 | 数据源新建 | `source-new.html` | 数据源与同步 | **P1** |
| 14 | DocIntel管道 | `pipeline-doc-intel.html` | 管道与数据治理 | **P1** |

---

## 11. 高优先级功能组件缺失汇总

### P0 — 影响核心体验

| 组件 | 所在页面 | 影响 |
|---|---|---|
| 左侧垂直步骤导航 | 创建应用 | 无法完成在线定制流程 |
| 暗色主题 + 三栏布局 | 订单管理 | 定位错配，运营无法使用 |
| 工具栏 + 4个pop-panel | 订单管理 | 无法添加/配置组件 |
| 组件属性面板 | 画布编辑器 | 无法配置组件属性 |

### P1 — 影响功能完整性

| 组件 | 所在页面 | 影响 |
|---|---|---|
| 图标选择器 + slug生成 | 创建应用 | 无法自定义模块标识 |
| 对象类型树 + 属性chips | 创建应用 | 无法绑定数据对象 |
| 模板卡 + 预览 | 创建应用 | 无法选择模块模板 |
| 优先级/日期Filter | 风险告警管理 | 无法筛选告警 |
| 活动日志时间线 | 风险告警管理 | 无法查看处理历史 |
| KPI业务化 | 态势大屏 | 数据不直观 |
| 风控分列 | Buddy助手 | 缺关键指标 |

---

## 12. 改造路线图

### Phase A — 工作台核心（当前进行中）
- [x] 应用列表页对齐（已完成）
- [ ] 创建应用补齐（左侧步骤+图标+slug+对象树+属性chips+模板）
- [ ] 风险告警管理补齐（Top bar+Filter+活动日志）
- [ ] 订单管理重写（暗色画布编辑器）
- [ ] 态势大屏补齐（KPI业务化）
- [ ] Buddy助手补齐（风控分列）

### Phase B — 应用程序构建工具
- [ ] 补齐3个缺失页面（组件注册表/变量管理器/主题与样式）
- [ ] 画布编辑器深度对齐（属性面板/工具栏/组件拖拽）

### Phase C — AIP决策引擎
- [ ] 补齐2个缺失页面（AIP助手/AIP分析师）
- [ ] 名字统一（8处）
- [ ] 各页面内容对齐

### Phase D — 模型管理
- [ ] 补齐2个缺失页面（模型目录/容量管理）
- [ ] 各页面内容对齐

### Phase E — 本体·数字孪生
- [ ] 补齐4个缺失二级页面
- [ ] 各页面内容对齐

### Phase F — 管道与数据治理 + 数据源与同步 + 运维交付
- [ ] 补齐缺失页面
- [ ] 各页面内容对齐

---

## 13. 用户已确认事项（决策记录）

| 问题 | 用户决策 |
|---|---|
| 改造节奏 | 后续专门写计划（Phase A→B→C→D→E→F 顺序） |
| 缺失页面处理 | **直接做真实页面**，严格按照视觉稿（不用占位页） |
| 名字统一 | **全部按视觉稿改**（8 处名字差异） |
| 本体提案 vs 漏斗管道 | **同义页**，按视觉稿改名"本体提案" |
| OKF funnel | 按视觉稿改名"OKF funnel"（去掉"行业"） |
| Module 核心原则 | Module 是在线定制出来的，不是写代码写出来的；新建 Module 能力必须很强 |

### 13.1 名字统一执行清单（8 处，全部按视觉稿改）

| # | 视觉稿名字 | 系统名字 | 文件位置 | 改动类型 |
|---|---|---|---|---|
| 1 | AIP 助手 | AIP Assist | `apps/web/src/nav.ts` + 路由注册 | 改 label |
| 2 | 对话机器人 | Chatbot Studio | `apps/web/src/nav.ts` | 改 label |
| 3 | AIP 分析师 | AIP Analyst | `apps/web/src/nav.ts` + 路由注册 | 改 label |
| 4 | 智能体目录 | 智能体注册表 | `apps/web/src/nav.ts` | 改 label |
| 5 | 本体提案 | 漏斗管道 | `apps/web/src/nav.ts` | 改 label |
| 6 | OKF funnel | OKF 行业漏斗 | `apps/web/src/nav.ts` | 改 label |
| 7 | Buddy · 智能助手 | Buddy 智能助手 | `apps/web/src/nav.ts` | 改 label（加中点号） |
| 8 | 活知识 Wiki | (系统拆成2项) | `apps/web/src/nav.ts` | 视觉稿合并为1项 |

### 13.2 缺失页面执行清单（14 页，全部做真实页面）

| # | 页面 | 视觉稿文件 | 所属分区 | 优先级 | 执行方式 |
|---|---|---|---|---|---|
| 1 | 组件注册表 | `workshop-widget-registry.html` | 应用程序构建工具 | **P0** | 新建路由+真实页面+nav项 |
| 2 | 变量管理器 | `workshop-variables.html` | 应用程序构建工具 | **P0** | 同上 |
| 3 | 主题与样式 | `workshop-styles.html` | 应用程序构建工具 | **P0** | 同上 |
| 4 | AIP 助手 | `aip-assist.html` | AIP 决策引擎 | **P0** | 路由注册+真实页面 |
| 5 | AIP 分析师 | `aip-analyst.html` | AIP 决策引擎 | **P0** | 同上 |
| 6 | 模型目录 | `aip-model-catalog.html` | 模型管理 | **P0** | 同上 |
| 7 | 容量管理 | `aip-capacity-management.html` | 模型管理 | **P0** | 同上 |
| 8 | 文档智能 | `document-intelligence.html` | 数据源与同步 | **P0** | 同上 |
| 9 | 属性类型详情 | `ontology-property.html` | 本体·数字孪生 | **P1** | 新建路由+真实页面 |
| 10 | Function 详情 | `ontology-function.html` | 本体·数字孪生 | **P1** | 同上 |
| 11 | Wiki 详情 | `ontology-wiki.html` | 本体·数字孪生 | **P1** | 同上 |
| 12 | Wiki 差异 | `ontology-wiki-diff.html` | 本体·数字孪生 | **P1** | 同上 |
| 13 | 数据源新建 | `source-new.html` | 数据源与同步 | **P1** | 同上 |
| 14 | DocIntel 管道 | `pipeline-doc-intel.html` | 管道与数据治理 | **P1** | 同上 |

### 13.3 核心组件缺失清单（按视觉稿补齐）

| # | 组件 | 所在页面 | 视觉稿 | 执行方式 |
|---|---|---|---|---|
| 1 | 左侧垂直步骤导航 | 创建应用 | `workshop-create.html` | 新建组件 |
| 2 | 图标选择器（6个预设） | 创建应用 | 同上 | 新建组件 |
| 3 | slug 自动生成 | 创建应用 | 同上 | 新建工具函数 |
| 4 | 业务域 chip 选择 | 创建应用 | 同上 | 新建组件 |
| 5 | 对象类型树 | 创建应用 | 同上 | 新建组件 |
| 6 | 属性 chips | 创建应用 | 同上 | 新建组件 |
| 7 | 模板卡（2×2）+ 预览 | 创建应用 | 同上 | 新建组件 |
| 8 | 暗色主题 `#1A1A2E` | 订单管理 | `workshop-app-order.html` | CSS + 主题切换 |
| 9 | 三栏布局（左280+中画布+右属性） | 订单管理 | 同上 | 重写页面 |
| 10 | Topbar（模块/预览切换+保存/发布） | 订单管理 | 同上 | 新建组件 |
| 11 | 工具栏 + 4 个 pop-panel | 订单管理 | 同上 | 新建组件 |
| 12 | 中画布动态渲染（widgets 配置驱动） | 订单管理 | 同上 | 新建渲染引擎 |
| 13 | Top bar（模块名+版本徽章+编辑模块） | 风险告警管理 | `workshop-module.html` | 新建组件 |
| 14 | 优先级/日期 Filter | 风险告警管理 | 同上 | 补齐组件 |
| 15 | 活动日志时间线 | 风险告警管理 | 同上 | 新建组件 |
| 16 | KPI 业务化 | 态势大屏 | `workshop-cop.html` | 改造组件 |
| 17 | SVG 供应链网络 | 态势大屏 | 同上 | 新建组件 |
| 18 | 风控分列 | Buddy 助手 | `workshop-aip-chat.html` | 补齐列 |
| 19 | 画布编辑器右侧属性面板 | 画布编辑 | `workshop-canvas.html` | 新建组件 |
| 20 | 画布编辑器底部状态栏 | 画布编辑 | 同上 | 新建组件 |

---

## 14. 附录：文件位置

### 视觉稿基准
- `/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/`（73个文件）
- `/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/assets/demo.css`（全局样式）

### 系统实现
- 导航定义：`aos-platform/apps/web/src/nav.ts`
- 主路由：`aos-platform/apps/web/src/App.tsx`
- S2路由：`aos-platform/apps/web/src/pages/s2/routes.tsx`
- 页面组件：`aos-platform/apps/web/src/pages/` + `aos-platform/apps/web/src/pages/s2/`

### 配套文档
- 菜单对齐：`/Users/ddt/work/projects/ai_agent/docs/palantier/20_tech/223-menu-alignment-full.md`
- 工作台深度方案：`/Users/ddt/work/projects/ai_agent/docs/palantier/20_tech/223-ui-alignment-plan.md`
- 种子数据整合方案：`/Users/ddt/work/projects/ai_agent/docs/palantier/20_tech/223-seed-data-consolidation-plan.md`