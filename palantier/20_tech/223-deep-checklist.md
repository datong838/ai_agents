# 223 全站 UI 深度检查清单

> 版本：v1.1（2026-07-29 功能完整度复审）
> 范围：全站 9 大分区 + 详情页，共 73 个视觉稿文件
> 检查标准：逐页分析组件级差距，输出每页的改造清单
>
> **v1.1 说明**：§1.1 起为「菜单页功能完整度」复审表。旧文中「组件注册表/变量/样式 = 0% 缺失」「Draft=0%」「多处路由未注册」等已过时——页面大多已接线，完整度见下表。§7+ 单页详表仍保留历史差距描述，以 §1.1 的 **new%** 为准。

---

## 0. 深度检查标准（每页必做 7 项）

对每个视觉稿页面，必须完成以下 7 项检查：

### 0.1 页面结构检查
- [ ] 页面整体布局（几栏？每栏宽度？）
- [ ] 顶部区域（面包屑、标题、操作按钮）
- [ ] 主内容区结构（卡片/列表/画布/表格）
- [ ] 侧边栏（左侧/右侧，有哪些面板）
- [ ] 底部区域（状态栏、分页、操作栏）

### 0.2 组件级盘点
- [ ] 列出页面中所有组件（按钮、输入框、表格、卡片、图表等）
- [ ] 标记哪些组件系统已有，哪些需要新建
- [ ] 标记哪些组件需要修改样式/交互

### 0.3 数据驱动检查
- [ ] 页面哪些数据是动态的（从 API 拉取）
- [ ] 需要哪些后端接口（列表/详情/创建/更新/删除）
- [ ] 需要哪些数据库表/字段
- [ ] 测试数据怎么造（数量、覆盖场景）

### 0.4 交互检查
- [ ] 页面有哪些交互（点击、悬停、拖拽、弹窗、切换）
- [ ] 哪些交互系统已有，哪些需要新增
- [ ] 状态流转（加载中、空状态、错误状态、成功状态）

### 0.5 主题与样式检查
- [ ] 页面主题（浅色/暗色/其他）
- [ ] 品牌色使用是否正确（`#0F6E56` 深绿）
- [ ] 字体、间距、圆角、阴影等设计 token
- [ ] 响应式布局（不同屏幕尺寸的表现）

### 0.6 与系统现状对比
- [ ] 系统当前页面路径（如果存在）
- [ ] 系统当前实现的完整度百分比（0%/30%/60%/90%）
- [ ] 核心差距列表（按 P0/P1/P2 分级）
- [ ] 改造工作量估算（人天）

### 0.7 风险与依赖
- [ ] 技术风险（复杂组件、性能、兼容性）
- [ ] 后端依赖（需要哪些 API/表/字段）
- [ ] 数据依赖（需要哪些测试数据）
- [ ] 其他页面依赖（是否依赖其他页面的改造）

---

## 1. 检查进度总览

| 分区 | 页面数 | 已检查 | 进度 | 优先级 |
|---|---|---|---|---|
| 概览 | 1 | 1 | ✅ 100% | - |
| 工作台 | 12 | 6 | ⏳ 50% | **P0** |
| 应用程序构建工具 | 7 | 0 | ⏳ 0% | **P0** |
| AIP 决策引擎 | 14 | 0 | ⏳ 0% | **P1** |
| 模型管理 | 4 | 0 | ⏳ 0% | **P1** |
| 本体·数字孪生 | 13 | 0 | ⏳ 0% | **P1** |
| 管道与数据治理 | 9 | 0 | ⏳ 0% | **P2** |
| 数据源与同步 | 7 | 0 | ⏳ 0% | **P2** |
| 运维交付 | 10 | 0 | ⏳ 0% | **P2** |
| **侧栏小计** | **77** | **7** | **9%** | - |
| 详情页/弹出页（不在侧栏） | ~6 | 0 | ⏳ 0% | - |
| **总计** | **~73 个文件** | **7** | **~10%** | - |

> 注：侧栏 77 项中有部分是系统多出的（不在视觉稿中），实际视觉稿文件约 73 个。

---

## 1.1 菜单页功能完整度总表（2026-07-29 复审）

### 评分口径（功能逻辑，不是纯视觉像素）

| 档位 | % | 含义 |
|------|---|------|
| 壳 | 0–15 | 能打开 / 占位文案，主能力未接 |
| 骨架 | 20–40 | 主区块有，多为 MOCK；主流程不闭环或很薄 |
| 可用 | 50–70 | 主流程可走（含 API 或可靠 mock 降级）；相对视觉稿仍有结构/能力缺口 |
| 接近 | 75–90 | 结构接近视觉 + 核心功能可用；细项/后端/1:1 对账未完 |
| 完成向 | 90+ | 演示产品意图基本闭环（仍可能有对账细节） |

**复审人理解的页面职责（写完整度前先对齐「这页干什么」）：**

| 分区 | 页面在产品里的角色 |
|------|-------------------|
| 工作台 | 业务人员打开/使用 Module（应用列表、订单、风险 Inbox、态势、Buddy） |
| 构建工具 | FDE 搭建 Module：画布 / 组件 / 变量 / 主题 / **接口契约** / 事件 / 发布 |
| AIP | AI 能力注入：助手、Agent、逻辑、工具、评测、Draft、谱系、可观测 |
| 模型 | 模型目录、供应商、路由、容量配额 |
| 本体 | 对象类型与知识（Discover、探索、Wiki、分支、健康） |
| 管道/数据源 | 数据进本体前的管道、调度、数据集、连接与同步 |
| 运维 | Hub/Spoke/Ferry/资产/变更/密钥与接入案例 |

> `/workshop/create`、`/workshop/module`：**侧栏已隐藏**（能力收敛到应用列表），路由保留，仍计入下表。

### A. 概览 + 工作台

| 路径 | 页面 | 职责一句话 | 旧% | **新%** | 现状要点 |
|------|------|------------|-----|--------|----------|
| `/` | 概览 | 全站入口域网格 | ~90 | **90** | 域卡+指标；视觉细节仍可抠 |
| `/workshop` | 应用列表 | 打开/新建 Module 入口 | — | **70** | 分类卡片+`/v1/modules`；mock 降级 |
| `/workshop/create` | 创建应用 *(隐)* | 四步向导建 Module | — | **55** | 已对齐 4 步视觉；创建失败走 mockId |
| `/workshop/module` | 模块管理 *(隐)* | Module CRUD（与列表重叠） | 60 | **70** | 列表/发布有 API；侧栏已藏 |
| `/workshop/orders` | 订单管理 | 订单运行态 demo | — | **60** | 列表/详情主流程 |
| `/workshop/inbox` | 风险告警 | Inbox 工单运行态 | — | **65** | 筛选+表格+详情流 |
| `/workshop/cop` | 态势大屏 | COP 态势可视化 | — | **55** | KPI/地图壳，演示向 |
| `/workshop/buddy` | Buddy | 业务助手对话 | — | **60** | Assist 对话；非全 Studio |
| `/analytics` | 分析建模 | 分析工作台 | — | **65** | 多块分析流；视觉未 1:1 |

### B. 应用程序构建工具（搭建链）

| 路径 | 页面 | 职责一句话 | 旧% | **新%** | 现状要点 |
|------|------|------------|-----|--------|----------|
| `/workshop/canvas` | 画布编辑 | 三栏拖拽搭页面 | **30** | **70** | 变量只读面板+属性绑定+树联动（W4 B1） |
| `/workshop/widget-registry` | 组件注册表 | Widget 目录三来源 | **0** | **70** | 卡片/详情齐；市场安装/usedBy 弱 |
| `/workshop/variables` | 变量管理器 | 集中管页面/应用/全局变量 | **0** | **65** | API CRUD + MOCK 降级（W1 A1） |
| `/workshop/styles` | 主题与样式 | Module 主题色/字体 | **0** | **60** | 编辑器较完整；未真正驱动全应用主题 |
| `/workshop/module-interface` | 模块接口 | Module **入参/出参契约** + Loop 嵌套示意 | **10** | **65** | schema CRUD + GET/PUT（W2 A2） |
| `/workshop/events` | 事件配置 | Widget 事件→动作绑定 | **20** | **60** | 列表+向导；API 可降级 MOCK |
| `/workshop/publish` | 发布入口 | Module 发布通道 | **20** | **65** | 环境卡+步骤+publish/deploy（W2 B4） |

### C. AIP 决策引擎

| 路径 | 页面 | 职责一句话 | 旧% | **新%** | 现状要点 |
|------|------|------------|-----|--------|----------|
| `/aip/assist` | AIP 助手 | 文档/本体感知问答 | **0** | **65** | 聊天+SSE；挂则 mock |
| `/aip/studio` | 对话机器人 | Agent 配置工作台 | **25** | **65** | 提示词/工具 Tab 可写保存（W2 B2） |
| `/aip/agents` | 智能体列表 | Agent 列表+向导 | — | **65** | 向导/试运行；多 MOCK |
| `/aip/analyst` | AIP 分析师 | NL/SQL 分析 | **0** | **60** | live query + 演示降级（W2 A4） |
| `/aip/logic` | AIP 逻辑画布 | 逻辑编排/handoff | **60** | **75** | execute API 有；预览粗 |
| `/aip/tools` | Agent 工具面板 | 工具目录与试跑 | **70** | **75** | 工具 API 实；评分等缺 |
| `/aip/maturity` | 成熟度楼梯 | L0–L4 门控 | **85** | **85** | 楼梯+熔断较齐 |
| `/aip/capabilities` | 智能体插件 | 能力插件卡 | **0** | **70** | 配置 PUT + 连通测试（W4 B5） |
| `/aip/agent-registry` | 智能体目录 | 浏览/发现 Agent | **30** | **60** | 卡片网格；可 MOCK |
| `/aip/agent-import` | 智能体导入 | 外部 Agent 导入 | **40** | **55** | 多步；扫描演示重 |
| `/aip/capability-import` | 能力导入 | 能力 YAML 导入 | **35** | **50** | 注册有；预览未满 |
| `/aip/evals` | Evals 门控 | 评测门控 | **75** | **75** | 读写可用；分项示意 |
| `/aip/drafts` | Draft 审批台 | HITL 审批写入 | **0** | **75** | 真 approve/reject + 演示降级（W3 A3） |
| `/aip/lineage` | 决策谱系 | 决策追溯 | **55** | **60** | 可拉 lineage |
| `/aip/observability` | 可观测性 | Trace/指标看板 | **50** | **60** | Overview/Traces 接采样 API（W2 A5） |

### D. 模型管理

| 路径 | 页面 | 职责一句话 | 旧% | **新%** | 现状要点 |
|------|------|------------|-----|--------|----------|
| `/aip/model-catalog` | 模型目录 | 模型浏览/注册 | **0** | **65** | catalog/register API（W2 A7） |
| `/aip/model-providers` | 模型供应商 | Provider/探针 | **65** | **75** | API 实 |
| `/aip/model-router` | 模型路由 | 路由规则/试聊 | **75** | **80** | CRUD+试聊较齐 |
| `/aip/capacity` | 容量管理 | 配额/限流 | **0** | **60** | usage/limits API（W2 A6） |

### E. 本体 · 数字孪生

| 路径 | 页面 | 职责一句话 | 旧% | **新%** | 现状要点 |
|------|------|------------|-----|--------|----------|
| `/ontology` | 本体管理 | Discover/类型目录 | — | **70** | 收藏/最近/列表+API |
| `/workshop/graph` | 对象探索 | 实例探索前端 | 40 | **65** | 浏览有；三栏保真一般 |
| `/ontology/funnel` | 本体提案 | 提案漏斗 | ~60 | **60** | 阶段 API |
| `/ontology/okf-funnel` | OKF funnel | 行业漏斗映射 | ~60 | **60** | 映射可用 |
| `/ontology/okf-overview` | OKF 概览 | OKF 总览 | ~60 | **55** | 壳深有限 |
| `/ontology/graph-health` | 图谱健康度 | 图质量指标 | ~80 | **80** | 指标 API 较齐 |
| `/ontology/wiki` | 活知识 Wiki | Wiki 知识卡 | ~65 | **60** | 非全量编辑器 |
| `/ontology/wiki-index` | Wiki 索引 | Wiki 索引表 | ~65 | **60** | 列表可用 |
| `/ontology/branches` | 分支管理 | Ontology 分支 | ~70 | **70** | checkout/merge 类 |
| `/ontology/wiki/:id` | Wiki 详情 | 全文编辑 | 0–20 | **55** | 可编辑保存+版本列表（W3 C1） |
| `/ontology/wiki/:id/diff` | Wiki 差异 | 版本对比 | **0** | **60** | 两版本文本 diff（W3 C5） |

