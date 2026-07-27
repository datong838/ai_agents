# 223 画布编辑 · 左侧调色板补齐写路径缺口

> 版本：v1.0（2026-07-26）
> 关联：[223-canvas-preview-edit-toggle.md](./223-canvas-preview-edit-toggle.md)
> 影响文件：
> - 后端：`aos-platform/plugins/widgets/{page-header,stat-card,filter-bar,detail-drawer,trend-chart}/manifest.json`（新增 5 个）
> - 后端：`aos-platform/services/aos-api/aos_api/widget_registry.py`（DEFAULTS 扩展）
> - 前端：`aos-platform/apps/web/src/pages/CanvasPage.tsx`（CanvasKind/KIND_SET/DRAG_WIDGETS/addNode/sectionLabel/WidgetPreview）
> - 前端：`aos-platform/apps/web/src/pages/ComponentRenderer.test.ts`（可选：扩展 widgetsToComponents 测试）

---

## 1. 问题（WRO 不对称）

| 通道 | 当前能力 | 状态 |
|---|---|---|
| 读路径（components JSON → 渲染） | 7 种 type：page-header / horizontal-grid / stat-card / filter-bar / object-table / detail-drawer / trend-chart | ✅ 完整 |
| 写路径（左侧调色板 → 拖拽） | 8 种 kind：table / filter / buddy / overlay / stub / action / graph / metric | ❌ 与读路径对不齐 |

**对不齐的 5 种 type**（订单页用到，但拖不出来）：
- `page-header`（页面头）
- `stat-card`（统计卡，与老 `metric` 是不同 widget）
- `filter-bar`（筛选栏，与老 `filter` 是不同 widget）
- `detail-drawer`（详情抽屉）
- `trend-chart`（趋势图，与老 `graph` 是不同 widget）

---

## 2. 设计原则

| 原则 | 说明 |
|---|---|
| 架构对齐 | 走完整 widget-plugins 机制（manifest → API → palette），不绕过 |
| 双通道兼容 | 新 widget 既能写 widgets 数组，也能在 components 模式下预览 |
| 一组件一 canvasKind | 一个 widget 对应一个 canvasKind，名字直接复用渲染器 type |
| 最小更改 | 不动现有 8 种老 widget 的行为；新 widget 是新增不是替换 |
| 默认安装 | 5 个新 widget 加入 DEFAULTS，list 后自动进 palette |

---

## 3. 后端改动

### 3.1 新增 5 个 manifest.json

文件目录：
```
aos-platform/plugins/widgets/
├── page-header/manifest.json     ← 新增
├── stat-card/manifest.json       ← 新增
├── filter-bar/manifest.json      ← 新增
├── detail-drawer/manifest.json   ← 新增
└── trend-chart/manifest.json     ← 新增
```

每个 manifest 模板（以 page-header 为例）：
```json
{
  "id": "page-header",
  "name": "Page Header",
  "nameZh": "页面头",
  "description": "页面标题 + 副标题 + 操作按钮 · scheme 223",
  "version": "0.1.0",
  "author": "aos",
  "runtime": "inproc",
  "capabilities": ["widget", "page-header"],
  "canvasKind": "page-header",
  "palette": true,
  "configSchema": {
    "type": "object",
    "properties": {
      "title": { "type": "string" },
      "subtitle": { "type": "string" },
      "icon": { "type": "string" }
    }
  }
}
```

5 个 widget 的差异化字段：

| id | nameZh | canvasKind | configSchema 关键字段 |
|---|---|---|---|
| page-header | 页面头 | page-header | title, subtitle, icon, actions |
| stat-card | 统计卡 | stat-card | title, objectType, metric, field, filter, icon, color |
| filter-bar | 筛选栏 | filter-bar | objectType, tabs, search, filters |
| detail-drawer | 详情抽屉 | detail-drawer | objectType, width, sections, actions |
| trend-chart | 趋势图 | trend-chart | title, objectType, dateField, days, endDate |

