# AIP 对八工作台、六数字同事与共享专业 Agent 全量支撑审查报告

> 审查日期：2026-08-13
> 审查状态：`REVIEWED_WITH_BLOCKERS`
> 总体判定：`ARCHITECTURALLY_SUPPORTABLE / NOT_YET_FULLY_COVERED / NOT_YET_OPERATIONALLY_READY`
> 文档性质：对当前 AIP 方案、全量开发清单和实时代码的只读审查；本文件不修改既有方案，不授权编码，也不把目标态对象声明为已实现。
> 工作台产品基线：`APPROVED_DETAILED_PRODUCT_BASELINE_V3`。
> 工作台技术基线：`APPROVED_TECHNICAL_BASELINE_V2`，其中 TaskBrief、自适应生产编排仍为目标态契约。
> 唯一真实业务范围：`org-org / dev-project`；`dev-org / dev-project` 仅作负向隔离 canary。
> 增量复核：2026-08-13，基于 `AOS-000017 / AIP6_AGENT_SKILL_HANDOFF_REVIEW_FREEZE` 进一步核对“标题生成/文案生成”“内容总监/Coordinator”和“素材采集”；修正初版按名称计数造成的过严判断，但不改变总体审查状态。
> A6D 实时复核：`aos-platform/m1@650981c` 已继续实现 CapabilityBinding、AgentRun、Handoff、exact Task/Run/Plan/Instance refs、实例快照、一次性 token 与接收方重授权失败关闭；本报告据此继续缩小 P0-03，但 A6E/A6F、领域目录、ModelRouteRevision authority 和公共生产契约仍未闭合，总体审查状态不变。
> W0A 复核：`18-AIP-W0A十类共享专业Capability目录别名与六角色职责Crosswalk.md` 已冻结 DS-01～DS-06 增量来源、十类 stable ID/Schema/alias、六角色与 37 Logic crosswalk、Coordinator ownership、readiness 和 `HandoffEnvelope` 唯一协议；P0-01/P0-04/P0-05/P0-06 的方案差异归零，可进入 A6E，但总体状态仍受 P0-02/P0-03/P0-07 与运行外部门阻断。
> A6E 实时复核：`aos-platform/m1@8b4022b` 已发布 `solution.ecommerce.growth@1.2.0`，真实 PostgreSQL 精确回读为 6 AgentTemplate / 37 evaluated SkillTemplate / 10 published CapabilityRevision，`title.generate → copy.generate` 唯一别名成立，累计 38 项回归 GREEN；全部 Capability readiness 仍为 `blocked`，未创建组织实例或运行绑定。P0-04 与 P0-06 的代码前置门据此关闭，但总体状态仍受 P0-02、A6F、AIP-7、P0-07 和外部数据门阻断。
> A6F 实时复核：`aos-platform/m1@556e92c + 914cff2` 已完成 Principal tenant Canonical API、唯一严格 SDK/UI 和组织安装；`org-org/dev-project` 精确存在 6 个 AgentInstance，SkillBinding/CapabilityBinding/AgentRun 均为 0，`dev-org/dev-project` 为 0 实例 canary。页面真实展示 6/6/37/10/0 runnable，旧 singleton 能力页已退出正式路由。P0-03 的 API/安装/UI 部分关闭，但 AIP-7 exact route、Provider/Eval、Binding 与 P0-02/P0-07 仍未关闭。

## 0. 使用的 Rules

1. 以当前代码、Git、项目检查点、不可变 Receipt 和真实回读为完成事实；不以文档标题、计划状态、页面卡片或预计数量推断实现完成。
2. 从八个工作台、六数字同事、10 类共享专业 capability 和新版公共生产契约反向验收 AIP，不能只证明 AIP 内部文档彼此有引用。
3. 严格执行四层分治：L0 提供领域无关 authority/runtime；L1 贡献电商角色、Logic、Schema、模板和 Evals；L2 提供平台 capability/回执；L3 只保存实例配置与真实引用。
4. 六数字同事和共享专业能力不得在 Workshop、BFF、前端状态或单例 Engine 中形成第二真源。
5. “已定义”“已进入清单”“代码已实现”“真实数据/Provider/Eval 已就绪”四种状态必须分开。
6. 本审查及增量复核只维护本报告；不修改 AIP 代码、数据库、接口、既有方案、全量清单或静态视觉稿。

## 1. 审查输入与方法

### 1.1 主要输入

- 本目录 `00～15` 与 `全量开发清单/00～17`；
- [20d · AOS 四层分治总纲](../../20d-AOS四层分治总纲-平台内核与领域资产包.md)；
- [229 · smart_lib 早期探索成果吸收](../../229-smart_lib早期探索成果吸收与工作台产品设计借鉴.md)；
- [229 探索机制产品化吸收矩阵](../12-工作台层方案/15-229探索机制产品化吸收与变更追踪矩阵.md)；
- [工作台产品 v3 公共生产契约](../12-工作台层方案/产品方案v2/11-任务书证据包专业职责与质量闭环公共契约.md)；
- [TaskBrief、证据包、评价契约与自适应生产编排技术方案](../12-工作台层技术方案/23-TaskBrief证据包评价契约与自适应生产编排技术方案.md)；
- [产品需求、技术资产与测试追踪矩阵](../12-工作台层技术方案/22-产品需求技术资产与测试追踪矩阵.md)；
- 当前 `aos-platform/m1` 代码、路由和 Git 状态；
- [当前项目状态](../../../AOS项目开发上下文/01-当前项目状态.md)、[当前执行检查点](../../../AOS项目开发上下文/06-当前执行检查点.md)及 AIP-5 E6 评审清单。

