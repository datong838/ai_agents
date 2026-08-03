# 224 · 全站样式规整实施方案

> **版本**：v1.1 · 2026-07-27（修正 DocIntel 路由状态描述 + 交叉引用错误）
> **原则**：业务流程逻辑优先 → 产品设计意图落地 → 样式风格规整
> **核心军规**：不能因为视觉而去掉功能；页面样式风格必须规整，以视觉效果为蓝图修改维护
> **参考文档**：220整体技术方案、221 AIP分阶段计划、222产品补充说明、223全站UI对齐计划、T-UI前端工程规范

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后代码 | 本文档只定义样式规整方案，不直接改业务代码 |
| 业务优先 | 样式规整以不影响功能为前提，功能完整性第一位 |
| 最小更改 | 优先调整CSS/组件样式，不改业务逻辑和数据结构 |
| 中文交付 | 全文中文 |
| 视觉稿为蓝图 | 样式规整以 foundry/html 视觉稿为对齐基准 |

---

## 0. 方案总览

### 0.1 核心理念：三层优先级

```
┌─────────────────────────────────────────────────────┐
│  第一层：业务流程逻辑（不可动）                        │
│  • 数据模型、API契约、核心功能、业务流转                │
│  • 任何样式调整不得破坏此层                            │
├─────────────────────────────────────────────────────┤
│  第二层：产品设计意图（可优化）                        │
│  • 信息架构、交互模式、用户操作路径                     │
│  • 样式调整需服务于更好的产品体验，而非为了改而改         │
├─────────────────────────────────────────────────────┤
│  第三层：样式风格规整（重点工作）                      │
│  • 颜色、字体、间距、圆角、阴影、图标等视觉元素          │
│  • 组件样式统一、布局结构对齐、视觉层级清晰              │
│  • 以视觉稿为蓝图，确保全系统风格一致                    │
└─────────────────────────────────────────────────────┘
```

### 0.2 样式规整范围

| 层级 | 内容 | 是否规整 | 说明 |
| --- | --- | --- | --- |
| **全局设计Token** | 颜色、字体、间距、圆角、阴影 | ✅ 是 | 统一全站视觉语言 |
| **公共组件样式** | 按钮、卡片、表格、表单、Tab、Badge | ✅ 是 | 确保组件表现一致 |
| **页面布局结构** | 顶栏、侧栏、面包屑、内容区布局 | ✅ 是 | 对齐视觉稿信息架构 |
| **交互反馈样式** | hover、active、loading、error状态 | ✅ 是 | 提升用户体验 |
| **业务功能逻辑** | API、数据模型、核心算法 | ❌ 否 | 功能完整性优先，不动 |
| **产品信息架构** | 页面结构、导航路径、操作流程 | ⚠️ 谨慎 | 仅在产品设计有明确依据时调整 |

---

## 1. 业务流程逻辑梳理（样式规整的前提）

### 1.1 工作台（Workshop）业务流

#### 核心业务链路

```
应用列表（workshop.html）
    │
    ├──→ 创建应用向导（4步：基本信息→数据绑定→模板选择→确认）
    │
    ├──→ 运行态应用（订单管理/风险告警/态势大屏/Buddy）
    │       │
    │       └──→ 进入画布编辑器（编辑态）
    │
    └──→ 应用程序构建工具（7个工具页）
            │
            ├── 画布编辑器（workshop-canvas.html）
            │       ├── Widget模式：UI组件拖拽编辑
            │       ├── Workflow模式：事件流编排
            │       └── 9个功能Tab（Dashboard/Queries/Functions/Objects/Events/Data/Dependencies/Styles/Variables）
            │
            ├── 组件注册表（workshop-widget-registry.html）
            │       └── 3种来源：平台内置 / 市场安装 / 代码开发
            │
            ├── 变量管理器（workshop-variables.html）
            ├── 主题与样式（workshop-styles.html）
            ├── 模块接口（workshop-module-interface.html）
            ├── 事件配置（workshop-events.html）
            └── 发布入口（workshop-publish.html）
```

#### 业务逻辑要点（样式规整时不可破坏）

1. **Module 是核心载体**：所有应用都是 Module，可在线定制，不是写代码写死的
2. **Widget 插件化**：组件通过注册表管理，新增 Widget 不改 Runtime 核心
3. **变量驱动**：页面状态通过 Variables 管理，支持 Object Set / Selection / Active / Scalar / Function 结果
4. **事件驱动**：Widget 事件触发动作，支持幂等性保证
5. **运行态 vs 编辑态**：订单管理等页面有两种形态——运行态（用户使用）和编辑态（开发者配置）

---

### 1.2 AIP 决策引擎业务流

#### 核心业务链路

```
AIP 决策引擎
    │
    ├──→ 应用层
    │       ├── AIP助手（aip-assist.html）- 聊天式AI助手
    │       ├── 对话机器人（agents.html）- Chatbot Studio
    │       └── AIP分析师（aip-analyst.html）- 深度分析界面
    │
    ├──→ 构建工具
    │       ├── AIP逻辑画布（aip-logic.html）- Logic图编排
    │       ├── Agent工具面板（aip-tools.html）- 工具配置
    │       └── 成熟度楼梯（aip-maturity.html）- L2/L3/L4分级
    │
    ├──→ 目录与插件
    │       ├── 智能体目录（agent-registry.html）- Agent市场
    │       └── 智能体插件（aip-capabilities.html）- 能力接入
    │
    ├──→ 治理与安全
    │       ├── Evals门控（aip-evals.html）- 评测集与门控
    │       ├── Draft审批台（aip-draft-inbox.html）- 人在回路
    │       ├── 决策谱系（aip-decision-lineage.html）- 可追溯
    │       └── 可观测性（aip-observability.html）- 运行监控
    │
    └──→ 导入与扩展
            ├── 智能体导入（aip-agent-import.html）
            └── 能力导入（aip-capability-import.html）
```

#### 业务逻辑要点（样式规整时不可破坏）

1. **分层架构**：模型层 → Logic层 → Agent层 → 应用层，样式调整不得打乱层级
2. **人在回路（HITL）**：Draft审批台是关键治理环节，样式不得弱化其存在感
3. **可观测性**：决策谱系 + 可观测性是信任基础，样式需突出信息层级
4. **成熟度分级**：L2/L3/L4 是产品核心叙事，视觉上需有明确区分
5. **熔断机制**：L4熔断是安全红线，视觉上需有强烈警示效果

---

### 1.3 模型管理业务流

#### 核心业务链路

```
模型管理（三层栈式架构）
    │
    ├── L1：模型供应商（aip-model-providers.html）
    │       ├── 供应商列表与健康状态
    │       ├── 凭据管理（密钥分槽，禁明文）
    │       └── 连通性测试
    │
    ├── L2：模型路由（aip-model-router.html）
    │       ├── 路由规则配置
    │       ├── 负载均衡策略
    │       └── 出境管控（禁公网/审批后）
    │
    ├── L3：模型目录（aip-model-catalog.html）
    │       ├── 模型列表与详情
    │       ├── 模型元数据管理
    │       └── 模型标签与分类
    │
    └── 容量管理（aip-capacity-management.html）
            ├── 使用量查看
            ├── 速率限制管理
            └── 预留容量配置
```

#### 业务逻辑要点（样式规整时不可破坏）

1. **三层栈式架构**：供应商 → 路由 → 目录，是产品核心叙事，样式需强化此认知
2. **Provider 插件化**：新增供应商不改 Facade 核心，样式需支持扩展
3. **密钥安全**：密钥分槽、禁明文，样式上需有安全视觉暗示
4. **熔断联动**：与成熟度L4/Lineage事件互通，样式上需有状态联动指示
5. **模型预热**：冷模型warm-up，样式需显示预热态/就绪态

---

### 1.4 本体 · 数字孪生业务流

#### 核心业务链路