### 3.2 widget_registry.py 扩展 DEFAULTS

```diff
- DEFAULTS = ("filter-list", "object-table", "buddy-chip", "object-view")
+ DEFAULTS = (
+     "filter-list", "object-table", "buddy-chip", "object-view",
+     "page-header", "stat-card", "filter-bar", "detail-drawer", "trend-chart",
+ )
```

注意：`required` 字段同步扩展，让 list_domain 把它们视为系统内置必装项。

---

## 4. 前端改动

### 4.1 CanvasPage.tsx · CanvasKind 类型扩展

```diff
- export type CanvasKind = "table" | "filter" | "buddy" | "overlay" | "stub" | "action" | "graph" | "metric";
+ export type CanvasKind =
+   | "table" | "filter" | "buddy" | "overlay" | "stub" | "action" | "graph" | "metric"
+   | "page-header" | "stat-card" | "filter-bar" | "detail-drawer" | "trend-chart";
```

### 4.2 CanvasPage.tsx · KIND_SET 扩展

```diff
- const KIND_SET = new Set<CanvasKind>(["table", "filter", "buddy", "overlay", "stub", "action", "graph", "metric"]);
+ const KIND_SET = new Set<CanvasKind>([
+   "table", "filter", "buddy", "overlay", "stub", "action", "graph", "metric",
+   "page-header", "stat-card", "filter-bar", "detail-drawer", "trend-chart",
+ ]);
```

> 这是关键：当前 palette 加载逻辑第 372 行 `if (!kind || !KIND_SET.has(kind)) return null`，不扩展 KIND_SET 则新 widget 会被过滤掉。

### 4.3 CanvasPage.tsx · DRAG_WIDGETS 扩展（左侧拖拽区视觉图标）

```diff
const DRAG_WIDGETS = [
  { kind: "table", label: "表格", icon: "📊" },
  { kind: "graph", label: "图表", icon: "📈" },
  { kind: "action", label: "表单", icon: "📝" },
  { kind: "stub", label: "按钮", icon: "🔘" },
  { kind: "overlay", label: "地图", icon: "🗺" },
  { kind: "metric", label: "文本", icon: "📄" },
+ { kind: "page-header", label: "页面头", icon: "🏷" },
+ { kind: "stat-card", label: "统计卡", icon: "🔢" },
+ { kind: "filter-bar", label: "筛选栏", icon: "🔽" },
+ { kind: "detail-drawer", label: "详情抽屉", icon: "📋" },
+ { kind: "trend-chart", label: "趋势图", icon: "📉" },
];
```

### 4.4 CanvasPage.tsx · addNode 默认配置映射

在 addNode 函数的 title/config/pluginId 三元表达式里追加 5 种新 kind 的默认值：

| kind | 默认 title | 默认 config | 默认 pluginId |
|---|---|---|---|
| page-header | "页面头" | { title: "页面标题", subtitle: "副标题" } | "page-header" |
| stat-card | "统计卡" | { objectType: "Order", metric: "count" } | "stat-card" |
| filter-bar | "筛选栏" | { objectType: "Order" } | "filter-bar" |
| detail-drawer | "详情抽屉" | { objectType: "Order", width: 400 } | "detail-drawer" |
| trend-chart | "趋势图" | { objectType: "Order", dateField: "order_date", days: 7 } | "trend-chart" |

### 4.5 CanvasPage.tsx · sectionLabel 扩展

```diff
function sectionLabel(kind: CanvasKind): string {
  if (kind === "filter") return "筛选";
  ...
+ if (kind === "page-header") return "页面头";
+ if (kind === "stat-card") return "统计卡";
+ if (kind === "filter-bar") return "筛选栏";
+ if (kind === "detail-drawer") return "详情抽屉";
+ if (kind === "trend-chart") return "趋势图";
  return "Overlay 详情";
}
```

### 4.6 CanvasPage.tsx · WidgetPreview 渲染分支

