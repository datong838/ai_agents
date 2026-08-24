# W3-04 四合同 ProductionContext 组合冻结与依赖解环 ADR

> 日期：2026-08-15
> Authority：`AOS-000214 / S3_W4_01_EARLY_EVIDENCE_BRIDGE_CODE_GREEN_S3_IN_PROGRESS_NO_RELEASE_MIGRATION_NOT_APPLIED`
> 状态：`IMPLEMENTATION_PLAN_GREEN / W3-04_SERIAL_IMPLEMENTATION_IN_PROGRESS / NO_RELEASE`
> 范围：在既有 W-L11 ProductionContext L0 authority 上增量补齐 exact ProductionProfile 留痕，并新增 Workshop typed freeze adapter；不执行迁移、发布或真实业务副作用。

## 1. 结论

W3-04 的“四个 exact refs”必须是一次可回读的用户确认事实，而不是四个单对象 freeze 调用的前端组合。当前 AIP 已有单对象 freeze 和 compile 后的 frozen ImpactPreview，但没有 pre-compile 四合同 aggregate；旧 D-waves 还存在 Evidence Build 循环依赖。因此 W3-04 方案必须先解环，并新增 AIP L0 owner 的 `ProductionContextRevision`（若最终采用等价名称，语义不得弱化）。

## 2. 旧依赖为何不可执行

旧边形成循环：W3-04 需要 EvidenceBundle；W3-03 只创建 EvidenceBuildRequest 且禁止隐藏 Provider 执行；W4-01 才构建 Bundle，却依赖 W3-14；W3-14 又依赖 W3-04 及后续任务。

现有 ImpactPreview 也不能直接补洞：它要求 PlanRef、StageTemplateRef，并承载 Route/Policy/Binding/Account/Impact 等后续依赖；而产品顺序要求用户先确认四合同，再由 compiler 生成 Plan。把 ImpactPreview 前移会反转用户确认与编译顺序。

## 3. 解环后的唯一顺序

```text
W3-03 prepare
  → W4-01 early Evidence Build bridge
  → 用户/策略确认 Eval 与 Responsibility
  → W3-04 ProductionContext freeze
  → W3-05 canonical compile
  → ImpactPreview + ActionProposal/Approval
  → Production start
```

W4-01 只作为 W3-04 的 early bridge 提前，不开放 W4-02～08；后者继续受 W3-14 与各自安全门约束。

## 4. ProductionContext 唯一契约

目标对象只保存 exact refs 与安全 provenance：

- TaskBriefRevision：frozen、typed schema 与 active installation provenance 有效；
- EvidenceBundleRevision：complete/fresh，missing/conflict/uncertainty 按 profile 无阻断；
- EvalContractRevision：frozen，publication/rules/artifact schema 当前有效；
- ResponsibilityPlanRevision：frozen、complete/ready，独立职责未被合并吞掉；
- PreparationReceipt、production profile、installation lock exact refs；
- dependencySnapshotHash、contentHash、actor/time、lifecycle 与 blockers。

ProductionContext 不复制四对象 payload，不包含 Plan、Stage、Impact、Approval、Action 或 Run 状态。它由 AIP L0 common production contracts 持有；Workshop 只提供 `ecommerceWorkshopFreeze` typed adapter 和投影。

## 5. CAS、幂等与失败态

服务端在同一 TenantScope 和一次决定中重读四 refs，并验证 type/id/revision/hash/lifecycle/readiness/profile/publication/revocation。相同 key + hash 重放同一 Context/Receipt；相同 key + 不同 hash 冲突；expected version 不符返回 Diff。任何 missing、partial、conflict、stale、revoked、expired、unknown、placeholder、dry-run、跨租户或 profile mismatch 都不得发布半成品。

若跨 Store 无法共享事务，先写 freeze intent/outbox，由 reducer 产生唯一 Context；commit 前 crash 不可见，commit 后 crash 通过 Receipt 回放。不得以补偿删除历史或换 latest 修复。

## 6. 与 compile、ImpactPreview、start 的传递

canonical compiler 必须消费 frozen ProductionContext exact ref，并把它写入 Plan risk/production contract。ImpactPreview 再固定 Plan、StageTemplate、ProductionContext 与 runtime/impact dependencies；ActionProposal/Approval 和 StartDecision 继续引用该 Preview，并能反查同一 ProductionContext。任一四合同或 profile 失效都通过 snapshot 传播 stale，不能改写旧 Context。

## 7. 两轮审查与整改

第一轮依赖审查发现 W3-04↔W4-01/W3-14 循环，以及 prepare 零副作用与 Bundle 输入不相容。整改：W4-01 改为 W3-03 后 early bridge，W3-04 显式依赖 W4-01；结论 `PASS_AFTER_REMEDIATION`。

