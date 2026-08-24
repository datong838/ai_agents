# 164 · 工作台层 Skill 消费与六数字同事产品落位方案

> 状态：`DESIGN_PROPOSAL / S2.5_WSK0_WSK1_TASK_COCKPIT_PILOT_IMPLEMENTED`
>
> 上位产品基线：[工作台产品方案 v2 总纲与权威索引](../12-工作台层方案/产品方案v2/00-产品方案总纲与权威索引.md)、[八工作台公共产品契约](../12-工作台层方案/产品方案v2/01-公共产品契约.md)、[任务书、证据包、专业职责与质量闭环公共契约](../12-工作台层方案/产品方案v2/11-任务书证据包专业职责与质量闭环公共契约.md)
>
> 上位能力方案：[163-AIP 通用原子 Skill 分层与六数字同事组合方案](../AIP通用能力实施方案/163-AIP通用原子Skill分层与六数字同事组合方案.md)
>
> 文档性质：定义八个 Workshop Module 如何消费 AIP Skill、六数字同事和领域/渠道能力；不代表 Skill 已发布、已绑定、Agent 可运行或外部 Action 已授权。

---

## 1. 使用的 Rules

1. 工作台只负责产品入口、交互、可重建投影和受控 Command，不复制 AIP SkillRegistry、Task、AgentRun、审批或 Action 状态机。
2. 六数字同事是 AgentTemplate/职责角色；八工作台是业务问题空间；原子 Skill 是可组合的方法，三者不是一一对应关系。
3. 每个页面必须区分只读事实、专业判断、建议、Draft、Approval、Action、Receipt 和 EffectReview。
4. Skill 是否可用只取服务端 exact readiness，不根据菜单存在、静态目录、历史测试或 UI 在线标识推断。
5. `unknown`、`stale`、`partial`、`blocked` 必须诚实展示；未知不能归零，HTTP 超时不能显示成功。
6. 工作台不直接访问源数据库、平台后台、Connector Secret 或 Provider；发现缺口只提交 DataNeed/DataRequirement。
7. 工作台只展示决策摘要、证据链、归因路径、关键假设和不确定性，不展示模型隐藏推理链。
8. 所有外部副作用仍经过 Suggestion → Draft → Approval → Lease → Attempt → Receipt → Reconcile/Effect。

---

## 2. 本方案解决什么问题

[163](../AIP通用能力实施方案/163-AIP通用原子Skill分层与六数字同事组合方案.md)解决的是能力供给侧：

- 什么是原子 Skill；
- 哪些方法应跨行业复用；
- 哪些能力属于电商 DomainPack、渠道插件或 Tool；
- 六数字同事如何通过 SkillBinding 和 Logic 组合能力。

本方案解决能力消费侧：

1. 用户在八个工作台中从哪里发起专业任务；
2. 页面如何说明“由谁负责、用了哪些 Skill、为什么能做或不能做”；
3. 一个任务跨多个数字同事、Skill 和工作台时如何连续呈现；
4. Skill 的证据、产物、评审、Handoff、Action 和 Effect 如何进入现有产品闭环；
5. 如何避免工作台因为追求交互方便而制造第二套权威状态。

---

## 3. 核心产品判断

### 3.1 不是新增“技能工作台”

Skill 不新增第九个一级工作台。一级导航仍然只有八个 Module：

1. 经营参谋 · 增长指挥中心；
2. 日常任务总控大屏；
3. 内容与活动工作台；
4. 统一运营驾驶舱；
5. 达人邀约与签约驾驶舱；
6. 多媒体任务全过程闭环工作台；
7. 价格治理驾驶舱；
8. 客户关系工作台。

Skill 作为任务内部的专业方法被用户感知，而不是成为需要用户先理解的技术目录。

### 3.2 用户看到的是“专业贡献”，不是底层编排细节

普通运营用户应看到：

- 当前经营问题；
- 当前主责数字同事与协作角色；
- 正在进行的专业步骤；
- 使用了哪些事实和证据；
- 产出了什么；
- 为什么等待、阻断或需要人工；
- 下一步会交给哪个工作台；
- 是否产生外部副作用。

高级审计/诊断视图再渐进披露：

