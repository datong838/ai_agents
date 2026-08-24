# W3-13 经营参谋 Insight / Decision / GrowthPlan / TaskGraph / EffectReview 预检 ADR

> 日期：2026-08-15  
> 状态：`CODE_BROWSER_GREEN / NO_RELEASE / NO_EXTERNAL_EFFECT`
> 实施基线：`AOS-000224`、`m1@7138b83`
> 证据：`.evidence/workshop/2026-08-25-w3-13-analyst-authority.json`

## 1. 决策与 AIP-8 边界

AIP-8 负责领域中立的 query/plan/saved-exploration shell、受控查询和异步作业基元；电商 SolutionPack/Workshop L1 负责 InsightRevision、DecisionSummary、GrowthPlanRevision、EffectReview schema/authority 与 GrowthPlan→TaskGraph 领域 materializer。双方只通过 exact contracts/refs 连接，AIP-8 不复制八 Module 页面或业务状态，L1 不复制通用 Task/Evidence/Eval/Handoff/Memory authority。

当前五个目标 authority 和 Analyst Store/API/strict SDK/Web 均不存在，AIP-8 也未 implementation GREEN；AOS-000040 的 BIND-3 进展不改变这些事实。本 ADR 只闭合方案，不进入实现。

## 2. Authority 与披露合同

- InsightRevision：append-only，显式类型为 observation/correlation/attribution/causal_claim，不可静默升级；绑定 exact metric/evidence/method/eval refs、cutoff、假设与 uncertainty。
- DecisionSummary：只存结论、证据链、归因路径、关键假设、反证、替代解释与不确定性；禁止保存、返回或用调试字段泄漏模型私有思维链。
- GrowthPlanRevision：append-only，固定目标、constraints、budget、expected effect、confidence、stop conditions 和 exact refs；修订使用 expectedVersion。
- TaskGraphRevision：canonical AIP Task authority 的物化结果，不在 L1 另建 Task 真源。
- EffectReview：append-only，固定 baseline/comparison/maturity window/eligible population/method/assumptions/limitations、exact plan/task/action/receipt refs 与 counterfactual 限制。

## 3. 原子物化与数量守恒

materialize 是显式、幂等、all-or-nothing 的服务端命令，只接受一个 approved exact GrowthPlanRevision。命令冻结 eligible plan items，产生稳定 mapping ledger，并保证 `eligiblePlanItemCount = createdOrExistingCanonicalTaskCount = mappingCount`。同 Idempotency-Key 同 hash 回读同一 TaskGraphRevision，异 hash 冲突；中途失败不得留下孤儿 Task。

批准后 metric/evidence/method/eval 漂移使 materialization readiness stale。用户必须接受 successor GrowthPlanRevision 后再物化新 TaskGraph；旧 Plan、Graph 与 Task 仍可达，不把新 Task 追加到旧 Graph，也不自动取消已执行 Task。

## 4. 效果成熟、修正与知识治理

成熟窗口前 EffectReview 只能 pending；样本不足、比较不可兼容、late data 未收敛或归因方法不支持时为 unknown/inconclusive，不能计入成功或伪装 0 effect。late data、方法漂移、假设更正和计划替代追加 successor Insight/Decision/Plan/EffectReview，并标明 corrected/supersedes；历史上下文不覆盖。

EffectReview 可以提出 MemoryCandidate，但知识治理、批准、晋升和撤销是独立流程；不得因 effect-matured 或模型高置信自动晋升 Wiki/记忆。

## 5. 依赖与验收

硬依赖为 W3-10、W2-06、DEP-C0、DEP-A8、`DEP-ANALYST-METRIC-OBSERVATION-QUALITY`、`DEP-INSIGHT-DECISION-AUTHORITY`、`DEP-GROWTH-PLAN-AUTHORITY`、`DEP-GROWTH-PLAN-TASKGRAPH-MATERIALIZER`、`DEP-EFFECT-REVIEW-AUTHORITY`、`DEP-EFFECT-MATURITY-POLICY` 与 `DEP-A8-GENERIC-ANALYST-SHELL`。

同一 release identity 必须覆盖 Contract、Store、API、strict SDK、Web、browser、安全和租户：口径兼容/unknown 非 0、四类 Insight 负向、DecisionSummary 披露扫描、Plan CAS/漂移、TaskGraph 原子/幂等/数量守恒、Effect maturity/late-data/inconclusive/correction、MemoryCandidate 非自动晋升、小群体最小披露、`org-org/dev-project` 正向和 `dev-org/dev-project` 负向。

## 6. 两轮审查

第一轮发现旧方案把 AIP-8、Analyst Module 与领域对象并列，却未明确谁拥有 Insight/Plan/Effect authority。整改后冻结 AIP-8 通用壳、SolutionPack/Workshop L1 领域 authority 与 canonical AIP Task 真源三者边界。

第二轮发现“Task 数量守恒”和“效果成熟”缺乏事务、幂等、mapping ledger、partial failure、late-data/inconclusive/correction 及 MemoryCandidate 治理语义。补齐后方案复审通过；运行时仍 `NOT_STARTED / HARD_GATE_BLOCKED`，不得勾选。

