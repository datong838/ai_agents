# W4-04 ReviewIssue、返工 Attempt 与 Lineage 闭环预检 ADR

> 状态：`RE-REVIEWED / IMPLEMENTATION_AUTHORIZED`
>
> 当前事实截面：AOS authority `AOS-000228`；任务 `workshop-w4-04-review-return-attempt-lineage-20260825`。

## 1. 审查结论

AIP W2-C 已提供可复用的 PostgreSQL authority：ReviewIssue create/list/get/resolve/return、append-only ReviewIssueEvent、ReturnDecision、新 queued StepRun attempt、旧 attempt 保留、ArtifactRelation exact hash 与有向防环。工作台不得复制这些 Store。

但 W4-04 尚不能编码或勾选，原因是“写入返工事实”尚未形成“可执行、可解释、可回读的返工闭环”：

1. return 允许从 `succeeded` attempt 返工并追加更高 attempt；Canonical TAOR 却把“任意历史 attempt 成功”视为该 step 已完成，因此新 queued attempt 可能被跳过。
2. return 只复制旧 `input_refs`，未将 Issue、ReturnDecision、修复 Artifact/Evidence 作为新 attempt 的 exact 输入，也未计算下游 Stage invalidation/reuse decisions。
3. `rule_ref` 以 exact ref 形态入库但没有对 Rule authority 做存在性/hash 校验。
4. resolve 接受 reason/resolution refs，却不验证 refs；事件仅保存 payload hash，没有 canonical 读取面，无法还原“为何解决、用什么证据解决”。
5. ReturnDecision 和 ReviewIssueEvent 没有 get/list API/SDK；Lineage 只有 TaskRun/StepRun，不包含 Issue、Decision 与 Eval/Evidence/Artifact 关系。
6. create/resolve/return 只有登录门，尚未看到明确 review/production-control 权限门。

## 2. 返工状态机

```text
ReviewIssue(open, exact artifact/eval/evidence/rule)
  → ReturnDecision(exact issue version + target stage + reason)
  → InvalidationSet(target + affected downstream stages)
  → ReuseDecision(each unaffected stage, exact input hash)
  → StepRun attempt N+1(queued, exact repair inputs)
  → ArtifactRevision N+1
  → same exact EvalContract rerun
  → ReviewIssue resolved or superseded
```

`returned` 只表示返工决定已持久化且新 attempt 已排队，不表示执行器已认领、修复已完成或问题已解决。

## 3. 必须补齐的 AIP 接缝

### 3.1 latest-attempt 执行语义

TAOR 对每个 `stepKey` 只以最大 attempt 为当前执行状态：

- latest=queued：必须可认领；
- latest=running：遵守 Lease/unknown/reconcile；
- latest=succeeded：才可视为该 step 当前完成；
- 旧 attempt 的 succeeded 只保留历史，不得遮蔽更高 attempt。

新增集成测试：attempt 1 succeeded → Review return → attempt 2 queued → TAOR 认领 attempt 2，而不是跳过。

### 3.2 invalidation 与精确输入

Return service 依据 Stage DAG 与 ArtifactRelation 生成 server-owned `InvalidationSet`。新 attempt 输入至少包含 exact Issue、ReturnDecision、源 Artifact、修复 Artifact/Evidence（如已有）和原合同；下游节点逐项记录 invalidate/reuse 及理由。禁止无解释地复制旧 input refs 后重跑。

### 3.3 Rule、Resolution 与读模型

- `ruleRef` 必须由可安装 Eval/Policy rule authority exact resolve；unknown/missing/drifted 失败关闭。
- resolution refs 必须按类型逐项验证，并持久化不可变的可读 event payload 或 exact payload artifact ref。
- 提供 Issue event timeline、ReturnDecision get/list 和 lineage read model；浏览器不拼装权威历史。

### 3.4 权限与并发

create issue 可由受信 Eval service identity 执行；resolve/return 需要显式 review/production-control permission。Return 与 Step claim 必须共用可证明的串行化边界，避免 executor 在返工写入中途认领旧状态。

