# 24-AIP-W2-B EvalContract 与 ResponsibilityPlan 实施清单

> 状态：APPROVED_FOR_IMPLEMENTATION
> 日期：2026-08-13
> 代码线：`/Users/ddt/work/projects/ai_agent/aos-platform-w1-aip` / `w1-aip`
> 上位依据：16、17、21、23 号方案；W2-A 与 A7-1～A7-3 实时代码

## 1. 目标与边界

W2-B 补齐工作台、AIP-9 与六数字同事共同需要的两个 L0 authority：`EvalContractRevision` 与 `ResponsibilityPlanRevision`。本波不复制 EvalRun/Report，不创建第二套 Agent/Binding，不启动生产 Run，不以固定 Agent 团队或显示名充当职责真源。

## 2. 复用真源

- Eval：`aip_eval_suite_revision`、`aip_publication_event`、`aip_release_gate_decision`、现有 EvalRun/Report。
- Agent：`aip_agent_instance`、`aip_skill_binding`、`aip_capability_binding` 与 A6F exact revision/hash refs。
- 共同能力：W2-A `aip_production_contract_receipt`、Principal TenantScope、canonical hash、稳定错误映射。

## 3. Canonical DTO

### 3.1 EvalContractRevision

- identity：`contractId/revision/version/contentHash/lifecycle`；
- exact refs：`suiteRef` 必须指向同租户 `EvalSuiteRevision` 并匹配 revision/hash；`publicationRef`、`releaseGateRef` 允许在 draft 阶段缺失，但 freeze 时必须存在、匹配 suite 且未 revoked/invalidated；
- policy：`artifactSchemaRef`、`severityThresholds`、`gatePolicy`、`returnMapping`、`overridePolicy`；
- readiness：`ready|blocked|stale|unknown` 与稳定 blocker code 列表，由服务端计算，不由客户端写入。

### 3.2 ResponsibilityPlanRevision

- identity：`planId/revision/version/contentHash/lifecycle/profile/templateRef`；
- slot：stable `slotId`、`responsibilityType`、required capability IDs、input/output schema refs、gate refs、return stage、assignee exact ref；
- assignee kind 仅允许 `agent_instance|human_principal|tool_binding|provider_capability_binding`；显示名不参与 identity；
- coverage：`complete|partial|blocked|unknown`、uncovered slots、merge decisions、readiness/blockers；
- 独立审核、硬合规、外部发布批准、Receipt 对账四类职责不可被 merge decision 吞并。

## 4. 持久化与迁移

- 新增线性迁移 `w2_002_eval_responsibility`，`down_revision=aip7_001`；不得修改历史迁移。
- 表：`aip_eval_contract_head/revision`、`aip_responsibility_plan_head/revision`；复合 tenant PK/FK、tenant 前缀索引、RLS/FORCE RLS。
- revision append-only；仅 head 允许 CAS 推进；Receipt 继续复用 W2-A 表。
- downgrade 仅允许无业务行开发环境；应用回滚保留历史 revision。

## 5. Store 与失败语义

- create draft：严格校验同租户依赖，写 revision/head/Receipt 原子事务；同幂等键同 payload replay，漂移 409。
- revise：只允许 draft，`expectedVersion` stale 为 409；不可原地改 revision。
- freeze：锁 head，重新解析 exact ref 与 readiness；blocked/stale/unknown 均返回 422 且不推进 head。
- read/list：按 Principal scope 读取，不 fallback；unknown 为 404。
- blocker code 至少覆盖：`EVAL_SUITE_MISSING/DRIFTED`、`EVAL_PUBLICATION_MISSING/REVOKED`、`EVAL_GATE_MISSING/INVALIDATED`、`ASSIGNEE_MISSING/DRIFTED`、`SKILL_BINDING_NOT_ACTIVE`、`CAPABILITY_BINDING_NOT_ACTIVE`、`RESPONSIBILITY_UNCOVERED`、`INDEPENDENT_REVIEW_CONFLICT`。

## 6. Canonical API

在 `/v1/aip/production-contracts` additive 增加：

- `POST/GET /eval-contracts`、`GET /eval-contracts/{id}`、`POST /eval-contracts/{id}/revisions`、`POST /eval-contracts/{id}/freeze`；
- `POST/GET /responsibility-plans`、`GET /responsibility-plans/{id}`、`POST /responsibility-plans/{id}/revisions`、`POST /responsibility-plans/{id}/freeze`。

写请求必须带 `Idempotency-Key`；revision/freeze body 带 `expectedVersion`。TenantScope 只取 Principal。

## 7. 实施切片

1. W2-B1：DTO、migration、Store、Store/迁移测试；
2. W2-B2：Canonical API、OpenAPI、权限/错误/隔离测试；
3. W2-B3：唯一 TypeScript SDK、Production Contracts 页面 Eval/Responsibility 视图；
4. W2-B4：`org-org/dev-project` 真实六实例候选与 blocked readiness 验收、`dev-org/dev-project` 0 数据 canary、累计回归与封板。

每个切片独立提交、更新 `01/06`；未通过前不进入下一切片。

## 8. 测试矩阵

- Contract：unknown enum/field、hash/ref/schema、重复 slot、非法 merge、独立审核冲突。
- Store：migration upgrade/downgrade、唯一 head、RLS、CAS、append-only、restart readback、幂等漂移、跨租户依赖。
- Eval：suite drift、publication revoked、gate invalidated、threshold/return mapping 冻结。
- Responsibility：六实例 exact ref、inactive/missing skill/capability、uncovered slot、显示名不可作 identity。
- API：Principal scope、400/404/409/422/503、OpenAPI 路由、旧 W2-A 无回归。
- Web：loading/empty/forbidden/blocked/stale/failed、禁用原因、刷新恢复、console 0 error。

## 9. 风险与回滚

- 最大风险是为了 freeze 人为激活 Binding；禁止。本轮预期真实结果可以是 draft 可读、freeze 422 blocked。
- publication/gate 事件是 append-only 事件流，解析时必须按 target/suite exact ref 选择当前有效事件，不能只按 ID 猜测。
- 若 W2-B 失败，关闭新增 mutation 路由并保留只读；不得删除已落 revision/Receipt。

## 10. 评审结论

首审重点核对了第二真源、迁移 head、draft/freeze 边界、exact assignee、独立审核不可合并和外部门诚实性。整改后已明确：只做 additive wrapper；freeze 时服务端复验；无 active Binding 时稳定 blocked；四切片独立封板。结论：`APPROVED_FOR_IMPLEMENTATION`，允许从 W2-B1 开始。
