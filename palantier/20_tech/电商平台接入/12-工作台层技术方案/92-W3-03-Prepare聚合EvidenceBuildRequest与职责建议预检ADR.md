# W3-03 Prepare 聚合、EvidenceBuildRequest 与职责建议预检 ADR

> 日期：2026-08-15；实施刷新：2026-08-24
> Authority：`AOS-000212 / S3_W3_02_EXACT_PROFILE_CANDIDATES_CODE_GREEN_S3_IN_PROGRESS_NO_RELEASE`
> 状态：`COMPLETED_CODE_CONTROL_GREEN / NO_RELEASE / MIGRATION_NOT_APPLIED / NO_EXTERNAL_EFFECT`
> 边界：只读核验已提交代码、共享 authority 与方案；不读取 w1-aip 未提交内容，不修改代码、数据库或租户数据。

## 1. 结论

W3-03 的产品方向成立，但当前不能进入运行态编码。已提交基线有 TaskBrief、EvidenceBundle、EvalContract、ResponsibilityPlan 的公共 revision authority，也有 Workshop module list/readiness 只读入口；尚不存在电商 `prepare` 聚合、Evidence build-request authority、installed signed responsibility-profile resolver 或聚合 PreparationReceipt。

更重要的是，原方案中的“构建 Evidence、解析职责”容易被误实现为隐藏执行。本 ADR 将其收敛为：

1. prepare 可创建或 CAS 修订 draft TaskBrief，但不 freeze；
2. prepare 只创建 EvidenceBuildRequest，不启动实际异步/Provider Evidence Job，也不把 request 冒充完成的 EvidenceBundle；
3. prepare 生成 ResponsibilityRecommendation，不直接写成用户已接受的 ResponsibilityPlan；
4. 三项结果由服务端聚合并返回同一 PreparationReceipt，前端不串调拼成功；
5. prepare 始终保持 0 provider fee、0 TaskRun/AgentRun、0 Action/Handoff、0 Approval/ExecutionLease 与 0 外部业务动作。

## 2. 当前真实基线

| 能力 | 当前事实 | W3-03 判定 |
|---|---|---|
| TaskBrief | create/revise/freeze/get/list、PostgreSQL Store、Canonical API 存在 | 可复用；prepare 只用 create/revise |
| EvidenceBundle | 可从已经选定的 exact Evidence refs 创建不可变 Bundle | 不能替代 build request；无自动构建语义 |
| EvalContract/ResponsibilityPlan | 公共 revision authority 存在 | 可复用；profile resolver/建议层缺失 |
| AIP Web SDK | 公共 production-contract strict SDK 基础存在 | 尚无 EvidenceBuildRequest/Recommendation/prepare operation |
| Workshop API | 只有 modules list/readiness | command route 不存在 |
| BIND1_2 | CapabilityBinding readiness 真实性增强 | 真实 Binding=0、Agent 不 runnable；不补 profile/prepare |
| 上游任务 | W2-10、W3-01、W3-02 均未 GREEN | 硬阻断运行态编码 |

## 3. 唯一目标接口

```text
POST /v1/ecommerce-workshop/modules/{moduleId}/commands/prepare
operationId: ecommerceWorkshopPrepare
```

TenantScope 只来自认证 Principal。请求必须携带 Idempotency-Key；修订既有 Brief 时还带 expected version/If-Match。body 只携带 module、command、typed Brief spec 或 draft Brief exact ref、subject/object snapshot refs、purpose/marking/cutoff、installed Evidence-selection/required-facts/Responsibility profile exact refs，以及 workload/output/risk/budget/due-at。禁止 org/project 注入、Provider 凭据、ProtectedContact 明文和任意未解析 Bundle path。

成功或阻断响应必须包含：