## 4. 工作台呈现

工作台只消费 AIP read model，向用户展示：问题规则、严重度、证据、原产物、评价报告、目标 Stage、每次 attempt、无效化范围、复用决定、当前 assignee/Lease、修复产物和再评结果。处置按钮显示影响预览和权限结果；请求返回后以服务器回读状态为准。

## 5. 验收门

- succeeded attempt 后返工可真实执行 N+1；旧 attempt 不覆盖、不被误当当前。
- target 与全部受影响下游 Stage 的 invalidate/reuse 结果可解释、可回读。
- 新 attempt exact 输入包含 Issue/Decision/repair refs，同一幂等键只产生一次。
- rule/eval/evidence/artifact 任一 missing/drifted/跨租户均失败关闭。
- resolve 的 reason 和 resolution evidence 可通过 canonical timeline 回读并校验 hash。
- Lineage 可从 Issue 走到 EvalReport、ReturnDecision、Step attempts、Artifact revisions 和再评结果。
- 未授权主体不能 create/resolve/return，不泄露跨租户对象存在性。

## 6. 明确废弃与禁止

- 废弃“插入 queued StepRun 就等于返工链已完成”的判断。
- 禁止 TAOR 用任意历史 succeeded 判断当前 step 完成。
- 禁止只复制旧 input refs、没有 Issue/Decision/repair refs 的盲目重跑。
- 禁止以不可回读的 payload hash 代替完整的处置审计证据。
- 禁止 Workshop 自建 Issue/Decision/lineage Store 或在前端推导 invalidation。

这些废弃项删除的是断裂路径，不削弱“保留旧产物、追加新 attempt、同版再评、全过程可干预”的原产品目标。

## 7. AOS-000228 重审与本波实施清单（2026-08-25）

### 7.1 已由后续交付关闭的旧缺口

W-L14 已把 TaskRun 完成与 Step claim 改为“每个 step 仅看最新 attempt”，并在 return 的同一数据库事务中追加 N+1 queued attempt；新 attempt 已携带 ReviewIssue、ReturnDecision、Artifact 精确输入。ReturnDecision get/list API 及 Task Cockpit 的 Issue/Decision/attempt 只读关联也已存在。本波禁止重复实现这些能力。

### 7.2 仍需关闭的真实缺口

1. 新增不可变 `ReviewRuleRevision` 精确权威；create issue 必须校验同租户 id/revision/hash，unknown/drifted 失败关闭。
2. ReviewIssueEvent 增加 canonical JSON payload；新事件同时校验 `payloadHash == canonical_hash(payload)`，旧事件允许 `payload=null` 并明确标记历史不可回读。
3. resolve 的 resolution refs 只接受 Artifact、Evidence、EvalReportRevision、ReturnDecision 四种服务器可解析类型，并逐项同租户精确校验。
4. return 根据 PlanRevision.dependencies 中的显式 `{fromStepKey,toStepKey}` DAG 计算目标与传递下游：目标及下游为 invalidate；其余 step 为 reuse。依赖字段缺失时仅单 step 计划可安全返回；多 step 计划缺失/畸形/成环必须失败关闭，不在前端猜测。
5. ReturnDecision 保存不可变 `impactDecisions`，每项包含 step、invalidate/reuse 与 reason；Task Cockpit 原样展示服务器结果。
6. create 仅允许 admin/reviewer/evaluator/eval_service/aip_executor；resolve/return 仅允许 admin/reviewer/approver/production_operator/operator。读接口保持登录且租户隔离。

### 7.3 163/164 分层约束

- 原子 Skill：本波不发布或冒充新 Skill，仅消费 `review-output-quality` 的 ReviewIssue/decision 合同。
- Logic 编排：返工 DAG/invalidation 由 AIP 服务端 authority 计算；Workshop 不复制编排算法。
- 数字同事绑定：本波不自动改绑，不把代码 GREEN 宣称为 Skill/Logic/Coworker 运营绑定 GREEN。
- 工作台贡献视图：只展示规则、证据、事件 payload、ReturnDecision、attempt 与 invalidate/reuse；不展示隐藏推理链，不制造业务结果。