### F. 管道与数据治理 / 数据源

| 路径 | 页面 | 职责一句话 | 旧% | **新%** | 现状要点 |
|------|------|------------|-----|--------|----------|
| `/data/pipelines` | 管道构建 | 管道列表入口 | **30** | **55** | 进画布有；非全 SVG 图例 |
| `/data/pipelines/:id` | 管道详情 | DAG 编辑 | 30 | **70** | 历史 Tab + 变换试运行（W3 C6） |
| `/data/pipeline-proposals` | 管道提案 | 提案审阅 | **10** | **45** | 列表壳；审阅薄 |
| `/data/schedules` | 计划编辑器 | 调度 | **30** | **50** | CRUD 向 |
| `/data/builds` | 搭建 | Build 列表 | **0** | **50** | 列表有；弹窗未对齐 |
| `/data/datasets` | 数据集 | 数据集目录 | **40** | **60** | 采样预览 API |
| `/data/code-repos` | 代码库 | 仓库连接 | **10** | **50** | 非四栏 IDE |
| `/data/lineage` | 数据沿袭 | 血缘图 | **20** | **50** | 图有；展开弱 |
| `/data/health` | 数据健康 | 健康规则 | **20** | **55** | 仪表有 |
| `/data` | 数据链接器 | 连接器网格 | **40** | **60** | 源管理 API |
| `/data/connections` | 数据连接 | 连接列表 | — | **55** | 管理页 |
| `/data/sources/new` | 新建数据源 | 向导建源 | **0** | **55** | 多步；演示向 |
| `/data/agents` | 边缘代理 | Edge Agent | **20** | **45** | 列表；登记弱 |
| `/data/sync-config` | 同步配置 | 同步策略 | **30** | **55** | 表单+API |
| `/data/sync-routes` | 同步路由 | 路由启停 | **20** | **50** | 启停有 |
| `/data/media-sets` | 媒体集 | 媒体上传 | **10** | **55** | 上传 API |
| `/aip/doc-intelligence` | 文档智能 | 文档抽取 | **0** | **55** | 抽取 API；pipeline-doc-intel 已并入（W4 E1） |

### G. 运维交付

| 路径 | 页面 | 职责一句话 | 旧% | **新%** | 现状要点 |
|------|------|------------|-----|--------|----------|
| `/settings/local-platform` | 本地平台 | 本机探活/控制 | — | **70** | 实操向 |
| `/settings/ops-start-guide` | 启停说明 | 运维文档 | — | **75** | 文档页 |
| `/apollo` | Hub 舰队 | Spoke 舰队总览 | **30** | **60** | 卡+probe |
| `/apollo/release` | Release | 发布通道 | **20** | **55** | 通道 UI+API |
| `/apollo/spoke` | Spoke 详情 | 单 Spoke | **20** | **55** | Full/Lite 内容 |
| `/apollo/ferry` | Ferry | 摆渡导入导出 | **10** | **50** | 步骤+API |
| `/apollo/assets` | FDE 资产包 | 资产清单 | **20** | **55** | 表+徽章 |
| `/apollo/change` | 变更审批 | 变更单 | **10** | **55** | 双栏+API |
| `/apollo/config` | 配置与密钥 | 覆盖/密钥 | **10** | **55** | 壳+API |
| `/apollo/cases` | 接入案例 | 案例叙事 | **10** | **40** | 静态页 |
| `/apollo/provisioning` | SaaS 开通 | 开通流程 | — | **50** | 深度有限 |

### 复审结论（给产品/排期）

1. **「10%」不等于全站只有 10%**：那是早期单页（如模块接口）或「深度检查进度」口径；**今日菜单功能中位大约 55–65%**。
2. **已从「缺失」变成「有页」**：组件注册表 / 变量 / 样式 / Draft / AIP 助手 / 容量壳 / 多块运维 —— 但 **变量、分析师、可观测、容量、文档智能** 仍偏演示（MOCK、无写回）。
3. **相对视觉稿最吃亏**：画布（保真）、Wiki 详情（编辑器）、模块接口（契约编辑）、变量（数据闭环）。
4. **相对最可用**：成熟度、工具面板、Evals、模型路由/供应商、图谱健康、本体 Discover、部分数据连接与运维。
5. **建议下一波功能优先**（非纯视觉）：① 变量 API↔画布；② 模块接口 schema 读写；③ Draft 接真审批；④ 画布缺面板按视觉补。
6. **统一补齐排期**：见 [`227-未完成项补齐计划.md`](./227-未完成项补齐计划.md)；P1/详情最新状态见 `-2`/`-3` v1.1。

### H. 二级详情页完整度（与 checklist-3 对齐，2026-07-29）

| 路径 | 页面 | **现%** | 要点 |
|------|------|--------|------|
| `/ontology/object-types/:id` | 对象类型详情 | **80** | 元数据+SVG 链接图（W3 C2） |
| `/ontology/link-types/:id` | 链接类型详情 | **70** | SVG 关系图（W4 C8a） |
| `/ontology/action-types/:id` | Action 详情 | **70** | Overview 双列+徽章（W4 C8b） |
| `/ontology/properties/:typeId` | 属性编辑 | **70** | 列映射 Tab（W3 C3） |
| `/ontology/functions` | Function | **65** | 参数表+试跑（W3 C4） |
| `/ontology/wiki/:id` | Wiki 详情 | **55** | 可编辑保存+版本（W3 C1） |
| `/ontology/wiki/:id/diff` | Wiki 差异 | **60** | 文本 diff（W3 C5） |
| `/data/pipelines/:id` | 管道详情 | **70** | 历史/变换（W3 C6） |
| `/data/sources/:id` | 数据源详情 | **65** | Schema 树+预览（W3 C7） |

---

## 2. 已深度检查的页面（7 个）

| # | 页面 | 视觉稿文件 | 检查状态 | 文档位置 |
|---|---|---|---|---|
| 1 | 概览 | `../foundry/html/index.html` | ✅ 已检查 | 223-menu-alignment-full.md |
| 2 | 应用列表 | `../foundry/html/workshop.html` | ✅ 已检查 | 223-ui-alignment-plan.md Phase A |
| 3 | 订单管理 | `../foundry/html/workshop-app-order.html` | ✅ 已检查 | 223-ui-alignment-plan.md Phase A |
| 4 | 风险告警管理 | `../foundry/html/workshop-module.html` | ✅ 已检查 | 223-ui-alignment-plan.md Phase A |
| 5 | 态势大屏 | `../foundry/html/workshop-cop.html` | ✅ 已检查 | 223-ui-alignment-plan.md Phase A |
| 6 | Buddy 助手 | `../foundry/html/workshop-aip-chat.html` | ✅ 已检查 | 223-ui-alignment-plan.md Phase A |
| 7 | 创建应用 | `../foundry/html/workshop-create.html` | ✅ 已检查 | 223-ui-alignment-plan.md Phase A |

---

## 3. 待深度检查的页面清单（按优先级排序）

### 3.1 P0：工作台 + 应用程序构建工具（13 页）

**工作台（剩余 6 页）：**

| # | 页面 | 视觉稿文件 | 系统路径 | 备注 |
|---|---|---|---|---|
| 1 | 画布编辑 | `../foundry/html/workshop-canvas.html` | `/workshop/canvas` | 视觉稿 145KB，最复杂 |
| 2 | 模块接口 | `../foundry/html/workshop-module-interface.html` | `/workshop/module-interface` |  |
| 3 | 事件配置 | `../foundry/html/workshop-events.html` | `/workshop/events` |  |
| 4 | 对象探索 | `../foundry/html/workshop-object-view.html` | `/workshop/graph` |  |
| 5 | 发布入口 | `../foundry/html/workshop-publish.html` | `/workshop/publish` |  |
| 6 | 模块管理（系统多出） | - | `/workshop/module` | 系统多出，检查是否保留 |

**应用程序构建工具（7 页，3 个缺失）：**

| # | 页面 | 视觉稿文件 | 系统路径 | 备注 |
|---|---|---|---|---|
| 7 | 组件注册表 | `../foundry/html/workshop-widget-registry.html` | - | 🔴 系统缺失，需全新建 |
| 8 | 变量管理器 | `../foundry/html/workshop-variables.html` | - | 🔴 系统缺失，需全新建 |
| 9 | 主题与样式 | `../foundry/html/workshop-styles.html` | - | 🔴 系统缺失，需全新建 |
| 10 | 画布编辑 | `../foundry/html/workshop-canvas.html` | `/workshop/canvas` | 与工作台共用 |
| 11 | 模块接口 | `../foundry/html/workshop-module-interface.html` | `/workshop/module-interface` | 与工作台共用 |
| 12 | 事件配置 | `../foundry/html/workshop-events.html` | `/workshop/events` | 与工作台共用 |
| 13 | 发布入口 | `../foundry/html/workshop-publish.html` | `/workshop/publish` | 与工作台共用 |

> 注：工作台和应用程序构建工具有 4 页共用（画布编辑、模块接口、事件配置、发布入口）

### 3.2 P1：AIP 决策引擎 + 模型管理 + 本体（31 页）

**AIP 决策引擎（14 页，2 个缺失）：**

| # | 页面 | 视觉稿文件 | 系统路径 | 备注 |
|---|---|---|---|---|
| 1 | AIP 助手 | `../foundry/html/aip-assist.html` | `/aip/assist` | 🔴 路由未注册 |
| 2 | 对话机器人 | `../foundry/html/agents.html` | `/aip/studio` | 名字差异（Chatbot Studio → 对话机器人） |
| 3 | AIP 分析师 | `../foundry/html/aip-analyst.html` | `/aip/analyst` | 🔴 路由未注册 |
| 4 | AIP 逻辑画布 | `../foundry/html/aip-logic.html` | `/aip/logic` |  |
| 5 | Agent 工具面板 | `../foundry/html/aip-tools.html` | `/aip/tools` |  |
| 6 | 成熟度楼梯 | `../foundry/html/aip-maturity.html` | `/aip/maturity` |  |
| 7 | 智能体目录 | `../foundry/html/agent-registry.html` | `/aip/agent-registry` | 名字差异（智能体注册表 → 智能体目录） |
| 8 | 智能体插件 | `../foundry/html/aip-capabilities.html` | `/aip/capabilities` |  |
| 9 | Evals 门控 | `../foundry/html/aip-evals.html` | `/aip/evals` |  |
| 10 | Draft 审批台 | `../foundry/html/aip-draft-inbox.html` | `/aip/drafts` |  |
| 11 | 决策谱系 | `../foundry/html/aip-decision-lineage.html` | `/aip/lineage` |  |
| 12 | 可观测性 | `../foundry/html/aip-observability.html` | `/aip/observability` |  |
| 13 | 智能体列表（系统多出） | - | `/aip/agents` | 系统多出 |
| 14 | 智能体导入（系统多出） | `../foundry/html/aip-agent-import.html` | `/aip/agent-import` | 系统多出 |
| 15 | 能力导入（系统多出） | `../foundry/html/aip-capability-import.html` | `/aip/capability-import` | 系统多出 |

**模型管理（4 页，2 个缺失）：**

| # | 页面 | 视觉稿文件 | 系统路径 | 备注 |
|---|---|---|---|---|
| 16 | 模型目录 | `../foundry/html/aip-model-catalog.html` | `/aip/model-catalog` | 🔴 路由未注册 |
| 17 | 模型供应商 | `../foundry/html/aip-model-providers.html` | `/aip/model-providers` |  |
| 18 | 模型路由 | `../foundry/html/aip-model-router.html` | `/aip/model-router` |  |
| 19 | 容量管理 | `../foundry/html/aip-capacity-management.html` | `/aip/capacity` | 🔴 路由未注册 |

**本体·数字孪生（13 页，5 个详情页缺失）：**