```
本体（Ontology）是 AOS 的语义层，所有业务对象的"单一事实来源"
    │
    ├──→ 本体管理（/ontology，疑似缺失首页）
    │       └── 收藏 Object 类型网格 + 最近查看列表
    │
    ├──→ 提案与治理（ontology.tsx，改造完成样板）
    │       ├── 本体提案 FunnelPage（/ontology/funnel）- 漏斗管道监控
    │       ├── 图谱健康度 GraphHealthPage（/ontology/graph-health）
    │       ├── 分支管理 BranchesPage（/ontology/branches）- checkout + Diff
    │       ├── OKF funnel OkfFunnelPage（/ontology/okf-funnel）- 行业漏斗 + Lint
    │       └── OKF 概览 OkfOverviewPage（/ontology/okf-overview）- 4行业卡片
    │
    ├──→ 类型编辑器（5个独立 Editor 文件，技术债重灾区）
    │       ├── 对象类型详情 ObjectTypeDetailPage（7 Tab 面板）
    │       ├── 属性类型详情 PropertyEditorPage（两栏 grid + CRUD）
    │       ├── Function 详情 FunctionEditorPage（代码编辑器 + 参数表）
    │       ├── Link 类型详情 LinkTypeEditorPage（4 section）
    │       └── Action 详情 ActionTypeEditorPage（4 section + 5 状态色）
    │
    └──→ 活知识 Wiki（知识载体）
            ├── Wiki 索引 WikiIndexPage（两栏，完全脱离 Bp 体系）
            ├── Wiki 详情 WikiDetailPage（73 处硬编码，最严重）
            └── Wiki 差异 WikiDiffPage
```

#### 业务逻辑要点（样式规整时不可破坏）

1. **本体是单一事实来源**：Object/Property/Link/Action/Function 五大类型构成语义层，样式调整不得打乱类型边界
2. **分支与提案**：ontology 支持 Branch（协作）+ Funnel（提案治理），样式需区分"草稿/已合并/已废弃"
3. **Wiki 写回**：AI 生成 Wiki 通过 Draft 审批流写回 Ontology，样式需体现"AI产出 → 人工审批 → 入库"链路
4. **OKF 行业映射**：4 个行业（电商/供应链/金融/医疗）的标准化漏斗，样式需支持行业切换
5. **类型编辑器是开发者工具**：与运行态页面不同，编辑器需高信息密度，不能为了视觉而牺牲字段展示

---

### 1.5 管道与数据治理业务流

#### 核心业务链路

```
数据治理（Pipeline）是把外部数据"洗进" Ontology 的生产流水线
    │
    ├──→ 管道构建 PipelinesPage（/data/pipelines）
    │       └── 两栏：左项目树 + 右最近编辑卡片网格（含 16 处硬编码）
    │
    ├──→ 管道详情 PipelineCanvasPage（/data/pipelines/:pipelineId）
    │       └── 三栏：DAG 画布 + 输出预览 + Inspector（含 10 处硬编码，部分 Bp）
    │
    ├──→ 管道提案 PipelineProposalsPage（/data/pipeline-proposals）
    │       └── 单栏 + Tab（待审/历史）+ Diff 提示（0 硬编码，规范）
    │
    ├──→ 数据集 DatasetPage（列表 + 详情）
    │       ├── DatasetsPage（/data/datasets）- 两栏 + 4 Tab
    │       └── DatasetPreviewPage（/data/datasets/:datasetId）- 两栏 + 3 Tab + CSV导出
    │
    ├──→ 调度与构建
    │       ├── SchedulesPage（/data/schedules）- 两栏 + Cron + 运行历史条形图（11 处硬编码）
    │       ├── BuildsPage（/data/builds）- 两栏
    │       └── BuildModalPage（/data/builds/current）- 单栏 + 3 Tab
    │
    ├──→ 治理与监控
    │       ├── DataLineagePage（/data/lineage）- 两栏 + SVG 图谱（12 处 fallback 硬编码）
    │       ├── DataHealthPage（/data/health）- 单栏 + 4 Tab（3 处 fallback）
    │       └── CodeRepositoriesPage（/data/code-repos）- 两栏 IDE（2 处 fallback）
    │
    └──→ DocIntel 管道 DocumentIntelligencePage（aip/doc-intelligence）
            ✅ 路由已注册（App.tsx:262），功能完整（796 行 + 375 行单元测试）
            ⚠️ 约 123 处硬编码 + 不用 Bp 组件体系，需样式规整
```

#### 业务逻辑要点（样式规整时不可破坏）

1. **Pipeline 是生产流水线**：从数据源 → 变换 → 写入 Ontology，样式需体现"流向"概念
2. **DAG 拓扑是核心**：管道详情用 DAG 图表达算子依赖，样式不得破坏节点/连线/层级关系
3. **提案治理**：管道变更走 Proposal 审批（类似本体 Funnel），样式需区分 Edit/Proposals/History 三态
4. **数据健康度**：质量规则 + 问题列表 + 趋势，样式需支持多维过滤和问题定位
5. **沿袭可追溯**：Lineage 是合规基础，SVG 图谱的上下游遍历样式不得简化

---

### 1.6 数据源与同步业务流

#### 核心业务链路

```
数据源（Connection）是 Pipeline 的上游，负责"接入"外部数据
    │
    ├──→ 连接管理
    │       ├── DataConnectionPage（/data/connections）- 单栏 + 卡片网格 + 表格双视图
    │       └── DataSourceCreatePage（/data/sources/new）- 5 步向导（选类型→配置→选表→测试→完成）
    │
    ├──→ 数据源详情 sourceDetailPage（/data/sources/:sourceId）
    │       └── 三栏：左表树 + 中采样预览 + 右 inspector（探索 Tab）
    │
    ├──→ 边缘代理 EdgeAgentsPage（/data/agents）
    │       └── 两栏（注册代理按钮 disabled 占位）
    │
    ├──→ 同步
    │       ├── SyncConfigPage（/data/sync-config）- 单栏多面板 + Cron/邮箱校验
    │       └── SyncRoutesPage（/data/sync-routes）- 单栏 + Tab + 可展开详情
    │
    ├──→ 媒体集 MediaSetsPage（/data/media-sets）
    │       └── 单栏 + 拖拽上传 + 批量打标签（约 10 处硬编码）
    │
    └──→ 文档智能 DocumentIntelligencePage（aip/doc-intelligence）
            ✅ 功能完整（796 行 + 375 行单元测试），路由已注册（App.tsx:262），导航已挂载（nav.ts:574）
            ⚠️ **约 123 处硬编码 + 不用 Bp 组件体系**（本模块最大样式问题）
            └── 两栏：左文件列表 + 右 OCR/提取/审核三面板
```

#### 业务逻辑要点（样式规整时不可破坏）

1. **连接器插件化**：9 种连接器类型（MySQL/Postgres/Kafka/API...），样式需支持类型扩展
2. **5 步向导**：数据源新建是关键转化路径，步骤指示器三态（已完成/当前/未达）样式不得混乱
3. **采样预览**：限制 50 行 20 列的采样数据，样式需支持大数据量滚动
4. **同步调度**：Cron 表达式 + 字段映射，样式需体现"源 → 目标"的映射关系
5. **文档智能四态状态机**：uploaded → processing_ocr → extracting → review（+ failed/needs_correction 分支），样式需清晰区分状态流转

---

## 2. 全局样式规整清单

### 2.1 设计Token统一

| # | Token类别 | 规整内容 | 修改原因 | 影响范围 |
|---|---------|---------|---------|---------|
| T1 | 品牌色 | **统一到 `var(--aos-accent)`**（tokens.css 已定义：浅色 `#2B6CB0` 蓝 / 深色 `#22d3ee` 青），**删除 8 处 `#0F6E56` 深绿硬编码** | tokens.css 已定义品牌色，`#0F6E56` 是 4 个页面擅自用的硬编码，主题切换不联动 | 全站按钮、链接、选中态、强调色 |
| T2 | 语义色 | 统一成功/警告/错误/信息色值 | 状态一致性、降低认知成本 | 全站Badge、Alert、状态指示 |
| T3 | 字体系统 | 统一字体栈、字号层级（11/12/13/14/16px） | 可读性、排版节奏 | 全站文字 |
| T4 | 间距系统 | 统一间距基数（4/8/12/16/20/24/32px） | 布局一致性、呼吸感 | 全站组件内/外边距 |
| T5 | 圆角规范 | 统一圆角层级（2/4/6/8px） | 视觉统一、风格协调 | 全站卡片、按钮、输入框 |
| T6 | 阴影系统 | 统一阴影层级（sm/md/lg） | 层次清晰、深度感 | 全站悬浮元素、卡片、弹窗 |

---

### 2.2 公共组件样式规整

#### 2.2.1 按钮体系

