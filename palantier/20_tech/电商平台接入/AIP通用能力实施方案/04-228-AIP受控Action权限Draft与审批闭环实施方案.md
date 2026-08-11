# 228-AIP 受控 Action、权限、Draft 与审批闭环实施方案

> 状态：**评审通过 · v1.5 `IMPLEMENTED_GREEN`（AIP-3A / AIP-3B / AIP-3C 全部封板）**
> 对应阶段：AIP-3。

## 1. 目标

把 Tool 请求、Ontology Action、外部 Connector 和人工审批统一为：

```text
ActionType policy
 -> ActionProposal
 -> server-side risk classification
 -> Draft
 -> maker-checker approval
 -> ExecutionLease
 -> Adapter call
 -> Receipt / UnknownExternalState
 -> reconcile / compensate
```

## 2. 风险分层

| 等级 | 示例 | 默认 |
|---|---|---|
| R0 | 本体/Wiki/公开证据只读查询 | 可执行，完整留痕 |
| R1 | 内容、回复、报告、活动草稿 | 自动生成 Draft，不外发 |
| R2 | 单次低影响发布/触达 | 指定角色批准后执行 |
| R3 | 批量触达、价格/优惠、公开直播 | maker-checker + 预算/频控 |
| R4 | 支付、退款、库存扣减、权限、不可逆 | 默认禁止，专项安全评审 |

客户端的 `risk_level` 只是提示，服务端策略必须抬高风险，不得降低。

## 3. Canonical 对象

- `ActionTypeRevision`：input schema、side effect、risk floor、permission、adapter、receipt schema、compensation。
- `ActionProposal`：task/run/actor/object refs、expected revision、idempotency key、expires_at。
- `Draft`：proposal snapshot、diff、evidence、approval policy。
- `ApprovalEvent`：maker/checker、decision、bound revision/hash。
- `ExecutionLease`：单次执行租约、截止时间、attempt。
- `ActionReceipt`：provider request id、accepted/applied/failed/unknown、reread evidence。

Proposal 状态为 `proposed -> drafted -> approved/rejected/expired -> leased -> executing -> applied/failed/unknown -> reconciled/compensated`。每次状态迁移均绑定 expected revision 和不可变事件；Approval 只能批准精确 proposal hash，ExecutionLease 不能跨 ActionProposal 复用。

## 4. 六层防线的现代化映射

旧“六层权限”不再堆 Prompt 规则，映射为：

1. Capability/ActionType allowlist。
2. 服务端风险下限与 Policy Engine。
3. AuthZ、租户、字段 marking、purpose check。
4. Draft 与职责分离。
5. Adapter 网络/密钥/预算/频控/kill switch。
6. Receipt 回读、对账、补偿与事故审计。

## 5. 现有映射与文件

复用 O1 Action/Draft/Receipt、现有 DraftInbox、tenant isolation、decision lineage。禁止继续扩展 `aip_drafts_engine` singleton 为生产真源。

```text
services/aos-api/alembic/versions/*_aip_action_control.py
services/aos-api/aos_api/aip_action_policy.py
services/aos-api/aos_api/aip_action_proposal_service.py
services/aos-api/aos_api/aip_action_execution_service.py
services/aos-api/aos_api/routers/aip_actions.py
apps/web/src/api/aipActions/*
apps/web/src/pages/DraftInboxPage.tsx
apps/web/src/pages/s2/LogicRunPanel.tsx
```

新增候选为 policy/proposal/execution service、迁移和 `/v1/aip/actions`；修改现有 `DraftInboxPage.tsx`、LogicRunPanel 及 O1 Action 适配边界。AIP-0 先形成旧 phase3 Draft、O1 Draft 与新 API 的路由去重表，禁止双写两套 Draft。

## 6. 对账、补偿与安全运营

- 外部请求使用稳定 idempotency key；若 provider 不支持，则记录 request fingerprint、发送窗口和 provider request id，并把超时置为 unknown。
- Reconciler 只能通过授权只读接口或回执查询确认结果；不能以“未收到响应”推断失败。
- Compensation 是新的受控 ActionProposal，不是数据库回滚；支付、退款、库存等 R4 动作没有专项批准时不提供补偿入口。
- kill switch 分平台、组织、工作区、ActionType 四级；触发后阻止新 lease，但保留对已发送请求的对账能力。
- 审批人、执行服务账号、策略维护者职责分离；紧急 break-glass 也必须有时限、双人确认和事故 Receipt。

## 7. 验收

1. 无批准时所有 R2+ Adapter 不可达。
2. 修改 proposal 后旧批准失效。
3. 重复请求只产生一个外部动作或进入明确 unknown/reconcile。
4. 超时不能直接标失败并重试；必须先按 provider request id 对账。
5. 跨租户、越权字段、过期批准、预算耗尽、kill switch 均失败关闭。
6. UI 的“批准”不等于已执行；只有 Receipt 回读才能显示已应用。
7. kill switch、服务重启和网络超时组合下不产生重复外部动作。
8. Proposal/Draft/Approval/Receipt 的租户、actor、purpose 和字段 marking 在导出时仍可审计。

