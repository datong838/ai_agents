# W3-07 职责覆盖、Readiness、改派与人工接管分层预检 ADR

> 日期：2026-08-15；2026-08-25 按 AOS-000218 与当前 m1 重新核验并进入实现
> 状态：`IMPLEMENTED_CODE_CONTROL_BROWSER_GREEN / NO_RELEASE / MIGRATION_NOT_APPLIED / NO_EXTERNAL_EFFECT`
> 范围：当前唯一开发分支 `m1`；允许实现 authority、additive migration、strict SDK、工作台读模型、测试与浏览器验收，但不 apply 迁移、不执行发布、Provider、AgentRun、Action、Approval、Handoff 或真实业务写入。

## 1. 结论

W3-07 必须把四个常被混淆的概念拆开：

1. `ResponsibilityPlanRevision` 负责结构职责与受保护职责分离；
2. `AssigneeResolutionReceipt` 负责某个时点的实际候选与 operational readiness；
3. TaskRun 前的 reassign 负责生成不可变 frozen plan 的显式 successor；
4. TaskRun/Stage attempt 后的 takeover 负责带 Lease/fence 的运行 owner 转移。

2026-08-25 重新核验表明，旧结论的前半部分已被后续 m1 交付替代：Responsibility readiness 已按 selected AgentInstance 的 active SkillBinding 所声明 binding IDs 回读 CapabilityBinding，不再以 tenant-global healthy binding 点亮 assignee；四类 `AssigneeResolutionReceipt` authority、ToolBinding instance scope 与 Task Cockpit resolution receipt 投影也已存在。实际剩余缺口收敛为：现有 resolver 对 human/agent 的 operational 条件仍不够完整、冻结 Plan 无 immutable successor/reassign authority、运行期无 maker-checker TakeoverDecision 和 monotonic assignment lease/fence、工作台尚未同时展示 structural/readiness/reassign/takeover 四轴。当前唯一开发者可直接补齐这些代码缺口，但 runtime 使用、迁移 apply 与发布继续失败关闭。

## 2. 当前平台事实与风险

当前 m1 `02899ba` 及其上游中：

- `ResponsibilityPlanRevision` 包含 profile、template exact ref、slots、merge decisions、coverage、uncovered slots、readiness、blockers 与 content hash；
- create/revise 有幂等与 expected-version CAS，freeze 只允许 ready draft；
- independent_review、hard_compliance、external_publication_approval、receipt_reconciliation 禁止被 merge；
- DTO 暴露多类 Assignee，但 Store 对所有非 `agent_instance` 返回 `ASSIGNEE_AUTHORITY_UNAVAILABLE`；
- AgentInstance resolution 目前只校验存在与 version，尚未同时固定 active status、当前 operational readiness 与 expiry；
- ResponsibilityPlan readiness 已从 selected instance 的 active SkillBinding 提取 binding IDs，再精确回读对应 CapabilityBinding，旧的 tenant-global false-positive 已关闭；
- `aip_assignee_resolution_receipt`、四类 resolver、instance-scoped ToolBinding 和 canonical `/v1/aip/assignee-authority/resolutions` 已存在，但 Receipt 尚未固定逐候选拒绝集合、required capability exact refs、policy/capacity/expiry 快照；
- frozen Plan 不允许 revise，且没有 successor/fork/reassign API；
- 当前代码未发现 AssigneeResolutionReceipt、ResponsibilityAssignmentRevision、TakeoverDecisionReceipt 或 runtime assignment fence。

最严重风险是 false positive：同一租户内另一个执行者拥有健康 binding 时，当前 assignee 可能被错误显示为 capability-ready。页面不得用 coverage complete、Agent active、Skill 声明或租户全局 binding 任一单项推断 runnable。

## 3. 四层 authority

### 3.1 结构职责计划

ResponsibilityPlan 固定责任槽、输入输出、gate、return stage、required exact capabilities、assignee exact ref 与 merge decisions。`coverage=complete` 仅代表槽位结构完整、protected separation 成立；不承诺实时健康、容量、Provider 或预算。

### 3.2 Operational readiness

唯一 resolver 输入是 signed installed ResponsibilityTemplate、slot、required Capability exact refs、TenantScope、purpose/marking、候选 assignee/binding、policy、health、capacity 与时间快照。输出 `AssigneeResolutionReceipt`：候选全集、逐候选拒绝 reasonCodes、选中 AssigneeBinding/CapabilityBinding exact refs、policy refs、observedAt、expiry 与 hash。

HumanPrincipal、AgentInstance、ToolBinding、ProviderCapabilityBinding 必须各有真实 resolver；未实现的 kind 应从发布合同移除，而不是让 UI 可选、后端永久拒绝。Agent 的 active 不等于 SkillBinding active，SkillBinding active 不等于 CapabilityBinding healthy，binding healthy 也不等于 Provider/route/budget operational-ready。

### 3.3 启动前 reassign

当 TaskRun 尚未创建，用户改派生成 successor ResponsibilityPlanRevision：