| # | 按钮类型 | 规整内容 | 修改原因 |
|---|---------|---------|---------|
| B1 | btn-nav | 页内/顶栏导航按钮，统一描边样式 | 导航按钮与操作按钮视觉区分，避免混淆 |
| B2 | btn-nav-accent | 当前相关/主跳转导航，琥珀描边浅底 | 突出当前上下文的导航入口 |
| B3 | btn | 次要操作（刷新、收起步骤），ghost描边 | 次级操作弱化视觉权重 |
| B4 | btn-primary | 主操作（保存、新建），实心（使用 `--aos-accent` 品牌色） | 主操作强视觉引导 |
| B5 | btn-outline-cyan | 强调次操作（测连通、试跑），青色描边 | 功能性次操作的视觉识别 |
| B6 | bp-action-link | 表内行级文字链，青色 | 表格内操作的轻量化表达 |

**规整原则**：
- 顶栏用导航按钮（btn-nav*），不用 muted 文字当导航
- 每页主操作按钮不超过 2 个
- 危险操作（删除、撤销）用红色/警告色区分
- 按钮高度、内边距、圆角全站统一

#### 2.2.2 卡片体系

| # | 卡片类型 | 规整内容 | 修改原因 |
|---|---------|---------|---------|
| C1 | 标准卡片 | 统一 padding、圆角、边框、hover 效果 | 卡片是最常用容器，一致性最重要 |
| C2 | 统计卡片 | 统一大数字字号、eyebrow标签样式、底部趋势线位置 | KPI信息快速读取 |
| C3 | 列表卡片 | 统一列表项高度、分隔线、hover高亮 | 列表浏览效率 |
| C4 | 状态卡片 | 统一状态徽章位置、状态色边框 | 状态信息一眼可识别 |

#### 2.2.3 表格体系

| # | 规整项 | 规整内容 | 修改原因 |
|---|-------|---------|---------|
| TBL1 | 表头 | 统一表头高度、背景色、文字样式 | 表格是核心数据载体，样式需专业 |
| TBL2 | 行高 | 统一定义紧凑/标准/宽松三档行高 | 不同数据密度场景适配 |
| TBL3 | 选中态 | 统一选中行背景色、左侧高亮边 | 选中状态清晰可识别 |
| TBL4 | hover态 | 统一行 hover 背景色 | 交互反馈 |
| TBL5 | 分页 | 统一分页控件样式和位置 | 翻页操作一致性 |

#### 2.2.4 Tab 体系

| # | 规整项 | 规整内容 | 修改原因 |
|---|-------|---------|---------|
| TAB1 | 顶栏Tab | 统一高度、下划线颜色、激活态样式 | 页面内导航一致性 |
| TAB2 | 侧边Tab | 统一宽度、左侧激活条、缩进层级 | 左侧导航Tab的视觉统一 |
| TAB3 | 卡片内Tab | 统一紧凑型样式、小字号 | 卡片内次级导航轻量化 |

---

### 2.3 页面布局规整

#### 2.3.1 页面结构统一

| # | 布局部件 | 规整内容 | 修改原因 |
|---|---------|---------|---------|
| L1 | 页面头部（PageChrome） | 统一标题 + 副标题 + 操作按钮区布局 | 每页入口信息结构一致 |
| L2 | 面包屑 | 统一面包屑样式、分隔符、字号 | 页面定位导航 |
| L3 | 内容区最大宽度 | 统一内容区最大宽度约束（窄内容/中等/全宽） | 阅读舒适度、避免过宽 |
| L4 | 侧边栏 | 统一左侧/右侧边栏宽度、折叠态样式 | 三栏/两栏布局一致性 |
| L5 | 底部操作栏 | 统一固定底栏样式、按钮排列 | 表单页操作区位置可预期 |

#### 2.3.2 布局模式规范

| 模式 | 适用场景 | 结构说明 |
|-----|---------|---------|
| 单栏居中 | 详情页、配置页、向导页 | 内容区 max-w-3xl/4xl/5xl，居中显示 |
| 两栏布局 | 列表+详情、设置页 | 左侧导航/列表（240-280px）+ 右侧主内容 |
| 三栏布局 | 画布编辑器、复杂工具 | 左面板（260-280px）+ 中间舞台 + 右属性面板（300-320px） |
| 全屏布局 | 画布、地图、COP大屏 | 内容铺满视口，工具栏浮动 |

---

## 3. 工作台样式规整明细

### 3.1 应用列表（workshop.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| W1-1 | 页面头部 | 标题 + 描述 + 新建按钮 | 对齐视觉稿：eyebrow + 标题 + 描述 + 右侧绿色主按钮 | 统一页面入口结构 | 低 |
| W1-2 | 最近使用区 | 有，卡片样式 | 对齐视觉稿卡片样式（eyebrow多色 + 应用名 + 描述 + 双链接） | 卡片信息结构一致 | 低 |
| W1-3 | 分类筛选Tab | 有，样式需统一 | 对齐视觉稿Tab样式（9个分类：全部/运营/分析/AI助手/风控/本体前端/态势感知/智能嵌入/系统集成） | 分类完整 + Tab样式统一 | 低 |
| W1-4 | 应用卡片网格 | 3列网格 | 对齐视觉稿网格间距、卡片圆角、hover效果 | 视觉统一 | 低 |
| W1-5 | 卡片状态徽章 | 部分有 | 统一徽章位置和样式（草稿/已发布） | 状态一眼可识别 | 低 |

**说明**：应用列表是工作台入口，样式规整以信息清晰度和分类效率为目标，不改变分类逻辑和卡片数据结构。

---

### 3.2 画布编辑器（workshop-canvas.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| W3-1 | 顶部工具栏 | 部分实现 | 对齐视觉稿：模块/预览切换 + 工作流模式 + 保存/发布 + 撤销重做 | 编辑态核心操作入口完整 | 低 |
| W3-2 | 模式切换按钮 | ✅ 已实现三态切换（模块/工作流/预览） | 仅需样式对齐视觉稿按钮样式 | 功能已就绪，仅样式规整 | 低 |
| W3-3 | 9个功能Tab | 部分有 | 补充完整 Tab：Dashboard/Queries/Functions/Objects/Events/Data/Dependencies/Styles/Variables | 画布编辑器功能完整性 | 中（部分Tab功能未实现，可先占位） |
| W3-4 | 左栏组件树 | 有 | 对齐视觉稿树状结构样式、图标、缩进 | 组件层级清晰 | 低 |
| W3-5 | 中间画布区 | 有 | 对齐视觉稿画布背景、网格、选中态样式 | 编辑体验一致 | 低 |
| W3-6 | 右栏属性面板 | 有 | 对齐视觉稿面板样式、分组、表单控件 | 属性配置效率 | 低 |
| W3-7 | 底部操作栏 | 部分有 | 对齐视觉稿删除组件 + 搜索组件栏 | 快捷操作可预期 | 低 |

**说明**：画布编辑器是工作台核心工具，样式规整以编辑效率和功能可达性为目标。缺的功能Tab可以先做样式占位，功能后续补充。**不因为样式而删减已有功能**。

---

### 3.3 组件注册表（workshop-widget-registry.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| W4-1 | 页面头部 | 有 | 对齐视觉稿：标题 + 描述 + 右侧"上传组件"按钮 | 统一页面结构 | 低 |
| W4-2 | 来源分类Tab | 有4个Tab | 对齐视觉稿Tab样式 + 确保4个Tab都有内容（全部/平台内置/市场安装/代码开发） | 插件化产品叙事清晰 | 低 |
| W4-3 | 卡片网格布局 | 2列 → 3列 | 对齐视觉稿3列卡片网格布局 | 信息密度合适 + 视觉稿对齐 | 低 |
| W4-4 | 组件卡片样式 | 部分实现 | 对齐视觉稿：图标 + 组件名 + 描述 + 来源标签（蓝/绿/橙色区分） | 组件信息清晰，来源一眼可识别 | 低 |
| W4-5 | 来源标签颜色 | 需统一 | 平台内置=蓝色、市场安装=绿色、代码开发=橙色 | 颜色编码降低认知成本 | 低 |

**说明**：组件注册表是Widget插件化的管理界面，样式规整以组件发现效率和来源区分为目标。

---

