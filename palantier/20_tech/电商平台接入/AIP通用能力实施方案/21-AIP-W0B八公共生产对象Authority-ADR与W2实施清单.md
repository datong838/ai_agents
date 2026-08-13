# AIP-W0B 八公共生产对象 Authority ADR 与 W2 实施清单

> 状态：`APPROVED_FOR_W2_IMPLEMENTATION`
> 日期：2026-08-13
> 上位输入：16 号全量支撑审查、17 号 W0 增量方案、18 号 W0A Crosswalk、工作台技术方案 23
> 实时代码基线：`aos-platform/m1@914cff2`
> 唯一真实范围：`org-org/dev-project`
> 负向隔离 canary：`dev-org/dev-project`

## 1. 使用的 Rules

1. 只扩展 AIP/L0 authority；Workshop、BFF、Bundle、YAML 和前端不得持有第二真源。
2. 复用已 GREEN 的 Task/Plan/Run/Step/Checkpoint、Evidence、Artifact、Eval、Action、Receipt、Lineage、Agent authority，不重建同义运行表。
3. revision 追加不可变；mutable aggregate 使用 expected-version CAS；mutation 使用 Principal tenant、Idempotency-Key 和 durable Receipt。
4. 所有租户表包含 `org_id/project_id`，启用 RLS/FORCE RLS；客户端 body 不接受租户覆盖。
5. exact ref 必须固化 resource type/id/revision/hash；跨租户、缺 revision/hash、漂移、撤回和 stale 均失败关闭。
6. `prepare → freeze → start → approve → execute → reconcile` 分离；freeze 不等于启动，preview 不等于批准，页面成功不等于外部执行成功。
7. W2 按最小垂直切片实施，每片均需迁移、Store、Service、Canonical API、严格 SDK、浏览器/负向证据和独立提交。

## 2. ADR 总结

| 对象 | ADR 裁决 | Canonical owner | W2 实现形态 |
|---|---|---|---|
| TaskBriefRevision | additive | AIP Task/Plan | 新增 immutable revision + mutable head；exact 绑定 Task |
| EvidenceBundleRevision | additive manifest | AIP Evidence/Artifact | 新增 immutable bundle manifest，只聚合 exact refs，不复制正文 |
| EvalContractRevision | additive wrapper | AIP Eval | 新增单任务 exact binding，复用 EvalSuite/Publication/Run/Report |
| ResponsibilityPlanRevision | additive | AIP Agent/Plan | 新增 immutable slot/assignee/coverage authority |
| StageTemplate | compiled projection | AIP Plan compiler | 新增签名模板目录/编译服务；不新增 StageRun 表 |
| Artifact family/Variant | additive relation | AIP Artifact/Lineage | 新增 append-only relation，不复制 Artifact payload |
| ReviewIssue/ReturnDecision | additive event | AIP Eval/Run | 新增 issue aggregate + append-only return event；复用新 Step attempt/Artifact |
| ImpactPreview | additive immutable revision | AIP Action | 新增 preview revision；ActionProposal exact 强绑定，drift 失效 |

明确禁止：`ProductionRun`、`StageRun`、`EvidencePayload`、`EvalRun`、`ProviderResult`、`ArtifactPayload` 的第二套 authority。

## 3. 共同引用与状态契约

### 3.1 ExactRevisionRef

统一复用/兼容现有 `ResourceRef`，W2 对可变业务契约要求：

```json
{
  "resourceType": "TaskBriefRevision",
  "resourceId": "brief-opaque-id",
  "revision": "3",
  "contentHash": "64-lowercase-sha256"
}
```

- `contentHash` 以 canonical JSON 计算；禁止前端计算并覆盖服务端结果。
- mutable head 只保存当前 revision/version，不保存可编辑正文副本。
- Run/Proposal/Approval 一旦引用，必须固化 exact ref；head 后续变化不回写历史。

### 3.2 共同状态

- draft revision：可由新 revision 取代，不允许原地修改。
- frozen：不可改写；依赖漂移只改变派生 readiness，不改写历史。
- withdrawn/superseded：追加事件/新 revision 表达；物理删除禁止。
- readiness：`ready / blocked / stale / unknown`，原因码为稳定机器值。

## 4. 八对象逐项 ADR

### 4.1 TaskBriefRevision

**复用**：`aip_task` identity/version、PlanRevision、ResourceRef、Receipt。

**新增**：

- `aip_task_brief_revision(org_id, project_id, brief_id, revision, task_id, brief_type, schema_ref, spec, content_hash, lifecycle, created_by, created_at)`；唯一键 tenant+brief+revision。
- `aip_task_brief_head(org_id, project_id, brief_id, current_revision, version, updated_at)`；CAS 只推进 head。
- API：create draft、create next revision、get/list revisions、diff、freeze/withdraw。

**失败语义**：unknown brief type/schema、Task 跨租户、stale expected version、hash drift、frozen overwrite 均稳定 4xx；freeze 不创建 TaskRun。

### 4.2 EvidenceBundleRevision

