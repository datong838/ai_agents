# 106 · Graph / Action Form 真组件方案

> 状态：✅ 已落地（方案先行）  
> 前置：[`102`](./102-Widget运行时挂载方案.md) · T08 §4 · 20 §3.1  
> 索引：[`00`](./00-技术方案索引.md) v1.0.75

---

## 1. 目标

把 102 中 **诚实 stub** 的 `action-form` / `graph-view` 升为 **可交互真渲染**（仍非 G6 / 非完整 Action 执行器）。

| pluginId | canvasKind | 渲染 |
| --- | --- | --- |
| `action-form` | `action` | 读 ActionType 参数 → 表单 → `POST /v1/actions/validate` |
| `graph-view` | `graph` | 读 `GET /v1/objects/{type}/{id}/neighbors` → 邻接列表（engine=adjacency_table） |
| `metric-card` | `stub` | **仍 stub**（本刀不动） |

---

## 2. 规则

1. manifest：`runtime=inproc`，`canvasKind=action|graph`；安装后进调色板。  
2. 旧 Layout：`kind=stub` + `pluginId=action-form|graph-view` → 前端 `resolveRenderKind` **仍按插件真渲染**（兼容已存模块）。  
3. Action Form：**默认只 validate**；不在画布上静默 `execute`（需 Idempotency-Key，另刀）。  
4. Graph：**不做 G6**；诚实展示 1-hop 邻接。  
5. 不改 P0 四种 widget 行为。

---

## 3. 配置

| Widget | config |
| --- | --- |
| action-form | `actionTypeId`（默认 `CloseWorkOrder`） |
| graph-view | `objectType` + `objectId`（默认 `WorkOrder` / 首行或 `wo-1001`） |

---

## 4. 自测

**API（pytest）**

- install `action-form` / `graph-view` → palette kind 为 `action` / `graph`，`runtime=inproc`  
- neighbors / validate 既有契约仍绿  

**前端（vitest）**

- `resolveRenderKind`：stub+pluginId 映射到 action/graph  
- `normalizeLayout` 识别新 kind  

---

## 5. 明确不做

- G6 / Force 图编辑器  
- ~~画布内 Action execute + Draft 全链路~~ → 见 [`107`](./107-画布Action-execute与Draft方案.md)（HITL Draft；禁画布 autoApprove）  
- metric-card 真组件  
