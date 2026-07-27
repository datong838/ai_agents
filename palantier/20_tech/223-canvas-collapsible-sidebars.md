# 223 画布编辑页 · 左右侧栏可折叠方案

> 版本：v1.0（2026-07-26）
> 关联：[223-plan.md](./223-plan.md) · P0 工作台"画布编辑"
> 影响文件：
> - `aos-platform/apps/web/src/pages/CanvasPage.tsx`
> - `aos-platform/apps/web/src/styles.css`

---

## 1. 背景与问题

### 1.1 现状缺陷
当前 `CanvasPage.tsx` 为了在「活应用预览模式」（`componentTree != null`）下让中间画布最大化，采用了**粗暴隐藏左侧 widget 组件列表**的做法：

```tsx
// 旧逻辑（要废除）
<aside className="p-slate-tree" style={componentTree ? { display: "none" } : undefined}>
```

副作用：
1. 用户在活应用预览模式下**完全看不到、也无法操作 widget 组件列表**（用户原话："边上那个 widget 组件列表不见了"）。
2. 右侧 `p-slate-props` 属性面板始终占 260px，无法让位。
3. 三栏布局变成两栏，破坏了画布编辑器的视觉一致性。

### 1.2 用户诉求
> "边上那个 widget 组件列表不见了 你再恢复他吧，我想的 为了让中间区最大化 是不是可以让左边 和右边 分表向左右折叠"

翻译为产品需求：
- **恢复**左侧 widget 组件列表（无论是否活应用预览）。
- 左、右侧栏**独立可折叠**，折叠后变成窄竖条（约 28px），点击可展开。
- 折叠状态**持久化**到 localStorage，刷新后保留。

---

## 2. 设计原则

| 原则 | 说明 |
|---|---|
| 最小更改 | 复用现有 `p-slate-tree` / `p-slate-props` 结构，只新增折叠态分支 |
| 不破坏现有功能 | widgets 模式、活应用预览模式、属性面板 Tab、底部 Tab 面板**全部保持原行为** |
| 双栏独立 | 左右折叠互不依赖，用户可只折叠一侧 |
| 持久化 | 折叠状态写入 localStorage，key = `canvas.sidebar.leftCollapsed` / `canvas.sidebar.rightCollapsed` |
| 视觉对齐 | 折叠竖条上展示一个 chevron 图标 + 纵向文字标签，与暗色画布编辑器风格一致 |

---

## 3. 状态模型

### 3.1 新增 React state

```tsx
const [leftCollapsed, setLeftCollapsed] = useState<boolean>(() => {
  if (typeof window === "undefined") return false;
  return window.localStorage.getItem("canvas.sidebar.leftCollapsed") === "1";
});

const [rightCollapsed, setRightCollapsed] = useState<boolean>(() => {
  if (typeof window === "undefined") return false;
  return window.localStorage.getItem("canvas.sidebar.rightCollapsed") === "1";
});
```

### 3.2 持久化 effect

```tsx
useEffect(() => {
  window.localStorage.setItem("canvas.sidebar.leftCollapsed", leftCollapsed ? "1" : "0");
}, [leftCollapsed]);

useEffect(() => {
  window.localStorage.setItem("canvas.sidebar.rightCollapsed", rightCollapsed ? "1" : "0");
}, [rightCollapsed]);
```

---

## 4. UI 结构

### 4.1 左侧 aside（`p-slate-tree`）

```tsx
<aside className={`p-slate-tree${leftCollapsed ? " is-collapsed" : ""}`}>
  {leftCollapsed ? (
    <button
      type="button"
      className="p-slate-side-restore"
      onClick={() => setLeftCollapsed(false)}
      title="展开组件列表"
      aria-label="展开组件列表"
    >
      <NavIcon name="chevron" style={{ transform: "rotate(0deg)" }} />
      <span className="p-slate-side-restore-label">组件</span>
    </button>
  ) : (
    <>
      <div className="p-slate-side-pin">
        <button
          type="button"
          className="p-slate-side-collapse-btn"
          onClick={() => setLeftCollapsed(true)}
          title="折叠组件列表（向左收起）"
          aria-label="折叠组件列表"
        >
          <NavIcon name="chevron" style={{ transform: "rotate(180deg)" }} />
        </button>
      </div>
      {/* …原有 search/tree/palette 内容不动… */}
    </>
  )}
</aside>
```

### 4.2 右侧 aside（`p-slate-props`）

