# AOS 系列技术文章 · 掘金发布计划

> **目标平台**：掘金（juejin.cn）
> **发布目录**：`docs/palantier/articles/`
> **版本**：v3.0 · 2026-07-26

---

## 系列定位（已确认）

**双重定位**：技术深度分析 + 产品设计哲学。

不是单纯翻译官方文档，而是回答一个核心问题——**「为什么企业 AI 需要操作系统」**。
以这个切入点为主线，把 Palantir Foundry 作为最佳案例来拆解：

1. **产品设计哲学**：为什么是 Ontology 而不是数据湖？为什么是 Action 而不是 API？为什么是 Logic 画布而不是 prompt chain？
2. **技术深度分析**：每个设计决策背后的架构原理、工程取舍、实现路径

目标读者：架构师、技术决策者、AI 产品经理——需要在企业级场景落地 AI 的人。

### 三条编辑方针

- **问题驱动**：每篇开头抛一个真实问题（如「LLM 幻觉了怎么办？」「200 个系统怎么统一语义？」），用 Palantir 的设计来回答
- **设计哲学优先**：先讲「为什么这么设计」，再讲「怎么实现」，避免沦为功能清单
- **官方截图直用**：1945 张官方截图直接引用，图片下方标注来源（`来源：Palantir Foundry 官方文档`）

---

## 素材库全景索引

写作前按需查阅，所有素材位于 `docs/palantier/` 下：

### A. 自有产品方案（核心骨架）

| 文档 | 路径 | 行数 | 用途 |
|------|------|------|------|
| 01 全链路总览 | `01-Palantir全链路总览.md` | ~500 | Apollo→Foundry→AIP 三层闭环 + 6 阶段管道 |
| 02 四大金刚拆解 | `02-四大金刚与子产品拆解.md` | ~400 | Gotham/Foundry/Apollo/AIP × 40+ 子模块 |
| 03 AOS PRD 框架 | `03-对标Palantir-AOS-PRD框架.md` | ~300 | 国产替代方案 + 差距对照 |
| 05 数据集成 | `05-数据集成Connectors-Pipeline-Dataset产品方案.md` | ~600 | 200+ Connector + Pipeline Builder |
| 06 Ontology 本体 | `06-语义本体Ontology-Mapping产品方案.md` | ~700 | Object/Action/Link + ODIF Funnel |
| 07 AIP 引擎 | `07-AIP引擎k-LLM与AgentStudio产品方案.md` | ~500 | k-LLM 路由 + Logic 画布 + Agent Studio |
| 08 Workshop | `08-Workshop产品方案.md` | ~400 | 低代码应用构建 + Canvas 事件编排 |
| 09 Apollo | `09-Apollo交付引擎产品方案.md` | ~300 | Hub-Spoke 气隙部署 |

### B. Palantir 官方文档（一手权威）

| 来源 | 路径 | 规模 | 说明 |
|------|------|------|------|
| **AIP 官方文档** | `AIP/` | **66 篇 / 18000 行 / 216 图** | AIP Logic/Agent Studio/Evals/Observability/Assist/Analyst 全量 |
| **Foundry 官方文档** | `foundry/pages/zh/foundry/` | **1308 篇** | 全部 Foundry 模块中文翻译 |
| **PRD 专题文档** | `prddetail/*.docx` | **52 篇 Word** | 含 1945 张原始截图，覆盖全部核心模块 |
| **截图库** | `foundry/images/foundry/` | **1945 张 PNG** | 每个 UI 界面的真实截图 |
| **官网页面** | — | 已抓取 | Foundry/Ontology/AIP/Apollo 四大产品页 |

#### AIP 文档 8 大子模块索引

| 子模块 | 路径 | 篇数 | 核心内容 |
|--------|------|------|---------|
| AIP 核心 | `AIP/aip/` | 20 | Overview/Features/Security/Supported LLMs/Capacity/Bring Your Own Model |
| AIP Logic | `AIP/logic/` | 10 | Core Concepts/Blocks/Branching/Automate/Execution Modes/Metrics |
| AIP Analyst | `AIP/aip-analyst/` | 6 | Overview/Capabilities/Resources/Workshop Widget/Embed |
| AIP Evals | `AIP/aip-evals/` | 10 | Suite/Create/Run/Experiments/Metrics Dashboard/Ontology Edits |
| AIP Observability | `AIP/aip-observability/` | 8 | Trace View/Logs/Metrics/Performance/Run History |
| AIP Assist | `AIP/assist/` | 9 | Custom Docs/Register Content/Suggested Actions/App Integrations |
| Workflow Lineage | `AIP/workflow-lineage/` | 1 | Usage Observability |
| Notepad | `AIP/notepad/` | 1 | AIP Features |