**复用**：`aip_evidence` 正文/来源/新鲜度、`aip_artifact`、ObjectSnapshot/ResearchJob/Receipt refs。

**新增**：

- immutable bundle revision：subject/brief exact ref、cutoff、items、coverage、missing、conflicts、uncertainties、freshness verdict、marking/license summary、content hash。
- build command 可创建现有 Task/Job；完成时由服务端从已授权 refs 固化 manifest。

**禁止**：复制 Evidence payload、把未知 count 写为 0、用摘要冒充事实。撤回/过期使 readiness stale/blocked，但历史 bundle 保留。

### 4.3 EvalContractRevision

**复用**：`aip_eval_suite_revision`、publication/release gate、EvalRun、EvalReportRevision。

**新增**：单任务 wrapper，保存 exact suite/publication refs、artifact schema、severity/threshold/gate/return mapping、override policy 和 hash。

Run start 时固定 exact contract；同一 Run 中禁止静默换标准。Suite 撤销/未发布、schema 不兼容、GoldSet/provider 未就绪均 blocked。

### 4.4 ResponsibilityPlanRevision

**复用**：AgentInstance、Skill/CapabilityBinding、PlanStep、HandoffEnvelope。

**新增**：

- plan revision：profile、template exact ref、slots、merge decisions、uncovered slots、content hash。
- slot：stable slot ID、responsibility type、required capability IDs、input/output contracts、gate refs、return stage、assignee exact ref。
- assignee kind：AgentInstance/HumanPrincipal/ToolBinding/ProviderCapabilityBinding；显示名不能作为 identity。

freeze 前检查 coverage；start 前复验 binding/readiness/policy。合并不能吞并独立审核、硬合规、外部发布批准和 Receipt 对账。

### 4.5 StageTemplate compiler

**复用**：PlanRevision/PlanStep DAG、TaskRun/StepRun/Checkpoint。

**新增**：签名 StageTemplate revision 与受控 compiler；模板声明 dependsOn、applicability DSL、required slots、input/output schema、gate、checkpoint/retry/compensation policy。

compiler 输出 canonical PlanRevision；Stage UI 只投影 StepRun。禁止 `aip_stage_run` 第二表、运行时任意代码/Prompt、删除不适用 Stage 而不留 `not_applicable` 证据。

### 4.6 Artifact family/Variant

**复用**：append-only `aip_artifact` payload、ArtifactRef、Lineage。

**新增**：`aip_artifact_relation` append-only relation，relation type 固定为 `family_member / variant_of / supersedes / derived_from`，两端 exact Artifact refs、原因、actor、createdAt；不允许环和跨租户。

母稿与平台 Variant 是关系语义，不新建媒体内容表；修订创建新 Artifact，不原地覆盖 URI/hash。

### 4.7 ReviewIssue/ReturnDecision

**复用**：EvalReport、Evidence、Artifact、StepRun attempt、Handoff/Checkpoint。

**新增**：

- ReviewIssue aggregate：rule/severity、exact artifact/location/evidence refs、suggested fix、return stage、status/version。
- ReturnDecision append-only event：issue/version、target stage、reason、actor、new attempt idempotency key。

return 创建明确新 Step attempt；后续新 Artifact/EvalRun 沿 lineage 关闭或 supersede issue。禁止改写旧 Artifact/EvalRun/Issue 历史。

### 4.8 ImpactPreview

**复用**：ActionProposal、Draft diff/evidence、Approval、Lease、Receipt、Usage/Capability Receipt。

**新增**：immutable preview revision，保存对象/渠道范围、费用/预算、风险、可逆性、审批链、rate/capacity/kill、account/capability exact refs，以及每字段 measured/estimated/unknown 质量。

ActionProposal 必须 exact 引用 preview hash；依赖漂移后 Approval/Lease 失败关闭，重新 preview。Adapter timeout 为 unknown/reconcile，不允许盲重试或换账号。

## 5. Canonical API 边界

建议统一前缀 `/v1/aip/production-contracts`：

```text
POST/GET /task-briefs
POST /task-briefs/{id}/revisions
POST /task-briefs/{id}/freeze
POST/GET /evidence-bundles
POST/GET /eval-contracts
POST/GET /responsibility-plans
POST /responsibility-plans/{id}/freeze
POST /stage-templates/{id}/compile
POST /artifact-relations
POST/GET /review-issues
POST /review-issues/{id}/return
POST/GET /impact-previews
POST /production-runs/start
```

共同要求：Principal tenant、strict DTO、Idempotency-Key、If-Match/expectedVersion、canonical ref/Receipt、稳定错误码；GET 不 silent fallback，mutation 不进入 offline queue 后宣称成功。

`start` 只接受 frozen Brief/Evidence/Eval/Responsibility exact refs 和 StageTemplate exact ref；服务端复验 freshness/coverage/publication/coverage/readiness/budget 后编译现有 Plan/TaskRun。依赖未齐时返回 blocker，不创建半运行。

## 6. 迁移与 Store 分组

W2 不一次建立全部表，按四个线性迁移切片：

