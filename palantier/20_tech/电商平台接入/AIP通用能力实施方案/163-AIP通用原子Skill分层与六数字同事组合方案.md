# 163 · AIP 通用原子 Skill 分层与六数字同事组合方案

> 状态：`DESIGN_PROPOSAL / S2.5_COMPATIBILITY_SLICE_IMPLEMENTED`
>
> 文档性质：能力分层、Skill 治理与后续实施指导；本文件不代表 Skill 已创建、发布、绑定或具备运行授权。
>
> 适用范围：AOS AIP、工作台六数字同事、电商垂直领域资产包、`plugins/ops` 渠道运营插件。
>
> 核心裁决：**六数字同事是角色与编排入口，不是六个大 Skill；Skill 应优先沉淀为跨角色、可独立评估、可组合的原子专业方法。**

---

## 1. 使用的 Rules

1. 先做能力分层与方案，再创建或修改 Skill、插件和代码。
2. AOS 平台内核、AIP 运行时、电商领域资产、渠道适配、客户实例必须分层，不因首个电商案例污染平台通用能力。
3. Agent、Skill、Logic、Tool/Capability、DomainPack、AdapterPack、InstanceOverlay 不得互相冒充。
4. 只有同时满足“稳定输入输出、可独立执行、可独立评估、可跨任务复用”的方法才上提为原子 Skill。
5. 查询、写入、模型调用、浏览器点击等确定性动作优先建模为 Tool/Capability；跨步骤流程由 Logic/Plan 编排。
6. Skill 不持有租户 Secret，不绕过 Data OS、本体、审批、Lease、Receipt、Handoff 与证据门。
7. 历史方案、测试数、发布记录只作为重构线索，不自动等于当前已发布、已绑定或可运行事实。

---

## 2. 为什么需要这份方案

现有方案已经形成三类很有价值的沉淀：

1. `11-AIP决策引擎升级方案` 中描述了私域管家、导购顾问、内容官、客服专员、活动策划师、数据参谋的“技能编排”；
2. `12-工作台层方案/技术方案` 中形成了八个业务工作台、任务合同、证据、审批、执行与复盘闭环；
3. `plugins/ops` 中通过真实平台摸索形成了微商城、微信小店、抖店等渠道认知和经营探究能力。

但三类文档中的“技能”口径并不完全一致。旧方案经常把以下内容都称为 Skill：

- 一个数字同事的完整职责；
- 一条端到端 LogicFlow；
- 一次数据库/API/浏览器查询；
- 一种模型、TTS、FFmpeg 或媒体生成工具；
- 一套电商领域方法；
- 一个具体平台的后台定位与操作路径。

这会产生四个后果：

- 同一方法在多个数字同事内重复定义；
- Skill 粒度过大，无法独立评估、版本化和复用；
- 平台通用方法、电商方法和渠道知识混在一起；
- SkillBinding 绑定的是“大包”，难以解释 Agent 为什么会做、能做到哪一步、缺什么能力。

本方案的目标不是否定旧设计，而是把旧设计中的专业知识重新蒸馏成稳定的能力层次。

---

## 3. 总体能力分层

### 3.1 七种构件的职责

| 构件                   | 回答的问题                    | 典型内容               | 是否是 Skill      |
| -------------------- | ------------------------ | ------------------ | -------------- |
| AgentTemplate / 数字同事 | 谁负责、以什么职责工作              | 数据参谋、内容官、导购顾问      | 否              |
| Skill                | 专家如何完成一个可复用的认知或专业任务      | 归因分析、证据包构建、异议处理    | 是              |
| Logic / Plan         | 多个 Skill、Tool 和人工门怎样按序协作 | 内容生产、活动全生命周期         | 否              |
| Tool / Capability    | 系统能执行什么确定性动作             | 查订单、读数据集、调用模型、发送消息 | 否              |
| DomainPack           | 某个行业“什么对象、指标、规则有意义”      | 商品、订单、客户、达人、价格、活动  | 否，但可携带领域 Skill |
| AdapterPack / 渠道插件   | 某个平台在哪里、怎么读取、怎么操作        | 微信小店菜单、抖店商品发布路径    | 否，但可携带渠道 Skill |
| InstanceOverlay      | 这一个客户/经营实体如何配置          | 实体计划、账号引用、策略参数      | 否              |

