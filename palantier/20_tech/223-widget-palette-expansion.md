# 223 Widget 调色板扩展方案 · 按视觉稿补齐

> 版本：v1.0（2026-07-27）
> 关联：[223-plan.md](./223-plan.md) · [223-widget-single-source-of-truth.md](./223-widget-single-source-of-truth.md) · [223-canvas-collapsible-sidebars.md](./223-canvas-collapsible-sidebars.md)
> 视觉稿来源：[docs/palantier/foundry/html/](../../foundry/html/) 4 个核心应用
> 影响文件：
> - `aos-platform/apps/web/src/pages/ComponentTreeEditor.tsx`
> - `aos-platform/apps/web/src/pages/ComponentRenderer.tsx`
> - `aos-platform/apps/web/src/pages/widgets/*`（新增目录）
> - `aos-platform/services/aos-api/aos_api/widget_registry.py`

---

## 1. 背景与问题

### 1.1 现状缺陷

当前 `ComponentTreeEditor.tsx` 的 `WIDGET_PALETTE` 只有 **16 种硬编码 widget**（含原 CanvasPage 13 种 CanvasKind + page-layout + horizontal-grid + filter-bar + stat-card + …），但视觉稿（4 个核心应用）实际用到了更多类型，导致：

1. **画布编辑器无法构建出视觉稿里的页面**（如态势大屏的关系图、Buddy 聊天侧栏、风险告警的 Wiki 卡片）
2. 调色板**没有分类**，16 个 widget 平铺，密度高、找起来累
3. 前后端 widget 注册表**未联动**：后端 `widget_registry.py` 9 个 plugin、前端 `WidgetRegistryPage.tsx` 16 个 builtin、Canvas 调色板 16 个硬编码——三套独立维护
4. CanvasPage 旧 CanvasKind（`table/filter/buddy/overlay/action/graph/metric/stub`）在 ComponentRenderer 里落入 `default` 分支，**渲染为"未知组件类型"占位框**

### 1.2 用户诉求

> "要对已知缺少的都要补齐，widget 是插件化增加的，请根据视觉稿里现有的 4 个应用（订单管理、风向告警管理、态势大屏、Buddy 智能助手）列出系统实际缺失的全部 widget 组件"

翻译为产品需求：
- **按视觉稿实际用到的 widget 全部补齐**到调色板
- 调色板要支持**插件化增加**（后续可独立扩展）
- 调色板按**分类**组织，避免平铺混乱
- 每个 widget 都要能**在画布上真实渲染**，不能落入"未知组件"占位

---

## 2. 视觉稿实际用到的 Widget 清单

### 2.1 来源

四个视觉稿 HTML 文件（来自 [docs/palantier/foundry/html/](../../foundry/html/)）：

| 应用 | 视觉稿 | 复杂度 |
|---|---|---|
| 订单管理 | [workshop-app-order.html](../../foundry/html/workshop-app-order.html) | 中（4 KPI + 表 + 折线图 + 详情卡） |
| 风险告警管理 | [workshop-module.html](../../foundry/html/workshop-module.html) | 中（3 栏：筛选 + 表 + 详情+活动） |
| 态势大屏 | [workshop-cop.html](../../foundry/html/workshop-cop.html) | 高（KPI 矩阵 + 关系图 + 钻取面板 + 事件流） |
| Buddy 智能助手 | [workshop-aip-chat.html](../../foundry/html/workshop-aip-chat.html) | 低（双栏：表 + 聊天侧栏） |

### 2.2 实际渲染的 widget 类型（去重）