### 3.4 变量管理器（workshop-variables.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| W5-1 | 两栏布局 | 有 | 对齐视觉稿：左侧变量类型分组 + 右侧变量详情/表单 | 变量管理信息架构清晰 | 低 |
| W5-2 | 变量类型分组 | 5种类型 | 对齐视觉稿分组样式：Object Set/Selection/Active/Scalar/Function结果 | 变量类型一目了然 | 低 |
| W5-3 | 变量表单 | 有 | 对齐视觉稿动态表单样式（根据类型显示不同字段） | 配置效率 | 低 |

**说明**：变量管理器是状态管理核心，样式规整以配置清晰度和类型区分为目标。

---

### 3.5 事件配置（workshop-events.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| W8-1 | 上下布局 | 有 | 对齐视觉稿：上部事件列表 + 下部5步创建向导 | 事件浏览 + 创建双场景兼顾 | 低 |
| W8-2 | 触发器卡片 | 部分有 | 对齐视觉稿6种触发器卡片样式（行选/按钮/筛选/页面加载/定时/外部事件） | 触发器类型直观可选择 | 低 |
| W8-3 | 动作卡片 | 部分有 | 对齐视觉稿5种动作卡片样式（写变量/调Action/刷数据/导航/弹框） | 动作类型直观可选择 | 低 |
| W8-4 | 步骤向导 | 部分有 | 对齐视觉稿5步向导样式（选触发器→配条件→选动作→设目标→确认） | 创建流程清晰引导 | 低 |

**说明**：事件配置是交互逻辑编排界面，样式规整以创建流程引导和类型识别为目标。

---

## 4. AIP 决策引擎样式规整明细

### 4.1 AIP 助手（aip-assist.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| A1-1 | 单栏聊天布局 | 有 | 对齐视觉稿：max-w-3xl 居中聊天界面 | 聊天体验聚焦，减少干扰 | 低 |
| A1-2 | AI消息气泡 | 样式不同 | 对齐视觉稿：紫蓝渐变气泡 + AI标识 | AI回答的视觉辨识度 | 低 |
| A1-3 | 建议卡片 | 部分有 | 对齐视觉稿：2列建议问题卡片网格 | 引导用户提问，降低使用门槛 | 低 |
| A1-4 | 输入区 | 有 | 对齐视觉稿输入框样式 + 快捷操作按钮 | 输入体验一致 | 低 |

**说明**：AIP助手是用户接触AI的第一入口，样式规整以对话舒适度和引导效率为目标。**不因为样式改变对话逻辑和AI响应质量**。

---

### 4.2 对话机器人（agents.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| A2-1 | 两栏布局 | 有 | 对齐视觉稿：左侧Agent列表（256px）+ 右侧4Tab详情区 | Agent管理信息架构清晰 | 低 |
| A2-2 | Agent列表项 | 样式不同 | 对齐视觉稿列表项样式（头像+名称+描述+状态徽章） | 列表浏览效率 | 低 |
| A2-3 | 右侧4Tab | 部分有 | 对齐视觉稿：配置/工具/测试/发布 4个Tab | Agent配置全流程覆盖 | 低 |
| A2-4 | 创建向导 | 有4步向导 | 对齐视觉稿4步向导样式（基本信息→选能力→配工具→确认） | 创建流程清晰引导 | 低 |

**说明**：对话机器人是Agent Studio核心，样式规整以配置效率和流程清晰为目标。

---

### 4.3 AIP 逻辑画布（aip-logic.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| A4-1 | 节点样式 | 部分实现 | 对齐视觉稿：Get Object/Wiki/LLM/Function/Draft/Action 6种节点样式 | 节点类型一眼识别 | 低 |
| A4-2 | 分支节点 | ✅ 已实现（branch + handoff） | 仅需样式对齐视觉稿双路红/绿 + 汇聚Handoff节点样式 | 功能已就绪，仅样式规整 | 低 |
| A4-3 | 连接线样式 | 有 | 对齐视觉稿连线粗细、颜色、箭头样式 | 逻辑流向清晰 | 低 |

**说明**：逻辑画布是AI编排核心，样式规整以逻辑可读性和节点类型区分为目标。

---

### 4.4 智能体目录（agent-registry.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| A7-1 | 布局形式 | 表格形式 → 卡片网格 | 对齐视觉稿3列卡片网格布局 | 卡片形式更适合Agent展示（头像+描述+标签） | 低 |
| A7-2 | 来源Tab | 有 | 对齐视觉稿Tab样式（全部/内置/市场/自定义） | 来源分类清晰 | 低 |
| A7-3 | 统计数字 | 缺 | 对齐视觉稿顶部统计区（总Agent数/已启用/待审核） | 概览信息快速获取 | 低 |
| A7-4 | Agent卡片 | 需重做 | 对齐视觉稿卡片：头像+名称+描述+能力标签+来源徽章+操作按钮 | Agent信息结构完整 | 低 |

**说明**：智能体目录是Agent发现和管理的入口，卡片形式比表格更适合展示Agent信息。**功能逻辑不变，只是展示形式从表格改为卡片**。

---

### 4.5 决策谱系（aip-decision-lineage.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| A11-1 | 6段阶段 | 划分不清晰 | 对齐视觉稿：输入/检索/推理/熔断事件/输出/回填 6个独立阶段 | 决策全链路可视化，可追溯 | 低 |
| A11-2 | 熔断高亮 | 不明显 | 对齐视觉稿：熔断事件阶段红色高亮警示 | 安全红线视觉强化 | 低 |
| A11-3 | 回填高亮 | 不明显 | 对齐视觉稿：回填阶段紫色高亮（AI写回Ontology） | 关键动作突出显示 | 低 |

**说明**：决策谱系是AI可解释性的关键，样式规整以链路清晰度和关键节点突出为目标。

---

## 5. 模型管理样式规整明细

### 5.1 模型目录（aip-model-catalog.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| M1-1 | 三层架构条 | ⚠️ 组件已开发但未接入 | 接入 BpArchitectureBar 组件（L3高亮） | 产品核心叙事：三层栈式架构，强化用户认知 | 低 |
| M1-2 | 架构条高亮 | 需实现 | 当前页（目录）L3高亮，L1/L2可点击跳转 | 跨页导航上下文清晰 | 低 |
| M1-3 | 3个内容Tab | 有 | 对齐视觉稿Tab样式（全部模型/我的收藏/最近使用） | 模型浏览多场景支持 | 低 |
| M1-4 | 模型卡片/列表 | 有 | 对齐视觉稿列表样式（模型名+提供商+描述+标签+状态） | 模型信息结构统一 | 低 |

**说明**：三层架构条是模型管理的产品核心叙事，必须在视觉上强化。这不是单纯的样式装饰，而是产品信息架构的一部分。

---

### 5.2 模型供应商（aip-model-providers.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| M2-1 | 三层架构条 | ⚠️ 组件已开发但未接入 | 接入 BpArchitectureBar 组件（L1高亮） | 与模型目录/路由页保持一致的导航上下文 | 低 |
| M2-2 | 健康检查总览卡 | 缺 | 补充4个健康检查卡（深度求索/Azure/vLLM/Anthropic），含p50延迟+可用率 | 供应商健康状态一眼可见，运维效率 | 中（需后端API支持） |
| M2-3 | 供应商列表 | 有 | 对齐视觉稿列表样式（名称+状态+模型数+延迟+操作） | 列表信息结构统一 | 低 |

**说明**：健康检查卡片是运维关键信息，样式规整以状态可见性为目标。如后端暂不支持完整健康数据，可先做样式骨架 + mock数据占位。

---

### 5.3 模型路由（aip-model-router.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| M3-1 | 三层架构条 | ⚠️ 组件已开发但未接入 | 接入 BpArchitectureBar 组件（L2高亮） | 保持三层架构叙事一致性 | 低 |
| M3-2 | 出境管控列 | 有 | 对齐视觉稿样式（禁公网/审批后标签） | 安全策略可视化 | 低 |
| M3-3 | 路由规则列表 | 有 | 对齐视觉稿表格样式（规则名+源模型+目标模型+策略+状态） | 规则管理清晰度 | 低 |

**说明**：模型路由是流量调度核心，样式规整以规则清晰度和安全可见性为目标。

---

### 5.4 容量管理（aip-capacity-management.html）