### C. 技术方案与开发计划

| 文档 | 路径 | 说明 |
|------|------|------|
| 220w 差距分析 | `20_tech/220w-与目标系统差距对照分析.md` | 1157 项 ✅ |
| 221m 差距分析 | `20_tech/221m-与目标系统差距对照分析.md` | 48 项 ✅ |
| 222 产品补充 | `20_tech/222-产品补充说明.md` | 19 章 |
| 220plan | `20_tech/220plan-分阶段开发与里程碑计划.md` | 270 项 ✅ |
| 220plan2 | `20_tech/220plan2-分阶段开发与里程碑计划（第二批）.md` | 316 项 ✅ |
| 221plan | `20_tech/221plan-分阶段开发与里程碑计划.md` | 33 项 ✅ |
| 222plan | `20_tech/222plan-分阶段开发与里程碑计划.md` | 104 项 ✅ |
| Phase A~E 技术方案 | `20_tech/222_phase[A-E]*.md` | 7 篇独立方案 |

### D. 代码库实测数据

| 维度 | 数据 |
|------|------|
| 后端 | 1554 .py 文件 / 3772 API 路由 / 468 include_router / 566 测试 |
| 前端 | 101 ts/tsx / 66 导航页面 / 59+ React 页面 |
| 插件 | 67 个（含 Action/Ontology/Model 等类型） |
| HTML Demo | 73 页（复刻 Foundry UI） |
| 全量回归 | 7161+4603 = 11764 测试 PASS |

### E. 架构模式与方法论

| 技能 | 路径 | 说明 |
|------|------|------|
| awesome-llm-apps-patterns | `~/.workbuddy/skills/awesome-llm-apps-patterns/` | 11 大模式（Advisor-Orchestrator-Worker / MCP Router / RouteLLM 等） |
| engineering-process | `~/.workbuddy/skills/engineering-process/` | 7 阶段工程方法论 |

---

## 文章清单

### 需求类（2 篇）— 回答「为什么」

| 编号 | 文件名 | 标题 | 核心问题 | 主要素材 | 字数 |
|------|--------|------|---------|---------|------|
| 01 | `01-why-enterprise-ai-needs-os.md` | 为什么企业 AI 需要一个操作系统：从 Palantir 千亿市值说起 | Palantir 凭什么千亿 → 它到底解决了什么别人没解决的问题 → 为什么答案是「OS」而不是更多模型 | 01 + 02 + 官网 + 客户案例 | 6-7k |
| 02 | `02-five-walls.md` | 企业 AI 落地的 5 道墙：数据孤岛、语义割裂、幻觉失控、行动无能、部署困境 | 纯问题定义，不讲方案——把每道墙的痛感和代价讲透，建立读者的痛点共识 | 官网案例 + 行业报告 + 01 文档痛点节选 | 5-6k |

### 产品设计类（4 篇）— 回答「怎么设计的」

| 编号 | 文件名 | 标题 | 核心问题 | 主要素材 | 字数 |
|------|--------|------|---------|---------|------|
| 03 | `03-ontology-semantic-layer.md` | Ontology 本体论：让 AI 真正理解企业业务的语义层设计 | 数据湖 vs 本体 → Object/Action/Link 三件套 → ODIF 四阶段 Funnel | 06 + AIP/logic + foundry/ontology-* | 7-9k |
| 04 | `04-data-integration-pipeline.md` | 数据集成与 Pipeline：200+ Connector 如何把杂乱数据编译成可信资产 | 200+ 异构系统怎么统一 → Pipeline Builder → 5 种写入模式 | 05 + prddetail + foundry/data-* | 6-8k |
| 05 | `05-aip-decision-engine.md` | AIP 决策引擎：让 AI 安全地行动——k-LLM 路由 + Logic 画布 + 安全闭环 | LLM 幻觉了怎么办 → k-LLM 路由 → Tools 安全调用 → L1~L4 成熟度 | 07 + AIP/ 全量 66 篇 | 8-10k |
| 06 | `06-workshop-lowcode.md` | Workshop 低代码平台：以 Object 为中心的应用构建革命 | 为什么传统低代码天花板低 → Ontology-native 应用 → Canvas 事件编排 | 08 + foundry/workshop | 6-7k |

