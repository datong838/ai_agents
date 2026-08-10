# 228-AIP 智能体、Skill Registry 与 Handoff 实施方案

> 状态：**评审通过 · v1.0 方案基线（仍不授权编码）**
> 对应阶段：AIP-6。

## 1. 核心决策

智能体不是静态卡片，也不是复制六套代码。采用三层模型：

1. `AgentTemplate/SkillTemplate`：平台或 SolutionPack 发布的不可变定义。
2. `AgentInstance/SkillBinding`：组织级定制，可覆盖名称、Prompt revision、允许能力、预算和治理策略。
3. `AgentRun/Handoff`：工作区级运行状态、Selection、Task、证据和最小披露上下文。

该结构满足“平台模板与组织实例分离、千人千面”，且删除某组织实例不影响其他组织。

## 2. 现状与处置

- `aip_agents_engine.py` 的 singleton 只作为迁移源，不作为新真源。
- `/v1/aip/agents`、`/v1/aip/agent-registry` 当前租户回读为空；前端 `MOCK_AGENTS` 必须移除真实模式 fallback。
- `AgentsPage`、`AgentRegistryPage`、导入向导必须显示真实空态、错误态、安装中和回执态。
- Capability C0/C1/C2 分类保留；C1/C2 必须是 Job/Session Adapter，不塞入 Function 沙箱。

## 3. Canonical 契约

| 对象 | 关键约束 |
|---|---|
| AgentTemplate | immutable version/hash/source/license/capability requirements |
| AgentInstance | org scoped；template_version；prompt_revision；policy_revision |
| SkillTemplate | input/output schema；Logic revision；EvalPack；risk |
| SkillBinding | instance + skill + capability versions + budget |
| CapabilityBinding | secretRef only；health；quota；network policy |
| HandoffEnvelope | task/run refs；allowed fields；marking；expiry；sender/receiver |
| AgentRun | exact instance/skill/logic/model route revisions |

Handoff 禁止复制整段对话或客户对象；只传 ObjectReference、Artifact/Evidence refs 和经过字段白名单的最小上下文。

## 4. 六数字同事首批模板

| 同事 | 首批只读 Skill | 首批受控产物 |
|---|---|---|
| 数据参谋 | 数据健康、异常、趋势、归因草稿 | Insight/Report/GrowthPlanDraft |
| 内容官 | 策略、脚本、标题、内容自检 | ContentDraft/MediaJobProposal |
| 导购顾问 | 需求诊断、商品检索、对比 | RecommendationDraft |
| 客服专员 | 意图、订单/物流只读、回复草稿 | ServiceReplyDraft |
| 私域管家 | canonical Customer 受限投影分层、跟进建议 | FollowupPlanDraft |
| 活动策划师 | 目标拆解、选品、促销解释 | ActivityPlanDraft |

任何发布、触达、退款、改价、库存动作均不属于本波自动能力。

历史文档中的 `CustomerLite` 只能解析为 canonical Customer 的字段白名单读投影；AgentTemplate、Skill 或 SolutionPack 不得以该名称创建第二对象类型、第二主键或独立持久化表。

## 5. 导入与安装

```text
Manifest upload/reference
 -> parse + license/SBOM
 -> schema/network/secret policy
 -> capability probe
 -> EvalPack
 -> Draft approval
 -> install receipt
 -> organization instance creation
```

扫描结果必须来自服务端 Job；页面不得预先显示“仓库可达/测试通过”。AGPL 资产仅可放参考区，不进入交付包。

Template 生命周期为 `draft -> evaluated -> published -> deprecated -> revoked`；Instance 生命周期为 `provisioning -> active -> suspended -> deleted`。Template 发布后不可原地改写；Instance 覆盖项必须通过 schema allowlist，不能降低模板风险、扩大网络或字段权限。

## 6. 持久化与失败语义

- Template、version/hash、license 和来源属于平台/包级真源；Instance、Binding、预算和 Overlay 按组织隔离；Run、Handoff 按工作区隔离。
- Registry 列表只读 canonical store；API 失败显示错误，空集合显示空态，禁止降级为静态 Agent。
- ImportJob 的 scan/probe/eval 每一步写服务端事件和 Artifact/Evidence；取消、超时、部分成功均有明确终态。
- HandoffEnvelope 使用一次性或有期限授权；接收方按当前权限重新解析 ObjectReference，不能继承发送方权限。
- 卸载先阻止新 Run，再处理活动 Run、Binding 和 secretRef；保留不可变历史引用与安装/卸载 Receipt。

## 7. 文件边界

```text
services/aos-api/alembic/versions/*_aip_agent_registry.py
services/aos-api/aos_api/aip_agent_registry_store.py
services/aos-api/aos_api/aip_agent_instance_service.py
services/aos-api/aos_api/aip_skill_registry.py
services/aos-api/aos_api/aip_handoff_service.py
services/aos-api/aos_api/routers/aip_agents.py
services/aos-api/aos_api/routers/aip_agent_imports.py
apps/web/src/api/aipAgents/*
apps/web/src/pages/s2/AgentRegistryPage.tsx
apps/web/src/pages/s2/AgentsPage.tsx
apps/web/src/pages/s2/AgentImportPage.tsx
apps/web/src/pages/s2/CapabilityImportPage.tsx
apps/web/src/pages/StudioPage.tsx
```

上述 `*_store.py`、service、router 和前端 API 目录为新增候选；现有 `aip_agents_engine.py`、`AgentRegistryPage.tsx`、`AgentsPage.tsx`、`AgentImportPage.tsx`、`StudioPage.tsx` 为迁移修改。AIP-0 必须逐项核实文件所有权后再冻结开发清单。

## 8. 验收

- API 空时页面为空，不出现 11/5 个静态 Agent。
- 一个模板可在两个组织形成不同实例；修改/删除互不影响。
- Agent run 可追溯到 template/instance/skill/logic/model/policy 精确版本。
- Handoff 超范围字段、过期 token、跨租户对象引用均拒绝。
- C1/C2 有 submit/status/artifact 或 open/push/close 的真实回执。
- Template revoke 后不能启动新 Run；历史 Run 仍能解析精确版本和来源。
- 导入失败、许可证拒绝、secret 不可用和卸载中状态在 API/UI 中一致，不出现假成功。
