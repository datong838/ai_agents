# W8-03 日常总控跨域派发、拒绝、Request More 与人工接管预检 ADR

> 日期：2026-08-15
> 决策：`NOT_STARTED / SCENARIO_CONTRACT_APPROVED / HARD_GATE_BLOCKED / NO_OWNER_MUTATION`
> 前置：产品正式封板；W3-14、W6-10、W7-11 当前 release 全 GREEN

## 1. 当前事实

AIP 已有 tenant-scoped、one-time Handoff 基元，本轮 6 项专项测试通过；这只证明可复用的底层 Handoff 仍稳定，不证明八 Module 已形成跨域决定闭环。日常总控的 CockpitReadModel、领域 Handoff compiler、拒绝/request-more/return/人工接管全状态以及浏览器证据均未端到端交付。产品仍待正式审查封板，W3-14、W6-10、W7-11 也未 GREEN。

因此本轮冻结可执行合同和负向边界，不用 Mock Task、静态页面或 generic Handoff 测试冒充场景跑通，不修改真实 owner。

## 2. 唯一 authority 与绑定合同

exact `TaskGraphRevision + TaskRun` 是场景根，`dispatchBindingHash` 至少覆盖：

1. PlanStep/Attempt 与 source/target Module installation；
2. ResponsibilityPlan revision/slot 与 current/requested assignee；
3. Capability revision、AgentInstance 与 readiness；
4. Handoff/SLA/Risk policy revision；
5. EvidenceBundle 或 ContextRequirement refs；
6. actor、policy decision、expectedVersion 与 cutoff。

CockpitReadModel 只读投影同一 canonical Task 集；总控只给派发建议和影响预览。用户确认后调用 canonical Task/Handoff service，由服务端重验 expectedVersion、policy、readiness 和权限。禁止总控直接改 owner，禁止第二套 Task、Handoff 或责任 authority。

## 3. 决定状态与守恒

- 接收决定分别是 `accepted`、`rejected`、`request_more`、`returned`，每次追加不可覆盖的 Receipt；
- `request_more` 只列出缺少的 scoped context/evidence requirement，不复制正文或受保护 payload，不代表拒绝或完成；
- 人工接管另走 `takeover_requested → takeover_approved/rejected`，通过审批、职责隔离、conflict、Lease/fence、readiness 与执行状态门；
- in-flight provider 处于 `unknown` 时只能 reconcile，不得强制覆盖 owner；
- 一个 responsibility slot/attempt 只能有一个 active owner；
- late/duplicate/conflicting decision 由 idempotency、decision fingerprint 和 expectedVersion 拒绝；
- accepted 表示责任决定生效，不表示任务执行完成；
- CockpitReadModel 从 Receipt 重建 owner timeline，分类总数等于 filtered canonical Task set；partial/unknown/stale/blocked 不并入 completed。

## 4. 验收门

负向至少覆盖：Module installation 缺失/禁用/跨租户，capability/instance/policy/evidence/version 漂移，拒绝与重复 request-more，双操作者 accept/reassign/takeover 竞态，active execution Lease/fence/provider-unknown，disabled Agent 被误计产能，取消/return 后延迟 Receipt，刷新重建不一致，跨 Module 泄露 PII/Evidence 正文/media payload，以及 shadow owner/handoff divergence。

正式正向只认 `org-org/dev-project`，`dev-org/dev-project` 只作隔离 canary；两者证据不得互换。没有产品封板、三项累计依赖和正负浏览器 EvidencePack，不得勾选 W8-03。

## 5. 两轮审查

### 第一轮：authority、语义与用户可干预性

- 总控只建议、canonical service 决定，用户能看到建议依据、当前责任和预计影响；
- accept/reject/request-more/return/takeover 语义彼此独立并可追溯；
- request-more 保留缺口且不丢失既有 Receipt；
- 单 active owner、任务数量与责任 timeline 都可重建。

结论：`PASS`。

### 第二轮：竞态、安全与执行资格

- expectedVersion、幂等、decision fingerprint 阻断重复与冲突决定；
- 人工接管不能绕过审批、职责隔离、Lease/fence 或 provider unknown；
- generic Handoff 通过不替代 Workshop bridge 与浏览器 E2E；
- 当前没有 owner、真实租户、浏览器或外部动作写入。

结论：`PASS_WITH_HARD_GATE_BLOCKED`。

## 6. 最终裁决

W8-03 场景合同可以作为未来施工和验收基线；当前不得运行或勾选。预检事实见 `.evidence/workshop/2026-08-15-w8-03-total-control-cross-domain-dispatch-reject-request-more-takeover-preflight.json`。

## 7. 2026-08-26 串行施工方案（AOS-000270）

依据 163/164 分层约束，W8-03 不把“日常总控跨域派发”包装成一个大 Skill，也不让页面直接改写 owner。场景投影必须分开并 exact 绑定：可复用原子 `SkillRevision` refs、跨步骤 `LogicRevision`、数字同事 `AgentTemplate/AgentInstance + SkillBinding` refs，以及 Task Cockpit 只读贡献视图。

文件级最小施工清单：

1. 新增 `services/aos-api/aos_api/ecommerce_workshop_dispatch_scenario_contracts.py` 和 `ecommerce_workshop_dispatch_scenario.py`，定义 exact `TaskGraphRevision + TaskRun` 根、`dispatchBindingHash`、7 段决定链、Skill/Logic/角色绑定分层、单 active owner 与决定数量守恒、5 独立结果轴和全 false Command 合同。
2. 在 `services/aos-api/aos_api/routers/ecommerce_workshop.py` 新增独立 GET-only Task Cockpit scenario 路由；默认 canonical reader 不存在时返回明确 blocked，不伪造 Task/Handoff/owner 事实。
3. 新增后端场景专项测试，并扩充 router/OpenAPI 合同测试；覆盖租户/cutoff/root/binding/分层/数量守恒漂移、provider unknown、重复/竞态决定和伪 operational-ready。
4. 扩充 `apps/web/src/api/ecommerceWorkshop/{contracts,parser,client}.ts` 及 parser 专项测试，严格拒绝 PII、Evidence 正文、media payload、支付或 Provider Secret 字段。
5. 最小扩充 `apps/web/src/components/workshop/TaskCockpitPage.tsx` 及 CSS/组件测试，展示 7 阶段、5 结果轴、原子 Skill/Logic/角色绑定贡献和接收方重新授权状态；本场景不增加任何写按钮。
6. 重生 `packages/contracts/openapi/v1.generated.json` 与 inventory，执行专项、全量 Web、typecheck/build、OpenAPI 确定性、scoped security 和内置浏览器验收；最后写 EvidencePack、Delivery Receipt、CAS 和 Prime 独立长记忆事实。

兼容与安全边界：不修改旧 Task Cockpit v1 已有字段语义；不 apply 共享迁移；不调用 dispatch/Handoff/takeover canonical Command；不写 `org-org/dev-project`；不调用 Provider、Action、发布、记忆晋升或 release。