| # | 页面 | 视觉稿文件 | 系统路径 | 备注 |
|---|---|---|---|---|
| 20 | 本体管理 | `../foundry/html/ontology.html` | `/ontology` |  |
| 21 | 对象探索 | `../foundry/html/workshop-object-view.html` | `/workshop/graph` | 与工作台共用 |
| 22 | 本体提案 | `../foundry/html/ontology-funnel.html` | `/ontology/funnel` | 名字差异（漏斗管道 → 本体提案） |
| 23 | 图谱健康度 | `../foundry/html/ontology-graph-health.html` | `/ontology/graph-health` |  |
| 24 | 活知识 Wiki | `../foundry/html/ontology-wiki-index.html` | `/ontology/wiki` | 视觉稿合并为 1 项，系统拆 2 项 |
| 25 | OKF funnel | `../foundry/html/funnel.html` | `/ontology/okf-funnel` | 名字差异（OKF 行业漏斗 → OKF funnel） |
| 26 | OKF 概览 | `../foundry/html/okf-funnel.html` | `/ontology/okf-overview` |  |
| 27 | 分支管理 | `../foundry/html/ontology-branches.html` | `/ontology/branches` |  |
| 28 | Wiki 详情 | `../foundry/html/ontology-wiki.html` | - | 🔴 详情页，系统缺失 |
| 29 | Wiki 差异 | `../foundry/html/ontology-wiki-diff.html` | - | 🔴 详情页，系统缺失 |
| 30 | 属性类型详情 | `../foundry/html/ontology-property.html` | - | 🔴 详情页，系统缺失 |
| 31 | Function 详情 | `../foundry/html/ontology-function.html` | - | 🔴 详情页，系统缺失 |
| 32 | 对象详情 | `../foundry/html/ontology-object.html` | - | ⚠️ 不在侧栏，需确认 |
| 33 | 动作详情 | `../foundry/html/ontology-action.html` | - | ⚠️ 不在侧栏，需确认 |
| 34 | 链接详情 | `../foundry/html/ontology-link.html` | - | ⚠️ 不在侧栏，需确认 |

### 3.3 P2：管道 + 数据源 + 运维（26 页）

**管道与数据治理（9 页，1 个缺失）：**

| # | 页面 | 视觉稿文件 | 系统路径 | 备注 |
|---|---|---|---|---|
| 1 | 管道构建 | `../foundry/html/pipeline-list.html` | `/data/pipelines` |  |
| 2 | 管道提案 | `../foundry/html/pipeline-proposals.html` | `/data/pipeline-proposals` |  |
| 3 | 计划编辑器 | `../foundry/html/schedules.html` | `/data/schedules` |  |
| 4 | 搭建 | `../foundry/html/builds.html` | `/data/builds` |  |
| 5 | 数据集预览 | `../foundry/html/dataset.html` | `/data/datasets` |  |
| 6 | 代码库 | `../foundry/html/code-repositories.html` | `/data/code-repos` |  |
| 7 | 数据沿袭 | `../foundry/html/lineage.html` | `/data/lineage` |  |
| 8 | 数据健康 | `../foundry/html/health.html` | `/data/health` |  |
| 9 | DocIntel 管道 | `../foundry/html/pipeline-doc-intel.html` | - | 🔴 系统缺失 |
| 10 | 管道详情 | `../foundry/html/pipeline.html` | - | ⚠️ 不在侧栏，需确认 |

**数据源与同步（7 页，2 个缺失）：**

| # | 页面 | 视觉稿文件 | 系统路径 | 备注 |
|---|---|---|---|---|
| 11 | 数据链接器 | `../foundry/html/data-connection.html` | `/data` |  |
| 12 | 边缘代理 | `../foundry/html/data-connection-agents.html` | `/data/agents` |  |
| 13 | 同步配置 | `../foundry/html/sync.html` | `/data/sync-config` |  |
| 14 | 同步路由 | `../foundry/html/sync-routing.html` | `/data/sync-routes` |  |
| 15 | 媒体集 | `../foundry/html/media-sets.html` | `/data/media-sets` |  |
| 16 | 文档智能 | `../foundry/html/document-intelligence.html` | `/aip/doc-intelligence` | 🔴 路由未注册 |
| 17 | 数据源新建 | `../foundry/html/source-new.html` | - | 🔴 系统缺失 |
| 18 | 数据源详情 | `../foundry/html/source-detail.html` | - | ⚠️ 不在侧栏，需确认 |

**运维交付（10 页，2 个系统多出）：**

| # | 页面 | 视觉稿文件 | 系统路径 | 备注 |
|---|---|---|---|---|
| 19 | Hub 舰队 | `../foundry/html/apollo-hub.html` | `/apollo` |  |
| 20 | Release 通道 | `../foundry/html/apollo-release.html` | `/apollo/release` |  |
| 21 | Spoke 详情 | `../foundry/html/apollo-spoke.html` | `/apollo/spoke` |  |
| 22 | Ferry 摆渡 | `../foundry/html/apollo-ferry.html` | `/apollo/ferry` |  |
| 23 | FDE 资产包 | `../foundry/html/apollo-assets.html` | `/apollo/assets` |  |
| 24 | 变更审批 | `../foundry/html/apollo-change-mgmt.html` | `/apollo/change` |  |
| 25 | 配置与密钥 | `../foundry/html/apollo-config.html` | `/apollo/config` |  |
| 26 | 接入案例 | `../foundry/html/integration-cases.html` | `/apollo/cases` |  |
| 27 | 本机探活（系统多出） | - | `/settings/local-platform` | 开发辅助 |
| 28 | 启停说明（系统多出） | - | `/settings/ops-start-guide` | 开发辅助 |
| 29 | SaaS 开通（系统多出） | - | `/apollo/provisioning` | 系统多出 |

---

## 4. 检查顺序建议

按优先级和依赖关系，建议按以下顺序进行深度检查：

```
第 1 批：P0 工作台剩余（6页）
    画布编辑 → 模块接口 → 事件配置 → 对象探索 → 发布入口 → 模块管理

第 2 批：P0 应用程序构建工具（3页全新）
    组件注册表 → 变量管理器 → 主题与样式

第 3 批：P1 AIP 决策引擎（14页）
    AIP 助手 → 对话机器人 → AIP 分析师 → AIP 逻辑画布 → Agent 工具面板
    → 成熟度楼梯 → 智能体目录 → 智能体插件 → Evals 门控 → Draft 审批台
    → 决策谱系 → 可观测性 → 智能体列表 → 智能体导入 → 能力导入

第 4 批：P1 模型管理（4页）
    模型目录 → 模型供应商 → 模型路由 → 容量管理

第 5 批：P1 本体·数字孪生（13页）
    本体管理 → 对象探索 → 本体提案 → 图谱健康度 → 活知识 Wiki
    → OKF funnel → OKF 概览 → 分支管理 → Wiki 详情 → Wiki 差异
    → 属性类型详情 → Function 详情 → （对象/动作/链接详情待确认）

第 6 批：P2 管道与数据治理（9页）
    管道构建 → 管道提案 → 计划编辑器 → 搭建 → 数据集预览
    → 代码库 → 数据沿袭 → 数据健康 → DocIntel 管道 → （管道详情待确认）

第 7 批：P2 数据源与同步（7页）
    数据链接器 → 边缘代理 → 同步配置 → 同步路由 → 媒体集
    → 文档智能 → 数据源新建 → （数据源详情待确认）

第 8 批：P2 运维交付（10页）
    Hub 舰队 → Release 通道 → Spoke 详情 → Ferry 摆渡 → FDE 资产包
    → 变更审批 → 配置与密钥 → 接入案例 → （3个系统多出项检查）
```

---

## 5. 每页检查输出模板

对每个页面，输出以下格式的文档（可追加到 223-full-ui-gap-analysis.md）：

```markdown
### X.X 页面名称

**视觉稿文件**：`xxx.html`
**系统路径**：`/xxx/yyy`（如不存在则标"缺失"）
**当前完整度**：0% / 30% / 60% / 90%
**改造工作量**：X 人天
**优先级**：P0 / P1 / P2

#### 页面结构
- 布局：X 栏布局（左 Xpx / 中自适应 / 右 Xpx）
- 顶部：面包屑 + 标题 + 操作按钮
- 主内容：...
- 侧边栏：...
- 底部：...

#### 组件清单
| 组件 | 视觉稿有 | 系统有 | 状态 | 备注 |
|---|---|---|---|---|
| 组件A | ✅ | ✅ | 一致 |  |
| 组件B | ✅ | ⚠️ | 需改造 | 样式/交互不符 |
| 组件C | ✅ | ❌ | 需新建 |  |

#### 数据与 API
- 需要的接口：GET /v1/xxx, POST /v1/xxx, ...
- 需要的表/字段：table_xxx.field_yyy
- 测试数据：X 条，覆盖 Y 个场景

#### 核心差距（按优先级）
- **P0**：xxx
- **P1**：xxx
- **P2**：xxx

#### 风险与依赖
- 技术风险：...
- 后端依赖：...
- 其他依赖：...
```

---

## 7. P0 深度检查结果（工作台 + 应用程序构建工具，共 9 页）

> 检查日期：2026-07-26
> 检查范围：P0 优先级的 9 个页面
> 总体结论：P0 共 9 页，其中 3 页系统完全缺失（组件注册表、变量管理器、主题与样式），6 页有不同程度的差距

### 7.1 画布编辑

**视觉稿文件**：`../foundry/html/workshop-canvas.html`（1867 行，最复杂页面）
**系统路径**：`/workshop/canvas`
**当前完整度**：30%
**改造工作量**：8-10 人天
**优先级**：P0

#### 页面结构
- 布局：**三栏布局**（左组件树 280px / 中画布自适应 / 右属性面板 320px）
- 顶部 Topbar：面包屑 + 模块名 + 版本标签 + Tab 切换（文件/帮助/页面）+ 动作/保存按钮 + 关闭
- 工具栏：3 模式切换（组件/工作流/预览）+ 9 个 Tab（仪表盘/查询/函数/对象/事件/数据/依赖/样式/变量）
- 左栏：组件树（搜索 + 分组 + 可展开层级 + 删除组件 + 添加组件入口 + 拖拽组件面板）
- 中栏：画布区域（Widget 卡片 + 选中态 + 拖拽放置指示器 + 底部相关配置链接）
- 右栏：属性面板（4 个 Tab：内容/样式/事件/数据）
- 工作流模式：另外一套三栏（左触发器列表 / 中 SVG 流程图 / 右节点详情）
- 底部：9 个 pop-panel（仪表盘/查询/函数/对象/事件/数据/依赖/样式/变量）

#### 组件清单
| 组件 | 视觉稿有 | 系统有 | 状态 | 备注 |
|---|---|---|---|---|
| Topbar（模块名+版本+Tab+保存） | ✅ | ❌ | 需新建 |  |
| 工具栏（3 模式 + 9 Tab） | ✅ | ❌ | 需新建 |  |
| 组件树（搜索+层级+拖拽） | ✅ | ⚠️ | 需改造 | 系统可能有基础版 |
| 画布区域（拖拽放置+选中态） | ✅ | ⚠️ | 需改造 | 系统可能有基础版 |
| 属性面板（4 Tab） | ✅ | ❌ | 需新建 | 内容/样式/事件/数据 |
| 工作流模式三栏 | ✅ | ❌ | 需新建 | 触发器列表+SVG流程+节点详情 |
| 9 个 pop-panel | ✅ | ❌ | 需新建 | 仪表盘/查询/函数/对象/事件/数据/依赖/样式/变量 |
| 拖拽组件面板（6 组件） | ✅ | ❌ | 需新建 | 表格/图表/表单/按钮/地图/文本 |

#### 数据与 API
- 需要的接口：
  - GET /v1/modules/:id/config（获取画布完整配置）
  - PUT /v1/modules/:id/config（保存画布配置）
  - GET /v1/widgets（获取可用组件列表）
  - GET /v1/modules/:id/events（获取事件配置）
  - GET /v1/modules/:id/queries（获取查询函数）
  - GET /v1/modules/:id/variables（获取变量列表）
- 需要的表/字段：
  - module_widgets 表（组件实例：id/module_id/widget_type/config/parent_id/sort_order）
  - module_events 表（事件配置）
  - module_queries 表（查询函数）
  - module_variables 表（变量）
- 测试数据：至少 1 个完整模块的画布配置（含 10+ 组件）

#### 核心差距（按优先级）
- **P0**：三栏布局 + 组件树 + 画布 + 属性面板（编辑模式核心）
- **P0**：9 个 pop-panel（工具栏下方展开面板）
- **P1**：工作流模式（触发器 + SVG 流程图 + 节点详情）
- **P1**：拖拽添加组件功能
- **P2**：Topbar 完整功能（版本、Tab、保存分支）

#### 风险与依赖
- 技术风险：极高，画布编辑器是最复杂的页面，涉及拖拽、状态管理、动态渲染
- 后端依赖：需要新增 module_widgets、module_events、module_queries、module_variables 表
- 其他依赖：依赖组件注册表、变量管理器、主题与样式页面的数据

---

### 7.2 模块接口

