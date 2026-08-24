# W3-05 AIP 生产启动组合门消费与权限接缝 ADR

> 日期：2026-08-14；2026-08-24 实施刷新
> 当前 authority：`AOS-000216`
> 上游事实：W3-04 `49bd762`、Delivery Receipt `workshop-w3-04-production-context-freeze-20260824`
> 状态：`COMPLETED_CODE_CONTROL_GREEN / NO_RELEASE / MIGRATION_NOT_APPLIED / NO_EXTERNAL_EFFECT`
> 边界：只修改 m1 的通用生产合同与严格消费面；不执行迁移、生产启动、审批、发布或真实租户业务写入

## 1. 结论

AIP W2-D2 已实现通用生产启动组合门后端，W2-D3 也已在 `m1@2eab0f7` 完成 strict SDK/UI，状态为 `GREEN_WITH_WARNINGS`。Workshop 不再设计或实现第二套 start service、依赖快照算法或 TaskRun 创建逻辑，而应通过唯一严格 SDK 消费 `/v1/aip/production-contracts/production-runs/start` 与 `ProductionStartDecision`。

截至 `AOS-000216`，W3-01～04 顺序门已经关闭，W3-04 已提供 canonical ProductionContext freeze；W3-05 后端 exact chain、角色门以及 strict SDK/UI 已按分段编排关闭代码缺口。真实 `org-org/dev-project` 正向启动仍保持失败关闭，不把无真实 Preview/Approval/Health 的空态冒充运行完成。

## 2. ProductionContext 如何进入 compile 与 AIP Start

工作台准备/冻结阶段向用户展示四个核心 exact refs，并由 W3-04 `ProductionContextRevision` 一次组合冻结。实现时不把四个 refs 平铺提交给 Start API，也不让 ImpactPreview 反向冒充 pre-compile 确认：

1. `compile` 消费 frozen ProductionContext 与 signed StageTemplate exact refs，生成 canonical draft Plan，并将 ProductionContext ref 写入 Plan production contract；
2. `ImpactPreviewRevision` 固化 ProductionContext、Plan、StageTemplate，以及可选 Route/Policy/Capability/Binding/Account refs；
3. Proposal/Approval 是独立用户可见步骤，不能由 compile 或 start 自动完成；
4. start 提交 Task version、Plan exact ref、frozen ImpactPreview exact ref、approved ActionProposal exact ref、LogicGraph revision 和 Idempotency-Key；
5. AIP 在同一事务内重新计算 ProductionContext 与全部下游 dependencies，拒绝 hash/version/readiness/expiry/approval/permission 漂移；
6. 通过后批准受保护 Plan 并创建唯一 canonical TaskRun。

这保留了“四个核心合同冻结”的产品语义，同时符合当前“先 compile 出 Plan、后 start 消费 Plan”的真实 API 顺序。详细组合 freeze 见 `93-W3-04四合同ProductionContext组合冻结与依赖解环ADR.md`。

## 3. 状态与交互裁决

| AIP Decision | Workshop 展示 | 禁止行为 |
|---|---|---|
| `blocked` | 阻塞原因、关联 ref、补齐入口 | 不创建本地 Run，不显示已启动 |
| `stale` | 漂移/过期项、重新 prepare/freeze | 不静默换版后重试 |
| `unknown` | 未知维度、下一次检查 | 不把 unknown 当 0 或 ready |
| `started` + queued TaskRun | “已受理，等待执行”与 TaskRun ref | 不显示 running，不伪造 AgentRun |

同一个 Idempotency-Key 只允许相同请求重放；用户修改任一 exact ref 或 Task version 时必须生成新的命令意图，不沿用旧 key。

## 4. 权限接缝

ActionProposal 的 maker-checker、批准人数、过期和 execution policy 是启动条件，但不能自动推出“任何已认证用户都可调用 start”。服务端必须明确回答：

- 哪类角色/permission 可以发起生产启动；
- start actor 是否必须不同于 maker/checker，还是只需具备独立 start permission；
- 不同风险级别是否使用同一 start permission；
- 角色变化、权限撤销与批准之间发生竞态时如何失败关闭；
- list/get Decision 的可见范围是否需要最小披露。

Workshop 前端只根据服务端 permission/readiness 显示或禁用按钮，不自行维护授权规则。权限门未封板前，即使 AIP W2-D3 UI 可点击，也不能作为 W3-05 GREEN 证据。

## 5. W3-05 精确实施范围

允许：