### 1.2 审查方法

本轮不是关键词命中审查，而是按以下顺序做反向验收：

```text
八 Module 用户任务
  → TaskBrief / EvidenceBundle / Eval / Responsibility / Stage / Artifact / Impact
  → 六数字同事与共享专业 capability 的职责和运行绑定
  → Task / Handoff / Action / Receipt / Memory / SavedExploration
  → AIP 方案任务
  → 全量开发清单任务 ID
  → 当前代码、Store、API、页面和真实 readiness
```

每项分别记录：架构归属、方案覆盖、清单覆盖、代码状态、外部门和工作台失败关闭行为。

## 2. 执行摘要

### 2.1 一句话结论

**现有 AIP 的架构方向能够演进为八工作台的完整底座，但当前方案和全量清单还不能称为“全面支撑工作台 v3”，当前运行实现更没有达到八工作台可开工的共同前置门。**

原因不是已有 AIP 底座弱，而是工作台产品在 2026-08-13 吸收 229 探索后新增了一组更严格的公共生产契约；AIP 的“全量覆盖”评审基线仍停留在 2026-08-11 的 38 份旧上位方案，没有把这些新增目标反向纳入。

### 2.2 已经可靠的部分

- AIP-1/2 的 Task、PlanRevision、TaskRun、StepRun、Checkpoint、Artifact/Evidence、TAOR 和 ResearchJob 已封板；
- AIP-3 的 ActionProposal、Draft、Approval、ExecutionLease、Receipt、unknown/reconcile 已封板；
- AIP-4 的 EvalSuite/Run/Report、Publication、Lineage、Telemetry、Usage/Capability/Delivery Receipt 已封板；
- AIP-5 E0～E5 的治理记忆、知识 Candidate、Query、七知识管道控制面已封板；
- AIP-5 E6A～E6F 的知识包契约、受控 Candidate adapter、检索投影、KnowledgeSearch、Eval runner 和 readiness 控制面已有代码/控制面 GREEN。

这些能力已经构成八工作台的坚实“运行、安全、证据、行动、记忆”底座，不应重做。

### 2.3 当前阻断全面支撑的部分

1. 工作台 v3 新增的 `TaskBriefRevision`、`EvidenceBundleRevision`、`EvalContractRevision`、`ResponsibilityPlanRevision`、`StageTemplate`、`ReviewIssue/ReturnDecision`、`ImpactPreview` 等尚未进入 AIP 总方案和全量清单的正式覆盖基线。
2. AIP-6 A6A～A6F 已落地通用 DTO、PostgreSQL revision/Instance/Binding/Run/Handoff/Capability authority、Store、CAS、durable Receipt、exact runtime refs、最小披露交接、领域 6/37/10 定义、Canonical API/Principal、组织安装和唯一 SDK/UI。`org-org/dev-project` 已有 6 个 exact AgentInstance，旧 singleton 不再是正式页面真源；但 AIP-7 ModelRouteRevision authority、Provider/Eval 与 Skill/Capability Binding 尚未完成，所以 0 runnable 是权威状态。
3. 10 类共享 capability 已具有唯一稳定目录、别名 crosswalk、Schema/Policy exact refs 和 PostgreSQL 不可变 revision；但 Provider、EvalPack、W0B 数据契约与 AIP-7 Route 未就绪，10/10 readiness 均诚实 `blocked`，不能按目录发布推断可运行。
4. 六数字同事的 exact AgentTemplate 已发布，37 Logic 对应 SkillTemplate 已以 `evaluated` 状态发布，六个组织 exact AgentInstance 已由 A6F 安装；AIP-5 E7 必须直接引用这些实例，不再允许按角色字符串硬编码。
5. AIP-8、AIP-9、AIP-10 尚未整体实现；AIP-5 E6 仍受真实知识、trusted provider、专家 GoldSet 和向量能力外部门约束。

因此本轮结论是：**基础能力较强，目标态可支撑；清单覆盖不完整，运行态仅部分支撑。**

## 3. 六数字同事和共享专业 Agent 到底应由哪一层“产生”

用户提出“六数字人和 10 个共享专业 Agent 也应该在 AIP 层产生”，方向正确，但“产生”必须拆成三个不同动作，否则会破坏四层分治。

| 动作 | 权威层 | 具体含义 |
|---|---|---|
| 定义/贡献 | L1 `solution.ecommerce.growth` | 六角色、37 Logic、10 类共享 capability、领域 Schema、EvalPack、职责模板和工作台 slot |
| 注册/发布/实例化/绑定/运行 | L0 AIP | Agent/Skill Template、组织 Instance、Capability/Skill Binding、Run、Handoff、版本、许可、预算、readiness 和 Receipt |
| 消费/投影/干预 | L1 Workshop | 展示角色和 capability，创建 Task/Handoff，查看 Stage/Artifact/Eval，重分派、接管、审批和 reconcile |

据此冻结三条裁决：

1. **六数字同事不是 AOS Core 内置的六个硬编码对象。** 它们是电商 SolutionPack 贡献的角色模板，由 AIP Registry 审核发布并在组织内实例化。
2. **10 类共享专业能力不是必须常驻的 10 个运行 Agent。** 它们是稳定的 capability 分类/可发现模板；运行时可以由一个或多个 Agent、人、工具或受控 Provider 承担，一个执行者也可承担多个兼容职责。
3. **Workshop 不创建 Agent authority。** 工作台只提交 exact ref、消费 readiness 和投影运行状态；离线、未绑定、被撤销或版本漂移时必须显示 `unknown/disabled/blocked`。

