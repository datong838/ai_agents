# 前端各菜单区「视觉稿对齐 + 测试数据驱动」实施方案

> 文档版本：v2.0（2026-07-26）
> 用户决策：工作台 6 页全做；后端按需大改；订单管理按视觉稿做成"活的"暗色画布编辑器；测试数据不限量。
> 配套规则：先方案再编码 / 最小更改 / 不影响已有功能 / 测试数据驱动（数据来自 dev-org/dev-project）。

---

## 0. 适用 Rules 与术语

- 用中文输出
- 优先查 Rules / 文档，不直接动代码
- 涉及新增/修改代码 → 输出具体文件目录
- 改动遵循「最小更改 + 不破坏已有功能/数据」
- 「测试数据驱动」= 数据来自 `dev-org` / `dev-project` 测试组织，**接口/逻辑必须与线上一致，禁止 mock 兜底**

术语：
- **视觉稿**：`docs/palantier/foundry/html/*.html`（共 73 个，Demo v1.6.5）
- **现状实现**：`aos-platform/apps/web/src/pages/**/*.tsx`
- **后端 API**：`aos-platform/services/aos-api/aos_api/`

---

## 1. 任务目标

1. **全量盘点**每个菜单区"视觉稿 vs 现状"差距（已完成）
2. **工作台 6 页全做**：测试数据驱动 + 视觉稿对齐的真实产品功能
3. **订单管理做成"活的"**：根据应用程序构建工具构建出来的暗色画布编辑器，不是写死的
4. 测试数据：dev-org/dev-project 按需任意写入数据库，不限制
5. **核心原则**：Module 是在线定制出来的，不是写代码写出来的。4 个应用（订单管理、风险告警管理、态势大屏、Buddy 智能助手）就是可定制的 4 个 Module。
6. 完成后按相同范式推进其他菜单区

---

## 1.5 Module 在线定制架构设计

### 核心理念