| # | Widget | order | module | cop | aip-chat | 现有支持 |
|---|---|---|---|---|---|---|
| — | **Layout 容器** |  |  |  |  |  |
| 1 | 页面布局（page-layout） | ✓ | ✓ | ✓ | ✓ | ✓ 已支持 |
| 2 | 水平网格（horizontal-grid） | ✓ | ✓ | ✓ | ✓ | ✓ 已支持 |
| 3 | 页头（page-header） | ✓ | ✓ | ✓ | ✓ | ✓ 已支持 |
| — | **数据展示** |  |  |  |  |  |
| 4 | 统计卡片（stat-card） | ✓×4 |  | ✓×4 |  | ✓ 已支持 |
| 5 | 数据表格（object-table） | ✓ | ✓ |  | ✓ | ✓ 已支持 |
| 6 | 详情抽屉/卡片（detail-drawer） | ✓ | ✓ |  |  | ✓ 已支持 |
| 7 | 状态徽章（status-badge） | ✓ | ✓ |  |  | ✗ **缺失** |
| 8 | Wiki 知识卡片（wiki-card） |  | ✓ |  |  | ✗ **缺失** |
| — | **筛选/操作** |  |  |  |  |  |
| 9 | 筛选栏（filter-bar） | ✓ | ✓ |  |  | ✓ 已支持 |
| 10 | 筛选列表（filter-list） |  | ✓ |  |  | ✗ **缺失**（旧 CanvasKind 走 default） |
| 11 | 按钮组（button-group） |  | ✓ | ✓ |  | ✗ **缺失** |
| — | **图表类** |  |  |  |  |  |
| 12 | 趋势图（trend-chart） | ✓ |  |  |  | ✓ 已支持 |
| 13 | 柱状图（bar-chart） | picker |  |  |  | ✗ **缺失** |
| 14 | 饼图（pie-chart） | picker |  |  |  | ✗ **缺失** |
| 15 | 关系图/拓扑图（network-graph） |  |  | ✓ |  | ✗ **缺失**（核心） |
| 16 | 地图（geo-map） | picker |  | (关系图替代) |  | ✗ **缺失** |
| — | **AI / 协作** |  |  |  |  |  |
| 17 | Buddy Chip（buddy-chip） |  |  |  | ✓ | ✗ 走 default |
| 18 | 聊天侧栏（chat-aside） |  |  |  | ✓ | ✗ **缺失**（核心） |
| 19 | 消息列表（message-log） |  |  |  | ✓ | ✗ **缺失** |
| 20 | 输入框+发送（chat-input） |  |  |  | ✓ | ✗ **缺失** |
| 21 | 上下文 Chip 组（context-chips） |  |  |  | ✓ | ✗ **缺失** |
| 22 | Assist 弹出气泡（assist-popover） |  |  |  | ✓ | ✗ **缺失** |
| — | **时间/事件** |  |  |  |  |  |
| 23 | 时间线（timeline） | picker | (活动日志形似) | (事件流形似) |  | ✗ **缺失** |
| 24 | 事件流（event-stream） |  |  | ✓ |  | ✗ **缺失** |
| 25 | 钻取面板（drill-panel） |  |  | ✓ |  | ✗ **缺失** |
| — | **旧 CanvasKind 兼容** |  |  |  |  |  |
| 26 | Object View · Wiki（overlay） |  | ✓ |  |  | ✗ 走 default |
| 27 | Action 表单（action） |  |  |  |  | ✗ 走 default |
| 28 | 关系图（graph） |  |  |  |  | ✗ 走 default（与 #15 合并） |
| 29 | 指标卡（metric） |  |  |  |  | ✗ 走 default（与 stat-card 合并） |
| 30 | Stub 插件（stub） |  |  |  |  | ✗ 走 default |

### 2.3 注册表已有的扩展 widget（视觉稿未用到，但 WidgetRegistry 已注册）

| Widget | 来源 |
|---|---|
| 看板（kanban） | market |
| 甘特图（gantt） | market |
| 日历（calendar） | market |
| 自定义图表（custom-chart） | custom |

---

## 3. 方案设计

### 3.1 设计原则