WidgetPreview 当前只处理老 8 种 kind。新 5 种需要追加分支：
- 因为 ComponentRenderer 已经实现了真渲染（PageHeader / StatCardWidget / FilterBarWidget / DetailDrawerWidget / TrendChartWidget），WidgetPreview 可以直接复用。

**关键设计**：让 WidgetPreview 引用 ComponentRenderer 的 RenderNode（如果可导出）。如果不可导出，则在 WidgetPreview 里加 5 个轻量占位（与拖拽预览场景匹配）。

**简化方案**（最小更改）：在 WidgetPreview 里给新 5 种 kind 各加一个**轻量预览分支**（标题 + 关键字段），用户实际看到的完整渲染走 ComponentRenderer。

### 4.7 CanvasPage.tsx · 右侧属性面板字段表单扩展

属性面板当前只对 filter/table/action/graph/metric 提供字段编辑器。新 widget 应该提供基本字段：
- page-header: title / subtitle 编辑
- stat-card: objectType / metric / field 编辑
- filter-bar: objectType 编辑
- detail-drawer: objectType / width 编辑
- trend-chart: objectType / dateField / days 编辑

**简化方案**：先复用通用 title/objectType 编辑器，特殊字段后续迭代。

---

## 5. 不变更项（防御式清单）

- ✅ 老 8 种 widget 的渲染逻辑、配置面板、palette 项不动
- ✅ ComponentRenderer 7 种 type 的渲染分支不动
- ✅ module_store.py 的 _ORDER_COMPONENTS 数据不动
- ✅ widgets ↔ components 双通道机制不动
- ✅ saveLayout / normalizeLayout 兼容（CanvasNode.config 是 open shape）
- ✅ 左右折叠、Preview/Widget/Workflow 三态切换、底部 Tab 面板不动

---

## 6. 验收清单

| # | 项 | 期望 |
|---|---|---|
| 1 | 重启后端服务 | `/v1/widget-plugins` 返回的 palette 包含 13 项（老 8 + 新 5） |
| 2 | 进入画布编辑页 | 左侧拖拽区显示 11 个图标（老 6 + 新 5，palette-list 部分会从 API 加载更多） |
| 3 | 拖"页面头"到画布 | 出现页面头 widget，标题可编辑 |
| 4 | 拖"统计卡" | 出现统计卡 widget，默认绑定 Order.count |
| 5 | 拖"筛选栏" | 出现筛选栏 widget |
| 6 | 拖"详情抽屉" | 出现详情抽屉 widget |
| 7 | 拖"趋势图" | 出现趋势图 widget |
| 8 | 切到 Preview 模式 | 新拖入的 widget 能被 ComponentRenderer 渲染 |
| 9 | 保存 module | 新 widget 持久化到 widgets 数组，刷新后还在 |
| 10 | tsc --noEmit | 通过 |
| 11 | 现有测试 | 不被破坏 |

---

## 7. 风险与回滚

| 风险 | 缓解 |
|---|---|
| 后端启动时 manifest 解析失败 | manifest 严格按现有格式（id/name/nameZh/canvasKind/palette/runtime 必填） |
| KIND_SET 扩展导致 palette 过滤逻辑改变 | 只新增不删除，老逻辑不变 |
| addNode 三元表达式嵌套过深 | 用 switch 重构（可选） |
| WidgetPreview 渲染新 kind 失败 | 加 default fallback 分支（已有） |

回滚：
- 后端：删除 5 个新 manifest 目录 + 恢复 DEFAULTS
- 前端：撤销 CanvasKind/KIND_SET/DRAG_WIDGETS/addNode/sectionLabel/WidgetPreview 的 diff

---

## 8. 实施顺序

1. 新增 5 个后端 manifest.json
2. widget_registry.py 扩展 DEFAULTS
3. 重启后端 API，curl 验证 palette 返回
4. 前端 CanvasKind/KIND_SET/DRAG_WIDGETS 扩展
5. addNode/sectionLabel 扩展
6. WidgetPreview 加 5 个分支
7. tsc + vitest 验证
8. 浏览器端到端验收
