# W3-12 统一运营 Case、分类、可逆聚合、SLA 与 Kill 预检 ADR

> 日期：2026-08-15
> 状态：`PLAN_REMEDIATED_GREEN / RUNTIME_NOT_STARTED / HARD_GATE_BLOCKED / NO_EXTERNAL_EFFECT`
> 基线：`AOS-000039`、`w2-workshop@e74b5fd73e9c4a24ee8bbb873d80d6c896e772ab`
> 证据：`.evidence/workshop/2026-08-15-w3-12-operations-authority-preflight.json`

## 1. 决策与四层边界

L0/O1 的 Order、OrderLine、ProductSku 库存语义、Shipment、Payment 与批准的售后 Event/Object 是不可复制、不可由 Workshop 改写的 originals。W3-12 的 OperationCase 是 tenant-scoped、event-sourced 的 L1 聚合 authority：它用 exact scoped refs/hash 组织 originals、分类决定、成员关系和 CaseEvent，但不是交易或原始事件真源。Case list、timeline、SLA 汇总只是可删除重建的 projection。

当前 Bundle 仅声明 `OperationCase` 类型名；OperationCase、AggregationPolicyRevision、OperationEventClassificationDecisionRevision、SlaPolicyRevision、kill Decision 与 operations Store/API/strict SDK/Web 全部不存在。W3-10/W2-01 未运行 GREEN，本 ADR 只闭合方案，不授权实现或外部动作。

## 2. Authority 与状态变化

| 事实 | authority | 变化方式 |
|---|---|---|
| 交易/原始事件 | L0/O1 upstream | Workshop 只读 exact ref/hash |
| 分类 | OperationEventClassificationDecisionRevision | append-only，记录 classifier/policy/evidence/confidence/actor/reason |
| 聚合规则 | AggregationPolicyRevision | append-only + expectedVersion |
| Case | OperationCase + CaseEvent | 成员/status 由 originals 与 append-only 决定重建 |
| 拆分/合并 | CaseMembershipDecisionRevision | append-only predecessor/successor/moved-originals |
| SLA | SlaPolicyRevision + SlaClockDecision | exact policy、event time、pause/resume |
| Kill | AutomationKillDecisionRevision 或 canonical platform kill ref | append-only；Proposal/Lease/执行前复验 |

创建/分类/附加 originals 以 provider event/ref/hash 和 Idempotency-Key 去重；修订、拆分、合并、priority、pause/resume、close/reopen 与 kill 使用 expectedVersion。服务端只取 Principal TenantScope，跨租户、缺失 originals、hash 漂移、重复 key 异 payload 一律失败关闭。

## 3. 可逆聚合与守恒

策略换版先在固定 cutoff 上产生候选 membership、before/after Diff、unmatched/conflict 与 count ledger；只有显式接受才追加 successor 决定。拆分/合并保存 predecessors、successors、moved originals、actor/reason 和前后数量，旧 Case timeline、Decision、Attempt 与 Receipt 永久可达。

每个 Case member 必须能回溯到 exact original；重复/晚到/乱序事件不重复成员或动作。删除或重建 projection 不删除 original、Classification、Policy、CaseEvent、Decision 或 Receipt。`original total = attached + unmatched + conflicted`，拆并前后 originals 多重集合守恒。

## 4. SLA 与 Kill

SLA 基于 source event time、exact SlaPolicyRevision 与显式 pause/resume Decision 计算；浏览器当前时间、列表排序或旧 deadline 缓存不构成 authority。policy drift 将 readiness 标 stale，经显式重算/接受后产生 successor，不覆盖历史 breach 判断。

kill 在 Proposal 创建、Lease 获取和 executor 调用前分别复验 exact scope/account/capability/policy。kill 激活后阻止新副作用，不撤销历史成功，也不把 in-flight/unknown 伪装为失败；它们必须继续可见并进入 reconcile。kill 解除同样是新 Decision，不自动重放被阻断动作。

## 5. 依赖、验证与停止门

硬依赖为 W3-10、W2-01、DEP-C0、`DEP-OPERATION-EVENT-CONTRACT`、`DEP-OPERATION-CASE-AUTHORITY`、`DEP-AGGREGATION-POLICY-AUTHORITY`、`DEP-CASE-REVERSIBLE-MEMBERSHIP`、`DEP-SLA-POLICY-AUTHORITY` 与 `DEP-AUTOMATION-KILL-AUTHORITY`。

同一 release identity 必须覆盖 Contract、Store、API、strict SDK、Web、browser、安全与租户。必测重复/晚到/乱序、跨租户、策略换版 Diff、拆并回放与数量守恒、SLA pause/resume/drift、kill 三检查点、in-flight unknown reconcile、PII/Secret 最小披露。正向只认 `org-org/dev-project`，`dev-org/dev-project` 只作负向 canary。

## 6. 两轮审查

第一轮发现旧文档同时把 OperationCase 写成 L1，又要求“未有 L0 authority 时不得在 L1 建真源”，层级矛盾。整改后明确 originals 属于 L0/O1，Case 是合法的 L1 事件化聚合 authority，view 才是 projection。

第二轮发现旧方案只有“幂等聚合、SLA、kill”关键词，没有分类 Decision、策略换版接受、拆并 successor、originals 多重集合守恒、SLA clock 和 kill 三检查点/in-flight 语义。补齐后方案复审通过；运行时仍为 `NOT_STARTED / HARD_GATE_BLOCKED`，不得勾选。

## 7. 2026-08-24 R37 依赖解环整改

> 后继基线：`AOS-000156 / m1@54031a8`
> 状态：`W3_12A_AUTHORITY_PENDING / W3_12B_RUNTIME_PENDING`

原第 5 节将 W3-12 硬依赖写成完整 `W2-01`，会与 W2-01 的 OperationCase 消费形成循环。后继裁决如下，优先于原硬依赖表述：

1. `W3-12A` 只依赖 D0 originals/售后 exact authority、`W2-01A` 已冻结的 public read primitives，以及既有 AIP Task/Action/Approval/Receipt 公共 ref；不得依赖 W2-01 full runtime 或 W2-01B。
2. `W3-12A` 建立唯一 OperationCase、CaseEvent、ClassificationDecision、AggregationPolicy、SLA 与 Kill Decision authority；任何 migration 都必须取得独立 Lease、保持 single head、RLS/FORCE RLS、append-only 与回滚验证。
3. `W2-01B` 消费 W3-12A exact Receipt 后闭合 Case slice；不得客户端拼装或复制 Case authority。
4. `W3-12B` 最后实现命令、运行交互、strict SDK/UI 和浏览器验收；真实副作用仍须 Proposal→Approval→ExecutionLease→Receipt，unknown 进入 reconcile，禁止盲重试。
5. 固定 Receipt 顺序：`DATA_D0_INVENTORY_AFTERSALES_AUTHORITY_GREEN` → `W2_01A_READ_MODEL_SHELL_GREEN` → `W3_12A_OPERATION_CASE_AUTHORITY_GREEN` → `W2_01B_UNIFIED_OPERATIONS_VIEW_GREEN` → `W3_12B_OPERATION_COMMAND_BROWSER_GREEN`。

当前唯一开发者可在 `m1` 串行维护 Data、Workshop、AIP 与运行层，因此不再因 Owner 交接停工；但缺少 exact authority 时只能实现诚实 blocked 合同，不得把计划、测试桩或通用对象名称冒充 runtime GREEN。
