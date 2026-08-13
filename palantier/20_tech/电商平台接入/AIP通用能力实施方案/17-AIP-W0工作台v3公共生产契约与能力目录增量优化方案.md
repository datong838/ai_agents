# AIP-W0 工作台 v3 公共生产契约与能力目录增量优化方案

> 状态：`REVIEWED / APPROVED_FOR_PLAN_INTEGRATION / NOT_CODE_AUTHORITY`
> 日期：2026-08-13
> 触发来源：`16-AIP对八工作台六数字同事与共享专业Agent全量支撑审查报告.md`
> 唯一真实范围：`org-org/dev-project`
> 负向隔离 canary：`dev-org/dev-project`

## 1. 目标与非目标

本方案把工作台 v3 和 229 增量提出的公共生产契约纳入 AIP 总序列，防止 Workshop、BFF、前端或领域包另建 TaskBrief、EvidenceBundle、ResponsibilityPlan、Stage、ReviewIssue、ImpactPreview 真源。

本方案不重做已经 GREEN 的 Task/Action/Eval/Memory/Artifact/Lineage/Agent Store，不改变四层分治，也不授权立即创建全部新表。它先冻结 owner、复用方式、增量边界、失败语义和实施插入点。

## 2. 实时代码基线

- AIP-1/2：Task/Plan/Run/Step/Checkpoint/Artifact/Evidence 可复用。
- AIP-3：ActionProposal/Draft/Approval/Lease/Receipt/unknown/reconcile 可复用。
- AIP-4：Eval/Publication/Lineage/Telemetry/Usage/Capability Receipt 可复用。
- AIP-5：治理记忆、七知识管道、KnowledgeSearch/readiness 已有底座；E6 外部门、E7 未闭合。
- AIP-6 A6A～A6C：`aip6_002`、Agent/Skill revision、Instance/SkillBinding、Store/CAS/durable Receipt GREEN；A6D～A6F 未完成。
- 工作台 v3 八公共对象没有 canonical L0 authority；代码检索无 `TaskBriefRevision`、`EvidenceBundleRevision`、`EvalContractRevision`、`ResponsibilityPlanRevision`、`StageTemplate`、`ReviewIssue/ReturnDecision`、`ImpactPreview` 实现。

## 3. 八公共对象 owner 裁决

| 对象 | L0 canonical owner | 复用/增量裁决 | L1 只允许贡献 |
|---|---|---|---|
| TaskBriefRevision | AIP Task/Plan | 新增 immutable typed brief revision；exact 绑定 Task/Plan，不复制 Task | 电商 brief profile/schema/defaults |
| EvidenceBundleRevision | AIP Evidence/Artifact | 新增 immutable manifest，聚合 exact refs、coverage/missing/conflict/uncertainty/freshness | required fact/evidence policy |
| EvalContractRevision | AIP Eval | 新增单任务 wrapper，exact 绑定 EvalSuite revision/hash、threshold、return mapping | rubric/profile |
| ResponsibilityPlanRevision | AIP Agent/Plan | 新增 immutable slot/assignee/coverage/merge-decision authority；assignee 只存 exact ref | 六角色与 10 capability slot template |
| StageTemplate | AIP Plan compiler | 签名模板编译为既有 PlanStep/StepRun；不新增第二 StageRun 真源 | 电商 Stage DAG/profile |
| Artifact family/Variant | AIP Artifact/Lineage | 通过 additive family/supersedes/variant relation 扩展既有产物真源 | 母稿/平台 Variant 语义 |
| ReviewIssue/ReturnDecision | AIP Eval/Run | 新增结构化 issue/event 与 return command；新 attempt/new artifact 进入既有 lineage | 领域 issue taxonomy/return policy |
| ImpactPreview | AIP Action | 新增 immutable preview exact ref/hash；Proposal/Approval 强绑定，drift 即失效 | 领域 impact calculator/profile |

共同规则：所有 revision/event/receipt 追加不可变；mutable aggregate 使用 expected-version CAS；全表 RLS/FORCE RLS；无 scope、跨租户、revision/hash drift、许可撤回、readiness unknown 均失败关闭。

## 4. 身份、职责、能力正交模型