### 技术类（3 篇）— 回答「怎么实现的」

| 编号 | 文件名 | 标题 | 核心问题 | 主要素材 | 字数 |
|------|--------|------|---------|---------|------|
| 07 | `07-apollo-delivery.md` | Apollo 持续交付引擎：跨云/气隙/零停机的工程级部署架构 | 企业级软件怎么部署到气隙环境 → Hub-Spoke → Release 通道 | 09 + 官网 Apollo | 6-7k |
| 08 | `08-system-architecture.md` | 系统架构与工程组织：从 PRD 到 3400+ 模块的代码库是怎么长出来的 | 3400 模块怎么不乱 → 3772 路由怎么管 → 714 项开发怎么编排 | 代码库 + 220plan/221plan/222plan | 7-8k |
| 09 | `09-tech-implementation.md` | 技术实现方案：714 项任务的工程落地——差距分析到全量回归 | 怎么从对标分析到可运行系统 → 差距矩阵 → 分阶段开发 → 回归基线 | 差距分析 + Phase A~E | 6-7k |

### 分类分布

```
需求类     01 + 02            ← 先建立痛点共识，读者带着问题往下读
产品设计类  03 + 04 + 05 + 06  ← 系列核心主力，逐层击破每道墙
技术类     07 + 08 + 09       ← 工程落地收尾
```

### 首发策略

**打头阵两篇连发**：

- **篇 01**「为什么企业 AI 需要一个操作系统」— 只讲一个故事：企业花了几百万买 LLM，为什么还是落不了地？Palantir 凭什么值千亿？用这个钩子把读者拉进来。
- **篇 02**「5 道墙」— 紧接着把 5 个痛点逐个拆透，不讲方案，只定义问题。让读者心里冒出"那怎么办？"。

然后篇 03 Ontology 开始逐墙击破。

---

## 发布顺序

**第一批（痛点+钩子）**：01 为什么需要 OS → 02 五道墙
**第二批（核心设计）**：03 Ontology → 04 数据集成
**第三批（AI+应用）**：05 AIP 决策引擎 → 06 Workshop
**第四批（工程落地）**：07 Apollo → 08 系统架构 → 09 技术实现

---

## 官网信息更新要点（2026-07 抓取）

写作时注意以下官方最新变化：

1. **AIP Agent Studio → 已更名为 AIP Chatbot Studio**（2026-04-27）
2. **Ontology MCP** — 官网新增概念：「Ontology MCP exposes your ontology primitives to external agents as MCP tools」
3. **Agent Tier Framework** — Tier 1~4 成熟度：Ad-hoc → RAG Agent → Action Agent → Autonomous
4. **Function-backed Context**（2025-02 新增）— Agent 自定义检索能力
5. **Agent as Function**（2025-03 新增）— Agent 可发布为 Function，可被其他 Agent 调用
6. **Palantir 获评 Forrester Wave AI/ML Platforms Leader**（Q3 2024）
7. **Dresner 排名 Palantir Agentic AI / AI DS ML / ModelOps 三个 No.1**（2025）

---

## 写作规范

- **标题**：H1 主标题，问题驱动式，避免「万字」「保姆级」等标题党
- **字数**：每篇 6-10k，掘金阅读时长 12-20 分钟
- **配图**：Palantir 官方截图直接使用，图片下方标注 `> 来源：Palantir Foundry 官方文档`
- **代码**：关键设计决策配代码片段，每段不超过 40 行
- **风格**：产品设计哲学 + 技术深度分析，不是功能翻译
- **分类标签**：后端 / 架构 / 人工智能
- **引用规范**：引用 Palantir 官方文档时标注来源路径

---

## 状态

**当前阶段：素材准备完成，分类方案 v3.0 确认（9 篇 2:4:3 分布），等待用户确认后开始写作。**
