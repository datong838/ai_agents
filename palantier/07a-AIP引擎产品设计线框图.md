# 07a · AIP 产品设计线框图

## k-LLM · AIP Logic · Chatbot Studio · Draft / Lineage

> **文档性质**：[`07 产品方案`](07-AIP引擎k-LLM与AgentStudio产品方案.md) 的 **UI/UX 线框规格** · 研发可直接对照实现  
> **版本**：v1.0 · 2026-07-14  
> **绘制原则**：布局对齐 AIP Logic 三栏 UI · Agent Studio 配置面 · Automate 提案台；通用占位符；**重点展开成熟度楼梯 + Agent 工具面板**  
> **对标在线**：[Logic Getting Started](https://www.palantir.com/docs/zh/foundry/logic/getting-started/) · [Logic↔Automate](https://www.palantir.com/docs/zh/foundry/logic/aip-logic-integration-automate/) · [Platform overview](https://www.palantir.com/docs/foundry/platform-overview/overview/index.html)  
> **关联**：[07 §5b / §8](07-AIP引擎k-LLM与AgentStudio产品方案.md) · [07b Capability](07b-Capability-Adapter重能力接入.md) · [06b Action](06b-Action与Function产品设计.md) · [06a](06a-语义本体Ontology-Mapping产品设计线框图.md) · [03 §3.3](03-对标Palantir-AOS-PRD框架.md)  
> **HTML Demo**：✅ [foundry/html](foundry/html/) v1.6.3 · 含 `aip-capabilities`

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 | 线框内按钮、标签、Tab 一律中文 |
| 先方案后代码 | 仅文档；不改业务代码 |
| 承接 07 | 映射 §8 页面清单 · §5b 成熟度 / 六工具 · §3 Logic 三栏 |
| 通用线框 | `{Agent}` `{Logic RID}` `{Object Type}` `{Action}` `{Model}` |
| 最小更改 | 新增本文件 + 回写 00 索引 / 07 线框链接 |

---

## 1. 信息架构（IA）

### 1.1 应用地图 · AIP 层

```text
┌─ Foundry 工作区 · AIP 应用群 ────────────────────────────────────────────────┐
│  [≡]  工作区 ▾   🔍  ⌘J 搜「AIP」   [通知]  [用户]                           │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  模型层                         逻辑层                    代理层              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │ 模型路由中心       │  │ AIP Logic        │  │ Chatbot Studio   │          │
│  │ + Artifacts/Adapter│ │ 画布 · Debug · Ev│  │ Agent 配置 / 部署 │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
│                                                                              │
│  治理与交付                                                                   │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│  │ 提案/Draft │ │ Lineage    │ │ Evals 门控  │ │ Workshop   │               │
│  │ 审批台     │ │ 决策溯源   │ │            │ │ Agent 组件 │               │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘               │
│                                                                              │
│  入门楼梯（横切）                                                             │
│  ┌──────────────────────────────────────────────────────────────────────────┐│
│  │ 成熟度楼梯 L1→L4 · Threads → Agent → Workshop → Function/Automate       ││
│  └──────────────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 页面对照表（07 §8 → 本文线框）

| 07 ID | 线框 ID | 页面 | 本章节 |
|-------|---------|------|--------|
| — | **WF-AIP-00** | 成熟度楼梯（横切导航） | §3 · **重点** |
| AIP-01 / 05b | **WF-AIP-01a/b** | 供应商接入 + 路由策略（两屏） | §4 |
| AIP-02 / 03 | **WF-AIP-02** | AIP Logic 画布（三栏） | §5 |
| AIP-04 | **WF-AIP-04** | 工具注册（Logic 侧） | §6 附 |
| AIP-05 | **WF-AIP-05** | Chatbot Studio 配置壳 | §6 |
| AIP-05 · Tools | **WF-AIP-05T** | **Agent 工具面板** | §7 · **重点** |
| AIP-05 · Cap | **WF-AIP-05C** | **重能力接入（Capability）** | §7.4 · [07b](07b-Capability-Adapter重能力接入.md) |
| AIP-06 | **WF-AIP-06** | 提案 / Draft 审批台 | §8 |
| AIP-07 | **WF-AIP-07** | Decision Lineage 详情 | §9 |
| AIP-08 | **WF-AIP-08** | Evals 门控 | §10 |
| — | **WF-AIP-09** | Workshop · Agent 组件 | §11 |

### 1.3 AIP 全局壳（Shell）

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ [☰]  AIP          🔍 Logic / Agent / 模型…     [成熟度 ▾ L2]  🔔  👤       │
├──────────┬───────────────────────────────────────────────────────────────────┤
│ 侧栏     │  面包屑：AIP / {Logic|Agent 名称} / {子页}                         │
│          ├───────────────────────────────────────────────────────────────────┤
│ 成熟度   │                                                                   │
│  └ L1–L4 │                    <<  主内容区  >>                                │
│ ─────    │                                                                   │
│ 模型     │                                                                   │
│  Logic   │                                                                   │
│  Agents  │                                                                   │
│  提案    │                                                                   │
│  Lineage │                                                                   │
│  Evals   │                                                                   │
└──────────┴───────────────────────────────────────────────────────────────────┘
```

**顶栏「成熟度 ▾」**：显示当前工作区主路径所在层（如配置 Agent = L2；挂 Workshop = L3）；点击打开 WF-AIP-00。

---

## 2. 线框图例

| 符号 | 含义 |
|------|------|
| `[ 按钮 ]` | 可点击 |
| `{占位符}` | 动态字段 |
| `▾` | 下拉 |
| `● / ○` | Tab 选中 / 未选 |
| `🟡` | HITL / Draft / 需审批 |
| `🟢` | 已 Eval / 可生产 |
| `🟣` | 谛听增强（Wiki Tool 等） |
| `┌─┐` 楼梯格 | 成熟度一层 |

---

## 3. WF-AIP-00 · 成熟度楼梯（重点）

**路由**：`/aip/maturity` 或顶栏「成熟度」面板  
**用户目标**：理解从探索 → 生产自动的路径；按层跳转到对应产品入口  
**对齐**：07 §5b.3 · 旅程 K

```text
┌─ AIP Agent 成熟度楼梯 ──────────────────────────────────── [关闭] ─────────┐
│  一句话：别一上来就做 L4。先 Threads，再固化 Agent，再嵌应用，最后才自动化。   │
│                                                                              │
│     L1 临时分析              L2 任务 Agent           L3 Agentic 应用          │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐          │
│  │ AIP Threads     │ →  │ Chatbot Studio  │ →  │ Workshop / OSDK │          │
│  │ 拖文档 · 即问即答│    │ Prompt·工具·上下文│    │ Agent 组件·变量 │          │
│  │                 │    │                 │    │                 │          │
│  │ [打开 Threads]  │    │ [打开 Studio]   │    │ [Workshop 模板] │          │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘          │
│                                      │                    │                   │
│                                      │                    ▼                   │
│                                      │         ┌─────────────────┐          │
│                                      └───────→ │ L4 自动化 Agent │          │
│                                                │ 发布为 Function │ 🟡       │
│                                                │ + Automate/定时 │          │
│                                                │ 须 Eval+Draft   │          │
│                                                │ [检查门控 →]    │          │
│                                                └─────────────────┘          │
├──────────────────────────────────────────────────────────────────────────────┤
│  当前工作区：{维修派单 Buddy}     判定层：● L2   下一推荐：挂 Workshop → L3    │
│  门禁： Eval ○未跑   Draft 策略 ●默认暂存   执行范围 ●用户范围                │
│  [标记升级到 L3]  [申请 L4 上线评审]                                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 楼梯侧栏迷你版（持久）

```text
┌ 成熟度 ┐
│ ● L1   │  Threads
│ ◆ L2   │  ← 你在这里
│ ○ L3   │  Workshop
│ ○ L4   │  🔒 需门控
└────────┘
```

### 3.2 层 → 入口映射

| 层 | 主入口线框 | 退出条件（可升层） |
|----|------------|-------------------|
| L1 | Threads（外链/轻页） | 有可复用对话模式 |
| L2 | WF-AIP-05 | 工具+上下文齐 · 试对话通过 |
| L3 | WF-AIP-09 | 变量绑定完成 · 一线试用 |
| L4 | WF-AIP-08 + WF-AIP-06 | Eval 绿 · Draft 策略确认 |

---

## 4. WF-AIP-01 · 模型路由 / 供应商接入（两屏）

> **2026-07-17：** 拆成 **接入** 与 **路由** 两屏（学 Dify 卡片+类型化表单，不搬 Marketplace）。Demo：ip-model-providers.html · ip-model-router.html。

### 4.1 WF-AIP-01a · 模型供应商（接入）

**路由**：/aip/model-providers · Demo：ip-model-providers.html

`	ext
┌─ 模型供应商 ────────────────────────────────── [Adapter 管理] [路由策略 →] ─┐
│  已接入：卡片（配置 / 管理凭据）                                              │
│  可接入类型：OpenAI兼容 · Azure · Anthropic · vLLM · 自定义 Adapter（卡片）   │
│  点卡片 → 展开【该类型 Schema 表单】→ 测连通 → 保存启用                       │
│  （无外链 Marketplace / 无安装量刷屏）                                        │
└──────────────────────────────────────────────────────────────────────────────┘
`

### 4.2 WF-AIP-01b · 模型路由策略

**路由**：/aip/models · Demo：ip-model-router.html

`	ext
┌─ 模型路由策略 ────────────────────────────── [模型供应商（接入）] ───────────┐
│  任务类型              首选模型              回退              出境            │
│  摘要/分类             {私有-小模} ▾          {私有-中} ▾      禁公网 ☑       │
│  业务问答+Wiki         {私有-中} ▾           —                禁公网 ☑       │
│  复杂推演/长 CoT       {高能力} ▾            {私有-中} ▾      审批后 ⚠       │
│  Logic 块默认          {按块覆盖} ▾          —                继承            │
│                                                                              │
│  熔断：主模连续失败 ≥3 → 自动切回退 · [演练] · 预热状态                        │
│  [保存策略]  [导出审计快照]                                                   │
└──────────────────────────────────────────────────────────────────────────────┘
`

**Adapter 抽屉（高级，挂在供应商页）：**

`	ext
┌─ Model Adapter: {my-llm} ────────────────────────────────────────────────────┐
│  Artifacts: [容器: my-llm:1.2] 或 [Source API 端点]                           │
│  加载 / 初始化 / 推理钩子： [查看 TypeScript]                                  │
│  可用于：☑ AIP Logic  ☑ Agents  ☑ PB Use LLM                                  │
│  [发布到平台]                                                                 │
└──────────────────────────────────────────────────────────────────────────────┘
`

---

## 5. WF-AIP-02 · AIP Logic 画布（三栏）

**路由**：`/aip/logic/{rid}`  
**对齐**：07 §3.0 · 官方入门三栏

```text
┌─ AIP Logic: {dispatch_repair_agent} ── 模型路由: k-LLM ▾ ── [Eval] [发布] ─┐
│  Tab: ● 编排  ○ 自动化(Uses)  ○ 运行历史  ○ 版本                            │
├────────────────────────────┬─────────────────────┬───────────────────────────┤
│ ① 输入 · 块 · 输出         │ ② 调试器            │ ③ 运行面板                │
│                            │                     │                           │
│ [Input]                    │ ▼ Use LLM 块 CoT    │ 示例入参                  │
│  name: device             │  思考: 温升超阈…     │ device = {DEV-019} ▾     │
│  type: Object · Device     │  工具请求: Query…   │ [▶ 运行]                  │
│                            │  提议 edits: 🟡 派单 │                           │
│ [Get Object Attributes]    │  （场景预览·不落库） │ 最近运行                  │
│  + status, alarm, 🟣Wiki   │                     │ · 14:02 成功 · [打开]     │
│                            │ [折叠块卡] [清工具]  │ · 13:55 失败 · [打开]     │
│ [Use LLM] ←─── 核心        │                     │                           │
│  Prompt…  [/ 插入变量]     │                     │ [保存为单元测试]          │
│  Tools: [配置 →05T样式]    │                     │                           │
│  块模型: {私有-中} ▾       │                     │ 右侧栏 · Uses             │
│  out: diagnosis            │                     │ [+ 创建自动化]            │
│                            │                     │ ⚠ 须输出 Ontology edits   │
│ [Transform] JSON→参数      │                     │                           │
│ [Apply Action Block]? 🟡   │                     │                           │
│                            │                     │                           │
│ Output: ● Ontology edits   │                     │                           │
│         ○ 值(string/obj)   │                     │                           │
└────────────────────────────┴─────────────────────┴───────────────────────────┘
│ 状态条：未发布 · 执行范围 ●用户范围  ○项目范围(需授权) · A-07 试跑不落库     │
└──────────────────────────────────────────────────────────────────────────────┘
```

**块工具条（添加到画布）：**

```text
[+ Create Variable] [+ Get Attributes] [+ Use LLM] [+ Transform]
[+ Apply Action Block] [+ Execute Function]
```

---

## 6. WF-AIP-05 · Chatbot Studio 配置壳

**路由**：`/aip/chatbots/{id}`  
**对齐**：07 §5b

```text
┌─ Chatbot Studio · {维修派单 Buddy} ──── 成熟度 ◆ L2 ── [试对话] [发布] ────┐
│  Tab: ● 配置  ○ 工具  ○ 上下文  ○ 记忆/State  ○ 部署  ○ 版本               │
├──────────────────────────────┬───────────────────────────────────────────────┤
│ 左侧 · 核心参数               │ 右侧 · 试对话                                 │
│                              │                                               │
│ 模型: {私有-中} ▾            │  用户: 这台设备要不要派单？                     │
│ 温度: [====·===] 0.2         │  Agent: 已查 Wiki+告警… 建议派单 🟡            │
│                              │       [查看工具调用] [打开 Lineage]            │
│ System Prompt                │  ─ 需澄清 ─                                   │
│ ┌──────────────────────────┐ │  Agent: 夜班是否可接？ [Request Clarification]│
│ │ 你是维修调度助手…        │ │  用户: [可以] [不行]                          │
│ │ 优先读 🟣 Wiki 字段…     │ │                                               │
│ │ [/ 引用工具或变量]       │ │                                               │
│ └──────────────────────────┘ │                                               │
│                              │                                               │
│ 工具调用模式                 │                                               │
│  ○ Prompted（单次一工具）    │                                               │
│  ● Native（并行·部分模型）   │                                               │
│                              │                                               │
│ 已挂工具: 4  [打开工具面板→] │                                               │
│  Action·Query·Function·Clarify│                                              │
└──────────────────────────────┴───────────────────────────────────────────────┘
```

### 6.1 上下文 / State 子页摘要

```text
上下文源:
  ☑ Ontology · 返回最多 [20] 条 Object
  ☑ 文档向量库 {维修手册 MediaSet}
  ☐ Function-based 语义检索 {similar_incidents}
  🟣 优先 Wiki 结构化字段（AIP-003）

Application State:
  | 名        | 类型        | 初值 / 绑定来源        |
  | ticket_id | String      | Workshop 输入框        |
  | devices   | Object Set  | 当前选中对象集         |
```

### 6.2 部署 Tab

```text
☑ 平台内部可用
☑ Workshop 组件 · 模块 {maintenance_ops}
☐ OSDK 应用
☐ 第三方 API

L4 发布为 Function: [ ] 启用  → 须 WF-AIP-08 绿 + Draft 默认
```

---

## 7. WF-AIP-05T · Agent 工具面板（重点）

**入口**：Chatbot Studio Tab「工具」· 或 Logic Use LLM「Tools」配置（子集）  
**对齐**：07 §5b.4 六类工具

```text
┌─ Agent 工具面板 · {维修派单 Buddy} ─────────────────── 模式: Native ▾ ─────┐
│  提示：LLM 只「请求」工具；平台以调用用户权限代调（A-08）。写路径默认可提案。 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─ 工具目录（六类）─┐  ┌─ 已启用 ──────────────────────┐  ┌─ 配置细项 ───┐│
│  │                    │  │                              │  │              ││
│  │ ☑ Action           │  │ 1. Action                    │  │ Action:      ││
│  │ ☑ Object Query     │  │    派单维修 {create_wo}      │  │ {create_wo}  ││
│  │ ☑ Function         │  │    HITL: ●确认后执行 ○自动   │  │              ││
│  │ ☐ Update App Var   │  │                              │  │ 何时使用:    ││
│  │ ☐ Command          │  │ 2. Object Query              │  │ 「故障确定…」││
│  │ ☑ Request Clarify  │  │    Device · 属性子集…        │  │              ││
│  │                    │  │                              │  │ 参数映射:    ││
│  │ 🟣 Wiki Field Tool │  │ 3. Function                  │  │ device←input ││
│  │   （谛听 · Query子集）│ │    health_score / Logic…    │  │ crew←LLM出参 ││
│  │                    │  │                              │  │              ││
│  │                    │  │ 4. Request Clarification     │  │ Criteria:    ││
│  │                    │  │    暂停 · 向用户要澄清        │  │ 过 06b 壳    ││
│  └────────────────────┘  └──────────────────────────────┘  └──────────────┘│
│                                                                              │
│  [+ 添加 Action] [+ 添加 Query] [+ 添加 Function] [+ 添加 Clarify]           │
│                                                                              │
│  Logic 侧对照（Use LLM 工具四类）:                                           │
│  Apply Action · Call Function · Query Objects · Calculator                   │
│  （Agent 多出：Update Variable · Command · Request Clarification）            │
│                                                                              │
│  [保存]  [在试对话中验证工具调用]                                            │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 7.1 单工具卡片展开 · Action

```text
┌─ 工具卡 · Action ────────────────────────────────────────────────────────────┐
│  Action Type: [派单维修 ▾]     RID: {ri.action…}                             │
│  执行策略:  ○ 对话中自动提交   ● 弹出 Action 表单供人确认   ○ 仅生成 Draft    │
│  说明给 LLM: 「仅当严重级≥高且用户未否决时调用」                              │
│  链接: [打开 06b Action 编辑器]                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 单工具卡片 · Request Clarification

```text
┌─ 工具卡 · Request Clarification ─────────────────────────────────────────────┐
│  触发示例句: 「信息不足时先问，不要猜」                                        │
│  UI: 对话气泡暂停 + 快捷回复 chips（可配）                                    │
│  恢复: 用户回答写入上下文 → 继续推理                                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Object Query 属性子集（控词元）

```text
Object Type: Device
属性: ☑ id  ☑ status  ☑ alarm_code  ☑ 🟣 wiki.risk_level  ☐ raw_payload
链接遍历深度: [1] ▾    过滤: status != retired
```

### 7.4 WF-AIP-05C · 重能力接入（Capability）

> 详规：[07b](07b-Capability-Adapter重能力接入.md)。与模型供应商同范式：卡片 + 类型化表单；**不**搬 Marketplace。

```text
┌─ 重能力接入 ────────────────────────── [登记 Adapter] [工具面板 →] ─┐
│ 已接入：短视频 Job · 直播稿 · 电商数字人 · 教育数字人                 │
│ 可接入：Media Job · Script Engine · Avatar Session · HTTP Adapter   │
│ 工具侧：Call Capability · kind=sync|job|session · 写回经 Action     │
└─────────────────────────────────────────────────────────────────────┘
```

Demo：`aip-capabilities.html`

---

## 8. WF-AIP-06 · 提案 / Draft 审批台

**路由**：`/aip/proposals`  
**对齐**：07 §5.1 · Automate 提案

```text
┌─ 代理提案 ───────────────────────────────────────────────────────────────────┐
│  来源过滤: [全部 ▾] [Automate:{repair_auto} ▾]   ⚠ 开放提案约 24h 可见       │
│  列: ● 待审批  ○ 已应用  ○ 已拒绝                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  ┌─ Draft #8842 · 派单维修 🟡 ─────────────────────────────────────────────┐ │
│  │ Device: DEV-019 · 班组: 夜班-3 · 依据: 温升+振动 · Wiki.risk=高           │ │
│  │ 预览操作: create_work_order(…)                                            │ │
│  │ [查看决策日志 / Lineage →]   [批准]   [驳回]   [改参后批准]                │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│  ┌─ Draft #8843 · Insight Backfill 🟣 ─────────────────────────────────────┐ │
│  │ 结论: 肽批次A纯度异常 ↔ 设备B振动  · 置信 0.93                              │ │
│  │ 预览: 新建 Insight + Link(BatchA, EquipB) · 可选更新属性                   │ │
│  │ [查看 Lineage →]   [批准回填]   [驳回]                                    │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│  ┌─ Draft #8841 · … ───────────────────────────────────────────────────────┐ │
│  │ …                                                                         │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

> **25：** Draft 类型含 `InsightBackfill`；批准后沉淀 Insight，≠ Funnel 水合。

---

## 9. WF-AIP-07 · Decision Lineage

**路由**：`/aip/lineage/{id}`  
**对齐**：07 §5.2 · Debugger / 代理决策日志

```text
┌─ 决策血缘 · {run_id} ────────────────────────────────────────────────────────┐
│  Agent/Logic: {dispatch_repair}   模型: {私有-中}   时间: 2026-07-14 14:02   │
│  审批: 张三 · 批准 · → Action create_wo · Write-back ✅                      │
├──────────────────────────────────────────────────────────────────────────────┤
│  时间线                                                                      │
│  1. Input  device=DEV-019                                                    │
│  2. Get Attributes + 🟣 Wiki.risk_level=高                                   │
│  3. Use LLM Prompt v3  (快照可展开)                                          │
│  4. Tool: Query Objects → 3 条相似工单                                       │
│  5. Tool: Request Clarification → 用户「可以」                               │
│  6. Tool: Action → Draft #8842                                               │
│  7. HITL Approve → Criteria OK → Funnel Changelog                            │
│  8. （若有）Insight Backfill → Insight#… + Link 相关 Object                  │
│                                                                              │
│  CoT 原文  [展开]     工具 JSON  [展开]     Prompt 版本 [对比]                │
│  [导出审计包]                                                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. WF-AIP-08 · Evals 门控

**路由**：`/aip/evals/{suite}`  

```text
┌─ AIP Evals · {dispatch_repair_suite} ────────────────────────────────────────┐
│  套件: 42 用例   最近跑: 41/42 通过  🟢                                       │
│  对比: 模型 A {私有-中} vs B {高能力}   方差: 3 次 rerun                      │
├──────────────────────────────────────────────────────────────────────────────┤
│  用例                  期望                     结果         操作             │
│  high_temp_device      生成派单 Draft           ✅           [开 Debugger]   │
│  low_risk_false_alarm  不调用 Action            ✅           …               │
│  missing_crew          Clarify 后派单           ❌ 跳过 Clarify [修 Prompt]  │
│                                                                              │
│  门控: ☑ 生产 Automate 必须套件绿   ☑ L4 Agent→Function 必须套件绿          │
│  [重跑] [发布通过徽章 → 解锁 Automate]                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. WF-AIP-09 · Workshop · Agent 组件

**路由**：Workshop 模块编辑器内  
**对齐**：07 §5b.5 · 成熟度 L3

```text
┌─ Workshop 模块 · {maintenance_ops} ──────────────────────────────────────────┐
│  画布: [筛选器] [对象表] [ Agent 组件 ● ] [提案小部件]                        │
├──────────────────────────────────────────────────────────────────────────────┤
│  Agent 组件属性                                                              │
│  绑定 Agent: {维修派单 Buddy} ▾                                              │
│  输入映射:                                                                   │
│    State.ticket_id  ←  变量 $selectedTicket                                  │
│    State.devices    ←  变量 $selectedDevices (Object Set)                    │
│  输出映射:                                                                   │
│    回复文本     →  Markdown 微件                                             │
│    提出的 Draft →  提案小部件 / 跳转 /aip/proposals                          │
│  [预览] [发布模块]                                                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 12. 用户旅程线框串联

### 12.1 旅程 I · 左引擎派单（HITL）

```text
事件/Workshop
  → WF-AIP-01 选私有模
  → WF-AIP-02 Logic: Get+Wiki → Use LLM → Draft
  → WF-AIP-06 批准
  → 06b Criteria → Write-back → Funnel
  → WF-AIP-07 复盘
```

### 12.2 旅程 J · 开放诊断（Tool Use）

```text
WF-AIP-05 试对话
  → WF-AIP-05T Query + Function
  → 返回清单 + CoT
  → （可选）Action 表单确认
```

### 12.3 旅程 K · 成熟度爬坡

```text
WF-AIP-00 L1 Threads
  → L2 WF-AIP-05 + 05T
  → L3 WF-AIP-09
  → L4：WF-AIP-08 绿 + WF-AIP-06 Draft 默认 → Agent 发布为 Function
```

---

## 13. 组件清单（研发）

| 组件 ID | 名称 | 出现页面 | 说明 |
|---------|------|----------|------|
| CMP-AIP-STAIR | 成熟度楼梯 / 迷你侧栏 | Shell · 00 | L1–L4 导航与门禁态 |
| CMP-AIP-LOGIC-3PANE | Logic 三栏 | 02 | 编排 / Debugger / 运行 |
| CMP-AIP-BLOCK-PALETTE | 块工具条 | 02 | 官方块类型 |
| CMP-AIP-TOOL-PANEL | Agent 工具面板 | 05T | 六类 + Wiki |
| CMP-AIP-TOOL-CARD | 单工具配置卡 | 05T | Action/Clarify 等 |
| CMP-AIP-PROPOSAL-BOARD | 提案看板 | 06 | 待审/已应用/拒绝 |
| CMP-AIP-LINEAGE | 决策时间线 | 07 | CoT + 工具序列 |
| CMP-AIP-EVAL-GATE | Eval 门控条 | 08 · L4 | 绿才解锁 |
| CMP-AIP-AGENT-WIDGET | Workshop Agent 组件 | 09 | 变量双向绑定 |
| CMP-AIP-MODEL-ROUTER | 路由表 | 01 | 任务→模型→出境 |

---

## 14. 与 07 / 06b 一致性自检

| 检查项 | 结果 |
|--------|------|
| 楼梯 L1–L4 与 07 §5b.3 一致 | ✅ |
| 工具六类 + Prompted/Native 与 07 §5b.4 一致 | ✅ |
| Logic 三栏 + 试跑不落库与 07 §3.0 / A-07 一致 | ✅ |
| Draft 批准后仍过 06b Criteria | ✅ 旅程 I / 提案台 |
| Wiki 优先作 Query 属性子集（AIP-003） | ✅ 工具面板 🟣 |
| HTML Demo | ✅ v1.6.3 · 含 `aip-capabilities`（07b） |

**风险提示**：Native Tool Calling 兼容矩阵因租户/模型而异，线框中必须保留 Prompted 回退选项。

---

## 15. 变更记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-07-14 | 初稿：WF-AIP-00~09 · 成熟度楼梯 · Agent 工具面板 · 旅程 I/J/K · 组件清单 |
| v1.0.1 | 2026-07-14 | HTML Demo v1.4 落地 maturity/tools/logic |
| v1.0.2 | 2026-07-17 | Draft/Lineage 增 Insight Backfill；对齐 [25](20_tech/25-LLM-Wiki启示与L2演进补丁.md) |
| v1.0.3 | 2026-07-17 | WF-AIP-01 拆 **供应商接入 / 路由策略** 两屏；Demo v1.6.2 |
| v1.0.4 | 2026-07-17 | WF-AIP-05C 重能力接入；链 07b；Demo v1.6.3 |


---

*v1.0.4 · docs/palantier/07a · 承接 07 / 07b · 楼梯 + 工具面板 + Capability*