## 8. 代码实时对账与最小迁移策略（2026-08-11）

### 8.1 已有能力

- O1 的 `meta_action_type`、字段 marking、submission criteria、`draft_dataset`、`decision_lineage` 与 Draft Inbox 可复用。
- `phase3_aip_drafts` 已不再注册公共路由，避免旧内存状态机继续成为第二 API owner。
- AIP-1 已提供 canonical Task/Plan/Run、不可变 Evidence、控制幂等与 unknown/reconcile 基础语义，可作为 Proposal 的 task/run 引用和审计上下文。

### 8.2 必须关闭的缺口

- 旧 Draft 批准会在同一请求内直接写 `obj_instance/wiki_page`，没有独立 Approval、ExecutionLease 和 Receipt，UI 因而把“批准”等同“已应用”。
- `/v1/actions/execute` 的 `autoApprove=true` 可绕过 maker-checker；本轮必须在真实范围失败关闭。
- `draft_dataset` 只有三态，且无法表达 proposal hash、审批过期、租约、unknown/reconcile。为避免破坏历史数据，本轮新增 AIP Action authority 表，不扩写旧表为第二复杂状态机。
- `aip_drafts_engine` 仅保留导入兼容和旧测试，不允许新生产代码读写。

### 8.3 Canonical 归属

- `meta_action_type` 继续是 O1 Action Type 定义真源；AIP 只保存精确引用与执行时 policy snapshot，不复制 Action Type。
- `aip_action_proposal` 是意图与精确 payload/hash 真源；`aip_action_draft` 是供人审阅的不可外发快照；`aip_action_approval_event` 是 append-only 决策事实。
- `aip_action_execution_lease` 只授权一次确定 payload 的一次 attempt；`aip_action_receipt` 是外部效果与最终展示真源。批准不代表应用成功。
- 旧 `draft_dataset` 仅作为 O1 兼容 Draft 投影；在 AIP-3C 切换完成前可读，但不得反向驱动新安全状态机。

## 9. 实施分波与文件边界

### AIP-3A：契约、数据与审批门

新增：

```text
services/aos-api/alembic/versions/aip3_001_action_control.py
services/aos-api/aos_api/aip_action_models.py
services/aos-api/aos_api/aip_action_store.py
services/aos-api/aos_api/aip_action_policy.py
services/aos-api/aos_api/aip_action_service.py
services/aos-api/aos_api/routers/aip_actions.py
services/aos-api/tests/aip/test_aip_action_*.py
```

修改：

```text
services/aos-api/aos_api/aip_contracts.py
services/aos-api/aos_api/main.py
services/aos-api/openapi.json
services/aos-api/tests/openapi/*
```

本子波只到 approved/rejected，不调用 Adapter，不写真实业务对象。

### AIP-3B：租约、执行、回执与补偿

在同一 canonical service/store 上增加 lease、预算/频控/kill switch、adapter registry、Receipt/reconcile；修改 `routers/runtime_write.py` 关闭 `autoApprove` 与直接批准写生产旁路。任何超时先写 unknown，只有主动回读可收敛；compensation 必须创建新 Proposal。

#### AIP-3B 权威执行契约（冻结）

1. `POST /v1/aip/action-proposals/{proposal_id}/lease` 只允许 `aip_executor/admin`，且执行人不得是 maker 或任一 approver；服务端在同一事务内锁定 Proposal，重新检查精确 hash/version、Action revision、审批角色当前有效性、审批时限、Proposal expiry、R4 默认禁用、预算/频控和四级 kill switch。
2. 每个 Proposal 只允许一个 attempt=1 的租约；并发申请通过 advisory lock 与唯一键收敛为同一 Lease。租约过期、撤销或已消费后不得复用，也不自动创建 attempt=2。
3. `POST /v1/aip/action-leases/{lease_id}/execute` 只能消费一次 active Lease。Adapter Registry 只接受明确注册的 adapter；调用参数使用 Proposal 冻结 payload，外部幂等键固定为 Proposal idempotency key + proposal hash，不接受客户端临时改写。
4. Adapter 返回 applied/failed 时追加初始 Receipt；超时、连接中断或无法判断外部效果时只追加 `unknown` Receipt，并返回 `AIP_OUTCOME_UNKNOWN` 语义，禁止自动重试。
5. `POST /v1/aip/action-receipts/{receipt_id}/reconcile` 仅允许授权只读 provider 查询。Receipt 不更新、不删除：对账结果以新的 Receipt 追加，使用 `supersedes_receipt_id` 指向 unknown Receipt；Proposal 的展示状态投影到最新 Receipt。
6. `POST /v1/aip/action-proposals/{proposal_id}/compensation` 不执行回滚，只以原 Proposal/Receipt 为 evidence 创建新的受控 Proposal；R4 在没有专项 policy 时仍拒绝。
7. kill switch 采用平台、组织、工作区、ActionType 四级匹配，任一级启用即阻止新 Lease；已发送请求仍允许只读 reconcile。预算按工作区 + ActionType + UTC 日窗口记账；频控按工作区 + ActionType 滚动分钟窗口计数。
8. `aip3_001` 已应用，不得修改。新增 `aip3b_001` 扩展 Receipt 追加链、执行 policy/usage 表与 RLS，`aip3b_002` 用数据库触发器阻断 Receipt UPDATE/DELETE/TRUNCATE；迁移必须保持单一 head。

