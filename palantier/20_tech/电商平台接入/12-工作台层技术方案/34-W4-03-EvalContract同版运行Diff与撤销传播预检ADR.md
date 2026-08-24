# W4-03 EvalContract 同版运行、Diff 与撤销传播预检 ADR

> 状态：`IMPLEMENTED / CODE_BROWSER_GREEN / NO_RELEASE / MIGRATION_NOT_LIVE_APPLIED`
>
> 事实截面：AOS authority `AOS-000024`；AIP W2-D2 固定提交 `0391f6846beda58235dc60e16100f2a81f74ebcd`；工作台证据 `.evidence/workshop/2026-08-14-w4-03-eval-binding-preflight.json`。

## 1. 审查结论

W4-03 的产品目标正确，但当前只能确认“评价契约 authority 已建立”，不能确认“评价契约已成为运行时标准”。AIP 已有 PostgreSQL `EvalContractRevision`、create/revise/freeze/list/get Canonical API，并能 exact 绑定 EvalSuite、PublicationEvent 与 ReleaseGateDecision；冻结前会重新检查直接依赖。

尚未通过实现门的核心原因不是页面缺一个按钮，而是执行链和失效链没有闭合：

1. `AipEvalRunner.run` 仍以 `suite_id + suite_revision` 启动，不接收 exact `EvalContractRevision`；severity、gate、return、override 等任务级契约尚未成为 EvalRun 的执行 authority。
2. 发布撤销是同一 `publication_id` 下追加 `revoked` 事件；当前 EvalContract 只检查原绑定 `published event_id` 那一行，因此撤销后原行仍是 `published`，合同可能继续显示 ready。
3. frozen ImpactPreview 的启动前复核只比较 EvalContract 行的 revision/hash/lifecycle，不递归检查其 Publication/ReleaseGate，撤销无法可靠传播到生产启动门。
4. 已有 revision 可精确读取，但没有服务端语义 Diff；生产契约页在固定截面上仅提供列表、blocker 和冻结操作。
5. 没有“以 exact EvalContract 同版重跑”的命令，也没有 EvalRun/EvalReport 对 contract ref 的可核验 lineage。

因此 W4-03 保持 `NOT_STARTED / IMPLEMENTATION_BLOCKED`，不得用现有 EvalSuite 精确运行能力替代 EvalContract 同版运行完成度。

## 2. 唯一 authority 与职责边界

| 能力 | 唯一 authority | 工作台允许做什么 | 工作台禁止做什么 |
|---|---|---|---|
| 评价契约 | AIP `EvalContractRevision` | 展示 exact ref、readiness、blocker、Diff | 自建 EvalContract 表或在浏览器重算 readiness |
| 评测套件 | AIP `EvalSuiteRevision` | 展示合同绑定套件 | 静默选择最新 suite |
| 评测执行 | AIP `EvalRun` / runner | 提交 exact contract ref、观察状态 | 绕过合同直接发 suite id/revision |
| 评测报告 | AIP `EvalReportRevision` | 展示结果与 lineage | 用前端计算结果代替报告 authority |
| 发布门与发布事件 | AIP `ReleaseGateDecision` / `PublicationEvent` | 展示当前有效状态和失效原因 | 只看历史 published 行判断仍有效 |
| 启动门 | AIP frozen `ImpactPreviewRevision` + canonical start service | 消费组合门结论 | 在 Workshop 再实现一套启动校验 |

## 3. 必须补齐的 AIP 接缝

### 3.1 exact contract 驱动运行

新增 AIP Canonical command，输入至少包含：

- exact frozen `EvalContractRevision`；
- exact target Artifact/Variant revision；
- task/run/stage/attempt context；
- Idempotency-Key 与 actor。

服务端同一事务内重读合同及其动态依赖，解析 exact suite，创建 EvalRun；EvalRun 与 EvalReport lineage 必须保存 `evalContractRef`。调用方不能另传一套阈值、return mapping 或 override policy 覆盖合同。

### 3.2 发布与发布门的有效状态

Publication 的有效状态按 `publication_id` 聚合全部 append-only events，不能按绑定的单一 `event_id` 推断。`revoked/suspended/deprecated` 必须使相关 EvalContract 动态 readiness 至少变为 `stale/blocked`。

