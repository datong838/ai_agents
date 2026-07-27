# 223 画布编辑 · 预览/编辑模式切换 + 文案"活"字清理

> 版本：v1.0（2026-07-26）
> 关联：[223-canvas-collapsible-sidebars.md](./223-canvas-collapsible-sidebars.md) · [223-canvas-trend-chart-placement.md](./223-canvas-trend-chart-placement.md)
> 影响文件：
> - `aos-platform/apps/web/src/pages/CanvasPage.tsx`
> - `aos-platform/apps/web/src/shell/icons.tsx`
> - `aos-platform/apps/web/src/styles.css`

---

## 1. 用户诉求

### 1.1 文案清理（"活"字）
> "中间的活应用预览（运行态）· 11 组件 · root=page-layout。这里 把 活 字 去掉"

3 处需要清理：
- 第 841 行：`● 活应用预览（运行态）· {N} 组件` → `● 应用预览（运行态）· {N} 组件`
- 第 845 行：`可编辑活应用（运行态只读预览）` → `可编辑应用（运行态只读预览）`
- 第 416 行：`已加载 {name} · 活应用预览（{N} 组件）` → `已加载 {name} · 应用预览（{N} 组件）`

### 1.2 预览/编辑切换（视觉稿对齐）
> "在视觉稿里 紧挨 工作流 的右边 有个 预览，点预览进入预览状态，在预览态 出一个 编辑（紫色字 那行的右边）"