### 3.2 一条完整执行链

```text
用户目标 / 经营问题
  → AgentTemplate 选择职责
  → Logic/Plan 拆解阶段
  → SkillBinding 选择专业方法
  → CapabilityBinding 选择数据、模型与工具
  → DomainPack 提供领域对象、指标与规则
  → AdapterPack / plugins/ops 提供渠道观察与操作知识
  → InstanceOverlay 提供当前经营实体配置
  → Eval / Approval / Lease / Receipt / Lineage 形成受控闭环
```

关键点：Skill 负责“怎么思考、怎么做专业判断”；Tool 负责“真正执行一个确定性动作”；AIP 运行时负责“能否执行、以谁的权限执行、如何留证”。

---

## 4. `plugins/ops` 与电商领域资产包的关系

### 4.1 `plugins/ops` 不是 AdapterPack 的替代品

现有渠道插件的价值主要是**可复用的运营程序知识**：

- 平台菜单和页面在哪里；
- 怎样安全地进行只读全域观察；
- 哪些页面、字段和状态能支持某个经营判断；
- 发现数据缺口时怎样形成证据和 DataNeed；
- 获得授权后怎样安全定位并执行单项操作。

AdapterPack 则是平台运行时接入资产：认证、Schema、同步、Webhook、动作协议、错误语义和 Receipt 映射。两者互补：

```text
渠道 Skill：专家知道去哪里看、看什么、如何解释
AdapterPack：系统能够稳定读取、映射或执行
```

### 4.2 电商领域资产包不应吞掉所有 Skill

以下内容属于电商领域资产：

- 商品、SKU、订单、履约、售后、客户、达人、活动、价格等对象语义；
- GMV、转化率、复购率、库存周转、佣金等指标定义；
- 电商选品、促销、达人销售、私域经营等行业规则；
- 电商领域的 EvalPack、模板与组合 Skill。

但“证据构建、异常识别、假设生成、方案比较、影响评估、任务拆解、复盘提炼”等方法并不专属于电商，应沉淀成 AOS 通用原子 Skill。

---

## 5. 判断一个能力是否应该成为原子 Skill

一个候选能力至少满足以下六项中的五项，才建议独立发布：

1. **目标单一**：一句话能说明它解决什么问题；
2. **输入稳定**：输入是明确 DTO、对象引用或 EvidencePack，不依赖隐式上下文；
3. **输出稳定**：有结构化产物、状态、置信度、缺口和证据引用；
4. **可独立评估**：能设计正例、反例、越权例和缺证据例；
5. **跨角色复用**：至少两个 Agent 或两个场景可使用；
6. **失败可解释**：缺数据、缺权限、低置信度和冲突不能被包装成成功。

不满足这些条件时，优先判断它是 Logic、Tool、模板、领域对象还是渠道知识。

---

## 6. 第一批 AOS 通用原子 Skill 候选

这些 Skill 不预设电商语义，可被经营参谋、FDE、行业研究、客服、内容和其他垂直领域复用。