- exact AgentTemplate/SkillRevision/LogicRevision/Binding refs；
- ModelRoute、Policy、Eval、Capability 与 SourceReadiness；
- TaskRun/StageRun/Checkpoint/Artifact/Receipt/Lineage refs；
- reasonCode、freshness、cutoff 和 conflicts。

### 3.3 六数字同事不是六个页面

六数字同事可以同时出现在多个工作台：

- 数据参谋既服务经营参谋，也服务价格、活动、达人和客户分析；
- 内容官既服务内容活动，也服务多媒体、达人和客户触达；
- 客服专员既服务统一运营，也参与客户关系和问题复盘；
- 私域管家既服务客户关系，也参与增长方案中的客户分层和旅程设计；
- 导购顾问既服务客户推荐，也参与达人选品和内容商品解释；
- 活动策划师既服务内容活动，也参与经营方案和价格治理。

工作台围绕业务对象和用户任务组织，数字同事围绕专业责任组织，Skill 围绕可复用方法组织。

---

## 4. 权威分层与数据流

```text
Workshop Module
  ├─ 展示 Module View / Task View / Skill Contribution View
  ├─ 提交 allowed Command
  └─ 展示人工 Review、Handoff、Action 与 Effect
          │
          ▼
L1 Module Application Service / BFF
  ├─ 校验 Principal、Module、对象和 expectedVersion
  ├─ 读取领域 authority 与 AIP projection
  ├─ 生成可重建聚合 View
  └─ 通过 Outbox/Receipt/CAS 调用 canonical 服务
          │
          ▼
AIP Authority
  ├─ Task / PlanRevision / TaskRun / StageRun / Checkpoint
  ├─ AgentTemplate / SkillRevision / SkillBinding / CapabilityBinding
  ├─ EvidenceBundle / EvalContract / ResponsibilityPlan
  ├─ Artifact / ReviewIssue / Handoff
  └─ AgentRun / Usage / Lineage / Receipt / EffectReview
          │
          ▼
Data OS / Ontology / DomainPack / AdapterPack
  ├─ 数据产品、本体对象、领域规则和渠道能力
  └─ SourceReadiness / Hydration / Fulfillment Receipt
```

### 4.1 工作台拥有的内容

- Module 安装、路由、Slot 和业务可见性；
- 领域 Case、GrowthPlan、Campaign、CreatorBatch 等 L1 领域对象；
- 面向当前 Module 的聚合读模型；
- 用户 Command 入口；
- 保存视图、筛选、渐进披露和可访问交互；
- 从 canonical authority 可重建的时间线投影。

### 4.2 工作台不拥有的内容

- SkillTemplate/SkillRevision 生命周期；
- SkillBinding、CapabilityBinding 与 AgentInstance 权威；
- TaskRun/AgentRun 状态推进；
- ModelRoute、Provider、Secret、Policy 和 Eval 权威；
- Approval、Lease、Receipt 和 Effect 的第二份副本；
- 源数据库、平台 Cookie、Token、SSH 或 Connector 配置。

---

## 5. 六数字同事 × 八工作台落位矩阵

符号说明：`主责`表示该 Module 的主要专业角色；`协作`表示在特定 Task/Stage 中承担职责；`交接`表示通常作为上游或下游 Handoff 目标；空白不代表绝对禁止，而是默认不安装该角色的页面入口。

| 工作台 | 数据参谋 | 私域管家 | 内容官 | 导购顾问 | 活动策划师 | 客服专员 |
|---|---|---|---|---|---|---|
| 经营参谋 | 主责 | 协作 | 交接 | 协作 | 协作 | 协作 |
| 日常任务总控 | 协作 | 协作 | 协作 | 协作 | 协作 | 协作 |
| 内容与活动 | 协作 | 协作 | 主责 | 协作 | 主责 | 交接 |
| 统一运营 | 协作 | 协作 | 交接 | 协作 | 协作 | 主责 |
| 达人邀约 | 协作 | 协作 | 协作 | 主责 | 协作 | 交接 |
| 多媒体生产 | 协作 |  | 主责 | 协作 | 协作 |  |
| 价格治理 | 主责 |  | 交接 | 协作 | 协作 | 协作 |
| 客户关系 | 协作 | 主责 | 协作 | 协作 | 交接 | 协作 |

### 5.1 日常任务总控的特殊定位

日常任务总控不是第七个数字同事，也不接管六同事的业务判断。它由经营负责人使用，聚合：

