# W7-03 StageTemplate 编译 PlanStep 与 TaskRun 组合门预检 ADR

> 日期：2026-08-15；2026-08-25 唯一开发者串行复核并开工
> 状态：`COMPLETED_GREEN / CODE_CONTRACT_BROWSER_GREEN / SECURITY_SCOPED_GREEN_REPO_BASELINE_RED / NO_EXTERNAL_EFFECT / NO_RELEASE`

## 决策

W7-03 分成三段且 authority 不合并：

1. Compiler 以 frozen exact 生产合同为输入，确定性输出 draft canonical PlanRevision 和 CompilationReceipt；
2. Plan 由 AIP 唯一审批 authority 批准；
3. 独立 ProductionStart 组合门复验后创建一个 queued canonical TaskRun。

Compiler 不启动运行，Workshop/BFF 不建 Plan、StageRun、TaskRun 第二真源。PlanStep 必须携带 exact capability、schema、责任/assignee、gate、applicability、checkpoint/retry/compensation；not-applicable Stage 必须有 canonical skipped 语义和证据。编译按规范化拓扑顺序、compiler version 与 input hash 生成稳定 content hash，并验证 dependency schema compatibility。

## 现场事实

机器证据：`.evidence/workshop/2026-08-15-w7-03-stage-template-compiler-taskrun-preflight.json`。

当前已有模板 freeze/seal、环/未知依赖拒绝、exact template/ResponsibilityPlan 校验、AipTaskStore Plan 写入、Plan 审批后才能建 TaskRun、租户与幂等基础，专项 29 项测试通过。

仍有 14 项阻断：W7-01/02 未 GREEN；ProductionStart 仅 DTO；PlanStep capability 丢失；Stage 执行语义仅在 opaque risk；not-applicable 仍为普通 Step；编译输入不含 Recommendation/Confirmation/Brief/Evidence/Eval/MergePolicy/Policy；schema compatibility、capability-assignee resolution、规范化拓扑/input hash、传递漂移、start gate 消费、TaskRun 组合和媒体正向证据缺失。

## 双轮复审

第一轮产品/职责边界：全生命周期可见、编译不暗中启动、用户确认与 Plan 审批保留，`PASS`。

第二轮技术/安全边界：单一 authority、确定性、exact refs、schema、skip、漂移、CAS/幂等和 fail-closed 已冻结；14 项缺口未被误报为完成，且无代码/数据库/租户/外部变更，`PASS`。

结论：W7-03 合同基线通过，实现保持未开始。

## 2026-08-25 独立复核与实施裁决

本次不沿用 2026-08-15 的历史阻断结论，按 `AOS-000257`、W7-01/02 Receipt 与当前代码重新核验：

1. W7-01 已提供 signed-installable LITE/STANDARD/FULL 媒体 Stage/Responsibility typed template、八责任与十 Capability 映射；W7-02 已提供 exact Recommendation/Confirmation/MergePolicy 与预计成本确认门。二者只形成候选/代码 authority，不冒充 publish/install/runtime。
2. 通用 W2-C 已有 frozen StageTemplate 编译、ResponsibilityPlan/ProductionContext exact 校验、canonical PlanRevision、幂等 Receipt；W2-D 已有 Preview/Action/Logic 组合复验，并在同一事务中批准 Plan、创建唯一 queued TaskRun，不建第二运行真源。
3. 当前缺口收敛为：PlanStep 仍只保留标题和输入引用；规范化拓扑、input/compilation hash、not-applicable canonical skip、Stage 的 capability/schema/responsibility/assignee/gate/checkpoint/retry/compensation 语义没有进入 PlanStep；受治理 Profile 的 Recommendation/Confirmation/MergePolicy 与 ProductionContext 四合同未形成编译输入快照；start gate 尚不能复验新 compiler envelope。
4. DEP-C0 的 canonical Task/Plan/Run 真源已存在，故不存在等待其他开发者的阻断；本波只扩展现有合同与 JSON authority，不新增 StageRun 表、不 apply 迁移、不创建真实 TaskRun、不调用 Provider。
5. 163/164 分层继续适用：Stage 只编排原子 Skill/Capability 合同，Logic 保持执行顺序与条件 authority，数字同事通过 ResponsibilityPlan assignee 绑定，工作台展示编译贡献、精确输入和阻断，不把 Tool/Provider 副作用下沉到 Skill。

## 2026-08-25 文件级施工清单