因此，更准确的表述是：

> 六数字同事和共享专业能力的电商定义来自 L1；它们的可信注册、组织实例、能力绑定、任务运行与交接由 AIP 产生；Workshop 负责让用户看见、指挥和干预。

## 4. 当前 AIP 阶段对工作台的支撑状态

| AIP 能力域 | 当前事实 | 工作台可用性 | 审查结论 |
|---|---|---|---|
| AIP-0 契约与真值 | 已封板 | 可作为历史公共基线 | 需用工作台 v3 delta 再开一次增量契约门 |
| AIP-1/2 Task/TAOR | `IMPLEMENTED_GREEN` | Task/Run/Checkpoint/Artifact 基础可复用 | 强支撑，但没有 TaskBrief/StageTemplate 产品契约 |
| AIP-3 Action | `IMPLEMENTED_GREEN` | Draft/Approval/Lease/Receipt/unknown 可复用 | 强支撑，但 ImpactPreview exact binding 缺失 |
| AIP-4 Eval/Lineage/Usage | `IMPLEMENTED_GREEN` | Eval、谱系、成本和外部 Job Receipt 可复用 | 强支撑，但单任务 EvalContract/ReviewIssue 缺失 |
| AIP-5 Memory/Wiki | E0～E5 GREEN；E6 code/control GREEN、外部门 BLOCKED；E7 未做 | Candidate/治理/知识状态可消费 | 部分支撑；不能宣称美妆知识和六同事共享记忆 operational |
| AIP-6 Agent/Skill/Handoff | A6A～A6F GREEN：DTO、全局/租户 authority、Store、CAS、revision/Instance/Binding/Run/Handoff、6/37/10 领域定义、Canonical API/Principal、组织安装、唯一 SDK/UI、exact refs 和 durable Receipt 已实现 | `org-org/dev-project` 可精确回读 6 实例，页面展示 37 evaluated/10 blocked/0 runnable；可排队 Run 和一次性交接，但不得进入 running | W1 身份/API/UI 门已关闭；AIP-7、Provider/Eval 和 Binding 是运行前置 |
| AIP-7 Model/Capacity | 方案态；部分 Usage/成本原语已在 AIP-4 落地 | provider/route 不就绪时必须失败关闭 | 部分基础可复用，端到端未 GREEN |
| AIP-8 Assistant/Analyst/Workbench | 方案态；SavedExploration 有 O1 既有 authority 可复用 | 通用查询壳和真实分析链未整体 GREEN | 经营参谋、总控等保持 gated |
| AIP-9 Content/Media/Harness | 方案态 | 多媒体 target-state/disabled | 多媒体和内容 Module 关键阻断 |
| AIP-10 FDE/通用场景 | 方案态 | 不能用方案验收八工作台 | 必须等公共底座和领域包分别封板 |

特别说明：E6A～E6F 的代码/控制面完成不等于美妆知识可用。当前真实 KnowledgePackage、授权正文、trusted resolver、专家 GoldSet 和 vector/rerank 仍不满足，工作台必须把它们显示为 `DATA_BLOCKED / PROVIDER_BLOCKED / EVAL_BLOCKED / DEGRADED`。

## 5. 八个工作台反向验收

| Module | 对 AIP 的核心依赖 | 当前支撑 | 缺口与未就绪行为 |
|---|---|---|---|
| 日常任务总控 | Task/Run、Agent readiness、Handoff、Approval、Stage/Responsibility 投影 | 部分支撑 | Task/Action 强；AIP-6、ResponsibilityPlan、Stage 产品投影缺失。只能显示真实 Task 和 disabled Agent，不得显示静态“在线” |
| 内容与活动 | TaskBrief、EvidenceBundle、EvalContract、母稿/Variant、Handoff、Action | 部分支撑 | Artifact/Eval/Action 原语有；Brief/Bundle/task binding、Variant family 和 AIP-9 未闭合，只能 Draft/blocked |
| 统一运营 | 事件证据、Case Task、Action、ImpactPreview、Receipt/reconcile | 较强但不完整 | Action 主链强；ImpactPreview exact ref/hash、事件聚合 policy 与领域 profile 尚缺，unknown 必须 reconcile |
| 达人邀约与签约 | 批次 Brief、候选 Evidence、职责、Handoff、合同/触达 Action | 部分支撑 | Task/Action/Evidence 基础有；AIP-6、Brief/Bundle/Impact 与领域模板未闭合，默认只到 Draft |
| 多媒体全过程 | 10 类 capability、ResponsibilityPlan、Stage DAG、Artifact/Eval/Issue、MediaJob/Session | 支撑不足 | AIP-9 未实现；10 capability 目录已发布但 Provider/Eval readiness blocked；职责/Stage/Issue 公共契约缺失，只能 target-state/disabled |
| 经营参谋 | Knowledge/Metric Query、Evidence、Eval、Plan、SavedExploration、MemoryCandidate | 部分支撑 | Task/Eval/Memory 强；AIP-8 未 GREEN、E6 外部门未闭合、TaskBrief/EvidenceBundle 缺失，结论必须标假设与不确定性 |
| 价格治理 | ResearchJob、Evidence、匹配/策略、Impact、Action、Receipt | 部分支撑 | ResearchJob/Action 强；同款领域规则归 L1，Impact binding 与平台 capability 未闭合，只允许观察/建议/Draft |
| 客户关系 | Agent/Skill、purpose/marking、TaskBrief、Memory、Handoff、触达 Action | 部分支撑 | Action/Memory 基础有；AIP-6、AIP-5 E7、Dialogue profile 和 consent 领域规则未闭合，只允许最小读投影与 Draft |