**视觉稿文件**：`../foundry/html/workshop-module-interface.html`（197 行，简单页面）
**系统路径**：`/workshop/module-interface`
**当前完整度**：45%（2026-07-29 复审；历史曾标 10% 占位——见 §1.1）
**改造工作量**：1-2 人天
**优先级**：P0

#### 页面结构
- 布局：单栏布局（最大宽度 5xl 居中）
- 顶部：标题 + 描述
- 主内容：2 列网格
  - 左卡：接口定义（input/output 列表，类似 API 文档）
  - 右卡：嵌套 Loop 示意图（父 Module → 子 Loop → 子 Module）
- 底部：提示条（蓝色背景，说明嵌套 Module 解耦）

#### 组件清单
| 组件 | 视觉稿有 | 系统有 | 状态 | 备注 |
|---|---|---|---|---|
| 接口定义卡片 | ✅ | ❌ | 需新建 | input/output 列表 |
| 嵌套 Loop 示意图 | ✅ | ❌ | 需新建 | 树形结构展示 |
| 提示条 | ✅ | ⚠️ | 复用 | 可复用现有提示组件 |

#### 数据与 API
- 需要的接口：
  - GET /v1/modules/:id/interface（获取模块接口定义）
  - PUT /v1/modules/:id/interface（保存模块接口）
- 需要的表/字段：
  - module_interfaces 表（接口定义：module_id/input_schema/output_schema）
- 测试数据：至少 2 个模块的接口定义

#### 核心差距（按优先级）
- **P0**：接口定义卡片（input/output 列表展示）
- **P1**：嵌套 Loop 示意图（可视化展示）
- **P2**：接口编辑功能（当前可能只读）

#### 风险与依赖
- 技术风险：低，页面结构简单
- 后端依赖：module_interfaces 表
- 其他依赖：无

---

### 7.3 事件配置

**视觉稿文件**：`../foundry/html/workshop-events.html`（608 行，中等复杂度）
**系统路径**：`/workshop/events`
**当前完整度**：20%
**改造工作量**：3-4 人天
**优先级**：P0

#### 页面结构
- 布局：上部配置列表 + 下部向导式配置器
- 顶部：标题 + 描述
- 事件列表：表格（事件名 / 触发器 / 动作 / 状态）
- 配置向导：
  - 步骤条（触发器 → 动作 → 变量 → 幂等键 → 完成）
  - 步骤 1：选择触发器类型（6 种：页面加载/行点击/按钮点击/筛选变化/定时器/自定义）
  - 步骤 2：选择动作类型（5 种：更新变量/跳转页面/打开弹窗/调用函数/触发事件）
  - 动作参数配置区
  - 预览卡片

#### 组件清单
| 组件 | 视觉稿有 | 系统有 | 状态 | 备注 |
|---|---|---|---|---|
| 事件列表表格 | ✅ | ⚠️ | 需改造 |  |
| 步骤条 | ✅ | ❌ | 需新建 | 5 步向导 |
| 触发器类型选择（6 种卡片） | ✅ | ❌ | 需新建 | 卡片式选择 |
| 动作类型选择（5 种卡片） | ✅ | ❌ | 需新建 | 卡片式选择 |
| 动作参数配置器 | ✅ | ❌ | 需新建 | 动态表单 |
| 预览卡片 | ✅ | ❌ | 需新建 |  |

#### 数据与 API
- 需要的接口：
  - GET /v1/modules/:id/events（获取事件列表）
  - POST /v1/modules/:id/events（新建事件）
  - PUT /v1/modules/:id/events/:event_id（更新事件）
  - DELETE /v1/modules/:id/events/:event_id（删除事件）
- 需要的表/字段：
  - module_events 表（id/module_id/trigger_type/trigger_config/action_type/action_config/idempotency_key/status）
- 测试数据：至少 5 个事件配置（覆盖各触发器类型）

#### 核心差距（按优先级）
- **P0**：事件列表表格
- **P0**：向导式配置器（步骤条 + 触发器选择 + 动作选择）
- **P1**：动作参数动态配置
- **P2**：幂等键配置

#### 风险与依赖
- 技术风险：中，向导式配置器交互较复杂
- 后端依赖：module_events 表
- 其他依赖：与画布编辑器的事件 Tab 数据互通

---

### 7.4 对象探索

**视觉稿文件**：`../foundry/html/workshop-object-view.html`（324 行，中等复杂度）
**系统路径**：`/workshop/graph`
**当前完整度**：40%
**改造工作量**：2-3 人天
**优先级**：P0

#### 页面结构
- 布局：三栏布局（左对象类型树 / 中对象列表 / 右对象详情）
- 顶部：搜索栏 + 筛选器
- 左栏：对象类型树（可展开，显示数量徽章）
- 中栏：对象列表（表格/卡片视图切换，分页）
- 右栏：对象详情（属性列表 / 关联对象 / 时间线）

#### 组件清单
| 组件 | 视觉稿有 | 系统有 | 状态 | 备注 |
|---|---|---|---|---|
| 对象类型树 | ✅ | ⚠️ | 需改造 |  |
| 对象列表（表格/卡片切换） | ✅ | ⚠️ | 需改造 |  |
| 对象详情面板 | ✅ | ⚠️ | 需改造 |  |
| 搜索 + 筛选器 | ✅ | ⚠️ | 需改造 |  |

#### 数据与 API
- 需要的接口：
  - GET /v1/ontology/object-types（获取对象类型列表）
  - GET /v1/ontology/objects（获取对象列表，支持筛选）
  - GET /v1/ontology/objects/:id（获取对象详情）
- 需要的表/字段：
  - 复用现有的本体相关表
- 测试数据：至少 3 种对象类型，每种 20+ 条实例

#### 核心差距（按优先级）
- **P0**：三栏布局对齐
- **P1**：对象详情面板内容丰富度
- **P2**：关联对象图谱可视化

#### 风险与依赖
- 技术风险：中，详情面板内容较多
- 后端依赖：本体 API
- 其他依赖：无

---

### 7.5 发布入口

**视觉稿文件**：`../foundry/html/workshop-publish.html`（173 行，简单页面）
**系统路径**：`/workshop/publish`
**当前完整度**：20%
**改造工作量**：1-2 人天
**优先级**：P0

#### 页面结构
- 布局：单栏，卡片式
- 顶部：标题 + 描述
- 发布流程：步骤条（开发 → 测试 → 预发布 → 生产）
- 环境卡片列表（每个环境一个卡片）
- 发布按钮 + 回滚按钮

#### 组件清单
| 组件 | 视觉稿有 | 系统有 | 状态 | 备注 |
|---|---|---|---|---|
| 发布步骤条 | ✅ | ❌ | 需新建 |  |
| 环境卡片 | ✅ | ❌ | 需新建 |  |
| 发布/回滚操作 | ✅ | ❌ | 需新建 |  |

#### 数据与 API
- 需要的接口：
  - GET /v1/modules/:id/deployments（获取发布历史）
  - POST /v1/modules/:id/deploy（发布到指定环境）
  - POST /v1/modules/:id/rollback（回滚）
- 需要的表/字段：
  - module_deployments 表（id/module_id/environment/version/status/deployed_at/deployed_by）
- 测试数据：至少 3 个环境的发布记录

#### 核心差距（按优先级）
- **P0**：发布流程可视化（步骤条 + 环境卡片）
- **P1**：发布/回滚操作
- **P2**：发布历史记录

#### 风险与依赖
- 技术风险：低
- 后端依赖：module_deployments 表
- 其他依赖：无

---

### 7.6 模块管理（系统多出）

**视觉稿文件**：无（系统多出的页面）
**系统路径**：`/workshop/module`
**当前完整度**：60%
**改造工作量**：0.5 人天（确认是否保留）
**优先级**：P2

#### 说明
- 视觉稿侧栏没有"模块管理"这一项
- 系统当前有这个页面，功能是 Module CRUD 列表
- 建议：保留但改名为"模块管理"（与"组件注册表"区分），不进侧栏主菜单，可从其他页面跳转

---

### 7.7 组件注册表

**视觉稿文件**：`../foundry/html/workshop-widget-registry.html`（449 行，中等复杂度）
**系统路径**：`/workshop/widget-registry`
**当前完整度**：70%（2026-07-29 复审；历史 0%「缺失」已过时）
**改造工作量**：3-4 人天
**优先级**：P0

#### 页面结构
- 布局：单栏，网格卡片
- 顶部：标题 + 描述
- 筛选 Tab：全部 / 平台内置 / 市场安装 / 代码开发（4 个来源）
- 组件网格：3 列卡片网格
  - 每张卡片：图标 + 名称 + 描述 + 版本 + 使用数 + 来源标签
- 组件详情：点击卡片弹出详情面板

#### 组件清单
| 组件 | 视觉稿有 | 系统有 | 状态 | 备注 |
|---|---|---|---|---|
| 筛选 Tab（4 个来源） | ✅ | ❌ | 需新建 |  |
| 组件卡片网格 | ✅ | ❌ | 需新建 | 3 列布局 |
| 组件详情面板 | ✅ | ❌ | 需新建 |  |
| 搜索框 | ✅ | ❌ | 需新建 |  |

#### 数据与 API
- 需要的接口：
  - GET /v1/widgets（获取组件列表，支持按来源筛选）
  - GET /v1/widgets/:id（获取组件详情）
  - POST /v1/widgets（注册新组件）
- 需要的表/字段：
  - widget_registry 表（id/name/description/type/source/version/icon/config_schema/usage_count）
  - widget_categories 表（组件分类）
- 测试数据：至少 16 个组件（12 内置 + 3 市场 + 1 自定义）

#### 核心差距（按优先级）
- **P0**：组件列表 + 筛选 Tab + 卡片网格
- **P1**：组件详情面板
- **P2**：组件注册/上传功能

#### 风险与依赖
- 技术风险：中
- 后端依赖：widget_registry 表
- 其他依赖：画布编辑器的组件面板依赖此页面的数据

---

### 7.8 变量管理器

**视觉稿文件**：`../foundry/html/workshop-variables.html`（782 行，中等复杂度）
**系统路径**：`/workshop/variables`
**当前完整度**：35%（2026-07-29 复审；UI 已对账，数据闭环弱；历史 0%「缺失」已过时）
**改造工作量**：3-4 人天
**优先级**：P0

#### 页面结构
- 布局：两栏布局（左变量列表 / 右变量详情）
- 顶部：标题 + 搜索 + 新建变量按钮
- 左栏：变量列表（分组：字符串/数字/布尔/对象/数组）
  - 每条：变量名 + 类型图标 + 默认值预览 + 作用域标签
- 右栏：变量详情
  - 基本信息（名称/类型/作用域/描述）
  - 默认值配置（根据类型动态显示输入控件）
  - 使用位置（在哪些组件/事件中使用了这个变量）

#### 组件清单
| 组件 | 视觉稿有 | 系统有 | 状态 | 备注 |
|---|---|---|---|---|
| 变量列表（分组） | ✅ | ❌ | 需新建 |  |
| 变量详情面板 | ✅ | ❌ | 需新建 |  |
| 类型动态表单 | ✅ | ❌ | 需新建 | 根据类型显示不同输入 |
| 使用位置列表 | ✅ | ❌ | 需新建 |  |

#### 数据与 API
- 需要的接口：
  - GET /v1/modules/:id/variables（获取模块变量列表）
  - POST /v1/modules/:id/variables（新建变量）
  - PUT /v1/modules/:id/variables/:var_id（更新变量）
  - DELETE /v1/modules/:id/variables/:var_id（删除变量）
  - GET /v1/modules/:id/variables/:var_id/usage（获取变量使用位置）
- 需要的表/字段：
  - module_variables 表（id/module_id/name/type/default_value/scope/description）
- 测试数据：至少 10 个变量（覆盖各种类型）

#### 核心差距（按优先级）
- **P0**：变量列表 + 分组 + 详情
- **P1**：类型动态表单
- **P1**：使用位置追踪
- **P2**：变量导入/导出

#### 风险与依赖
- 技术风险：中，类型动态表单较复杂
- 后端依赖：module_variables 表
- 其他依赖：画布编辑器的变量 Tab 依赖此页面的数据

---

### 7.9 主题与样式

**视觉稿文件**：`../foundry/html/workshop-styles.html`（394 行，中等复杂度）
**系统路径**：`/workshop/styles`
**当前完整度**：60%（2026-07-29 复审；历史 0%「缺失」已过时）
**改造工作量**：2-3 人天
**优先级**：P0

