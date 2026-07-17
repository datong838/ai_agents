# T08 · Workshop 工作台详细技术方案

> **版本**：v1.0.1 · 2026-07-17  
> **状态**：✅ **方案完成**  
> **对齐产品**：[08](../08-Workshop产品方案.md) · [08a](../08a-Workshop产品设计线框图.md) · [20 §6.6](20-AOS整体技术方案.md) · [T-UI](T-UI-前端工程与foundry-html落地规范.md) · [T-API](T-API-aos-api稳定契约.md) · [21](21-AOS开源选型与功能清单.md) · [23 军规](23-AOS开源引用与交付军规.md)（ToolJet 只参考交互）  
> **UI 真源**：`foundry/html/workshop*.html` v1.6

---

## 使用的 Rules

先方案后代码 · 产品对齐 · UI 必引用 html · Widget **插件化** · 护栏（Selection/分页/Marking/幂等）必写

---

## 1. 范围

| 做 | 不做 |
| --- | --- |
| Module 工厂 · Layout · Widget · Variables · Events · Selection | SQL 面板 / 另起 BI 产品 |
| Inbox / 知识图谱 / Buddy / COP / 发布入口 | Apollo 控制面本体（→ T09） |
| 运行态权限与 Marking | 完整低代码「任意 JS 应用」 |

---

## 2. 逻辑架构

```text
apps/web /workshop/*
        → aos-api
            → Module Runtime（定义 / 发布 / 运行）
            → Object Query（L2）
            → Action Runtime（L2/06b）
            → AIP Chat API（Buddy）
            → Publish Adapter → Apollo
```

自有服务建议：`services/module-runtime/`（或并入 `aos-api` 模块，边界清晰即可）。

---

## 3. 核心模型

| 模型 | 说明 |
| --- | --- |
| **Module** | 应用单元：Layout 树 + Variables + Events + 权限 |
| **Layout** | Header / Page / Section / Overlay（对齐 08a WF-WS-02） |
| **Widget** | 可插拔渲染单元；配置 JSON Schema；绑定 Variables |
| **Variable** | Object Set / Selection / Active / Scalar / Function 结果 |
| **Selection** | 运行时实例集合；**维度 ≤10**（产品补强） |
| **Event** | 行选 → Overlay；按钮 → Action；须 **幂等键** |

### 3.1 Selection 上限（强制）

| 规则 | 实现 |
| --- | --- |
| 筛选维度 ≤10 | Runtime 拒绝第 11 维；UI 计数见 `workshop-module.html` |
| 多选对象 | 可批量进 Action；仍受 ACT-07 |
| Active | 单对象详情 / Wiki / Buddy Context |

### 3.2 表格分页（强制）

Object Table：**>10000 行**必须服务端分页或游标；禁止一次拉全量。

### 3.3 Widget Markings（强制）

Widget 声明所需 Marking/角色；运行态无权限则不挂载（构建态可选显示锁定态）。

### 3.4 事件幂等（强制）

前端防抖 + 请求头/体 `idempotencyKey`；与 06b ACT-07 同源。

---

## 4. Widget 插件化

### 4.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| Module 工厂 | Layout（Header/Page/Section/Overlay）+ Variables + Events | 08a WF-WS-01/02 |
| Widget 插件 | 注册/配置/挂载；JSON Schema；绑定 Variables | 新增 Widget 不改 Runtime 核心 |
| Selection | 维度 ≤10；Active 单对象 | 超限禁加 |
| Object Table | >10000 行服务端分页/游标 | 不卡死 |
| Marking | 无权限不渲染 Widget | 财务等受限区 |
| 事件幂等 | `idempotencyKey` 与 ACT-07 同源 | 连点一次成功 |
| Buddy / COP | AIP Chat 嵌入 · 全屏态势 | 写仍走 Action |
| 发布入口 | 只跳 Apollo；不实现舰队 | workshop-publish |
| 嵌套/Loop（P2） | Module interface · Loop · 事件冒泡 | v1.1 执行器 |
| 离线缓存 | 只读快照；写仅待同步队列 | 离线禁直写 |

### 4.1 契约

```text
manifest:
  id, version, capabilities: ["render","configure"]
  configSchema, requiredVariables, requiredMarkings
lifecycle: register → configure → mount → unmount
isolation: 默认同应用进程内组件；高风险第三方 Widget 用 iframe sandbox（v1.1 启用，契约预留 `sandboxed: true`）
```

### 4.4 嵌套 Module / Loop（P2 完整语义 · 已定）

| 概念 | 语义 |
| --- | --- |
| **Module interface** | 子 Module 声明输入 Variables（类型+必填）与输出 Variables |
| **嵌入** | 父 Layout 节点 `type=embedded-module` 绑定 `moduleId` + 变量映射表 |
| **Loop** | 对 Object Set 每元素渲染子 Section 一次；迭代变量名固定注入 `loop.item` |
| **事件冒泡** | 子 Module Action 默认不穿透；须显式 `re-emit` 到父 Events |
| **权限** | 子 Module 另算 Marking；父可见≠子可写 |

