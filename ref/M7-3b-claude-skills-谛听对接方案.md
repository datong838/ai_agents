# M7-3b · claude-skills 筛选与谛听 WorkBuddy 对接方案

> **版本**：v1.0 · 2026-07-11  
> **状态**：方案定稿 · 筛选完成 · **未接入 salesagent**  
> **上游仓库**：`claudeskills/`（镜像 [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)）  
> **关联**：[M7-3 WorkBuddy 方案](M7-3-跨境电商AI-WorkBuddy-知识网与Claude范式方案.md) · [M7-3a OKF 离在线关系](M7-3a-OKF离线与在线知识库关系说明.md) · [M6-2 客服技能集](../M6-2-通用客服智能体与话术策略知识库方案.md) · [M6-3 智能写作](../M6-3-智能写作技能-文案脚手架方案.md) · [M7-1 短视频](../M7-1-短视频创作-导演智能体总体方案.md)

---

## 1. 文档目的

从本地 `claudeskills/`（355 Skill / 99 Agent / 7 Persona / 13 平台）中，**筛选适合谛听跨境电商 WorkBuddy 场景的 Skill 子集**，并给出与现有 `activate → propagate → package → llm → skill_output` 契约的对接路径。

**本方案不做的事：**

- 不整包导入 355 个 Skill（体量过大、SaaS 偏置、与自研知识网重复）
- 不替换已有 `cs_dialogue` / `doc_writer` 等落地 Skill
- 不在 POC 阶段调用境外 API 或外发卖家数据

---

## 2. 筛选原则

| 维度 | 标准 |
|------|------|
| **业务贴合** | 直接服务 Listing、导购、选品、短视频、跨境合规、OKF 知识维护 |
| **契约兼容** | `SKILL.md` 结构可映射为谛听 `agent_skills` 策略包（manifest + prompts + references） |
| **知识网协同** | 产出可挂 `chunk_id` / `concept` 溯源，或回写 Layer 2 OKF Bundle |
| **工程可行** | Python 脚本 stdlib-only 可本地复用；不依赖 pip / 境外 SaaS API |
| **合规** | 生产环境数据不出域；境外 Skill 仅作 **参考模板** 或 **POC 编排逻辑** |

**优先级定义：**

| 级别 | 含义 | 接入策略 |
|------|------|----------|
| **P0** | 与 Buddy 核心任务直接对齐 | Phase 1 试点优先改编 |
| **P1** | 强支撑、需跨境电商语境适配 | Phase 2 按需引入 |
| **P2** | 参考借鉴，不直接上线 | 文档/写作规范参考 |

---

## 3. 架构映射：claude-skills ↔ 谛听

### 3.1 三层概念对齐

| claude-skills | 谛听 M7-3 | 对接方式 |
|---------------|-----------|----------|
| **Skill**（How） | `agent_skills` 策略包 + Skill 契约 | 改编 `SKILL.md` → `manifest.json` + `prompts/` |
| **Agent**（What） | WorkBuddy 角色入口 / Orchestrator 子任务 | 参考 `agents/cs-*.md` 编排模式 |
| **Persona**（Who） | 岗责宪法 + Buddy 人格 | 参考 `agents/personas/`，写入 `constitution/` |

### 3.2 执行链路映射

```text
claude-skills 原生：
  用户 Prompt → 加载 SKILL.md → scripts/ 辅助 → LLM 产出

谛听 WorkBuddy：
  @Buddy 委托 → activate(strategy_id)
            → propagate(PPR 子图)
            → package(子图 + 策略 + 用户意图)
            → llm(可切换模型)
            → skill_output(附溯源)
            → 边权更新 / OKF 回写
```

**关键差异：** 谛听 **生产 Query 走 PPR 子图**，claude-skills 默认 **读 Markdown + scripts**。对接时须把 claude-skills 的 `references/` 迁入 OKF Layer 2 或 `agent_skills` 附表，**检索层仍用 PPR**。

### 3.3 知识层映射

| claude-skills Skill | 谛听知识层 | 说明 |
|---------------------|------------|------|
| `llm-wiki` | Layer 2 OKF Bundle + `index.md` / `log.md` | 与 Karpathy 范式、M7-3 §6 直接对齐 |
| `arquiteto-de-empresa` | `knowledge/schema/OKF_ECOM.md` + Bundle 脚手架 | 含 `okf_linter.py`、`scaffold_bundle.py` |
| `marketing-context` | 店铺级 `marketing-context.md` Concept | 品牌声线 / ICP，供文案/导购共用 |
| `rag-architect` | Layer 3 PPR 评测参考 | **不替代 PPR**；用于分块/评测方法论 |