```
┌─────────────────────────────────────────────────────────────────┐
│                    工作台 · 应用列表                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
│  │订单管理  │  │风险告警  │  │态势大屏  │  │Buddy    │  +新建    │
│  │系统    │  │管理     │  │         │  │智能助手 │          │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘          │
│       │            │            │            │                  │
│       ▼            ▼            ▼            ▼                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │            Module 在线定制系统（低代码平台）           │       │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │       │
│  │  │创建应用  │ │画布编辑  │ │组件注册  │ │变量管理│ │       │
│  │  │向导     │ │器       │ │表       │ │器     │ │       │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └───┬────┘ │       │
│  │       │            │            │            │       │       │
│  │       ▼            ▼            ▼            ▼       │       │
│  │  ┌──────────────────────────────────────────────┐     │       │
│  │  │           运行态渲染引擎                      │     │       │
│  │  │  根据 widgets 配置 → 动态渲染 UI 组件         │     │       │
│  │  └──────────────────────────────────────────────┘     │       │
│  └─────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

### Module 数据模型（后端）

```
meta_module 表：
┌──────────────┬──────────────┬──────────────────────────────┐
│ 字段         │ 类型         │ 说明                         │
├──────────────┼──────────────┼──────────────────────────────┤
│ id           │ TEXT         │ 主键，如 mod-order-xxx       │
│ name         │ TEXT         │ 模块名称                     │
│ status       │ TEXT         │ draft / published            │
│ description  │ TEXT         │ 描述                         │
│ category     │ TEXT         │ 运营 / 分析 / AI 助手 / 风控 / 本体前端 / 态势感知 / 智能嵌入 / 系统集成 │
│ theme        │ TEXT         │ light / dark                 │
│ objectType   │ TEXT         │ 绑定的对象类型               │
│ entryPath    │ TEXT         │ 运行态入口路径               │
│ widgets      │ JSONB        │ 组件配置数组                 │
│ buddyBound   │ BOOLEAN      │ 是否绑定 Buddy               │
│ lastOpenedAt │ TIMESTAMPTZ  │ 最后打开时间                 │
│ createdAt    │ TIMESTAMPTZ  │ 创建时间                     │
│ orgId        │ TEXT         │ 组织 ID                     │
│ projectId    │ TEXT         │ 项目 ID                     │
└──────────────┴──────────────┴──────────────────────────────┘
```

### Widget 组件系统

| Widget ID | 名称 | 描述 | 配置参数 |
|---|---|---|---|
| `table` | 表格 | 数据表格 | columns, filters, sort, pagination |
| `chart` | 图表 | 趋势图/柱状图 | type, dataSource, dimensions, measures |
| `stats` | 统计卡片 | KPI 数字卡片 | title, value, trend, color |
| `details` | 详情面板 | 对象详情 | fields, layout |
| `filters` | 筛选器 | 条件筛选 | fields, operators |
| `graph` | 图谱 | 对象关系图 | nodeTypes, linkTypes |
| `chat` | 聊天 | AI 对话 | model, context, history |
| `canvas` | 画布 | 低代码画布 | layout, widgets |
| `kpi` | KPI 面板 | 大屏 KPI | value, unit, trend, color |
| `map` | 地图 | 供应链网络 | nodes, edges, zoom |
| `events` | 事件流 | 实时事件 | events, filters |

### 4 个预置 Module 配置

#### 1. 订单管理系统（mod-order-management）
```json
{
  "category": "运营",
  "theme": "dark",
  "widgets": [
    {"type": "stats", "id": "total-orders", "title": "今日订单", "dataSource": "Order", "aggregation": "count"},
    {"type": "stats", "id": "total-amount", "title": "今日成交额", "dataSource": "Order", "aggregation": "sum", "field": "amount"},
    {"type": "stats", "id": "pending", "title": "待发货", "dataSource": "Order", "aggregation": "count", "filter": {"status": "pending"}},
    {"type": "stats", "id": "refund", "title": "退款率", "dataSource": "Order", "aggregation": "percent", "filter": {"status": "refunded"}},
    {"type": "table", "id": "order-table", "dataSource": "Order", "columns": ["orderNo", "customer", "amount", "status", "createdAt"]},
    {"type": "chart", "id": "trend-chart", "dataSource": "Order", "type": "line", "xAxis": "date", "yAxis": "amount"},
    {"type": "details", "id": "order-details", "dataSource": "Order", "fields": ["orderNo", "customer", "items", "amount", "status", "address"]}
  ]
}
```

#### 2. 风险告警管理（mod-ops-inbox）
```json
{
  "category": "风控",
  "theme": "light",
  "widgets": [
    {"type": "filters", "id": "risk-filters", "fields": ["status", "priority", "date"]},
    {"type": "table", "id": "risk-table", "dataSource": "WorkOrder", "columns": ["orderNo", "issue", "shop", "level", "status"]},
    {"type": "details", "id": "risk-details", "dataSource": "WorkOrder", "fields": ["riskScore", "riskFactors", "actions"]},
    {"type": "events", "id": "activity-log", "dataSource": "ActivityLog"}
  ]
}
```

#### 3. 态势大屏（mod-cop-dashboard）
```json
{
  "category": "态势感知",
  "theme": "dark",
  "widgets": [
    {"type": "kpi", "id": "in-transit", "title": "在途订单", "dataSource": "Order", "filter": {"status": "shipped"}},
    {"type": "kpi", "id": "stockout", "title": "缺货 SKU", "dataSource": "Product", "filter": {"stock": 0}},
    {"type": "kpi", "id": "turnover", "title": "周转天数", "dataSource": "Inventory"},
    {"type": "kpi", "id": "risk-factories", "title": "风险工厂", "dataSource": "Factory", "filter": {"riskLevel": "high"}},
    {"type": "map", "id": "supply-map", "dataSource": "SupplyChain"},
    {"type": "events", "id": "real-time-events", "dataSource": "SystemEvents"}
  ]
}
```

#### 4. Buddy 智能助手（mod-buddy-assist）
```json
{
  "category": "AI 助手",
  "theme": "light",
  "widgets": [
    {"type": "table", "id": "workorder-table", "dataSource": "WorkOrder", "columns": ["orderNo", "status", "riskScore"]},
    {"type": "chat", "id": "buddy-chat", "model": "default", "context": ["Selection", "Ontology"]},
    {"type": "filters", "id": "workorder-filters", "fields": ["status", "riskScore"]}
  ]
}
```

### 创建应用向导流程（4 步）

```
Step 1: 基本信息
├── 模块名称（必填）
├── 模块标识（slug，自动生成，可编辑）
├── 图标选择器（6 个预设图标）
├── 业务域（chip 选择：运营/分析/风控/供应链/AI/其他）
└── 用途描述（可选）