**UI：** `workshop-module-interface.html` · `workshop-events.html`  
**Runtime：** v1.0 可只存 Schema；**v0.3 里程碑不阻塞**；v1.1 前完成执行器。

### 4.5 桌面离线缓存（已定）

| 项 | 策略 |
| --- | --- |
| 缓存什么 | 已打开 Module 定义 + 最近 Object Set 页（只读快照） |
| 存哪 | Tauri 侧 SQLite（或现有本地库）；Web 用 IndexedDB |
| 失效 | `ETag`/`updatedAt`；上线后后台刷新 |
| 写路径 | **离线禁止** Action 直写；仅队列「待同步草稿」，上线后按 ACT-07 提交 |

### 4.2 首批 Widget（P0）

| Widget | 蓝图 | 变量依赖 |
| --- | --- | --- |
| Filter List | `workshop-module` | Object Set |
| Object Table | 同上 | Object Set · Selection |
| Object View | module / object-view | Active |
| Graph | `workshop-object-view` | Object+Link |
| Action Form | object-view 弹层 | Selection + ActionType |
| AIP Chat / Assist | `workshop-aip-chat` | Selection + AgentId |
| Metric / Map（COP） | `workshop-cop` | 聚合变量 |

### 4.3 开源参考（已核对）

| 仓 | 路径 | 抄 | 不抄 | 选型 |
| --- | --- | --- | --- | --- |
| ToolJet | `D1_WorkshopFactory/ToolJet/frontend` | 组件面板 / 属性表单模式 | 整站与数据源协议 | **建议**画布交互参考（视觉仍 html） |
| Appsmith | `D1_WorkshopFactory/appsmith` | Widget 配置思路 | 品牌壳 | 备选对照 |
| ag-grid | `D3_HighPerfGrid/ag-grid` | 虚拟滚动 · 列定义 | 对象语义 | **建议**大表 |
| G6 | `B3_GraphViz/G6` | 图布局与交互 | OMA 配置 | **建议**知识图谱 |
| cytoscape.js | `B3_GraphViz/cytoscape.js` | 图交互备选 | OMA 配置 | 备选 |
| kepler.gl | `D4_Map/kepler.gl` | COP 地图层 | 独立产品壳 | COP 需要时启用 |

---

## 5. UI 蓝图（强制引用）

| 功能 | UI 蓝图 | 组件要点 |
| --- | --- | --- |
| 应用列表 | [`workshop.html`](../foundry/html/workshop.html) | 卡片 · 进入构建 |
| 画布空态 | [`workshop-canvas.html`](../foundry/html/workshop-canvas.html) | Layout 树 · 先 Object Set 再拖 Widget |
| Inbox | [`workshop-module.html`](../foundry/html/workshop-module.html) | Filter+Table+View；维数/分页/Marking |
| 知识图谱+Action | [`workshop-object-view.html`](../foundry/html/workshop-object-view.html) | 点选 Selection；Action 幂等 |
| Buddy/Assist | [`workshop-aip-chat.html`](../foundry/html/workshop-aip-chat.html) | Context 芯片；链决策谱系 |
| COP | [`workshop-cop.html`](../foundry/html/workshop-cop.html) | 全屏态势 |
| 发布入口 | [`workshop-publish.html`](../foundry/html/workshop-publish.html) | → `apollo-release` / `apollo-assets` |
| 模块接口（P2） | `workshop-module-interface.html` | 子 Module / Loop |
| Events（P2） | `workshop-events.html` | 行选→Overlay |

---

## 6. API 面（建议）

| API | 用途 |
| --- | --- |
| `GET/POST /v1/modules` | Module CRUD |
| `GET /v1/modules/{id}/runtime` | 运行态 Schema + 初始变量 |
| `POST /v1/object-sets/query` | 分页查询（强制 limit） |
| `POST /v1/actions/execute` | 带 idempotencyKey · HITL/Draft |
| `POST /v1/aip/chat` | Buddy（Context=Selection） |
| `POST /v1/modules/{id}/publish` | Publish Adapter → Apollo |

禁止 UI 直调 Ontology 写接口（HR-01）。

---

## 7. 与上下游边界

| 上游 | 关系 |
| --- | --- |
| L2 Ontology | 只读 Object/Link/Wiki 字段；写走 Action |
| AIP | Buddy 工具同源 AIP-003；建议 Action 仍 HITL |
| Apollo | 只发 Module/Asset Bundle；不实现舰队 |

---

## 8. 验收

| # | 标准 |
| --- | --- |
| A1 | Inbox 三联可筛选/点选/开 Action，维数徽标正确 |
| A2 | 1万+ 行演示数据不卡死（分页） |
| A3 | 无 Marking 用户看不到财务 Widget |
| A4 | 连点 Action 只成功一次 |
| A5 | 发布入口可达 Apollo 页（联调 Mock 即可） |

---

## 9. 已决结论（原缺口已关闭）

| ID | 结论 |
| --- | --- |
| T08-G1 | Loop/嵌套语义见 **§4.4**；执行器排 v1.1，不阻塞 v0.3 Inbox |
| T08-G2 | 离线缓存见 **§4.5**；写路径离线只入待同步队列 |

---

*T08 v1.0 · docs/palantier/20_tech*