### 7.4 文件级最小改动

- `services/aos-api/alembic/versions/w4_003_review_return_lineage.py`
- `services/aos-api/aos_api/aip_production_contracts.py`
- `services/aos-api/aos_api/aip_production_contract_store.py`
- `services/aos-api/aos_api/routers/aip_production_contracts.py`
- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit_contracts.py`
- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit.py`
- `services/aos-api/tests/aip/test_w4_04_review_return_lineage.py`
- `services/aos-api/tests/aip/test_w_l14_review_return_attempt.py`（补 ReviewRule authority seed，保持原能力不倒退）
- `apps/web/src/api/ecommerceWorkshop/contracts.ts`
- `apps/web/src/api/ecommerceWorkshop/parser.ts`
- `apps/web/src/components/workshop/TaskCockpitPage.tsx`
- 对应 Web parser/page 测试、生成 OpenAPI 与本波 evidence。

### 7.5 验证与安全边界

先以测试证明 rule missing/hash drift、resolution missing/cross-tenant、权限拒绝、DAG invalidation/reuse、事件 hash 漂移均失败；再跑 AIP 专项与累计回归、Web 专项与全量测试、类型检查、构建、OpenAPI 确定性检查、Alembic 单 head，并以 `org-org/dev-project` 内置浏览器只读验收。迁移仅生成与静态验证，不对真实数据库执行；不触发真实 EvalRun/AgentRun/Action/Approval/Handoff、发布或业务写入。

## 8. 实施与验收结果（2026-08-25）

- `m1@6f62541` 新增租户隔离、append-only 的 `ReviewRuleRevision` authority；create issue 必须重读 exact id/revision/hash，missing、跨租户或 drift 均失败关闭。ReviewIssueEvent 新事件保存 canonical payload 并由 Task Cockpit 回读时复算 hash；历史无 payload 的事件保持可读并显式标记 `legacy_unavailable`。
- resolve 只接受并精确校验 Artifact、Evidence、EvalReportRevision、ReturnDecision；return 由服务端读取 Plan 的显式 DAG，目标和传递下游输出 `invalidate`，不受影响节点输出 `reuse`，缺边、畸形边、自环或环路均失败关闭。ReturnDecision 保存该不可变影响集合；既有 latest-attempt 与 N+1 queued attempt 语义保持不变。
- create 与 resolve/return 使用分离的显式 review/control 角色门；Workshop 只展示服务端事件 payload、attempt 和影响决定，不复制 DAG 算法、不发布新 Skill、不自动改绑数字同事，也不声明运营贡献。
- 后端专项 `35 passed`，W4 累计 `61 passed`；OpenAPI `13 passed`、确定性导出 `2582 paths / 2162 schemas`；Web 全量 `221 files / 2091 tests`、Desktop `9 files / 40 tests` 与 production build 均通过；compileall、diff check、Alembic 单 head `w4_003` 通过。
- 内置浏览器在真实租户 `org-org/dev-project` 的 canonical `/workshop/cockpit` 只读页面完成宿主、真实任务与失败关闭验收，1280 有效视口无横向溢出且未触发任何命令。当前真实页面没有可见的 W4-04 ReviewIssue，因此 exact payload 与 invalidate/reuse 的呈现由 strict parser/component 测试闭合；不据此宣称 live migration、运营 lineage 或 release GREEN。
- 证据：`.evidence/workshop/2026-08-25-w4-04-review-return-lineage.json`；代码提交 `6f62541`，证据提交 `a1a7c7f`。

结论：W4-04 在代码、控制面、严格读模型和只读浏览器宿主范围内闭合，且旧功能测试无倒退；真实 migration、返工执行、EvalRun、Provider、Action、Approval、Handoff、发布与业务写入均未发生。下一串行任务为 W4-05。