| 原则 | 说明 |
|---|---|
| 最小更改 | 不破坏现有 8 个 case，只新增 case 和 widget 文件 |
| 插件化 | 新增 widget 文件独立，ComponentRenderer 通过 switch 注册，便于后续抽出 WidgetPluginRegistry |
| 分类组织 | 调色板按 category 分组（Layout / 数据 / 图表 / AI / Action / 时间） |
| 视觉一致 | 新 widget 复用项目 CSS 变量（`--aos-bg` / `--aos-border` / `--aos-text-muted` 等），不引入额外 UI 库 |
| 数据驱动 | 后端 `widget_registry.py` 与前端调色板保持同步，作为单一来源 |

### 3.2 选型对比

| 方案 | 优点 | 缺点 | 选用 |
|---|---|---|---|
| A. 硬编码到 WIDGET_PALETTE | 实现快 | 每加 widget 都改核心代码，不算"插件化" | ❌ |
| **B. WidgetPluginRegistry 完整插件化** | 真插件化、零侵入扩展、调色板/渲染/属性面板全部从 registry 读 | 改动较大，需重构现有渲染入口与属性面板 | ✅ **本次采用** |
| C. 补 widget 文件 + ComponentRenderer 加 case | 平衡、易回滚 | 仍需改 ComponentRenderer switch | ❌ |

**结论**：本次直接走方案 B（WidgetPluginRegistry）。新增 widget 只要写一个 plugin 文件并在入口注册一次，**调色板 / 属性面板 / 运行态渲染三处零侵入扩展**。

### 3.2.1 WidgetPluginRegistry 接口设计

```ts
// aos-platform/apps/web/src/pages/widgets/registry.ts
export type WidgetCategory =
  | "layout" | "data" | "filter" | "action"
  | "chart" | "ai" | "time" | "extra";

export type PropFieldType = "text" | "number" | "select" | "color" | "textarea";

export interface PropFieldDef {
  key: string;                              // 配置字段名
  label: string;                            // 属性面板显示标签
  type: PropFieldType;
  options?: { label: string; value: string }[];  // 仅 select
  placeholder?: string;
}

export interface WidgetContext {
  components: ComponentTree;                 // 完整组件树（容器需要）
  depth: number;
}

export interface WidgetPlugin {
  type: string;                              // 唯一标识，如 "bar-chart"
  name: string;                              // 调色板显示名
  icon: string;                              // emoji
  category: WidgetCategory;
  defaultConfig: Record<string, any>;
  isContainer?: boolean;                     // 容器组件（可放子节点）
  render: (
    config: Record<string, any>,
    ctx: WidgetContext,
    children?: React.ReactNode
  ) => React.ReactNode;
  propsSchema: PropFieldDef[];               // 属性面板字段（声明式）
}

// 注册 / 查询 API
export function registerWidget(plugin: WidgetPlugin): void;
export function getWidgetPlugin(type: string): WidgetPlugin | undefined;
export function getAllWidgets(): WidgetPlugin[];
export function getWidgetsByCategory(): Record<WidgetCategory, WidgetPlugin[]>;
```

### 3.2.2 改造后的运行机制

```
┌──────────────────────────────────────────────────────┐
│  widgets/registry.ts (中心化 Map<type, WidgetPlugin>)│
└────────┬─────────────────┬──────────────────┬───────┘
         │                 │                  │
    ┌────▼─────┐     ┌─────▼──────┐     ┌────▼──────┐
    │ Palette  │     │ PropertyPnl│     │ Renderer  │
    │ (左侧)   │     │ (右侧)     │     │ (运行态)  │
    │          │     │            │     │           │
    │ 读       │     │ 读         │     │ 调用      │
    │ getByCat │     │ propsSchema│     │ plugin    │
    │ egory()  │     │            │     │ .render() │
    └──────────┘     └────────────┘     └───────────┘
```