- 六数字同事承担的 Task/Stage；
- readiness、blocker、Checkpoint 和 SLA；
- 待人工审批、待接管和待对账事项；
- Handoff 发送/接收状态；
- 业务产物和 EffectReview 的只读摘要。

总控可以派发、改派、暂停、恢复或请求更多信息，但这些动作必须提交 canonical Command；页面不能直接改写 TaskRun。

---

## 6. 八工作台的 Skill 消费模型

### 6.1 经营参谋 · 增长指挥中心

主要任务：Metric/Observation 观察、Insight 形成、GrowthPlan 候选、TaskGraph 协同和 EffectReview。

典型 Skill 组合：

```text
frame-problem
→ build-evidence-pack
→ identify-data-gaps
→ form-hypotheses
→ diagnose-metric-change / analyze-root-cause
→ compare-alternatives / estimate-impact
→ rank-recommendations
→ draft-action-plan
```

工作台呈现：指标口径与 cutoff、Observation、Insight、证据与反证、决策摘要、GrowthPlan 候选、TaskGraph、EffectReview 和 Handoff 目标。

### 6.2 日常任务总控大屏

主要任务：查看全部 Task/Stage/职责覆盖、阻断、审批、接管和复盘。

它不主动运行专业 Skill，而是消费：

- `ResponsibilityPlan` 中声明的 Skill/角色需求；
- 当前 TaskRun 的 Skill/Agent contribution 投影；
- 阻断原因与恢复建议；
- `prepare-handoff`、`review-output-quality`、`review-outcomes` 的结果摘要。

### 6.3 内容与活动工作台

主要任务：内容策略、Campaign、活动目标、选品、Offer、计划、母稿和多渠道交接。

典型组合：

```text
frame-content-brief
→ content-strategy
→ ecommerce-assortment-planning
→ pricing-and-promotion-design
→ copy-or-script-drafting
→ verify-claims
→ estimate-impact
→ design-experiment
```

创建优惠、投放、发布等仍是独立 Action，不由 Skill 完成。

### 6.4 统一运营驾驶舱

主要任务：订单、库存、履约、售后事件聚合，OperationCase 判断和补救草案。

典型组合：

```text
service-intent-classification
→ build-evidence-pack
→ case-triage
→ analyze-root-cause
→ policy-and-case-retrieval
→ compare-alternatives
→ response-or-remediation-draft
→ prepare-handoff
```

查订单、查库存、查物流是 Tool；退款、补偿、改地址、重发是 Action。

### 6.5 达人邀约与签约驾驶舱

主要任务：达人发现、匹配、批次准备、邀约、条款、签约和履约关系。

典型组合：

```text
frame-recruitment-brief
→ build-evidence-pack
→ segment-entities
→ ecommerce-creator-match
→ compare-alternatives
→ commission-impact-estimate
→ negotiation-draft
→ plan-responsibilities
```

发送邀约、签约、结算和平台触达必须进入渠道 Action 治理。

### 6.6 多媒体任务全过程闭环工作台

主要任务：Brief、素材、母稿、Variant、生产 Stage、四门 Eval、Issue/Return 和交付。

典型组合：

```text
frame-content-brief
→ content-strategy
→ script-or-storyboard
→ asset-selection
→ channel-content-adaptation
→ verify-claims
→ review-output-quality
```

图像、TTS、视频渲染、转码、上传是 Tool/Provider Capability；Skill 负责策略、组织、判断和质量方法。

### 6.7 价格治理驾驶舱

主要任务：价格 Observation、同款 Match、Research、Policy、Impact、Case 和 ActionProposal。

典型组合：

```text
frame-price-research
→ build-evidence-pack
→ identify-data-gaps
→ ecommerce-product-match
→ compare-alternatives
→ pricing-and-promotion-design
→ estimate-impact
→ review-output-quality
```

改价、优惠配置和平台提交均是受控 Action。

### 6.8 客户关系工作台

主要任务：CustomerLite、Consent、Segment、Journey、Dialogue、触达 Draft 和效果复盘。

典型组合：

```text
build-evidence-pack
→ segment-entities
→ consent-and-purpose-check
→ needs-discovery
→ customer-journey-plan
→ response-or-outreach-draft
→ verify-claims
→ review-outcomes
```

