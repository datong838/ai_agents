# M7-5 · Palantir 学习笔记与谛听三层架构白皮书

> **版本**：v1.0 · 2026-07-12  
> **状态**：学习定稿 · 个人知识库  
> **关联**：[Palantir-Foundry-AIP-Ontology-Apollo-解析和优化.pptx](Palantir-Foundry-AIP-Ontology-Apollo-解析和优化.pptx)（v2.2 · L2双引擎） · [M7-6 实时决策架构](M7-6-高性能实时决策架构方案.md) · [M7-4 BDNS](M7-4-BDNS-生物数字自主进化智能体方案.md) · [M7-3 WorkBuddy](M7-3-跨境电商AI-WorkBuddy-知识网与Claude范式方案.md) · [Palantir-Apollo-深度解析.md](Palantir-Apollo-深度解析.md)

---

## 0. 学习原则（别记做法，记为什么）

| 错误学法 | 正确学法 |
|----------|----------|
| 背「Foundry 有 200 个连接器」 | 问：**为什么**要先集成而不是先上 AI？ |
| 背「Ontology 有 Object/Link/Action」 | 问：**为什么**表结构不够，非要「对象+动作」？ |
| 背「AIP 有 Logic/Agent/Evals」 | 问：**为什么** LLM 不能直接查数据库？ |
| 背「Apollo Hub-Spoke」 | 问：**为什么** 不用 Jenkins 而要约束求解？ |

**一句话收获：** Palantir 卖的不是软件功能清单，而是 **「在混乱数据中建立可行动的世界模型」** 的方法论。你去接政府、药企、电商项目，话术应是 **「先本体化，再决策流，再数字员工」**——比「我能写代码」高一个维度。

---

## 1. 核心逻辑：杂乱数据 → 可计算对象

### 1.1 甲方真正的痛

客户手里不是「缺一个算法」，而是：

```text
Excel 补货表 + PDF 产品说明 + ERP 库存 + 平台 Listing HTML
+ 客服聊天记录 + 竞品页面 + 传感器/日志
= 没有人能回答「这款防晒该不该加大泰国站备货？」
```

**为什么 RAG/BI 不够？**

| 方案 | 缺什么 |
|------|--------|
| BI 看板 | 只有聚合数字，没有「对象间关系」和「可执行动作」 |
| 向量 RAG | chunk 无类型、无权限、无动作，每次重发现 |
| 自研大模型 | 模型不懂企业对象世界，幻觉写库 |

### 1.2 Palantir 的答案：Ontology（本体化）

```text
杂乱数据源
   ↓  Foundry：Connectors + Pipeline（清洗，不改源）
Backing Dataset（Iceberg，物理层不动）
   ↓  Funnel：列 → 属性/主键/链接（映射，非复制）
Object / Link / Property（业务对象世界）
   ↓  Action + Function（受控动词）
Workshop / AIP Agent（人类 + AI 行动）
   ↓  可选回写 ERP/平台
真实世界变化
```

**为什么叫 Ontology 而不是「知识图谱」？**

- 知识图谱：偏「描述关系」
- Palantir Ontology：偏 **「可执行」** —— 带 Action（写）、Function（算）、Governance（谁准写）

### 1.3 你的甲方话术（直接可用）

> 「我们不急着上大模型。第一阶段做 **数据本体化**——把你们的 Excel、平台数据、客服记录，统一映射成 **商品对象、功效概念、订单事件** 和它们之间的关系。第二阶段在这个本体上构建 **决策流和数字员工**。这样 AI 不是在猜，是在你们定义的业务世界里行动。」

---

## 2. Palantir 四大核心 & 为什么这样分

### 2.1 总览

```text
Foundry  → 为什么：数据孤岛无法决策
Ontology → 为什么：表没有「动作」和「权限」
AIP      → 为什么：LLM 需要世界边界，不能直写库
Apollo   → 为什么：同一套系统要跑在云端、机房、气隙、边缘
```

### 2.2 Foundry — 企业数据操作系统

**是什么：** 集成、治理、管道、分析应用的平台（Contour/Quiver/Workshop）。

**为什么独立一层：**

- 企业已有 ERP/CRM/WMS，不会推倒重来
- Foundry **叠加** 在现有系统之上，做统一数据湖（MMDP / Iceberg）
- 没有这一层，Ontology 无米下锅

**你的映射 → L1 数据本体层（离线）**

| Palantir | 谛听 |
|----------|------|
| Connectors + Pipeline | `knowledge/raw/` 接入 + Ingest |
| Dataset (Iceberg) | Layer 1 不可变源 |
| Workshop 低代码 | ditingclient 运营界面（远期） |