- 引用被替代的 frozen exact revision，旧版永不覆盖；
- 保存 Diff、来源/目标 assignee 与 binding、actor、reason、政策与 approval refs；
- expected plan version/CAS 防止双操作者覆盖；
- 重新计算 coverage、separation 与 readiness，旧 ProductionContext/Plan/Preview/Approval 因 exact ref 漂移而 stale；
- 不创建 TaskRun、Handoff 或外部动作。

### 3.4 运行中 takeover

TaskRun/Stage attempt 已存在时，不能修改 frozen plan 假装历史 owner 从未存在。takeover 使用独立 `takeover_requested → takeover_approved/rejected`，通过后创建新 execution assignment lease 与单调 fence。Receipt 固定旧/新 owner、TaskRun/step/attempt、Checkpoint、unfinished refs、审批、原因、health/expiry、Provider outcome 和影响范围。

存在 active lease、职责隔离冲突或 in-flight Provider unknown 时不得强制换 owner；必须先到安全点、释放/失效旧 Lease，或 reconcile Provider。fence 前进后，旧 owner 的 heartbeat、Checkpoint、Artifact 与终态迟到写全部失败关闭。

## 4. Handoff 与职责边界

HandoffEnvelope 只完成最小上下文安全送达；accepted Handoff 不等于 assignee/owner 已变更。reassign 或 takeover 也不隐式表示 receiver 已 consume/accepted。需要交接上下文时，两者通过 exact refs 与 Receipts 关联，但各自状态独立：

```text
Responsibility successor / TakeoverDecision
  ├─ ownership authority
  ├─ optional HandoffEnvelope exact ref
  └─ optional HandoffDecision exact ref
```

任何跨 Module 交接不得复制客户资料、Evidence 正文或媒体 payload；只传授权 exact refs、purpose、requestedOutcome 与 markings。

## 5. 目标操作与读模型

- `ecommerceWorkshopResponsibilityCoverageGet`：同时返回 structural coverage 与 protected separation；
- `ecommerceWorkshopAssigneeResolve`：返回 immutable Resolution Receipt 与 readiness blockers；
- `ecommerceWorkshopResponsibilityReassign`：仅 TaskRun 前生成 successor plan；
- `ecommerceWorkshopTakeoverRequest/Decide`：仅运行期管理 maker-checker 决定；
- `ResponsibilityMatrixReadModel`：按 slot 展示计划 assignee、实时 readiness、候选、blocked reason、reassign/takeover 可用性和 Receipt links。

UI 必须把“责任已覆盖”“当前可执行”“改派待复核”“接管待批准”“Provider 状态未知”分开，不用在线人数或绿色圆点替代权威状态。禁用操作仍可聚焦并说明 reasonCode、所需权限与恢复动作。

## 6. 依赖与停止门

| 依赖 | 当前状态 | 关闭条件 |
|---|---|---|
| W3-01 | runtime 未 GREEN | Agent/Binding/Run canonical API、SDK、exact refs GREEN |
| W3-04 | ProductionContext 方案已解环，runtime 未 GREEN | frozen Responsibility exact ref 进入组合 authority |
| DEP-RESPONSIBILITY-TEMPLATE-RESOLVER | 缺失 | signed installed 8/8 templates 可 exact resolve |
| DEP-EXACT-ASSIGNEE-RESOLVER | 缺失 | 四类 assignee 支持或发布合同收敛 |
| DEP-ASSIGNEE-BINDING-OWNERSHIP | RED | 每个 required capability 证明属于 selected assignee |
| DEP-FROZEN-PLAN-SUCCESSOR | 缺失 | immutable successor + supersedes + CAS GREEN |
| DEP-RUNTIME-ASSIGNMENT-FENCE | 缺失 | lease/fence/checkpoint/late-write tests GREEN |
| DEP-TAKEOVER-DECISION-AUTHORITY | 缺失 | maker-checker Decision/Receipt/timeline GREEN |

## 7. 验收矩阵

正向覆盖 8/8 Module template、四类支持中的每一类 assignee、结构 complete 但 runtime blocked、reassign 使旧 ProductionContext/Preview stale、takeover 后旧 fence 拒写、刷新重建。负向覆盖：

- 租户内无关 healthy binding 不能点亮 assignee；
- suspended/revoked/stale instance、Skill、Capability、Binding、route/provider；
- protected responsibilities 被 merge 或同一主体违反 separation；
- 双操作者 reassign/takeover CAS 冲突；
- active lease、unsafe checkpoint、Provider unknown、旧 fence 和迟到回包；
- 跨租户 template/candidate/binding/Receipt；
- org-org 正向与 dev-org 隔离、重启恢复与 slot 数量守恒。

## 8. 两轮审查

第一轮发现：现有 coverage/readiness 容易被合并成单一绿色状态，且 tenant-wide binding 会产生 false positive。整改后冻结 structural coverage 与 AssigneeResolutionReceipt 双轴，并要求 binding 对 selected assignee 的 exact ownership。结论：`PASS_AFTER_REMEDIATION`。