第二轮 authority/顺序反查发现 frozen ImpactPreview 虽复验四合同，却要求 compile 后 Plan/StageTemplate，不能代表编译前用户确认。整改：新增 `DEP-PRODUCTION-CONTEXT-FREEZE`，冻结独立 pre-compile aggregate，并规定向 Plan/Preview/Start 的 exact ref 传递；结论 `PASS_AFTER_REMEDIATION`。

## 8. 2026-08-24 实施复核

独立回读确认此前“L0 authority 缺失”已经过时：`FreezeProductionContextRequest`、`ProductionContextRevision`、PostgreSQL append-only/RLS Store、freeze/get/list API、OpenAPI 与 W-L11 精确引用测试均已存在；W3-03 与 W4-01 early bridge 也已分别在 `AOS-000213`、`AOS-000214` 关闭代码控制门。因此本波不重建第二套 ProductionContext 真源，只关闭以下真实缺口：

1. 现有 Context 只保存 `profile: string`，无法证明冻结时消费的是哪个已安装 `ProductionProfileRevision` exact ref；
2. Workshop 尚无 `ecommerceWorkshopFreeze` typed command，客户端仍可能自行拼装 preparation、Profile 与四合同；
3. PreparationReceipt 尚未由服务端按 preparation result hash 形成 exact ref 并写入 Context；
4. 缺少 Workshop 适配层对 module、prepared Brief、EvidenceBundle Brief lineage、required facts 与 active installation Profile 的原子复验。

采用向后兼容的增量方案：给 L0 request/response/Store 增加可选 `productionProfileRef`，并用新 append-only schema migration 增加 nullable JSONB 列；历史调用与历史行保持可读。Workshop adapter 则强制该 exact ref 必填，并只接受服务端回读的 Preparation 与 active installation Profile。L0 继续原子重读四合同，Workshop 不复制 L0 状态机。

## 9. 当前波文件级施工清单

- 方案与追踪：本 ADR、D-waves 总清单；
- L0 additive contract/store/schema：`services/aos-api/aos_api/aip_production_contracts.py`、`services/aos-api/aos_api/aip_production_contract_store.py`、新 Alembic revision；
- Workshop typed adapter：新增 freeze contracts/service，并在 `ecommerce_workshop.py` 暴露唯一 command；
- 生成物：domain router manifest、OpenAPI 与对应确定性基线；
- 测试：L0 Profile exact ref 留痕、Workshop 成功/幂等、跨租户、Profile 漂移、Preparation/Bundle lineage 漂移与零副作用；累计回归不得少于当前 W4-01 的 169 项集合；
- 页面：本波不新增可执行按钮；浏览器只验收现有页面仍失败关闭、无越权 command、无横向溢出。

## 10. 不变量与完成门

freeze 本身保持 0 Provider、0 Run、0 Action/Handoff/Approval/Execution Lease、0 Plan compile、0 发布和 0 外部业务副作用。不得解析 latest、不得接收客户端自报 readiness、不得把 `profile` 文本当 exact Profile、不得以 Context ready 冒充可 start。代码、专项/累计测试、OpenAPI/manifest、浏览器、Receipt、authority CAS 与 Prime 回读全部闭合后才可勾选 W3-04。

历史预检机器证据：`.evidence/workshop/2026-08-15-w3-04-four-ref-freeze-preflight.json` 与 `.evidence/workshop/2026-08-15-w3-04-freeze-cycle-remediation-doc-ledger.json`；本次实施 EvidencePack 使用新的 2026-08-24 cutoff，不覆盖历史证据。

## 11. 2026-08-24 实施验收

W3-04 已在代码控制面完成。新增的 `ecommerceWorkshopFreeze` 只接收 preparation ID、exact ProductionProfile/EvidenceBundle/EvalContract/ResponsibilityPlan refs；服务端回读 canonical Preparation、active installation Profile、Bundle→Brief lineage 与四合同，再调用唯一 L0 `freeze_production_context`。L0 同时保存 exact Profile，并在 dependency snapshot 中记录 active-installation 解析结果；未解析的 Profile 以 `PRODUCTION_PROFILE_MISSING_OR_DRIFTED` 失败关闭。

专项组 `34 passed + 2 subtests`，累计组 `176 passed + 2 subtests`；OpenAPI 为 `2570 paths / 2123 schemas / 4338 operations`，确定性导出 GREEN，唯一 migration head 为 `w3_014`。内置浏览器在 `/workshop` 验收 `1280 == scrollWidth`、单 H1、active installation 0、aos-api 不可达事实显式、Freeze/Evidence/Production 可执行按钮 0。机器证据：`.evidence/workshop/2026-08-24-w3-04-production-context-freeze.json`。

结论为 `COMPLETED_CODE_CONTROL_GREEN / NO_RELEASE / MIGRATION_NOT_APPLIED / NO_EXTERNAL_EFFECT`。下一任务是 W3-05；本结论不代表生产迁移、Module/Profile 安装、运行态 start 或发布 GREEN。