Step 2: 数据绑定
├── 对象类型树（左侧：选择绑定的 ObjectType）
├── 属性 chips（右侧：勾选要展示的属性）
└── 权限提示（public/restricted）

Step 3: 模板选择
├── 空白模板
├── 表格列表模板（table + filters）
├── 仪表盘模板（stats + chart + table）
└── 对象探索模板（graph + table + filters）

Step 4: 确认创建
├── 信息汇总表
├── "创建后自动执行"清单（同步配置、权限设置、发布检查）
└── 创建按钮 → 跳转到画布编辑器
```

---

## 2. 视觉稿全量盘点（73 个 HTML → 10 个分区）

| # | 分区 | 视觉稿数 | 代表性文件 |
|---|---|---|---|
| 1 | 概览 | 1 | `index.html` |
| 2 | **工作台** | 6 | `workshop.html` / `workshop-create.html` / `workshop-module.html` / `workshop-app-order.html` / `workshop-cop.html` / `workshop-aip-chat.html` |
| 3 | 应用程序构建工具 | 7 | `workshop-canvas.html`（145KB）/ `workshop-widget-registry.html` / `workshop-variables.html` / `workshop-styles.html` / `workshop-module-interface.html` / `workshop-events.html` / `workshop-publish.html` |
| 4 | AIP 决策引擎（5 子组） | 14 | `aip-assist.html` / `agents.html` / `aip-analyst.html` / `aip-logic.html` / `aip-tools.html` / `aip-maturity.html` / `agent-registry.html` / `aip-capabilities.html` / `aip-evals.html` / `aip-draft-inbox.html` / `aip-decision-lineage.html` / `aip-observability.html` |
| 5 | 模型管理 | 4 | `aip-model-catalog.html` / `aip-model-providers.html` / `aip-model-router.html` / `aip-capacity-management.html` |
| 6 | 本体·数字孪生 | 9+7 | `ontology.html` / `workshop-object-view.html` / `ontology-funnel.html` / `ontology-graph-health.html` / `ontology-wiki-index.html` / `ontology-wiki.html` / `funnel.html` / `okf-funnel.html` / `ontology-branches.html`（+ 7 个二级详情页） |
| 7 | 管道与数据治理 | 9 | `pipeline-list.html` / `pipeline-proposals.html` / `schedules.html` / `builds.html` / `dataset.html` / `code-repositories.html` / `lineage.html` / `health.html` / `pipeline.html` / `pipeline-doc-intel.html` |
| 8 | 数据源与同步 | 6+2 | `data-connection.html` / `data-connection-agents.html` / `sync.html` / `sync-routing.html` / `media-sets.html` / `document-intelligence.html`（+ `source-new.html` / `source-detail.html`） |
| 9 | 运维交付 Apollo | 8 | `apollo-hub.html` / `apollo-release.html` / `apollo-spoke.html` / `apollo-ferry.html` / `apollo-assets.html` / `apollo-change-mgmt.html` / `apollo-config.html` / `integration-cases.html` |

**全局设计语言**：
- 主字号 **13px**，tracking-tight；标题 13px font-medium，描述 13px gray-600，meta 11px gray-500，cta 10px
- 品牌主色 `#0F6E56`（深绿），hover `#085041`
- panel 容器 `.aos-panel`（白底圆角 p-5）
- module 卡片 `.aos-module-card`（group-hover 文字变蓝）
- 类型 eyebrow 多色：blue-700 业务应用 / blue-700 风控 / purple-700 本体前端 / yellow-600 智能嵌入