| # | 规整项 | 当前状态 | 目标样式 | 修改原因 | 风险 |
|---|-------|---------|---------|---------|------|
| M4-1 | 3个Tab | 缺 | 补充3个Tab：查看使用量/管理速率限制/预留容量 | 容量管理三场景覆盖 | 低 |
| M4-2 | Info Banner | 缺 | 补充提示Banner（说明限额策略） | 降低用户困惑，减少咨询 | 低 |
| M4-3 | 使用量图表 | 部分有 | 对齐视觉稿图表样式（折线图+统计数字） | 用量趋势可视化 | 低 |

**说明**：容量管理是成本控制关键，样式规整以用量可见性和配置便捷性为目标。

---

## 6. 本体 · 数字孪生样式规整明细

> **模块特点**：页面分两类——`ontology.tsx`/`remainder.tsx` 是已改造样板（0 硬编码 + 全量 Bp），5 个独立 Editor 文件 + WikiIndexPage 是技术债重灾区。规整策略：**样板不动，重灾区优先治理硬编码**。

### 6.1 本体提案与治理（已改造样板，仅微调）

| # | 页面 | 文件 | 当前状态 | 规整项 | 修改原因 | 风险 |
|---|------|------|---------|--------|---------|------|
| O-F1 | 图谱健康度 | ontology.tsx:29（`aos-platform/apps/web/src/pages/s2/ontology.tsx#L29`） | ✅ 0 硬编码 + 全量 Bp | 无需改动，作为样板参考 | 已达标 | — |
| O-F2 | 本体提案 | ontology.tsx:206（`aos-platform/apps/web/src/pages/s2/ontology.tsx#L206`） | ✅ 0 硬编码 + BpStagePipeline | 无需改动 | 已达标 | — |
| O-F3 | 分支管理 | ontology.tsx:697（`aos-platform/apps/web/src/pages/s2/ontology.tsx#L697`） | ✅ 0 硬编码 + checkout + Diff | 无需改动 | 已达标 | — |
| O-F4 | OKF funnel | remainder.tsx:28（`aos-platform/apps/web/src/pages/s2/remainder.tsx#L28`） | ✅ 11 种 Bp 组件 | 无需改动 | 已达标 | — |
| O-F5 | OKF 概览 | remainder.tsx:970（`aos-platform/apps/web/src/pages/s2/remainder.tsx#L970`） | ✅ 轻量完整 | 无需改动 | 已达标 | — |

### 6.2 类型编辑器（技术债重灾区，重点治理）

| # | 页面 | 文件 | 硬编码数 | 规整项 | 修改原因 | 风险 |
|---|------|------|---------|--------|---------|------|
| O-E1 | 对象类型详情 | ObjectTypeDetailPage.tsx（`aos-platform/apps/web/src/pages/s2/ObjectTypeDetailPage.tsx`） | 壳 0 / Panel 待查 | 确认 objectTypeDetail.tsx（`aos-platform/apps/web/src/pages/s2/objectTypeDetail.tsx`） Panel 内硬编码情况 | 壳已达标，Panel 需验证 | 低 |
| O-E2 | 属性类型详情 | PropertyEditorPage.tsx（`aos-platform/apps/web/src/pages/s2/PropertyEditorPage.tsx`） | **10 处** | 硬编码 → token；Bp 组件仅外壳，主体需补 BpTable/BpTabs | 主体脱离设计体系 | 中（CRUD 逻辑密集，需小心）|
| O-E3 | Function 详情 | FunctionEditorPage.tsx（`aos-platform/apps/web/src/pages/s2/FunctionEditorPage.tsx`） | **10 处** | 硬编码 → token；代码编辑器区域保留自定义 | 编辑器主体可保留，外壳需统一 | 中 |
| O-E4 | Link 类型详情 | LinkTypeEditorPage.tsx（`aos-platform/apps/web/src/pages/s2/LinkTypeEditorPage.tsx`） | **32 处** | 硬编码 → token；4 section 改用 Bp 组件 | 硬编码量大，优先治理 | 中 |
| O-E5 | Action 详情 | ActionTypeEditorPage.tsx（`aos-platform/apps/web/src/pages/s2/ActionTypeEditorPage.tsx`） | **37 处** | 硬编码 → token；5 个状态色（ACTION_STATUS_COLORS）抽到 token | 硬编码量最大（编辑器类） | 中 |

### 6.3 活知识 Wiki（最严重技术债）

| # | 页面 | 文件 | 硬编码数 | 规整项 | 修改原因 | 风险 |
|---|------|------|---------|--------|---------|------|
| O-W1 | Wiki 索引 | WikiIndexPage.tsx（`aos-platform/apps/web/src/pages/s2/WikiIndexPage.tsx`） | 7 处 + 完全脱离 Bp | **整体重构**：引入 Bp 组件体系，替换 `bp-wiki-card` 自创 className | 唯一完全脱离 Bp 的页面，优先级最高 | 高（需保留分支树+卡片网格功能）|
| O-W2 | Wiki 详情 | WikiDetailPage.tsx（`aos-platform/apps/web/src/pages/s2/WikiDetailPage.tsx`） | **73 处（全站之最）** | 硬编码 → token；widget/workflow/runtime 三模式样式统一 | 硬编码量全站第一，主题切换全失效 | 高（715 行 + 三种模式，需分批治理）|
| O-W3 | Wiki 差异 | WikiDiffPage.tsx | 待查 | 对齐 BpDiffViewer 组件样式 | 复用已有 BpDiffViewer | 低 |

### 6.4 本体模块治理优先级

| 优先级 | 治理目标 | 理由 |
|-------|---------|------|
| **P0** | WikiDetailPage 73 处硬编码 | 全站之最，主题切换全失效 |
| **P0** | WikiIndexPage 整体重构 | 唯一完全脱离 Bp 体系的页面 |
| **P1** | ActionTypeEditorPage 37 处 + LinkTypeEditorPage 32 处 | 编辑器类硬编码重灾区 |
| **P2** | PropertyEditorPage 10 处 + FunctionEditorPage 10 处 | 量级可控 |
| **样板** | ontology.tsx / remainder.tsx | 已达标，作为重构参考基线 |

---

## 7. 管道与数据治理样式规整明细

> **模块特点**：大部分页面已用规范的 `var(--p-*, #fallback)` 形式（可接受），但 `data.tsx` 16 处和 `pipelineCanvas.tsx` 10 处是直接写死的硬编码（需治理）。另有 DocumentIntelligencePage 样式规整和 DataHealthPage 死代码风险。

### 7.1 管道构建与详情（硬编码重点）

| # | 页面 | 文件 | 硬编码数 | 规整项 | 修改原因 | 风险 |
|---|------|------|---------|--------|---------|------|
| P-P1 | 管道构建 | data.tsx:80（`aos-platform/apps/web/src/pages/s2/data.tsx#L80`） | **16 处（直接写死）** | 统计卡内联色（`#f0fff4`/`#c6f6d5`/`#22543d` 等）→ token；保留两栏布局 | 直接写死非 fallback，主题切换失效 | 中 |
| P-P2 | 管道详情 | pipelineCanvas.tsx:106（`aos-platform/apps/web/src/pages/s2/pipelineCanvas.tsx#L106`） | **10 处（直接写死）** | 右键菜单 + 画布工具栏色（`#2a3540`/`#e2e8f0` 等）→ token；DAG 节点保留自定义 | 画布交互密集，需保留功能 | 中（画布交互复杂）|

### 7.2 数据集与调度（fallback 形式，可接受）

| # | 页面 | 文件 | 硬编码数 | 规整项 | 修改原因 | 风险 |
|---|------|------|---------|--------|---------|------|
| P-D1 | 数据集列表 | data.tsx:344（`aos-platform/apps/web/src/pages/s2/data.tsx#L344`） | 含于 16 处 | 随 P-P1 一并治理 | 同源文件 | 中 |
| P-D2 | 数据集详情 | DatasetPreviewPage.tsx:219（`aos-platform/apps/web/src/pages/s2/DatasetPreviewPage.tsx#L219`） | 3 处 fallback | ✅ 已用 `var(--p-*, #xxx)` 形式，可接受 | 已达标 | 低 |
| P-D3 | 计划编辑器 | dataSchedules.tsx:63（`aos-platform/apps/web/src/pages/s2/dataSchedules.tsx#L63`） | **11 处** | 运行历史条形图色（`#10B981`/`#EF4444`/`#3B82F6`）→ token | 图表色板可保留，状态色需 token | 低 |
| P-D4 | 搭建 | data.tsx:263（`aos-platform/apps/web/src/pages/s2/data.tsx#L263`） | 含于 16 处 | 随 P-P1 一并治理 | 同源文件 | 中 |
| P-D5 | 当前构建详情 | BuildModalPage.tsx:256（`aos-platform/apps/web/src/pages/s2/BuildModalPage.tsx#L256`） | 5 处 fallback | ✅ 已达标 | 已达标 | 低 |