#### 旧入口兼容裁决（冻结）

- `POST /v1/actions/execute` 仅在 `autoApprove=false` 且未传 `draftId` 时保留“只创建旧 Draft、不写生产”的兼容行为；`autoApprove=true`、传 `draftId` 及 `POST /v1/aip/drafts/{draft_id}/approve` 均返回 `AIP_LEGACY_WRITE_PATH_DISABLED`，不再写 `obj_instance/wiki_page`。
- 旧 Draft 的 create/list/get/reject 可保留为历史只读/撤回兼容，但不能反向驱动 AIP 权威状态机。
- 不迁移或伪造历史旧 Draft 为新 Proposal；需要继续执行时由调用方显式创建 canonical Proposal，确保新的 hash、risk、policy 与审批事实完整。

#### AIP-3B 新增及修改文件

```text
services/aos-api/alembic/versions/aip3b_001_action_execution.py
services/aos-api/alembic/versions/aip3b_002_receipt_immutability.py
services/aos-api/aos_api/aip_action_adapters.py
services/aos-api/aos_api/aip_action_execution.py
services/aos-api/aos_api/aip_action_models.py
services/aos-api/aos_api/aip_action_store.py
services/aos-api/aos_api/aip_action_service.py
services/aos-api/aos_api/routers/aip_actions.py
services/aos-api/aos_api/routers/runtime_write.py
services/aos-api/tests/aip/test_aip3b_action_execution.py
services/aos-api/tests/aip/test_aip3b_legacy_write_closed.py
```

### AIP-3C：前端消费与浏览器封板

新增唯一 `apps/web/src/api/aipActions/` SDK；修改 `DraftInboxPage.tsx` 和 Logic Run 入口。UI 必须分别展示“已批准”“已获执行租约”“已提交外部系统”“结果待对账”“已应用”，且服务不可用时不注入示例 Draft、不启用本地状态机。

#### AIP-3C 前端消费契约（冻结）

1. 增加只读 `GET /v1/aip/action-proposals/{proposal_id}/execution`，返回当前 Proposal、Lease 与 immutable Receipt 链；这是刷新后恢复执行事实的唯一入口，前端不得从本地状态或 timeline 文案猜测 Receipt。
2. `apps/web/src/api/aipActions/` 作为唯一 Action SDK，严格解析 Proposal/Draft/Approval/Lease/Receipt；未知状态、跨资源引用、重复 Receipt 或缺失 hash 均失败关闭。TenantScope 只从统一请求头注入，body 禁止携带 org/project。
3. Draft Inbox 只读取 canonical Proposal；查询参数 `taskId/runId` 仅作当前租户内客户端筛选。页面分别展示待审批、已批准、执行中、待对账、已完成/失败，不把 approved 文案写成“已落生产”。
4. approve/reject 绑定当前 Proposal version/hash 并写幂等键；lease/execute/reconcile 只在服务端状态允许时开放。每次写操作后必须重新读取 canonical bundle/execution view；服务失败时保留最后一次已核验快照但禁用写操作。
5. Logic Run 的 canonical TaskRun 面板提供“查看本次受控 Action”入口，携带服务端 Task/Run id 跳转，不创建第二套 Action 状态。
6. 正向浏览器验收只读 `org-org/dev-project`；功能写路径由前端契约/交互测试覆盖，跨租户由后端 canary 覆盖。不得为浏览器展示向真实租户插入验收 Proposal 或调用真实外部 Adapter。
7. 清查仍调用旧 `/v1/actions/execute` 的页面：禁止发送 `autoApprove=true`，兼容入口只能诚实显示“待审草稿已创建”，不得显示“执行成功”或刷新业务对象来暗示已落生产；后续由上层场景在具备精确 Action revision/evidence 后改为创建 canonical Proposal。

## 10. AIP-3A 实施结果（2026-08-11）