第二轮发现：旧方案将 reassign 与人工接管写成“新 Plan revision 或 assignment event”，未按 TaskRun 边界决定唯一 authority。整改后冻结 TaskRun 前 successor plan、TaskRun 后 TakeoverDecision + execution lease/fence，并将 Handoff 状态完全解耦。结论：`PASS_AFTER_REMEDIATION`。

## 9. 2026-08-25 文件级实施清单

1. `services/aos-api/aos_api/aip_responsibility_assignment.py`：冻结 successor、takeover request/decision、assignment lease/fence、read model 与 blocker 合同；所有 exact refs、CAS、maker-checker、expiry 与安全点条件严格校验；
2. `services/aos-api/aos_api/aip_responsibility_assignment_store.py`：实现 tenant-scoped append-only successor/takeover timeline 与单调 assignment head；启动前只允许 TaskRun 不存在时生成新 frozen successor，运行中批准只允许 safe checkpoint 且无 Provider unknown/active competing lease；
3. `services/aos-api/alembic/versions/w3_016_responsibility_assignment.py`：增加 additive authority 表、RLS/FORCE、append-only trigger、unique/CAS/fence 约束；本波只验证迁移图和 SQL，不 apply 到真实库；
4. `services/aos-api/aos_api/routers/aip_responsibility_assignment.py` 与 domain aggregate：注册 canonical coverage/readiness/reassign/takeover/fence API，权限从 Principal 获取，拒绝 body tenant 注入；
5. `services/aos-api/tests/test_w3_07_responsibility_assignment.py`：覆盖 immutable successor、TaskRun 边界、maker-checker、active lease、Provider unknown、CAS、fence late write、跨租户与零外部副作用；
6. `services/aos-api/aos_api/ecommerce_workshop_task_cockpit*` 与 `apps/web/src/api/ecommerceWorkshop/*`：投影 structural coverage、current readiness、successor/takeover 状态与 strict parser；
7. `apps/web/src/components/workshop/TaskCockpitPage*`：分开显示“结构已覆盖 / 当前可执行 / 改派 / 接管 / Provider unknown”，所有命令在 exact readiness 缺失时可聚焦但禁用并显示恢复动作；
8. `.evidence/workshop/2026-08-25-w3-07-*`：记录专项、累计、迁移图、构建、内置浏览器和副作用守恒。

## 10. 当前决议

W3-07 由旧的 `HARD_GATE_BLOCKED` 更新为 `IN_PROGRESS`。当前唯一开发者不再等待外部代码交付，直接维护所需 AIP 与 Workshop 层；但代码完成仍只允许声明 `CODE_CONTROL_BROWSER_GREEN`，不得把未 apply 的迁移、未发生的 live assignment/takeover 或未发布的版本描述为 operational/release GREEN。

历史机器证据：`.evidence/workshop/2026-08-15-w3-07-responsibility-reassign-takeover-preflight.json` 与 `.evidence/workshop/2026-08-15-w3-07-responsibility-reassign-takeover-doc-ledger.json`；本波闭环将新增 `.evidence/workshop/2026-08-25-w3-07-*`。

## 11. 2026-08-25 实施与复审结论

W3-07 已按上述四层 authority 完成代码控制闭环：

1. 新增 frozen ResponsibilityPlan successor，要求 source exact ref、expected version、目标 AssigneeResolution Receipt，且检测到 TaskRun 后强制转入 takeover；旧 plan 不覆盖；
2. 新增 maker-checker takeover request/decision、decision-time StepRun 安全重验、monotonic assignment lease/fence 与 exact fence assertion；active lease、terminal step、Provider outcome unknown 全部失败关闭；
3. 新增 `w3_016` additive migration，四表 tenant RLS/FORCE，三类事件 append-only，assignment head 仅允许受控 fence 前进；本波只验证迁移图及 `w3_015:w3_016` 离线 SQL，未 apply；
4. 新增 run-scoped observation，将 request、decision 与 current lease 分开；Task Cockpit 以独立失败域展示“结构覆盖 / 当前可执行 / 启动前改派 / 运行中接管”，旧 Resolution Receipt 只标记观测时已解析，不冒充当前 runnable；
5. 页面中的 reassign/takeover 命令保持可聚焦但禁用，明确 `TASK_RUN_EXISTS_USE_TAKEOVER` 与 exact Step、Receipt、maker-checker、安全点恢复条件；未执行任何外部副作用。

验收：后端专项与累计分别 `11 / 54 passed`；Web 专项 `47 passed`、累计 `220 files / 2068 tests passed`；生产构建、Python compile、OpenAPI 五路由、迁移单头与区间离线 SQL 均 GREEN。内置浏览器在 1280px 下无横向溢出，且 aos-api 不可用时明确显示离线和读取失败，没有空集合或伪 ready。机器证据：`.evidence/workshop/2026-08-25-w3-07-responsibility-assignment.json`。

方案/代码一致性复审结论：`PASS_AFTER_IMPLEMENTATION_REVIEW`。仍不得声明 migration applied、runtime operational 或 release GREEN；授权迁移与发布前，新表读模型失败必须保持独立失败关闭。
