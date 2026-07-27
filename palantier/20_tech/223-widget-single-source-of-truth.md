# 223 画布编辑 · widget 目录单一真相源 + 名字统一

> 版本：v1.0（2026-07-26）
> 关联：[223-canvas-palette-write-gap.md](./223-canvas-palette-write-gap.md)
> 影响文件：
> - `aos-platform/apps/web/src/pages/CanvasPage.tsx`（合并冗余区块 + icon 映射）
> - `aos-platform/apps/web/src/pages/s2/WidgetRegistryPage.tsx`（API 驱动替代硬编码）
> - `aos-platform/apps/web/src/pages/s2/WidgetRegistryPage.test.tsx`（可选：新增）
> - `aos-platform/plugins/widgets/*/manifest.json`（可选：补 icon 字段）

---

## 1. 问题

### 1.1 三套清单互不关联

| 清单 | 数据源 | 数量 |
|---|---|---|
| 画布编辑左侧 "Widget 调色板" | 后端 `/v1/widget-plugins` palette（manifest.json 驱动） | 12 |
| 画布编辑左侧 "拖拽到画布" | `DRAG_WIDGETS` 硬编码常量 | 11 |
| `/workshop/widget-registry` 页面 | `WIDGETS` 硬编码数组 | 16 |

三套清单互不关联，名字也不一致。

### 1.2 名字不一致示例

| 后端 manifest nameZh | 前端 DRAG_WIDGETS label | widget-registry WIDGETS.name |
|---|---|---|
| 对象表 | 表格 | 数据表格 |
| 关系图 | 图表 | — |
| 趋势图 | 趋势图 | 趋势图（id=chart） |
| 统计卡 | 统计卡 | 统计卡片（id=stat） |
| 筛选列表 | — | 筛选器（id=filter） |
| 详情抽屉 | 详情抽屉 | — |
| 动作表单 | 表单 | 编辑表单（id=form） |
| 页面头 | 页面头 | — |

### 1.3 两个冗余区块

画布编辑左侧同时存在 "Widget 调色板" 和 "拖拽到画布" 两个区块，最终都调用同一个 addNode 函数，行为完全一致。

---

## 2. 设计原则

| 原则 | 说明 |
|---|---|
| 单一真相源 | 后端 manifest.json 是 widget 元数据的唯一来源；前端不再硬编码 widget 清单 |
| 名字以 nameZh 为准 | 前端展示的 widget 名字一律用后端 manifest 的 `nameZh` 字段 |
| 合并冗余区块 | 画布编辑左侧只保留一个 widget 列表区块，支持点击 + 拖拽 |
| 最小更改 | 不破坏现有 palette 加载逻辑、addNode、WidgetPreview 渲染 |
| 渐进迁移 | widget-registry 页面切换到 API，但保留 fallback 兜底 |

---

## 3. 改动 A：合并画布编辑两个冗余区块

### 3.1 删除 DRAG_WIDGETS 常量

`CanvasPage.tsx` 删除：
```diff
- const DRAG_WIDGETS: { kind: CanvasKind; label: string; icon: string }[] = [
-   { kind: "table", label: "表格", icon: "📊" },
-   ...
- ];
```

### 3.2 新增 KIND_ICON 映射

只保留 emoji 图标映射（轻量、不依赖 manifest 扩展）：
```tsx
const KIND_ICON: Record<CanvasKind, string> = {
  table: "📊",
  graph: "📈",
  action: "📝",
  stub: "🔘",
  overlay: "🗺",
  metric: "📄",
  filter: "🔽",
  buddy: "💬",
  "page-header": "🏷",
  "stat-card": "🔢",
  "filter-bar": "📋",
  "detail-drawer": "🗂",
  "trend-chart": "📉",
};
```

### 3.3 重构左侧 widget 列表区块

合并成一个区块，标题 "Widget 组件"，每项显示 emoji + nameZh + 拖拽 + 点击：
```tsx
<div className="p-slate-tree-section-title" style={{ marginTop: "8px" }}>
  Widget 组件
</div>
<div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "4px", padding: "4px" }}>
  {palette.map((w) => (
    <div
      key={`${w.pluginId || w.kind}-${w.label}`}
      draggable
      onDragStart={(e) => e.dataTransfer.setData("text/plain", w.kind)}
      onClick={() => addNode(w)}
      title={w.runtime ? `runtime=${w.runtime}` : undefined}
      style={{
        padding: "5px 6px",
        borderRadius: "4px",
        background: "var(--aos-surface)",
        border: "0.5px solid var(--aos-border)",
        fontSize: "10px",
        cursor: "grab",
        display: "flex",
        alignItems: "center",
        gap: "4px",
        color: "var(--aos-text)",
      }}
    >
      <span style={{ fontSize: "12px" }}>{KIND_ICON[w.kind] || "📦"}</span>
      <span style={{ fontSize: "11px" }}>
        {w.label.replace(/^\+\s*/, "")}
        {w.stub ? " · stub" : ""}
      </span>
    </div>
  ))}
</div>
```