#### 页面结构
- 布局：两栏布局（左主题列表 / 右主题编辑器）
- 顶部：标题 + 新建主题按钮
- 左栏：主题预设列表（浅色/暗色/高对比度等）
  - 每张卡片：主题预览缩略图 + 名称 + 适用范围
- 右栏：主题编辑器
  - 颜色配置（主色/辅助色/背景色/文字色/边框色）
  - 字体配置（字体族/字号/行高）
  - 间距配置（基础间距/圆角/阴影）
  - 实时预览区

#### 组件清单
| 组件 | 视觉稿有 | 系统有 | 状态 | 备注 |
|---|---|---|---|---|
| 主题列表（卡片） | ✅ | ❌ | 需新建 |  |
| 主题编辑器（颜色/字体/间距） | ✅ | ❌ | 需新建 | 多 Tab |
| 颜色选择器 | ✅ | ❌ | 需新建 | 取色器 + 色板 |
| 实时预览区 | ✅ | ❌ | 需新建 |  |

#### 数据与 API
- 需要的接口：
  - GET /v1/themes（获取主题列表）
  - GET /v1/themes/:id（获取主题详情）
  - POST /v1/themes（新建主题）
  - PUT /v1/themes/:id（更新主题）
  - DELETE /v1/themes/:id（删除主题）
- 需要的表/字段：
  - themes 表（id/name/description/preview/config/is_default/scope）
  - module_themes 表（模块-主题关联）
- 测试数据：至少 3 套主题（浅色/暗色/高对比度）

#### 核心差距（按优先级）
- **P0**：主题列表 + 主题编辑器
- **P1**：实时预览
- **P2**：主题导入/导出

#### 风险与依赖
- 技术风险：中
- 后端依赖：themes 表
- 其他依赖：画布编辑器的样式 Tab 依赖此页面的数据

---

## 8. P0 检查总结

### 8.1 总体数据

| 指标 | 数值 |
|---|---|
| P0 页面总数 | **9 页** |
| 系统完全缺失 | **3 页**（组件注册表、变量管理器、主题与样式） |
| 有不同程度差距 | **6 页** |
| 估算总工作量 | **22-32 人天** |

### 8.2 后端依赖汇总

P0 需要新增的数据库表：

| 表名 | 用途 | 优先级 |
|---|---|---|
| module_widgets | 画布组件实例 | P0 |
| module_events | 事件配置 | P0 |
| module_queries | 查询函数 | P1 |
| module_variables | 变量管理 | P0 |
| module_interfaces | 模块接口定义 | P1 |
| module_deployments | 发布历史 | P2 |
| widget_registry | 组件注册表 | P0 |
| widget_categories | 组件分类 | P1 |
| themes | 主题预设 | P0 |
| module_themes | 模块-主题关联 | P1 |

### 8.3 依赖关系图

```
组件注册表 ←——— 画布编辑器（组件面板）
变量管理器 ←——— 画布编辑器（变量 Tab）
主题与样式 ←——— 画布编辑器（样式 Tab）
事件配置   ←——— 画布编辑器（事件 Tab）
模块接口   ←——— 画布编辑器（数据 Tab）
发布入口   ←——— （独立，无强依赖）
对象探索   ←——— （独立，依赖本体数据）
```

### 8.4 建议实施顺序

1. **第 1 步**：后端建表 + 种子数据（2-3 人天）
2. **第 2 步**：组件注册表 + 变量管理器 + 主题与样式（8-11 人天，3 个全新页面，是画布编辑器的依赖）
3. **第 3 步**：画布编辑器（8-10 人天，最复杂，依赖上面 3 个）
4. **第 4 步**：事件配置 + 模块接口 + 发布入口 + 对象探索（4-8 人天）

---

## 10. P2 深度检查结果（管道 + 数据源 + 运维，共 26 页）

> 检查日期：2026-07-26
> 检查范围：P2 优先级的 26 个页面（管道与数据治理 9 页 + 数据源与同步 8 页 + 运维交付 8 页 + 1 个系统多出）
> 总体结论：P2 共 26 页，其中 3 页系统缺失（DocIntel 管道、文档智能、数据源新建），1 页实际是配置弹窗（builds.html），其余 22 页有不同程度差距

### 10.1 管道与数据治理（9 页 + 1 详情页）

#### 10.1.1 管道构建

**视觉稿文件**：`../foundry/html/pipeline-list.html`（333 行）
**系统路径**：`/data/pipelines`
**当前完整度**：30%
**改造工作量**：4-5 人天
**优先级**：P2

**页面结构**：
- 三栏布局（左图例 180px / 中画布自适应 / 右文件树 280px）
- 顶部 Topbar：面包屑 + 模块名 + 版本标签 + Tab 切换（文件/帮助/页面）+ 动作/保存按钮 + 关闭
- 左栏：图例（颜色分组 + 计数 + 添加颜色）
- 中栏：SVG 画布（节点矩形 + 连线 + 节点可点击跳转 pipeline.html）
- 右栏：Pipeline 文件树（可点击节点列表，含图标区分类型）

**主要组件**：
| 组件 | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 三栏布局 + Topbar | ✅ | ⚠️ | 需改造 |
| SVG 节点图（矩形+连线+跳转） | ✅ | ⚠️ | 需改造 |
| 图例面板（颜色+计数） | ✅ | ❌ | 需新建 |
| 文件树面板（节点列表+图标） | ✅ | ❌ | 需新建 |
| 分支切换按钮组 | ✅ | ❌ | 需新建 |

**数据需求**：
- GET /v1/pipelines（管道列表）
- GET /v1/pipelines/:id/graph（管道图数据：nodes + edges）
- GET /v1/pipelines/:id/files（文件树）
- 测试数据：至少 3 个管道，每个含 10+ 节点

**核心差距**：
- **P0**：SVG 节点图画布 + 文件树联动
- **P1**：图例面板 + 分支切换
- **P2**：节点拖拽编辑（此页面可能只读，编辑在 pipeline.html）

**风险**：中，SVG 图可视化复杂度中等

---

#### 10.1.2 管道提案

**视觉稿文件**：`../foundry/html/pipeline-proposals.html`（211 行，简单页面）
**系统路径**：`/data/pipeline-proposals`
**当前完整度**：10%
**改造工作量**：1-2 人天
**优先级**：P2

**页面结构**：
- 单栏布局
- 顶部 Tab 切换：Edit / Proposals(active) / History
- 过滤行：状态下拉（open/merged/closed）
- 提案卡片列表（每条：图标 + 标题 + 创建时间 + 作者头像）
- 顶部操作按钮：Discard / Save to branch

**主要组件**：
| 组件 | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 三联 Tab（Edit/Proposals/History） | ✅ | ❌ | 需新建 |
| 状态过滤下拉 | ✅ | ❌ | 需新建 |
| 提案卡片列表 | ✅ | ❌ | 需新建 |
| 作者头像组件 | ✅ | ❌ | 需新建 |

**数据需求**：
- GET /v1/pipelines/:id/proposals（提案列表，支持 status 筛选）
- POST /v1/pipelines/:id/proposals/:pid/discard
- POST /v1/pipelines/:id/proposals/:pid/merge
- 测试数据：至少 5 个提案（覆盖各状态）

**核心差距**：
- **P0**：提案列表 + 状态过滤
- **P1**：Discard/Save 操作
- **P2**：提案详情展开

**风险**：低

---

#### 10.1.3 计划编辑器

**视觉稿文件**：`../foundry/html/schedules.html`（570 行，中等复杂度）
**系统路径**：`/data/schedules`
**当前完整度**：30%
**改造工作量**：3-4 人天
**优先级**：P2

**页面结构**：
- 两栏布局（左沿袭图 flex:1 / 右计划详情 420px）
- 左栏：数据沿袭图（顶部工具栏 + SVG 画布，节点可点击高亮）
- 右栏：管理计划详情
  - 返回链接 + 标题 + 关联数据集
  - 最新运行区块（状态徽章 + 时间 + 耗时 + 20 次运行条形图）
  - 最后更新（时间 + 用户）
  - 目标数据集列表
  - 搭建时机（触发器徽章 + Cron 表达式 + 时区 + 下次运行）
  - 搭建范围（项目 + 权限）
  - 操作按钮（Run now / Edit / Pause）
- 顶部 header 按钮：Export / + New schedule

**主要组件**：
| 组件 | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 沿袭图（SVG + 节点高亮） | ✅ | ⚠️ | 需改造 |
| 计划详情面板 | ✅ | ❌ | 需新建 |
| 运行历史条形图（20 条） | ✅ | ❌ | 需新建 |
| Cron 表达式展示 | ✅ | ❌ | 需新建 |
| Run/Edit/Pause 操作 | ✅ | ❌ | 需新建 |

**数据需求**：
- GET /v1/schedules（计划列表）
- GET /v1/schedules/:id（计划详情，含 last_run/run_history/trigger/scope）
- POST /v1/schedules/:id/run
- PUT /v1/schedules/:id
- POST /v1/schedules/:id/pause
- 测试数据：至少 5 个计划，每个含 20 次运行历史

**核心差距**：
- **P0**：两栏联动（图+详情）
- **P0**：计划详情完整字段
- **P1**：运行历史条形图
- **P2**：Export / New schedule

**风险**：中，沿袭图与详情联动

---

#### 10.1.4 搭建（Build Status Check 配置弹窗）

**视觉稿文件**：`../foundry/html/builds.html`（204 行，简单页面）
**系统路径**：`/data/builds`
**当前完整度**：0%
**改造工作量**：1-2 人天
**优先级**：P2

**⚠️ 注意**：视觉稿实际是单个 build status check 的**配置弹窗**，不是搭建历史列表页。如果产品方案需要"搭建历史列表页"，应另外补充视觉稿。

**页面结构**：
- 单栏，居中放置一个配置弹窗卡片
- 弹窗 Header：标题"搭建状态" + 副标题 + 关闭按钮
- 信息提示行：说明检查针对输出数据集
- 规则区块：通过条件 + 编辑严重级别链接
- 复选框：连续失败 N 次后升级 + 添加时间
- 分组区块 + 添加检查分组链接
- 备注区：textarea
- 复选框：失败时自动创建问题
- 底部按钮：取消 / 保存

**主要组件**：
| 组件 | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 配置弹窗 | ✅ | ❌ | 需新建 |
| 规则配置表单 | ✅ | ❌ | 需新建 |
| 阈值输入 + 严重级别 | ✅ | ❌ | 需新建 |
| 自动创建问题开关 | ✅ | ❌ | 需新建 |

**数据需求**：
- GET /v1/builds/:id/checks/:check_id
- PUT /v1/builds/:id/checks/:check_id
- 测试数据：至少 3 个 check 配置

**核心差距**：
- **P0**：配置弹窗 UI
- **P1**：规则配置逻辑
- **P2**：搭建历史列表页（视觉稿缺失，需确认是否补充）

**风险**：低，但需确认是否需要补"搭建历史列表页"

---

#### 10.1.5 数据集预览

**视觉稿文件**：`../foundry/html/dataset.html`（393 行，中等复杂度）
**系统路径**：`/data/datasets`
**当前完整度**：40%
**改造工作量**：3-4 人天
**优先级**：P2

**页面结构**：
- 两栏布局（左主区 / 右信息面板 320px）
- 顶部：数据集 Header（标题 + 徽章 + 路径 + 格式 + 列数 + 分支 + 按钮）
- Tab 栏：预览(active) / 历史 / 详情 / 健康 / 比较
- 预览 Tab：
  - 4 个统计卡（行数/大小/事务/上次更新）
  - 数据表（列头带类型徽章 + 8 行示例 + 工具栏：列搜索/筛选/上传）
  - 右侧信息面板（关于/列统计/计划）
- 历史 Tab：构建表
- 详情 Tab：模式表 + 文件列表 + 同步状态
- 健康 Tab：4 个健康卡
- 比较 Tab：搜索框选择对比数据集

**主要组件**：
| 组件 | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 数据集 Header（多元信息） | ✅ | ⚠️ | 需改造 |
| 5 Tab 切换 | ✅ | ⚠️ | 需改造 |
| 统计卡（4 个） | ✅ | ❌ | 需新建 |
| 数据预览表（带类型徽章） | ✅ | ⚠️ | 需改造 |
| 右侧信息面板（关于/列/计划） | ✅ | ❌ | 需新建 |
| 构建历史表 | ✅ | ❌ | 需新建 |
| 健康检查卡 | ✅ | ❌ | 需新建 |