```tsx
<aside className={`p-slate-props${rightCollapsed ? " is-collapsed" : ""}`}>
  {rightCollapsed ? (
    <button
      type="button"
      className="p-slate-side-restore"
      onClick={() => setRightCollapsed(false)}
      title="展开属性面板"
      aria-label="展开属性面板"
    >
      <span className="p-slate-side-restore-label">属性</span>
      <NavIcon name="chevron" style={{ transform: "rotate(180deg)" }} />
    </button>
  ) : (
    <>
      <div className="p-slate-props-header">
        <NavIcon name="apps" ... />
        <span>{node ? node.title : "未选中 Widget"}</span>
        <button
          type="button"
          className="p-slate-side-collapse-btn"
          onClick={() => setRightCollapsed(true)}
          title="折叠属性面板（向右收起）"
          aria-label="折叠属性面板"
        >
          <NavIcon name="chevron" ... />
        </button>
      </div>
      {/* …原有 Tab/section 内容不动… */}
    </>
  )}
</aside>
```

---

## 5. CSS 改动（追加到 `styles.css`）

```css
/* ===== 画布编辑器 · 左右侧栏折叠态 ===== */
.p-slate-tree,
.p-slate-props {
  position: relative;
  transition: width 160ms ease, min-width 160ms ease;
}

.p-slate-tree.is-collapsed,
.p-slate-props.is-collapsed {
  width: 28px;
  min-width: 28px;
  overflow: hidden;
}

.p-slate-side-pin {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 2;
}

.p-slate-side-collapse-btn {
  width: 22px;
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 4px;
  color: var(--aos-text-tertiary);
  cursor: pointer;
}
.p-slate-side-collapse-btn:hover {
  background: var(--aos-surface-hover);
  color: var(--aos-text);
}

.p-slate-side-restore {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 100%;
  padding: 12px 0;
  background: transparent;
  border: none;
  color: var(--aos-text-secondary);
  cursor: pointer;
}
.p-slate-side-restore:hover {
  background: var(--aos-surface-hover);
  color: var(--aos-accent);
}
.p-slate-side-restore svg {
  width: 12px;
  height: 12px;
  color: var(--aos-text-tertiary);
}
.p-slate-side-restore-label {
  font-size: 10px;
  letter-spacing: 0.2em;
  writing-mode: vertical-rl;
  text-orientation: mixed;
}
```

---

## 6. 必须删除的旧逻辑

```diff
- <aside className="p-slate-tree" style={componentTree ? { display: "none" } : undefined}>
+ <aside className={`p-slate-tree${leftCollapsed ? " is-collapsed" : ""}`}>
```

```diff
- <div className="p-slate-canvas" style={componentTree ? { padding: 12 } : undefined}>
+ <div className="p-slate-canvas">
```

> 理由：通过折叠机制让用户自行决定是否让出空间，比"自动隐藏"更可控、可预期；padding 回到 24px 是因为侧栏折叠后画布自然变宽，不需要再缩 padding。

---

## 7. 不变更项（防御式清单）

- ✅ widgets 模式（无 componentTree）的渲染逻辑、saveLayout、addNode、removeNode、moveNode 全部不动
- ✅ 活应用预览（ComponentRenderer）逻辑不动
- ✅ 顶部 module 下拉、保存按钮、模式切换、9 个 Tab、底部 panel 不动
- ✅ 右侧属性面板 4 个 Tab（content/style/events/data）内容不动
- ✅ CSS 既有的 `.p-slate-tree` / `.p-slate-props` 宽度规则不动（仅在 `.is-collapsed` 时覆盖）

---

## 8. 验收清单

| # | 项 | 期望 |
|---|---|---|
| 1 | 进入画布编辑页 | 左 220px / 右 260px 正常显示 |
| 2 | 点左侧"折叠"按钮 | 左侧收缩为 28px 竖条，画布变宽，组件列表隐藏 |
| 3 | 点竖条 | 左侧展开，组件列表恢复 |
| 4 | 点右侧"折叠"按钮 | 右侧收缩为 28px 竖条，属性面板隐藏 |
| 5 | 切换到活应用预览 module | 左右侧栏不再被强制隐藏，仍可独立折叠 |
| 6 | 折叠后刷新页面 | 折叠状态保留（localStorage） |
| 7 | 切换 widgets ⇄ 活应用 | 折叠状态不被重置 |
| 8 | 类型检查 | `npm run typecheck` 无新错误 |
| 9 | 单元测试 | `CanvasPage.test.tsx`（如有）通过 |

---

## 9. 风险与回滚

| 风险 | 缓解 |
|---|---|
| 旧的 `display:none` 残留导致回归 | 全文搜索 `componentTree ? { display` 必须为 0 命中 |
| localStorage 在 SSR 环境报错 | useState 初始化加 `typeof window === "undefined"` 守卫 |
| chevron 图标方向不直观 | 左侧折叠按钮指向左（rotate 180），竖条上的指向右；右侧相反 |
| 旧用户偏好丢失 | key 命名独立，旧 key 不存在等价于 false（展开），无破坏 |

回滚：撤销 `CanvasPage.tsx` 中 `leftCollapsed/rightCollapsed` 状态及 JSX 分支，恢复 `display:none` 即可。
