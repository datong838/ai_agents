# 08 · Workshop 产品方案

## L3 应用交互层：零代码前端工厂 + AIP 嵌入

> **文档性质**：对标 Palantir **Workshop** 的产品设计 · 固化为 PRD 子章  
> **版本**：v1.2 · 2026-07-15  
> **状态**：可直接作为 [03 PRD §3.4](03-对标Palantir-AOS-PRD框架.md) 详稿 · 研发 / PPT 素材  
> **对标在线（本期深挖）**：  
> · [Workshop Overview](https://www.palantir.com/docs/foundry/workshop/overview/)  
> · [Getting started](https://www.palantir.com/docs/foundry/workshop/getting-started/)  
> · [Layouts](https://www.palantir.com/docs/foundry/workshop/concepts-layouts/) · [Widgets](https://www.palantir.com/docs/foundry/workshop/concepts-widgets/) · [Variables](https://www.palantir.com/docs/foundry/workshop/concepts-variables/) · [Events](https://www.palantir.com/docs/foundry/workshop/concepts-events/)  
> · [Module interface](https://www.palantir.com/docs/foundry/workshop/module-interface/) · [Loop layouts](https://www.palantir.com/docs/foundry/workshop/loop-layouts/)  
> · [Object Table](https://www.palantir.com/docs/foundry/workshop/widgets-object-table/) · [AIP Chatbot widget](https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot)  
> · [AIP Assist event](https://www.palantir.com/docs/foundry/workshop/concepts-events/) · [AIP features](https://www.palantir.com/docs/foundry/aip/aip-features/)  
> **关联**：[03 §3.4](03-对标Palantir-AOS-PRD框架.md) · [06](06-语义本体Ontology-Mapping产品方案.md) · [06b](06b-Action与Function产品设计.md) · [07](07-AIP引擎k-LLM与AgentStudio产品方案.md) · **发布详稿 → [09 Apollo](09-Apollo交付引擎产品方案.md)**

---

## 使用的 Rules


| Rule   | 应用                                                                    |
| ------ | --------------------------------------------------------------------- |
| 中文     | 全文中文                                                                  |
| 先方案后代码 | 本期交付方案文档；线框 08a / HTML Demo 列 Backlog，改码前先过方案                         |
| 照抄官方   | Module / Section / Widget / Variable / Action / COP 以官方为准             |
| 与上下游自洽 | 只吃 L2 Object/Action/Function/Link；决策走 07 Draft→Action；**发布走 09 Apollo** |
| 最小变更   | 反哺 03 只补 §3.4，不重写 L1/L2/AIP 已定稿                                       |


---

## 1. 总体定位

### 1.1 官方一句话

> *Workshop enables application builders to create interactive and high-quality applications for operational users.*  
> 来源：[Workshop Overview](https://www.palantir.com/docs/foundry/workshop/overview/)

产品对外可概括为：

**Workshop is a low-code application builder that lets you create custom applications powered by your Ontology — no frontend engineering required.**

### 1.2 官方三原则（照抄）


| 原则                               | 官方表述要点                                                       | 对 AOS / 本文              |
| -------------------------------- | ------------------------------------------------------------ | ----------------------- |
| **Object data**                  | 以 Object 层为主要构建块；读 Object；写靠 **Actions**；业务逻辑靠 **Functions** | 不吃裸表，只吃 L2              |
| **Consistent design**            | 统一设计系统 · Widget 可干净联动                                        | UI 资产可复用、可培训            |
| **Interactivity and complexity** | 比典型仪表盘更动态；Layouts + Events，目标接近定制 React 体验                   | Application ≠ Dashboard |


### 1.3 核心三句话（对外金句）

1. **Ontology-powered**：Workshop 不吃裸表，只吃 L2 的 Object / Action / Function / Link——这是和 Retool / 帆软的最大区别。
2. **Low-code, not No-code**：拖 Widget + 配变量 + 写少量表达式（官方可到 TS Function），但不用写 React。
3. **Application 操作台**：能触发 Action、调 Function、嵌 AIP——是**操作台**，不是**展示台**。

### 1.4 L3 与交付边界：谁造应用 · 谁嵌 AI · 谁发应用

```text
┌─ 工作台（对标 Workshop）──┐   造应用：Module / Section / Widget + 变量联动
├─ AIP Chat / Assist ───────┤   嵌 AI：侧边对话 + 流程内提问
└─ Apollo（详稿 09）────────┘   发软件 + 发 Module/实施资产 · 灰度 · 气隙
         │
         ▼ 吃的是 L2 名词动词 + 07 决策提议
```

| 构件 | 角色 | 对应 |
| --- | --- | --- |
| **工作台** | 零代码前端工厂 | UI-001~UI-006 |
| **AIP Chat / 业务 Agent** | WorkBuddy | UI-002 |
| **嵌入式 Copilot** | 流程内提问 | UI-005 |
| **Apollo** | 持续交付 OS | [09](09-Apollo交付引擎产品方案.md) · OPS-001~009 |

> **金句：** *工作台造应用，Apollo 发应用；AIP 把决策嵌进应用。* 发布机制 / Hub-Spoke / Ferry / OPS 全部见 **09**，本文不展开。

> **命名边界（与 07 对齐）**：官方 [AIP Assist](https://www.palantir.com/docs/foundry/aip/aip-features/) 首先是**平台导航助手**。官方 Workshop 另有 **[Send to AIP Assist](https://www.palantir.com/docs/foundry/workshop/concepts-events/) 事件**与 **[AIP Chatbot Widget](https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot)**。本文 **UI-005** = 业务「流程内提问」产品形态；**UI-002** = 嵌在工作台的业务 Chatbot（对标 AIP Chatbot Widget + Chatbot Studio Agent）。

### 1.5 官网能力地图 vs 本文覆盖（v1.2 补缺）

| 官网章节 | v1.1 | v1.2 |
| --- | --- | --- |
| Overview 三原则 · Inbox/COP | ✅ | ✅ |
| **Layouts**：Header / **Page** / Section / **Overlay** | △ 仅 Module→Section | ✅ §2 |
| Section 布局：Columns/Rows/Tabs/Flow/Toolbar/**Loop** | ❌ | ✅ §2.2 |
| Widgets 五类 + Object Table 进阶 | △ | ✅ §3.1 补 |
| **Variables** 全类型 · 定义方式 · Lazy · Recompute · Lineage | △ 只有 Selection | ✅ §4 |
| **Module interface**（模块 API / URL / 嵌套传参） | ❌ | ✅ §4.5 |
| **Events**（Layout / Variable / Assist / 开应用） | ❌ 仅原则提到 | ✅ §4.6 |
| Embed module · Loop · 跨模块通信 | ❌ | ✅ §4.5 |
| AIP Chatbot Widget · Send to Assist | △ 自拟两种嵌入 | ✅ §5 对齐官方名 |
| Permissions / Applications Portal | ❌ | ✅ §2.4 简述 |
| Scenarios / Iframe bidirectional | ❌ | §10 Backlog |
| Apollo 发布 | ✅ 迁 09 | 不变 |

---

## 2. 画布结构（官方 Layouts）

> 官方布局构件：[Layouts](https://www.palantir.com/docs/foundry/workshop/concepts-layouts/) —— **Header · Pages · Sections · Overlays**。  
> Overview 写明应用动态性靠 **Layouts + Events**，目标接近定制 React。

### 2.1 四级结构（纠正 v1.1「仅 Section」简化）

```text
工作台 Module（对标 Workshop Module · 资源粒度）
├── Header（跨 Page 持久工具条：标题/Logo/Tabs/按钮 · 可横/竖 · 可折叠）
├── Page 1（多屏工作流画布之一；仅 Header 跨页常驻）
│   ├── Section …（Columns / Rows / Tabs / Flow / Toolbar / Loop）
│   │     └── Widget …
│   └── Overlay（Drawer / Modal · 情境层）
├── Page 2 …
└── …
```

对外「App」多为 **一个或多个 Module** 组合（可经 Applications Portal 策展）；Apollo 发布的 payload 含 Module 资源（详 09）。

| 层级 | 官方定义要点 | 产品含义 |
| --- | --- | --- |
| **Module** | Workshop 资源；编辑三栏：Layout / 画布 / 配置 | 「电商运营台」「知识图谱」 |
| **Header** | 模块级工具条；可设标题/图标/收藏；方向横或竖 | 全局导航、Buddy 入口、发布入口 |
| **Page** | 复杂应用多屏；用 Layout event / Tabs 切换 | Inbox 一屏 · 报表一屏 · 设置一屏 |
| **Section** | Page/Overlay 内分区；可折叠、**条件显隐**、Drop zone | 左筛中表右详 |
| **Overlay** | Drawer（侧滑）/ Modal（居中）；可变量控制显隐 | 详情抽屉、Action 确认层 |
| **Widget** | Section 内最小单元 | Table / Graph / Chat … |

**评审金句：** *造应用的资源粒度是 Module；交互骨架是 Page + Section + Overlay；业务人员打开的是场景页，不是报表文件夹。*

### 2.2 Section 布局选项（官方）

| 布局 | 用途 |
| --- | --- |
| **Columns / Rows** | 纵横分栏；Rows 可滚 |
| **Tabs** | Section 内多 Tab 配置不同 Widget |
| **Flow** | 纵向可滚长页 |
| **Toolbar** | 横条放 Button Group / Metric 等小控件 |
| **Loop** | 对 Object Set/数组 **循环嵌入子 Module**（每条独立作用域） |

另：Section 可配 **Drop Handling**（拖入 Object 写变量/触发 Event）；复制粘贴可选「共用输入变量 / 复制变量」。

### 2.3 样式（简述）

官方提供页/区/Widget 级背景、边框海拔、padding；模块可存色板；可 Toggle light/dark（Event）。非本期差异化重点，实现时跟设计系统，不强行自研主题引擎。

### 2.4 权限与应用入口（官网补一句）

- Module / 用例权限：官方各 Widget 篇均强调 **Permission a use case**——打开应用受 Foundry 权限模型约束（与 Ontology Marking 同源叙事）。  
- **Applications Portal**：可策展对外应用列表（Overview 上页「Curating apps in Applications Portal」）——对标我们 WF-WS-01「工作台 · 应用列表」。
- **Widget 级权限（补强）**：与 Ontology **Markings** 对齐——例如财务类 Widget 仅财务角色可见，普通业务人员不可见（构建态可选、运行态强制过滤）。
- **事件幂等（补强）**：用户重复点击时，同一 Action 只执行一次（06b ACT-07）；前端防抖 + 服务端幂等。

---

## 3. Widget 体系（官方分类 × PRD 对齐）

官方 Widget 大类（[Concepts · Widgets](https://www.palantir.com/docs/foundry/workshop/concepts-widgets/)）：

- Core display widgets  
- Visualization widgets  
- Filtering widgets  
- Event-triggering & navigational widgets  
- Embed Foundry apps

下表按**能力**重组，便于和 03 的 UI-001~UI-006 对齐：

### 3.1 对象展示类（UI-006 / 部分 UI-001）


| 官方 Widget                         | 绑定 L2               | 说明                                                                     |
| --------------------------------- | ------------------- | ---------------------------------------------------------------------- |
| **Object Table**                  | ONT-001 Object Type | 列 = Property；输入 Object Set；输出 **Active object** / **Selected objects** |
| **Object View**                   | ONT-001             | 单对象详情（非表格）；属性分组；可嵌图谱 / 触发 Action                                       |
| **Object List / Object Dropdown** | ONT-001             | 轻量选择器、侧栏                                                               |


> 官方教程标准链路：Filter List → Object Table → Object View 绑 **Active Object** → Button Group 绑 Action。

**Object Table 大数据分页（补强）：** 超过 **1 万行**必须分页/虚拟滚动加载，禁止一次性拉全量（避免前端崩溃）。

**Object Table 官网进阶（补缺）：** 多 Object Type、**Function 衍生列**、Time series 列、OMA 条件格式、**行选触发 Event**、右键自定义 Action、**Inline editing**（单元格写回须配 Editing Action）、观众可自配可见列。详见 [Object Table](https://www.palantir.com/docs/foundry/workshop/widgets-object-table/)。

### 3.2 关系可视化类（UI-001）


| 官方 Widget | 绑定 L2                      | 说明                                |
| --------- | -------------------------- | --------------------------------- |
| **Graph** | ONT-002 Link Type + Object | 边 = Link，节点 = Object；可高亮传导路径（PPR） |
| **Map** 等 | Object + 地理属性              | COP / 态势场景常用                      |


节点右键 → 触发 Action / 打开 Wiki —— 对齐 §3.2.4 交互原则。

### 3.3 交互操作类（UI-003）


| 官方 Widget                  | 绑定 L2               | 说明                                                    |
| -------------------------- | ------------------- | ----------------------------------------------------- |
| **Button Group + Action**  | ONT-003 Action Type | 表单参数 = Action 输入 schema；可 Hidden 参数、默认绑 Active Object |
| **Action Form / Multiple** | ONT-003             | 单条 / 批量写回；走 06b Submission Criteria + 07 HITL         |


**硬约束（与 07 一致）：** Workshop 里直接调 Logic Function ≠ 直接改 Ontology；写回必须顶层是 **Action**。

### 3.4 图表与分析类


| 官方 Widget                  | 绑定 L2                | 说明                    |
| -------------------------- | -------------------- | --------------------- |
| **Metric Card / KPI Tile** | ONT-004 Function 或聚合 | 聚合值 = Function / 汇总结果 |
| **Chart XY 等**             | Object Set + 聚合规则    | 配规则，不写 SQL            |
| **Quiver Embed**           | 嵌入 Foundry 分析应用      | 深度分析场景                |


### 3.5 AIP 嵌入类（UI-002 / UI-005）


| 形态                         | 绑定                | 说明                                       |
| -------------------------- | ----------------- | ---------------------------------------- |
| **AIP Chat Widget**        | AIP-002 Agent     | 侧边栏/底栏；Context = Selection + Ontology 范围 |
| **嵌入式 Copilot（Assist 隐喻）** | AIP-002 + AIP-003 | 附着表格/卡片/表单旁；流程内提问，不切窗口                   |


### 3.6 布局与过滤容器

| 官方能力 | 说明 |
| --- | --- | --- |
| Tab / Column / Container | 复杂布局 |
| **Filter List** | 输出 Object Set Filter，下游 Table 消费 |
| **Conditional Section** | 按权限 / 数据状态显隐 |

### 3.7 Workshop ↔ L2/L3 绑定总表（官方）


| Workshop 概念         | 绑定的 L2/L3 实体        | 说明                              |
| ------------------- | ------------------- | ------------------------------- |
| Object Table / View | ONT-001 Object Type | Widget 列 / 字段 = Object Property |
| Graph               | ONT-002 Link Type   | 边 = Link，节点 = Object            |
| Action Form         | ONT-003 Action Type | 表单参数 = Action 输入 schema         |
| Chart / Metric      | ONT-004 Function    | 聚合值 = Function 计算结果             |
| AIP Chat / Chatbot Widget | AIP-002 Agent | Context = Selection + Ontology · 可读写 Workshop 变量 |
| Wiki 面板             | WIKI-001~004        | 嵌在 Object View 侧边（**行业定制**增强）   |


---

## 4. 变量 · Module Interface · Events（官网核心三件套）

> Overview：应用接近定制 React，靠 **Layouts + Events**；数据流靠 **Variables**。  
> 来源：[Variables](https://www.palantir.com/docs/foundry/workshop/concepts-variables/) · [Events](https://www.palantir.com/docs/foundry/workshop/concepts-events/) · [Module interface](https://www.palantir.com/docs/foundry/workshop/module-interface/)

### 4.1 Input / Output 与 Object Table 输出

> *Input variables define the data passed into a given widget… Output variables define the data passed out…*  
> 来源：[Widgets](https://www.palantir.com/docs/foundry/workshop/concepts-widgets/)

| 变量 | 含义 |
| --- | --- |
| **Active object** | 当前高亮 / 焦点行 |
| **Selected objects** | 多选勾选集（Enable multi-select） |
| **Object set（输入）** | 表格显示什么 |
| **Filter output** | Filter List → Object Set Filter |

### 4.2 官方变量类型全表（补缺）

| 类型 | 用途 |
| --- | --- |
| **Object set** | 一组 Object；可 Filter / Search Around 到 Link |
| **Object set filter** | 属性过滤条件，消费进 Object set |
| String / Numeric / Boolean / Date / Timestamp | 标量 |
| Array / Struct | 数组、结构（Struct 字段不可再嵌套 Struct） |
| GeoPoint / GeoShape | 地理 |
| **Time series set** | 单对象时序 + transform（Metric/Chart/Table 可消费） |

### 4.3 变量定义方式与重算（补缺）

| 定义方式 | 含义 |
| --- | --- |
| **Static** | 手写固定值 |
| **Function** | Function 动态算（ONT-004） |
| **Object set aggregation** | Object Set 聚合 |
| **Object property** | 单对象某属性（复杂低性能属性官方不支持作变量） |
| **Object set definition** | 从 Object Type + filter + 遍历定义 |
| **Variable transformation** | 系列运算/拼接，可引用其他变量 |

**Recompute：** Automatic（默认）· Only when triggered by event · On module load + event。  
**Lazy：** 不可见 Page/Tab/Overlay/Loop 页上的变量**不计算**，直到显示——性能设计硬口径。  
**调试：** Variables 面板 + **Variable lineage graph**（依赖、用处、计算耗时）。  
**Settings 开关（每变量）：** Module interface · Routing · State saving。

### 4.4 产品化叙事（保留）

| 产品话 | 官方落点 |
| --- | --- |
| Selection / Active | Active object / Selected objects |
| 筛选链 | Object set filter → Object set |
| 静态上下文 | Static（用户、日期等） |
| 跨区传参 | 任意类型变量 + Events |

**一句话：** 工作台 **不做 SQL 面板**，做 **变量传递**。L2 Object = 类型；Selection = 运行时实例。

#### 4.4.1 多维度 Selection 上限（补强）

Filter 可同时选「时间范围 + 纯度 + 设备」等多维条件；Table 多选写入 Selected 变量传给 Action/AIP。

| 规则 | 说明 |
| --- | --- |
| **维度上限** | 建议最多 **10 个维度**同时筛选；前端超限拦截并提示 |
| **原因** | 超过后查询组合爆炸，性能指数级下降 |
| **多选对象** | Selected objects 可批量进 Action；仍受 ACT-07 幂等约束 |


### 4.5 Module interface · 嵌套 Module · Loop（补缺）

> Module interface = **模块的 API**：嵌入父模块时可映射、可用 **URL 参数初始化**（[Module interface](https://www.palantir.com/docs/foundry/workshop/module-interface/)）。

| 能力 | 说明 |
| --- | --- |
| Interface 变量 | 给变量加 external ID + 开 Module interface |
| 父子/兄弟通信 | 共享 interface 变量作共同状态（选中对象、Tab、Overlay 开闭） |
| Open Workshop module Event | 打开另一 Module 并映射 interface，免手拼 URL |
| **Loop layout** | 对 Object Set/数组循环嵌入子 Module；每实例独立 scope；可共享 interface 变量 |

→ 产品：列表卡可用 Loop；详情可用 Overlay + interface，不必所有逻辑堆一个巨型 Page。

### 4.6 Events 体系（补缺 · Overview 灵魂另一半）

触发源举例：Button Group、Object Table 行选、Dropdown、Tabs…  
**执行顺序：** 按配置顺序串行；**不等待**前序事件引发的下游重算全部完成（官方限制——复杂链要拆成多次用户触发）。

| 事件类 | 代表 | 产品用途 |
| --- | --- | --- |
| **Layers** | Open/Close Overlay | 开详情抽屉 / Action 层 |
| **Layout** | Switch Page · Expand/Collapse Section · Switch Tab | 多屏工作流、展开 Object View |
| **Variables** | Set / Reset / Recompute | Selection 注入、强制重算 Function 变量 |
| **LLM** | Stream LLM response into variable | 流式写入字符串变量（轻量生成） |
| **AIP Assist** | **Send to AIP Assist** | 打开 Assist 侧栏并送 Prompt（可默认 Chatbot） |
| **Applications** | Open Workshop / Quiver / Object View / Explorer / Notepad / Vertex | 跳出到其他 Foundry 资源 |
| **Data** | Refresh data in module | 整模块刷新 |
| **Appearance** | Toggle light/dark | 主题 |

典型 Inbox：**行选 Event** → Set Active → Open Overlay / Expand Section → Button On click = Action 或再绑 Events。

### 4.7 典型联动链路（官方 Inbox 模式）

```text
用户点 Table 行 / Graph 节点
        ↓（常伴随 Layout/Variable Event）
Active / Selection: Supplier #123
        ↓
Object View / Overlay 绑 Selection → 属性 + Wiki
        ↓
Action「发起尽调」supplierId ← Selection（可 Hidden）
        ↓
Submit → 06b Criteria →（可选）07 HITL → Write-back
```

---

## 5. AIP 在工作台的嵌入（对齐官方 Widget / Event）

### 5.1 模式 A · AIP Chatbot Widget（WorkBuddy / UI-002）

官方：[AIP Chatbot](https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot)

- 独立侧栏/区域；绑定 **Chatbot Studio** 应用变量 ↔ Workshop 变量（声明读写）。  
- 可挂工具：AIP Logic / FoO / 打开其他 Workshop 应用 / Ontology 探索与聚合等。  
- Context：当前 Selection + Module Ontology 范围（产品叙事）。  
- 问完可建议 Action；写回仍须顶层 Action（06b/07）。

### 5.2 模式 B · 流程内提问（UI-005）+ 官方 Assist 事件

| 能力 | 官方 | 我们 UI-005 |
| --- | --- | --- |
| **Send to AIP Assist** Event | 按钮打开 Assist 侧栏并送 Prompt；可选默认 Chatbot | 表旁 💡 / 按钮实现首选 |
| 平台 AIP Assist | 平台导航助手 | **不**等同业务 Copilot；可共侧栏 UX |

产品口径：**Analysis in the flow of work**——不离开操作流提问；实现优先 Event → Assist/Chatbot；可用 Variable Transformation 拼当前 Active Object 进 Prompt。

### 5.3 共享约束

| 约束 | 说明 |
| --- | --- |
| 工具同源 | 优先 AIP-003 Ontology+Wiki；结构化字段优先 |
| 写回同源 | Agent/Assist 只提议；执行走 06b + AIP-004 |
| 权限同源 | 调用用户权限内执行（07） |
| 变量同源 | Chatbot 读写的是普通 Workshop 变量，可驱动其他 Widget |

---
## 6. 官方应用模式 ↔ UI-004 口径

官方明确两种常见模式（[Overview](https://www.palantir.com/docs/foundry/workshop/overview/)）：


| 官方模式                                | 说明                                 | 对 PRD           |
| ----------------------------------- | ---------------------------------- | --------------- |
| **Inbox / Task**                    | 分诊、优先级、关闭告警（Flight Alert Inbox 教程） | UI-003 + UI-006 |
| **COP（Common Operational Picture）** | 墙上大屏态势：地图 + 统计图 + 筛选钻取 + 连到其他视图    | **UI-004**      |


**UI-004 口径（修正）：**  
不是独立「大屏产品线」，而是 **工作台全屏 / COP 布局（Page + Map/Graph + Metric + Selection）**。  
老板问「大屏是啥产品」→ 答：**Workshop COP 应用模式**，不是第三个壳。

---

## 7. 与 Apollo 的边界（详稿已迁至 09）

工作台 Module / App 是 Apollo 可发布的 **payload 之一**（另含平台软件与 FDE 实施资产包）。

| 本层（08） | 交付层（09） |
| --- | --- |
| 造 Module · Widget · Selection · AIP 嵌入 | Hub-Spoke · Channel · Ferry · Delta · 密钥注入 · OPS-001~009 |

**详见：** [09-Apollo交付引擎产品方案](09-Apollo交付引擎产品方案.md) · [03 §3.5 / §3.6](03-对标Palantir-AOS-PRD框架.md)

**金句：** *工作台造应用，Apollo 发应用。*

---

## 8. 典型场景（销售 / 架构评审用）

### 8.1 电商运营台（Inbox + Action）


| Section | Widget                          | 变量                        |
| ------- | ------------------------------- | ------------------------- |
| 左筛      | Filter List（状态/店铺/风控等级）         | Filter → Object Set       |
| 中表      | Object Table（Order / RiskAlert） | Active / Selected         |
| 右详      | Object View + Wiki（行业政策/店铺规则）   | 绑 Active                  |
| 底栏      | Button Group：改价 / 冻结 / 申诉       | 参绑 Active；HITL 待办进 UI-003 |
| 侧边      | AIP Chat（WorkBuddy）             | Context = Active Order    |


### 8.2 知识图谱（本体前端）（Graph + Wiki + Action）


| Section | Widget                | 变量               |
| ------- | --------------------- | ---------------- |
| 中图      | Graph（污染物 → 企业 → 法规）  | 点节点更新 Selection  |
| 右卡      | Object View + Wiki 面板 | 绑 Selection      |
| 操作      | Action Form：立案 / 移交   | 自动注入对象 ID        |
| 辅助      | 嵌入式 Copilot           | 「这条传导链还有哪些遗漏企业？」 |


### 8.3 供应链 COP（UI-004）

全屏：Map/Graph + Metric Tile + Filter；点击工厂节点 → 右侧 Object View + 建议 Action；可选 AIP Chat 解读态势。

---

## 9. 与 03 §3.4 需求表映射


| 需求 ID  | 描述          | Workshop 承载                                      | 优先级 |
| ------ | ----------- | ------------------------------------------------ | --- |
| UI-001 | 图谱 Tab      | Graph Widget + Selection                         | P0  |
| UI-002 | WorkBuddy   | AIP Chat Widget                                  | P0  |
| UI-003 | 运营后台        | Action Form / Button Group + HITL 待办 Module      | P1  |
| UI-004 | 数字孪生大屏      | Workshop 全屏 COP + Graph/Map + Metric + Selection | P2  |
| UI-005 | 嵌入式 Copilot | Assist 隐喻 · 流程内入口                                | P1  |
| UI-006 | 对象卡片视图      | Object View（+ Wiki 侧栏）                           | P1  |


**界面原则：** 展示对象世界，不是裸数据表。

---

## 10. Backlog（线框与 Demo）

按 06a / 07a 节奏，后续交付：


| 交付物                     | 内容                                                                                                | 状态  |
| ----------------------- | ------------------------------------------------------------------------------------------------- | --- |
| **08a-Workshop 线框图.md** | WF-WS-01~08 为主；WF-WS-09 仅入口指针 → 09a | ✅ [08a](08a-Workshop产品设计线框图.md) |
| **HTML Demo**           | WF-WS-01~09 全量页 · 见 foundry/html v1.5.1 | ✅ [foundry/html](foundry/html/) |
| **发布 / Apollo** | Hub-Spoke · Ferry · OPS · FDE 资产 | ✅ 迁至 [09](09-Apollo交付引擎产品方案.md) |
| **官网补缺（v1.2）** | Page/Overlay · Events · Module interface · Loop · 变量全类型 · AIP Chatbot | ✅ 本文 §1.5–§5 |
| **待开高级能力** | Scenarios Widget · Iframe bidirectional 自定义控件 · Applications Portal 策展深页 | Backlog |


建议线框编号（08a 已有 + 可增）：


| ID       | 画面                                            |
| -------- | --------------------------------------------- |
| WF-WS-01 | App / Module 列表（按业务场景）                        |
| WF-WS-02 | Module 画布：Header + Page + Section + Overlay 空态 |
| WF-WS-03 | Object Table + Filter + Active 联动 Object View |
| WF-WS-04 | Graph 传导路径 + 右键 Action                        |
| WF-WS-05 | Action Form（参数自动注入 + HITL 提示）                 |
| WF-WS-06 | AIP Chatbot 侧边栏（Context 芯片）                 |
| WF-WS-07 | Send to AIP Assist / 表旁 💡                   |
| WF-WS-08 | COP 全屏（UI-004）                                |
| WF-WS-09 | 发布入口（示意）→ 09a                                 |
| WF-WS-10 | Module interface + 嵌入子 Module / Loop（可选）    |
| WF-WS-11 | Events 配置面板（行选 → Overlay）（可选）              |


---

## 11. 一致性自检


| 检查项                        | 结论                                        |
| -------------------------- | ----------------------------------------- |
| 是否声称 Workshop 直连 SQL / 裸表？ | **否** · 只认 Object Set / Variable |
| 画布是否只有 Section？ | **否** · Header/Page/Section/Overlay（v1.2） |
| Events / Module interface / Loop？ | **是** · §4.5–§4.6 |
| 变量类型是否完整？ | **是** · §4.2–§4.3 |
| 是否把 Logic 直调当成写回？ | **否** · 顶层须 Action（07 / 06b） |
| UI-004 是否独立产品？ | **否** · COP 布局模式 |
| AIP Assist vs UI-005 | 官方 Assist Event ≠ 业务壳；UI-002 对齐 Chatbot Widget |
| 与 Apollo | 造应用属 08；发应用/舰队/气隙属 **09** |
| 与 Wiki | Object View 侧栏嵌入 WIKI；行业定制增强，不另起壳 |


---

## 12. 修订记录


| 版本   | 日期         | 说明                                                                |
| ---- | ---------- | ----------------------------------------------------------------- |
| v1.0 | 2026-07-15 | 首版：官方三原则 · 画布 · Widget · 变量 · 双 AIP 嵌入 · Apollo · 场景 · 反哺 03 §3.4 |
| v1.0.1 | 2026-07-15 | §10 线框状态：08a 已交付 |
| v1.1 | 2026-07-15 | Apollo 深挖迁出至 09；§7 改为边界指针 |
| v1.2 | 2026-07-15 | **对照官网补缺**：Layouts(Header/Page/Overlay/Loop) · Variables 全类型/Lazy/Recompute · Module interface · Events · AIP Chatbot/Assist Event · Object Table 进阶 · §1.5 能力地图 |
| v1.2.1 | 2026-07-15 | HTML Demo 落地 foundry/html v1.5.0 · 并入 AOS 侧栏「工作台 L3」 |


---

*08 · Workshop · Ontology 零代码前端工厂 · 接续 06/06b/07 · 交付操作台而非仪表盘*