发送消息、发券、建群、外呼等是 Action；Skill 不能根据 CustomerLite 自动扩大披露范围。

---

## 7. 工作台公共 View 合同

工作台不直接拼接多个 AIP API。各 Module 的 BFF/Application Service 应把 AIP 与领域 authority 投影为统一、严格解析的公共结构。

### 7.1 `SkillContributionView`

```text
SkillContributionView
├─ contributionId
├─ taskRunRef / stageRunRef / checkpointRef
├─ moduleId / businessObjectRefs
├─ roleRef / assigneeRef
├─ canonicalSkillRef / skillRevisionRef
├─ bindingRef / logicRevisionRef
├─ displayName / purpose / responsibility
├─ readiness
│  ├─ status / reasonCode / freshness
│  ├─ source / semantic / evidence
│  ├─ model / policy / eval / capability
│  └─ lastVerifiedAt / receiptRef
├─ runProjection
│  ├─ status / startedAt / updatedAt
│  ├─ progressLabel / checkpoint
│  └─ waitingFor / blockerRefs
├─ inputRefs / evidenceRefs
├─ outputArtifactRefs / reviewIssueRefs
├─ assumptions / uncertainties / conflicts
├─ nextContributionRefs / handoffRef
└─ allowedCommands
```

这是可重建 View，不是 SkillRun 或 AgentRun 的新权威。

### 7.2 `RoleCollaborationView`

用于展示一个任务内的多角色协作：

- 主责、协作、审核、接收方；
- 每个责任槽的 assignee 与 readiness；
- 角色合并或人工接管；
- 责任是否覆盖；
- 当前 Handoff 与退回路径。

角色卡上的“在线”“工作中”只能来自新鲜运行证据；没有证据时显示“目录已安装/运行未验证”，不能显示绿色在线。

### 7.3 `ModuleSkillSummaryView`

用于 Module 首页聚合：

- 当前任务数、阻断数、待人工数；
- 本 Module 安装的可用 Skill 目录摘要；
- 近期产物与 EffectReview；
- exact readiness cutoff；
- 数据、模型、渠道或审批依赖。

该摘要不能成为 Skill 数量、Binding 数量或运行状态的第二统计真源。

---

## 8. 用户可见的公共组件

### 8.1 `ProfessionalContributionRail`

用一条阶段轨道展示“谁正在用什么方法解决什么问题”：

```text
数据参谋·证据构建
  → 数据参谋·归因分析
  → 活动策划师·影响评估
  → 经营负责人·人工评审
  → 内容官/私域管家·Handoff
```

轨道节点显示业务名，不把 canonical ID 当主标题；展开后可查看 exact refs。

### 8.2 `SkillContributionCard`

卡片至少包含：

- 专业步骤名称；
- 主责数字同事/实际 assignee；
- 输入事实与证据覆盖；
- 当前产物；
- 状态、阻断和等待对象；
- 关键假设、不确定性和冲突；
- “查看证据”“查看产物”“请求补充”“人工接管”等 allowed Command。

不得展示模型内部思维过程、原始 Secret、全量 Provider 请求或跨租户数据。

### 8.3 `ReadinessAndBlockerPanel`

至少分轴展示：

- SourceReadiness；
- SemanticReadiness；
- EvidenceReadiness；
- Skill/BindingReadiness；
- Model/Policy/EvalReadiness；
- HandoffReadiness；
- ActionReadiness。

每个 blocker 显示 owner、reasonCode、恢复条件和证据 cutoff。工作台可以发起 DataNeed、请求人工或跳转治理页，但不能自行把 blocker 改绿。

### 8.4 `ArtifactAndReviewPanel`

统一展示：

- Artifact revision、hash、来源和状态；
- Evidence refs 和适用范围；
- ReviewIssue、严重度和责任人；
- accept / return / request_more；
- Diff、历史 revision 和被替代关系。

### 8.5 `HandoffPanel`

显示目标 Module/Role、purpose、最小披露引用、到期时间、receiver readiness 和决定状态。接收方必须重新授权；发送方不能通过 Handoff 扩大持久权限。

### 8.6 `ActionBoundaryPanel`

当建议需要外部副作用时，单独显示：