ReleaseGate 若保留 `invalidated_by`，必须有明确的 append-only invalidation command、权限、reason/evidence 与查询语义；若不采用该字段，应删除含混模型并用新的 decision/事件表达，不能留下永远为空的“伪生命周期”。

### 3.3 启动门的传递失效

二选一，且只能由 AIP 实现：

1. `assert_frozen_preview_current` 对 EvalContract 调用统一动态 readiness resolver；或
2. EvalContract 输出服务端 dependency-state hash，Publication/ReleaseGate 生命周期变化时使该状态发生可检测变化。

无论采用哪种方式，旧 ImpactPreview/Approval 都不能在依赖撤销后继续启动。失败返回稳定 reasonCode，并保留被撤销的 exact ref 和当前有效状态证据。

### 3.4 服务端语义 Diff

Diff 输入为同一 contract 的两个 exact revisions，输出至少覆盖：

- suite/publication/release-gate refs；
- artifact schema；
- severity thresholds；
- gate policy；
- return mapping；
- override policy；
- 对 Stage/Artifact/Approval 的 dependency impact。

Diff/hash 由服务端产生，浏览器只展示。任何标准变化都创建新 revision；已运行任务继续引用原合同，除非用户通过有 Receipt 的显式重编排选择新合同。

## 4. 工作台实现顺序

1. 等待 W3 全部退出门通过。
2. AIP 关闭 `DEP-EVAL-RUN-CONTRACT-BINDING`、`DEP-EVAL-PUBLICATION-REVOCATION`、`DEP-EVAL-TRANSITIVE-START-INVALIDATION`。
3. AIP 提供 strict SDK：get/list/diff/run-by-contract，并对 blocked/stale/unknown 失败关闭。
4. 工作台实现 `EvalContractBadge/Diff`、同版运行入口、EvalRun/Report/ReviewIssue lineage 展示。
5. 浏览器验收标准变更、发布撤销、发布门失效、同版返工、跨租户与幂等重放。

## 5. 验收门

- exact contract A 运行产生的 Run/Report 可证明引用 A，之后创建合同 B 不影响 A 的历史。
- publication revoke 后，合同、ImpactPreview 与 start 均在同一事实截面失败关闭。
- release gate 失效后行为同上，并返回稳定 blocker。
- Diff 完全来自服务端，能解释“改了什么、影响什么、哪些批准失效”。
- 同一 idempotency key 不产生第二 EvalRun；跨租户 ref 返回 not-found/forbidden，不泄露存在性。
- 返工生成新 attempt 与 Artifact revision，继续使用原 exact contract 时不得静默换 suite/policy。

## 6. 明确废弃与禁止

- 废弃“EvalSuite exact run 已存在，所以 W4-03 已完成”的判断。
- 禁止 Workshop 直接调用 `suite_id + suite_revision` 模拟 contract-driven run。
- 禁止用原 `published event_id` 仍存在证明 publication 仍有效。
- 禁止只比较 EvalContract 自身 hash 而忽略传递依赖。
- 禁止前端本地计算权威 Diff、readiness 或 release-gate 结论。

这些废弃项不削弱原设计目标；它们删除的是会造成静默换尺和撤销失效不传播的替代实现。

## 7. AOS-000227 复核与 W4-03 实施清单（2026-08-25）

### 7.1 已由上游实现关闭的差距

本轮重新以代码而非旧预检结论核对后，以下三项已经由 W-L13 / W3 实现，不重复建设：

1. Publication 的当前有效状态已按同一 `publication_id` 的最新 append-only event 聚合；`revoked/suspended/deprecated` 会让 EvalContract readiness 失败关闭。
2. frozen ImpactPreview 启动前会重新解析 EvalContract 动态 readiness，并比较 dependency snapshot；发布或发布门状态变化会传递阻断启动。
3. 服务端已经提供同一 EvalContract 两个 exact revision 的语义 Diff，并明确旧批准不能自动继承。

因此 W4-03 的剩余最小缺口收敛为：EvalRun/EvalReport 缺少 exact `EvalContractRevision` 血缘；严格 Web SDK 与工作台没有消费服务端 Diff。

### 7.2 文件级实施清单