### 2.3 Ontology — 可执行语义内核

**是什么：** Object Type / Link / Action / Function / Governance 三区并列。

**为什么三区并列（不是三层堆叠）：**

- 读对象时同时要裁决「谁能看」「能执行什么动作」
- AI Agent 若只能读不能写，或只能写不能审，都无法上线生产

**你的映射 → L1 规范 + L2 引擎的「基因」**

| Palantir | 谛听 |
|----------|------|
| Object/Link Schema | `OKF_ECOM.md` + Compile → `knowledge_nodes/edges` |
| Action Type | WorkBuddy Skill 写回 + MCP |
| Governance | 岗责宪法 + 行列权限 |

### 2.4 AIP — AI 编排治理层

**是什么：** k-LLM / Logic / Agent Studio / Assist / Evals。

**为什么不让 LLM 直接 SQL：**

- 概率模型 + 确定性数据 = 灾难（幻觉写库）
- 正确模式：**LLM 提议 → 系统校验权限 → 确定性执行 Action**

**你的映射 → L2 决策智能层（在线）**

| Palantir | 谛听 |
|----------|------|
| AIP Logic Block 链 | `activate → propagate → package → llm → skill_output` |
| Agent World Definition | Buddy 岗责宪法 + 工具白名单 |
| Evals 门控 | Skill 策略验收 + 人工抽检 |
| Ontology Tool | PPR 子图 + `agent_skills` |

### 2.5 Apollo — 自主部署操作系统

**是什么：** Hub-Spoke、约束求解、气隙交付、舰队回滚。

**为什么不是 Jenkins：**

- 客户环境：公有云 + 私有云 + 断网战术节点
- 300+ 微服务有 **产品级依赖**，不是一份 YAML 能描述
- 需要「约束满足才升级」，不是「强制收敛到版本 v1.2.3」

**你的映射 → L3 行动交付层（交互 + 运维）**

| Palantir | 谛听 |
|----------|------|
| Apollo Plan 编排 | 私有化部署 / 多租户发布流水线（待建） |
| Rubix 蓝绿 | salesagent 滚动升级 + 健康检查 |
| Release Channel | beauty 试点 → 全品类 通道 |
| 数字孪生可视化 | 图谱 Tab + 传导日志 |

---

## 3. 你的 L1 / L2 / L3 架构（技术白皮书核心）

> **话术：** 「我研究了一套基于 Palantir 思想的国产自主架构，L1/L3 复用全球最佳实践，L2 双引擎并行——AIP 主路 + 自研加速补位。」

```text
┌─────────────────────────────────────────────────────────────┐
│  L3 交互界面 — 对标 Palantir Apollo                          │
│  数字孪生大屏 · 运营操作后台 · 图谱/Workshop 可视化             │
│  谛听：ditingclient · WorkBuddy · MCP 行动                    │
├─────────────────────────────────────────────────────────────┤
│  L2 决策层（双引擎并行）                                      │
│  ┌────────────────────────┬────────────────────────────┐    │
│  │ Palantir 原生 AIP       │ 自研实时决策引擎              │    │
│  │ K-LLM · 检索→生成【主路】│ PPR+ANN+EGB · 过滤→快决策【应急】│    │
│  └────────────────────────┴────────────────────────────┘    │
│  左：环科院政策查询 / 常规客服  │  右：直播间弹幕 / 订单洪峰    │
├─────────────────────────────────────────────────────────────┤
│  L1 离线本体层 — 对标 Palantir Ontology / Foundry            │
│  OKF Bundle · raw/ · Ingest/Compile · git 审计              │
└─────────────────────────────────────────────────────────────┘
```

> **v2.0 术语拉齐：** L3 统一叫「交互界面」；L2 不是「自研替代 AIP」，而是 **双引擎并列、互为备份**。详见 [M7-6](M7-6-高性能实时决策架构方案.md)。

### 3.1 与 BDNS 五层对照

| BDNS 层 | 你的 Lx | Palantir 近似 |
|---------|---------|---------------|
| EGB 基因 | L1（schema）/ L2右（调优） | OMS Schema + 边权演化 |
| ANN 感知 | L2 右引擎 | BGE + OSS 检索 |
| PPR 反射/思考 | L2 右引擎 | Search Around + Logic |
| Cortex 思考 | **L2 左引擎** | **AIP Logic + K-LLM** |
| Body Loop | L3 | Action 写回 + Apollo 运维 |
| LIFE LOOP | L1↔L3 | Feedback → 基因/边权演化 |

