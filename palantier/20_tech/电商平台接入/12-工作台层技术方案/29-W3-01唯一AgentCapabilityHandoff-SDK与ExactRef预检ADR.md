# W3-01 唯一 Agent/Capability/Handoff SDK 与 Exact Ref 预检 ADR

> 日期：2026-08-14  
> 状态：`PREPARATION_REFRESHED_GREEN / W3-01_NOT_STARTED / DEP-A6R_PARTIAL_HARD_GATE_BLOCKED`  
> 范围：只读审查当前 w2 基线、共享 authority 与已提交 Delivery Receipt；未读取 w1 未提交内容，未修改 AIP/Workshop 代码、数据库或真实租户。

## 1. 结论

现有 `apps/web/src/api/aipAgentControl` 是应继续复用的唯一 Agent/Capability SDK，不应新建第二套 `workshopAgentClient`。它已严格消费 Agent catalog、AgentInstance 和 Capability catalog，并保留 instance/template/capability 的 revision 与 content hash。

但 W3-01 的全部运行前置尚未成立：AOS-000041 已交付 CapabilityBinding/SkillBinding canonical HTTP 与 OpenAPI；AgentRun、HandoffEnvelope 仍只有后端 Service/合同基础，没有所需 canonical HTTP/OpenAPI；三者在 Workshop 当前固定基线中也没有 BIND1-5 strict SDK。Workshop 不能因 Binding API 存在就判断 runnable、发送交接或恢复交接。

因此：

1. `DEP-A6F` 只关闭目录、实例、Capability 定义和组织安装的 HTTP/UI 门；
2. `DEP-A6R` 是组合门：Binding API 已闭合，AgentRun/Handoff API 与 BIND1-5 strict SDK/browser 仍阻断；
3. W3-01 预检完成但不得编码，更不得由 Workshop 包装后端 Service 或自建 BFF authority 绕开缺失 API；
4. AIP API 进入 m1 后，Workshop 只扩展既有 `aipAgentControl` 并增加无状态 L1 readiness adapter。

## 2. 当前已存在的唯一入口

已进入 OpenAPI 的 canonical HTTP：

- `GET /v1/aip/agent-registry`
- `GET /v1/aip/agents`
- `GET /v1/aip/agents/{instance_id}`
- `GET /v1/aip/capability-catalog`
- `POST /v1/aip/agents/install-ecommerce`
- CapabilityBinding/SkillBinding 的 list/get/preview/create/evaluate/activate/suspend/revoke 14 个 path family（AOS-000041 Delivery Receipt；尚待固定集成基线与 BIND1-5 strict SDK）

前端唯一 SDK 根：`apps/web/src/api/aipAgentControl`，当前 operation 为 `listCatalog/listInstances/listCapabilities/installEcommerce`。六实例和十 Capability 的存在只代表 definition/installation，不代表 Binding healthy、Provider 可用或 Agent runnable。

## 3. Canonical runtime-control 差量

当前差量如下：

| Authority | 已有 Service | W3 必需的最小 API 语义 |
|---|---|---|
| CapabilityBinding / SkillBinding | `AipCapabilityBindingService` / SkillBinding service | 后端 API/OpenAPI 已由 BIND1-4 关闭；仍等待 BIND1-5 strict SDK、固定集成 SHA 与真实正负浏览器证据 |
| AgentRun | `AipAgentRunService` | get/list exact TaskRun/instance/skill/logic/model route/policy refs 与运行状态；unknown/revoke/drift 失败关闭 |
| HandoffEnvelope | `AipHandoffService` | issue/get/consume/revoke/expire 传输生命周期；一次性 token、expiry、receiver exact revision、allowlist/marking 与 version CAS。accept/reject/request-more/return 不属于该 Service，另由 W3-06 的领域 Decision authority 承接 |

这些 API 的 owner 是 AIP。Workshop 只允许消费，不得创建第二 Store、第二状态机或本地 HandoffContext。

## 4. 现有 strict parser 仍需收紧

W3-01 实施时应在既有 parser 上先写 Red tests：

- exact ref revision 必须为正整数，拒绝 0、负数、小数和 NaN；字段必须验证预期 assetType；
- response tenant 必须与每个 nested AgentInstance tenant 一致；count 必须与 items 数量一致；instance/capability identity 必须唯一；
- Binding/Run/Handoff 的 status/readiness/health 只接受冻结枚举；revoked、unknown、drifted、unavailable 必须映射显式 blocker；
- exact refs 原样保留，不自动解析/升级 latest；
- 0 localStorage、0 singleton、0 mock fallback、0 Workshop 业务真源写入。

## 5. W3-01 候选最小文件

AIP API 已进入 m1 后，Workshop 候选范围冻结为：

- 扩展 `apps/web/src/api/aipAgentControl/{contracts,parser,index}.ts` 及 parser/client tests；
- 新增 `apps/web/src/api/ecommerceWorkshop/agentReadiness.ts` 与测试，只把 canonical refs/readiness 映射成 Workshop blocker/view model；
- 不在本 Task 修改页面；公共 UI、Handoff command 与 Responsibility Matrix 仍分别属于 W3-06/07/09。