---

## 4. 按 Buddy 筛选清单

### 4.1 文案 Buddy（Listing / SEO / AEO / 多语）

> 对齐 M6-3 `doc_writer`；claude-skills 补强 SEO、AEO、结构化数据、竞品对比页。

| 优先级 | Skill | 路径（相对 `claudeskills/`） | 用途 |
|--------|-------|------------------------------|------|
| P0 | copywriting | `marketing-skill/skills/copywriting/` | Listing 标题/卖点/CTA 写作框架 |
| P0 | copy-editing | `marketing-skill/skills/copy-editing/` | 多轮润色已有 Listing |
| P0 | content-production | `marketing-skill/skills/content-production/` | 长文/指南端到端生产 |
| P0 | content-humanizer | `marketing-skill/skills/content-humanizer/` | 去 AI 腔，适配多语种自然度 |
| P0 | seo-audit | `marketing-skill/skills/seo-audit/` | 技术/On-page SEO 诊断 |
| P0 | aeo | `marketing-skill/skills/aeo/` | Answer Engine Optimization，LLM 引用优化 |
| P0 | schema-markup | `marketing-skill/skills/schema-markup/` | Product/FAQ JSON-LD，富摘要 |
| P0 | programmatic-seo | `marketing-skill/skills/programmatic-seo/` | 品类/对比/地域页批量 SEO |
| P0 | competitor-alternatives | `marketing-skill/skills/competitor-alternatives/` | 竞品对比 Listing 结构 |
| P0 | marketing-context | `marketing-skill/skills/marketing-context/` | 店铺品牌上下文（全营销 Skill 前置） |
| P0 | brand-guidelines | `marketing-skill/skills/brand-guidelines/` | 跨站点品牌一致性 |
| P1 | page-cro | `marketing-skill/skills/page-cro/` | 商品页转化率优化 |
| P1 | prompt-engineer-toolkit | `marketing-skill/skills/prompt-engineer-toolkit/` | 文案 Prompt 版本化与 A/B |
| P1 | research-summarizer | `product-team/research-summarizer/skills/research-summarizer/` | 研究资料摘要 → Listing 论据 |
| P2 | local-seo-manager | `marketing-skill/skills/local-seo-manager/` | 本地商家 SEO（跨境自营站弱相关） |

**Agent 编排参考（非 SKILL）：**

- `agents/marketing/cs-content-creator.md` — 内容生产质量门禁
- `agents/marketing/cs-aeo.md` — AEO 审计编排

---

### 4.2 导购 Buddy（客服 / 转化 / 留存）

> 对齐 M6-2 `cs_dialogue`；claude-skills 补强心理模型、挽留、邮件序列。

| 优先级 | Skill | 路径 | 用途 |
|--------|-------|------|------|
| P0 | customer-success-manager | `business-growth/skills/customer-success-manager/` | 客户健康分、流失风险 |
| P0 | churn-prevention | `marketing-skill/skills/churn-prevention/` | 取消/挽留流程、催款邮件 |
| P0 | email-sequence | `marketing-skill/skills/email-sequence/` | 欢迎/复购/唤醒序列 |
| P1 | marketing-psychology | `marketing-skill/skills/marketing-psychology/` | 70+ 消费心理模型 → 话术 |
| P1 | behuman | `engineering/behuman/skills/behuman/` | 降低机器感，提升对话自然度 |
| P1 | form-cro / popup-cro | `marketing-skill/skills/form-cro/` 等 | 结账/询盘摩擦优化 |
| P1 | ab-test-setup | `marketing-skill/skills/ab-test-setup/` | 话术 A/B 实验设计 |
| P1 | pulse | `research/pulse/skills/pulse/` | 近期口碑/痛点脉冲（FAQ 素材） |
| P2 | referral-program | `marketing-skill/skills/referral-program/` | 推荐激励（偏 SaaS） |

---

### 4.3 选品 Buddy（市场 / 竞品 / 跨境进入）

> 对齐 M7-3 选品增强；claude-skills 补强 TAM 测算、深度调研、竞品拆解。