### 3.2 与 M7-3 WorkBuddy 对照

| WorkBuddy | 落在哪层 |
|-----------|----------|
| 导购/文案/选品/库存 Buddy | L2 Skill + L3 行动 |
| OKF Ingest/Compile | L1 |
| PPR 子图生产 Query | L2 |
| MCP / 平台 API | L3 |
| 突触可塑性 | L2 边权 → L1 Synthesis 回写 |

---

## 4. 零售 / 电商：Palantir 做了什么 & 你的预制菜

### 4.1 公开案例（有据可查）

| 客户/场景 | Palantir 做了什么 | 量化（公开） | 痛点 |
|-----------|-------------------|--------------|------|
| **C&A 时尚零售** | Foundry 数字孪生 + AI 采购推荐 | 3 个月上线全流程 | 库存周转、过库存 |
| **匿名巴西时尚零售商** | Foundry 库存优化（白皮书） | +$16M；SKU 可用性 +13% | 缺货/积压 |
| **F&B 快消**（白皮书泛述） | 实时运营画面、减过库存 | — | 供应链可视化 |
| **Walmart** | ⚠️ **非公开 Palantir 客户**；自有 Retail Link + Load Planner + 数字孪生 | — | 供应链 AI |
| **可口可乐** | ⚠️ 无公开 Palantir 案例 | — | — |

**C&A 关键句（PR Newswire 2023）：**

> 「We formed a Digital Twin of the company's logistics chain… simulate new rules and scenarios.」

### 4.2 零售共性痛点 → 你的「马帮预制菜」

| 痛点 | Palantir 解法 | 谛听/马帮 预制菜 |
|------|---------------|------------------|
| 库存周转 | 数字孪生 + 需求信号 + 自动补货建议 | **库存 Buddy** + 销量时序边 |
| 供应链断链 | 多源集成 + 情景模拟 | 多平台数据入 OKF + PPR 传导 |
| 动态定价 | 成本分摊到 SKU + 弹性模型 | 竞品 concept 扩散 + 定价 Skill |
| 用户画像 | Object 统一 + 跨渠道链接 | 导购 Buddy + `mentions` 功效→商品 |
| Listing 优化 | 商品对象 + 外部信号（竞品价） | **文案 Buddy** + SEO/AEO Skill |
| 数字员工 | AIP Agent + HITL | WorkBuddy 四角色 + 岗责宪法 |

### 4.3 预制菜交付模板（单干可用）

```text
Phase 0 · 2 周 POC（¥30-80万）
  L1：50 SKU Ingest → OKF Bundle 样例
  L2：导购 Buddy 问答 + PPR 溯源
  交付：对比「纯 RAG」报告

Phase 1 · 3 月 MVP（¥150-300万）
  L1：全品类 OKF + Compile 管道
  L2：导购 + 文案 Buddy + 图谱 Tab
  L3：单租户私有化部署

Phase 2 · 年框（¥80-200万/年）
  L2：选品/库存 Buddy + 边权演化
  L3：多店铺扩展 + 运维 SLA
```

---

## 5. 定价与交付模式（接项目必读）

### 5.1 Palantir 怎么收钱（公开信息综合）

| 层级 | 内容 | 参考区间 |
|------|------|----------|
| **平台年费** | Foundry/AIP 核心 License，3-5 年约 | $5M–$25M/年 起 |
| **扩展消费** | 数据源数、用户数、Ontology 类型、算力、AIP Token | 按量叠加 |
| **专业服务** | Forward Deployed Engineers（FDE）驻场实施 | $200K–$500K/人/年 |

**Land-and-Expand 路径：**

```text
Pilot（$1-5M）→ 部门扩展（$10-25M）→ 企业基础设施（$50-100M+/年）
NRR > 118%（客户持续加购）
```

**卖的不是席位，是「决策能力」+ 极高切换成本。**

### 5.2 Palantir 怎么交付

| 模式 | 说明 |
|------|------|
| **软件 License** | 年费 upfront；产品「交付」= 开通访问权 |
| **FDE 驻场** | 初期 2-5 人嵌入客户，建本体+应用；成熟后减少 |
| **气隙/边缘** | 签名离线包 + Spoke 自治升级 |
| **不负责** | 不替客户做业务流程外包；提供 OS，客户/PA 共建 |

### 5.3 你可借鉴的定价（国产化）

