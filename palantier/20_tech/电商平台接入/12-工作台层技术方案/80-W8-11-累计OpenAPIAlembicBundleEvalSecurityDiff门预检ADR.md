# W8-11 累计 OpenAPI、Alembic、Bundle Eval、Security 与 Diff 门预检 ADR

> 日期：2026-08-15  
> 状态：`CUMULATIVE_GATE_CONTRACT_APPROVED / IMPLEMENTATION_IN_PROGRESS / NO_MIGRATION_APPLY / NO_EXTERNAL_EFFECT / NO_RELEASE`  
> 基线：`AOS-000280`、`m1@2b720d484988bcd678778204f3cd53d6e66668b8`  
> 证据：`.evidence/workshop/2026-08-15-w8-11-cumulative-openapi-alembic-bundle-eval-security-diff-preflight.json`

## 1. 决策

W8-11 是同一 Git/build、AOS revision、Bundle/Installation 与 tenant cutoff 下的 release ledger，不是跨提交汇总测试数量。W8-01～10 均未 GREEN，本轮只冻结累计门。

## 2. Release identity 与十四栏

identity 固定 Git/clean tree、authority/Receipts、build hashes、OpenAPI/SDK、Alembic/schema、Bundle/lock/Installation/八 Module、policy/capability/adapter/account/model/provider/Eval，以及 `org-org` 正向、`dev-org` 负向与 cutoff。

十四栏为：contract/schema、unit/parser、Store/RLS/CAS/append-only、Service/integration、OpenAPI、Alembic、Bundle/Resolver/Installation/Eval、Web/typecheck/build、browser/a11y、security/supply-chain、fault/restart/race/reconcile、operational/SLO/runbook/DR、diff/generated/honesty、Receipts/exact readback。

## 3. 汇总规则

每栏保存 command、exit、scope、artifact/evidence ref、revision 和 disposition。历史通过数不跨 commit 相加；generic AIP 测试不替代领域测试；blocked/failed-close 不替代正向；skipped、deselected、xfail、warning、unavailable、N/A 均需理由、owner 与 release 决策。代码或依赖漂移使受影响栏失效，补跑前最终聚合保持 blocked。

只有十四栏所有 required 项 GREEN、P0/P1/critical/high 与 release unknown blocker 为零，W8-11 才可勾选。

## 4. 两轮审查

第一轮补齐 release identity 与十四栏，禁止混合 revision 测试数。第二轮补齐漂移失效、N/A 处置、负向证明和 Receipt exact readback。合同通过；实际累计门硬阻断。

## 5. 2026-08-26 串行实施范围与文件级清单

本波把第 2～3 节冻结的合同实现为只消费调用方结构化 EvidencePack 的纯计算门与只读贡献卡片。它不主动执行测试、生成 OpenAPI/SDK、运行 Alembic、安装 Bundle、扫描依赖、修改生成物、探测真实租户或改变 release 状态。具体文件：

1. `apps/web/src/components/workshop/workshopCumulativeReleaseGate.ts`：定义同一 release identity、十四栏 Evidence、disposition、P0/P1/critical/high/unknown blocker 与 drift invalidation 的纯计算判定；验证 Git clean、AOS revision、build/OpenAPI/SDK/Alembic/schema/Bundle/Installation/八 Module 与 tenant cutoff exact 一致，任何 skipped/N/A/xfail/warning/unavailable 无 owner/理由/决策即失败关闭。
2. `apps/web/src/components/workshop/workshopCumulativeReleaseGate.test.ts`：覆盖空输入、跨 commit 聚合、dirty tree、cutoff/revision/hash 漂移、十四栏缺失、失败关闭替代正向、disposition 不完整、负向租户缺失、Receipt readback 不 exact、严重安全项/unknown blocker、受影响栏未补跑与完整证据合同 GREEN。
3. `apps/web/src/components/workshop/WorkshopCumulativeReleaseGateCard.tsx` 与测试：只读展示“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献”、十四栏状态、release identity、风险计数与 unknown；不显示运行、修复、迁移、安装或发布按钮。
4. `apps/web/src/components/workshop/TaskCockpitPage.tsx` 与现有测试：将 W8-11 卡片独立挂载在 Task API `AsyncStateBoundary` 外；既有任务、交接、W8-07～W8-10 卡片和错误态不得回退。
5. `.evidence/workshop/w8-11/`：记录专项、累计、TypeScript、build、只读合同探针与内置浏览器验收。视觉 fixture 仅证明布局和失败关闭，不成为任何十四栏正向证据。

所有 `runTests`、`generateOpenApi`、`applyMigration`、`installBundle`、`fixSecurity`、`mutateGenerated`、`release` 命令恒为 false。涉及 OpenAPI、Alembic、Bundle Eval、security 与 diff 的实际命令由本轮工程验收在终端显式执行并形成 EvidencePack；页面本身永不执行。

## 6. 验收与停止条件

- 十四栏每栏必须携带 command、exit、scope、artifact/evidence ref、revision、cutoff 与 disposition；同 release identity 之外的历史测试数不得累计。
- required 栏只有真实 `passed` 且 exit 0、exact Evidence ref、无漂移才算 GREEN；blocked/failed-close/skipped/N/A/xfail/warning/unavailable 均不替代正向，例外处置必须有 reason、owner、decision ref，且仍由 release 决策显式裁决。
- `org-org/dev-project` 正向和 `dev-org/dev-project` 负向证据必须同 cutoff；P0/P1/critical/high 与 release unknown blocker 必须为 0；Receipt exact readback 必须与 release identity 同版。
- 专项、Task Cockpit 既有测试、Web 全量、TypeScript、生产构建、OpenAPI 只读校验、Alembic 只读图校验、Bundle Eval、security 与 diff/honesty 均需记录真实结果；不执行 migration apply、Bundle 安装、自动修复或发布。
- 页面必须用内置浏览器确认唯一 H1/main、无横向溢出、unknown 不归零、十四栏逐栏可见且无状态改变按钮。
- 本波最多签发 `ENGINEERING_CUMULATIVE_GATE_BROWSER_GREEN / RELEASE_LEDGER_POSITIVE_EVIDENCE_BLOCKED / NO_MIGRATION_APPLY / NO_EXTERNAL_EFFECT / NO_RELEASE`；工程命令自身 GREEN 不等于真实同版十四栏聚合、operational ready 或 release GREEN。
