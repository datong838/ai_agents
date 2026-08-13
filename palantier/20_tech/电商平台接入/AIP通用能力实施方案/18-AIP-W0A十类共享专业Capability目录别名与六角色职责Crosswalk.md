# AIP-W0A 十类共享专业 Capability 目录、别名与六角色职责 Crosswalk

> 状态：`APPROVED_FOR_A6E_INPUT / NOT_W2_CODE_AUTHORITY`
> 日期：2026-08-13
> 上位方案：`17-AIP-W0工作台v3公共生产契约与能力目录增量优化方案.md`
> 触发审查：`16-AIP对八工作台六数字同事与共享专业Agent全量支撑审查报告.md`
> 唯一真实范围：`org-org / dev-project`
> 负向隔离 canary：`dev-org / dev-project`

## 1. 本文解决什么问题

本文完成 W0A 文档门，冻结 A6E 可以消费的：

1. 十类共享专业 Capability 的稳定 ID、父子语义、兼容别名和 Schema 边界；
2. 六数字同事、37 条电商 Logic、专业 Capability 与 Coordinator 职责的正交关系；
3. 229、工作台产品 v3、产品吸收矩阵和技术 22/23 对 AIP 的增量来源覆盖；
4. `HandoffEnvelope` 唯一协议名和 AIP-5 E7/AIP-6/AIP-9 的依赖顺序；
5. A6E manifest、A6F API/UI 和后续 W2 公共生产契约的失败关闭条件。

本文授权 A6E 使用本目录生成领域贡献 manifest；不授权提前实现 W0B 的八类公共生产对象，也不把“目录已冻结”解释为 Provider、模型、平台账号或外部写能力已经可用。

## 2. Rules 与四层归属

1. L0 AIP 持有 Agent/Skill/Capability 的注册、revision、Instance、Binding、Run、Handoff、readiness 和 Receipt authority。
2. L1 `solution.ecommerce.growth` 只贡献六角色、37 Logic、十类 Capability profile、Eval/Policy/Responsibility 模板，不在 Core 硬编码电商角色。
3. L2 AdapterPack 贡献平台 capability probe、凭据引用和外部回执；L3 InstanceOverlay 只保存 `org-org/dev-project` 的实例配置与 exact refs。
4. Capability 是稳定语义分类，不等于固定运行 Agent。Agent、人、工具和 Provider 都只能通过版本化 Binding 承担能力。
5. 未发布、未绑定、撤销、Schema/hash 漂移、许可/预算/Provider/Eval/数据状态为 `unknown` 时一律不可执行；页面不得把它显示为“在线”。
6. 所有外部副作用继续走 `ActionProposal → Draft → Approval → ExecutionLease → Receipt → EffectReview`；本目录不授予外发、发布、开播、调价或退款权限。

## 3. W0A 增量来源清单

旧 `全量开发清单/17` 的 38 份来源基线继续保留历史价值；以下增量是当前工作台 v3 反向约束 AIP 的新增输入：

| Delta ID | 来源 | AIP 必须吸收 | 本文承接 |
|---|---|---|---|
| DS-01 | `../../229-smart_lib早期探索成果吸收与工作台产品设计借鉴.md` | 任务书、事实先行、同版评价、专业分工、可恢复阶段、Candidate、资产/Variant、成本与不可逆确认 | §5、§8、W0B 跟踪 |
| DS-02 | `../12-工作台层方案/产品方案v2/00～11` | 八 Module、公共生产契约、LITE/STANDARD/FULL、ResponsibilityPlan | §6、§8 |
| DS-03 | `../12-工作台层方案/15-229探索机制产品化吸收与变更追踪矩阵.md` | 229 十二项机制和四项改造的产品吸收状态 | §8；明确产品吸收不等于代码完成 |
| DS-04 | `../12-工作台层技术方案/22-产品需求技术资产与测试追踪矩阵.md` | 产品对象到技术资产、测试和门禁的可追踪性 | §8、§10 |
| DS-05 | `../12-工作台层技术方案/23-TaskBrief证据包评价契约与自适应生产编排技术方案.md` | 八类公共对象的 L0/L1 边界与自适应生产依赖 | §7、§8；转交 W0B/W2 |
| DS-06 | `../12-工作台层技术方案/D-waves/WORKSHOP-TECH-FORMAL-REVIEW-工作台层开发详细清单与依赖关系.md` | W0-06 crosswalk、W0/W2 顺序和工作台失败关闭 | §4～§10 |

