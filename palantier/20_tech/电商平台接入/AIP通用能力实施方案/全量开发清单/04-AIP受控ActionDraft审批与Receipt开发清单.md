# 04 AIP 受控 Action、Draft、审批与 Receipt 开发清单

> 状态：**v1.5 · IMPLEMENTED_GREEN（AIP-3A / AIP-3B / AIP-3C 全部封板）**
> 上位依据：`../04-228-AIP受控Action权限Draft与审批闭环实施方案.md`
> 对应阶段：AIP-3；前置：02 Task/Run 主链 GREEN。

## 0. 实时基线与实施子波（2026-08-11）

- 代码基线：`m1@a7f3aa2`；迁移唯一 head 与开发库当前版本均为 `aip3b_002`；正向范围只允许 `org-org/dev-project`，`dev-org` 只作负向 canary。
- 已确认旧 `draft_dataset` 只有 proposed/approved/rejected 三态，`/v1/aip/drafts/{id}/approve` 会直接写生产；`POST /v1/actions/execute` 仍允许 `autoApprove=true`。两者均不满足 Proposal→Approval→Lease→Receipt 安全链。
- 旧 `aip_drafts_engine` 仍为内存 singleton，但其 phase3 公共路由已清空；本轮只保留可导入兼容，不再作为生产真源。
- AIP-3A：冻结 DTO/错误码/状态机，新增 PostgreSQL authority、FORCE RLS、服务端风险下限、Proposal snapshot/hash、Draft 与 maker-checker Approval；此子波禁止调用外部 Adapter。
- AIP-3B：新增单次 ExecutionLease、预算/频控/kill switch、Adapter 幂等、Receipt、unknown/reconcile 与 compensation 新 Proposal；关闭 `autoApprove` 和旧直接写生产旁路。
- AIP-3C：建立 `apps/web/src/api/aipActions/` 唯一 SDK，Draft Inbox 显示真实 Proposal/Draft/Approval/Lease/Receipt 状态，完成真实浏览器、跨租户 canary 与 EvidencePack。

停止条件：出现第二迁移 head、需要破坏性回填真实 Draft、必须改写 O1 Action 公共契约、外部调用无法提供稳定幂等/只读对账，或任何跨租户可见时立即停止当前子波。

## 1. 工作包

| ID | 任务 | 文件边界 | 验收 |
|---|---|---|---|
| 04-01 | ✅ 冻结 ActionTypeRevision/Risk/Proposal/Draft/Approval/Lease/Receipt DTO | contracts/OpenAPI | O1 Action 引用复用，无第二 Action |
| 04-02 | ✅ 建 proposal/approval/lease/receipt/event 表及 RLS/FK | migration | 组合唯一键、append-only 事件 |
| 04-03 | ✅ 实现服务端风险下限与 policy engine | `aip_action_policy.py` | 客户端只能提示，不能降风险 |
| 04-04 | ✅ 实现 Proposal snapshot/diff/evidence/expiry | proposal service | revision/hash 变化旧批准失效 |
| 04-05 | ✅ maker-checker、执行职责分离与权限时限重验 | approval/execution service | 双人/时限/职责分离已覆盖 |
| 04-06 | ✅ 实现单次 ExecutionLease、预算、频控、kill switch | execution service | 过期/重复 lease 不可执行 |
| 04-07 | ✅ 实现 Adapter 调用、稳定幂等与 provider request id | adapters | 未注册失败关闭，单次消费 |
| 04-08 | ✅ 实现 immutable Receipt 与 unknown/reconcile | reconciler | 超时不直接失败或盲重试 |
| 04-09 | ✅ 实现 compensation 为新 Proposal | compensation service | 不把数据库回滚当补偿 |
| 04-10 | ✅ 收敛 O1 Draft、`runtime_write.py` 与旧 phase3 | routes/compat | 无双写、无 transition 绕权 |
| 04-11 | ✅ Draft Inbox/Logic Run UI 对接 canonical 状态 | SDK/pages | 批准不等于已执行，Receipt 才 applied |

### AIP-3B 编码顺序（已评审）

1. 新增 `aip3b_001`，不修改已应用的 `aip3_001`：Receipt 攺为 append-only 链，新增 `supersedes_receipt_id/receipt_kind`，初始 Receipt 每 Lease 唯一；reconcile Receipt 可追加且必须指向同租户同 Lease 的 unknown Receipt。
> 迁移补充：在 `aip3b_001` 之后追加 `aip3b_002` 数据库触发器，阻断 Receipt UPDATE/DELETE/TRUNCATE；两者保持单一迁移 head。

2. 新增四级 kill switch、工作区 Action 日预算与分钟频控使用事实；全部使用复合租户键、FORCE RLS，策略更新与使用记账在 Lease 事务内完成。
3. 增加 Lease DTO/API/Store：执行角色、职责分离、精确 hash/version、当前 Action revision、审批有效期、Proposal expiry、R4、预算/频控/kill switch 全量重验；并发只产生一个 attempt=1 Lease。
4. 增加 Adapter Registry 与执行服务：仅注册 adapter 可达，稳定 provider idempotency key，Lease 单次消费；确定结果写初始 Receipt，超时/连接中断写 unknown 且禁止自动重试。
5. 增加 Receipt 查询与 reconcile：只读 provider 查询，unknown 只能通过追加 `reconcile` Receipt 收敛；不原地 UPDATE Receipt。
6. compensation 只创建新 Proposal，并绑定原 Proposal/Receipt evidence；R4 无专项 policy 继续拒绝。
7. 旧 `/v1/actions/execute` 只保留 `autoApprove=false` 的 Draft-only 兼容；`autoApprove=true`、`draftId` 执行和旧 Draft approve 均改为 `AIP_LEGACY_WRITE_PATH_DISABLED`；保留历史读/拒绝兼容，不迁移、不双写、不直写生产对象。
8. 完成迁移/RLS、职责分离、并发 Lease、预算/频控/kill switch、超时 unknown、reconcile、补偿、跨租户及旧旁路测试；随后更新 OpenAPI/route inventory，才进入 AIP-3C。

