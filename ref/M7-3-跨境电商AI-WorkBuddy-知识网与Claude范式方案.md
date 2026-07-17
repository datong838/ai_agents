# 基于知识网与 Claude 范式的跨境电商 AI WorkBuddy

> **版本**：v1.2 · 2026-07-11  
> **状态**：方案定稿 · 知识资产骨架已建（`knowledge/` · 未接入 Compile）  
> **v1.2 变更**：仓库落地 `knowledge/` + `third_party/okf/` + `schema/OKF_ECOM.md`（见 §6.8）  
> **v1.1 变更**：第 6 章重写——对齐 [Karpathy LLM Wiki](https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/) 运维范式 + [Google OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) 交换格式，明确三层知识架构与谛听知识网的映射。  
> **关联**：[M7-2 生物-数字双模态知识网宣讲稿](M7-2-谛听-生物数字双模态知识网宣讲稿.md) · [知识库-结构化入库方案 §十四](../知识库-结构化入库方案.md) · [M6-2 通用客服与技能集](../M6-2-通用客服智能体与话术策略知识库方案.md) · [M6-3 智能写作](../M6-3-智能写作技能-文案脚手架方案.md) · [M7-1 短视频导演智能体](../M7-1-短视频创作-导演智能体总体方案.md)

---

## 目录