增量追踪结论：DS-01～DS-06 均已进入明确对象、Module、清单门或后续 W0B 任务；旧“38/38”只能描述 2026-08-11 基线，当前覆盖结论必须同时引用本文。

## 4. 十类 canonical Capability 目录

### 4.1 稳定 ID 与边界

| # | 稳定 ID | 中文显示名 | 输入 Schema v1 | 输出 Schema v1 | 风险基线 | 关键依赖 |
|---:|---|---|---|---|---|---|
| 1 | `material.collect` | 素材采集 | `MaterialCollectRequest` | `MaterialBundleRef` | MEDIUM | Object/Evidence/Knowledge/ResearchJob/Media/License exact refs |
| 2 | `strategy.plan` | 策略规划 | `StrategyPlanningRequest` | `StrategyPlanDraftRef` | MEDIUM | EvidenceBundle、约束、目标、预算/时间窗 |
| 3 | `copy.generate` | 文案生成 | `CopyGenerationRequest` | `ContentVariantRef[]` | MEDIUM | 商品事实、受众、渠道规则、品牌调性、Eval |
| 4 | `script.compose` | 脚本撰写 | `ScriptCompositionRequest` | `ScriptArtifactRef` | MEDIUM | ContentBrief、素材、时长、镜头/互动约束 |
| 5 | `speech.synthesize` | 语音合成 | `SpeechSynthesisRequest` | `AudioArtifactRef` | HIGH | Voice license、Provider/ModelRoute、Usage、时间戳 |
| 6 | `video.compose` | 视频合成 | `VideoCompositionRequest` | `VideoArtifactRef` | HIGH | 素材许可、音频/字幕/BGM、MediaJob、成本 |
| 7 | `content.review` | 内容审核 | `ContentReviewRequest` | `ContentEvalReportRef` | HIGH | 事实、品牌、版权、平台、技术 Rubric；maker-checker |
| 8 | `live.orchestrate` | 直播编排 | `LiveOrchestrationRequest` | `LivePlanRef` | CRITICAL | KnowledgeSnapshot、AvatarSession、人工接管、kill switch |
| 9 | `platform.adapt` | 平台适配 | `PlatformAdaptationRequest` | `PlatformVariantRef` | HIGH | CapabilitySnapshot、Harness revision、平台规则、许可 |
| 10 | `performance.review` | 数据复盘 | `PerformanceReviewRequest` | `EffectReviewRef` | MEDIUM | 指标口径、时间窗、归因/Eval、Receipt、MemoryCandidate |

稳定 ID 一经 A6E 发布不可改写；中文显示名可本地化，但不得作为 API identity。Schema 名在 A6E manifest 中必须绑定 exact `revision/hash`；W0B 公共对象尚未落地时，依赖它们的 Binding 保持 `blocked_dependency`，不得用字典或前端 JSON 冒充 authority。

### 4.2 子能力、profile 与兼容 alias