新增 widget 流程：
1. 在 `widgets/` 目录新建 `XxxWidget.tsx`
2. 在 `widgets/index.ts` 调用 `registerWidget({...})`
3. 完成 ✓（调色板、属性面板、运行态渲染自动生效）

### 3.3 缺失 widget 补齐清单（按优先级）

#### P0 - 高优先级（视觉稿核心使用，必须补）

| Widget | type 标识 | category | 视觉稿来源 |
|---|---|---|---|
| 柱状图 | `bar-chart` | chart | order picker |
| 饼图 | `pie-chart` | chart | order picker |
| 关系图 | `network-graph` | chart | cop 核心 |
| 时间线 | `timeline` | time | module / cop |
| 按钮组 | `button-group` | action | module / cop |
| Wiki 知识卡片 | `wiki-card` | data | module |
| 聊天侧栏 | `chat-aside` | ai | aip-chat 核心 |
| 消息列表 | `message-log` | ai | aip-chat 核心 |
| 输入框+发送 | `chat-input` | ai | aip-chat 核心 |

#### P1 - 中优先级（视觉稿用到但非核心 / 替代品）

| Widget | type 标识 | category | 视觉稿来源 |
|---|---|---|---|
| 钻取面板 | `drill-panel` | data | cop |
| 事件流 | `event-stream` | time | cop |
| 上下文 Chip 组 | `context-chips` | ai | aip-chat |
| Assist 弹出气泡 | `assist-popover` | ai | aip-chat |
| 状态徽章 | `status-badge` | data | order / module（表格内嵌） |
| 地图 | `geo-map` | chart | picker（cop 用关系图替代） |

#### P2 - 兼容旧 CanvasKind（消除 default 占位）

| Widget | type 标识 | 处理方式 |
|---|---|---|
| 筛选列表 | `filter-list`（原 `filter`） | 新增 renderer |
| Object View · Wiki | `object-view`（原 `overlay`） | 与 wiki-card 合并 |
| Action 表单 | `action-form`（原 `action`） | 新增 renderer |
| Buddy Chip | `buddy-chip`（原 `buddy`） | 新增 renderer |
| 指标卡 | `metric-card`（原 `metric`） | 与 stat-card 合并 |
| Stub 插件 | `stub-plugin`（原 `stub`） | 新增 renderer |
| 关系图 | `graph`（原 `graph`） | 与 network-graph 合并 |
| Object Table | `table`（原 `table`） | 与 object-table 合并 |

#### P3 - WidgetRegistry 已注册但视觉稿未用到

| Widget | type 标识 | category |
|---|---|---|
| 看板 | `kanban` | data |
| 甘特图 | `gantt` | chart |
| 日历 | `calendar` | time |
| 自定义图表 | `custom-chart` | chart |

---

## 4. 实施计划

### 4.1 新增文件目录

```
aos-platform/apps/web/src/pages/widgets/
├── BarChartWidget.tsx          # P0 柱状图
├── PieChartWidget.tsx          # P0 饼图
├── NetworkGraphWidget.tsx      # P0 关系图/拓扑图
├── TimelineWidget.tsx          # P0 时间线
├── ButtonGroupWidget.tsx       # P0 按钮组
├── WikiCardWidget.tsx          # P0 Wiki 知识卡片
├── ChatAsideWidget.tsx         # P0 聊天侧栏容器
├── MessageLogWidget.tsx        # P0 消息列表
├── ChatInputWidget.tsx         # P0 输入框+发送
├── DrillPanelWidget.tsx        # P1 钻取面板
├── EventStreamWidget.tsx       # P1 事件流
├── ContextChipsWidget.tsx      # P1 上下文 Chip 组
├── AssistPopoverWidget.tsx     # P1 Assist 弹出气泡
├── StatusBadgeWidget.tsx       # P1 状态徽章
├── GeoMapWidget.tsx            # P1 地图
├── KanbanWidget.tsx            # P3 看板
├── GanttWidget.tsx             # P3 甘特图
└── CalendarWidget.tsx          # P3 日历
```