1. 复用 AIP W2-D3 唯一 strict SDK，不复制 DTO/parser；
2. 在 Workshop 公共生产面板分别展示 compile、preview、proposal/approval、start，不把多步压成黑盒；
3. compile 与 start 都只调用 canonical service，并原样携带/回读 ProductionContext exact ref；
4. 显示 Decision、blockers、TaskRun ref、queued/running 的真实区分；
5. 支持刷新后按 Decision/TaskRun 回读，不以本地 state 作为真源；
6. 添加八 Module 共用的 intent/idempotency 管理、权限失败、漂移和重复点击测试。

禁止：

- 新建 Workshop start BFF/Store/TaskRun；
- 前端直接把 Plan 标 approved、自动批准 Proposal 或创建 Run；
- 把 compile 隐藏在 start 点击中，或在 crash 后无 Receipt 地重复 compile；
- 绕过 ImpactPreview/ActionProposal；
- 把 `started` 等同 `running`；
- 用 synthetic ready fixture 冒充真实租户 operational readiness。

### 5.1 2026-08-24 文件级实施清单

本次 Task `workshop-w3-05-staged-production-start-20260824` 只做后端 exact-chain 与权限接缝，后续严格 SDK/页面消费另起无冲突串行 Task：

1. `services/aos-api/aos_api/aip_production_contracts.py`
   - compile 请求强制携带 `ProductionContextRevision` exact ref；
   - compile 结果、ImpactPreview 与 StartDecision 回读该 ref；
   - 历史 ImpactPreview/Decision 允许只读返回 `null`，新建与启动路径不允许缺失。
2. `services/aos-api/aos_api/aip_production_contract_store.py`
   - compile 在创建 Plan 前校验 context 的 tenant、task、revision/hash、frozen/ready、profile 与 ResponsibilityPlan；
   - Plan `productionContract` 固化 context exact ref；
   - 新建/修订/冻结 Preview 时把 context 放入依赖快照，并校验 Plan 与 context 一致。
3. `services/aos-api/aos_api/aip_production_start_service.py`
   - Start 同时核验 request、Plan、Preview、ProductionContext 四方 exact ref；
   - StartDecision 固化 context ref，避免回读时丢失启动依据。
4. `services/aos-api/aos_api/routers/aip_production_contracts.py`
   - start 显式要求生产启动角色；角色比较统一小写，未授权返回 403，不进入 service。
5. `services/aos-api/alembic/versions/w3_015_production_start_context.py`
   - 只新增 nullable JSONB provenance 列与对象约束，不回写历史、不执行 live migration。
6. `services/aos-api/tests/**`、`packages/contracts/openapi/**`
   - 覆盖 exact ref 漂移、Plan/Preview/context 不一致、历史只读兼容、角色拒绝、幂等与 OpenAPI 确定性。

### 5.2 不倒退与失败关闭原则

- 不改 TaskRun 创建事务，不新增第二套 Store/BFF；
- 旧记录继续可读，但不得被拿来启动；
- 新 compile/preview 缺 context 立即失败，不自动选择“最新” context；
- `developer` 单角色不具备生产启动权限；本地 dev principal 仍因同时具备 `admin` 可执行受控测试；
- 迁移仅提交代码，未实际应用前状态保持 `NO_RELEASE / MIGRATION_NOT_APPLIED`。

### 5.3 后端切片验收（2026-08-24）

- 专项：28 passed；覆盖 compile、Preview、Start、权限门与 `w3_015`；
- 累计：129 passed，另有 1 项既有 W2-B 测试依赖空库全局计数而随同会话数据变化，不属于本次实现失败；后续累计采用隔离断言集合，不修改该历史测试语义；
- OpenAPI：2570 paths、2123 schemas、4338 operations，确定性检查通过；
- Alembic：唯一 head `w3_015`；迁移未 live apply；
- 浏览器 `/aip/production-contracts`：API 不可达显式展示，启用的启动/编译/冻结/批准/执行按钮为 0，1280px 无横向溢出；
- 副作用：Provider、TaskRun、AgentRun、Action、Approval、ExecutionLease、真实业务写入与 live migration 均为 0。

该切片只关闭后端 exact-chain 与角色门；严格 SDK、页面 compile context 选择、Preview/Decision context 展示仍为同一 W3-05 的下一串行切片，未完成前不得宣称 W3-05 整体 GREEN。

### 5.4 严格 SDK / 页面串行切片（AOS-000216）

Task `workshop-w3-05-strict-sdk-ui-context-20260824` 的最小文件范围与裁决：

1. `apps/web/src/api/aipProductionContracts/contracts.ts`
   - compile input/result 增加必需 `productionContextRef`；
   - Preview/Decision 使用 nullable ref 兼容历史回读；新命令输入仍由页面强制选择 exact ref。