八页没有一页需要另造 AIP 真源；但也没有一页能在 AIP-6 和新版公共生产契约缺失时诚实宣称“完整可运行”。

## 6. 六数字同事审查

### 6.1 已覆盖

- 总方案已把六数字同事放入 `solution.ecommerce.growth`；
- AIP-6 方案定义 Template/Instance/Binding/Run/Handoff 三层模型；
- 清单 `03-10`、`03-13～03-18` 与 AIP-11 已覆盖六角色、37 Logic、Schema、Tool allowlist、risk、EvalPack、Memory/Handoff policy 和场景验收；
- AIP-11 明确六同事不复制 Task、Action、Memory、Wiki、Eval、Model Router 底座。

### 6.2 未覆盖或冲突

1. PostgreSQL Registry/Store、六角色领域模板、Principal Canonical API 与六个组织实例均已存在；正式目录/实例/能力页面已切换到唯一严格 SDK。后续不得恢复 singleton 或由页面按显示名自行实例化。
2. AIP-11.3 仍写 `HandoffContext`，与 AIP-6 已冻结“只使用 `HandoffEnvelope`”冲突。
3. AIP-5 E7 要做“六同事个人记忆/共享投影”；六角色 exact template 与组织 exact instance 已由 A6E/A6F 提供。E7 必须引用 A6F 实例，不得退回角色字符串。
4. `AgentDefinition` 与 `AgentTemplate`、`SkillDefinition` 与 `SkillTemplate` 在 20d 和 AIP 文档中并存，缺唯一 canonical 名/兼容别名 ADR。
5. “职责、输入、输出、可调用 Skill 明确且单一”容易被实现成“一角色一固定 Skill/一固定 Agent”。应改成“角色 identity 与 accountable 边界唯一；任务职责和执行者可按 ResponsibilityPlan 动态组合”。

### 6.3 必须冻结的生产路径

```text
solution.ecommerce.growth manifest
  → 六 RoleTemplate + 37 Logic/SkillTemplate
  → AIP Registry scan/eval/publication
  → org AgentInstance + Skill/CapabilityBinding
  → TaskBrief/ResponsibilityPlan 选择 exact binding
  → AgentRun + HandoffEnvelope + Artifact/Eval/Receipt
  → Workshop readiness/Stage 投影
```

模板发布、组织实例、运行绑定和工作台投影四个状态不能合并成一个“在线”。

## 7. 10 类共享专业 capability 审查

### 7.1 工作台 v3 的唯一产品目录

| # | 共享 capability | 稳定职责 |
|---:|---|---|
| 1 | 素材采集 | 商品事实、合规素材、达人、品牌规范和外部证据收集 |
| 2 | 策略规划 | 受众、渠道、卖点、节奏、禁忌与方案结构 |
| 3 | 文案生成 | 商品、社媒、客服、邀约和活动文案 Variant |
| 4 | 脚本撰写 | 短视频、直播、口播、分镜和字幕脚本 |
| 5 | 语音合成 | TTS、时间戳和受控声音能力 |
| 6 | 视频合成 | 图像、音频、字幕、BGM 和视频后期合成 |
| 7 | 内容审核 | 事实、品牌、版权、合规、平台和技术质量门 |
| 8 | 直播编排 | 知识快照、话术、安全、互动与导播控制 |
| 9 | 平台适配 | 平台规则、规格、内容 Variant 和 capability probe |
| 10 | 数据复盘 | 效果、归因、质量与改进 Candidate |

这 10 项是可发现 capability 分类，不是固定运行编制；影视的导演、编剧、评估、美术、分镜、摄影、剪辑、制片仍以 `ResponsibilitySlot` 保留专业责任，不强制等于八个 Agent。

### 7.2 增量复核：不能按 Agent 显示名判断能力缺失

AIP 清单 08 当前以“内容总监 + 策略、脚本、标题、配音、合成、审核、直播、平台适配、数据复盘”描述团队；工作台 v3 则以 10 类稳定 capability 描述可发现能力。两者处于不同抽象层，必须先做语义 crosswalk，再判断是否缺失：

| 工作台 capability | AIP 现有语义证据 | 增量复核结论 |
|---|---|---|
| 素材采集 | AIP-9 运行链已有 `product/Wiki/evidence read → asset selection`；清单 08 已要求素材 catalog、license、provenance、hash 与撤权影响；C01、D02 和 ResearchJob/KnowledgeSearch 提供内外部研究与证据入口 | **语义与目录身份已覆盖，运行依赖未闭合。** 它是商品/知识/研究/媒体资产能力的受治理组合，不应为凑人数再复制一套数据真源 |
| 策略规划 | 策略 Agent、C02 ContentBrief、活动策划与数据参谋相关 Logic | **语义已覆盖** |
| 文案生成 | 清单 08 的脚本 Agent 明写“文案、脚本、分镜”，标题 Agent负责“标题和钩子变体”；AIP-11 的 C03 明确为跨渠道 `ContentVariant Draft` | **语义已覆盖。** “标题生成”是文案生成的子能力/别名，不是用来替换整类文案能力，也不应重复计数 |
| 脚本撰写 | 脚本 Agent 与 C04 覆盖口播、分镜、字幕、画面和 CTA | **语义已覆盖**；需要与通用文案按输入输出 Schema 划清边界 |
| 语音合成 | 配音 Agent、TTS/音频/时间戳 | **语义已覆盖** |
| 视频合成 | 合成 Agent、MediaJob、字幕/BGM/mp4 | **语义已覆盖** |
| 内容审核 | 审核 Agent、C06、ContentEvalReport/StageGate | **语义已覆盖** |
| 直播编排 | 直播编排 Agent、LivePlan/KnowledgeSnapshot/AvatarSession | **语义已覆盖** |
| 平台适配 | 平台适配 Agent、14 个 Harness Skill、ContentVariant/capability probe | **语义已覆盖** |
| 数据复盘 | 数据复盘 Agent、C08/D06、EffectReview/MemoryCandidate | **语义已覆盖** |