### 7.3 治理与监控（fallback 形式，基本达标）

| # | 页面 | 文件 | 硬编码数 | 规整项 | 修改原因 | 风险 |
|---|------|------|---------|--------|---------|------|
| P-M1 | 管道提案 | remainder.tsx:230（`aos-platform/apps/web/src/pages/s2/remainder.tsx#L230`） | **0 处** | ✅ 已达标，作为样板 | 已达标 | — |
| P-M2 | 数据沿袭 | DataLineagePage.tsx:224（`aos-platform/apps/web/src/pages/s2/DataLineagePage.tsx#L224`） | 12 处 fallback | ✅ 已用 fallback；SVG 图谱色板可保留 | 已达标 | 低 |
| P-M3 | 数据健康 | DataHealthPage.tsx:233（`aos-platform/apps/web/src/pages/s2/DataHealthPage.tsx#L233`） | 3 处 fallback | ✅ 已达标；清理 data.tsx:606（`aos-platform/apps/web/src/pages/s2/data.tsx#L606`） 死代码版本 | 死代码风险 | 低 |
| P-M4 | 代码库 | CodeRepositoriesPage.tsx:237（`aos-platform/apps/web/src/pages/s2/CodeRepositoriesPage.tsx#L237`） | 2 处 fallback | ✅ 已达标 | 已达标 | 低 |

### 7.4 样式规整重点（功能完整但样式需对齐）

| # | 页面 | 文件 | 问题 | 规整项 | 修改原因 | 风险 |
|---|------|------|------|--------|---------|------|
| P-O1 | DocIntel 管道 | DocumentIntelligencePage.tsx（`aos-platform/apps/web/src/pages/s2/DocumentIntelligencePage.tsx`） | ✅ 路由已注册（aip/doc-intelligence），功能完整（796行+375行测试） | **样式规整**：引入 Bp 组件体系，123 处硬编码 token 化，四态状态机样式统一 | OCR 提取 + 四态审核流是保留功能，需样式对齐 | 中 |

### 7.5 管道模块治理优先级

| 优先级 | 治理目标 | 理由 |
|-------|---------|------|
| **P0** | data.tsx 16 处直接写死硬编码 | 非 fallback 形式，主题切换失效 |
| **P0** | pipelineCanvas.tsx 10 处直接写死 | 画布核心，主题切换失效 |
| **P1** | dataSchedules.tsx 11 处图表色 | 状态色需 token 化 |
| **P1** | DocIntel 样式规整 | 功能已确认保留，按 P0 执行样式规整 |
| **P2** | DataHealthPage 死代码清理 | data.tsx:606 版本未使用 |
| **样板** | PipelineProposalsPage / DataLineagePage / DataHealthPage / CodeRepositoriesPage | 已达标，作为参考 |

---

## 8. 数据源与同步样式规整明细

> **模块特点**：大部分页面已规范使用 Bp 组件，但 DocumentIntelligencePage 样式问题较多（约 123 处硬编码 + 不用 Bp 组件体系），MediaSetsPage 和 DataSourceCreatePage 有约 10 处硬编码需治理。

### 8.1 连接管理（基本达标）

| # | 页面 | 文件 | 硬编码数 | 规整项 | 修改原因 | 风险 |
|---|------|------|---------|--------|---------|------|
| D-C1 | 数据连接器 | DataConnectionPage.tsx（`aos-platform/apps/web/src/pages/s2/DataConnectionPage.tsx`） | 1 处（`#dc2626` 删除按钮）| 删除按钮色 → `var(--aos-red)` | 危险操作色 token 化 | 低 |
| D-C2 | 数据源新建 | DataSourceCreatePage.tsx（`aos-platform/apps/web/src/pages/s2/DataSourceCreatePage.tsx`） | **约 10 处** | 步进器色（`#d1fae5`/`#dbeafe`/`#10b981` 等）→ token；卡片选中态 `#2563eb` → `--aos-accent` | 5 步向导是关键转化路径，样式需规范 | 中 |
| D-C3 | 数据源详情 | sourceDetailPage.tsx（`aos-platform/apps/web/src/pages/s2/sourceDetailPage.tsx`） | 0 处 | ✅ 已达标；文件名全小写需统一为 PascalCase | 命名规范 | 低（仅重命名）|

### 8.2 边缘代理与同步（已达标）

| # | 页面 | 文件 | 硬编码数 | 规整项 | 修改原因 | 风险 |
|---|------|------|---------|--------|---------|------|
| D-S1 | 边缘代理 | data.tsx:707（`aos-platform/apps/web/src/pages/s2/data.tsx#L707`） | 0 处 | ✅ 已达标；"注册代理"按钮 disabled 占位需确认是否补功能 | 功能占位 | 需产品确认 |
| D-S2 | 同步配置 | SyncConfigPage.tsx（`aos-platform/apps/web/src/pages/s2/SyncConfigPage.tsx`） | 0 处 | ✅ 已达标 | 已达标 | — |
| D-S3 | 同步路由 | SyncRoutesPage.tsx（`aos-platform/apps/web/src/pages/s2/SyncRoutesPage.tsx`） | 0 处 | ✅ 已达标 | 已达标 | — |

### 8.3 媒体集（硬编码治理）

| # | 页面 | 文件 | 硬编码数 | 规整项 | 修改原因 | 风险 |
|---|------|------|---------|--------|---------|------|
| D-M1 | 媒体集 | MediaSetsPage.tsx（`aos-platform/apps/web/src/pages/s2/MediaSetsPage.tsx`） | **约 10 处** | 分类标签色（`#dbeafe`/`#fef3c7`/`#fce7f3` 等）→ token；拖拽区 + 缩略图网格保留 | 分类色板需 token 化支持主题 | 中 |

### 8.4 文档智能（全模块最大问题）

| # | 页面 | 文件 | 问题 | 规整项 | 修改原因 | 风险 |
|---|------|------|------|--------|---------|------|
| D-DI1 | 文档智能 | DocumentIntelligencePage.tsx（`aos-platform/apps/web/src/pages/s2/DocumentIntelligencePage.tsx`） | ✅ 路由已注册（aip/doc-intelligence），功能完整（796行+375行测试）；⚠️ **约 123 处硬编码 + 不用 Bp 组件体系** | **样式规整**：1) 引入 Bp 组件体系（BpToolbar/BpBadge/BpCard/BpTabs）；2) STATE_META/TYPE_META 色板 token 化；3) 四态状态机样式统一；4) OCR/提取/审核三面板样式对齐 | OCR 提取 + 四态审核流是保留功能方向，需样式对齐设计系统 | 中（功能完整，仅样式重构）|

### 8.5 数据源模块治理优先级

| 优先级 | 治理目标 | 理由 |
|-------|---------|------|
| **P0** | DocumentIntelligencePage 样式规整 | OCR 提取 + 四态审核流是保留功能，约 123 处硬编码 + 不用 Bp，需样式对齐设计系统 |
| **P1** | DataSourceCreatePage 10 处硬编码 | 5 步向导是关键转化路径 |
| **P1** | MediaSetsPage 10 处硬编码 | 分类色板需 token 化 |
| **P2** | DataConnectionPage 1 处删除按钮色 | 量级小 |
| **P2** | sourceDetailPage 文件名统一 | 命名规范 |
| **样板** | SyncConfigPage / SyncRoutesPage / sourceDetailPage | 已达标，作为参考 |

---

## 9. 与已有工作的衔接（Phase 6 基础）

### 9.1 Phase 6 已完成的基础工作

Phase 6 已建立完整的样式 Token 体系和共享组件层，224 方案在此基础之上补齐剩余部分，**不重复造轮子**。