**数据需求**：
- GET /v1/datasets/:id（元数据 + 统计 + schema + 列统计）
- GET /v1/datasets/:id/preview（前 N 行数据）
- GET /v1/datasets/:id/builds（构建历史）
- GET /v1/datasets/:id/health（健康检查）
- GET /v1/datasets/:id/sync-config（同步配置）
- 测试数据：至少 3 个数据集，每个含完整 schema + 20 行预览数据 + 5 次构建历史

**核心差距**：
- **P0**：5 Tab 切换 + 预览 Tab 完整内容
- **P1**：右侧信息面板（列统计 + 关联计划）
- **P1**：历史/详情/健康 Tab 内容
- **P2**：比较 Tab

**风险**：中，Tab 数量多，内容丰富

---

#### 10.1.6 代码库

**视觉稿文件**：`../foundry/html/code-repositories.html`（386 行，中等复杂度）
**系统路径**：`/data/code-repos`
**当前完整度**：10%
**改造工作量**：3-4 人天
**优先级**：P2

**页面结构**：
- 四栏布局（仓库列表 256px / 文件树 208px / 代码面板自适应 / 元数据面板 224px）
- 第 1 栏：仓库列表（搜索 + 语言筛选 + 5 个仓库按钮）
- 第 2 栏：文件树（6 个文件，带类型图标）
- 第 3 栏：代码面板（顶部 tab：文件名+行数+大小+Blame/History + 代码块）
- 第 4 栏：元数据面板（仓库信息 + 关联资源 + 最近提交 + 待审提案）
- 顶部 Repo Header：仓库名 + 语言徽章 + 分支信息 + 关联管道链接 + 克隆 + 提案链接

**主要组件**：
| 组件 | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 四栏 IDE 式布局 | ✅ | ❌ | 需新建 |
| 仓库列表（搜索+筛选） | ✅ | ❌ | 需新建 |
| 文件树（带图标） | ✅ | ❌ | 需新建 |
| 代码视图（语法高亮） | ✅ | ❌ | 需新建 |
| 元数据面板（关联资源） | ✅ | ❌ | 需新建 |

**数据需求**：
- GET /v1/repos（仓库列表，支持语言筛选）
- GET /v1/repos/:id（仓库详情 + 元数据）
- GET /v1/repos/:id/files（文件树）
- GET /v1/repos/:id/files/:path（文件内容）
- GET /v1/repos/:id/commits（提交历史）
- 测试数据：至少 3 个仓库，每个含 5+ 文件 + 代码内容

**核心差距**：
- **P0**：四栏 IDE 式布局
- **P0**：代码视图（语法高亮）
- **P1**：文件树 + 仓库列表
- **P2**：Blame/History 视图

**风险**：中，代码语法高亮需要引入代码编辑器组件

---

#### 10.1.7 数据沿袭

**视觉稿文件**：`../foundry/html/lineage.html`（389 行，中等复杂度）
**系统路径**：`/data/lineage`
**当前完整度**：20%
**改造工作量**：3-4 人天
**优先级**：P2

**页面结构**：
- 两栏布局（左搜索/属性侧栏 280px / 右主区自适应）
- 左栏：4 个 Tab（搜索/属性/搭建/计划）+ 搜索框 + 最近浏览 + 属性区块
- 右栏：顶部工具栏 + 沿袭图 + 底部节点详情条
- 沿袭图：7 个节点（5 种类型：数据源/数据集/管道/对象类型/漏斗），带展开上下游箭头
- 底部节点详情条：选中节点信息 + "在数据集预览中打开"链接

**主要组件**：
| 组件 | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 全局沿袭图（SVG + DOM 节点） | ✅ | ⚠️ | 需改造 |
| 左侧 4 Tab 侧栏 | ✅ | ❌ | 需新建 |
| 节点展开上下游（箭头按钮） | ✅ | ❌ | 需新建 |
| 底部节点详情条 | ✅ | ❌ | 需新建 |
| 图例（5 种节点类型） | ✅ | ❌ | 需新建 |
| 工具条（平移/选择/展开） | ✅ | ❌ | 需新建 |

**数据需求**：
- GET /v1/lineage/search（全局搜索）
- GET /v1/lineage/graph（沿袭图数据：nodes + edges，支持按节点展开上下游）
- GET /v1/lineage/nodes/:id（节点属性）
- 测试数据：至少 10 个节点，覆盖 5 种类型

**核心差距**：
- **P0**：沿袭图 + 节点展开
- **P0**：底部节点详情条
- **P1**：左侧 4 Tab 侧栏
- **P2**：平移/缩放工具

**风险**：中高，图可视化 + 交互较复杂

---

#### 10.1.8 数据健康

**视觉稿文件**：`../foundry/html/health.html`（746 行，复杂页面）
**系统路径**：`/data/health`
**当前完整度**：20%
**改造工作量**：4-5 人天
**优先级**：P2

**页面结构**：
- 单栏内容区，从上至下
- 顶部：标题 + 描述 + 操作按钮（导出报告 / 添加健康检查）
- Tab 栏：全部检查 / 检查组 / 监测中 / 问题
- 4 个汇总统计卡（通过 24 / 告警 5 / 严重 2 / 打盹中 1）
- 过滤栏（状态/类型/严重性下拉 + 搜索 + 仅监测开关）
- 检查表（15 行，列：数据集/检查类型/状态/严重性/详情/上次评估/打盹按钮）
- 底部双栏：直方图卡 + 未解决问题卡

**主要组件**：
| 组件 | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 4 Tab 切换 | ✅ | ❌ | 需新建 |
| 4 统计卡 | ✅ | ❌ | 需新建 |
| 多维过滤栏 | ✅ | ❌ | 需新建 |
| 检查表（15 行） | ✅ | ❌ | 需新建 |
| 直方图卡（7 天数据） | ✅ | ❌ | 需新建 |
| 未解决问题卡 | ✅ | ❌ | 需新建 |
| 检查组卡片 | ✅ | ❌ | 需新建 |

**数据需求**：
- GET /v1/health/checks（检查列表，支持多维筛选）
- GET /v1/health/stats（统计聚合）
- GET /v1/health/histogram（直方图数据）
- GET /v1/health/issues（问题列表）
- GET /v1/health/groups（检查组列表）
- 测试数据：至少 15 个检查 + 3 个问题 + 4 个检查组

**核心差距**：
- **P0**：检查表 + 4 统计卡
- **P0**：4 Tab 切换
- **P1**：直方图 + 问题卡
- **P2**：检查组 + 监测订阅

**风险**：中，数据量大，过滤维度多

---

#### 10.1.9 DocIntel 管道（LLM 文档智能配置）

**视觉稿文件**：`../foundry/html/pipeline-doc-intel.html`（397 行，中等复杂度）
**系统路径**：缺失（需新建）
**当前完整度**：0%
**改造工作量**：3-4 人天
**优先级**：P2

**页面结构**：
- 两栏布局（左迷你画布 / 右配置面板）
- 左栏：迷你 Pipeline 图（输入→Use LLM→输出，3 个节点 + 箭头连接）
- 右栏：LLM 配置面板（header + 5 Tab + body + footer）
- 5 Tab：Configure(active) / Preview / Trial run / Input table / Output table
- Configure Tab：
  - 模板选择网格（6 张卡片：分类/总结/翻译/情感/实体提取/空模板）
  - 配置字段（Multiplicity + Context + Categories 标签输入 + Column 选择）
  - 可折叠区块（Optional configuration / Advanced Model configuration / Entities to extract）
- Footer：Cancel / Create prompt / Apply

**主要组件**：
| 组件 | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 迷你 Pipeline 图 | ✅ | ❌ | 需新建 |
| 5 Tab 配置面板 | ✅ | ❌ | 需新建 |
| 模板选择卡片网格（6 种） | ✅ | ❌ | 需新建 |
| 标签输入组件 | ✅ | ❌ | 需新建 |
| 可折叠配置区块 | ✅ | ❌ | 需新建 |
| 输出预览表 | ✅ | ❌ | 需新建 |

**数据需求**：
- GET /v1/pipelines/:id/nodes/:node_id/config（LLM 节点配置）
- PUT /v1/pipelines/:id/nodes/:node_id/config
- GET /v1/models（可用模型列表）
- POST /v1/pipelines/:id/nodes/:node_id/trial-run（试运行）
- 测试数据：至少 1 个 LLM 节点的完整配置

**核心差距**：
- **P0**：模板选择 + 配置表单
- **P1**：迷你画布 + 5 Tab
- **P2**：Trial run 试运行

**风险**：中，配置项多且动态

---

#### 10.1.10 管道详情（Pipeline Builder 编辑器）

**视觉稿文件**：`../foundry/html/pipeline.html`（422 行，复杂页面）
**系统路径**：`/data/pipelines/:id`（详情页，不在侧栏）
**当前完整度**：30%
**改造工作量**：5-6 人天
**优先级**：P2

**页面结构**：
- 两栏布局（左画布区自适应 / 右输出侧栏 320px）
- 顶部全宽工具栏：撤销/重做 + 分支切换 + 已保存 + 提议 + 部署 + 视图切换（编辑/提案/历史）+ 徽章 + 搭建设置 + 分享
- 左画布区：
  - 画布工具栏（10 个变换按钮：Filter/Join/Aggregate/Explode/Cast/Union/Sort/Distinct/Expression/Window + 添加数据集 + 参数）
  - SVG 画布（4 个节点 + 连线，节点可选中）
  - 缩放控制（缩小/100%/放大/适应）
  - 图例（3 种节点颜色）
  - 底部预览面板（选中节点的数据表 + 相关链接）
- 右输出侧栏：
  - 数据集输出（APPEND 模式 + 列数变化 + 状态）
  - Object 类型输出（Write Mode + 部署状态）
  - 链接类型输出（1:N + predicate + 部署状态）
  - 详细信息（描述 + 浏览次数 + 协作者）

**主要组件**：
| 组件 | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 两栏布局 + 工具栏 | ✅ | ⚠️ | 需改造 |
| 10 个变换按钮 | ✅ | ❌ | 需新建 |
| SVG 画布（节点+连线+选中） | ✅ | ⚠️ | 需改造 |
| 缩放控制 | ✅ | ❌ | 需新建 |
| 底部预览面板（数据表） | ✅ | ❌ | 需新建 |
| 右侧输出侧栏（3 类输出） | ✅ | ❌ | 需新建 |
| 视图切换（编辑/提案/历史） | ✅ | ❌ | 需新建 |

**数据需求**：
- GET /v1/pipelines/:id（管道元数据 + 节点图 + 输出配置）
- GET /v1/pipelines/:id/nodes/:node_id/preview（节点预览数据）
- PUT /v1/pipelines/:id（保存管道配置）
- GET /v1/pipelines/:id/proposals（提案列表）
- GET /v1/pipelines/:id/history（历史记录）
- 测试数据：至少 1 个完整管道（含 5+ 节点 + 3 类输出）

**核心差距**：
- **P0**：SVG 画布 + 变换工具栏
- **P0**：底部预览面板
- **P0**：右侧输出侧栏
- **P1**：视图切换（提案/历史）
- **P2**：搭建设置 + 分享

**风险**：高，画布编辑器复杂度仅次于工作台的 workshop-canvas

---

### 10.2 数据源与同步（8 页 + 1 详情页）

#### 10.2.1 数据链接器

**视觉稿文件**：`../foundry/html/data-connection.html`
**系统路径**：`/data`
**当前完整度**：40%
**改造工作量**：2-3 人天
**优先级**：P2

**页面结构**：
- 两栏布局（左分组导航 / 右主内容区）
- 左栏：连接器类型分组导航（Sources / Protocol sources / 管理）
- 右栏：
  - "Sources" 分组（搜索框 + 连接器卡片网格）
  - "Protocol sources" 分组（搜索框 + 协议源卡片网格）
- 连接器卡片：图标 + 名称 + 能力标签（Batch syncs / Streaming syncs / Virtual tables / Use in code）

**主要组件**：分组导航 + 搜索 + 卡片网格 + 能力标签

**数据需求**：
- GET /v1/connectors（连接器列表，含 type/name/icon/capabilities）
- GET /v1/protocol-sources（协议源列表）
- 测试数据：至少 15 个连接器 + 5 个协议源

**核心差距**：**P0** 连接器卡片网格 + 能力标签；**P1** 分组导航；**P2** 搜索

**风险**：低

---

#### 10.2.2 边缘代理

**视觉稿文件**：`../foundry/html/data-connection-agents.html`
**系统路径**：`/data/agents`
**当前完整度**：20%
**改造工作量**：3-4 人天
**优先级**：P2