| Canonical ID | 子能力/profile | 仅迁移 alias | 裁决 |
|---|---|---|---|
| `material.collect` | `product.fact.collect`、`knowledge.collect`、`research.collect`、`media.asset.collect` | 素材采集 Agent、资料收集、Research Agent | 组合并引用既有真源，不新建素材事实库 |
| `strategy.plan` | `content.strategy.plan`、`campaign.strategy.plan`、`growth.strategy.plan` | 策略 Agent、策划 Agent | profile 不生成新 CapabilityTemplate |
| `copy.generate` | `title.generate`、`product.copy.generate`、`outreach.copy.generate`、`service.copy.generate` | 标题 Agent、文案 Agent、话术生成 | `title.generate ⊂ copy.generate`，不重复计数 |
| `script.compose` | `short_video.script`、`live.script`、`storyboard.compose` | 脚本 Agent、编剧 Agent、分镜 Agent | 与通用文案按 Schema 分界 |
| `speech.synthesize` | `tts.synthesize`、`voiceover.synthesize` | 配音 Agent、TTS Agent | voice/license/consent 缺失即 blocked |
| `video.compose` | `short_video.compose`、`subtitle.compose` | 合成 Agent、剪辑 Agent | 摄影/美术是 ResponsibilitySlot，不自动变为新能力 |
| `content.review` | `fact.review`、`brand.review`、`compliance.review`、`technical.review` | 审核 Agent、评估 Agent、质检 Agent | 独立审核和硬门不得被 Coordinator 合并 |
| `live.orchestrate` | `live.plan`、`live.interaction.orchestrate`、`live.direct` | 直播编排 Agent、导播 Agent | 公开直播仍需 L2 能力与专项授权 |
| `platform.adapt` | `douyin.adapt`、`kuaishou.adapt`、`wechat_shop.adapt`、`xiaohongshu.adapt` | 平台适配 Agent、Harness Agent | 平台 profile 不宣称真实写能力 |
| `performance.review` | `content.performance.review`、`campaign.performance.review`、`growth.performance.review` | 数据复盘 Agent、归因 Agent | 结论必须带口径、证据、不确定性与 EffectReview |

兼容 alias 只允许解析旧引用并返回 canonical exact ref；禁止由 alias 再发布第二份 Template。未知 alias 失败关闭，不做模糊猜测。

## 5. 身份、职责、能力与执行者正交

| 概念 | Authority | 是否属于十类目录 | 关键约束 |
|---|---|---:|---|
| 六数字同事 | L1 AgentTemplate contribution → L0 Registry/Instance | 否 | 是业务责任主体，不是十个专业能力的固定容器 |
| `production.coordination` | Responsibility profile/slot | 否 | 默认由内容官承担内容生产统筹，不是第七同事或第十一能力 |
| 经营增长协调 | Responsibility profile/slot | 否 | 默认由数据参谋承担；不替代活动/内容 owner |
| 活动战役协调 | Responsibility profile/slot | 否 | 默认由活动策划师承担 |
| TAOR/Production runtime | L0 Task/Plan/Run/Checkpoint | 否 | 只调度执行，不承担业务结果责任 |
| 十类 Capability | L0 catalog + L1 profile contribution | 是 | 可由 Agent、人、工具或 Provider exact binding 承担 |
| 专业工种 | ResponsibilitySlot | 否 | 导演、编剧、美术、摄影、剪辑、制片等按任务保留职责，不固定为 Agent 数量 |

同一 AgentInstance 可以承担多个兼容槽，但每个槽必须分别保留 capability/skill/eval exact ref。以下职责不可被合并吞掉：独立内容审核、maker-checker、外部发布批准、严重风险动作批准、真实直播人工值守与 Receipt 对账。

## 6. 六角色、37 Logic 与十类 Capability Crosswalk

此表描述“默认消费/协调关系”，不赋予执行权限，也不把 37 Logic 改名为十类 Capability。