| 候选 Skill | 核心职责 | 结构化输入 | 结构化输出 | 主要复用者 |
|---|---|---|---|---|
| `frame-problem` | 把模糊诉求冻结成可回答的问题、范围和 nonClaims | 目标、约束、对象引用 | ProblemBrief | 数据参谋、FDE、活动策划师 |
| `build-evidence-pack` | 汇总事实、来源、新鲜度、冲突和缺口 | SourceRef、ObjectRef、cutoff | EvidencePack | 所有数字同事 |
| `identify-data-gaps` | 判断现有证据能否回答问题并提出数据需求 | Brief、EvidencePack | DataNeed[]、SourceReadiness | 数据参谋、导购、客服 |
| `profile-data-semantics` | 发现字段、关系、分布、质量和业务语义候选 | DatasetRef、SchemaRef | SemanticProfile、QualityFinding[] | 数据参谋、FDE |
| `form-hypotheses` | 形成可验证的解释候选而不是直接下结论 | 问题、证据、约束 | HypothesisSet | 数据参谋、活动策划师、客服 |
| `diagnose-metric-change` | 分解指标变化并验证驱动因素 | MetricRef、时间窗、维度 | DriverFinding[] | 数据参谋、经营参谋 |
| `analyze-root-cause` | 建立症状—原因—证据—反证关系 | Finding、EvidencePack | RootCauseGraph | 数据参谋、客服、运维角色 |
| `forecast-with-uncertainty` | 给出假设透明的趋势和区间 | 时间序列、外部假设 | Forecast、Assumption[] | 数据参谋、活动策划师 |
| `segment-entities` | 按目标和可解释特征形成分群 | EntitySetRef、目标、特征 | SegmentDefinition[] | 私域管家、导购、数据参谋 |
| `compare-alternatives` | 在共同约束下比较多个方案 | Alternative[]、criteria | ComparisonMatrix、Tradeoff[] | 活动策划师、导购、经营参谋 |
| `estimate-impact` | 估算收益、成本、风险和不确定性 | Proposal、baseline、约束 | ImpactPreview | 活动策划师、经营参谋 |
| `design-experiment` | 把建议转成可验证实验 | Hypothesis、对象、指标 | ExperimentPlan | 内容官、活动策划师、导购 |
| `rank-recommendations` | 按价值、置信度、成本和风险排序 | Recommendation[] | RankedRecommendation[] | 数据参谋、经营参谋 |
| `draft-action-plan` | 把已评审建议转为行动草案 | approved finding、constraints | ActionPlanDraft | 所有业务角色 |
| `plan-responsibilities` | 拆任务、角色、阶段、依赖和接管点 | ActionPlanDraft、catalog | ResponsibilityPlanDraft | 总控、内容官、活动策划师 |
| `verify-claims` | 检查每个主张是否有证据、时效和适用范围 | Artifact、EvidencePack | ClaimCheckResult | 内容官、数据参谋、客服 |
| `review-output-quality` | 按 EvalContract 做一致性、完整性和安全审查 | Artifact、EvalContract | ReviewIssue[]、decision | 所有数字同事 |
| `prepare-handoff` | 将最小上下文、引用和未决问题交给下一角色 | TaskRef、ArtifactRef、refs | HandoffDraft | 所有协作角色 |
| `review-outcomes` | 对计划、执行、结果和偏差进行复盘 | Plan、Receipt、Effect | EffectReview | 数据参谋、活动策划师、内容官 |
| `extract-memory-candidate` | 从复盘中提炼可治理的经验候选 | EffectReview、evidence | MemoryCandidate | 所有数字同事 |

### 6.1 原子 Skill 的共同输出约束

每个 Skill 输出至少包含：

- `status`：`READY / BLOCKED / NEEDS_REVIEW / PARTIAL`；
- `summary`：决策摘要，不保存隐藏推理链；
- `evidenceRefs`：使用了哪些证据；
- `assumptions`：关键假设；
- `uncertainties`：不确定性；
- `conflicts`：证据冲突；
- `missingInputs`：继续工作所需输入；
- `recommendedNextSkill`：仅为建议，不自动越权执行。

---

## 7. 应保留为跨行业专业 Skill 的能力

以下能力不是 AOS 内核原子，但也不应锁死为“电商专属”。它们可以作为专业 Skill 包，被多个行业复用，再由领域 Profile 注入术语、规则和 Eval：

### 7.1 内容与传播

- 内容策略生成；
- Brief 拆解；
- 文案与脚本生成；
- 标题优化；
- 事实、品牌、安全与合规审核；
- 内容效果复盘；
- 渠道内容适配。