```text
Recommendation
→ ActionDraft
→ Proposal
→ Approval
→ Lease
→ Attempt
→ Receipt / Unknown-Reconcile
→ EffectReview
```

Skill 卡的“完成”只代表专业产物完成，不代表 Action 已执行。

---

## 9. 状态模型

### 9.1 能力准备度与任务运行态分离

能力准备度回答“现在能否启动”：

```text
AVAILABLE / DEGRADED / DISABLED / BLOCKED / UNKNOWN / STALE
```

任务运行态回答“本次工作进行到哪里”：

```text
NOT_STARTED
→ PREPARING
→ READY
→ RUNNING
→ WAITING_DATA / WAITING_HUMAN / PAUSED / BLOCKED
→ REVIEW
→ COMPLETED / RETURNED / CANCELLED / FAILED
```

横向对账态：`UNKNOWN / RECONCILING`。

页面不能用“Skill 已发布”替代 `AVAILABLE`，也不能用“Task completed”替代 Action/Effect 成功。

### 9.2 页面七态仍然保留

八 Module 既有 `loading / ready / empty / degraded / blocked / forbidden / failed` 产品七态继续有效。Skill 状态是页面数据的一部分，不另建一套全局 UI 状态机。

### 9.3 刷新与恢复

- 页面刷新必须从服务端 View 重建；
- localStorage 只保存非权威外观偏好；
- Command 成功后 GET 回读相同 revision/Receipt；
- HTTP 超时显示 `UNKNOWN/正在对账`；
- 幂等结果未确认前禁止重复发起状态变更。

---

## 10. 工作台 Command 边界

服务端返回 `allowedCommands`，按钮可见性不等于授权。

### 10.1 通用任务命令

| Command | 用途 | 关键门 |
|---|---|---|
| `PREPARE_TASK` | 编译 Brief、Evidence、Eval、职责计划 | scope、exact refs、readiness |
| `START_TASK` | 启动合法 TaskRun | frozen contracts、Binding、Health |
| `PAUSE_TASK` | 人工暂停 | expectedVersion、合法状态 |
| `RESUME_TASK` | 从 Checkpoint 恢复 | blocker resolved、fresh readiness |
| `REQUEST_MORE_EVIDENCE` | 请求补证或 DataNeed | purpose、marking、owner |
| `REQUEST_HUMAN_TAKEOVER` | 人工接管职责槽 | lease/assignee policy |
| `REVIEW_ARTIFACT` | accept/return/request_more | exact artifact/Eval |
| `PREPARE_HANDOFF` | 形成最小交接草案 | approved artifact、receiver scope |
| `DECIDE_HANDOFF` | 接收、拒绝或补充 | receiver reauthorization |
| `CLOSE_TASK` | 终止或封存 | terminal state、summary |

### 10.2 领域命令

各 Module 可增加领域 Command，例如创建 Campaign、OperationCase、CreatorBatch、GrowthPlanCandidate 或 PriceCase。但领域 Command 只能通过 Module Application Service 调用 canonical authority，不得从前端直接串联多个后端并拼出成功。

### 10.3 外部 Action 不混入通用命令

发布、改价、上下架、触达、退款、发券、签约、结算、数据写回等不属于本章通用任务 Command，必须进入独立 Action 治理链。

---

## 11. Skill 选择与组合规则

### 11.1 默认由服务端编译，不让页面随意拼 Skill

工作台提交业务目标、对象、范围和约束；AIP 根据：

- AgentTemplate/责任槽；
- DomainProfile；
- Module 安装贡献；
- Task 档位 `LITE/STANDARD/FULL`；
- Skill/Capability/Model/Source readiness；
- Eval 和成本预算；

编译 `ResponsibilityPlanRevision + StageTemplateRevision + exact Skill refs`。页面只预览、确认或请求调整。

### 11.2 高级用户可以“请求方法”，不能绕过编译门

高级界面可以提供：

- 建议增加反证分析；
- 建议增加影响评估；
- 请求渠道对照；
- 请求人工专业复核。

这些操作提交“method preference”，由服务端重新编译 PlanRevision；前端不能直接创建 SkillBinding 或 AgentRun。

### 11.3 自动降级必须可见

例如模型不可用时可降级为确定性统计和人工分析，但必须显示：

- 哪个 Skill 未运行；
- 替代方法是什么；
- 输出能力损失；
- 哪些结论不能生成；
- 是否需要人工批准降级。