1. [项目背景与定位](#1-项目背景与定位)
2. [核心理念：三位一体](#2-核心理念三位一体)
3. [技术架构](#3-技术架构)
4. [数字员工角色设计](#4-数字员工角色设计)
5. [工程路线：Claude API + 逆向工程](#5-工程路线claude-api--逆向工程)
6. [知识库底座：LLM Wiki Format 管线](#6-知识库底座llm-wiki-format-管线)
7. [自学习进化：突触可塑性](#7-自学习进化突触可塑性)
8. [与平台现有 AI 的互补关系](#8-与平台现有-ai-的互补关系)
9. [实施路径](#9-实施路径)
10. [预期收益](#10-预期收益)
11. [模型选型与合规说明](#11-模型选型与合规说明)
12. [下一步行动](#12-下一步行动)

---

## 1. 项目背景与定位

### 1.1 行业现状：AI 已上线，但未成「员工」

典型跨境电商 SaaS 平台 today 往往已具备：

| 能力 | 常见形态 |
|------|----------|
| **Listing / 文案 AI** | 商品标题、多语种描述生成 |
| **客服 AI** | 平台内问答、工单辅助 |
| **选品 AI** | 趋势、竞品、毛利分析 |
| **领域大模型** | 基于百万级 SKU / 订单语料微调 |
| **MCP / OpenAPI** | 百级业务 API 封装，供 Agent 调用 |

这些能力解决了「有没有 AI」的问题，但多数仍停留在 **工具层**：用户打开功能、填参数、看结果——**缺少角色、权限边界、跨任务记忆与自主编排**。

### 1.2 存在的缝隙

| 缝隙 | 表现 |
|------|------|
| **工具 ≠ 员工** | 无岗责宪法、无身份隔离、无「@某个 Buddy 帮我搞定」的委托范式 |
| **通用 WorkBuddy 不够** | 腾讯等通用助手难处理 170+ 平台异构详情、小语种、合规红线、ERP 脏数据 |
| **知识散、结构弱** | PDF/邮件/历史 Listing 沉睡；向量 chunk 看不见「功效→商品→同图多品」结构 |
| **越用不会 smarter** | 推荐路径不沉淀；成功/失败案例不回写知识网 |

卖家侧仍大量依赖人工：选品判断、Listing 迭代、库存调拨、跨平台操作——**AI 能答，但不能持续代劳**。

### 1.3 我们的定位

```text
跨境电商 WorkBuddy = Claude 思想 × 知识网底座 × 自学习进化
```

**我们做的不是又一个 Chatbot**，而是：

- 有 **岗责宪法**（能做什么、不能做什么、何时人审）
- 有 **知识网**（商品/段落/概念/媒体异构图 + PPR 神经扩散）
- 会 **越用越准**（边权突触可塑性，形成数据壁垒）

产品形态：**用户 @Buddy 委托任务 → Orchestrator 路由 → Subagent 并行执行 → MCP/API/Computer Use 落地 → 结果回写知识网**。

与谛听已有能力对齐：美妆电商场景下 **智能客服（M6-1/2）**、**文案写手（M6-3）**、**短视频创作（M7-1）** 已验证「同一张网、不同 Skill」；本方案将其 **泛化到跨境多品类、多角色 WorkBuddy**。

---

## 2. 核心理念：三位一体

> 图 1 · 三位一体：Claude 思想 × 知识库底座 × 自学习进化

| 维度 | 内涵 | 工程体现 |
|------|------|----------|
| 🤖 **Claude 思想** | Constitutional AI（岗责宪法）、身份隔离、Subagents/Swarm、Computer Use | 每个数字员工有显式权限边界与可审查原则；多角色协作编排；无 API 场景下浏览器/桌面级操作兜底 |
| 📚 **知识库底座** | 知识网本体（异构图）+ **OKF / LLM Wiki 三层管线** | OKF Bundle（Markdown+YAML）→ 编译为 `document/section/concept/media` 图；PPR 神经扩散；`index.md` / `log.md` 渐进披露 |
| 🧠 **自学习进化** | 突触可塑性：边权随使用动态调整 | 成功推荐 → 边权 ↑；错误/退货/投诉 → 边权 ↓；冷启动靠结构，热启动靠演化 |

**一句话**：Claude 范式解决「怎么组织员工」；知识网解决「员工凭什么懂业务」；突触可塑性解决「为什么越用越离不开」。

---

## 3. 技术架构

### 3.1 端到端链路

```text
用户委托（@导购Buddy / @文案Buddy …）
   ↓
岗责宪法（权限检查 · 身份隔离 · 输出约束）
   ↓
Orchestrator（店铺总管 · 任务分解 · Buddy 路由）
   ↓
四位 Buddy Subagents（Swarm · 可并行/异步）
   ↓
activate → propagate(PPR + meta-path) → package → llm → skill_output
   ↓
平台 MCP / OpenAPI · Computer Use 兜底（无 API 的脏活）
   ↓
执行结果 → 边权更新（自学习）→ Dashboard 可审计
```

### 3.2 关键组件（我们已实现 / 在研）

| 组件 | 说明 | 状态 |
|------|------|------|
| **知识网本体** | 异构图：`document` / `section` / `concept` / `media` / `evaluate`；边：`contains` / `mentions` / `appears_in` / `references` / `related_product` | ✅ beauty 类目已验收 |
| **神经扩散引擎** | BGE-M3 ANN 种子 → PPR 沿 meta-path 白名单扩散 → 结构化子图 | ✅ 生产默认 `ann_then_ppr` |
| **技能集 Skills** | 统一契约 `activate → propagate → package → llm → skill_output`；策略进 `agent_skills` 知识库 | ✅ 客服/写作；🚧 短视频 |
| **岗责宪法** | 每 Buddy 绑定：可调 API 白名单、可访数据域、输出模板、Human-in-the-Loop 触发条件 | 🔜 首期 POC 编码 |
| **Orchestrator** | 委托解析、Buddy 选择、子任务拆分、结果聚合 | 🔜 方案设计 |
| **Computer Use** | 无 MCP 覆盖时的浏览器/桌面操作兜底 | 🔜 远期 |

### 3.3 与纯 RAG / 纯 Agent 的差异

| | 纯向量 RAG | 纯 Claude Agent | 本方案 |
|--|-----------|-----------------|--------|
| 检索 | chunk 相似度 | 模型参数 + 工具 | **ANN + PPR 子图**，路径可解释 |
| 角色 | 无 | Prompt 模拟 | **Constitution + 身份隔离 + Subagent** |
| 行动 | 无 | Tool/MCP | **MCP + Computer Use 双通道** |
| 进化 | 静态 | 会话记忆 | **边权突触可塑性**，跨会话沉淀 |

---

## 4. 数字员工角色设计

> 图 2 · 四位 Buddy：导购 / 文案 / 库存 / 选品

每个 Buddy = **Claude-style Identity**（权限 / 工具 / 记忆隔离），可独立启用或组合。

| 角色 | 岗位职责 | 核心 Skill | 依赖的知识网能力 | 自学习点 |
|------|----------|------------|------------------|----------|
| 🛒 **导购 Buddy** | 售前咨询、推荐商品、搭配套餐 | `cs_dialogue` 渐进式四步 + 商品扩散 | `mentions`（功效→商品）、`appears_in`（同图多品） | 搭配成交率高的路径 → 边权强化 |
| ✍️ **文案 Buddy** | Listing 生成、多语优化、A/B 变体 | `doc_writer` 信任状脚手架 + 多平台文库 | `section` 分段 + `concept` 节点 + 子图事实清单 | 历史点击率/转化反馈 → 边权调整 |
| 📦 **库存 Buddy** | 监控、预警、调拨建议 | 数据查询 + 规则引擎 + 时序边 | 商品节点 + 销量/库存时序边（扩展） | 补货阈值随准确率自调整 |
| 🔍 **选品 Buddy** | 趋势分析、竞品对比、新品建议 | 选品增强 Skill + 概念聚类 | meta-path 跨商品扩散 + `concept` 聚类 | 失败案例路径 → 边权弱化 |

### 4.1 与谛听技能集的映射

| WorkBuddy 角色 | 谛听已有 Skill | 备注 |
|----------------|----------------|------|
| 导购 Buddy | M6-1/2 智能客服 · `cs_dialogue` | ✅ 已 POC，金牌导购式四步话术 |
| 文案 Buddy | M6-3 智能写作 · `doc_writer` | ✅ 已落地，图谱勾选 → 可溯源文章 |
| 选品 Buddy | 需求雷达 + 类目过滤 + 结构化需求 | ✅ 主链路；选品 Skill 扩展中 |
| 库存 Buddy | — | 🔜 规则引擎 + 时序边，Phase 3 |
| （扩展）短视频 Buddy | M7-1 导演 + 编剧/美术 Skill | 🚧 与 Listing/导购共用素材包血缘 |

**组合示例**：卖家 `@店铺总管 把这款防晒做成 Shopee Listing 并配三条FAQ` → Orchestrator 拆给 **文案 Buddy**（Listing）+ **导购 Buddy**（FAQ 话术），共用同一商品子图，结果分别写入文库与客服策略库。

---

## 5. 工程路线：Claude API + 逆向工程

> 图 3 · 分层：哪些用 Claude API，哪些自研

### 5.1 分层说明

| 层 | 使用 Claude API | 逆向工程 / 自研 | 说明 |
|----|:---------------:|:---------------:|------|
| **LLM 推理** | ✅ | — | POC 阶段调用 Claude Opus/Sonnet，验证复杂推理与多步 Agent |
| **岗责宪法** | — | ✅ | 复刻 Constitutional AI 思想，适配跨境合规与平台规则 |
| **身份隔离 / Swarm** | — | ✅ | 复刻 Subagents 范式：每 Buddy 独立权限、工具、记忆 |
| **Computer Use** | — | ✅ | 跨系统无 API 操作（浏览器/桌面），与 MCP 互补 |
| **知识网本体** | — | ✅ | 完全自研，与 Claude 解耦 |
| **PPR 神经扩散** | — | ✅ | 完全自研，与 Claude 解耦 |

### 5.2 为什么这么做

1. **Claude API = 原型验证机**：快速验证「@Buddy + 宪法 + Swarm + 知识网」范式是否成立，缩短 Phase 1 周期。  
2. **核心能力自研**：岗责、隔离、编排、知识网、PPR **不被任何闭源模型锁定**。  
3. **生产可切换**：POC 后推理层可无缝替换为 **平台自研领域模型** 或 **DeepSeek 等私有化部署**，Skill 与知识网层 **无感**。

### 5.3 我们的工程原则

```text
本体优先 · Skill 可插拔 · 推理层可替换 · 来源可审计
```

与 [M7-2 宣讲稿](M7-2-谛听-生物数字双模态知识网宣讲稿.md) 一致：**今日交付 PPR，明日可上 R-GCN/HAN；Skill 层不感知底层扩散算法**。

---

## 6. 知识库底座：OKF × LLM Wiki × 知识网编译

> **参考范式**  
> - [Karpathy · LLM Wiki](https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/) — **怎么运维**（LLM 维护持久 Wiki，知识复利，非每次 RAG 重发现）  
> - [Google · Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) — **怎么交换**（Markdown + YAML frontmatter，Bundle 可 git diff、任意 Agent 可读写）  
> - [谛听 · 知识网 §十四](../知识库-结构化入库方案.md) — **怎么传导**（异构图 + ANN + PPR + 突触可塑性，WorkBuddy 真正「懂业务」的引擎）

### 6.0 为什么这套方式好——对 RAG 的超越

传统 RAG：**每次提问 → 向量检索 chunk → LLM 临时拼答案**。知识不积累， subtle 问题要反复「从碎片里重新发现」。

[Karpathy LLM Wiki](https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/) 的核心洞见：

| RAG 模式 | LLM Wiki 模式 |
|----------|---------------|
| 检索原始文档片段 | LLM **增量编译**持久 Wiki |
| 交叉引用每次现找 | 链接、矛盾、综合 **已写好** |
| 对话结束即消失 | **Query 的好答案可回写** Wiki，探索也复利 |
| 人维护 Wiki 会弃坑 | **LLM 做 bookkeeping**（跨 10–15 页一次 Ingest 更新） |

[Google OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) 把上述 Wiki 思路 **标准化为可互操作格式**：

- **Vendor-neutral**：不绑定 Claude / ADK / LangChain，任何人可生产、任何人可消费  
- **Human + Agent readable**：`cat` 即读，无需 SDK  
- **Git-native**：PR 审阅知识变更，和改代码一样  
- **Graph-shaped**：Markdown 交叉链接表达超越目录树的语义关系  
- **Progressive disclosure**：`index.md` 逐层导航，不必一次加载全库  

**我们的判断**：OKF/Wiki 解决「知识怎么 **写进去、存下来、交换**」；谛听知识网解决「知识怎么 **传导、解释、进化**」。二者 **不替代，而是串联**。

### 6.1 三层知识架构（我们采用的合体方案）

```text
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1 · Raw Sources（原始层 · 不可变）                          │
│  170+ 平台商品 HTML · PDF 说明书 · 邮件 · 客服记录 · 竞品页面       │
│  原则：LLM 只读，不改源文件 —— 溯源真相在此                         │
└───────────────────────────────┬─────────────────────────────────┘
                                │ Ingest（LLM Agent · 蒸馏 · 抽取）
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 2 · OKF Bundle / LLM Wiki（编译层 · LLM 维护）             │
│  Markdown + YAML frontmatter · 交叉链接 · index.md · log.md       │
│  原则：LLM 写、人审；git 版本化；符合 OKF v0.1 最小 conformance      │
└───────────────────────────────┬─────────────────────────────────┘
                                │ Compile（结构化入库 · 边构建 · 嵌入）
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 3 · 知识网 Graph（传导层 · 谛听引擎）                       │
│  document/section/concept/media 节点 · mentions/appears_in 边     │
│  BGE-M3 向量 · PPR + meta-path · 突触可塑性                        │
│  原则：WorkBuddy Skills 消费子图，不直接裸读 OKF 全文                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    WorkBuddy：activate → propagate → package → llm → skill_output
```

对应 Karpathy 三层：

| Karpathy | 我们 |
|----------|------|
| Raw sources | Layer 1 原始文档库 |
| The wiki | Layer 2 OKF Bundle（+ `schema/` 岗责与入库契约） |
| The schema（CLAUDE.md / AGENTS.md） | `schema/OKF_ECOM.md` — 告诉 Agent 如何 Ingest / Query / Lint / Compile |

### 6.2 OKF Concept → 知识网节点映射

OKF 每个 **Concept** = 一个 `.md` 文件（YAML frontmatter + Markdown body + 交叉链接）。编译进知识网时：

| OKF frontmatter | 知识网映射 | 示例（跨境电商） |
|-----------------|------------|------------------|
| `type: Product Document` | `document` 节点 | Shopee 防晒 Listing 母稿 |
| `type: Section` | `section` 节点 | 「成分说明」段落 |
| `type: Concept` | `concept` 节点 | `spf50`、`敏感肌`、`烟酰胺` |
| `type: Media` | `media` 节点 | 主图 / 详情图（VLM 描述） |
| `type: Playbook` | `agent_skills` 策略引用 | 导购四步 PDS、Listing 脚手架 |
| `type: Reference` | `references/` 外链概念 | 平台官方政策页镜像 |
| body 内 `[link](/concepts/spf50.md)` | `mentions` / `references` 边 | 段落提及概念 |
| 同图跨文档链接 | `appears_in` 边 | 同 SKU 图出现在多 Listing |
| `resource:` URI | 节点 `source_url` / 商品 ID | 回链 ERP / 平台原始 URL |
| `tags:` | `sub_category` / 运营分组 | `[beauty, sunscreen, th]` |

**OKF Bundle 目录建议**（beauty 试点）：

```text
bundles/beauty/
├── index.md                 # 类目总览 · progressive disclosure
├── log.md                   # Ingest / Query / Lint 时间线
├── products/
│   ├── index.md
│   └── {sku_id}.md          # type: Product Document
├── concepts/
│   ├── index.md
│   └── {slug}.md            # type: Concept（功效/成分/肤质）
├── playbooks/
│   ├── cs_dialogue_pds.md   # type: Playbook
│   └── doc_writer_listing.md
└── references/
    └── shopee-listing-policy.md
```

### 6.3 三大运维操作（借鉴 LLM Wiki · 我们工程化）

#### 6.3.1 Ingest — 新源入库

```text
1. 原始文档进入 Layer 1（raw/，不可变）
2. Ingest Agent 读取源 + 现有 Bundle（index + 相关 Concept）
3. LLM 蒸馏：去噪 · 实体抽取 · 小语种对齐 · 矛盾标注
4. 写入/更新 OKF Concept（单源常触达 10–15 个 Concept 页）
5. 更新 index.md · 追加 log.md
6. Compile Job：OKF → 知识网节点/边 · BGE embed · verify 验收
```

与纯 HTML 去标签的差异：**Ingest = 教学**——LLM 理解后再写 Wiki，而非机械切块。

#### 6.3.2 Query — Buddy 消费知识

```text
1. 用户 @Buddy 提问 / 委托
2. 先读 index.md 定位相关 Concept（中小规模足够，无需 embedding 基础设施）
3. activate：ANN 种子 + PPR 扩散 → 子图（Layer 3）
4. package → llm → skill_output
5. ★ 高价值回答（对比表、选品结论、Listing 变体）→ 回写为新 Concept 或更新现有页（Query 也复利）
```

这与 M6-3「子图事实清单 → 文章 → 文库入库」、M7-1「母稿 → 短视频项目」**同构**。

#### 6.3.3 Lint — 知识库健康体检

定期 Agent 任务（建议周批 + 大 Ingest 后触发）：

| 检查项 | 动作 |
|--------|------|
| 页面间矛盾 | 标注冲突，优先以新源 / 成交数据为准 |
|  stale 声明 | 下架商品、过期政策 → 标记 + 图谱边 `staleness` |
| 孤儿 Concept | 无入链 → 补交叉引用或合并 |
| 缺页概念 | 正文多次提及但未建 Concept → 补建 |
| 断链 | OKF 容忍 broken link；Lint 报告待补全 |
| 数据缺口 | 建议 Web 抓取或内部 API 补源 |

Lint 结果写入 `log.md`，严重项同步图谱 Tab「待治理」标记。

### 6.4 Compile 管线（Layer 2 → Layer 3）

```text
原始文档（Layer 1）
   ↓
Ingest Agent → OKF Bundle（Layer 2 · Markdown + YAML + 链接）
   ↓
Compile Service
   ├── 解析 frontmatter.type → node_type
   ├── 解析 body 链接 → rel_type（mentions / contains / appears_in …）
   ├── section 切分 → section 节点 + contains 边
   ├── concept 抽取（或复用 OKF concepts/ 目录）
   ├── BGE-M3 嵌入 → Chroma
   └── 写 knowledge_nodes / knowledge_edges
   ↓
WorkBuddy Skills（ANN 种子 + PPR 扩散 + 子图输出）
```

### 6.5 我们相对 OKF / LLM Wiki 的增量（护城河）

OKF 与 LLM Wiki 解决 **表示与交换**；以下能力需谛听知识网 **自建**：

| 能力 | OKF/Wiki | 谛听增量 |
|------|----------|----------|
| 可读/可 diff | ✅ Markdown git | 同样保留 Layer 2 |
| 交叉链接 | ✅ Markdown link | 编译为 **有类型边** + 权重 |
| 检索 | index + 可选 BM25 | **ANN + PPR + meta-path**，跨文档多跳 |
| 可解释 | 链接路径 | **传导日志 + chunk_id / edge_id 溯源** |
| 进化 | 人工/Agent 改 Wiki | Wiki 变更 **+ 边权突触可塑性**（§7） |
| 行动 | 无 | **Skill 契约 + MCP + Computer Use** |
| 多角色 | 无 | **Buddy 宪法 + Swarm 编排** |

```text
OKF/Wiki = 知识库的「源代码」
知识网 Graph = 编译后的「运行时引擎」
WorkBuddy = 面向业务的「操作系统」
```

### 6.6 对跨境电商的直接价值

| 价值 | 机制 |
|------|------|
| **沉睡数据激活** | PDF / 邮件 / 旧 Listing → Ingest → OKF → 图，永久资产 |
| **多语种对齐** | 同一 `concept/spf50.md` 下挂 en/th/vi 多 Section，编译为跨语种同节点 |
| **跨平台统一** | 170+ 平台详情 → 统一 OKF `type: Product Document`，再映射 ERP SKU |
| **运营可审** | 知识变更走 git PR；Lint 报告可人工批注后再 Compile |
| **Buddy 可解释** | 推荐不只说「相似 chunk」，而说「沿 mentions 从 spf50 概念扩散到这三款 SKU」 |

### 6.7 Phase 1 落地建议（beauty + 导购 Buddy）

| 步骤 | 产出 |
|------|------|
| 1 | 编写 `schema/OKF_ECOM.md`（Concept type 枚举、Ingest/Compile 规则） |
| 2 | 100 商品详情 Ingest → `bundles/beauty/` OKF Bundle |
| 3 | Compile Job v0.1：OKF → 现有 knowledge_nodes/edges |
| 4 | 导购 Buddy 问答验收：对比「纯 RAG chunk」vs「OKF+图子图」 |
| 5 | 可视化：参考 OKF [viz.html](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) 思路，图谱 Tab 已有类似能力 |

### 6.8 仓库目录约定（已落地 · 未接代码）

> **原则**：只新增 `knowledge/`、`third_party/okf/`，**不改动** `data_root` 与现有 salesagent/ditingclient 路径。

```text
wchat/
├── knowledge/                          # Layer 1 + Layer 2 知识资产
│   ├── README.md
│   ├── schema/OKF_ECOM.md              # 电商 OKF 扩展契约 ★
│   ├── raw/{category}/                 # Layer 1 不可变源
│   └── bundles/{category}/             # Layer 2 OKF Bundle
├── third_party/okf/                    # OKF v0.1 本地规范快照
│   ├── SPEC.md · LICENSE.md · UPSTREAM.md
└── docs/ref/M7-3-…md                    # 本方案
```

| 路径 | 状态 |
|------|------|
| [knowledge/schema/OKF_ECOM.md](../../knowledge/schema/OKF_ECOM.md) | ✅ v0.1 定稿 |
| [knowledge/bundles/beauty/](../../knowledge/bundles/beauty/) | ✅ 试点样例（1 SKU + 3 Concept + 1 Playbook） |
| [third_party/okf/SPEC.md](../../third_party/okf/SPEC.md) | ✅ 上游快照 |
| `scripts/okf_compile.py` | 🔜 未建（不影响现有功能） |

---

## 7. 自学习进化：突触可塑性

### 7.1 机制

每条边（`contains` / `mentions` / `appears_in` 等）附带可演化权重：

| 事件 | 边权变化 | 示例 |
|------|----------|------|
| 推荐被采纳 / 成交 / 好评 | weight ↑ | 导购搭配「防晒 + 修护」路径强化 |
| 退货 / 投诉 / 人工否决 | weight ↓ | 错误功效关联弱化 |
| 长期未命中 | staleness ↑ | 图谱 Tab 红色半透明，待运营清理 |
| 高频 traversals | Hub 增厚 | PPR 停留概率提高，「常走的路更宽」 |

### 7.2 阶段效果

| 阶段 | 依赖 | 表现 |
|------|------|------|
| **冷启动** | 知识库初始结构 + LLM Wiki 入库 | 可解释推荐，带来源路径 |
| **热启动** | 边权随使用演化 | 推荐/Listing/选品越来越准 |
| **数据壁垒** | 独家路径权重沉淀 | 竞品难以复制「怎么连、哪条路更准」 |

### 7.3 工程实现（与入库方案 §14.6 对齐）

```json
// knowledge_edges.props_json 示例
{
  "weight": 0.92,
  "traversal_count": 847,
  "last_traversal_at": "2026-07-10T08:00:00Z",
  "staleness": 0.12,
  "pruned": false
}
```

- **在线**：每次 Skill 输出后，根据业务反馈写回 traversals / weight。  
- **离线批处理**：低置信边 `pruned=true`；高置信边固化；与图谱 Tab 运营治理联动。  
- **L3 远期**：R-GCN / HAN 可学习扩散，与今日 PPR **共用 propagate 接口**。

---

## 8. 与平台现有 AI 的互补关系

不替代平台已有投资，而是 **补「岗责 + 知识网 + 编排 + 自学习」四层**。

| 平台已有资产 | 作用 | WorkBuddy 补充什么 |
|--------------|------|---------------------|
| **领域大模型（如 12B SKU 微调）** | 推理能力（脑） | 知识网约束输出 + PPR 可解释路径，降幻觉 |
| **MCP / 百级 OpenAPI** | 执行能力（手） | 身份隔离 + 权限管控 + Orchestrator 路由 |
| **AI Listing / 客服 / 选品工具** | 单点工具能力 | 升级为有角色、有记忆、可组合的数字员工 |
| **卖家运营数据** | 数据资产 | 结构化入库 + 边权自演化 |

```text
平台提供「脑 + 手 + 数据」  →  我们提供「宪法 + 知识网 + Swarm + 进化」
```

**集成方式**：Buddy 的 `skill_output` 调用平台 MCP；推理层 PO C 用 Claude，生产切换平台模型；知识网与 Skill 契约 **保持独立部署**，可按 SaaS / 私有化交付。

---

## 9. 实施路径

### Phase 1（1–2 个月）—— 单点验证

| 项 | 内容 |
|----|------|
| **范围** | 1 个品类（如 beauty）+ 1 个角色（导购 Buddy） |
| **交付** | OKF Bundle（`bundles/beauty/`）+ Compile → 知识网；`schema/OKF_ECOM.md` |
| **跑通** | 用户问功效 → PPR 子图 → 导购 Buddy 推荐 + 四步话术 |
| **验收** | 推荐准确率、溯源完整率、用户满意度；路径可解释（非黑盒 chunk） |

### Phase 2（3–4 个月）—— 多角色扩展

| 项 | 内容 |
|----|------|
| **范围** | +2~3 品类；上线文案 Buddy、选品 Buddy |
| **交付** | 对接平台 MCP；Orchestrator 多 Buddy 编排 |
| **跑通** | `@总管 生成 Listing 并优化标题 A/B` → 文案 Buddy + 平台发布 API |
| **验收** | Listing 点击率、选品人效、MCP 调用成功率 |

### Phase 3（5–6 个月）—— 深化与进化

| 项 | 内容 |
|----|------|
| **范围** | 全品类；库存 Buddy；突触可塑性上线 |
| **交付** | 边权自演化批处理；数字员工运营 Dashboard |
| **跑通** | 成交/退货反馈 → 边权更新 → 下一轮推荐自动变准 |
| **验收** | 边权演化可审计；Dashboard 展示 Buddy 任务量、采纳率、ROI |

---

## 10. 预期收益

### 10.1 卖家侧

| 收益 | 说明 |
|------|------|
| **人效** | 重复咨询、Listing 迭代、选品初筛由 Buddy 代劳，人聚焦策略与例外 |
| **质量** | 推荐/文案带来源子图，可审查、可溯源，减少「AI 胡编」信任危机 |
| **多语种** | 同一 concept 跨语种对齐，一套知识服务多站点 |
| **越用越准** | 成功路径沉淀在边权，非每次从零 prompt |

### 10.2 平台侧

| 收益 | 说明 |
|------|------|
| **差异化** | 从「功能清单」升级为「数字员工编制」，提高 ARPU 与粘性 |
| **数据壁垒** | 独家知识网 + 演化边权，难以被通用 WorkBuddy 复制 |
| **合规可控** | 岗责宪法 + 私有化部署，卖家数据不出域 |
| **资产复用** | 现有大模型、MCP、Listing/客服工具 **升级而非废弃** |

### 10.3 可量化指标（建议 POC 起跟踪）

- 导购：推荐采纳率、搭配成交率、平均响应时长  
- 文案：Listing 点击率、转化率、A/B 胜出率  
- 选品：新品建议命中率、调研人时节省  
- 系统：PPR 路径采纳率、边权演化幅度、MCP 调用成功率  

---

## 11. 模型选型与合规说明

> 图 4 · 场景 × 模型 × 合规红线

| 场景 | 推荐模型 | 原因 |
|------|----------|------|
| **POC / 范式验证** | Claude Opus / Sonnet API | 复杂推理、多步 Agent、Swarm 行为验证最快 |
| **生产环境（默认）** | 平台自研领域模型 / DeepSeek V3·R1 私有化 | 数据不出域、成本可控、可与 SKU 语料微调 |
| **特殊任务（小语种 / 长文本）** | 按任务路由，知识网统一上下文 | 通过 Orchestrator + Skill 层灵活切换，**不换知识网** |

### 合规红线

```text
卖家数据（订单 / 客户 / 商品 / 对话）不得出境；
生产环境默认不使用境外 API；
Claude 仅用于 POC 阶段验证范式与编排逻辑。
```

**工程保障**：

- 推理网关与知识库 **物理/逻辑隔离**，可部署在卖家 VPC；  
- 岗责宪法显式限制 Buddy 可访字段；  
- 审计日志：每次 `skill_output` 附 `chunk_id` / `edge_id` 溯源链。

---

## 12. 下一步行动

| # | 行动 | 负责 | 产出 |
|---|------|------|------|
| 1 | 确认 Phase 1 试点品类与 Buddy（建议 beauty + 导购） | 产品 | 试点范围一页纸 |
| 2 | 编写 `schema/OKF_ECOM.md` + Ingest 100 商品 → `knowledge/bundles/beauty/` | 工程 | OKF Bundle + Compile 验收报告 |
| 3 | 岗责宪法 v0.1（导购 Buddy 权限/API/输出模板） | 产品+工程 | `constitution/cs_buddy_v0.json` |
| 4 | Orchestrator 技术选型（自研 vs 开源框架） | 架构 | ADR 文档 |
| 5 | 与平台 MCP 清单对齐（首期 20 API 白名单） | 集成 | API 映射表 |
| 6 | Claude POC 2 周：@导购 委托 → 子图 → 话术 + 假 MCP 回写 | 工程 | POC Demo + 指标基线 |
| 7 | 合作模式与数据合规评审 | 商务+法务 | 数据出境评估结论 |

---

## 附录 A · 术语速查

| 术语 | 说明 |
|------|------|
| **WorkBuddy** | 可委托的数字员工，有角色、权限、工具与记忆 |
| **岗责宪法** | Constitutional AI 实践：原则清单约束 Buddy 行为 |
| **Swarm / Subagents** | 多 Buddy 并行/异步协作 |
| **知识网** | document/section/concept/media 异构图 + 有向边 |
| **PPR 神经扩散** | ANN 种子 + 沿 meta-path 的个性化 PageRank |
| **OKF** | [Open Knowledge Format v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)：Markdown + YAML frontmatter 的知识 Bundle 交换格式 |
| **Knowledge Bundle** | OKF 分发单元：可 git clone 的目录树，含 Concept / index / log |
| **LLM Wiki** | [Karpathy 范式](https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/)：LLM 增量维护持久 Wiki，Ingest / Query / Lint 复利 |
| **Compile** | OKF Bundle → 知识网 Graph 的编译作业（Layer 2 → Layer 3） |
| **LLM Wiki Format** | 泛指 Layer 2 编译层；工程上对齐 OKF v0.1 + 电商扩展 type |
| **突触可塑性** | 边权随使用反馈强化/弱化 |

---

## 附录 B · 与谛听文档索引

| 文档 | 关联章节 |
|------|----------|
| [M7-2 宣讲稿](M7-2-谛听-生物数字双模态知识网宣讲稿.md) | 知识网机制、技能集应用、PPR 链路 |
| [知识库-结构化入库方案 §十四](../知识库-结构化入库方案.md) | 节点/边/meta-path、突触可塑性 |
| [M6-2 通用客服](../M6-2-通用客服智能体与话术策略知识库方案.md) | 导购 Buddy · 技能集三栏 |
| [M6-3 智能写作](../M6-3-智能写作技能-文案脚手架方案.md) | 文案 Buddy · doc_writer |
| [M7-1 短视频](../M7-1-短视频创作-导演智能体总体方案.md) | 扩展 Buddy · 素材包血缘 |
| [knowledge/schema/OKF_ECOM.md](../../knowledge/schema/OKF_ECOM.md) | §6 · 仓库契约 · Ingest/Compile |
| [knowledge/bundles/beauty/](../../knowledge/bundles/beauty/) | §6.8 · 试点 Bundle 样例 |
| [M7-3a 离在线关系说明](M7-3a-OKF离线与在线知识库关系说明.md) | 新增目录与 client/salesagent 关系 · Compile 现状 |
| [third_party/okf/SPEC.md](../../third_party/okf/SPEC.md) | OKF v0.1 上游规范 |

---

## 附录 C · OKF × LLM Wiki × 知识网：启示摘要

### C.1 从 Karpathy LLM Wiki 借鉴什么

来源：[LLM Wiki 原文](https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/)

| 启示 | 我们的做法 |
|------|------------|
| Wiki 是 **持久复利资产**，不是每次 RAG 重发现 | Layer 2 OKF Bundle 长期维护；Query 结果回写 |
| LLM 做 **bookkeeping**（交叉引用、更新 10+ 页） | Ingest Agent + Lint 周批 |
| `index.md` 渐进披露，中等规模不必上向量库 | 先 index → 再 PPR 子图；规模化后 BGE 增强 |
| `log.md` 可审计时间线 | 对齐 Buddy 操作日志 + 边权变更 |
| Schema 文件定义 Agent 纪律 | `schema/OKF_ECOM.md` + 岗责宪法 |

### C.2 从 Google OKF 借鉴什么

来源：[OKF README](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) · [SPEC v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)

| 启示 | 我们的做法 |
|------|------------|
| **Vendor-neutral** 交换格式 | 不绑定 Claude；Compile 输出标准知识网 API |
| 最小 conformance：frontmatter + `type` | 电商扩展 type 枚举，消费端宽容未知 type |
| Markdown 链接 = 图边 | Compile 为 `mentions` / `references` |
| `resource` URI 绑真实资产 | 对齐 ERP SKU / 平台 URL |
| Bundle 可 viz 可视化 | 图谱 Tab + 传导日志（已有） |
| Reference Agent 两阶段（元数据 + Web  enrich） | Ingest = 元数据抽取；可选 Web 补平台政策 |

### C.3 我们不必照搬的部分

| OKF/Wiki 默认 | 谛听选择 |
|---------------|----------|
| 查询主要靠读 Markdown | **生产 Query 走 PPR 子图**，Markdown 作源与审计 |
| 无权重/evolution | **突触可塑性**写回边权 |
| 无 Skill / MCP | **WorkBuddy 行动层** |
| 个人 Wiki / 数据 catalog 场景 | 扩展为 **跨境多语种 + 多 Buddy + 合规** |

### C.4 一句话架构口诀

```text
Karpathy 教你怎么「养」Wiki  ·  OKF 规定 Wiki 长什么样  ·  知识网决定 Wiki 怎么「传导」
```

---

*v1.2 · 2026-07-11 · 基于知识网与 Claude 范式的跨境电商 AI WorkBuddy 方案*