| 优先级 | Skill | 路径 | 用途 |
|--------|-------|------|------|
| P0 | market-research | `research-ops/skills/market-research/` | TAM/SAM/SOM、调研样本、细分评分 |
| P0 | research-ops-skills | `research-ops/skills/research-ops-skills/` | 研究子技能路由 |
| P0 | deep-research | `research/deep-research/skills/deep-research/` | 多源三角验证决策级调研 |
| P0 | pulse | `research/pulse/skills/pulse/` | Reddit/HN/社媒趋势与口碑 |
| P0 | research | `research/research/skills/research/` | 研究请求总路由 |
| P0 | competitive-teardown | `product-team/skills/competitive-teardown/` | 12 维竞品矩阵、战卡 |
| P0 | intl-expansion | `c-level-advisor/skills/intl-expansion/` | 跨境市场选择、进入模式、本地化 |
| P1 | product-research | `research-ops/skills/product-research/` | 用户研究方法、样本量 |
| P1 | product-discovery | `product-team/skills/product-discovery/` | 假设验证、发现冲刺 |
| P1 | pricing-strategy | `marketing-skill/skills/pricing-strategy/` | 定价层级、毛利测算 |
| P1 | competitive-intel | `c-level-advisor/skills/competitive-intel/` | 系统化竞品追踪 |
| P1 | universal-scraping-architect | `engineering/universal-scraping-architect/skills/universal-scraping-architect/` | 竞品/平台数据采集架构 |
| P2 | patent | `research/patent/skills/patent/` | 硬货选品 IP 格局 |

---

### 4.4 库存 Buddy（缺口与替代）

> **claude-skills 无 WMS/补货/安全库存专用 Skill**。以下为最接近组合：

| 优先级 | Skill | 路径 | 用途 |
|--------|-------|------|------|
| P1 | market-research | `research-ops/skills/market-research/` | 市场规模 → 备货量级参考 |
| P1 | pulse | `research/pulse/skills/pulse/` | 需求/口碑信号 → 补货判断 |
| P1 | product-analytics | `product-team/skills/product-analytics/` | KPI、队列/留存分析 |
| P1 | data-quality-auditor | `engineering/data-quality-auditor/skills/data-quality-auditor/` | SKU/订单数据质量审计 |
| P1 | statistical-analyst | `engineering/statistical-analyst/skills/statistical-analyst/` | 销量实验假设检验 |
| P2 | revenue-operations | `business-growth/skills/revenue-operations/` | 管道预测（偏 SaaS） |

**建议：** 库存 Buddy 核心逻辑 **自研**（规则引擎 + 时序边，见 M7-3 §4 Phase 3），claude-skills 仅提供数据分析方法论参考。

---

### 4.5 短视频 Buddy（M7-1 扩展）

> 对齐 M7-1 导演/编剧/美术 Skill 链；claude-skills 补强社媒策略与投放。

| 优先级 | Skill | 路径 | 用途 |
|--------|-------|------|------|
| P0 | video-content-strategist | `marketing-skill/video-content-strategist/skills/video-content-strategist/` | 短视频策略、脚本、TikTok/Reels/Shorts |
| P0 | social-content | `marketing-skill/skills/social-content/` | 多平台帖文、内容日历 |
| P1 | social-media-analyzer | `marketing-skill/skills/social-media-analyzer/` | 互动率、跨平台 ROI |
| P1 | ad-creative | `marketing-skill/skills/ad-creative/` | 短视频广告文案变体 |
| P1 | paid-ads | `marketing-skill/skills/paid-ads/` | Meta/TikTok/Google 投放策略 |
| P1 | youtube-full | `marketing-skill/skills/youtube-full/` | 竞品视频研究、转录 |
| P1 | demo-video | `engineering/demo-video/skills/demo-video/` | 产品演示视频自动化 |
| P2 | x-twitter-growth | `marketing-skill/skills/x-twitter-growth/` | X 平台增长 |

**注意：** M7-1 已有编剧/美术/分镜 Skill 链，短视频 Buddy **以 M7-1 为主、claude-skills 为辅**，避免双轨脚本规范冲突。

---

### 4.6 Orchestrator / 知识基础设施

> 店铺总管、OKF 维护、跨 Buddy handoff。