| 角色 | 37 Logic 逐项映射 | 默认协调责任 |
|---|---|---|
| 数据参谋 D01～D06 | D01→`material.collect`；D02→`material.collect`；D03→`strategy.plan`；D04→经营增长协调；D05→`performance.review`；D06→`performance.review` | 跨同事经营任务、证据和效果总协调 |
| 内容官 C01～C08 | C01→`material.collect`；C02→`strategy.plan`；C03→`copy.generate`；C04→`script.compose`；C05→`platform.adapt`；C06→`content.review`；C07→`material.collect`+`copy.generate`；C08→`performance.review` | `production.coordination`；按任务编排 speech/video/live 等能力 |
| 导购顾问 G01～G06 | G01→`material.collect`；G02→`material.collect`+`strategy.plan`；G03→`copy.generate` profile；G04→`strategy.plan`；G05→`copy.generate` profile；G06→`strategy.plan`+Handoff | 商品与成交建议责任；不直接发布或承诺 |
| 客服专员 S01～S06 | S01→`material.collect`；S02→`material.collect`；S03→`material.collect`；S04→`strategy.plan`+Draft；S05→`copy.generate` profile+Handoff；S06→`performance.review` | 服务处置与人工升级责任；敏感事实最小披露 |
| 私域管家 P01～P05 | P01→`material.collect`；P02→`strategy.plan`；P03→`strategy.plan`；P04→`copy.generate` profile；P05→`performance.review` | consent/频控/关系维护责任 |
| 活动策划师 A01～A06 | A01→`material.collect`+`performance.review`；A02→`strategy.plan`；A03→`strategy.plan`+`performance.review`；A04→活动战役协调；A05→`performance.review`；A06→`performance.review` | 活动目标、预算、节奏、止损和复盘协调 |

37/37 Logic 已全部可定位。十类中 `speech.synthesize`、`video.compose`、`live.orchestrate` 主要由内容官生产任务按需绑定，不需要为凑齐目录再增加 Logic；它们由 AIP-9/内容官专项实现并受 Provider、成本、许可和人工门控制。

## 7. 八工作台反向消费矩阵

| Module | 主要 Capability | 必须保持的失败关闭 |
|---|---|---|
| 日常任务总控 | `material.collect`、`strategy.plan`、`performance.review` | 只投影 exact refs；缺 Brief/Evidence/Responsibility 时 blocked |
| 内容与活动 | `material.collect`、`strategy.plan`、`copy.generate`、`content.review`、`platform.adapt`、`performance.review` | 未批准只到 Draft；平台能力 unknown 不可发布 |
| 统一运营 | `material.collect`、`strategy.plan`、`content.review`、`performance.review` | 原始业务事件仍由业务源权威；摘要不升级为事实 |
| 达人邀约 | `material.collect`、`strategy.plan`、`copy.generate`、`content.review`、`performance.review` | 邀约默认 Draft-only；PII、频控、许可不足 blocked |
| 多媒体全过程 | 十类全部 | ResponsibilityPlan/Stage/Eval/Provider/License 任一 unknown 即 blocked |
| 经营参谋 | `material.collect`、`strategy.plan`、`performance.review` | 结论标明证据、关键假设和不确定性；不生成伪确定结论 |
| 价格治理 | `material.collect`、`strategy.plan`、`performance.review` | 同款匹配/新鲜度/来源许可不足只补证；禁止恶意动作 |
| 客户关系 | `material.collect`、`strategy.plan`、`copy.generate`、`content.review`、`performance.review` | consent/purpose/frequency/identity 不满足即 blocked |

## 8. W0B 八公共对象依赖交接

W0A 只冻结目录，不创建以下 authority：`TaskBriefRevision`、`EvidenceBundleRevision`、`EvalContractRevision`、`ResponsibilityPlanRevision`、`StageTemplate`、Artifact family/Variant、`ReviewIssue/ReturnDecision`、`ImpactPreview`。

A6E 可以发布六角色、37 Logic、Capability profile 和职责模板，但：

- 依赖上述对象的运行 Binding 必须标记 `blocked_dependency`；
- 不得用 SolutionPack YAML、BFF DTO、前端 local state 或 singleton 代替 L0 authority；
- W0B 需逐对象冻结 owner/API/store/RLS/revision/CAS/idempotency/failure/rollback 后，W2 才可编码；
- AIP-9 必须在 W2 后消费 ResponsibilityPlan/Stage/EvalContract，不能把固定 Agent 团队变成第二真源。

## 9. A6E manifest 必填字段与 readiness

每个角色、Logic、Capability contribution 必须至少包含：