| 已完成项 | 位置 | 说明 | 224 如何衔接 |
|---------|------|------|-------------|
| CSS Token 体系（70+ 变量）| tokens.css（`aos-platform/packages/ui-kit/tokens.css`） | 含品牌色别名层 `--brand-primary` + 语义别名层 `--color-*` / `--bg-*` / `--text-*` | 224 的 T1-T6 Token 规整**直接使用已有 Token**，不再新增 |
| 主题切换 API | theme.ts（`aos-platform/apps/web/src/theme.ts`） | `getTheme/setTheme/toggleTheme/initTheme` | 224 样式规整后验证深浅主题切换正常 |
| 9 个 Bp 共享组件 | components/bp/（`aos-platform/apps/web/src/components/bp/`） | BpBadge/BpCard/BpToolbar/BpEmpty/BpArchitectureBar/BpStepper/BpCodeEditor/BpDiffViewer/BpSparkline/BpCronInput | 224 的组件样式规整**基于已有组件**，不新建组件 |
| 组件使用覆盖 | 50 个文件 95 处 | Bp 系列组件已覆盖绝大部分 s2 业务页面 | 224 聚焦**未接入**组件的页面 + 样式细节对齐 |

### 9.2 Phase 6 残留项（224 需补齐）

| 残留项 | 位置 | 问题 | 224 修复方案 |
|-------|------|------|-------------|
| `#0F6E56` 硬编码 8 处 | WorkshopListPage.tsx:268（`aos-platform/apps/web/src/pages/WorkshopListPage.tsx#L268`）、WorkshopCreatePage.tsx:341,366,430（`aos-platform/apps/web/src/pages/s2/WorkshopCreatePage.tsx#L341`）、AgentImportPage.tsx:2126（`aos-platform/apps/web/src/pages/s2/AgentImportPage.tsx#L2126`）、CapabilityImportPage.tsx:271,1117,1250（`aos-platform/apps/web/src/pages/s2/CapabilityImportPage.tsx#L271`） | `#0F6E56` 是 4 个页面擅自用的深绿色，**不是品牌色**（tokens.css 品牌色是 `#2B6CB0`/`#22d3ee` 蓝青系） | 替换为 `var(--aos-accent)`（见 §2.1 T1） |
| 灰阶 hex 硬编码 **1043 行** | 见 §6.5 详细分布 | `#6B7280`(327) / `#E5E7EB`(292) / `#9CA3AF`(178) / `#111827`(151) / `#F3F4F6`(95) 等，主题切换不联动 | 分批 token 化（见 §6.5） |
| BpArchitectureBar 悬空 | BpArchitectureBar.tsx（`aos-platform/apps/web/src/components/bp/BpArchitectureBar.tsx`） | 组件已开发+导出+有测试，但**0 个业务页面接入** | 224 的 P1 任务：接入模型管理 3 页 |
| ModelCatalogPage 手写架构条 | ModelCatalogPage.tsx:328,363-457（`aos-platform/apps/web/src/pages/s2/ModelCatalogPage.tsx#L328`） | 手写了一个不兼容版本（`number` 类型 + 层顺序与组件相反） | 替换为 `<BpArchitectureBar activeLayer="L3" />` |
| ProvidersPage 无架构条 | aip.tsx:641（`aos-platform/apps/web/src/pages/s2/aip.tsx#L641`） | 完全没有架构条 | 新增 `<BpArchitectureBar activeLayer="L1" />` |
| ModelRouterPage 无架构条 | aip.tsx:1750（`aos-platform/apps/web/src/pages/s2/aip.tsx#L1750`） | 完全没有架构条 | 新增 `<BpArchitectureBar activeLayer="L2" />` |

### 9.3 已确认功能就绪的页面（224 仅做样式规整）

| 页面 | 功能 | 确认结果 | 224 工作 |
|-----|------|---------|---------|
| 画布编辑器 CanvasPage.tsx（`aos-platform/apps/web/src/pages/CanvasPage.tsx`） | 模块/工作流/预览三态切换 | ✅ 已实现（`canvasMode` 状态 + WorkflowMode 组件） | 仅样式对齐 |
| AIP 逻辑画布 LogicCanvasPage.tsx（`aos-platform/apps/web/src/pages/s2/LogicCanvasPage.tsx`） | 分支节点 + 汇聚节点 | ✅ 已实现（`branch` + `handoff` 两种 BlockKind） | 仅样式对齐 |

### 9.4 BpArchitectureBar 接入注意事项

接入前需处理以下不一致点：

| 不一致项 | 当前状态 | 目标状态 |
|---------|---------|---------|
| 层语义顺序 | ModelCatalogPage 手写版 L1=目录/L2=供应商/L3=路由（与组件相反）| 统一为 BpArchitectureBar 默认：L1=供应商/L2=路由/L3=目录 |
| activeLayer 类型 | ModelCatalogPage 用 `number`（0/1/2/3）| 统一为 `"L1"|"L2"|"L3"|"AIP"` 字符串字面量 |
| 视觉风格 | ModelCatalogPage 手写版 4 种 tone 颜色 | 统一为 BpArchitectureBar 的蓝色高亮 + 灰色非活跃 |

### 9.5 灰阶 hex 硬编码治理（最大规模残留项）

> 全站 .tsx/.ts 文件硬编码 hex 颜色 **3473 处**（6位 3153 + 3位 317），其中灰阶系列 **1043 行**是重灾区，主题切换时全部失效。这是 Phase 6 未完成的最大的技术债。

#### 9.5.1 灰阶颜色映射表（优先治理）

| 硬编码值 | 命中行数 | 语义 | 目标 Token（tokens.css 已有）|
|---------|---------|------|------------------------------|
| `#6B7280` | 327 | 次级文字 / 图标 | `var(--aos-text-secondary)` |
| `#E5E7EB` | 292 | 边框 / 分隔线 | `var(--aos-border)` |
| `#9CA3AF` | 178 | 占位符 / 禁用态 | `var(--aos-text-tertiary)` |
| `#111827` | 151 | 主文字 | `var(--aos-text)` |
| `#F3F4F6` | 95 | 次级背景 | `var(--aos-surface)` |
| `#D1D5DB` | 61 | 输入框边框 | `var(--aos-border-strong)` |
| `#1F2937` | 27 | 深色标题 | `var(--aos-text)` |
| **小计** | **1131** | — | — |

#### 9.5.2 强调色与状态色映射表

| 硬编码值 | 命中行数 | 语义 | 目标 Token |
|---------|---------|------|-----------|
| `#3B82F6` | 75 | 蓝色强调（链接/选中）| `var(--aos-accent)` |
| `#0F6E56` | 8 | 错误的深绿品牌色 | `var(--aos-accent)`（见 §2.1 T1）|
| `#22d3ee` | 1 | 深色品牌色误用 | `var(--aos-accent)` |

#### 9.5.3 治理优先级（按命中行数倒序）

| 优先级 | 治理目标 | 文件数 | 命中行数 | 策略 |
|-------|---------|--------|---------|------|
| **P0** | `#6B7280` → `--aos-text-secondary` | 36 | 327 | 全局批量替换 + 视觉回归 |
| **P0** | `#E5E7EB` → `--aos-border` | 33 | 292 | 全局批量替换 + 视觉回归 |
| **P0** | `#9CA3AF` → `--aos-text-tertiary` | 31 | 178 | 全局批量替换 + 视觉回归 |
| **P0** | `#111827` → `--aos-text` | 19 | 151 | 全局批量替换 + 视觉回归 |
| **P1** | `#F3F4F6` → `--aos-surface` | 28 | 95 | 批量替换 |
| **P1** | `#3B82F6` → `--aos-accent` | 29 | 75 | 批量替换（注意确认是否真的强调色）|
| **P1** | `#D1D5DB` → `--aos-border-strong` | 20 | 61 | 批量替换 |
| **P2** | `#0F6E56` → `--aos-accent` | 4 | 8 | 替换（非品牌色，见 §2.1 T1）|
| **P2** | `#1F2937` → `--aos-text` | 13 | 27 | 批量替换 |

#### 9.5.4 重点治理文件（硬编码密度 Top 10）