1. `AgentTemplate/AgentInstance` 表示责任主体身份，不等于固定岗位编制。
2. `ResponsibilitySlot` 表示一次任务的 accountable 职责；可分配 Agent、人、工具或 Provider exact ref。
3. 共享专业能力目录固定十类 canonical 语义：素材采集、策略规划、文案生成、脚本撰写、语音合成、视频合成、内容审核、直播编排、平台适配、数据复盘。
4. `标题生成` 是 `文案生成` 子能力/alias；不重复计数。`Coordinator/内容总监` 是内容官在内容生产范围的 `production.coordination` responsibility profile，不占第十一类 capability。
5. 素材采集是数据/知识/ResearchJob/媒体资产/许可 authority 的受治理组合，不复制数据真源。

正式稳定 ID、父子关系、input/output schema、risk、Eval、required data/tool、readiness 在 A6E manifest/crosswalk 中冻结；未冻结前不得用显示名作为 API identity。

## 5. Handoff、Memory 与运行依赖

- canonical 交接对象只有 `HandoffEnvelope`；`HandoffContext` 只允许作为文档迁移 alias，不建立 DTO、表或路由。
- A6D Handoff/Run/Capability 基础 authority 可先继续，因为不依赖工作台 v3 新对象。
- A6E 在发布六角色/37 Logic/10 capability 前必须完成本方案的 catalog/crosswalk 评审。
- AIP-5 E7 必须引用 A6E exact AgentTemplate/AgentInstance；个人记忆 subject 不使用角色字符串。
- AIP-9 必须消费 ResponsibilityPlan、StageTemplate compiler 与 EvalContract，不使用固定 Agent 团队作为 authority。

## 6. 实施波次与插入点

### W0A · 来源与术语冻结

- 将 229、工作台产品 v3、产品吸收矩阵、技术 22/23 加入 AIP 来源索引/覆盖矩阵。
- 冻结 AgentTemplate、SkillTemplate、Capability、ResponsibilitySlot、HandoffEnvelope canonical 术语与 alias。
- 形成十 capability ID/crosswalk 草案和六角色 ownership 表。

退出门：P0-01/P0-04/P0-05/P0-06 的方案差异为 0。

### W0B · 公共 authority ADR 与契约清单

- 为八对象逐项冻结 store/API/RLS/revision/CAS/idempotency/失败语义/回滚。
- 明确哪些只扩展既有表、哪些新增 immutable revision/event 表、哪些只做 typed projection。
- 输出 OpenAPI DTO、迁移和负向测试矩阵，但仍不编码。

退出门：不存在 Workshop/BFF/前端第二真源；方案评审通过。

### W0C · 与现有 AIP 序列合并

- A6D 可与 W0A/W0B 文档门串行衔接。
- A6E/A6F 先消费 capability/ownership 裁决。
- W2 公共生产契约编码插入 A6F 后、AIP-5 E7/AIP-8/AIP-9 前。
- E7、AIP-8、AIP-9、AIP-10 和八 Module 验收使用同一 exact refs，不并行造表。

## 7. 验收矩阵

- 来源覆盖：新增来源逐对象、逐 Module、逐清单任务可追踪。
- authority：八对象每项只有一个 L0 owner；L1 只有 profile/schema/template。
- identity：六角色 6/6、37 Logic 37/37、10 capability 10/10 exact revision 可回读；运行 Agent 数量允许变化。
- safety：跨租户、无 scope、stale CAS、hash drift、revoke、license、budget/provider unknown 全部失败关闭。
- integration：TaskBrief→EvidenceBundle→ResponsibilityPlan→Stage/Artifact→Eval/Issue→Impact/Action→Receipt/Memory 同一 lineage。
- UI：工作台仅展示 API truth；loading/empty/forbidden/stale/failed/unknown/blocked 可区分。

## 8. 复审记录

第一轮发现：原 A6C 清单没有工作台 v3 八公共对象，若直接进入 AIP-9 会形成上层第二真源；需要独立 W0 增量门。

整改后复审：owner、复用/增量裁决、身份/职责/能力正交关系、Handoff/E7/A6E/AIP-9 依赖、插入顺序和失败语义已闭合；方案可作为总计划增量输入。它不替代具体 W0B 编码清单，也不授权在清单评审前实现八对象。

最终结论：`APPROVED_FOR_PLAN_INTEGRATION`。当前允许继续 A6D 基础 authority；A6E 前完成 W0A catalog/crosswalk，AIP-9 前完成 W0B/W2 公共生产契约。