- draft TaskBrief exact ref 与语义 Diff；
- EvidenceBuildRequest exact ref、`queued/blocked/satisfied/unknown` readiness，以及已有 canonical Evidence refs、missing/conflict/uncertainty/freshness/license blockers；
- ResponsibilityRecommendation exact ref、coverage、uncovered slots、候选 assignee exact refs 与 readiness blockers；
- PreparationReceipt exact ref、request hash、replay 标志、输入/输出数量守恒；
- `nextAllowedCommands`，未满足 reviewable 条件时 freeze 明确 disabled。

## 4. 三类对象不能混同

### 4.1 EvidenceBuildRequest 不是 EvidenceBundle

Request 保存 required facts、selection profile、subject refs、cutoff、purpose/marking、licensed source requirements 与已知缺口。prepare 可纳入租户内已经 canonical 且许可/freshness/cutoff 有效的 Evidence；需要采集、检索、生成或 Provider 的事实只保持请求/阻断。实际 Evidence Build Job 属于 W4-01，必须经过自己的授权、capacity/budget/route 和 Receipt 门。

只有构建完成并经 exact refs、coverage、missing/conflict/uncertainty、license/marking 校验后，才创建 EvidenceBundleRevision。`queued`、`partial` 或 `unknown` 不得映射 complete。

### 4.2 ResponsibilityRecommendation 不是 ResponsibilityPlan

Recommendation 保存签名 profile exact ref、职责槽覆盖、候选 assignee/capability readiness、merge 建议和硬分离规则。它是可解释建议，不代表用户确认、责任已分配或 Agent runnable。只有用户确认或 canonical policy 通过后，才能调用公共 authority 创建/修订 ResponsibilityPlan；独立审核、合规、批准和结果对账职责不得被 merge 吞掉。

### 4.3 Draft Brief 不是 Frozen Brief

prepare 仅 create/revise draft，并返回 Diff。freeze 由 W3-04 独立执行，CAS 固定 Brief/Evidence/Eval/Responsibility 四个 exact refs；prepare 不解析 latest、不自动 freeze，也不因为 profile 默认值补齐就跳过人工确认。

## 5. 原子性、幂等与 unknown

优先由同一服务端事务创建三项 revision 与 PreparationReceipt。若公共 authority 跨服务，先持久化 preparation intent/outbox，再由幂等 reducer 收敛；任何 crash window 都能按 commandId + Idempotency-Key + request hash 回读。

- 同 key + 同 hash：返回相同 Receipt 与 exact refs；
- 同 key + 异 hash：`WORKSHOP_IDEMPOTENCY_CONFLICT`；
- expected version 失配：`WORKSHOP_REVISION_CONFLICT` + Diff；
- dependency timeout：保持 `unknown` + reconcile ref，不重交、不换 key；
- partial/unknown：不点亮 freeze，不用 latest 或旧缓存兜底。

## 6. 零副作用硬门

prepare 的服务与测试必须证明：

```text
providerInvocationCount = 0
providerFee = 0
taskRunCreatedCount = 0
agentRunCreatedCount = 0
actionOrHandoffCreatedCount = 0
approvalOrExecutionLeaseCreatedCount = 0
externalBusinessMutationCount = 0
```

外部业务变更包括联系达人/客户、发布媒体/内容、创建订单/物流、修改价格/库存/会员、占用外部配额。Secret、Cookie、ProtectedContact 与未脱敏正文不得进入请求、响应、日志或 Receipt。

## 7. 四层所有权

- L0/AIP：拥有公共 Brief/Evidence/Eval/Responsibility revision；若 EvidenceBuildRequest 跨领域通用，也由 L0 提供唯一 authority；Agent/Capability/Binding readiness 仍归 AIP。
- L1/Workshop：拥有电商 prepare 聚合、typed profile 解释、领域 blocker 与 recommendation 投影；只能调用 canonical authority，不复制 Store。
- L2 Adapter：只报告 licensed source/provider capability readiness；prepare 阶段不执行外部动作。
- L3 Overlay：只贡献允许范围内默认值、预算与 assignee 偏好；不能删除硬职责或把 blocker 改成 ready。