| 排名 | 命中行数 | 文件路径 |
|-----|---------|---------|
| 1 | 333 | AgentImportPage.tsx（`aos-platform/apps/web/src/pages/s2/AgentImportPage.tsx`） |
| 2 | 193 | LogicPage.tsx（`aos-platform/apps/web/src/pages/LogicPage.tsx`） |
| 3 | 157 | CapabilityImportPage.tsx（`aos-platform/apps/web/src/pages/s2/CapabilityImportPage.tsx`） |
| 4 | 154 | AgentsPage.tsx（`aos-platform/apps/web/src/pages/s2/AgentsPage.tsx`） |
| 5 | 144 | ModelCatalogPage.tsx（`aos-platform/apps/web/src/pages/s2/ModelCatalogPage.tsx`） |
| 6 | 123 | DocumentIntelligencePage.tsx（`aos-platform/apps/web/src/pages/s2/DocumentIntelligencePage.tsx`） |
| 7 | 117 | CapacityPage.tsx（`aos-platform/apps/web/src/pages/s2/CapacityPage.tsx`） |
| 8 | 113 | StylesPage.tsx（`aos-platform/apps/web/src/pages/s2/StylesPage.tsx`） |
| 9 | 110 | EventsPage.tsx（`aos-platform/apps/web/src/pages/s2/EventsPage.tsx`） |
| 10 | 100 | StudioPage.tsx（`aos-platform/apps/web/src/pages/StudioPage.tsx`） |

> Top 10 文件合计 1540 行，占全站总量约 44%。建议优先治理这 10 个文件，收益最大。

#### 9.5.5 治理原则

1. **只换 CSS 属性值**：替换 hex → `var(--token)`，不改 JSX 结构、不改 className、不改业务逻辑
2. **逐色验证**：每完成一个颜色的全站替换，立即跑视觉回归（深浅双主题截图对比）
3. **保留必要硬编码**：图表色板、渐变中间色等无对应 token 的，**不在本次治理范围**
4. **新增 lint 规则**：治理完成后在 ESLint/Stylelint 增加 `no-hex-color` 规则，防止回潮

---

## 10. 实施策略与优先级

### 10.1 实施原则

| 原则 | 说明 |
|-----|------|
| **功能不动** | 样式规整只调整CSS/组件样式，不改业务逻辑、API、数据结构 |
| **渐进式** | 从全局Token到公共组件，再到各页面，分批实施，每批验证 |
| **验证优先** | 每批规整后跑视觉回归，确保不误伤功能 |
| **用户反馈** | 关键页面规整后收集用户反馈，确认体验提升 |

### 10.2 实施优先级

| 优先级 | 规整内容 | 理由 | 预计工作量 |
|-------|---------|------|-----------|
| **P0** | 灰阶 hex 治理 P0 批次（4 色 948 行：`#6B7280`/`#E5E7EB`/`#9CA3AF`/`#111827`） | 主题切换全失效，影响最广，收益最大 | 2-3天 |
| **P0** | 8 处 `#0F6E56` 硬编码替换为 `var(--aos-accent)` | 错误的深绿色，非品牌色 | 0.5天 |
| **P0** | 按钮体系 + 卡片体系 + 表格体系样式对齐 | 最常用组件，一致性收益最大 | 3-5天 |
| **P0** | WikiDetailPage 73 处硬编码治理（本体） | 全站单文件硬编码之最，主题切换全失效 | 2-3天 |
| **P0** | WikiIndexPage 整体重构（本体） | 唯一完全脱离 Bp 体系的页面 | 2-3天 |
| **P1** | 三层架构条接入（模型管理3页） | 组件已开发，仅需接入3页 + 处理不一致点 | 1-2天（组件已有，工作量减少） |
| **P1** | 灰阶 hex 治理 P1 批次（3 色 231 行：`#F3F4F6`/`#3B82F6`/`#D1D5DB`） | 次级影响，主题切换失效 | 1-2天 |
| **P1** | 重点文件治理 Top 10（共 1540 行）| 占总量 44%，集中收益 | 3-4天 |
| **P1** | ActionTypeEditorPage 37 处 + LinkTypeEditorPage 32 处（本体） | 编辑器类硬编码重灾区 | 2-3天 |
| **P1** | data.tsx 16 处 + pipelineCanvas.tsx 10 处直接写死（管道） | 非 fallback 形式，主题切换失效 | 2-3天 |
| **P0** | DocumentIntelligencePage 样式规整（数据源） | OCR 提取 + 四态审核流是保留功能，约 123 处硬编码 + 不用 Bp 组件体系 | 3-5天 |
| **P1** | 页面头部 + 面包屑统一 | 每页入口信息结构一致 | 2-3天 |
| **P1** | 工作台核心3页（应用列表/画布/组件注册表） | 工作台是主入口，用户接触最多 | 4-6天 |
| **P2** | DataSourceCreatePage + MediaSetsPage 各约 10 处（数据源） | 5 步向导 + 分类色板 | 1-2天 |
| **P2** | dataSchedules.tsx 11 处图表色（管道） | 状态色需 token 化 | 0.5-1天 |
| **P2** | PropertyEditorPage 10 处 + FunctionEditorPage 10 处（本体） | 量级可控 | 1-2天 |
| **P2** | DataHealthPage 死代码清理（管道） | data.tsx:606 版本未使用 | 0.5天 |
| **P2** | AIP核心4页（助手/对话机器人/逻辑画布/目录） | AIP是核心能力展示窗口 | 5-7天 |
| **P2** | 模型管理剩余页（供应商/路由/容量） | 模型管理完整性 | 3-4天 |
| **P2** | 其他页面渐进规整 | 长尾页面，影响较小 | 持续进行 |

### 10.3 风险与缓解

| 风险 | 影响 | 缓解措施 |
|-----|------|---------|
| 样式调整影响功能布局 | 中 | 每批调整后做全量功能回归测试 |
| 组件样式改动面太大 | 中 | 从共享组件入手，分批推进，每批范围可控 |
| 视觉稿与实际功能有冲突 | 高 | **功能优先**，样式为功能服务。如视觉稿设计与功能逻辑冲突，先确认产品意图，再决定是否调整样式或功能 |
| 用户习惯改变 | 低 | 关键调整提前通知，提供切换过渡期 |

---

## 11. 验收标准

### 11.1 样式规整验收清单

- [ ] 全站品牌色走 `var(--aos-accent)` token，无 `#0F6E56` 硬编码残留
- [ ] 灰阶 hex 治理完成（`#6B7280`/`#E5E7EB`/`#9CA3AF`/`#111827`/`#F3F4F6`/`#D1D5DB` 共 948+ 行全部 token 化）
- [ ] 深浅主题切换后所有文字/边框/背景颜色正确联动
- [ ] 按钮体系6种类型全部可用，样式一致
- [ ] 卡片/表格/Tab/Badge 等公共组件样式统一
- [ ] 页面头部 + 面包屑结构一致
- [ ] 模型管理3页三层架构条完整（使用 BpArchitectureBar 组件，非手写），跳转正确
- [ ] 工作台核心页面布局与视觉稿对齐
- [ ] AIP核心页面布局与视觉稿对齐
- [ ] 本体：WikiDetailPage 73 处硬编码 + WikiIndexPage 重构完成，接入 Bp 体系
- [ ] 本体：Action/Link/Property/Function 4 个编辑器硬编码全部 token 化
- [ ] 管道：data.tsx + pipelineCanvas.tsx 直接写死硬编码全部 token 化
- [ ] DocumentIntelligencePage 样式规整完成（接入 Bp 组件体系 + 123 处硬编码 token 化 + 四态状态机样式统一）
- [ ] 数据源：DataSourceCreatePage + MediaSetsPage 硬编码 token 化
- [ ] 所有页面功能完整可用，样式调整未破坏功能
- [ ] 深色/浅色主题下样式均正常
- [ ] 关键页面截图对比视觉稿，差异在可接受范围内

### 11.2 功能完整性验证

- [ ] 所有现有API调用正常
- [ ] 所有表单提交正常
- [ ] 所有页面导航跳转正常
- [ ] 所有数据展示正确（数量、排序、筛选）
- [ ] 所有交互操作正常（点击、输入、拖拽）

---

## 12. 配套文档

- [220-AOS整体技术方案](./20-AOS整体技术方案.md)
- [222-产品补充说明](./222-产品补充说明.md)
- [223-plan](./223-plan.md)（全站UI对齐开发计划）
- [T-UI-前端工程与foundry-html落地规范](./T-UI-前端工程与foundry-html落地规范.md)
- [80-蓝图按钮体系与复杂交互页层次规范](./80-蓝图按钮体系与复杂交互页层次规范.md)
- [38-T-UI-壳与蓝图视觉对齐方案](./38-T-UI-壳与蓝图视觉对齐方案.md)