## 7. 2026-08-25 实施复核与文件级清单

### 7.1 当前事实

- 当前 authority 为 `AOS-000224`，W3-10、W3-11、W3-12 已形成代码、浏览器与 Receipt 证据；W3-13 是 S3 的下一个串行门。
- 现有 `ecommerce_workshop_analyst*` 与 `AnalystPage` 只提供七视图只读指标/质量壳；仓内没有电商领域 `InsightRevision`、`DecisionSummaryRevision`、`GrowthPlanRevision`、`TaskGraphRevision` authority。
- AIP 已有领域中立 Task 与通用 EffectReview 基元，但不得复制为第二套 Task 真源，也不得把通用 EffectReview 自动解释为电商增长归因完成。
- 本波依赖由唯一开发者在同一 `m1` 串行补齐，不再以“等待他人交付”为停工理由；发布、线上迁移、真实 Task 创建/调度、Action、Approval、Handoff、takeover、业务写与 Memory 晋升仍保持失败关闭。

### 7.2 163/164 落位决策

W3-13 沿用“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图”的四段链。领域 authority 只记录可审计业务对象与 exact refs；不把 Skill/Logic/Coworker 投影写成运行真源。工作台贡献视图只在收到 exact binding refs 时显示已绑定，否则显式 `unknown`，不得从角色名或页面路由推断。

### 7.3 本波最小实现清单

- `services/aos-api/aos_api/ecommerce_analyst_authority_contracts.py`：严格合同、四类 Insight、有限披露 Decision、Plan CAS、TaskGraph 数量守恒、Effect maturity/correction 约束。
- `services/aos-api/aos_api/ecommerce_analyst_authority_store.py`：租户隔离、append-only revision、expectedVersion CAS、幂等 Receipt 与 exact readback。
- `services/aos-api/aos_api/ecommerce_analyst_materializer.py`：只编排 canonical AIP Task authority；完整返回后才提交 TaskGraph，partial/mismatch/drift 失败关闭。
- `services/aos-api/alembic/versions/w3_018_ecommerce_analyst_authority.py`：additive authority 表、FORCE RLS、append-only guard；本波不执行真实环境迁移。
- `services/aos-api/tests/test_ecommerce_analyst_authority_contracts.py`、`test_ecommerce_analyst_authority_store.py`、`test_ecommerce_analyst_materializer.py`、`test_w3_018_ecommerce_analyst_authority_migration.py`：合同、CAS、幂等、跨租户、原子失败、数量守恒与迁移静态门。
- `apps/web/src/components/workshop/AnalystPage.tsx` 与测试：补齐七视图 ContributionLineage；缺 exact refs 时诚实显示 unknown，不改变现有指标与质量能力。
- `.evidence/workshop/2026-08-25-w3-13-analyst-authority.json`、Delivery Receipt、01/06/authority：专项测试、累计回归、三视口浏览器、方案一致性与 Prime 回读闭环后再写入。

### 7.4 验收与回退边界

专项测试先证明失败关闭，再跑 S3 后端累计、Web 全量、TypeScript、build、OpenAPI 与 Alembic 单 head；页面用内置浏览器在 `org-org/dev-project` 三视口验收并检查控制台。任何失败只回退本波 additive 代码/未应用迁移，不修改真实业务数据，不冲洗离线队列，不自动创建 Task 或晋升 MemoryCandidate。

## 8. 2026-08-25 实施结论

- 已建立四类 Insight、有限披露 DecisionSummary、GrowthPlan CAS、TaskGraph 数量守恒与 EffectReview maturity/correction 严格合同；pending/unknown 保持未知，不伪装为 0。
- Store 已落实租户/actor 隔离、append-only revision、expectedVersion CAS、幂等 Receipt 与 exact readback；`w3_018` 只新增 authority 表、RLS 与 append-only guard，本波未对真实环境执行迁移。
- materializer 只接受 approved/current exact GrowthPlanRevision，并要求 canonical Task adapter 完整、原子返回；仓内不存在满足该合同的安全 adapter，因此未安装替代实现、未创建真实 Task，相关路径继续失败关闭。
- Analyst 工作台新增 ContributionLineage；缺少 exact SkillBinding/LogicRevision/AgentRun 时，原子 Skill、Logic、数字同事保持 `unknown`，不从页面角色反推绑定。
- 验证通过：后端专项 `15 passed`、S3 后端累计 `282 passed`、Web 全量 `221 files / 2084 tests`、TypeScript、production build、compileall、OpenAPI deterministic/contract `13/13`、Alembic 单 head 与 diff-check。当前环境未安装 Ruff，因此该轴记录为 `NOT_RUN_TOOL_UNAVAILABLE`，没有冒充 GREEN。
- 内置浏览器在 `org-org/dev-project` 的 1280×720、1440×900、1920×1080 三档完成 Analyst 七视图、质量页、贡献链与 unknown 语义验收，控制台 error 为 0；观察到既有待同步离线写入 `1`，本波没有冲洗或触发它，业务写仍为 0。

结论：W3-13 达到 `CODE_BROWSER_GREEN / NO_RELEASE / NO_EXTERNAL_EFFECT`，只开放 W3-14 三领域 authority 与公共编排最终累计门。