1. 扩展 canonical `PlanStep`，结构化携带 applicability、capability、schema、responsibility/assignee、gate、checkpoint/retry/compensation 与 skip 语义；旧调用保持兼容。
2. 扩展编译请求/结果，受治理 Profile 必须携带 Recommendation/Confirmation/MergePolicy 与 Brief/Evidence/Eval exact refs；输出 server-owned inputHash、compilationHash、规范化 topo stage IDs 与 compiler version。
3. 编译器按稳定 stageId tie-break 的拓扑序编译，拒绝环、未知依赖、schema 不兼容、缺失 slot、assignee/capability 缺口与治理 ref 漂移；not-applicable 保留 canonical skipped step，不删除谱系。
4. Plan risk 中保存不可变 productionContract dependency snapshot；W2-D start gate 与 TaskStore 只接受完整 `w7c.v1` envelope，并复验 context/plan/input/compilation hash 后在既有同事务路径创建唯一 queued TaskRun。
5. Web SDK/parser 与生产合同页展示编译 hash、适用/跳过 Stage 和“不启动任务”的边界；页面写入口继续只生成 draft Plan。
6. 覆盖确定性、拓扑顺序、环/未知依赖、schema、capability/assignee、skip、治理 refs、漂移、幂等、跨租户和单一 TaskRun；再执行累计后端、Web 全量/build、OpenAPI/Router、安全与内置浏览器三视口验收。
7. 形成 Evidence、Delivery Receipt、安全提交、authority CAS 与 Prime 回读后自动进入 W7-04。

预计代码范围：

- `services/aos-api/aos_api/aip_contracts.py`
- `services/aos-api/aos_api/aip_production_contracts.py`
- `services/aos-api/aos_api/aip_production_contract_store.py`
- `services/aos-api/aos_api/aip_production_start_service.py`
- `services/aos-api/aos_api/aip_task_store.py`
- `services/aos-api/tests/aip/test_w7_03_stage_template_compiler.py`
- `services/aos-api/tests/aip/test_w2c_contracts.py`
- `services/aos-api/tests/aip/test_w2d_start_gate.py`
- `apps/web/src/api/aipProductionContracts/contracts.ts`
- `apps/web/src/api/aipProductionContracts/parser.ts`
- `apps/web/src/api/aipProductionContracts/parser.test.ts`
- `apps/web/src/pages/s2/ProductionContractsPage.tsx`
- `apps/web/src/pages/s2/ProductionContractsPage.test.tsx`
- `packages/contracts/openapi/v1.generated.json`
- `packages/contracts/openapi/v1.inventory.json`
- `scripts/export_openapi.py`
- `services/aos-api/tests/test_openapi_contract.py`
- `services/aos-api/tests/test_domain_router_manifest.py`
- `.evidence/workshop/2026-08-25-w7-03-stage-template-compiler-taskrun.json`

若实现中必须扩大范围，先回写本 ADR 与 Task Lease，再改代码。

## 2026-08-25 累计回归基线修复说明

累计回归独立发现两项测试基线需要随当前 authority 合同同步，均不改变运行语义：

1. `ExactContractRef` 新增为 OpenAPI schema 后，确定性 schema 数量由 2313 增至 2314；只更新结构计数基线，route 数量保持 2641。
2. 既有 W2-C review-return 测试夹具仍引用 `EvalRuleRevision/rule-w2c@1`，但没有插入已经强制校验的 `aip_review_rule_revision` authority。修复夹具为显式插入 exact rule，不删除或绕过 `_require_review_rule` 失败关闭。

两项均位于开工前已登记的文件范围：

- `services/aos-api/tests/aip/test_w2c_contracts.py`
- `services/aos-api/tests/test_openapi_contract.py`

## 2026-08-25 交付闭环

W7-03 已按本 ADR 完成，且在最终一致性复审中补齐了 start gate 对 `inputHash` 的独立复算：组合门现在同时复算治理依赖输入摘要与 Plan 结构摘要，替换 `governedDependencies`、Stage/Plan/Context exact refs、规范化 Stage 集合或 Plan step/dependency 均会失败关闭。

验收事实：

1. 后端专项与累计 `66 passed + 2 subtests`；稳定拓扑、环/未知依赖、schema compatibility、治理 exact refs、assignee/capability、canonical skip、input/compilation hash 与 start gate 漂移均覆盖。
2. Web 专项 `35 tests`、全量 `232 files / 2133 tests`、TypeScript 与 build `344 modules` GREEN；OpenAPI/Router artifact 为 `2641 paths / 2314 schemas / 4412 operations`。
3. 内置浏览器受控 fixture 在 768/1440/1920 三视口无横向溢出；治理输入锁定提示可见，编译草稿按钮可用但未点击，ProductionStart 仍禁用，console error 为 0。
4. Alembic 保持单 head `w7_001` 且未 apply；16 个本波文件安全扫描 `0 critical / 0 warning`。全仓安全门仍有历史基线 `5 critical / 326 warning`，不冒充全仓 GREEN，也不扩大本波代码范围处理。
5. 未修改真实租户数据，未审批 Plan，未创建 TaskRun，未调用 Provider，未生成媒体，未安装、发布或上线。

证据：`.evidence/workshop/2026-08-25-w7-03-stage-template-compiler-taskrun.json`。结论：`W7_03_STAGE_TEMPLATE_PLAN_COMPILER_CODE_CONTRACT_BROWSER_GREEN_SECURITY_SCOPED_GREEN_REPO_BASELINE_RED_NO_EXTERNAL_EFFECT_NO_RELEASE`，交付闭环后自动进入 W7-04。