1. `w2_001_brief_evidence`：Brief revision/head、EvidenceBundle revision、command Receipt。
2. `w2_002_eval_responsibility`：EvalContract、ResponsibilityPlan revision/head。
3. `w2_003_stage_artifact_review`：StageTemplate revision、ArtifactRelation、ReviewIssue/ReturnDecision。
4. `w2_004_impact_start`：ImpactPreview revision、ActionProposal exact ref 扩展、start compiler binding。

每片迁移必须：单 head、独立 upgrade/downgrade、复合 FK、RLS/FORCE RLS、索引含 tenant 前缀、无默认测试数据；历史表只做 additive nullable/exact-ref 扩展。

## 7. W2 开发波次

### W2-A · Brief + Evidence

- DTO/迁移/Store/CAS/Receipt/API/严格 SDK；
- 在 `org-org/dev-project` 创建一份最小真实 Brief draft、freeze 与只引用现有 Evidence 的 Bundle；
- canary 为 0；不启动 Run。

### W2-B · Eval + Responsibility

- exact EvalSuite binding、severity/return policy；
- 以 A6F 六实例解析一份 ResponsibilityPlan，但在 Skill/Capability 未绑定时 freeze/readiness 诚实 blocked；
- 不用显示名或固定 10 Agent 代替 assignee ref。

### W2-C · Stage + Artifact + Review

- 受控 StageTemplate 编译为 PlanRevision；环、unknown expression、缺 slot 均失败；
- Artifact relation 无环/跨租户；Review return 产生新 attempt/lineage。

### W2-D · Impact + start 组合门

- Preview exact binding 与 drift invalidation；
- `production-runs/start` 组合校验；在 AIP-7/Provider/Binding 未就绪时只验收稳定 blocked，不伪造运行成功；
- AIP-7 GREEN 后再补真实 running E2E，不回改 W2 authority。

## 8. 测试与证据矩阵

- Contract：strict/unknown enum/hash/ref/schema/version；
- Store：RLS、CAS、append-only、restart readback、idempotency drift、复合 FK；
- Compiler：DAG、环、applicability、LITE/STANDARD/FULL、缺 slot/readiness；
- Integration：Brief→Bundle→Eval→Responsibility→Plan/Run→Artifact/Issue→Preview/Action 同一 lineage；
- Security：跨租户、撤回、stale、PII/Secret、license/provider unknown；
- Browser：loading/empty/forbidden/stale/failed/unknown/blocked、刷新恢复、disabled reason、console 0 error；
- Positive：只使用 `org-org/dev-project`；negative：`dev-org/dev-project` 始终不见正租户对象。

## 9. 回滚与风险

- 回滚应用代码不删除 revision/event/Receipt；可关闭 create/freeze/start feature gate，保留只读审计。
- 迁移 downgrade 只允许在尚无业务行的开发验证库；有业务行时使用前向补偿迁移。
- 最大风险是八对象一次性大爆炸和跨层第二真源；以 W2-A～D 独立提交/证据门控制。
- AIP-7 与 W2 是正交依赖：W2 可以先建立契约 authority，但没有 route/provider/eval/binding 时 start 必须 blocked。

## 10. 评审—整改—复审

### 10.1 首轮发现

| ID | 发现 | 级别 |
|---|---|---|
| R1 | 把 StageRun、Evidence payload、EvalRun 再建一套会形成第二真源 | BLOCKER |
| R2 | 八对象一次迁移/一次提交，失败域与回滚面过大 | BLOCKER |
| R3 | ResponsibilityPlan 若只存角色名，无法证明 exact assignee/binding | BLOCKER |
| R4 | ImpactPreview 若不与 Proposal/Approval 固定 hash，批准可被漂移 | BLOCKER |
| R5 | W2 若等待 AIP-7 才建 authority，会迫使上层继续临时造对象 | HIGH |
| R6 | W2 若绕过 AIP-7 启动 Run，会把 0 runnable 伪装成在线 | BLOCKER |

### 10.2 整改

- StageRun/正文/评估运行全部改为 typed projection/复用；只新增缺失 revision/relation/event。
- 拆为 W2-A～D 四个线性、可独立验证的切片。
- assignee 只接受 exact Agent/Human/Tool/Provider binding ref；显示名仅投影。
- Preview/Proposal/Approval/Lease 固定 exact hash，依赖漂移失效。
- W2 authority 可先实现，start 与 running 分别受 W2/AIP-7 双门约束。

### 10.3 第二轮复审

| 退出门 | 结果 |
|---|---|
| 八对象 owner 唯一，无 Workshop/BFF 第二真源 | PASS |
| 复用/投影/additive 边界逐项明确 | PASS |
| Store/API/RLS/CAS/幂等/失败/回滚可执行 | PASS |
| W2-A～D 依赖、提交和证据边界清楚 | PASS |
| 与 A6F/AIP-7/E7/AIP-8/9/10 顺序自洽 | PASS |
| 未把 authority GREEN 冒充 operational ready | PASS |

最终结论：`APPROVED_FOR_W2_IMPLEMENTATION`。首个安全编码切片为 W2-A；不授权跳过 AIP-7 阻断启动真实 AgentRun。