| 收费项 | 建议 | 为什么 |
|--------|------|--------|
| **本体建模费** | 一次性，按品类/SKU 规模 | 对应 Palantir FDE 前期价值 |
| **平台年费** | 按店铺数/SKU 数/ Buddy 数 | 对应扩展消费 |
| **实施 POC** | 固定价 2 周 | 降低甲方决策门槛 |
| **运维 SLA** | 年框 15-20% | 对应 Apollo 持续运维 |

**避免：** 纯人力外包计价（像外包公司）；**要做：** 平台 + 本体资产积累（切换成本）。

---

## 6. 从 Palantir 到谛听的「为什么」清单

| # | Palantir 做法 | 根本原因 | 谛听已有什么 | 缺什么 |
|---|---------------|----------|--------------|--------|
| 1 | 200+ Connectors | 数据孤岛是决策前提 | 170+ 平台详情经验 | OKF 统一 Ingest |
| 2 | Ontology 三区 | 名词/动词/权限同时裁决 | PPR 图 + Skill | Compile + Action 写回 |
| 3 | OSv2 解耦 | 规模到数十亿对象 | ANN+PPR 生产 | 反射缓存/多层 PPR |
| 4 | AIP HITL | LLM 不能自动写生产 | 人工审核话术 | Draft Action 流程 |
| 5 | Evals 门控 | 非确定性输出无法上线 | verify 脚本 | Agent 级 Evals |
| 6 | Apollo 约束求解 | 多环境舰队自治 | 单仓 salesagent | 多租户发布编排 |
| 7 | 数字孪生 | 模拟先于行动 | 图谱 Tab | 供应链仿真 Skill |
| 8 | 边权/反馈 | 越用越准 | M7-3 突触可塑性设计 | 批处理未上线 |

---

## 7. 投资人 / 老板 / 甲方 三版话术

### 7.1 投资人（30 秒）

> 我们采用 Palantir 验证过的 **L1 本体化 + L2 决策引擎 + L3 数字员工** 三层架构，但聚焦跨境电商垂直场景。L1 用 OKF 标准做知识源码，L2 用自研 PPR 神经扩散替代昂贵 Ontology 全家桶，L3 用 WorkBuddy 数字员工直接产生 GMV 和人效。比通用 Palantir 轻一个数量级，比纯 LLM SaaS 深一个维度。

### 7.2 老板 / 技术负责人（1 分钟）

> Palantir 教我们的不是买 Foundry，而是 **先本体、再决策、再 AI**。我们已有 PPR 知识网和客服/文案 Skill，下一步把 OKF Compile 和边权演化接上，就是自己的 BDAEA。Apollo 思想用于私有化交付，不依赖境外 API。

### 7.3 甲方电商客户（2 分钟）

> 你们现在的问题是数据在 Excel、平台后台、客服系统里各睡各的。我们第一步 **本体化**——把商品、功效、订单、Listing 变成统一对象和关系；第二步 **决策流**——导购推荐、文案生成带来源路径；第三步 **数字员工**——@Buddy 委托任务。先 2 周 POC 看对比，再谈年框。

---

## 8. 文档与 PPT 索引

| 资源 | 用途 |
|------|------|
| [Palantir-Foundry-AIP-Ontology-Apollo-解析和优化.pptx](Palantir-Foundry-AIP-Ontology-Apollo-解析和优化.pptx) | **主 PPT v2.2**（L2双引擎并列 · 20页） |
| [Palantir-Foundry-AIP-Ontology-深度解析.pptx](Palantir-Foundry-AIP-Ontology-深度解析.pptx) | 文字详版 v1（28 页，备查） |
| [Palantir-Apollo-深度解析.md](Palantir-Apollo-深度解析.md) | Apollo 专题 |
| [docs/palantier PRD 规划](../palantier/00-索引.md) | **全链路解剖 + PRD 框架 + 武器谱** |
| [M7-3 WorkBuddy](M7-3-跨境电商AI-WorkBuddy-知识网与Claude范式方案.md) | 产品方案 |

---

## 9. 准确性声明

- 零售案例：**C&A** 有 PR 来源；沃尔玛/可口可乐与 Palantir 的关联 **无可靠公开来源**，本文未写。
- 定价区间：来自公开市场分析（Coomia 等）及 SEC 合同模板，**非 Palantir 官方价目表**。
- L1/L2/L3 映射：基于 Palantir 思想的 **谛听自主诠释**，非 Palantir 官方术语。

---

*v1.0 · 2026-07-12 · 学习笔记 · 从 Palantir 到谛听 L1/L2/L3*