---

## 3. 工作台区 6 页深度差距清单

### 3.1 差距总览表

| # | 页面 | 视觉稿 | 现状 | 差距分 | 数据驱动 | 关键差距摘要 |
|---|---|---|---|---|---|---|
| 1 | 应用列表 | `workshop.html` | `WorkshopListPage.tsx` | **中** | ✅ 真实 API | 缺「最近使用」分区 + 卡片双链接；品牌色未应用 |
| 2 | 创建应用 | `workshop-create.html` | `s2/WorkshopCreatePage.tsx` | **高** | ✅ 真实 API | 左侧垂直步骤导航 + 图标/业务域/slug/对象树/属性 chips/模板预览 **全缺**；主色错（蓝 vs 绿） |
| 3 | 风险告警 Inbox | `workshop-module.html` | `InboxPage.tsx` | **中** | ✅ 真实 API+幂等 | 缺 Top bar 版本徽章 + Filter 优先级/日期组 + 活动日志 |
| 4 | 订单管理 | `workshop-app-order.html` | `s2/OrderManagementPage.tsx` | **高** | ✅ 真实 API+Action | **定位错配**（视觉稿=暗色画布编辑器，现状=浅色运行态） |
| 5 | 态势大屏 COP | `workshop-cop.html` | `s2/extras.tsx:CopPage` | **中** | ⚠️ 半驱动 | KPI 偏技术；工厂/事件列表仍 mock |
| 6 | Buddy 助手 | `workshop-aip-chat.html` | `BuddyPage.tsx` | **低** | ✅ 真实 API | 表用 WorkOrder 非 Order；缺"风控分"列；布局基本对齐 |

**整体观察**：6 页**全部已接入真实 API**（视觉稿都是静态 HTML），数据层优于视觉稿；差距集中在**布局结构**、**关键交互组件缺失**、**视觉品牌色**。

---

### 3.2 后端 API 现状（关键约束）

| 接口 | 状态 | 关键问题 |
|---|---|---|
| `GET /v1/modules` | ✅ 真实存在 | 返回 `{items:[…], store:"postgres"}`，dev-org 种子 3 条 |
| `POST /v1/modules` | ✅ 真实存在 | 接受 `name(必填) / description / objectType / markings / entryPath / widgets / buddyBound` |
| `PATCH /v1/modules/{id}` | ✅ 真实存在 | 同上字段 |
| `/v1/orders` | ❌ **不存在** | 订单仅作为 `Order`/`OrderItem` ObjectType 的种子 obj_instance，无专属 REST |
| `/v1/inbox` | ❌ **不存在** | alerts 类接口都在 `/api/...`，与工作台风控无关 |

**Module 实体字段缺失**（视觉稿需要的 2 个字段都没有）：
1. **无 `category` 字段** → 无法支撑视觉稿"全部/运营/分析/AI 助手"分类筛选
2. **无 `openedAt` / `lastOpenedAt` 字段** → 无法支撑视觉稿"最近使用"按打开时间排序

---

## 4. 分批改造方案

### Phase A — 工作台 6 页全做（本批次）

**目标**：工作台 6 页全部按视觉稿对齐，测试数据驱动的真实产品功能。

**范围**：应用列表、创建应用、风险告警 Inbox、订单管理（暗色画布编辑器）、态势大屏 COP、Buddy 助手。

**核心原则**：
- 订单管理做成**活的**：根据应用程序构建工具构建出来的，不是写死的
- 测试数据不限量：dev-org/dev-project 按需写入数据库

#### Phase A 任务拆解（WBS）

##### A. 后端改造