据此修正初版结论：

1. **方案语义覆盖可判为 10/10，不能再把“文案生成”判为功能缺失。**
2. **AIP canonical capability catalog 已冻结并发布为 10/10。** 稳定 ID、profile/alias、input/output Schema、risk、Policy 与 exact revision 已进入 PostgreSQL authority；Eval、required data/tool、组织 binding/readiness 仍由后续门闭合。
3. **运行态仍不是 10/10。** AIP-6 定义 authority GREEN，但组织实例/binding、Provider/Eval/AIP-7 路由与 AIP-9 内容生产尚未整体 GREEN；目录出现能力名称不能替代真实运行和 Receipt。

建议冻结如下兼容关系：

```text
copy.generate                  文案生成（canonical）
├── title.generate             标题/钩子生成（子能力或兼容 alias）
├── product.copy.generate      商品文案 profile
├── outreach.copy.generate     达人邀约 profile
└── service.copy.generate      客服/私域话术 profile

script.compose                 脚本撰写（canonical）
├── short_video.script
├── live.script
└── storyboard.compose
```

稳定 ID 的最终字面值应在 AIP-6 ADR/manifest 中冻结；上图只裁决语义关系，不提前替代正式命名评审。

### 7.3 Coordinator/内容总监的身份裁决

`Coordinator/内容总监` 不是“其他某个共享专业 Agent”，而是**六数字同事之一——内容官——在一次内容生产任务中的统筹责任**。现有方案将 SolutionPack 路径放在 `agents/content_officer/*`，AIP-6 又把内容官列为六个 `AgentTemplate` 之一；这两处证据共同否定了“再新增一个内容总监身份”的必要性。

但 `Coordinator` 也不能被理解成全平台唯一职位。它是**有业务范围的责任 profile**：

| 协调范围 | 默认业务 owner | 协调内容 |
|---|---|---|
| 经营增长与跨同事 Task DAG | 数据参谋 | 诊断、GrowthPlan、任务拆解、派发、监控和复盘 |
| 活动战役 | 活动策划师 | 活动目标、预算、档期、跨同事子任务和止损 |
| 内容/多媒体生产 | 内容官（此处的内容总监/Coordinator） | 生产计划、专业职责、质量门、产物汇总与交付 |
| 技术执行调度 | TAOR/Production runtime | lease、StepRun、checkpoint、暂停恢复和状态推进；不承担业务结果责任 |

所以，如果问题是“清单 08 里的 Coordinator 是不是数据参谋或另一个 Agent”，答案是：**不是。它特指内容生产范围内的内容官责任；数据参谋是更上层经营任务的总调度，两者可通过 Task/Handoff 衔接，但不能合并身份。**

必须同时区分四件事：

| 概念 | 正确身份 | 是否计入十类共享专业 capability |
|---|---|---:|
| 内容官 | 电商 L1 贡献、AIP 注册实例化的数字同事 `AgentTemplate/AgentInstance` | 否 |
| Coordinator/内容总监 | 内容官默认承担的内容生产统筹责任/profile：计划、派发、质量门、产物汇总 | 否；属于内容生产范围内的跨能力责任槽/元职责 |
| 共享专业能力 | 素材、策略、文案、脚本、语音、视频、审核、直播、适配、复盘 | 是，固定为十类目录 |
| TAOR/Production runtime | 编译并执行 Task/Plan/Step/lease/checkpoint 的平台内核 | 否；它没有内容业务身份，也不替内容官承担结果责任 |

运行时允许同一个内容官实例同时被分配多个兼容职责。例如它既承担 `production.coordination`，又在轻量任务承担“策略规划”或“文案生成”；但必须在 `ResponsibilityPlanRevision` 中形成不同职责槽，并分别绑定 exact Skill/Capability/Eval。不能因为“同一个 Agent”就把专业执行隐藏在 Coordinator 名下。

因此，旧 AIP 文档的“Coordinator 不直接执行专业工具”应解释为**角色边界**而不是**身份绝对禁令**：

- Coordinator 责任槽本身只做计划、派发、质量门和汇总，不用该身份绕过专业 binding；
- 同一内容官实例可以另行承接兼容的专业责任槽；
- 独立审核、硬合规门、maker-checker、外部发布批准和 Receipt 对账不得被兼任吞并；
- 职责合并、替换和人工接管由 frozen `ResponsibilityPlanRevision` 留下 revision、原因和 Handoff。

### 7.4 当前 AIP-6 代码证据的边界

当前 A6A～A6E 已冻结 DTO，并新增 PostgreSQL revision/instance/binding/run/handoff/capability authority、Store、expected-version CAS、append-only revoke/deprecate、durable Receipt、exact runtime refs、一次性交接及 6/37/10 领域定义发布；它仍**未注册 Canonical 路由，也未把旧内存 Engine 变成 authority**。当前实现尚未表达：

- 电商 10 capability 在具体组织内的 Provider/Eval/License/Route 可运行绑定；
- 内容官与 Coordinator responsibility profile 的绑定；
- `ResponsibilityPlanRevision` 如何把责任槽解析到 Agent、人、工具或 Provider；
- 素材采集组合所需的数据/知识/研究/许可依赖如何形成统一 readiness。