### 4.2 修改文件

| 文件 | 改动内容 |
|---|---|
| `ComponentTreeEditor.tsx` | 1. WIDGET_PALETTE 扩展至 ~30 项<br>2. 按 category 分组渲染（Layout / 数据 / 图表 / AI / Action / 时间）<br>3. PropertyPanel 加新 widget 的字段 schema |
| `ComponentRenderer.tsx` | switch 增加 ~15 个 case 分支，调用新 widget 组件 |
| `widget_registry.py` | DEFAULTS 增加 9 个新 plugin（P0 阶段） |

### 4.3 调色板分类设计

```
┌─ 组件库 ─────────────────────────┐
│ ▼ Layout                          │
│   📐 页面布局  ⊞ 水平网格  🏷 页头│
│ ▼ 数据                            │
│   📊 统计卡  📋 表格  📄 详情抽屉 │
│   🗳 状态徽章  📚 Wiki 卡         │
│   🗂 钻取面板                     │
│ ▼ 筛选/操作                       │
│   📋 筛选栏  🔽 筛选列表          │
│   🔘 按钮组                       │
│ ▼ 图表                            │
│   📈 趋势图  📊 柱状图  🥧 饼图   │
│   🌐 关系图  🗺 地图              │
│ ▼ AI / 协作                       │
│   💬 聊天侧栏  📨 消息列表        │
│   ⌨️ 输入框  🏷 上下文 Chip       │
│   💡 Assist 气泡  👥 Buddy Chip   │
│ ▼ 时间/事件                       │
│   ⏱ 时间线  📅 事件流             │
│ ▼ 扩展组件                        │
│   📌 看板  📊 甘特图  📅 日历     │
└──────────────────────────────────┘
```

---

## 5. 风险与规避

| 风险 | 规避方式 |
|---|---|
| 新 widget 渲染器实现质量参差 | P0 9 种先做出占位 + 简化版渲染，确认效果再优化 |
| 调色板条目变多导致拥挤 | 按 category 分组（可折叠组），保持单组 ≤6 项 |
| 后端 widget_registry 与前端不同步 | 本次同步修改 `widget_registry.py` DEFAULTS |
| 旧 CanvasKind 兼容性 | 保留 `filter/table/buddy/overlay/...` 在调色板，但渲染走新 renderer（filter-list / object-table / buddy-chip / wiki-card 等） |
| 图表库选型 | 复用现有 TrendChartWidget 的 SVG 自绘方式，不引入 ECharts/Recharts（保持 bundle 体积） |
| 已有功能回归 | 不动现有 8 个 case 的实现，只新增 case 和 widget 文件 |

---

## 6. 验证方式

### 6.1 构建验证
```bash
cd aos-platform/apps/web && npm run build
```

### 6.2 功能验证（手测）
- 拖入调色板每个新 widget，画布能渲染出真实内容（非"未知组件"占位）
- 属性面板对应字段能编辑
- 保存后重新加载，componentTree 数据正确
- 4 个应用页面用画布编辑器能复刻出视觉稿效果

### 6.3 一致性验证
- 后端 `widget_registry.py` 的 plugin 数量 ≥ 前端调色板数量
- `WidgetRegistryPage.tsx` 显示的 builtin widget 与调色板一致

---

## 7. 后续规划（不在本次范围）

| 阶段 | 内容 |
|---|---|
| P3 | 抽出 `WidgetPluginRegistry`，定义 `WidgetPlugin` 协议（type/name/icon/category/render/propsSchema），调色板与 ComponentRenderer 全部动态读取 |
| P4 | 后端 widget_registry 增加 `category` / `propsSchema` / `icon` 字段，前端通过 API 拉取（消除前端硬编码） |
| P5 | 第三方 widget 上架流程（market 类），支持业务方独立扩展 |