| 任务 | 文件 | 改动类型 | 风险 |
|---|---|---|---|
| A1. module 表新增 `category` / `last_opened_at` / `theme` / `widgets` 列 | `services/aos-api/aos_api/module_store.py` | 表 DDL + ensure_module_schema | 低 |
| A2. `CreateModuleRequest` / `PatchModuleRequest` 增加 `category` / `theme` / `widgets` | `services/aos-api/aos_api/routers/modules.py` | Schema 扩展 | 低 |
| A3. `_row_to_mod` 输出 `category` + `lastOpenedAt` + `theme` + `widgets` | `services/aos-api/aos_api/module_store.py` | 序列化 | 低 |
| A4. 新增 `POST /v1/modules/{id}/touch` 接口 | `services/aos-api/aos_api/routers/modules.py` | 新接口 | 低 |
| A5. 新增 `GET /v1/modules/{id}/runtime` 接口（运行态数据） | `services/aos-api/aos_api/routers/modules.py` | 新接口 | 低 |
| A6. 种子数据扩展到 9 条 + 订单/风控/对象实例数据 | `services/aos-api/aos_api/demo/module_seed.py` | seed 扩展 | 低 |

##### B. 前端改造

| 任务 | 文件 | 改动类型 | 风险 |
|---|---|---|---|
| B1. 应用列表页重写（最近使用+全部应用+双链接+品牌色） | `apps/web/src/pages/WorkshopListPage.tsx` | 重构 | 中 |
| B2. 创建应用补齐（左侧垂直步骤+图标/业务域/slug/对象树/属性chips/模板预览） | `apps/web/src/pages/s2/WorkshopCreatePage.tsx` | 重构 | 中 |
| B3. 风险告警 Inbox 补齐（Top bar+优先级日期Filter+活动日志） | `apps/web/src/pages/InboxPage.tsx` | 改造 | 中 |
| B4. 订单管理重写成暗色画布编辑器（左接口列+中画布+右属性面板+工具栏） | `apps/web/src/pages/s2/OrderManagementPage.tsx` | **重写** | 高 |
| B5. 态势大屏 COP 补齐（KPI业务化+工厂/事件接入真实数据） | `apps/web/src/pages/s2/extras.tsx:CopPage` | 改造 | 中 |
| B6. Buddy 助手补齐（风控分列+表格列头对齐） | `apps/web/src/pages/BuddyPage.tsx` | 改造 | 低 |
| B7. CSS 新增 `.aos-panel` / `.aos-module-card` / 暗色主题 / 品牌色变量 | `apps/web/src/styles.css` | 样式 | 低 |
| B8. 前端 API 类型扩展（含 category/lastOpenedAt/theme/widgets） | `apps/web/src/lib/api.ts` | 类型 | 低 |

##### C. 测试数据

| 任务 | 文件 | 改动类型 | 风险 |
|---|---|---|---|
| C1. 9 条 module 种子（覆盖运营/分析/AI助手/风控/本体前端/智能嵌入等分类） | `services/aos-api/aos_api/demo/module_seed.py` | seed | 低 |
| C2. 订单数据（20 条 Order + OrderItem） | `services/aos-api/aos_api/demo/order_seed.py` | seed | 低 |
| C3. 风控告警数据（10 条） | `services/aos-api/aos_api/demo/risk_seed.py`（新建） | seed | 低 |
| C4. 对象实例数据（WorkOrder/Order/Agent 等） | `services/aos-api/aos_api/demo/object_seed.py`（新建） | seed | 低 |

#### Phase A 各页视觉稿对齐细节

##### 1. 应用列表（workshop.html）

| 块 | 视觉稿 | 改造方向 |
|---|---|---|
| B1 标题区 | 标题"应用列表"（13px）+ 描述 + 绿色「+ 新建 Module」按钮 | 字号 13px；按钮改 `#0F6E56` |
| B2 最近使用 panel | 独立 .aos-panel + grid 3 列 + 双链接 | 新增：`lastOpenedAt` 排序 Top 3；卡片含双链接 |
| B3 全部应用 panel | 独立 .aos-panel + 标题右侧 4 Tab（全部/运营/分析/AI助手）+ grid 3 列 | 套 panel；Tab 改为 category 维度 |
| B4 卡片样式 | eyebrow（11px 多色）+ 应用名（13px）+ 描述（11px）+ 双链接 | 加 eyebrow（按 category 上色）+ 双链接 |

##### 2. 创建应用（workshop-create.html）