**页面结构**：
- 两栏布局（左代理列表 320px / 右详情区自适应）
- 左栏：搜索框 + 代理卡片列表（名称 + 状态徽章 + IP/版本 + 资源摘要）
- 右栏：
  - 顶部：代理标题 + 状态徽章 + 操作按钮（重启/编辑/日志）
  - 指标卡片区（3 列网格：内存/CPU/磁盘 + sparkline 迷你折线图）
  - Tab 切换（Sources / Health / Configuration）

**主要组件**：代理列表 + 指标卡（含 sparkline）+ 3 Tab 面板

**数据需求**：
- GET /v1/agents（代理列表）
- GET /v1/agents/:id/metrics（实时指标 + 时序数据）
- GET /v1/agents/:id/sources（关联数据源）
- GET /v1/agents/:id/health（健康检查）
- GET /v1/agents/:id/config（配置详情）
- 测试数据：至少 3 个代理 + 时序指标数据

**核心差距**：**P0** 两栏联动 + 指标卡；**P1** 3 Tab 面板；**P2** sparkline 图表

**风险**：中，实时指标 + sparkline

---

#### 10.2.3 同步配置

**视觉稿文件**：`../foundry/html/sync.html`
**系统路径**：`/data/sync-config`
**当前完整度**：30%
**改造工作量**：3-4 人天
**优先级**：P2

**页面结构**：
- 多 Tab 单栏布局
- 顶部：同步任务名称 + 状态徽章 + 保存/运行按钮
- Tab 栏：配置 / 调度 / 历史 / 高级
- 配置 Tab：源选择器 + 目标选择器 + 字段映射表
- 调度 Tab：调度策略（手动/定时/流式）+ Cron 表达式
- 历史 Tab：运行历史列表
- 高级 Tab：增量列 + 错误处理 + 重试策略

**主要组件**：4 Tab 切换 + 源/目标选择器 + 字段映射表 + 调度策略 + 历史列表

**数据需求**：
- GET /v1/syncs/:id（同步任务详情）
- GET /v1/syncs/:id/runs（运行历史）
- PUT /v1/syncs/:id
- POST /v1/syncs/:id/run
- 测试数据：至少 3 个同步任务 + 5 次运行历史

**核心差距**：**P0** 4 Tab + 字段映射；**P1** 调度策略；**P2** 高级配置

**风险**：中

---

#### 10.2.4 同步路由

**视觉稿文件**：`../foundry/html/sync-routing.html`
**系统路径**：`/data/sync-routes`
**当前完整度**：20%
**改造工作量**：2-3 人天
**优先级**：P2

**页面结构**：
- 单栏，分区布局
- 顶部：数据源标题 + 类型徽章 + 状态
- "可用能力" 区：能力卡片网格（Batch syncs / Streaming syncs / Virtual tables / Use in code）
- "现有同步" 区：同步任务列表（名称 + 源→目标 + 状态 + 最近运行 + 操作）
- "文档资源" 区：文档卡片网格（缩略图 + 标题 + 元信息 + 状态徽章）

**主要组件**：数据源头部 + 能力卡片 + 同步任务列表 + 文档卡片

**数据需求**：
- GET /v1/sources/:id（数据源详情）
- GET /v1/sources/:id/capabilities（可用能力）
- GET /v1/sources/:id/syncs（已配置同步）
- GET /v1/sources/:id/documents（关联文档）
- 测试数据：至少 1 个数据源 + 4 种能力 + 3 个同步任务 + 5 个文档

**核心差距**：**P0** 能力卡片 + 同步列表；**P1** 文档卡片；**P2** 搜索

**风险**：低

---

#### 10.2.5 媒体集

**视觉稿文件**：`../foundry/html/media-sets.html`
**系统路径**：`/data/media-sets`
**当前完整度**：10%
**改造工作量**：2-3 人天
**优先级**：P2

**页面结构**：
- 3 Tab 单栏布局（浏览 / 同步 / 变换）
- 浏览 Tab：媒体文件网格（缩略图卡片）
- 同步 Tab：同步配置表单
- 变换 Tab：可用变换卡片网格（2 列，含变换名称 + 描述 + 计费信息 + "在 Pipeline 中使用"跳转）

**主要组件**：3 Tab + 媒体文件网格 + 同步表单 + 变换卡片

**数据需求**：
- GET /v1/media-sets/:id（媒体集详情）
- GET /v1/media-sets/:id/files（文件列表）
- GET /v1/media-sets/:id/transformations（可用变换）
- 测试数据：至少 1 个媒体集 + 10 个文件 + 3 个变换

**核心差距**：**P0** 3 Tab + 文件网格；**P1** 变换卡片；**P2** 同步配置

**风险**：低

---

#### 10.2.6 文档智能（缺失页）

**视觉稿文件**：`../foundry/html/document-intelligence.html`
**系统路径**：缺失（需新建，路由 `/aip/doc-intelligence`）
**当前完整度**：0%
**改造工作量**：3-4 人天
**优先级**：P2

**页面结构**：
- 两栏布局（左文档卡片网格 / 右提取字段面板）
- 顶部 Header：面包屑 + 搜索框 + 操作按钮（导入文档 / 新建提取模板）
- 左栏：文档卡片网格（auto-fill minmax 240px）
  - 每张卡片：缩略图区（180px 高，PDF/图片图标）+ 信息区（标题 + 大小 + 状态徽章）
  - 状态四态：已提取（绿）/ 处理中（黄）/ 失败（红）/ 待处理（灰）
- 右栏：选中文档的提取字段列表
  - 每行：字段名 + 类型标签（日期/文本/数字）+ 提取值

**主要组件**：文档卡片网格 + 4 态状态徽章 + 提取字段面板 + 导入/模板操作

**数据需求**：
- GET /v1/documents（文档列表，含 status/size/title）
- GET /v1/documents/:id/extracted-fields（提取字段）
- POST /v1/documents/import
- GET /v1/extraction-templates
- 测试数据：至少 10 个文档（覆盖 4 种状态）+ 每个含 5+ 提取字段

**核心差距**：**P0** 文档卡片网格 + 提取字段面板；**P1** 导入/模板；**P2** 重新提取

**风险**：中，OCR + LLM 提取涉及后端复杂逻辑

---

#### 10.2.7 数据源新建（缺失页）

**视觉稿文件**：`../foundry/html/source-new.html`
**系统路径**：缺失（需新建）
**当前完整度**：0%
**改造工作量**：2-3 人天
**优先级**：P2

**页面结构**：
- 单栏 4 步向导布局
- 顶部工具栏（48px 高）：标题
- 步骤指示器（4 步圆形节点 + 连接线，居中 max-width 700px）：
  - is-done（绿色 ✓）/ is-current（蓝色数字）/ is-pending（灰色数字）三态
- 卡片内容区（max-width 800px 居中）：
  - 步骤 1：连接器网格（4 列，单选高亮）
  - 步骤 2：连接方式网格（2 列：Agent 方式 / Direct 直连）
  - 步骤 3：表单（数据源名称 + 所属项目选择器）
  - 步骤 4：配置表单（主机/端口/数据库/用户名/密码，双列布局）
- 底部页脚（56px 高）：信息提示 + 上一步/下一步按钮

**主要组件**：4 步步骤指示器 + 连接器网格 + 连接方式选择 + 表单 + 双列配置

**数据需求**：
- GET /v1/connectors（连接器列表）
- GET /v1/projects（项目列表）
- POST /v1/sources（创建）
- POST /v1/sources/test-connection（连接测试）
- 测试数据：连接器列表 + 项目列表

**核心差距**：**P0** 4 步向导 + 步骤指示器；**P1** 连接测试；**P2** 表单校验

**风险**：低，向导式表单较标准

---

#### 10.2.8 数据源详情（数据库浏览器）

**视觉稿文件**：`../foundry/html/source-detail.html`
**系统路径**：缺失（详情页，不在侧栏）
**当前完整度**：0%
**改造工作量**：4-5 人天
**优先级**：P2

**页面结构**：
- 三栏布局（左 Schema 树 260px / 中关系图+预览 / 右已选表清单 280px）
- 顶部工具栏（44px 高）：标题 + 状态徽章"已连接" + 操作按钮
- 左栏：Schema 树
  - 搜索框 + Schema 分组（可折叠）+ 表项（可展开列）+ FK 列紫色高亮
- 中栏：
  - 上半：表关系图（SVG，表节点 + FK 连线）
  - 下半（240px 高）：数据预览表（粘性表头 + FK 列紫色）
- 右栏：已选表清单
  - 头部（标题 + 关闭）+ 列表（表名 + 元信息 + 移除按钮）+ 底部操作按钮

**主要组件**：Schema 树 + 表关系图（SVG）+ 数据预览表 + 已选表清单

**数据需求**：
- GET /v1/sources/:id/schemas（Schema 列表）
- GET /v1/sources/:id/schemas/:schema/tables（表清单）
- GET /v1/sources/:id/tables/:table/columns（列定义，含 PK/FK）
- GET /v1/sources/:id/tables/:table/foreign-keys（外键关系）
- GET /v1/sources/:id/tables/:table/preview（数据预览）
- 测试数据：至少 2 个 Schema + 10 个表 + 外键关系 + 预览数据

**核心差距**：**P0** 三栏布局 + Schema 树；**P0** 表关系图 SVG；**P1** 数据预览；**P2** 已选表清单

**风险**：中高，表关系图可视化较复杂

---

### 10.3 运维交付（8 页 + 2 个系统多出）

#### 10.3.1 Hub 舰队

**视觉稿文件**：`../foundry/html/apollo-hub.html`
**系统路径**：`/apollo`
**当前完整度**：30%
**改造工作量**：2-3 人天
**优先级**：P2

**页面结构**：
- 单栏布局（max-w-6xl）
- 顶部标题 + 副标题
- 状态条 Banner（绿色，展示 Hub 区域 + 在线 Spoke 数 + 最近 Probe 时间 + Release 通道链接）
- Spoke 卡片网格（响应式 3 列，5 个真实 + 1 个"+"占位）
- 每张 Spoke 卡片：名称 + 健康状态徽章 + Probe 状态 + 通道版本 + Bundle 版本 + Spoke 形态

**主要组件**：状态条 Banner + Spoke 卡片网格 + 占位卡片

**数据需求**：
- GET /v1/hub（Hub 元数据）
- GET /v1/spokes（Spoke 列表，含 health/probe/channel/bundle/spokeType）
- 测试数据：至少 5 个 Spoke（覆盖各健康状态）

**核心差距**：**P0** Spoke 卡片网格 + 状态条；**P1** Probe 轮询数据；**P2** 注册新 Spoke

**风险**：低

---

#### 10.3.2 Release 通道

**视觉稿文件**：`../foundry/html/apollo-release.html`
**系统路径**：`/apollo/release`
**当前完整度**：20%
**改造工作量**：2-3 人天
**优先级**：P2

**页面结构**：
- 单栏布局（max-w-4xl）
- Pipeline 三段卡片（rc → beta(当前) → stable，SVG 箭头连接）
- Hotfix 紧急发布卡片（红色区分，含补丁包版本 + CVE 描述 + 推送按钮）
- Recall 回滚卡片（当前版本 → 回滚目标 + 执行按钮）
- 底部三向导航（Hub / Ferry / Assets）

**主要组件**：三段 Pipeline 卡片 + Hotfix 通道 + Recall 回滚 + 底部导航

**数据需求**：
- GET /v1/releases（rc/beta/stable 三段状态）
- GET /v1/releases/hotfix（Hotfix 信息）
- GET /v1/releases/recall（回滚历史）
- POST /v1/releases/hotfix/push
- POST /v1/releases/recall/execute
- 测试数据：3 段版本 + 1 个 Hotfix + 1 个回滚记录

**核心差距**：**P0** 三段 Pipeline + Hotfix；**P1** Recall 回滚；**P2** 审批跳转

**风险**：低

---

#### 10.3.3 Spoke 详情

**视觉稿文件**：`../foundry/html/apollo-spoke.html`
**系统路径**：`/apollo/spoke`
**当前完整度**：20%
**改造工作量**：2-3 人天
**优先级**：P2

**页面结构**：
- 单栏布局（max-w-4xl）
- 标题区（动态名称 + 区域 + 通道）
- 出站轮询 Callout（蓝色提示条，含轮询间隔 + 最近同步时间）
- Spoke 形态切换 Tab（Full / Lite）
- 形态对比双卡片（Full：完整运行时/双向同步 vs Lite：轻量代理/仅出站）
- 部署计划清单（3 行：Bundle/FDE/Config Override）
- 操作按钮（预览 Plan Diff / 配置覆盖）
- 返回 Hub 链接