| 优先级 | Skill | 路径 | 用途 |
|--------|-------|------|------|
| P0 | agent-harness | `engineering/agent-harness/skills/agent-harness/` | 任意域 Skill → 可验证闭环 Agent 循环 |
| P0 | llm-wiki | `engineering/llm-wiki/skills/llm-wiki/` | 持久 Wiki 增量维护（对齐 M7-3 §6） |
| P0 | arquiteto-de-empresa | `c-level-advisor/skills/arquiteto-de-empresa/` | OKF Bundle 脚手架 + `okf_linter.py` |
| P0 | handoff | `productivity/handoff/skills/handoff/` | 跨 Buddy 会话交接文档 |
| P0 | marketing-ops | `marketing-skill/skills/marketing-ops/` | 营销多 Skill 战役编排 |
| P0 | marketing-skills | `marketing-skill/skills/marketing-skills/` | 44 营销 Skill 目录路由 |
| P0 | agent-workflow-designer | `engineering/skills/agent-workflow-designer/` | 多 Agent 流水线与 handoff 契约 |
| P1 | capture | `productivity/capture/skills/capture/` | 杂乱输入结构化捕获 |
| P1 | chief-of-staff | `c-level-advisor/skills/chief-of-staff/` | 跨域问题路由 |
| P1 | orchestration 协议 | `orchestration/ORCHESTRATION.md` | Persona + Skill + Agent 分阶段编排（文档） |

**组合示例（M7-3 §4.1）：**

```text
@店铺总管 把这款防晒做成 Shopee Listing 并配三条 FAQ

Orchestrator:
  Phase 1 → 文案 Buddy：copywriting + seo-audit + schema-markup
          （PPR 子图：商品 concept + section）
  Phase 2 → 导购 Buddy：cs_dialogue + marketing-psychology
          （同一子图 → FAQ 话术）
  handoff → 写入 OKF Bundle + 边权更新
```

---

### 4.7 工程治理（平台 Skill 开发）

| 优先级 | Skill | 路径 | 用途 |
|--------|-------|------|------|
| P0 | zero-hallucination-coder | `engineering/zero-hallucination-coder/skills/zero-hallucination-coder/` | 防幻觉开发五步法 |
| P0 | security-guidance | `engineering/security-guidance/skills/security-guidance/` | PreToolUse 安全拦截 Hook |
| P0 | prompt-governance | `engineering/prompt-governance/skills/prompt-governance/` | 生产 Prompt 版本化与 Eval |
| P0 | rag-architect | `engineering/skills/rag-architect/` | RAG 评测方法论（对照 PPR） |
| P1 | write-a-skill | `engineering/write-a-skill/skills/write-a-skill/` | 新 Skill 编写规范 |
| P1 | mcp-server-builder | `engineering/skills/mcp-server-builder/` | 平台 API → MCP 暴露 |
| P1 | llm-cost-optimizer | `engineering/llm-cost-optimizer/skills/llm-cost-optimizer/` | 多 Buddy LLM 成本架构 |
| P1 | skill-security-auditor | `engineering/skills/skill-security-auditor/` | 第三方 Skill 安装前安全扫描 |

---

### 4.8 合规（EU 跨境 / AI 平台）

| 优先级 | Skill | 路径 | 用途 |
|--------|-------|------|------|
| P0 | gdpr-dsgvo-expert | `ra-qm-team/skills/gdpr-dsgvo-expert/` | GDPR 扫描、DPIA、DSAR |
| P0 | eu-ai-act-specialist | `ra-qm-team/skills/eu-ai-act-specialist/` | EU AI Act 风险分级 |
| P0 | ra-qm-skills | `ra-qm-team/skills/ra-qm-skills/` | 15 合规 Skill 路由 |
| P1 | agent-decision-receipts | `ra-qm-team/skills/agent-decision-receipts/` | Agent 决策可验证存证 |
| P1 | contract-and-proposal-writer | `business-growth/skills/contract-and-proposal-writer/` | 含 EU/GDPR 的合同/DPA 模板 |

**明确排除（医疗器械/非电商）：** `mdr-745-*`、`fda-*`、`iso13485-*`、`clinical-research`、`qms-audit-expert` 等。

---

## 5. P0 汇总速查（建议首批改编）

共 **38 个 P0 Skill** + **2 个 Agent 参考**：