## 6. 开工门与 Watchdog 边界

W3-01 只有在以下条件全部满足后才能登记编码 Receipt：

1. W2 波次硬门按正式清单关闭；
2. AIP runtime-control API/OpenAPI Delivery Receipt 已进入 m1，且 capability/agent/handoff operationId 唯一；
3. authority、01/06、Git、memory gate 与全部 Lease 当前核验 GREEN；
4. AIP/Workshop 精确文件范围无交叠，Red tests 与回滚点冻结。

当前还有可并行预检工作，因此不因 `DEP-A6R` 休眠。若未来它成为唯一阻塞，必须先为对应 AIP Delivery Receipt/Lease 配置只读 Watchdog，并验证“阻塞静默、完成后单次唤醒、重新核验、成功续跑或安全 no-op”，才允许任务休眠。

机器证据：`.evidence/workshop/2026-08-14-w3-01-sdk-exact-ref-preflight.json`。

## 7. AOS-000038 刷新与两轮复审

2026-08-15 依据 authority `AOS-000038 / BIND1_1_CONTRACT_ADDITIVE_MIGRATION_GREEN_WITH_WARNINGS` 重新核验。BIND-1 已完成 additive contracts、`bind1_001` migration 与定向回归，但 authority 同时明确：**没有 Agent runnable，没有 evaluated binding activatable**；下一门是 `BIND1_2_CAPABILITY_READINESS_SERVICE`，BIND-2～BIND-6 仍不完整。该进展只证明持久化/合同向前，不等于 W3-01 依赖 GREEN。

第一轮复审关闭时间漂移：继续复用唯一 `aipAgentControl`，把 catalog published、instance installed、binding persisted、binding evaluated、operational-ready 和 runnable 分开；Workshop 不得从六实例/十 Capability 或 BIND-1 migration 推断运行能力。结论 `PASS_AFTER_REMEDIATION`。

第二轮反查 `w2-workshop` 已提交基线与生成 OpenAPI：CapabilityBinding、AgentRun、Handoff service foundation 存在，但当前 OpenAPI 仍无它们的 runtime-control paths，前端也无 strict operations/readiness adapter。分支可能落后最新 m1 AIP 提交，因此这里只认 shared authority 与固定 commit，不读取 w1 未提交内容，也不把“尚未合入 w2”解释成 AIP 未开发。W3-01 只有在 W2 GREEN、BIND1_2 及所需后续门 GREEN、AIP Delivery Receipt + m1 fixed SHA + OpenAPI/SDK/正负租户证据齐备后才能编码。结论 `PASS_AFTER_REMEDIATION`。

刷新机器证据：`.evidence/workshop/2026-08-15-w3-01-sdk-exact-ref-refresh-preflight.json` 与 `.evidence/workshop/2026-08-15-w3-01-sdk-exact-ref-refresh-doc-ledger.json`。最终状态保持 `NOT_STARTED / HARD_GATE_BLOCKED / NO_EXTERNAL_EFFECT`。

## 8. AOS-000041 / BIND1-4 差量复审

2026-08-15 再按 authority `AOS-000041 / BIND1_4_CANONICAL_API_OPENAPI_GREEN_WITH_WARNINGS` 与 Delivery Receipt `aip-bind1-4-canonical-binding-api-20260815` 重核。BIND1-4 已真实关闭 CapabilityBinding/SkillBinding 的 tenant-scoped list/get/preview/create/evaluate/activate/suspend/revoke API 与 14 个 OpenAPI path family；Principal scope、Idempotency-Key、expected snapshot/CAS、Receipt 与稳定 401/403/404/409 语义进入后端合同。这是 W3-01 的实质进展，旧文“CapabilityBinding 无 HTTP/OpenAPI”不再代表当前 AIP authority。

第一轮差量复审同时确认 BIND1-4 **没有**交付 AgentRun lifecycle read 或 HandoffEnvelope issue/get/consume/revoke/expire API，也没有 TypeScript strict SDK、管理 UI、浏览器证据或真实 Binding。`org-org/dev-project` 与 `dev-org/dev-project` 回读均为 0；目录/API available 不能推导 Agent runnable。整改后 `DEP-A6R` 拆成 Binding API 已闭合、AgentRun/Handoff API 未闭合、BIND1-5 SDK/browser 未闭合三段。

第二轮所有权复审确认 BIND1-5 的文件范围正是现有 `apps/web/src/api/aipAgentControl/`。Workshop 不提前复制 parser/client，不从 w1 commit 直接取未集成代码，也不建立 `workshopBindingClient` 或 BFF authority。只有相关 AIP 交付进入固定 m1/Workshop 基线、W2 门关闭、AgentRun/Handoff 所需 API 与 strict SDK/正负租户证据齐备后，W3-01 才能登记编码 Receipt。