所以真正的 P0 不是“缺文案生成逻辑”，而是 **AIP-6 在领域包和 Canonical API 前，必须冻结身份、责任和 capability 的正交模型及 crosswalk**。

## 8. 工作台 v3 公共生产契约对账

| v3 产品对象 | 当前可复用 AIP 原语 | 当前判断 | AIP 需要补什么 |
|---|---|---|---|
| `TaskBriefRevision` | Task.goal/selection/policy、PlanRevision、ResourceRef | **缺公共 authority** | revision/CAS/Diff/freeze + typed spec 注册；L1 只贡献 profile |
| `EvidenceBundleRevision` | 单条 Evidence、Artifact、ObjectSnapshot/Receipt refs | **缺不可变 bundle** | manifest、coverage/missing/conflict/uncertainty、exact refs 和 freshness |
| `EvalContractRevision` | EvalSuiteRevision、Run、Report、Publication/Gate | **缺单任务 exact binding** | contract wrapper、severity/threshold、return mapping、运行固定 hash |
| `ResponsibilityPlanRevision` | PlanStep capability/input refs、未来 Agent/Skill binding | **缺职责 authority** | ResponsibilitySlot、assignee、coverage、merge decision、版本和 Handoff |
| `ProductionRun/StageRun` | TaskRun、StepRun、Checkpoint | **运行真源可复用** | 签名 StageTemplate/compiler、applicability/invalidation；StageRun 只做投影 |
| `ArtifactRevision/Variant` | append-only `aip_artifact`、ArtifactRef、Lineage | **部分可复用** | family/supersedes/variant 关系 ADR；不另建媒体产物真源 |
| `ReviewIssue/ReturnDecision` | EvalReport、Evidence、Artifact、Step attempt | **缺结构化闭环** | issue 生命周期、定位、return command、new attempt/new artifact lineage |
| `ImpactPreview` | ActionProposal、Draft diff/evidence、Approval/Lease/Receipt | **缺强绑定** | immutable preview ref/hash 与 Proposal/Approval exact binding、drift invalidation |
| `SavedExploration` | O1 UX 已有 PostgreSQL authority | **可复用但需对接** | AIP-8/Workshop 使用唯一服务，不再建内存或 localStorage authority |
| Candidate/知识晋升 | AIP-5 Candidate→治理→MemoryItem | **已具备底座** | L1 提供领域 Candidate/Eval policy；外部门未过时诚实 blocked |

核心裁决与技术方案 23 一致：这些名称当前不是已存在的独立 AIP authority，不能通过改名或在 Workshop BFF 加表解决。实施前必须形成一份 L0 复用/增量 ADR，逐项决定：

1. 直接复用既有 authority；
2. 作为既有 authority 的 typed projection；
3. 新增 additive contract；
4. 只由 L1 提供 Schema/template；
5. 依赖未就绪时工作台如何失败关闭。

## 9. 229、产品吸收矩阵和技术方案 23 是否只适用于工作台

### 9.1 审查结论

**不只适用于工作台。** 三份文档共同描述的是一套跨 L0/L1/L2/L3 的 AI 生产与决策体系；工作台只是用户可见的消费面。

### 9.2 229 十二项直接机制的真实归属

| 机制 | L0/AIP 责任 | L1/Workshop 责任 |
|---|---|---|
| 任务书编译 | revision/ref/freeze/Diff/运行绑定 | 电商 typed Brief 与编辑/预览 |
| 事实先行 | Evidence/Bundle authority、来源、hash、marking | required facts、缺口规则、Evidence Drawer |
| 同版生产与验收 | Eval authority、exact binding、Run/Report | 领域 EvalPack、Rubric 和返回阶段 |
| 产物版本化 | Artifact/Lineage/Receipt | 母稿、Variant、业务审批状态 |
| 专业分工 | Agent/Skill/Capability Registry、Responsibility authority | 六角色、10 capability、职责模板和用户重分派 |
| 可恢复阶段 | Task/Run/Checkpoint/lease | 领域 Stage DAG、阻塞解释和干预入口 |
| 三层披露 | 权限化 refs、错误、trace、usage | 业务/审核/工程视图编排 |
| 先收集再启动 | prepare/freeze/start 的幂等与副作用隔离 | 批次准备、确认和影响预览 |
| 知识 Candidate | AIP-5 治理链 | 领域 Candidate/Eval/人工审批策略 |
| 版本化创作资产 | 通用 Artifact/ref/hash/许可门 | 品牌、人物、场景、镜头和风格资产 Schema |
| 母稿/Variant | Artifact family/lineage 基座 | 内容与平台 Variant 业务语义 |
| 成本/不可逆确认 | Usage、Impact、Approval、Action、Receipt | 领域 impact calculator 和用户确认界面 |

### 9.3 四项改造机制

- 渐进式客服：属于 L1/VerticalPack 策略；AIP 提供策略版本、Eval、Task/Action 和 Handoff 外壳。
- 连续事件聚合：原始事件 authority 属平台/业务源，AggregationPolicy 属 L1；AIP 只消费可追溯投影，不得把摘要升级为事实。
- 图谱探索：O1/Workshop 的 `SavedExploration` 承担产品形态；AIP 引用它做受控分析上下文。
- 影视/美术资产：领域/VerticalPack 定义资产和 Rubric；AIP 提供 Artifact、Agent/Skill、Eval、Job/Session 和治理运行时。

### 9.4 三份文档的状态不能互相替代