| 块 | 视觉稿 | 改造方向 |
|---|---|---|
| B1 左侧垂直步骤导航 | 高亮绿 `#0F6E56` + 对勾已完成态 + 蓝色提示框 | 新增左侧导航 |
| B2 Step1 | 模块名称 / 模块标识（slug 自动生成）/ 6 个图标选择器 / 业务域 chip | 补齐所有组件 |
| B3 Step2 | 对象类型树（左）+ 属性 chips（右）+ 权限提示 | 补齐对象树和属性 chips |
| B4 Step3 | 2×2 模板卡（空白/表格列表/仪表盘/对象探索）+ 预览缩略图 | 补齐模板预览图 |
| B5 Step4 | 信息汇总表 + "创建后自动执行"清单 | 补齐清单 |

##### 3. 风险告警 Inbox（workshop-module.html）

| 块 | 视觉稿 | 改造方向 |
|---|---|---|
| B1 Top bar | 模块名 + 版本徽章 + 「编辑模块 / 返回列表」 | 新增 |
| B2 左 Filter | 状态 / 优先级 / 日期 三组 checkbox + Object Set Filter | 补齐优先级和日期分组 |
| B3 中 Table | 订单号 / 问题 / 店铺 / 等级，选中行左蓝边 | 列头对齐 |
| B4 右 Object View | 风控分大数字 + 属性 grid + Wiki 黄底卡 + Actions + 活动日志时间线 | 补齐活动日志 |

##### 4. 订单管理 — 暗色画布编辑器（workshop-app-order.html）⭐ 重点

| 块 | 视觉稿 | 改造方向 |
|---|---|---|
| B1 暗色主题 | `#1A1A2E` + `p-ws-dark` | 全局暗色主题 |
| B2 三栏布局 | 左 280px「模块接口/参数/事件处理/函数」面板 + 中画布 + 右「属性面板」 | 三栏布局 |
| B3 Topbar | 模块/预览切换 + 保存 / 发布按钮 | 新增 |
| B4 工具栏 + 4 个 pop-panel | 添加微件 grid（12 个 widget）、布局、变量、事件 | 补齐全部 |
| B5 中画布 | 4 统计卡片 + 订单表格 + 趋势 SVG + 详情卡 | 动态渲染（从 widgets 配置） |

##### 5. 态势大屏 COP（workshop-cop.html）

| 块 | 视觉稿 | 改造方向 |
|---|---|---|
| B1 KPI 行 | 在途订单 / 缺货 SKU / 周转天数 / 风险工厂 | KPI 业务化 |
| B2 主体 | 左 SVG 供应链网络 + 右钻取侧栏 | SVG 地图对齐 |
| B3 底部 | 风险工厂详情 + 实时事件 | 接入真实事件流 |

##### 6. Buddy 助手（workshop-aip-chat.html）

| 块 | 视觉稿 | 改造方向 |
|---|---|---|
| B1 表格列 | 订单号 / 状态 / 风控分💡 / 选中标记 | 补齐风控分列 |
| B2 Assist popover | 流程内提问 + 上下文说明 + AI 回答 | 对齐 |
| B3 右 Buddy 侧栏 | Context chips + 对话 log + 输入框 | 对齐 |

#### Phase A 数据驱动方式

- 列表：`GET /v1/modules?orgId=dev-org` → 返回 9 条种子
- 最近使用：`lastOpenedAt desc` 排序，点击时调用 `/touch`
- 分类筛选：客户端按 `category` 字段过滤
- 订单数据：`GET /v1/objects/Order` + `GET /v1/actions/execute`
- 风控数据：`GET /v1/object-sets/query` + `GET /v1/wiki/WorkOrder/{id}`
- 模块运行态：`GET /v1/modules/{id}/runtime` 返回 widgets 配置

#### Phase A 新增 API 设计

##### 1. `POST /v1/modules/{id}/touch` — 更新最后打开时间

**请求体**：无

**响应**：
```json
{
  "ok": true,
  "moduleId": "mod-order-management",
  "lastOpenedAt": "2026-07-26T10:30:00Z"
}
```