差量证据：`.evidence/workshop/2026-08-15-w3-01-02-bind1-4-dependency-refresh.json`。当前状态保持 `NOT_STARTED / PREPARATION_REFRESHED_GREEN / HARD_GATE_BLOCKED / NO_EXTERNAL_EFFECT`。

## 9. 2026-08-24 · AOS-000210 / S3 串行接续裁决

> 当前裁决：`APPROVED_FOR_W3_01_IMPLEMENTATION / READ_ONLY_SDK_FIRST / NO_EXTERNAL_EFFECT`

### 9.1 过期阻断已解除

现场代码与生成 OpenAPI 已确认：

- AgentRun 已有 canonical `create/get` 及 execution-attempt API；
- Handoff 已有 canonical `issue/get/consume` 与独立 Decision `create/list/get` API；
- CapabilityBinding/SkillBinding API 与 `aipAgentControl.runtimeReadiness()` 严格解析已进入当前 `m1`；
- S2.5 已完成 `SkillContributionView` Task Cockpit 只读试点，并保持旧 Skill identity 不变。

因此旧结论中的“AgentRun/Handoff API 缺失”和“BIND1-5 strict SDK 全缺失”不再成立。W3-01 可以开工，但本子波只补齐唯一公共 SDK 与无状态 readiness 映射，不开放 Handoff/Run 写命令。

### 9.2 163/164 强制链路

W3-01 的公开读模型必须按以下顺序保留 exact authority：

`SkillTemplateRevision → LogicRevision → SkillBinding → AgentInstance/AgentTemplate → AgentRun/Handoff → Workshop 专业贡献/阻断`

- 原子 Skill 与 Logic 必须为两个 exact ref，不得把角色 Logic 再命名成新 Skill；
- 数字同事只通过 AgentInstance/Template 与真实 SkillBinding 表达职责，不从角色名推断绑定；
- Workshop adapter 只映射 canonical readiness 与 blocker，不建立第二 Store、不在浏览器推断 runnable；
- Handoff 只传引用；Decision 与 Envelope 生命周期分离，页面本波不提供命令。

### 9.3 文件级施工清单

1. 扩展 `apps/web/src/api/aipAgentControl/contracts.ts`：保留 Skill content hash/Logic exact ref，并增加 AgentRun、HandoffEnvelope、HandoffDecision 只读 DTO；
2. 扩展 `apps/web/src/api/aipAgentControl/parser.ts`：严格校验 tenant echo、asset type、positive revision、SHA-256、count/headVersion、状态枚举和引用一致性；
3. 扩展 `apps/web/src/api/aipAgentControl/index.ts`：只新增 `getAgentRun/getHandoff/listHandoffDecisions` GET；
4. 新增 `apps/web/src/api/ecommerceWorkshop/agentReadiness.ts`：把 canonical catalog/binding 映射为 `Skill → Logic → 数字同事 → Workshop blocker`，无绑定或 stale/unknown 时失败关闭；
5. 先补 parser/client/adapter Red tests，再做最小实现；不修改页面、不新增 BFF、不执行 Run/Handoff/Action。

### 9.4 退出门

- exact Skill/Logic/Agent/Binding/Run/Handoff ref 不丢失、不自动升级 latest；
- duplicated identity、tenant drift、count drift、unknown/revoked/stale 均显式拒绝或阻断；
- `aipAgentControl` 仍是唯一 SDK，Workshop adapter 无状态；
- 专项、Web 累计、TypeScript/build、OpenAPI deterministic 与 diff check GREEN；
- 因本波无页面改动，浏览器只做现有 Task Cockpit/S2.5 贡献视图无倒退验收。

### 9.5 实施与验收结论

2026-08-24 已按上述边界完成，状态为 `COMPLETED_GREEN / READ_ONLY / NO_EXTERNAL_EFFECT`：

- `aipAgentControl` 新增 AgentRun、HandoffEnvelope、HandoffDecision 的 canonical GET 与严格 parser；路径段、tenant echo、exact revision/hash、类型、数量、唯一性与 Decision 语义均失败关闭；
- catalog Skill 保留 `contentHash + logicRevisionRef`，Workshop 新增无状态 `projectProfessionalBindings()`，按 `Skill → Logic → SkillBinding → AgentInstance` 输出专业绑定与 blocker；
- 没有新增 Run/Handoff/Decision 写命令、Store、BFF、migration、provider 调用或真实业务写入；
- 专项 `3 files / 16 tests`、Workshop API 累计 `11 files / 58 tests`、Web 全量 `220 files / 2058 tests`、TypeScript 与 production build 全部 GREEN；
- 内置浏览器回归 `/workshop` 与 `/workshop/task-cockpit`，页面正常、console error 为 0，原有 `degraded` 与 `VISUAL_FIXTURE_ONLY` 仍如实展示；
- 代码与证据提交：`0337370e96ec603cd0fc1c69c920057ba2bfc8cf`；证据：`.evidence/workshop/2026-08-24-w3-01-readonly-agent-runtime-sdk.json`。