### 7.2 客户服务与关系

- 服务意图识别；
- 需求澄清；
- 异议识别与应答设计；
- 投诉分级与升级建议；
- 满意度归因；
- 跟进计划与提醒策略。

### 7.3 研究与决策

- 多来源研究；
- 竞争对象比较；
- 趋势与机会扫描；
- 决策报告组织；
- 研究结论证据审查。

这些 Skill 可服务电商、医疗服务、教育、企业运营等领域；领域差异由 DomainPack 和 Profile 注入，而不是复制整套 Skill。

---

## 8. 必须留在电商垂直领域的 Skill

以下方法直接依赖电商对象、指标或经营机制，适合放入电商 VerticalPack / SolutionPack：

- 经营指标异常诊断；
- 商品结构与选品策略；
- 电商价格、优惠与促销组合；
- 商品推荐、搭配购与加购提升；
- 私域客户生命周期经营；
- 体验品、体验码与链式分销分析；
- 达人发现、匹配、邀约、佣金与履约分析；
- 订单、物流、退款、售后与客诉治理；
- 库存、履约与缺货风险分析；
- 活动 ROI 与活动复盘；
- 电商内容—商品—流量—成交归因；
- 平台间商品、订单、客户与指标语义对齐。

这些领域 Skill 应尽量组合第 6 章的通用原子 Skill。例如“经营指标异常诊断”不是重新实现证据、归因和排序，而是：

```text
frame-problem
  → build-evidence-pack
  → identify-data-gaps
  → diagnose-metric-change
  → ecommerce-driver-analysis
  → rank-recommendations
  → draft-action-plan
```

---

## 9. 六数字同事如何组合 Skill

六数字同事应定义为 AgentTemplate + ResponsibilityProfile + SkillBindingSet，而不是在六个文件里各复制一套方法。

### 9.1 数据参谋

组合：

```text
frame-problem
→ build-evidence-pack
→ identify-data-gaps
→ profile-data-semantics
→ form-hypotheses
→ diagnose-metric-change / analyze-root-cause / forecast-with-uncertainty
→ rank-recommendations
→ decision-report（专业 Skill）
→ review-outcomes
```

电商 Profile 再注入 GMV、转化、复购、商品、客户、达人和活动语义。

### 9.2 私域管家

组合：

```text
build-evidence-pack
→ segment-entities
→ consent-and-purpose-check（专业治理 Skill）
→ customer-journey-plan（专业 Skill）
→ follow-up-plan（专业 Skill）
→ draft-action-plan
→ prepare-handoff
```

“客户沉淀”是包含识别、同意、关系绑定、标签和跟进的复合 Logic，不宜继续作为单一大 Skill。

### 9.3 内容官

组合：

```text
frame-content-brief
→ content-strategy
→ copy-or-script-drafting
→ title-optimization
→ channel-content-adaptation
→ verify-claims
→ review-output-quality
→ design-experiment
→ review-outcomes
```

图像、TTS、视频渲染、转码和发布是 Tool/Provider Capability，不叫 Skill；数字人直播是复合 Production Logic。

### 9.4 导购顾问

组合：

```text
needs-discovery
→ build-evidence-pack
→ product-retrieval（领域 Skill + 查询 Tool）
→ compare-alternatives
→ product-explanation（专业 Skill）
→ bundle-recommendation（电商 Skill）
→ objection-handling（专业 Skill）
→ prepare-handoff
```

订单查询、库存查询、商品读取本身是 Tool；“根据需求和证据形成解释与建议”才是 Skill。

### 9.5 活动策划师

组合：

```text
goal-decomposition
→ ecommerce-assortment-planning
→ pricing-and-promotion-design
→ compare-alternatives
→ estimate-impact
→ design-experiment
→ draft-action-plan
→ plan-responsibilities
→ review-outcomes
```

创建优惠券、改价格、上架活动是受控 Action，不属于 Skill。