### AIP-3C 编码顺序（已评审）

1. 增加只读 execution view API，让刷新后的 UI 可恢复 Lease 与 Receipt 链，不从 Proposal 状态或 timeline 文案反推执行事实。
2. 建立 `apps/web/src/api/aipActions/` 严格 contracts/client/test，覆盖 list/get/timeline/decision/lease/execute/reconcile；统一使用 AIP client 和租户请求头。
3. Draft Inbox 切换至 canonical Proposal，删除生产路径的 Mock/本地状态机；展示审批、租约、外部提交、unknown/reconcile、applied/failed 的真实区别。
4. 每个写按钮绑定当前 version/hash 和幂等键，成功后服务端重读；失败或响应不一致时禁用继续写入并显示可行动错误。
5. Canonical TaskRun 面板增加按 taskId/runId 打开受控 Action Inbox 的入口。
6. 完成 SDK/组件/交互、TypeScript/build、真实租户只读、跨租户 canary 与内置浏览器验收后，更新 EvidencePack 和项目上下文。
7. 清查旧页面调用方；把订单管理的 `autoApprove=true` 改为 Draft-only，并把成功文案改为“待审草稿已创建”，禁止误报外部动作已经执行。

### AIP-3A 编码顺序（已评审）

1. 在 `aip_contracts.py` 增加 ActionTypeRevisionRef、ActionProposal、DraftSnapshot、ApprovalEvent、ExecutionLease 与 ActionReceipt 严格 DTO；客户端 risk 仅作 hint。
2. 增加 `aip3_001_action_control.py`，新表全部使用 `(org_id, project_id, id)` 复合真值键、组合 FK、append-only event、FORCE RLS；不改写既有 `draft_dataset` 历史行。
3. 增加 `aip_action_store.py`、`aip_action_policy.py` 与 `aip_action_service.py`：服务端读取 O1 `meta_action_type`，计算风险下限，冻结 object/task/run/purpose/marking/payload/diff/evidence snapshot 与 sha256 hash。
4. Proposal 创建同时建立 canonical Draft；Approval 只能绑定精确 proposal revision/hash，maker 不得自批，过期/撤权/修改后的 Approval 不可复用。
5. 发布 `/v1/aip/action-proposals` 的 create/list/get/decision/timeline API；decision 以严格枚举统一 approve/reject，AIP-3A 不发布 execute/lease Adapter 能力。
6. 完成迁移、RLS、并发、幂等、hash 失效、maker-checker、跨租户、OpenAPI/route inventory 测试后才进入 AIP-3B。

### AIP-3A GREEN 证据（2026-08-11）

- commit：`60344d5`；迁移：`aip3_001 (head)`。
- 54 tests passed + 2 subtests；并发 Proposal/Approval、相同与不同 payload 幂等、过期、审批角色、maker-checker、R4 双人批准、跨租户不可发现均覆盖。
- OpenAPI：4089 route rows / 4079 unique pairs / 2324 paths；513 个 manifest routers；双进程导出确定且当前。
- 开发 API 已重启到新代码；只读烟测 `org-org/dev-project=0`、`dev-org/dev-project=0`，本波未写真实业务对象和验收 Proposal。

### AIP-3B GREEN 证据（2026-08-11）

- commit：`a7f3aa2`；迁移唯一 head / current：`aip3b_002`。
- 76 tests passed + 2 subtests；覆盖职责分离、并发 Lease、kill switch、预算/频控、Adapter allowlist、applied/unknown/reconcile、Receipt 数据库不可变、compensation、旧旁路关闭与跨租户不可发现。
- OpenAPI/Router inventory 已更新且确定性检查通过；Python compileall 与 diff check 通过，当前环境无 `ruff`，不计为通过。
- 开发 API 已重启到新代码；只读烟测 `org-org/dev-project=0`、`dev-org/dev-project=0`，未调用真实外部 Adapter，未写真实业务对象和验收 Proposal。

### AIP-3C GREEN 证据（2026-08-11）

- commit：`b7bcb76`；新增 execution view、唯一 Action SDK、canonical Draft Inbox 与 TaskRun 深链。
- 后端相关回归 77 passed + 2 subtests；OpenAPI 12 passed；Router 8 passed + 2 subtests。
- 前端定向 114 passed，补充专项 20 passed；TypeScript 与 production build PASS。
- 双租户只读列表均为 200/count=0；内置浏览器确认 `org-org/dev-project` 的栖月汇真实空态与刷新一致，未注入 Mock、未执行写操作。
- EvidencePack：`20_tech/evidence/aip/aip-3/AIP-3C_20260811T180832+0800/summary.json`。

## 2. 安全测试矩阵

- R0～R4、字段 marking、purpose、权限撤回、过期批准、预算、频控、kill switch。
- 并发批准、并发 lease、相同/不同 payload 幂等键、网络超时、迟到回执、provider 无幂等能力。
- 跨租户资源枚举、审批人=执行人、break-glass 超时、补偿越权均拒绝。

## 3. 退出门

- [x] 无批准时 R2+ adapter 不可达；R4 默认禁止。
- [x] proposal 修改、批准过期、撤权、预算耗尽均阻止执行。
- [x] unknown 可对账并收敛；重复请求不产生双外部动作。
- [x] UI、API、数据库事件、Receipt 状态一致；AIP-3C 不删除审计事实，Lineage 深化进入 AIP-4。