##### 2. `GET /v1/modules/{id}/runtime` — 获取模块运行态配置

**响应**：
```json
{
  "id": "mod-order-management",
  "name": "订单管理系统",
  "category": "运营",
  "theme": "dark",
  "widgets": [
    {"type": "stats", "id": "total-orders", "title": "今日订单", "dataSource": "Order", "aggregation": "count"},
    {"type": "stats", "id": "total-amount", "title": "今日成交额", "dataSource": "Order", "aggregation": "sum", "field": "amount"},
    {"type": "table", "id": "order-table", "dataSource": "Order", "columns": ["orderNo", "customer", "amount", "status", "createdAt"]},
    {"type": "chart", "id": "trend-chart", "dataSource": "Order", "type": "line", "xAxis": "date", "yAxis": "amount"},
    {"type": "details", "id": "order-details", "dataSource": "Order", "fields": ["orderNo", "customer", "items", "amount", "status", "address"]}
  ],
  "dataQueries": [
    {"name": "orders-today", "objectType": "Order", "filter": {"createdAt": {"$gte": "today"}}},
    {"name": "orders-pending", "objectType": "Order", "filter": {"status": "pending"}}
  ]
}
```

##### 3. `POST /v1/modules/{id}/widgets` — 画布编辑器动态添加组件

**请求体**：
```json
{
  "widget": {
    "type": "chart",
    "id": "new-chart",
    "title": "转化率趋势",
    "dataSource": "Order",
    "type": "line",
    "xAxis": "date",
    "yAxis": "conversionRate"
  }
}
```

**响应**：
```json
{
  "ok": true,
  "widgetId": "new-chart",
  "moduleId": "mod-order-management"
}
```

##### 4. `DELETE /v1/modules/{id}/widgets/{widgetId}` — 删除画布组件

**响应**：
```json
{
  "ok": true,
  "deletedWidgetId": "new-chart"
}
```

##### 5. `GET /v1/widget-registry` — 获取可用组件清单

**响应**：
```json
{
  "widgets": [
    {"id": "table", "name": "表格", "category": "数据展示", "icon": "table"},
    {"id": "chart", "name": "图表", "category": "数据展示", "icon": "chart"},
    {"id": "stats", "name": "统计卡片", "category": "数据展示", "icon": "bar-chart"},
    {"id": "details", "name": "详情面板", "category": "数据展示", "icon": "panel"},
    {"id": "filters", "name": "筛选器", "category": "交互", "icon": "filter"},
    {"id": "graph", "name": "图谱", "category": "数据展示", "icon": "network"},
    {"id": "chat", "name": "聊天", "category": "AI", "icon": "message-circle"},
    {"id": "kpi", "name": "KPI 面板", "category": "数据展示", "icon": "trending-up"},
    {"id": "map", "name": "地图", "category": "数据展示", "icon": "map"},
    {"id": "events", "name": "事件流", "category": "实时", "icon": "activity"}
  ]
}
```

#### 运行态渲染引擎设计

**核心逻辑**：前端根据 `widgets` 配置数组，动态渲染对应的 React 组件。

```typescript
// WidgetRenderer.tsx
interface WidgetConfig {
  type: string;
  id: string;
  title?: string;
  [key: string]: unknown;
}

const WIDGET_COMPONENTS: Record<string, React.ComponentType<WidgetProps>> = {
  table: TableWidget,
  chart: ChartWidget,
  stats: StatsWidget,
  details: DetailsWidget,
  filters: FiltersWidget,
  graph: GraphWidget,
  chat: ChatWidget,
  kpi: KpiWidget,
  map: MapWidget,
  events: EventsWidget,
};

export function WidgetRenderer({ widgets }: { widgets: WidgetConfig[] }) {
  return (
    <div className="widget-grid">
      {widgets.map((widget) => {
        const Component = WIDGET_COMPONENTS[widget.type];
        if (!Component) return null;
        return <Component key={widget.id} config={widget} />;
      })}
    </div>
  );
}
```