### 9.6 客服专员

组合：

```text
service-intent-classification
→ policy-and-case-retrieval（专业 Skill + 查询 Tool）
→ case-triage
→ response-drafting
→ verify-claims
→ escalation-decision
→ prepare-handoff
→ satisfaction-analysis
```

查订单和查物流是 Tool；退款、补偿、改地址等是受审批和 Lease 保护的 Action；客服 Skill 只负责理解、判断、拟稿和路由。

---

## 10. 渠道 Skill 如何接入六数字同事

渠道插件不绑定某一个数字同事，而是被多角色按任务组合：

| 渠道 Skill | 数据参谋 | 内容官 | 导购 | 活动策划 | 客服 | 私域管家 |
|---|---:|---:|---:|---:|---:|---:|
| 平台全域只读观察 | ✓ |  |  | ✓ |  |  |
| 菜单/页面快速定位 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 商品与内容状态观察 | ✓ | ✓ | ✓ | ✓ |  |  |
| 订单/售后状态观察 | ✓ |  |  |  | ✓ |  |
| 平台经营指标采集方法 | ✓ |  |  | ✓ |  |  |
| 平台规则与风险定位 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 获授权后的单项操作路径 |  | ✓ |  | ✓ | ✓ | ✓ |

具体店铺账号、登录状态、经营计划和实例策略仍属于 InstanceOverlay / Case / Evidence，不进入通用 Skill 内容。

---

## 11. 哪些内容明确不要做成 Skill

| 内容 | 正确归属 | 原因 |
|---|---|---|
| Provider/ModelRoute/Eval/Binding/AgentRun | AIP 平台内核 | 是运行控制面和状态机 |
| Task/Plan/TaskRun/Handoff/Receipt/Lineage | AIP 平台内核 | 是权威合同和治理链 |
| 查订单、查物流、读数据集 | Tool/Capability | 确定性调用，不是专家方法 |
| TTS、图片生成、视频渲染、FFmpeg | Provider Tool | 底层执行能力 |
| 浏览器点击某菜单 | 渠道 Tool/定位 Recipe | 过细且平台相关 |
| 抖店或微信小店全部经营流程 | 渠道插件 + Logic | 范围过大，无法独立评估 |
| 六数字同事完整工作流 | AgentTemplate + Logic | 是角色编排，不是单一技能 |
| 商品、订单、达人、活动 Schema | 电商 DomainPack | 是领域语义，不是方法 |
| 具体客户账号与经营策略 | InstanceOverlay / Case | 客户实例信息不可泛化 |
| Prompt 文本 | PromptTemplate/Artifact | 是 Skill 的版本化依赖之一，不等于 Skill |

---

## 12. 对现有“约 37 个技能”的重构裁决

历史发布台方案记录过“约 37 个技能”的目标，但不得直接将它们整体迁移为插件目录。应先执行逐项分类：

1. **KEEP_ATOMIC**：已是目标单一、I/O 稳定、可独立 Eval 的原子 Skill；
2. **SPLIT**：一个“大 Skill”拆为多个原子 Skill + Logic；
3. **MERGE**：多个角色中重复的方法合并为一个通用 Skill；
4. **MOVE_TO_TOOL**：查询、生成、写入等动作移到 Tool/Capability；
5. **MOVE_TO_DOMAIN**：电商对象、指标、规则移到 DomainPack；
6. **MOVE_TO_CHANNEL**：微信、抖音、淘宝等平台方法移到对应渠道插件；
7. **MOVE_TO_OVERLAY**：具体客户和店铺配置移到实例层；
8. **DEPRECATE**：被新合同、治理链或更精确 Skill 替代。

历史 `published/evaluated/binding` 只能作为核查入口。重构必须保留 canonical identity、版本和兼容策略，不能在没有迁移设计时删除或换名。

### 12.1 2026-08-24 现场审查与 S2.5 裁决

