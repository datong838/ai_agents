# 223 画布编辑 · 近 7 天订单趋势位置修正

> 版本：v1.0（2026-07-26）
> 关联：[223-canvas-collapsible-sidebars.md](./223-canvas-collapsible-sidebars.md)
> 影响文件：
> - `aos-platform/apps/web/src/pages/ComponentRenderer.tsx`
> - `aos-platform/apps/web/src/pages/ComponentRenderer.test.ts`

---

## 1. 问题

用户反馈："为了完全一样 你把 近 7 天订单趋势 放在订单表格的下面吧"。

### 1.1 数据层（已正确）
`module_store.py` 的 `_ORDER_COMPONENTS["root"].children`：
```python
["page-header", "stat-row", "filter-bar", "order-table", "detail-drawer", "trend-chart"]
```
trend-chart 已经在 detail-drawer 之后，**数据顺序正确**。

### 1.2 渲染层（有 bug）
`ComponentRenderer.tsx` 第 78~105 行 `case "page-layout"`：

```tsx
const pair = detectTableDrawerPairByIds(components, childIds);
if (pair) {
  const others = pair.otherIds.map(...).filter(...);   // 包含 trend-chart
  return (
    <div ...>
      {others.map(...)}                                 // ← 全部在前
      <TableWithDrawerLayout ... />                     // ← 表格在后
    </div>
  );
}
```

`pair.otherIds` 把 table+drawer 之外的所有 children 拍平返回（顺序保留），但渲染时**全部放在 TableWithDrawerLayout 之前**，导致 trend-chart 被拉到表格上方。

---

## 2. 修复策略（最小更改 + 向后兼容）

### 2.1 核心：按 tableId 在 children 中的位置切分 before/after

把 `pair.otherIds` 按 tableId 在原 children 中的位置切成两段：
- **beforeIds**：tableId 之前的 children（不含 drawerId）
- **afterIds**：tableId 之后的 children（不含 drawerId）

渲染顺序：`beforeIds → TableWithDrawerLayout → afterIds`

### 2.2 实现选择

为保持向后兼容（现有测试 `pair!.otherIds` 仍要生效），采用：
- 保留 `TableDrawerPair.otherIds` 字段不动
- 在 `TableDrawerPair` 新增 `beforeIds` 和 `afterIds` 两个字段
- 在 `detectTableDrawerPairByIds` 中按 tableId 在 childIds 中的 index 切分

### 2.3 这样改动后

| children 顺序 | 渲染顺序 |
|---|---|
| page-header | page-header |
| stat-row | stat-row |
| filter-bar | filter-bar |
| order-table | ┐ |
| detail-drawer | ├ TableWithDrawerLayout |
| **trend-chart** | ┘ **trend-chart**（落到表格下方）✅ |

---

## 3. 具体代码改动

### 3.1 `ComponentRenderer.tsx`

**改动 A：扩展 TableDrawerPair 类型**

```diff
 type TableDrawerPair = {
   tableId: string;
   drawerId: string;
   otherIds: string[];
+  beforeIds: string[];
+  afterIds: string[];
 };
```

**改动 B：detectTableDrawerPairByIds 切分**

```diff
 export function detectTableDrawerPairByIds(
   tree: ComponentTree,
   childIds: string[],
 ): TableDrawerPair | null {
   const tableId = childIds.find((id) => tree[id]?.type === "object-table");
   const drawerId = childIds.find((id) => tree[id]?.type === "detail-drawer");
   if (!tableId || !drawerId) return null;
   const otherIds = childIds.filter((id) => id !== tableId && id !== drawerId);
+  const tableIdx = childIds.indexOf(tableId);
+  const beforeIds = childIds
+    .slice(0, tableIdx)
+    .filter((id) => id !== drawerId);
+  const afterIds = childIds
+    .slice(tableIdx + 1)
+    .filter((id) => id !== drawerId);
-  return { tableId, drawerId, otherIds };
+  return { tableId, drawerId, otherIds, beforeIds, afterIds };
}
```

**改动 C：page-layout 渲染分支**

```diff
 case "page-layout": {
   const childIds = node.children || [];
   const pair = detectTableDrawerPairByIds(components, childIds);
   if (pair) {
     const tableNode = components[pair.tableId];
     const drawerNode = components[pair.drawerId];
-    const others = pair.otherIds
+    const beforeNodes = pair.beforeIds
+      .map((id) => components[id])
+      .filter((c): c is ComponentNode => !!c);
+    const afterNodes = pair.afterIds
       .map((id) => components[id])
       .filter((c): c is ComponentNode => !!c);
     return (
       <div style={{ ... }}>
+        {beforeNodes.map((c, i) => (
+          <RenderNode key={`b-${i}`} node={c} components={components} depth={depth + 1} />
+        ))}
-        {others.map((c, i) => (
-          <RenderNode key={`o-${i}`} node={c} components={components} depth={depth + 1} />
-        ))}
         <TableWithDrawerLayout tableNode={tableNode} drawerNode={drawerNode} />
+        {afterNodes.map((c, i) => (
+          <RenderNode key={`a-${i}`} node={c} components={components} depth={depth + 1} />
+        ))}
       </div>
     );
   }
   ...
 }
```

### 3.2 `ComponentRenderer.test.ts`

新增测试用例验证切分正确：

```ts
it("splits otherIds into beforeIds/afterIds by table position", () => {
  const tree: ComponentTree = {
    root: {
      type: "page-layout",
      children: ["page-header", "stat-row", "filter-bar", "order-table", "detail-drawer", "trend-chart"],
    },
    "page-header": { type: "page-header" },
    "stat-row": { type: "horizontal-grid" },
    "filter-bar": { type: "filter-bar" },
    "order-table": { type: "object-table" },
    "detail-drawer": { type: "detail-drawer" },
    "trend-chart": { type: "trend-chart" },
  };
  const pair = detectTableDrawerPair(tree, "root");
  expect(pair!.beforeIds).toEqual(["page-header", "stat-row", "filter-bar"]);
  expect(pair!.afterIds).toEqual(["trend-chart"]);
  expect(pair!.otherIds).toEqual(["page-header", "stat-row", "filter-bar", "trend-chart"]);
});
```

---

## 4. 不变更项（防御式清单）

- ✅ `module_store.py` 的 `_ORDER_COMPONENTS` 完全不动（数据顺序已正确）
- ✅ `TableDrawerPair.otherIds` 字段保留，向后兼容
- ✅ 现有测试 `pair!.otherIds` 断言不变
- ✅ `detectTableDrawerPair` / `detectTableDrawerPairByIds` 签名不变
- ✅ 无 table+drawer 配对时走原 fallback 路径，渲染行为不变
- ✅ 不影响 widgets 模式、horizontal-grid、stat-card 等其他类型

---

## 5. 风险与回滚

| 风险 | 缓解 |
|---|---|
| beforeIds/afterIds 切分边界错误（drawerId 在 tableId 之前的情况） | 用 `.filter(id => id !== drawerId)` 兜底过滤 |
| 现有测试 otherIds 断言失败 | otherIds 字段语义不变，仍按原 childIds 顺序 |
| 渲染 key 冲突 | beforeNodes 用 `b-${i}`，afterNodes 用 `a-${i}`，避免与原 `o-${i}` 冲突 |

回滚：撤销 ComponentRenderer.tsx 的 3 处 diff 即可。