**暗色主题切换**：
- 视觉稿中订单管理使用暗色主题（`#1A1A2E`）
- 通过 `theme` 字段控制：`dark` → 应用暗色样式类；`light` → 默认浅色

**画布编辑器交互**：
- 左侧面板：拖拽组件到画布
- 中间画布：自由布局 + 组件拖拽排序
- 右侧面板：选中组件时显示属性配置
- 工具栏：添加微件、布局设置、变量管理、事件配置

#### Phase A 验收标准

1. ✅ 6 页视觉与对应 HTML 截图 1:1
2. ✅ 订单管理是"活的"：根据 widgets 配置动态渲染画布
3. ✅ 无 mock 兜底，无控制台 error
4. ✅ 单元测试 + 回归测试通过
5. ✅ 所有数据来自 dev-org/dev-project 真实数据库

---

### Phase B — 应用程序构建工具（7 页）

补全缺失的 3 页（组件注册表、变量管理器、主题与样式）+ 画布编辑器深度对接。

### Phase C — 其他 8 个分区

按用户优先级排序推进。

---

## 5. 风险与影响

| 风险 | 影响 | 缓解 |
|---|---|---|
| module 表新增列 | 老数据 NULL | 用 `ALTER TABLE … ADD COLUMN … NULL` + 序列化时 NULL→默认值 |
| 订单管理重写（暗色画布编辑器） | 工作量大，涉及三栏布局+工具栏+属性面板+微件系统 | 分阶段：先搭框架，再逐块填充；参考 workshop-canvas.html 的架构 |
| 前端整页重写 | 已有 API 调用逻辑可能丢 | 保留 `apiGet/apiPost` 调用，仅改 UI 层 |
| `/touch` 接口被滥用 | 数据库写放大 | fire-and-forget + 客户端节流（同 module 5 分钟内只触一次） |
| 测试数据量大 | dev-org 数据膨胀 | 提供清理脚本，可按需重置 |

---

## 6. 用户已确认事项（决策记录）

| 问题 | 用户决策 |
|---|---|
| Phase A 范围 | 工作台 6 页全做（不是只做应用列表） |
| 后端加字段 | 可以大改，按需加字段 |
| 订单管理定位 | 按视觉稿做成"活的"暗色画布编辑器（左接口列+中画布+右属性面板+工具栏），不是写死的 |
| 测试数据 | 可以任意写，不做限制 |
| 品牌色 | 全局推广 `#0F6E56`（深绿） |
| 改造节奏 | 后续专门写计划（Phase A→B→C→D→E→F 顺序） |
| 缺失页面处理 | **直接做真实页面**，严格按照视觉稿（不用占位页） |
| 名字统一 | **全部按视觉稿改**（8 处名字差异） |
| 本体提案 vs 漏斗管道 | **同义页**，按视觉稿改名"本体提案" |
| OKF funnel | 按视觉稿改名"OKF funnel"（去掉"行业"） |
| Module 核心原则 | Module 是在线定制出来的，不是写代码写出来的；新建 Module 能力必须很强 |

---

## 7. 附录：相关文件清单

### 7.1 视觉稿（参考）
- `/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/workshop.html`
- `/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/workshop-create.html`
- `/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/workshop-module.html`
- `/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/workshop-app-order.html`
- `/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/workshop-cop.html`
- `/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/workshop-aip-chat.html`
- 全局样式：`/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/assets/demo.css`

### 7.2 现状实现（待改）
- `/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/pages/WorkshopListPage.tsx`
- `/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/pages/s2/WorkshopCreatePage.tsx`
- `/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/pages/InboxPage.tsx`
- `/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/pages/s2/OrderManagementPage.tsx`
- `/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/pages/s2/extras.tsx`
- `/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/pages/BuddyPage.tsx`

### 7.3 后端 API（Phase A 待扩）
- `/Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/aos_api/routers/modules.py`
- `/Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/aos_api/module_store.py`
- `/Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/aos_api/demo/module_seed.py`

### 7.4 导航/路由（仅参考）
- `/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/nav.ts`
- `/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/App.tsx`
- `/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/shell/AppShell.tsx`（全局外壳已对齐，不动）