---

## 12. 跨 Module Handoff 设计

### 12.1 经营参谋是方案入口，不是所有执行的 owner

经营参谋形成经过证据和影响评估的 `Insight/DecisionSummary/GrowthPlanCandidate` 后，再按职责交接：

| 方案内容 | 目标工作台 | 典型接收角色 |
|---|---|---|
| 内容生产与活动 | 内容与活动 | 内容官、活动策划师 |
| 短视频/直播/媒体 | 多媒体 | 内容官 |
| 达人招募与签约 | 达人邀约 | 导购顾问 |
| 客户分层与旅程 | 客户关系 | 私域管家 |
| 订单履约与售后补救 | 统一运营 | 客服专员 |
| 价格研究与调价建议 | 价格治理 | 数据参谋、活动策划师 |
| 跨模块执行协调 | 日常任务总控 | 经营负责人 |

### 12.2 交接只传引用

Handoff 不复制业务 payload，只传：

- source TaskRun/StageRun；
- approved Artifact/Evidence refs；
- target Module/Role；
- purpose、requested outcome 和 dueAt；
- marking、minimum disclosure；
- readiness snapshot；
- acceptance/return/request_more 条件。

### 12.3 退回不是失败

接收方发现证据不足、范围不清、预算不明或 Capability 不可用时，可 `request_more/return`。页面应显示退回目标和缺口，不把它合成红色系统失败。

---

## 13. Evidence、Lineage 与 Memory 在页面中的落位

### 13.1 Evidence

每个专业结论可展开：来源、hash、cutoff、freshness、confidence、applicability、marking、conflict 和 revoked 状态。工作台只读取 Evidence authority，不上传无治理的“页面截图即事实”。

### 13.2 Lineage

页面展示从业务问题到结果的可审计关系：

```text
TaskBrief
→ EvidenceBundle
→ SkillContribution
→ ArtifactRevision
→ ReviewDecision
→ Handoff / ActionProposal
→ Receipt
→ EffectReview
```

只有服务端返回的 exact lineage ID 才是 Lineage；trace ID 不能冒充业务谱系。

### 13.3 Memory

工作台只能提交 `MemoryCandidate`，不能把一次成功自动写成正式经验。Candidate 必须经过提炼、冲突检查、Eval、许可、审批和 revision 晋升。

---

## 14. 安全、隐私与租户边界

1. 所有 View 与 Command 强制 `orgId + projectId + Principal`；
2. 经营实体、渠道、Module、Task 和 Evidence refs 必须属于同一 scope；
3. CustomerLite 只提供当前 purpose 所需最小字段；
4. Skill 不获得比调用 Task 更大的数据权限；
5. Handoff 接收方重新授权，不继承发送方长期权限；
6. 页面不接收或显示 Secret、Cookie、Token、SSH、数据库地址和 Provider payload；
7. SourceReadiness、Health、Binding 超过 TTL 后阻断依赖步骤；
8. `dev-org/dev-project` 只能作负向隔离证据，不能作为真实经营实体正向数据。

---

## 15. API 与前端边界建议

以下为未来实现范围建议，不表示当前创建文件。

### 15.1 公共严格 SDK

```text
apps/web/src/api/workshopSkills/
├─ contracts.ts
├─ parser.ts
├─ client.ts
└─ index.ts
```

职责：解析公共 `SkillContributionView`、`RoleCollaborationView`、readiness 和 allowed Command；不得提供 generic request 或原始 AIP 任意调用器。

### 15.2 公共 UI 组件

```text
apps/web/src/components/workshop/skills/
├─ ProfessionalContributionRail.tsx
├─ SkillContributionCard.tsx
├─ RoleCollaborationPanel.tsx
├─ ReadinessAndBlockerPanel.tsx
├─ ArtifactAndReviewPanel.tsx
├─ HandoffPanel.tsx
└─ ActionBoundaryPanel.tsx
```

组件只接收 ViewModel 和 command callback，不自行拼租户、计算 readiness 或直接调用 AIP。

### 15.3 API/BFF

公共 View 可由 Workshop BFF 提供，但不得把聚合表变成第二权威：