## 8. 两轮审查与整改

### 第一轮：语义与副作用审查

发现原“构建 Evidence、解析职责”没有明确区分 request/result 和 recommendation/authority，存在隐藏 Provider 执行、前端拼成功、建议自动落为责任计划的风险。整改后新增 EvidenceBuildRequest、ResponsibilityRecommendation、PreparationReceipt 三个明确角色，并把实际 Evidence Job 路由至 W4-01；结论 `PASS_AFTER_REMEDIATION`。

### 第二轮：authority、并发与失败态反查

反查当前 Store/router/Web SDK 后确认：现有 EvidenceBundle create 要求调用者已给出 item refs，不能承担 Evidence 构建；Workshop router 也没有 command endpoint。整改进一步冻结 server-side aggregate、intent/outbox/reducer、同 key 重放、unknown/reconcile、数量守恒和 exact ref 不升 latest；并明确 BIND1_2 只提供 readiness 进展，不使依赖 GREEN。结论 `PASS_AFTER_REMEDIATION`。

## 9. 开工与退出门

编码前必须全部满足：

1. W2-10、W3-01、W3-02 GREEN；
2. EvidenceBuildRequest 与 ResponsibilityRecommendation（或经评审的等价唯一 authority）合同、Store、API、OpenAPI、strict SDK GREEN；
3. installed signed profile exact resolver 与八 Module non-placeholder profile refs GREEN；
4. prepare 原子性/幂等/重启回读/跨租户/stale/conflict/partial/unknown 测试 GREEN；
5. `org-org/dev-project` 正向和 `dev-org/dev-project` 负向证据证明全部零副作用计数；
6. 开工前重新核验 authority、01/06、Git、Delivery Receipt、memory gate 与 Lease。

机器证据：`.evidence/workshop/2026-08-15-w3-03-prepare-aggregate-preflight.json` 与 `.evidence/workshop/2026-08-15-w3-03-prepare-aggregate-doc-ledger.json`。当前 W3-03 保持未勾选；方案预检通过不等于运行态实现完成。

## 10. AOS-000212 实施刷新与当前波文件级清单

2026-08-24 按 `m1@878806f / AOS-000212` 重核，历史阻断需要重新分类：

1. W2-10、W3-01、W3-02 的代码/控制门已 GREEN，“上游均未 GREEN”不再是开工阻断。W3-02 候选 Bundle 仍 `NO_RELEASE`，所以默认运行必须因未安装 exact profile 失败关闭，但不阻断合同、持久化与纯聚合服务的开发。
2. 公共 `BuildEvidenceBundleRequest`/`build_evidence_bundle` 已存在，但它要求 frozen Brief 并立即创建 immutable `EvidenceBundleRevision`；这不能替代 prepare 阶段针对 draft Brief 的 `EvidenceBuildRequest`，prepare 不得调用该 Build Job。
3. `InstalledProductionProfileResolver` 已具备 tenant installation/composition lock/published signed digest 联合校验；W3-03 只对其补充受控 profile resource-type 覆盖，不另建解析真源。
4. 目前仍没有 `EvidenceBuildRequest`、`ResponsibilityRecommendation`、`PreparationReceipt` 的唯一持久化 authority，也没有 `ecommerceWorkshopPrepare`。本波不用内存 cache 伪装持久化，而是用 additive migration 定义 tenant-RLS preparation intent/result；只交付迁移代码与测试，不对任何真实数据库执行 migration。

### 10.1 实施切片

