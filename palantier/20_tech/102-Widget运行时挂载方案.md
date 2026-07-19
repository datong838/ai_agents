# 102 · Widget 运行时挂载（画布按插件渲染）

> **版本**：v1.0 · 2026-07-19  
> **状态**：✅ 已落地 · 自测通过  
> **上游**：[98](98-插件化剩余域收口方案.md) · T08 §4 · 20 §3.1  
> **Rules**：调色板只认已装插件 · stub 诚实空态 · Object Table 用真预览数据 · 最小更改

---

## 1. 范围

| # | 能力 | 做法 |
| --- | --- | --- |
| **A** | stub 进调色板 | action-form / metric-card / graph-view：`canvasKind=stub` · `palette=true`；安装后可拖 |
| **B** | 节点带 pluginId | CanvasNode 存 `pluginId` · 渲染读插件元数据 |
| **C** | stub 渲染 | 诚实 Banner：未实现真组件 · runtime=stub |
| **D** | Object Table | Widget 预览用 `object-sets/query` 真行，去掉写死 wo-1001 |
| **E** | palette API | 返回 pluginId / runtime / nameZh |

非目标：iframe sandbox · ~~Graph 真 G6 · Action Form 完整提交器~~ → 见 [`106`](./106-Graph与ActionForm真组件方案.md)（邻接列表 + validate；仍非 G6 / execute）。

## 2. 自测

1. install action-form → palette 含 stub ✅  
2. 画布加 stub 节点见诚实文案（UI）  
3. Object Table 预览行来自 API（非写死样例） ✅  
4. 原有 P0 四种 kind 仍可用 ✅  

pytest：`test_widget_runtime_102` + `test_pluginization_98` → **6 passed**