- 229 的 `DESIGN_REFERENCE_ABSORBED_WITH_TRACEABILITY`：表示探索完成裁决；
- 产品矩阵的 `PRODUCT_ABSORPTION_COMPLETE`：只表示机制已进入 Markdown 产品基线；
- 技术方案 23 的 `TARGET_TECHNICAL_CONTRACT`：表示跨层目标态已提出；
- AIP 当前状态：这些 L0 增量契约仍未全部进入方案、清单和实现。

因此“产品吸收完成”不等于“AIP 吸收完成”，更不等于“运行能力完成”。产品吸收矩阵本身边界写得正确，问题在于 AIP 的覆盖矩阵尚未吸收该增量。

## 10. 审查问题清单

### 10.1 P0：全面支撑前必须关闭

| ID | 问题 | 风险 | 关闭条件 |
|---|---|---|---|
| P0-01 | **方案门已关闭**：W0A DS-01～DS-06 已纳入 229、产品 v3、产品吸收矩阵、技术 22/23 和正式开发清单 | 仍需后续代码/运行证据，不能以 plan 替代 GREEN | A6E/W0B/W2 按 delta matrix 逐项实现 |
| P0-02 | 八类公共生产对象缺 L0 authority/typed projection ADR | Workshop/BFF 各造一套 Brief、Evidence、Stage 和 Issue | 每个对象完成 owner/API/store/RLS/迁移/失败语义/回滚裁决 |
| P0-03 | **身份/API/UI 门已关闭**：A6F 已完成 Principal API、组织安装、唯一 SDK/UI 和双租户浏览器验收；Run 启动仍受 AIP-7 exact route、Provider/Eval 与 Binding 阻断 | 六实例已有权威真值，但共享能力还没有 operational binding/readiness | 完成 AIP-7 route authority、Provider/Eval 与按需 binding；版本/撤销、真实空态、API/浏览器继续 GREEN |
| P0-04 | **定义门已关闭**：W0A 冻结且 A6E 发布 10 stable ID/profile/alias/Schema/Policy exact revision | 10/10 readiness 仍 blocked，不能误报运行完成 | A6F 展示目录与绑定分层状态；AIP-7/Provider/Eval 分别解锁 |
| P0-05 | **已关闭**：AIP-11 已统一为 `HandoffEnvelope`；`HandoffContext` 仅保留历史输入 alias | 后续代码若再输出旧名会形成协议漂移 | DTO/OpenAPI/测试继续禁止第二协议 |
| P0-06 | **身份门已关闭**：A6E 已发布六角色 exact AgentTemplate，A6F 已安装六个组织 exact AgentInstance | E7 仍需严格引用实例并验证撤回/最小披露 | 可进入 E7 方案复审与实现，不得退回角色字符串 |
| P0-07 | AIP-9 仍以固定内容 Agent 团队为主，未消费 ResponsibilityPlan/Stage/EvalContract | 自适应生产只能停留在工作台文档 | AIP-9 绑定 common contracts、10 capability 和 LITE/STANDARD/FULL 组合验收 |

### 10.2 P1：实施前应关闭

| ID | 问题 | 处理建议 |
|---|---|---|
| P1-01 | `AgentDefinition/Template`、`SkillDefinition/Template` 术语并存 | 以 ADR 冻结 canonical 名，旧名只保留 alias/crosswalk |
| P1-02 | “内容总监只编排”可能被误读为内容官实例永远不得兼任专业职责 | Coordinator 责任槽不直接执行专业工具；同一内容官实例可另承接经 binding/readiness/policy 允许的专业责任槽；独立审核和外部 Action 不得合并 |
| P1-03 | Artifact family/Variant、ReviewIssue、ImpactPreview 当前主要依赖约定 | 冻结强引用、hash、supersedes、drift invalidation 和负向测试 |
| P1-04 | AIP 总控和 01/06 顶部状态存在阶段性滞后，最新 E6 事实只在后续章节/Git 中 | 每波同步顶层状态与唯一下一门，避免开发者读取旧入口 |
| P1-05 | 产品吸收完成状态容易被误读为技术完成 | AIP 覆盖矩阵增加 `product_absorbed / aip_planned / code_green / operational_ready` 四列 |
| P1-06 | AIP-8 通用工作台与八个领域 Module 的边界容易混淆 | AIP-8 只提供查询/保存探索/通用壳；八 Module 由 SolutionPack slot 注册 |

## 11. 建议整改波次

以下命名是本审查建议的“工作台支撑增量门”，不是新增 AIP 编号，也不构成编码授权。

### W0 · 上游目标与 authority 冻结

- 把 229、产品 v3、产品矩阵、技术 22/23 纳入 AIP 来源索引；
- 完成八公共对象 L0 复用/增量 ADR；
- 冻结六数字同事、37 Logic、10 capability、ResponsibilitySlot 的唯一术语和 ownership，并明确 `标题生成 ⊂ 文案生成`、`Coordinator → 内容官责任 profile`、素材采集是受治理组合能力；
- 修正 Handoff、AIP-5 E7/AIP-6 依赖和 AIP-9 固定 Agent 口径。

退出门进展：P0-01/P0-04/P0-05/P0-06 已由 W0A 关闭方案差异；P0-02 仍待 W0B authority ADR。W0A 不自动授权 W2 编码。

### W1 · AIP-6 Registry 与电商角色/能力目录