现场代码确认，现有 SolutionPack 发布器仍按一条角色 Logic 生成一个同名 Skill；这与本方案的 Skill/Logic/Tool/Domain/Channel 分层存在差距。S2.5 已获授权执行最小兼容切片，具体实施以 [165-S2.5 原子 Skill 兼容重构实施 ADR](../12-工作台层技术方案/165-S2.5原子Skill兼容重构实施ADR.md) 为准。

本次授权只包含：37 项逐项分类、旧 ID 兼容校验、Workshop 只读贡献投影和回归门。它不授权批量发布未完成 Eval 的新原子 Skill，不删除旧 Skill，不迁移历史 Binding，也不改变外部 Action 门。

---

## 13. 建议的插件与 Skill 包结构

以下仅为目录规划，不代表本轮创建：

```text
plugins/
├── skills/
│   ├── aos-reasoning-skills/          # 证据、假设、归因、比较、影响、复盘等通用原子 Skill
│   ├── aos-professional-skills/       # 内容、服务、研究等跨行业专业 Skill
│   └── ecommerce-operations-skills/   # 电商领域 Skill 与领域 Profile
└── ops/
    ├── wchat-qyh-ops/                 # Niushop 微商城渠道与已授权实例方法
    ├── wx-store-op/                   # 微信小店渠道方法
    ├── douyin-store-op/               # 抖店渠道方法
    └── cbec-ops/                       # 跨境电商运营方法
```

如果现有插件框架要求统一位于 `plugins/ops`，也应通过命名和 manifest 明确 `common / professional / vertical / channel` 四类，不要继续把所有 Skill 命名为“电商通用”。

每个 Skill 目录建议只包含：

- `SKILL.md`：触发条件、工作流、边界；
- `references/`：稳定的协议、方法库和领域 Profile；
- `scripts/`：需要确定性执行且可重复验证的辅助脚本；
- `assets/`：确有必要的模板或样例。

不要在 Skill 中复制大型产品方案、客户凭证、运行日志或具体店铺全量数据。

---

## 14. SkillRegistry 最小治理合同

未来每个 SkillRevision 至少登记：

- `canonicalSkillId`、`revision`、`contentHash`；
- 中文业务名、职责和触发条件；
- 输入/输出 Schema；
- 依赖的 Capability、Tool、DomainProfile 与渠道 Skill；
- 所需数据分类、出境策略和权限；
- `EvalPackRef`、通过阈值和失败关闭规则；
- 适用 AgentTemplate 与禁止绑定的角色；
- maturity、deprecation 和 replacement 关系；
- 证据、Receipt 与 Lineage 要求。

Skill 的发布不等于 Agent 可运行。运行仍必须满足 Provider、ModelRoute、Policy、Eval、CapabilityBinding、SkillBinding、数据准备度和租户权限等组合门。

---

## 15. 分阶段实施建议

### Wave S0：全量盘点与分类

- 盘点 `11-AIP决策引擎升级方案`、AIP SkillRegistry、LogicPublication 和 `plugins/ops`；
- 为每个现有候选标记第 12 章的分类结果；
- 识别重复 Skill、Tool 冒充 Skill、渠道知识污染和实例配置泄漏；
- 产出迁移矩阵，不改运行态。

### Wave S1：冻结通用原子合同

- 优先冻结 `frame-problem`、`build-evidence-pack`、`identify-data-gaps`、`form-hypotheses`、`compare-alternatives`、`estimate-impact`、`review-outcomes`；
- 为每个 Skill 建输入输出 Schema、EvalPack 和失败关闭用例；
- 明确其只产出建议/草案，不直接产生外部副作用。

### Wave S2：六数字同事去重组合

- 把六同事方案改为 AgentTemplate + SkillBindingSet + Logic；
- 删除文档层重复实现，保留兼容映射；
- 验证同一原子 Skill 能被至少两个角色正确复用。

### Wave S3：电商领域 Skill 包