```text
services/aos-api/aos_api/routers/ecommerce_workshop_*.py
services/aos-api/aos_api/ecommerce_workshop_*_views.py
services/aos-api/aos_api/ecommerce_workshop_*_commands.py
```

具体文件应在编码波根据现有目录和 owner 复核后冻结，禁止为本方案预先创建第二套 `skill_store`、`task_store` 或 `agent_run_store`。

---

## 16. Feature Flag、安装与降级

- Module 是否显示由 Bundle/Installation 决定；
- Skill 是否可选由 Module contribution + SkillBinding readiness 决定；
- Command 是否可用由服务端 allowedCommands 决定；
- 关闭 Feature Flag 只关闭入口或命令，不删除 Task、Artifact、Receipt 和历史；
- 未安装渠道插件时可显示通用分析，但必须明确缺少渠道观察/Action 能力；
- 缺模型时可降级为确定性/人工流程，不能伪造 Agent 在线；
- 历史任务继续可读，使用当时 exact revisions，不自动迁移为当前 Skill。

---

## 17. 可观测性与度量

### 17.1 产品度量

- Task 准备成功率与准备耗时；
- Skill blocker 分布；
- 人工接管率、退回率和补证率；
- Handoff 接受/拒绝/超时；
- Artifact 一次通过率与返工次数；
- 建议到 Draft、Approval、Action、Effect 的转化；
- Skill 复用率和跨角色重复定义减少量；
- EffectReview 完成率和 MemoryCandidate 晋升率。

### 17.2 技术观测

- View 构建延迟和 authority lag；
- allowed Command 决策延迟；
- idempotency/reconcile backlog；
- Source/Skill/Model/Action readiness freshness；
- exact revision mismatch；
- cross-tenant reject；
- Handoff receiver reauthorization failure。

业务数量未知时不得上报为 0；Telemetry Span 为空表示缺证据，不表示调用次数为零。

---

## 18. 分阶段实施建议

> 2026-08-24 授权边界：S2.5 只执行 WSK-0 和 WSK-1 的 Task Cockpit 只读试点；WSK-2～WSK-6 仍按后续 S3～S7 波次消费，不因本次状态更新提前授权 Action 或全模块改造。文件级范围、兼容与回归门见 [165-S2.5 原子 Skill 兼容重构实施 ADR](165-S2.5原子Skill兼容重构实施ADR.md)。

### WSK-0：合同与归属冻结

- 冻结 `SkillContributionView`、`RoleCollaborationView` 和 allowed Command；
- 逐字段标注唯一权威和 projection 来源；
- 对账 163 原子 Skill 与现有约 37 个历史 Skill；
- 退出门：无第二 Task/Skill/Agent/Action authority。

### WSK-1：公共只读投影

- 建立公共严格 SDK 和只读组件；
- 首先在日常任务总控显示角色/Skill contribution、readiness 和 blocker；
- 只读运行，不提供 Start、Handoff 或 Action Command；
- 退出门：刷新可重建、跨租户拒绝、unknown 诚实显示。

### WSK-2：经营参谋通用分析消费试点

- 把 Metric、Observation、Insight、DecisionSummary、GrowthPlan 和 EffectReview 映射到原子 Skill 贡献；
- 展示指标口径、Evidence、假设与反证、归因结果、方案比较和 Handoff；
- 使用受控演示数据验证交互，不把演示状态报告为真实经营运行；
- 退出门：未批准的 GrowthPlanCandidate 不能进入执行工作台。

### WSK-3：六角色跨工作台组合

- 内容活动、多媒体、达人、客户、价格、统一运营接入公共组件；
- 验证同一 Skill 被多个角色/Module 复用；
- 验证角色合并、人工替代和职责覆盖；
- 退出门：无页面内复制 Logic 或本地角色状态。

### WSK-4：Handoff 与评审闭环

- 接入 Artifact Review、request_more/return 和 receiver reauthorization；
- 日常总控聚合待接管、待审批和待对账；
- 退出门：Handoff 只传 refs，跨 scope 失败关闭。

### WSK-5：Action 与 Effect 边界

- 仅展示 canonical ActionProposal/Approval/Lease/Receipt；
- 接入 EffectReview 和 MemoryCandidate；
- 退出门：Skill 完成不等于 Action 成功，unknown 进入 reconcile。

### WSK-6：累计浏览器与发布门