**主要组件**：Callout + Full/Lite Tab + 对比卡片 + 部署计划清单

**数据需求**：
- GET /v1/spokes/:id（Spoke 详情 + outboundPolling）
- GET /v1/spokes/:id/plan（部署计划）
- GET /v1/spokes/:id/plan-diff（Plan Diff 预览）
- 测试数据：至少 1 个 Spoke 的完整数据 + 3 个部署计划项

**核心差距**：**P0** Full/Lite 切换 + 部署计划；**P1** Plan Diff 预览；**P2** 配置跳转

**风险**：低

---

#### 10.3.4 Ferry 摆渡

**视觉稿文件**：`../foundry/html/apollo-ferry.html`
**系统路径**：`/apollo/ferry`
**当前完整度**：10%
**改造工作量**：2-3 人天
**优先级**：P2

**页面结构**：
- 单栏布局（max-w-3xl，最窄）
- 4 步骤指示器（选择 Bundle → 校验签名 → 导出介质 → 目标 Spoke 导入）
- 当前步骤内容卡片（步骤 1：Bundle 选择，2 个 radio 选项）
- 气隙传输说明提示框
- 底部跳转链接

**主要组件**：4 步步骤指示器 + Bundle 选择 radio + 气隙说明

**数据需求**：
- GET /v1/ferry/bundles（可 Ferry 的 Bundle 列表）
- POST /v1/ferry/submit
- 测试数据：至少 2 个可 Ferry 的 Bundle

**核心差距**：**P0** 4 步向导 + Bundle 选择；**P1** 步骤 2-4 实现；**P2** 签名校验

**风险**：低，但视觉稿只有步骤 1 的 UI，步骤 2-4 需补设计

---

#### 10.3.5 FDE 资产包

**视觉稿文件**：`../foundry/html/apollo-assets.html`
**系统路径**：`/apollo/assets`
**当前完整度**：20%
**改造工作量**：1-2 人天
**优先级**：P2

**页面结构**：
- 单栏布局（max-w-5xl）
- 资产包表格（5 列：资产包名 / SemVer / 绑定通道 / 内容 / 状态）
- 4 行示例数据（apollo-core / fde-维修派单 / fde-库存预警 / config-overrides-sh）
- 通道徽章颜色编码（stable 绿 / beta 黄 / rc 灰）
- 底部双链接（发布通道 / Ferry 导出）

**主要组件**：资产包表格 + 通道徽章 + 底部导航

**数据需求**：
- GET /v1/assets（资产包列表，含 name/semver/channel/contentTypes/status/boundSpoke）
- 测试数据：至少 4 个资产包（覆盖各通道和状态）

**核心差距**：**P0** 资产包表格 + 徽章；**P1** 通道筛选；**P2** 行点击详情

**风险**：低

---

#### 10.3.6 变更审批

**视觉稿文件**：`../foundry/html/apollo-change-mgmt.html`
**系统路径**：`/apollo/change`
**当前完整度**：10%
**改造工作量**：2-3 人天
**优先级**：P2

**页面结构**：
- 双栏布局（左变更审批列表 288px / 右详情区自适应）
- 左栏：3 个变更单按钮（CHG-2026-0412 高亮 / CHG-2026-0408 / CHG-2026-0395）
- 右栏：
  - 标题 + 元信息（变更类型 + 申请人）
  - 详情卡片（4 行 key-value：变更类型/目标 Spoke/Bundle 版本/计划窗口）
  - 审批流卡片（3 步流水：提交 → 安全评审 → 变更委员会）
  - 操作按钮组（批准 / 驳回 / 关联发布通道）

**主要组件**：双栏布局 + 变更单列表 + 审批流卡片 + 操作按钮

**数据需求**：
- GET /v1/changes（变更单列表）
- GET /v1/changes/:id（变更单详情 + 审批流）
- POST /v1/changes/:id/approve
- POST /v1/changes/:id/reject
- 测试数据：至少 3 个变更单（覆盖各状态）+ 审批流步骤

**核心差距**：**P0** 双栏联动 + 审批流；**P1** 批准/驳回操作；**P2** 关联发布通道

**风险**：低

---

#### 10.3.7 配置与密钥

**视觉稿文件**：`../foundry/html/apollo-config.html`
**系统路径**：`/apollo/config`
**当前完整度**：10%
**改造工作量**：2 人天
**优先级**：P2

**页面结构**：
- 单栏布局（max-w-3xl）
- 维护窗口卡片（amber 主题，2 列：开始时间 + 结束时间，readonly）
- 覆盖项列表（3 行：aip.model.default / db.connection.poolSize / integration.apiKey）
- 安全提示蓝色 Callout（禁止明文密钥，强制 Vault/KMS 引用）
- 操作按钮（保存覆盖 / ← Spoke 详情 / FDE 资产包 →）

**主要组件**：维护窗口卡 + 覆盖项列表 + 安全 Callout + 操作按钮

**数据需求**：
- GET /v1/spokes/:id/config（配置覆盖项）
- PUT /v1/spokes/:id/config
- GET /v1/spokes/:id/maintenance-window
- 测试数据：至少 3 个覆盖项 + 1 个维护窗口

**核心差距**：**P0** 覆盖项列表 + 维护窗口；**P1** 编辑模式；**P2** Vault/KMS 校验

**风险**：低

---

#### 10.3.8 接入案例

**视觉稿文件**：`../foundry/html/integration-cases.html`（535 行，最大页面）
**系统路径**：`/apollo/cases`
**当前完整度**：10%
**改造工作量**：4-5 人天
**优先级**：P2

**页面结构**：
- 单栏布局（`p-ic` 命名空间样式，与其他 apollo-* 页面不同）
- 顶部 Header（标题 + 副标题 + 导出清单 / + 新建案例 按钮）
- 统计条（6 个统计卡：平台数 9 / 连接器 9 / 同步 47 / 本体对象 38 / OKF 映射 9 / 应用消费 12）
- 端到端链路总览（6 节点流水线：数据接入→同步→管道清洗→OKF 映射→本体实例化→应用消费）
- 平台案例列表区：
  - 筛选条（状态 + 地区下拉）
  - 9 个案例卡片（微商城/淘宝/拼多多/京东/抖音/Shopify/跨境Shopify/Amazon/天猫）
  - 每个卡片：图标 + 名称 + 标签 + 子标题 + 状态 + 6 步 mini flow + 5 个指标 + 查看链路
- G1-G10 公共阻塞项网格（10 个 blocker 卡片）

**主要组件**：6 统计卡 + 链路流水线 + 9 案例卡片 + 筛选 + 10 阻塞项

**数据需求**：
- GET /v1/integration-cases/stats（6 个统计聚合）
- GET /v1/integration-cases（案例列表，含 tag/connector/steps/metrics/status）
- GET /v1/integration-cases/blockers（G1-G10 阻塞项）
- 测试数据：9 个平台案例 + 10 个阻塞项

**核心差距**：**P0** 案例卡片 + 统计条；**P0** 端到端链路；**P1** 阻塞项网格；**P2** 筛选 + 导出

**风险**：中，页面内容量大，案例卡片信息密度高

**⚠️ 注意**：此页面使用独立的 `p-ic-*` 样式前缀，与其他 apollo-* 页面的 Tailwind 风格不一致，迁移时需统一

---

#### 10.3.9-10.3.10 系统多出页面（3 个）

| # | 页面 | 系统路径 | 处理建议 |
|---|---|---|---|
| 9 | 本机探活 | `/settings/local-platform` | 开发辅助页，保留不动 |
| 10 | 启停说明 | `/settings/ops-start-guide` | 开发辅助页，保留不动 |
| 10a | SaaS 开通 | `/apollo/provisioning` | 系统多出，保留不动 |

---

### 10.4 P2 检查总结

#### 总体数据

| 指标 | 数值 |
|---|---|
| P2 页面总数 | **26 页**（含 1 个详情页 + 1 个系统多出共 3 个） |
| 系统完全缺失 | **3 页**（DocIntel 管道、文档智能、数据源新建） |
| 有不同程度差距 | **23 页** |
| 估算总工作量 | **65-85 人天** |

#### 各分区工作量分布

| 分区 | 页面数 | 估算工作量 | 复杂度 |
|---|---|---|---|
| 管道与数据治理 | 10 页 | 28-36 人天 | 中-高（含 2 个画布编辑器） |
| 数据源与同步 | 8 页 | 21-29 人天 | 中（含 1 个三栏 DB 浏览器） |
| 运维交付 | 8 页 | 17-22 人天 | 低-中（大多为简单卡片/表格） |

#### 后端依赖汇总

P2 需要新增/扩展的数据库表：

| 表名 | 用途 | 所属分区 |
|---|---|---|
| pipelines | 管道元数据 | 管道 |
| pipeline_nodes | 管道节点图 | 管道 |
| pipeline_proposals | 管道提案 | 管道 |
| schedules | 计划调度 | 管道 |
| schedule_runs | 计划运行历史 | 管道 |
| datasets | 数据集元数据 | 管道 |
| dataset_columns | 数据集列统计 | 管道 |
| dataset_builds | 数据集构建历史 | 管道 |
| code_repositories | 代码库 | 管道 |
| code_files | 代码文件 | 管道 |
| lineage_graph | 沿袭图数据 | 管道 |
| health_checks | 健康检查 | 管道 |
| health_issues | 健康问题 | 管道 |
| health_groups | 检查组 | 管道 |
| llm_node_configs | LLM 节点配置 | 管道 |
| connectors | 连接器 | 数据源 |
| protocol_sources | 协议源 | 数据源 |
| agents | 边缘代理 | 数据源 |
| agent_metrics | 代理指标时序 | 数据源 |
| syncs | 同步任务 | 数据源 |
| sync_runs | 同步运行历史 | 数据源 |
| media_sets | 媒体集 | 数据源 |
| media_files | 媒体文件 | 数据源 |
| documents | 文档 | 数据源 |
| extracted_fields | 提取字段 | 数据源 |
| extraction_templates | 提取模板 | 数据源 |
| sources | 数据源 | 数据源 |
| source_tables | 数据源表 | 数据源 |
| source_columns | 数据源列 | 数据源 |
| hub | Hub 元数据 | 运维 |
| spokes | Spoke 列表 | 运维 |
| releases | Release 通道 | 运维 |
| asset_bundles | 资产包 | 运维 |
| change_orders | 变更单 | 运维 |
| config_overrides | 配置覆盖 | 运维 |
| integration_cases | 接入案例 | 运维 |
| integration_blockers | 阻塞项 | 运维 |

#### 关键风险点

1. **管道详情（pipeline.html）**：两栏画布编辑器，复杂度仅次于工作台的 workshop-canvas，工作量 5-6 人天
2. **数据沿袭（lineage.html）**：全局图可视化 + 节点展开交互，复杂度中高
3. **数据源详情（source-detail.html）**：三栏 DB 浏览器 + 表关系图 SVG，复杂度中高
4. **接入案例（integration-cases.html）**：页面最大（535 行），信息密度高，且样式独立
5. **Ferry 摆渡**：视觉稿只有步骤 1 的 UI，步骤 2-4 需补设计
6. **搭建（builds.html）**：视觉稿是配置弹窗，不是列表页，需确认是否补充列表页视觉稿

#### 依赖关系

```
数据链接器 → 数据源新建 → 数据源详情 → 同步路由 → 同步配置
                                                ↓
管道构建 → 管道详情 → 数据集预览 → 数据沿袭
                ↓                       ↓
            代码库 ←──── 数据健康 ←── 计划编辑器
                ↓
            DocIntel 管道

Hub 舰队 → Spoke 详情 → 配置与密钥
    ↓         ↓
Release 通道 → 变更审批
    ↓
Ferry 摆渡 → FDE 资产包

接入案例（独立，聚合展示各分区数据）
```

#### 建议实施顺序

1. **第 1 步**：运维交付 8 页（17-22 人天，大多简单，可快速出成果）
2. **第 2 步**：数据源与同步 8 页（21-29 人天，含 3 个缺失页）
3. **第 3 步**：管道与数据治理 10 页（28-36 人天，含 2 个复杂画布编辑器）

---

## 11. 配套文档

- 开发计划：`palantier/20_tech/223-plan.md`
- 全量页面差距盘点：`palantier/20_tech/223-full-ui-gap-analysis.md`
- 菜单对齐全表：`palantier/20_tech/223-menu-alignment-full.md`
- 工作台深度方案：`palantier/20_tech/223-ui-alignment-plan.md`
- 种子数据整合方案：`palantier/20_tech/223-seed-data-consolidation-plan.md`