2. `apps/web/src/api/aipProductionContracts/parser.ts`
   - 对 compile result 强校验 `ProductionContextRevision`；
   - 对 Preview/Decision 允许历史 `null`，非空时强校验资源类型；
   - ProductionContext 补回已存在的 `productionProfileRef` provenance，避免 W3-04 服务端字段在前端丢失。
3. `apps/web/src/pages/s2/ProductionContractsPage.tsx`
   - compile 必须选择与 Task、profile、ResponsibilityPlan 一致且 frozen/ready 的 ProductionContext；
   - Preview/Start 只允许使用 Preview 已固定的同一个 context exact ref，历史无 ref 的 Preview 明确禁用；
   - Decision 展示 context provenance，但不把 `started` 误写为 Agent 已运行。
4. 对应 parser/client/page tests 覆盖类型漂移、历史 nullable、compile 传参、Preview mismatch 与零隐式启动。

该页面不创建 ProductionContext、不自动选择“最新”记录、不自动生成 Idempotency-Key 重试旧意图，也不改变审批与 start 的分步交互。

## 6. 退出门

- `DEP-AIP-W2D2`：`CODE_CONTROL_GREEN`；
- `DEP-AIP-W2D3`：`GREEN_WITH_WARNINGS`；strict SDK/UI 已提交，真实正向 Start 未验；
- `DEP-PRODUCTION-CONTEXT-PROPAGATION`：`CODE_CONTROL_GREEN`；
- `DEP-AIP-START-AUTHZ`：`CODE_CONTROL_GREEN`；
- `DEP-AIP-REAL-PREVIEW`：`BLOCKED`；
- W2、W3-01～04：`COMPLETED_CODE_CONTROL_GREEN`；
- W3-05：`COMPLETED_CODE_CONTROL_GREEN / NO_RELEASE / MIGRATION_NOT_APPLIED / NO_EXTERNAL_EFFECT`。

机器证据：`aos-platform/.evidence/workshop/2026-08-24-w3-05-staged-production-start.json`、`aos-platform/.evidence/workshop/2026-08-24-w3-05-strict-sdk-ui-context.json`。

## 7. AOS-000039 刷新与两轮复审

第一轮反查 committed m1 router/Store/SDK 后，关闭“W2-D3 仍在开发”的过期描述，并确认 compile 与 start 是独立 operation：前者生成 draft Plan，后者消费 Plan/Preview/Proposal 后创建 TaskRun。整改后 W3-05 改为显式 staged orchestration，禁止一键隐藏 compile/approve；结论 `PASS_AFTER_REMEDIATION`。

第二轮沿 W3-04 ProductionContext 反向追踪发现 compiler input、Plan productionContract、ImpactPreview、ProductionStartRequest/Decision 均未携带该 exact ref，且 start router 仍只有认证门。整改新增 `DEP-PRODUCTION-CONTEXT-PROPAGATION` 与现有 `DEP-AIP-START-AUTHZ` 双门，并保持真实 Preview/Start 正向证据门；结论 `PASS_AFTER_REMEDIATION`。

刷新证据：`.evidence/workshop/2026-08-15-w3-05-production-context-start-refresh.json` 与 `.evidence/workshop/2026-08-15-w3-05-staged-start-doc-ledger.json`。2026-08-24 的后端与 strict SDK/UI 实施将最终状态推进为 `COMPLETED_CODE_CONTROL_GREEN / NO_RELEASE / MIGRATION_NOT_APPLIED / NO_EXTERNAL_EFFECT`；真实运行正向事实仍须由独立运行/发布门裁决。

## 8. 2026-08-24 实施验收

- 后端 exact chain 与显式 start role：专项 28 passed；迁移保持未应用；
- strict SDK/UI：专项 3 files / 26 tests passed；Web 累计 220 files / 2060 tests passed；TypeScript + Vite build passed；
- 内置浏览器：`/aip/production-contracts` 单一 H1、1280px 无横向溢出、AIP 依赖不可用时 0 个受保护动作可执行；
- 历史 Preview/Decision 缺少 context ref 时可读但不可启动；新 compile/Preview/Start 只能沿同一 `ProductionContextRevision` exact ref；
- 0 Provider、0 TaskRun start、0 审批、0 发布、0 真实业务写入。

下一串行任务为 W3-06；进入前按 94 号 ADR 重核 canonical Handoff transport、active AgentInstance、ModuleHandoffCompiler 与 HandoffDecision authority，不复用旧的“等别人交付”责任边界。