| Buddy / 域 | P0 数量 | 核心 Skill |
|------------|---------|------------|
| 文案 | 11 | copywriting, copy-editing, content-production, content-humanizer, seo-audit, aeo, schema-markup, programmatic-seo, competitor-alternatives, marketing-context, brand-guidelines |
| 导购 | 3 | customer-success-manager, churn-prevention, email-sequence |
| 选品 | 7 | market-research, research-ops-skills, deep-research, pulse, research, competitive-teardown, intl-expansion |
| 短视频 | 2 | video-content-strategist, social-content |
| Orchestrator | 8 | agent-harness, llm-wiki, arquiteto-de-empresa, handoff, marketing-ops, marketing-skills, agent-workflow-designer, (+ orchestration 协议) |
| 工程 | 4 | zero-hallucination-coder, security-guidance, prompt-governance, rag-architect |
| 合规 | 3 | gdpr-dsgvo-expert, eu-ai-act-specialist, ra-qm-skills |

---

## 6. 对接实施路径

### 6.1 改编流程（SKILL.md → agent_skills）

```text
claudeskills/{domain}/{skill}/SKILL.md
        │
        ▼ 人工/半自动改编（非直接拷贝）
salesagent/config/agent_skills/{family}/{strategy_id}/
        ├── manifest.json      # id, enabled, triggers, constitution_ref
        ├── prompts/
        │   ├── system.md      # 从 SKILL.md Body 提取
        │   └── workflow.md    # 工作流步骤
        ├── references/        # 从 claude-skills references/ 迁入
        └── scripts/           # 可选：复用 stdlib Python 工具
```

**manifest.json 最小字段（对齐现有 M6-2/M6-3）：**

```json
{
  "id": "listing_seo_v1",
  "family": "doc_writer",
  "enabled": true,
  "triggers": ["Listing SEO", "商品页优化", "AEO 审计"],
  "claude_skills_source": "marketing-skill/skills/seo-audit",
  "constitution_ref": "constitution/copy_buddy_v0.json",
  "ppr_required": true
}
```

### 6.2 分阶段 rollout

| 阶段 | 范围 | 动作 | 验收 |
|------|------|------|------|
| **Phase 0**（当前） | 文档 | 本方案定稿；`claudeskills/` 本地镜像 | 筛选清单评审通过 |
| **Phase 1** | beauty + 导购/文案 | 改编 P0：marketing-context、seo-audit、copywriting、marketing-psychology；`arquiteto-de-empresa` 脚本接入 OKF Lint | POC：@文案 Listing + @导购 FAQ，附 PPR 溯源 |
| **Phase 2** | 选品 + 短视频 | 改编 competitive-teardown、market-research、video-content-strategist；handoff 跨 Buddy | 选品报告 + 短视频脚本共用商品子图 |
| **Phase 3** | Orchestrator + 合规 | agent-harness 编排模式；gdpr-dsgvo-expert 合规检查清单 | 多 Buddy 委托单链路；EU 站点合规审计样例 |
| **Phase 4** | 库存 + 自研补齐 | 库存 Buddy 自研；claude-skills 仅保留 analytics 参考 | 补货建议 + 数据质量报告 |

### 6.3 Cursor 开发侧（可选）

研发团队可在 Cursor 中引用 claude-skills 作为 **Rules / Skills 参考**：

```bash
cd claudeskills
./scripts/convert.sh --tool cursor
./scripts/install.sh --tool cursor --target c:\work\projects\wchat
```

此路径 **仅影响 IDE 辅助开发**，不自动接入 salesagent 生产链路。

### 6.4 与 OKF Compile 的衔接

| 步骤 | 模块 | 说明 |
|------|------|------|
| 1 | `arquiteto-de-empresa` | 用 `scaffold_bundle.py` / `okf_linter.py` 校验 `knowledge/bundles/` |
| 2 | `llm-wiki` | Ingest 流程：raw → Bundle Concept 增量更新 |
| 3 | Compile（待建） | Bundle → `knowledge_nodes` / `knowledge_edges` |
| 4 | PPR | WorkBuddy `propagate` 读 Layer 3 子图 |
| 5 | 回写 | 高价值 `skill_output` → Layer 2 Synthesis Concept |

详见 [M7-3a](M7-3a-OKF离线与在线知识库关系说明.md) §4。

---

## 7. 风险与约束