- 八 Module、三视口、键盘和屏幕阅读器验收；
- loading/empty/degraded/blocked/forbidden/failed/unknown/历史只读覆盖；
- 当前 Authority、固定 Git、OpenAPI、迁移、RLS、Bundle、Eval 和 Security diff 累计门；
- 未获得新鲜运行证据时，只能报告代码/控制面状态，不能报告 operational ready。

---

## 19. 验收矩阵

### 19.1 架构验收

1. SkillRegistry、SkillBinding、TaskRun、AgentRun、Action 和 Receipt 都只有一个权威；
2. 八 Module 只通过严格 View/Command 消费公共能力；
3. 六数字同事、八工作台、专业职责和原子 Skill 四者可独立演进；
4. DomainPack、渠道插件和 InstanceOverlay 不污染 AIP/Workshop 内核。

### 19.2 产品验收

1. 用户能看懂谁负责、正在做什么、用了什么证据、为什么阻断；
2. 同一任务的跨角色协作与 Handoff 连续可见；
3. 不要求普通用户理解 canonical ID，但审计视图可回链 exact refs；
4. 人工可暂停、接管、退回、补证和批准；
5. Skill、Task、Action、Effect 的“完成”不会被混为一个绿色状态。

### 19.3 安全验收

1. 缺 org/project/Principal 失败关闭；
2. 跨租户 View、Command、Handoff 和 Evidence 拒绝；
3. 前端无法提交 SQL、Cookie、Token、Secret 或数据库地址；
4. stale/unknown readiness 禁止启动依赖步骤；
5. 无 Approval/Lease 不发生外部副作用；
6. 页面不展示隐藏推理链或超出 purpose 的个人信息。

### 19.4 恢复验收

1. 刷新后从服务端重建；
2. HTTP 超时不重复创建 Task/Run/Action；
3. 重复事件和迟到 Receipt 可 reconcile；
4. Feature Flag 回滚不丢历史；
5. Skill 或角色不可用时能人工接管或显式降级。

---

## 20. 明确非主张

- 不主张六数字同事当前 runnable；
- 不主张 163 中候选原子 Skill 已创建、发布或绑定；
- 不主张八工作台已经消费本方案的公共 View；
- 不主张 Provider call、AgentRun、渠道 Connector 或外部 Action 已获授权；
- 不主张静态视觉稿、菜单、历史测试或目录数量是运行证据；
- 不主张工作台可以直接探索源数据库或平台后台；
- 不主张 Skill published 等于业务效果已经发生。

---

## 21. 与 163 的闭环关系

```text
163 能力供给侧
  AOS 通用原子 Skill
  + 跨行业专业 Skill
  + 电商领域 Skill
  + 渠道 Skill
          │
          │ SkillRevision / Binding / Logic / Readiness
          ▼
164 产品消费侧
  六数字同事承担专业责任
  + 八工作台提供业务入口
  + Task/Evidence/Review/Handoff/Action/Effect 提供人机治理
```

163 回答“平台有哪些可复用方法、怎么组合”；164 回答“用户在现有产品中如何安全地使用、观察、干预和复盘这些方法”。两者共同构成 Skill 从发布到业务价值的完整闭环。

---

## 22. 主要参考

- `docs/palantier/20_tech/电商平台接入/AIP通用能力实施方案/163-AIP通用原子Skill分层与六数字同事组合方案.md`
- `docs/palantier/20_tech/电商平台接入/12-工作台层方案/产品方案v2/00-产品方案总纲与权威索引.md`
- `docs/palantier/20_tech/电商平台接入/12-工作台层方案/产品方案v2/01-公共产品契约.md`
- `docs/palantier/20_tech/电商平台接入/12-工作台层方案/产品方案v2/11-任务书证据包专业职责与质量闭环公共契约.md`
- `docs/palantier/20_tech/电商平台接入/12-工作台层技术方案/00-总纲与技术方案索引.md`
- `docs/palantier/20_tech/电商平台接入/12-工作台层技术方案/03-TaskHandoff与Action闭环.md`
- `docs/palantier/20_tech/电商平台接入/12-工作台层技术方案/07-领域读模型Command与错误契约.md`
- `docs/palantier/20_tech/电商平台接入/12-工作台层技术方案/23-TaskBrief证据包评价契约与自适应生产编排技术方案.md`