| 切片 | 文件 | 最小改动 |
|---|---|---|
| W3-03A | `services/aos-api/aos_api/ecommerce_workshop_prepare_contracts.py` | strict request/result，明确 draft Brief intent、EvidenceBuildRequest、ResponsibilityRecommendation、PreparationReceipt 四者边界 |
| W3-03A | `services/aos-api/alembic/versions/w3_013_workshop_preparation.py` | 新增 append-oriented tenant-RLS preparation intent/result authority；仅 migration code，不执行 live apply |
| W3-03A | `services/aos-api/aos_api/ecommerce_workshop_prepare_store.py` | 按 tenant + operation + Idempotency-Key + request hash 持久化 pending/final result，同 key 异 hash 冲突 |
| W3-03B | `services/aos-api/aos_api/ecommerce_workshop_prepare_service.py` | 先写 intent，再幂等 create/revise draft Brief，生成 request/recommendation，最后固化 Receipt；不 build Evidence、不写 ResponsibilityPlan |
| W3-03B | `services/aos-api/aos_api/routers/ecommerce_workshop.py` | 新增唯一 `POST /modules/{moduleId}/commands/prepare`，tenant 只来自 Principal，必须 Idempotency-Key |
| W3-03C | `services/aos-api/tests/test_ecommerce_workshop_prepare.py` 及 migration/OpenAPI 专项 | 覆盖 replay/conflict、create/revise、跨租户、stale exact ref、unknown 恢复、0 provider/run/action/handoff/approval/lease/business write |
| 证据 | `.evidence/workshop/2026-08-24-w3-03-prepare-aggregate.json` | 记录专项、累计、浏览器、方案一致性与副作用守恒 |

### 10.2 实现不变式

- `EvidenceBuildRequest` 只记录 required facts、已有 canonical Evidence refs 与 blocker；不创建 `EvidenceBundleRevision`。
- `ResponsibilityRecommendation` 保留 protected slot，只输出候选 assignee/readiness；不创建 `ResponsibilityPlanRevision`。
- draft Brief 只 create/revise，不 freeze；任意 partial/blocked/unknown 不允许 `freeze`。
- 聚合返回 `providerInvocationCount/taskRunCreatedCount/agentRunCreatedCount/actionOrHandoffCreatedCount/approvalOrExecutionLeaseCreatedCount/externalBusinessMutationCount = 0`，且不接收 secret/cookie/protected-contact 字段。
- 保持 163/164 链路：职责建议的 slot 只引用原子 Skill，Logic/数字同事 exact binding 是 readiness 条件，工作台只投影贡献与 blocker。

### 10.3 实施与验收结论

2026-08-24 已按上述文件清单完成 W3-03 代码/控制门实现，结论为：

- 唯一 `ecommerceWorkshopPrepare` 由服务端聚合，tenant 只取 Principal，`Idempotency-Key + request hash` 形成持久化重放边界；同 key 异请求冲突。
- preparation intent 的身份和请求字段不可变，只允许 `pending → complete/unknown`；result revision=1 且 append-only。迁移保持 `w3_013 (head)`，本波未对任何真实数据库执行 migration。
- installed `ProductionProfileRevision` 通过单次 Registry 快照校验 active installation/composition lock/published signature/digest，再从 immutable release mirror 回读并复核内容哈希，消除双查询竞态。
- prepare 只 create/revise draft Brief；EvidenceBuildRequest 对未能规范解析的 required facts 明确 `blocked`；ResponsibilityRecommendation 保留 `atomicSkillIds`、protected review 与 binding blocker。没有 build Evidence、freeze Brief、写 ResponsibilityPlan 或创建执行对象。
- 专项 prepare/store 8/8、resolver/migration/router/OpenAPI 组合 35/35、Workshop 累计 145/145、Python compile 与 diff check 均 GREEN。
- 内置浏览器 `/workshop` 正常渲染既有工作台；`aos-api` 不可达与目录读取失败明确可见，active installation=0，未把 W3-03 或未发布 Profile 候选伪装成可执行能力。

机器证据：`.evidence/workshop/2026-08-24-w3-03-prepare-aggregate.json`。

状态更新为 `COMPLETED_CODE_CONTROL_GREEN / NO_RELEASE / MIGRATION_NOT_APPLIED / NO_EXTERNAL_EFFECT`。该结论允许进入 W3-04 代码/控制门，不等于运行态、迁移、Profile 发布安装或生产发布授权。