| 风险 | 说明 | 缓解 |
|------|------|------|
| **SaaS 偏置** | 多数 Skill 默认 B2B SaaS 语境（MRR、PLG） | 改编时替换为 SKU/订单/平台规则语境 |
| **检索层冲突** | claude-skills 偏 Markdown 直读；谛听生产走 PPR | 策略进 `agent_skills`，检索仍用 PPR；references 作 OKF 附表 |
| **库存缺口** | 无原生 WMS Skill | Phase 4 自研；不强行套用 revenue-ops |
| **短视频双轨** | M7-1 已有完整 Skill 链 | claude-skills 仅补社媒策略/投放，不改 M7-1 导演契约 |
| **数据出境** | M7-3 §11 合规红线 | 生产不用境外 API；claude-skills 作离线参考 |
| **许可** | MIT License | 改编产物保留 attribution；不闭源上游脚本逻辑 |
| **维护负担** | 上游 355 Skill 持续更新 | 仅跟踪已改编子集；`manifest.claude_skills_source` 记录溯源版本 |

---

## 8. 明确不引入的 Skill 类别

| 类别 | 原因 |
|------|------|
| 医疗器械合规（MDR、FDA、ISO 13485） | 与跨境电商无关 |
| C-Level 全套 68 Skill | 仅保留 intl-expansion、competitive-intel；其余偏融资/董事会 |
| SaaS 脚手架（saas-scaffolder） | 与谛听技术栈无关 |
| 纯工程 POWERFUL 80 个中的基础设施类 | Terraform、Helm、K8s Operator 等仅研发参考，不进入 Buddy |
| local-seo-manager | 跨境多站点弱相关 |

---

## 9. 下一步行动

| # | 行动 | 负责 | 产出 |
|---|------|------|------|
| 1 | 评审本方案 P0 清单，确认 Phase 1 试点 Skill（建议 5 个） | 产品 | 试点 Skill 一页纸 |
| 2 | 定义 `agent_skills` 改编模板（manifest + constitution_ref） | 工程 | `docs/ref/M7-3c-Skill改编模板.md`（待写） |
| 3 | 将 `arquiteto-de-empresa` 的 `okf_linter.py` 接入 `knowledge/` CI | 工程 | Lint 脚本 + 样例报告 |
| 4 | 改编 `marketing-context` + `seo-audit` → `doc_writer` 新策略包 | 工程 | `listing_seo_v1` manifest |
| 5 | 改编 `marketing-psychology` → `cs_dialogue` 话术增强附表 | 工程 | `cs_psychology_ref_v1` |
| 6 | Orchestrator POC：handoff + 双 Buddy 委托 Demo | 工程 | Demo + 指标基线 |
| 7 | 合规评审：gdpr-dsgvo-expert 检查清单本地化 | 法务+产品 | EU 站点合规附录 |

---

## 附录 A · 文件路径索引

| 资源 | 路径 |
|------|------|
| claude-skills 本地镜像 | `claudeskills/` |
| 谛听已有客服策略 | `salesagent/config/agent_skills/` |
| OKF 电商 Schema | `knowledge/schema/OKF_ECOM.md` |
| 试点 Bundle | `knowledge/bundles/beauty/` |
| M7-3 主方案 | `docs/ref/M7-3-跨境电商AI-WorkBuddy-知识网与Claude范式方案.md` |
| claude-skills 编排协议 | `claudeskills/orchestration/ORCHESTRATION.md` |
| claude-skills 写作标准 | `claudeskills/SKILL-AUTHORING-STANDARD.md` |

---

## 附录 B · 与 M7-3 文档索引

| 文档 | 关联 |
|------|------|
| [M7-3](M7-3-跨境电商AI-WorkBuddy-知识网与Claude范式方案.md) | Buddy 角色、Skill 契约、实施路径 |
| [M7-3a](M7-3a-OKF离线与在线知识库关系说明.md) | OKF Compile、Layer 2/3 分工 |
| [M6-2](../M6-2-通用客服智能体与话术策略知识库方案.md) | 导购 Buddy · `cs_dialogue` |
| [M6-3](../M6-3-智能写作技能-文案脚手架方案.md) | 文案 Buddy · `doc_writer` |
| [M7-1](../M7-1-短视频创作-导演智能体总体方案.md) | 短视频 Buddy 主 Skill 链 |

---

*v1.0 · 2026-07-11 · claude-skills 筛选与谛听 WorkBuddy 对接方案*