| 层次 | 文件 | 最小改动 |
|---|---|---|
| contract | `services/aos-api/aos_api/aip_eval_contracts.py` | 为 Run/Report 增加可验证 exact EvalContract ref |
| persistence | `services/aos-api/aos_api/aip_eval_authority_store.py`、`services/aos-api/aos_api/aip_eval_runner.py` | 持久化并回读 contract lineage；新增 contract-driven runner 入口，服务端重读 frozen/ready exact contract 后解析 suite |
| schema | `services/aos-api/alembic/versions/w4_002_eval_contract_run_lineage.py` | 仅新增 nullable JSONB 列与约束，兼容历史记录；本轮不执行真实迁移 apply |
| API tests | `services/aos-api/tests/aip/test_aip_eval_runner.py`、W-L13 相关测试 | 验证同版绑定、幂等、跨租户/漂移/撤销失败关闭、历史无回归 |
| strict SDK | `apps/web/src/api/aipProductionContracts/{contracts,parser,index}.ts` | 增加服务端 Diff DTO、严格解析与 getDiff 方法 |
| Workshop | `apps/web/src/pages/s2/ProductionContractsPage.tsx` | 只展示权威 Diff；无两版时诚实空态，不在浏览器计算 authority |
| Web tests | 对应 parser/index/page tests | 覆盖解析、请求参数、差异与空态、可访问性 |
| generated contract | `packages/contracts/openapi/v1.generated.json`、`packages/contracts/openapi/v1.inventory.json`、`services/aos-api/tests/test_openapi_contract.py` | exact EvalContract ref 引入一个新 schema 后确定性重生成，并把结构计数门同步到 2156；不改变路由数量 |

### 7.3 163/164 分层约束

EvalContract、Publication、ReleaseGate 和 EvalRunner 都属于控制平面，不伪装成原子 Skill，也不直接制造数字同事贡献。工作台只把服务端 EvalContract Diff 解释为“评价标准变化与影响”，并在已有 `原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图` 链路旁提供治理证据；缺少真实运行与绑定事实时保持未知/空态。

### 7.4 本轮安全边界与验收

- 浏览器验收只读真实租户 `org-org/dev-project`，不触发 EvalRunner、冻结、发布、Approval、Action 或业务写入。
- migration 只做静态/临时 schema 测试，不在真实环境 apply。
- 历史无 `evalContractRef` 的 Run/Report 保持可读；新 contract-driven run 必须保存 exact ref，直接 suite-run 仍保留为兼容入口但不能冒充合同驱动运行。
- 专项测试后执行 AIP Eval/Production 合同累计回归、Web 全量测试与构建；页面用内置浏览器在 1280/1440/1920 三视口验收。

## 8. 实施与验收结果（2026-08-25）

- `m1@b6678dd0bc3824e34ae2c9878f56d3126e58e267` 已让新 EvalRun/EvalReport 保存 exact `EvalContractRevision`，并提供服务端 `run_by_contract`：先重读 frozen、ready、无 blocker 的合同，再核验合同绑定 suite 的 id/revision/hash；相同幂等键不会产生第二条 EvalRun。
- 历史 direct-suite 路径继续可读且不伪造合同血缘；`w4_002` 仅增加 nullable JSONB 与 exact-ref 约束，真实数据库没有执行 migration apply，存在已绑定记录时 downgrade 明确失败关闭。
- Web strict SDK 与生产契约页消费已有服务端语义 Diff；真实租户 `org-org/dev-project` 读到 8 个 frozen/ready 合同，并显示修订 1→2 的服务端 lifecycle 变更。浏览器不重算 authority，也没有新增运行、冻结、发布或业务写入入口。
- 后端专项 `10 passed`，累计 `64 passed`；Web 专项 `3 files / 30 tests`，全量 `221 files / 2091 tests`，TypeScript、production build、compileall、单 Alembic head 均通过。OpenAPI 确定性门为 `2580 paths / 2156 schemas / 13 passed`。
- 内置浏览器 1280/1440/1920 三视口均无横向溢出，合同创建保持 disabled，console error 为 0。证据：`.evidence/workshop/2026-08-25-w4-03-eval-contract-lineage.json`。

结论：W4-03 在代码/控制面与只读页面范围内闭合；不宣称 migration、真实 EvalRun、业务运行或 release 已执行。下一串行任务为 W4-04。