### 3.4 palette label 规范化

后端 `palette_items()` 已经返回 `+ nameZh` 格式 label，前端去除 "+ " 前缀后就是干净的 nameZh。无需改后端。

---

## 4. 改动 B：widget-registry 页面切换为 API 驱动

### 4.1 WidgetRegistryPage.tsx 改造

```diff
- const WIDGETS: WidgetItem[] = [
-   { id: "table", name: "数据表格", ... },
-   ...
- ];
+ // 改为从 API 加载
+ const [widgets, setWidgets] = useState<WidgetItem[]>([]);
+ const [loading, setLoading] = useState(true);
+ 
+ useEffect(() => {
+   apiGet<{ items?: WidgetApiItem[]; palette?: WidgetApiItem[] }>("/v1/widget-plugins")
+     .then((res) => {
+       const items = (res.items || []).filter(it => it.installed);
+       setWidgets(items.map(apiItemToWidgetItem));
+     })
+     .finally(() => setLoading(false));
+ }, []);
```

### 4.2 类型映射

后端 manifest 字段 → 前端 WidgetItem：
- `id` → `id`
- `nameZh` → `name`
- `description` → `description`
- `version` → `version`
- `runtime === "stub"` → `source: "custom"`
- `author === "aos"` → `source: "builtin"`
- 其它 → `source: "market"`
- `usedBy` 字段后端没有，暂时硬编码 0 或后续从 module count 接口取
- `icon` 从 canvasKind 映射

### 4.3 source 分类

manifest 没有 source 字段，根据 runtime 推断：
- runtime = "inproc" + author = "aos" → builtin（平台内置）
- runtime = "stub" → custom（占位/未实现）
- 其他 → market（市场安装）

---

## 5. 名字统一对照表

修复后，所有地方都用后端 manifest 的 nameZh：

| 后端 manifest id | 后端 nameZh | 统一显示名 |
|---|---|---|
| object-table | 对象表 | **对象表** |
| filter-list | 筛选列表 | **筛选列表** |
| buddy-chip | Buddy | **Buddy** |
| object-view | 对象视图 | **对象视图** |
| action-form | 动作表单 | **动作表单** |
| graph-view | 关系图 | **关系图** |
| metric-card | 指标卡 | **指标卡** |
| page-header | 页面头 | **页面头** |
| stat-card | 统计卡 | **统计卡** |
| filter-bar | 筛选栏 | **筛选栏** |
| detail-drawer | 详情抽屉 | **详情抽屉** |
| trend-chart | 趋势图 | **趋势图** |

---

## 6. 不变更项（防御式清单）

- ✅ CanvasKind/KIND_SET 类型不动（已扩展）
- ✅ addNode/sectionLabel/WidgetPreview 不动（已扩展）
- ✅ palette API 加载逻辑不动
- ✅ module_store.py 数据不动
- ✅ 既有 8 + 5 = 13 种 widget 的渲染不动

---

## 7. 验收清单

| # | 项 | 期望 |
|---|---|---|
| 1 | 进入画布编辑页 | 左侧只有一个 "Widget 组件" 区块，无重复 |
| 2 | 区块内每项 | emoji + 中文名（来自 nameZh），支持点击和拖拽 |
| 3 | 进入 /workshop/widget-registry | 显示 12 个 widget（API 返回），与画布编辑一致 |
| 4 | 名字一致 | 同一个 widget 在两个页面名字完全相同 |
| 5 | typecheck | 通过 |
| 6 | 现有测试 | 不被破坏 |

---

## 8. 风险与回滚

| 风险 | 缓解 |
|---|---|
| widget-registry API 加载失败 | fallback 到原硬编码 WIDGETS |
| KIND_ICON 不全 | 加 `|| "📦"` 兜底 |
| palette label 格式后端变化 | `.replace(/^\+\s*/, "")` 容错 |

回滚：撤销 CanvasPage.tsx 的列表区块 diff；撤销 WidgetRegistryPage.tsx 的 useEffect/apiGet diff。

---

## 9. 实施顺序

1. CanvasPage.tsx：删 DRAG_WIDGETS、加 KIND_ICON、合并列表区块
2. WidgetRegistryPage.tsx：API 驱动 + fallback
3. typecheck + 浏览器验收