视觉稿 [workshop-canvas.html#L160-L165](file:///Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/workshop-canvas.html#L160-L165) 工具栏左侧确实是 3 个按钮：
```html
<button class="p-slate-mode is-active" data-mode="edit">组件</button>
<button class="p-slate-mode" data-mode="workflow">工作流</button>
<button class="p-slate-mode" data-mode="preview">预览</button>  <!-- 缺失 -->
```

当前实现只有 widget / workflow 两态，**缺 preview 态**。

---

## 2. 设计原则

| 原则 | 说明 |
|---|---|
| 视觉稿对齐 | 工具栏严格按视觉稿 3 按钮排列，眼睛图标 + "预览"文字 |
| 模式独立 | canvasMode 扩展为三态：`widget` / `workflow` / `preview` |
| 预览即全屏 | preview 态下隐藏左右侧栏（CSS 级，不动折叠 state），中间画布占满 |
| 编辑入口可见 | preview 态下中间紫色提示条右侧出现"编辑"按钮，点击回到 widget 态 |
| 文案一致 | 同步清理所有"活应用"措辞为"应用" |
| 向后兼容 | 不破坏 widget/workflow 现有行为；左右折叠 state 在切回 widget 时恢复 |

---

## 3. 状态模型扩展

```diff
- const [canvasMode, setCanvasMode] = useState<"widget" | "workflow">("widget");
+ const [canvasMode, setCanvasMode] = useState<"widget" | "workflow" | "preview">("widget");
```

---

## 4. UI 结构

### 4.1 工具栏新增 Preview 按钮（紧挨 Workflow 右边）

```tsx
<button
  type="button"
  className={`p-slate-mode${canvasMode === "preview" ? " is-active" : ""}`}
  onClick={() => setCanvasMode("preview")}
  title="预览应用（运行态只读）"
>
  <NavIcon name="eye" style={{ width: "14px", height: "14px" }} />
  Preview
</button>
```

### 4.2 预览态布局（preview 模式分支）

preview 模式下，中间画布区独立分支：
- 不渲染左侧组件列表 aside（保留 p-slate-body 占位避免栅格错乱）
- 不渲染右侧属性面板 aside
- 中间画布占满
- 顶部保留紫色提示条，右侧新增"编辑"按钮
- 内容区根据 componentTree 是否存在渲染：
  - 有 componentTree → 渲染 ComponentRenderer（完整应用预览）
  - 无 componentTree → 渲染 widgets 简化预览（与构建态 widget 模式相同的 nodes 列表 + 运行态 rows）

### 4.3 紫色提示条右侧"编辑"按钮

```tsx
<div style={{ ...紫色提示条 }}>
  <span>● 应用预览（运行态）· {N} 组件 · root={type}</span>
  <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
    <span style={{ fontSize: 10, opacity: 0.7 }}>可编辑应用（运行态只读预览）</span>
    <button
      type="button"
      onClick={() => setCanvasMode("widget")}
      style={{
        fontSize: 11,
        padding: "3px 10px",
        borderRadius: 4,
        background: "#4f46e5",
        color: "#fff",
        border: "none",
        cursor: "pointer",
        fontWeight: 500,
      }}
    >
      ✎ 编辑
    </button>
  </div>
</div>
```

---

## 5. 图标新增

`icons.tsx` 暂无 eye 图标，新增（对齐视觉稿 SVG path）：

```diff
 const PATHS: Record<IconName, string> = {
   ...
   activity: '...',
+  eye: '<path stroke-linecap="round" stroke-linejoin="round" d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
 };
```

同步更新 IconName 联合类型（如果有显式枚举）。

---

## 6. CSS（可选增强）

无需新增 CSS。preview 态通过条件渲染（不挂载 aside）即可让中间画布自动 flex:1 占满。

---

## 7. 必须删除/修改的旧逻辑

| 位置 | 旧 | 新 |
|---|---|---|
| L279 | `"widget" \| "workflow"` | `"widget" \| "workflow" \| "preview"` |
| L416 | `· 活应用预览（` | `· 应用预览（` |
| L673 | `canvasMode === "workflow" ? <WorkflowMode/> : <widget分支>` | 三态分支：workflow / preview / widget |
| L841 | `● 活应用预览（运行态）` | `● 应用预览（运行态）` |
| L845 | `可编辑活应用（运行态只读预览）` | `可编辑应用（运行态只读预览）` |
| L845 后 | （无编辑按钮） | 新增"✎ 编辑"按钮 |

---

## 8. 不变更项（防御式清单）

- ✅ widget 模式的所有交互（addNode / removeNode / moveNode / saveLayout / 属性 Tab）不动
- ✅ workflow 模式（WorkflowMode 组件）不动
- ✅ componentTree 数据结构不动
- ✅ 左右折叠 state（leftCollapsed/rightCollapsed）不动；preview 态结束后切回 widget 仍按用户偏好折叠
- ✅ 底部 Tab 面板不动（preview 态仍可使用，与画布正交）
- ✅ module 下拉、保存按钮、9 个 toolbar Tab 不动

---

## 9. 验收清单

| # | 项 | 期望 |
|---|---|---|
| 1 | 进入画布编辑页 | 工具栏左侧出现 3 个按钮：Widget / Workflow / Preview |
| 2 | Widget 高亮 | 默认 widget 态，左侧组件列表 + 右侧属性面板正常 |
| 3 | 切到 Preview | 左右侧栏消失，中间画布占满，顶部紫色条 + "✎ 编辑"按钮 |
| 4 | 点"✎ 编辑" | 切回 widget 态，左右侧栏按原折叠偏好恢复 |
| 5 | Preview 态切 module | 应用预览内容跟随 module 切换 |
| 6 | 无 componentTree 的 module 在 Preview 态 | 显示 widgets 简化预览，不报错 |
| 7 | 文案检查 | 全文搜索 `活应用` 为 0 命中 |
| 8 | 类型检查 | `tsc --noEmit` 通过 |
| 9 | 单元测试 | 现有测试不被破坏 |

---

## 10. 风险与回滚

| 风险 | 缓解 |
|---|---|
| preview 态下用户误以为属性面板丢失 | 紫色条明确写"运行态只读预览"，并提供"✎ 编辑"显眼入口 |
| 没有 componentTree 时 preview 态空白 | fallback 到 widgets 简化预览 |
| Workflow → Preview 直接切换 | 三态互斥，setCanvasMode 直接覆盖，无副作用 |
| eye 图标 path 不准确 | 直接复用视觉稿原始 SVG path |

回滚：撤销 CanvasPage.tsx 的 canvasMode 类型扩展 + 工具栏按钮 + preview 分支；撤销 icons.tsx 的 eye 新增。