```yaml
id: stable.canonical.id
displayName: 本地化显示名
revision: 1
schemaVersion: 1
parentRef: null
aliases: []
inputSchemaRef: { id: schema.id, revision: 1, hash: sha256:... }
outputSchemaRef: { id: schema.id, revision: 1, hash: sha256:... }
risk: LOW|MEDIUM|HIGH|CRITICAL
requiredDataRefs: []
requiredToolRefs: []
requiredCapabilityRefs: []
evalPackRef: { id: eval.id, revision: 1, hash: sha256:... }
memoryPolicyRef: { id: policy.id, revision: 1, hash: sha256:... }
handoffPolicyRef: { id: policy.id, revision: 1, hash: sha256:... }
effectReviewSchemaRef: { id: schema.id, revision: 1, hash: sha256:... }
licensePolicyRef: { id: policy.id, revision: 1, hash: sha256:... }
readinessPolicyRef: { id: policy.id, revision: 1, hash: sha256:... }
```

统一 readiness 枚举：`available / degraded / disabled / blocked / unknown`。只有 `available` 可启动生产 Run；`degraded` 仅在策略明确允许且 UI 显示降级影响时可运行；其余状态不可启动。目录发布成功不等于实例 Binding `available`。

## 10. 协作协议与实施顺序

1. canonical 协议只使用 `HandoffEnvelope`；`HandoffContext` 仅作为历史文档输入 alias，不建立 DTO、表、路由或输出字段。
2. 顺序固定为：A6D GREEN → W0A 本文通过 → A6E 领域贡献 → A6F Canonical API/UI → W0B 评审 → W2 公共契约 → AIP-5 E7/AIP-8/AIP-9/AIP-10。
3. AIP-5 E7 只引用 A6E 发布的 exact AgentTemplate/AgentInstance；不得按中文角色字符串建立个人记忆真源。
4. AIP-7 尚无 exact ModelRouteRevision authority 时，AgentRun 可以保持 queued/blocked，但不得冒充 running。

## 11. 评审—整改—复审记录

### 11.1 第一轮评审发现

| ID | 发现 | 首轮结论 |
|---|---|---|
| W0A-R1 | 十类只有显示名，无稳定 ID/Schema | BLOCKER |
| W0A-R2 | 标题、文案、邀约/客服话术可能重复注册 | BLOCKER |
| W0A-R3 | 内容总监/Coordinator 容易被算作第七同事或第十一能力 | BLOCKER |
| W0A-R4 | 素材采集可能复制数据/知识/研究/媒体真源 | BLOCKER |
| W0A-R5 | 旧 38 来源未吸收 229 与工作台 v3 delta | BLOCKER |
| W0A-R6 | `HandoffContext` 与 `HandoffEnvelope` 并存 | BLOCKER |
| W0A-R7 | readiness 未覆盖 Schema/Eval/Route/License/Budget unknown | BLOCKER |

### 11.2 整改结果

- §3 建立 DS-01～DS-06 增量来源清单；
- §4 冻结 10 个 stable ID、Schema、风险、父子/profile/alias；
- §5 裁决 Coordinator 与专业工种为 Responsibility，不增加身份或 Capability 计数；
- §6 完成六角色、37/37 Logic crosswalk；
- §7 完成八 Module 反向消费和失败关闭；
- §8 明确 W0B 未实现对象不得被 manifest/BFF/UI 替代；
- §9 将 exact refs 与五态 readiness 设为 A6E 必填门；
- §10 统一 `HandoffEnvelope` 并冻结后续顺序。

### 11.3 第二轮复审

| 退出门 | 结果 |
|---|---|
| P0-01 delta source inventory 可逐来源追踪 | PASS |
| P0-04 十 Capability 稳定 ID/alias/Schema/Coordinator/素材组合无歧义 | PASS |
| P0-05 canonical Handoff 名称唯一 | PASS |
| P0-06 A6E 先于 E7 | PASS |
| 六角色 6/6、37 Logic 37/37、十 Capability 10/10 可定位 | PASS |
| 八 Module 无第二 authority、unknown 失败关闭 | PASS |
| A6E manifest 可直接据此实现 | PASS |

最终结论：`APPROVED_FOR_A6E_INPUT`。W0A 全部审查差异归零；可以进入 A6E，但 W0B/W2 仍是独立方案与编码门。
