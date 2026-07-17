# 08a · Workshop 产品设计线框图

## Module · Section · Widget · Selection · AIP 嵌入 · COP · Apollo

> **文档性质**：[`08 产品方案`](08-Workshop产品方案.md) 的 **UI/UX 线框规格** · 研发可直接对照实现  
> **版本**：v1.1 · 2026-07-15（对齐 08 v1.2：Page/Overlay/Events 口径）  
> **绘制原则**：对齐官方 Workshop **Header/Page/Section/Overlay** + Widget + 右侧配置；变量联动为主叙事；通用占位符  
> **对标在线**：[Workshop Overview](https://www.palantir.com/docs/foundry/workshop/overview/) · [Layouts](https://www.palantir.com/docs/foundry/workshop/concepts-layouts/) · [Variables](https://www.palantir.com/docs/foundry/workshop/concepts-variables/) · [Events](https://www.palantir.com/docs/foundry/workshop/concepts-events/) · [Getting started](https://www.palantir.com/docs/foundry/workshop/getting-started/) · [Widgets](https://www.palantir.com/docs/foundry/workshop/concepts-widgets/) · [Object Table](https://www.palantir.com/docs/foundry/workshop/widgets-object-table/)  
> **关联**：[08 v1.2](08-Workshop产品方案.md) · [03 §3.4](03-对标Palantir-AOS-PRD框架.md) · [06b](06b-Action与Function产品设计.md) · [07 / 07a](07a-AIP引擎产品设计线框图.md) · [09 Apollo](09-Apollo交付引擎产品方案.md)  
> **HTML Demo**：✅ [foundry/html](foundry/html/) v1.5.1 · `workshop` / `workshop-module` / `workshop-object-view` / `workshop-aip-chat`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 中文 | 线框内按钮、标签、Tab 一律中文 |
| 先方案后代码 | 仅文档；不改业务代码；HTML Demo 单列 Backlog |
| 承接 08 | 映射 08 §10 · WF-WS-01~09（+10/11 可选）· Layouts/Events 口径随 08 v1.2 |
| 通用线框 | `{Module}` `{Object Type}` `{Action}` `{Agent}` `{Selection}` |
| 最小更改 | 新增本文件 + 回写 00 索引 / 08 §10 状态 |
| 与上下游自洽 | 只认 Object Set/Variable；写回顶层 Action；UI-004 = COP 模式 |

---

## 1. 信息架构（IA）

### 1.1 应用地图 · L3 工作台层

```text
┌─ Foundry 工作区 · 工作台 / 应用门户 ────────────────────────────────────────┐
│  [≡]  工作区 ▾   🔍  ⌘J 搜「工作台」   [通知]  [用户]                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  构建                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │ App / Module 列表 │  │ Module 画布编辑器 │  │ Widget 选择器     │          │
│  │ WF-WS-01         │→ │ WF-WS-02         │→ │ + 配置面板        │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
│                                                                              │
│  运行时操作台（同一 Module，不同 Widget 组合）                                  │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│  │ Inbox 三联  │ │ Graph 传导 │ │ Action 表单 │ │ AIP Chat    │               │
│  │ WS-03      │ │ WS-04      │ │ WS-05      │ │ WS-06      │               │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘               │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐                              │
│  │ 嵌入 Copilot│ │ COP 全屏   │ │ Apollo 发布 │                              │
│  │ WS-07      │ │ WS-08      │ │ WS-09      │                              │
│  └────────────┘ └────────────┘ └────────────┘                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 页面对照表（08 §10 → 本文线框）

| 08 ID | 线框 ID | 页面 | UI 映射 | 本章节 |
| --- | --- | --- | --- | --- |
| — | **WF-WS-01** | App / Module 列表 | — | §3 |
| — | **WF-WS-02** | Module 画布空态（Header/Page/Section/Overlay） | — | §4 |
| Inbox 模式 | **WF-WS-03** | Filter + Table + Object View | UI-006 | §5 · **重点** |
| UI-001 | **WF-WS-04** | 知识图谱（本体前端） | UI-001 | §6 |
| UI-003 | **WF-WS-05** | Action Form + HITL | UI-003 | §7 |
| UI-002 | **WF-WS-06** | AIP Chatbot 侧边栏 | UI-002 | §8 |
| UI-005 | **WF-WS-07** | 嵌入式 Copilot / Assist Event | UI-005 | §9 |
| UI-004 | **WF-WS-08** | COP 全屏态势 | UI-004 | §10 |
| Apollo | **WF-WS-09** | 发布入口指针 → 09a | OPS | §11 |
| （可选） | **WF-WS-10/11** | Module interface·Loop / Events 面板 | — | 见 08 §10 |

### 1.3 工作台全局壳（Shell）

> 官方：左侧 **Layout** 面板 · 中央 **画布** · 右侧 **Widget / Section 配置** · 可选底部 Unused widgets。

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ [☰]  工作台     {Module 名称} ▼     [预览] [发布 ▾] [变量 ▾]  🔔  👤       │
├──────────┬───────────────────────────────────────────────────┬───────────────┤
│ Layout   │  面包屑：应用 / {App} / {Module}                    │ 配置面板      │
│          ├───────────────────────────────────────────────────┤               │
│ ▾ Header     │                                                   │ ● Widget 设置 │
│ ▾ Page 1     │              <<  画布：Page · Sections · Overlay >>│ ○ 显示        │
│   Section    │                                                   │ ○ 元数据/JSON │
│    └ Widget  │                                                   │               │
│   Overlay    │                                                   │ 输入变量 ▾    │
│ ▾ Page 2     │                                                   │ 输出变量 ▾    │
│ ─────        │                                                   │ Events ▾     │
│ 变量 / Lineage│                                                   │ Action ▾      │
│ Unused       │                                                   │               │
│  widgets     │                                                   │               │
└──────────┴───────────────────────────────────────────────────┴───────────────┘
```

**预览态**：隐藏 Layout/配置，仅保留运行时交互 + 可选 AIP Chat 抽屉。  
**变量 ▾**：打开变量面板（Object Set / Filter / Active / Selected / Static）。

---

## 2. 线框图例

| 符号 | 含义 |
| --- | --- |
| `[ 按钮 ]` | 可点击 |
| `{占位符}` | 动态字段 |
| `▾` | 下拉 |
| `● / ○` | Tab / 行选中 |
| `🔗 Selection` | 变量联动高亮 |
| `🟡` | HITL / 需审批 |
| `💡` | 嵌入式 Copilot 入口 |
| `🟣` | 行业定制增强（Wiki 面板等） |

---

## 3. WF-WS-01 · App / Module 列表

**路由**：`/workbench` 或应用门户 → 工作台  
**用户目标**：按业务场景找到 / 新建 Module  
**对齐**：08 §2 · 旅程 L 入口

```text
┌─ 工作台 · 应用列表 ────────────────────────────── [+ 新建 Module] ──────────┐
│  🔍 搜索场景…     筛选：全部 ▾  我的 ▾  标签：电商│环科│供应链                 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─ 运营台（电商示例）─────────┐  ┌─ 知识图谱 ────────────────┐           │
│  │ Module · Inbox              │  │ Module · 知识图谱（本体前端）│           │
│  │ 最近：2 小时前 · 已发布 v1.4 │  │ 最近：昨天 · 草稿            │           │
│  │ [打开] [预览] [发布通道…]   │  │ [打开] [预览]                │           │
│  └─────────────────────────────┘  └─────────────────────────────┘           │
│                                                                              │
│  ┌─ 供应链 COP ────────────────┐  ┌─ Flight Alert Inbox（教程样）─┐         │
│  │ Module · 全屏 COP · P2      │  │ Module · 官方 Inbox 模式       │         │
│  │ [打开]                      │  │ [打开]                        │         │
│  └─────────────────────────────┘  └──────────────────────────────┘         │
│                                                                              │
│  提示：Module = 独立业务场景页；不是报表文件夹。                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

**验收**：列表可见场景名 / 发布态；新建进入 WF-WS-02。

---

## 4. WF-WS-02 · Module 画布空态

**路由**：`/workbench/modules/{id}/edit`  
**用户目标**：搭 Section 骨架，再塞 Widget  
**对齐**：08 §2 Layouts（Header/Page/Section/Overlay）· 官方 Add widget / Add section / New page / New overlay

```text
┌─ 编辑 · {Module：电商运营台} ──────── [预览] [保存] [发布 ▾] ─────────────────┐
├─ Layout ────┬─ 画布 ─────────────────────────────────────┬─ 配置 ───────────┤
│ ▾ Header     │                                             │ Page / Section   │
│   图标/标题  │  ┌─ Page：Inbox 主屏 ─────────────────────┐ │ 条件显隐：关     │
│ ▾ Page:Inbox │  │  Section：筛选 [+Widget] [折叠]         │ │                 │
│   筛选       │  │  Section：主表                          │ │ [+ New Overlay] │
│   主表       │  │  Section：详情（可折叠）                 │ │ Overlay=抽屉   │
│   Overlay详情│  └────────────────────────────────────────┘ │ Widget：Table ▾ │
│ ○ Page:设置  │                                             │                 │
│ ─────        │  提示：多屏用 Page；情境层用 Overlay(Drawer/Modal) │                 │
│ 变量 / Events│                                             │                 │
└──────────────┴───────────────────────────────────────────┴─────────────────┘
```

**空态文案**：先定义 **Object Set 变量**，再拖 Widget——否则表格无处取值。

---

## 5. WF-WS-03 · Inbox 三联（Filter + Table + Object View）· 重点

**路由**：预览 / 运行 · `{Module}`  
**用户目标**：分诊告警 / 订单；看详情；准备 Action  
**对齐**：官方 Flight Alert Inbox · 08 §4.3 · UI-006

```text
┌─ {Module：风控告警 Inbox} ─────────────────────────── [💡 Assist] [💬 Buddy] ┐
├─ 筛选 ──────────┬─ 对象表 ─────────────────────────┬─ 对象详情 ────────────┤
│ Filter List     │ Object Table                     │ Object View           │
│                 │ Object set ← Filter 输出 🔗      │ Object ← Active 🔗    │
│ ☑ 状态：异常    │                                  │                       │
│ ☑ 优先级：高    │ ● ORD-8821  超售风险  店铺A  高  │ 标题：ORD-8821        │
│ □ 日期范围 …    │   ORD-8819  物流滞留  店铺B  中  │ 类型：Order           │
│ [允许用户加减筛]│   ORD-8801  价格异常  店铺C  低  │ ─────                 │
│                 │                                  │ 金额  ¥1,280          │
│ 输出：          │ Active → ORD-8821 🔗             │ 店铺  店铺A           │
│ Filter output   │ Selected（多选关）               │ 风控分  0.91          │
│                 │                                  │ ─────                 │
│                 │                                  │ 🟣 Wiki 侧栏 [展开]   │
│                 │                                  │ 店铺规则 · 清关说明…  │
│                 │                                  │                       │
│                 │                                  │ [发起申诉] [冻结] 🟡  │
└─────────────────┴──────────────────────────────────┴───────────────────────┘
│ 变量条：Selection=ORD-8821 · Filter=状态∈{异常} · User={当前用户}            │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 5.1 配置侧（构建态摘录）

| Widget | 输入 | 输出 |
| --- | --- | --- |
| Filter List | Starting Object Set：`{RiskAlert}` | Filter output |
| Object Table | Object set ← Filter output | **Active object** · Selected |
| Object View | Object ← Active object | — |
| Button Group | On click = Action；参数默认 ← Active；可 Hidden | 打开 WF-WS-05 |

**验收**：改 Filter → 表刷新；点行 → 详情刷新；Wiki 可开。

---

## 6. WF-WS-04 · 知识图谱（Object+Link 页面展示）+ 右键 Action

**路由**：`{Module：知识图谱}` · Graph Section  
**用户目标**：浏览本体关系图；从节点开详情 / 触发 Action  
**对齐**：UI-001 · 08 §3.2 · 本体层前端（配置在 OMA，展示在工作台）

```text
┌─ 知识图谱 · Graph ───────────────────────────────────────── [💬 Buddy] ───┐
├─ Graph ────────────────────────────────────────┬─ 对象卡片 / Wiki ──────────┤
│                                                │ Object View ← Selection 🔗 │
│         (污染物P)                              │                            │
│            │ Link:影响                         │ {企业名称}                 │
│            ▼                                   │ 信用代码 …                 │
│     ●(企业E)─── Link:适用 → (法规R)            │ ─────                     │
│       ▲ 高亮路径                               │ 🟣 Wiki：排放限值 / 条款   │
│                                                │                            │
│ 图例：Object=节点  Link=边  ●=Selection        │ 右键菜单（节点上）：        │
│ [力导向 ▾] [层级] [适配画布]                   │  · 设为焦点（更新 Selection）│
│                                                │  · 打开对象视图            │
│                                                │  · 触发 Action ▾           │
│                                                │  · 在 Wiki 中打开 🟣      │
└────────────────────────────────────────────────┴────────────────────────────┘
```

**验收**：点节点 → 右侧刷新；右键 Action → 进入 WF-WS-05 且参数已注入对象 ID。

---

## 7. WF-WS-05 · Action Form（参数自动注入 + HITL）

**路由**：Button / 右键 Action → 模态或底部表单  
**用户目标**：确认写回；走 Criteria / 审批  
**对齐**：UI-003 · 06b · 07 Draft/HITL · 08 §3.3

```text
┌─ Action · {发起尽调} ──────────────────────────────────────────── [×] ─────┐
│  来源：Object View / Graph 右键 · Selection = Supplier #123 🔗               │
│                                                                              │
│  参数（schema = ONT-003）                                                    │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ supplierId     [ Supplier #123        ]  👁 Hidden（已绑 Active）       │ │
│  │ 尽调级别       [ 标准 ▾ ]                                               │ │
│  │ 说明           [ ________________________ ]                             │ │
│  │ 附件           [ + 上传 ]                                               │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  🟡 Submission Criteria 预检：通过 · 将进入 HITL（AIP-004）                   │
│  提示：顶层必须是 Action；不可用「仅调 Logic」替代写回。                       │
│                                                                              │
│                         [取消]                    [提交 · 送审] 🟡            │
└──────────────────────────────────────────────────────────────────────────────┘
```

**批量态（Action Multiple）**：Selected objects = N 行；参数共用；列表展示将生效对象。

**验收**：Hidden 参数来自 Selection；提交后待办出现在运营后台 Module。

---

## 8. WF-WS-06 · AIP Chat 侧边栏（WorkBuddy / UI-002）

**路由**：顶栏 `[💬 Buddy]` 或 AIP Chat Widget Section  
**用户目标**：带着当前 Selection 问 Agent；可委托任务  
**对齐**：08 §5.1 · 07a WF-AIP-09 · UI-002

```text
┌─ Module 主画布（Inbox/Graph…） ──────────────┬─ AIP Chat · WorkBuddy ───────┐
│                                              │ Agent：{风控 Buddy} ▾         │
│          <<  现有 Widget 保持  >>             │ Context 芯片：                │
│                                              │  [Selection: ORD-8821 ×]     │
│                                              │  [Ontology: Order+Wiki ×]    │
│                                              │ ─────                       │
│                                              │ Buddy：这单风控分偏高，主要  │
│                                              │ 因为近 7 日退货率与库存…     │
│                                              │ 引用：Order.riskScore ·      │
│                                              │ Wiki「店铺A清关规则」🟣      │
│                                              │                              │
│                                              │ 建议：[打开申诉表单] 🟡       │
│                                              │        [查看 Lineage]         │
│                                              │ ─────                       │
│                                              │ 你：@Buddy 帮我发起申诉       │
│                                              │ [发送]                       │
└──────────────────────────────────────────────┴──────────────────────────────┘
```

**验收**：切换 Active 行 → Context 芯片更新；建议 Action 打开 WF-WS-05；不直写 Ontology。

---

## 9. WF-WS-07 · 嵌入式 Copilot（UI-005）

**路由**：表格列头 / 卡片字段旁 `💡`  
**用户目标**：不切 Chat 窗，在操作流里问  
**对齐**：08 §5.2 · Analysis in the flow of work

```text
┌─ Object Table ───────────────────────────────────────────────────────────────┐
│  订单号      状态     风控分 💡    店铺        操作                           │
│  ☑ ORD-8821  异常     0.91        店铺A       …                              │
│  ☑ ORD-8819  异常     0.72        店铺B       …                              │
│  ☐ ORD-8801  正常     0.21        店铺C       …                              │
│                                                                              │
│  已选 2 行 · Selected objects 🔗                                             │
│                                                                              │
│  ┌─ 💡 流程内提问 ────────────────────────────────────────────── [×] ────┐ │
│  │  上下文：Selected = ORD-8821, ORD-8819 · 不离开表格                     │ │
│  │  问：这批里哪些可能超售？请高亮并给建议 Action                           │ │
│  │  答：ORD-8821 命中超售特征…  [高亮行] [建议：冻结库存] 🟡               │ │
│  │                                              [在 Buddy 中打开完整对话]   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

**与 WF-WS-06 关系**：共享 Agent + AIP-003；07 是轻量入口，06 是完整对话态。

**验收**：多选有效；回答可驱动行高亮；写回仍进 Action Form。

---

## 10. WF-WS-08 · COP 全屏（UI-004）

**路由**：`{Module：供应链 COP}` · 布局模式 = 全屏 / 墙上屏  
**用户目标**：态势感知 + 钻取到单对象 + 联动 Action  
**对齐**：官方 Common Operational Picture · 08 §6 · **非独立大屏产品**

```text
┌─ COP · 供应链态势 全屏 ──────────────────────────────── [退出全屏] [💬] ───┐
│  ┌ Metric ┐ ┌ Metric ┐ ┌ Metric ┐ ┌ Metric ┐                               │
│  │在途订单│ │缺货 SKU│ │周转天数│ │风险工厂│  ← Function / 聚合 绑定       │
│  │ 12,480 │ │   86  │ │  18.2 │ │   3   │                               │
│  └────────┘ └────────┘ └────────┘ └────────┘                               │
├─ Map / Graph（主视觉）─────────────────────────┬─ 钻取面板 ────────────────┤
│                                                 │ Filter pills …            │
│      [工厂F]───链路───[仓W]───[门店S]            │ Object View ← Selection 🔗│
│         ● Selection                             │ {工厂F} 库存 / SLA …      │
│                                                 │ [调拨 Action] 🟡          │
│                                                 │ [打开 Inbox Module]       │
└─────────────────────────────────────────────────┴──────────────────────────┘
│ Selection 驱动：点工厂 → 指标局部刷新（可选）→ 右侧详情 → Action 参注入      │
└──────────────────────────────────────────────────────────────────────────────┘
```

**老板口径金句**：这是工作台的 **COP 布局模式**，不是第三个壳。

---

## 11. WF-WS-09 · 发布入口（指针 · 详稿 09 / 09a）

**路由**：Module 顶栏 `[发布 ▾]` → 跳转 / 抽屉打开 Apollo 通道  
**对齐**：[09 Apollo](09-Apollo交付引擎产品方案.md) · [09a](09a-Apollo交付引擎产品设计线框图.md) **WF-AP-02/03**  
**本页只保留入口语义**，不展开 Hub-Spoke / Ferry / 舰队。

```text
┌─ 发布 · {电商运营台} ──────────────────────────────────────────── [×] ─────┐
│  当前版本：Module rev `a3f2…`                                                │
│  目标通道：○ 开发  ● 试点(beta)  ○ 区域  ○ 全量(stable)   ← OPS-004          │
│  [推送到试点]  [打开 Apollo Spoke 详情…]  [Ferry 气隙向导…]                   │
│                                                                              │
│  💡 舰队健康 / Delta / 密钥注入 / FDE 资产包 → 见 09 产品方案 · 09a 线框      │
└──────────────────────────────────────────────────────────────────────────────┘
```

**验收**：业务人员知道「发布」走交付引擎；不在工作台内伪造完整 Apollo 控制台。

---

## 12. 用户旅程线框串联

> 编号接续 07a 旅程 I / J / K。

### 12.1 旅程 L · Inbox 分诊写回（电商）

```text
WF-WS-01 打开「电商运营台」
  → WF-WS-03 Filter 筛异常 → 点行
  → Object View + Wiki
  → [发起申诉] WF-WS-05（参自动注入）
  → 🟡 HITL → 06b Criteria → Write-back
  → （可选）07a WF-AIP-07 Lineage 复盘
```

### 12.2 旅程 M · 知识图谱 + Buddy

```text
WF-WS-01「知识图谱」
  → WF-WS-04 点企业节点 → Selection
  → 右键 Action 或 🟣 Wiki
  → WF-WS-06 @Buddy「还有哪些遗漏关联？」
  → 建议高亮 → WF-WS-05 立案 / 写回
```

### 12.3 旅程 N · 流程内 Copilot + COP

```text
WF-WS-03 多选订单 → WF-WS-07 💡「哪些可能超售？」
  → 高亮 + 建议冻结
  → WF-WS-05 批量 Action
  → （态势）WF-WS-08 COP 看库存 → 钻取回 Inbox
  → WF-WS-09 发布入口 →（详）09 / 09a Apollo 通道
```

---

## 13. 组件清单（研发）

| 组件 ID | 名称 | 出现页面 | 说明 |
| --- | --- | --- | --- |
| CMP-WS-SHELL | 工作台三栏壳 | 全编辑页 | Layout / 画布 / 配置 |
| CMP-WS-SECTION | Section 容器 | 02~08 | 折叠 · 条件显隐 · 列宽 |
| CMP-WS-OBJ-TABLE | Object Table | 03 · 07 | Active / Selected 输出 |
| CMP-WS-FILTER | Filter List | 03 | Filter → Object Set |
| CMP-WS-OBJ-VIEW | Object View | 03 · 04 · 08 | 绑 Selection |
| CMP-WS-WIKI-PANE | Wiki 侧栏 🟣 | 03 · 04 | 行业定制增强 |
| CMP-WS-GRAPH | Graph Widget | 04 · 08 | 边=Link 节点=Object |
| CMP-WS-ACTION-FORM | Action Form | 05 | schema=ONT-003 · Hidden 参 |
| CMP-WS-BTN-GROUP | Button Group | 03 · 05 | On click = Action |
| CMP-WS-AIP-CHAT | AIP Chat 侧栏 | 06 | Context 芯片 |
| CMP-WS-COPILOT-TIP | 嵌入式 💡 | 07 | 流程内提问浮层 |
| CMP-WS-METRIC | Metric Tile | 08 | Function / 聚合 |
| CMP-WS-VAR-BAR | 变量条 / 面板 | 全预览 | Selection 可视 |
| CMP-WS-PUBLISH | Apollo 发布抽屉 | 09 | 灰度档位 |

---

## 14. 与 08 / 03 / 07 一致性自检

| 检查项 | 结论 |
| --- | --- |
| 线框是否出现裸 SQL / 裸表配置？ | **否** · 只出现 Object Set / Variable |
| Selection 是否贯穿 03/04/05/06/07/08？ | **是** · 灵魂箭头 |
| UI-004 是否画成独立产品壳？ | **否** · WF-WS-08 标注 COP 布局 |
| Chat vs Copilot | 06=侧栏完整对话；07=表旁轻量；共享 Agent |
| 写回 | 05 明确顶层 Action + HITL；对齐 06b/07 |
| Wiki | Object View 侧栏 🟣；非独立应用 |
| Apollo | 详稿 09；WF-WS-09 仅入口指针 → 09a |
| 旅程编号 | L/M/N 接续 07a I/J/K |

---

## 15. HTML Demo ↔ 线框对照（v1.5.1 全量）

> **分层**：WF-WS-01 应用列表 = 唯一入口；运营台 / 知识图谱 = 列表内 Module。知识图谱 = Ontology Object+Link+Wiki 的**页面端展示**（配置仍在 OMA）。

| 线框 ID | 画面 | Demo 页 | 状态 |
| --- | --- | --- | --- |
| **WF-WS-01** | App / Module 列表 | `workshop.html` | ✅ |
| **WF-WS-02** | Module 画布空态 | `workshop-canvas.html` | ✅ |
| **WF-WS-03** | Inbox 三联（运营台） | `workshop-module.html` | ✅ |
| **WF-WS-04** | 知识图谱 Graph | `workshop-object-view.html` | ✅ |
| **WF-WS-05** | Action Form + HITL | 同上页内弹层 | ✅ 合页 |
| **WF-WS-06** | AIP Chat Buddy | `workshop-aip-chat.html` | ✅ |
| **WF-WS-07** | 嵌入式 Assist 💡 | 同上页内浮层 | ✅ 合页 |
| **WF-WS-08** | COP 全屏 | `workshop-cop.html` | ✅ |
| **WF-WS-09** | 发布入口 → 09 | `workshop-publish.html` | ✅ 指针 |
| WF-WS-10/11 | Module interface / Events 面板 | — | ⏳ 可选未开 |

首页 `index.html`：工作台区仅突出 **应用列表**；下方为「列表内 Module 示例」，避免运营台与列表平级。

## 16. 变更记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-15 | 初稿：WF-WS-01~09 · Inbox/Graph/Action/AIP/COP/Apollo · 旅程 L/M/N · 组件清单 |
| v1.1 | 2026-07-15 | 对齐 08 v1.2：Header/Page/Overlay · Events 口径；WF-WS-02/壳/对照表更新 |
| v1.2 | 2026-07-15 | 政策审查→**知识图谱**；Demo v1.5.1 与 WF-WS-01~09 一一对齐；首页层级修正 |

---

*08a · 工作台线框 · 操作台不是仪表盘 · Selection 驱动一切*