- A6A～A6E 已完成领域无关 Agent/Skill/Capability authority、Instance/Binding、Run、Handoff、exact refs、Receipt 和 `solution.ecommerce.growth@1.2.0` 的六角色/37 Logic/10 capability contribution；
- A6F 只完成 Canonical API/Principal、组织安装/实例化、唯一 SDK/UI 和真实 readiness，不复制 Agent 或数据真源；
- 组织安装形成六数字同事实例和按需专业 Agent/Provider binding；
- Registry、readiness、revoke、license、budget、跨租户和真实空态封板。

W1 退出门已通过：六角色 6/6、37 Logic 37/37、capability 10/10 均按 exact revision 回读；A6F API/安装/UI 与真实租户隔离 GREEN。这不代表运行时固定 10 个 Agent，也不代表 10 capability 已 operational。

### W2 · 公共生产契约

- 实现/映射 TaskBrief、EvidenceBundle、EvalContract、ResponsibilityPlan；
- StageTemplate 编译为现有 Plan/Task DAG，StageRun 只投影 StepRun；
- 补 Artifact family、ReviewIssue/ReturnDecision、ImpactPreview exact binding；
- 完成 prepare/freeze/start/approve/execute/reconcile 分离。

退出门：八 Module 不建第二真源；跨租户、revision drift、许可撤回、capability unknown、预算 unknown 均失败关闭。

### W3 · AIP-9 自适应生产与 AIP-5 E7 集成

- AIP-9 按 capability + ResponsibilityPlan 解析执行者，不按固定 Agent 编制；
- LITE/STANDARD/FULL 保留责任完整性和独立审核；
- AIP-5 E7 在 AIP-6 identity 上实现个人记忆与受治理共享投影；
- MediaJob/C2 Session、Usage、Artifact、Eval、Issue、Checkpoint 和人工接管形成同一 lineage。

### W4 · 八 Module 反向验收

逐 Module 验收：真实 Task/Run、Evidence、Agent readiness、Stage/职责、Action/Receipt、Memory/Candidate、空态/错误态/blocked、刷新恢复和跨租户 canary。所有外部平台写能力继续受 L2 capability 与专项授权门约束。

## 12. AIP 对工作台“全面支撑”的完成定义

只有同时满足以下条件，才可把本审查状态改为 `FULLY_SUPPORTS_WORKSHOP_V3`：

1. 新增来源已纳入 AIP 权威索引和全量覆盖矩阵，P0/P1 为 0；
2. 六数字同事由 SolutionPack 贡献、经 AIP Registry 发布并按组织实例化，6/6 可真实回读；
3. 10 类共享 capability 有唯一目录、Schema、risk、Eval、binding/readiness，10/10 可回读；标题等子能力不重复计数，Coordinator 不占共享目录名额；
4. 运行时 Agent 数量可变，ResponsibilityPlan 仍能证明所有必要职责已覆盖；
5. TaskBrief、EvidenceBundle、EvalContract、ResponsibilityPlan、Stage、Artifact、Issue、Impact 有唯一 authority 或批准的 typed projection；
6. AIP-5 E7 与 AIP-6 identity 边界闭合，个人记忆、共享投影、撤回和最小披露通过负向测试；
7. AIP-8/9/10 相关退出门按真实代码、API、Store、浏览器和 EvidencePack 分别 GREEN；
8. 八 Module 只消费 exact refs，不在前端/BFF/localStorage 建第二真源；
9. 未具备的知识、Provider、模型、平台 Adapter 和外部写能力明确 `blocked/degraded/unknown`；
10. `org-org/dev-project` 完成正向验收，`dev-org/dev-project` 只证明隔离，无 Mock、静态在线或页面成功冒充业务完成。

## 13. 最终判定

### 13.1 对“现有 AIP 是否全面支撑工作台方案”的回答

**否，当前尚未全面支撑。**

更准确的分层结论是：

- **架构可支撑**：四层分治、Task/Action/Eval/Memory 等主干方向正确，且已有大量高质量实现；
- **方案部分支撑**：六数字同事、37 Logic、内容生产、通用工作台均有规划，但没有吸收工作台 v3 的全部新增契约；
- **清单增量已识别但未实施完整**：229 与 v3 增量已进入 W0/W0A；canonical catalog、alias/crosswalk 与 Coordinator ownership 已冻结并由 A6E 发布，W0B/W2 公共生产契约仍未完成；
- **运行态未支撑完整工作台**：AIP-6 A6A～A6F GREEN，六实例已安装但 0 runnable；AgentRun 启动仍受 AIP-7 exact route、Provider/Eval 与 Binding 阻断；AIP-8/9/10 未整体 GREEN，AIP-5 E6 外部门和 E7 仍未闭合。

### 13.2 对三份 229 相关文档的回答

- 229 不是 Workshop 专属参考，而是跨层产品/架构模式来源；
- 产品吸收矩阵已经正确完成 Workshop 产品侧吸收，但不能证明 AIP 已吸收；
- 技术方案 23 的 L0 部分必须上提进入 AIP authority/实施方案，L1 typed profile 和 UI 消费部分继续留在工作台技术方案；
- 不建议简单移动或删除技术方案 23，而应建立“AIP L0 契约方案 + Workshop L1 集成方案”的双向追踪关系。

### 13.3 当前安全下一步

W0A、A6E 与 A6F 已 GREEN，数据库精确回读 6/37/10，并在 `org-org/dev-project` 安装六个 exact AgentInstance。当前安全下一步是完成 W0B/W2 公共生产契约，并正交推进 AIP-7 exact ModelRoute/Provider/Eval 门；随后进入 AIP-5 E7、AIP-8/AIP-9。AIP-7 与 Binding 未就绪时必须保持 `blocked`，不得因目录、实例或页面存在而提前硬编码“在线”。