- 将商品、价格、活动、达人、私域、订单售后等能力归入电商领域包；
- 用 DomainProfile 注入指标、对象、规则和 Eval；
- 组合通用原子 Skill，不复制通用方法。

### Wave S4：渠道插件绑定

- 为微信小店、抖店、Niushop 等渠道 Skill 声明适用任务和只读/写入边界；
- AdapterPack 提供运行协议，渠道 Skill 提供专家观察与定位方法；
- 具体店铺由 InstanceOverlay 和 Case 选择。

### Wave S5：发布、绑定与累计验收

- exact evaluated revision → LogicPublication → publish → SkillBinding；
- 逐角色验证最小可用 SkillBindingSet；
- 验证跨租户拒绝、缺数据阻断、缺 Capability 阻断、低置信度人工复核；
- 不以“核心包足够”代替全量盘点收口。

---

## 16. 验收标准

1. 任一能力都能唯一归属为 Agent、Skill、Logic、Tool、Domain、Channel 或 Overlay；
2. 六数字同事不再复制同名方法；
3. 通用原子 Skill 至少被两个角色或两个行业场景复用；
4. 每个 Skill 有稳定 I/O、EvalPack、证据引用和失败关闭语义；
5. 渠道插件不持有具体客户凭证，实例层不污染通用 Skill；
6. Tool 调用、Action 副作用与 Skill 判断在审计上可区分；
7. Skill published 不被误报为 AgentRun、外部平台调用或运营就绪；
8. 工作台只消费 canonical Task、Artifact、Evidence、Review、Receipt 和 Effect 投影，不建立第二状态机。

---

## 17. 关键结论

当前设计方向是正确的，但还缺一次“技能去领域化、去角色复制、去工具混淆”的治理波次。

最终应形成：

```text
AOS 通用原子 Skill
  + 跨行业专业 Skill
  + 电商领域 Skill / DomainProfile
  + 微信/抖音/Niushop 等渠道 Skill
  + 具体店铺 InstanceOverlay
  → 由六数字同事按 Logic 动态组合
```

这样做以后，六数字同事仍然保持清晰的职业人格和职责，但其能力不再被锁死在六个大文件中；AOS 也能把已经验证过的证据分析、问题诊断、方案比较、影响评估、任务拆解和复盘方法复用到其他行业。

---

## 18. 主要参考

- `docs/palantier/20_tech/20d-AOS四层分治总纲-平台内核与领域资产包.md`
- `docs/palantier/20_tech/电商平台接入/11-AIP决策引擎升级方案/02-私域管家技能编排.md`
- `docs/palantier/20_tech/电商平台接入/11-AIP决策引擎升级方案/04-导购顾问技能编排.md`
- `docs/palantier/20_tech/电商平台接入/11-AIP决策引擎升级方案/05-内容官技能编排.md`
- `docs/palantier/20_tech/电商平台接入/11-AIP决策引擎升级方案/06-客服专员技能编排.md`
- `docs/palantier/20_tech/电商平台接入/11-AIP决策引擎升级方案/07-活动策划师技能编排.md`
- `docs/palantier/20_tech/电商平台接入/11-AIP决策引擎升级方案/08-数据参谋技能编排.md`
- `docs/palantier/20_tech/电商平台接入/11-AIP决策引擎升级方案/10-AIP-Logic电商场景编排总览.md`
- `docs/palantier/20_tech/电商平台接入/AIP通用能力实施方案/64-W-F2F3技能发布台API与UI方案.md`
- `docs/palantier/20_tech/电商平台接入/AIP通用能力实施方案/69-W-F4-技能首批发布对账.md`
- `docs/palantier/20_tech/电商平台接入/AIP通用能力实施方案/80-W-F6-技能全量收尾策略.md`
- `aos-platform/plugins/ops/wchat-qyh-ops/`
- `aos-platform/plugins/ops/wx-store-op/`
- `aos-platform/plugins/ops/douyin-store-op/`
- `aos-platform/plugins/ops/cbec-ops/`