- 代码基线：`aos-platform/m1@60344d5`；开发库与唯一迁移 head 均为 `aip3_001`。
- 已建立 Proposal、Draft、ApprovalEvent、ExecutionLease、Receipt、Event 六张租户权威表；全部使用复合租户键、组合外键和 FORCE RLS，审批与事件事实 append-only。
- Proposal hash 已绑定 TenantScope、发起人、ActionType 精确 revision、task/run/object/purpose/payload/diff/evidence/expiry；客户端风险提示只能抬高、不能降低服务端风险下限。
- canonical API 为 create/list/get/decision/timeline；`decision` 用严格 decision DTO 统一承载 approve/reject，避免两个动作端点产生状态机分叉。Proposal 创建同步产生不可外发 Draft。
- maker-checker 同时校验不同 actor 与审批角色；R3/R4 至少双人审批，R4 仍 `executionAllowed=false`，本子波未发布 lease/execute，也未调用 Adapter 或写业务对象。
- 幂等键在事务级 advisory lock 下串行化；并发 Proposal 与并发 Approval 重放均只产生一份权威事实，不同 payload 重用幂等键返回冲突。
- 验证：AIP/OpenAPI/router 定向集 54 passed + 2 subtests；OpenAPI 4089 route rows / 4079 unique pairs / 2324 paths，AIP 无重复 owner；真实开发服务中 `org-org/dev-project` 与 `dev-org/dev-project` 列表均为 200/0，未写验收垃圾数据。
- 下一门：AIP-3B 必须在执行前重验审批人/执行人职责、权限撤回、expiry、预算/频控/kill switch；超时只允许进入 unknown，禁止盲重试。

## 11. AIP-3B 实施结果（2026-08-11）

- 代码基线：`aos-platform/m1@a7f3aa2`；唯一迁移 head 与开发库均为 `aip3b_002`。
- 已发布 canonical lease、execute、reconcile、compensation API；职责分离、当前 Action revision/hash、Approval 时限、Proposal expiry、字段权限、R4、预算/频控与四级 kill switch 在获取 Lease 前统一重验。
- 每个 Proposal 只产生 attempt=1 Lease；未注册 Adapter 在消费 Lease 前失败关闭。Adapter 超时/连接中断只追加 immutable `unknown` Receipt，禁止盲重试；只读 reconcile 通过追加 Receipt 收敛。
- Receipt 以数据库触发器阻断 UPDATE/DELETE/TRUNCATE；initial 与 reconcile 使用局部唯一索引和 `supersedes_receipt_id` 形成可审计追加链。
- compensation 只创建绑定原 Receipt evidence 的新 Proposal，不把数据库回滚冒充外部补偿。
- 旧 Draft approve、`autoApprove=true` 和携带 `draftId` 的旧执行入口统一返回 `AIP_LEGACY_WRITE_PATH_DISABLED`；仅保留无外部副作用的 Draft-only 兼容创建。
- 验证：AIP 与相关契约/旧入口回归共 76 passed + 2 subtests；OpenAPI 确定性检查、Python compileall、diff check 通过；真实服务只读烟测 `org-org/dev-project=0`、`dev-org/dev-project=0`，未产生验收垃圾数据。
- 下一门：AIP-3C 只负责 canonical SDK、Draft Inbox/Logic Run 的真实状态投影与浏览器证据，不在前端复制策略引擎或本地伪造状态迁移。

## 12. AIP-3C 实施结果（2026-08-11）

- 代码基线：`aos-platform/m1@b7bcb76`；新增只读 execution view，使刷新后的 UI 从服务端恢复 Lease 与 immutable Receipt 链。
- `apps/web/src/api/aipActions/` 成为 Action 前端唯一 SDK，严格解析 Proposal/Draft/Approval/Lease/Receipt；Draft Inbox 已切换至 canonical Proposal，不再注入示例数据或维护本地状态机。
- 页面明确区分 approved、leased、executing、unknown、applied/reconciled；所有写按钮绑定当前 version/hash，成功后重读权威状态，失败后停止继续写入。
- Canonical TaskRun 已提供 taskId/runId 受控 Action 入口；订单管理旧调用已关闭 `autoApprove=true`，只允许诚实创建“待审草稿”，不再误报执行成功。
- 验证：后端相关回归 77 passed + 2 subtests；前端定向 114 passed，补充修正后专项 20 passed；OpenAPI 12 passed、Router 8 passed + 2 subtests；TypeScript、生产构建、diff check 通过。
- 真实服务只读烟测 `org-org/dev-project=0`、`dev-org/dev-project=0`；内置浏览器确认“栖月汇商贸有限公司 / 默认工作区”真实空态，刷新一致，未写验收 Proposal、未调用真实 Adapter。
- 下一门：进入 AIP-4 Evals 发布门控、决策谱系与可观测性权威链，不重开 AIP-3 状态机。
