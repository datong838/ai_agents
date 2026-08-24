# W3-06 HandoffEnvelope 传输与领域 Decision 分层预检 ADR

> 日期：2026-08-15；2026-08-25 按 m1 重新核验并进入实现
> 状态：`CODE_CONTROL_BROWSER_GREEN / W3-06_COMPLETE / NO_RELEASE / NO_MIGRATION_APPLIED / NO_EXTERNAL_EFFECT`
> 范围：当前唯一开发分支 `m1`；只实现合同、编译、受控命令 SDK、工作台入口、测试与浏览器验收，不执行迁移、发布、Provider、AgentRun、Action、Approval 或真实业务写入。

## 1. 结论

W3-06 的产品意图成立，但旧清单把“安全送达”和“接收后的业务决定”压成一个 Handoff 状态机，容易诱导实现去重新打开已经消费的 Envelope。经两轮审查后冻结为两层 authority：

1. AIP `HandoffEnvelope` 只拥有 `issued / consumed / revoked / expired` 传输生命周期；
2. `consume` 是一次性终态，只证明目标实例在当时权限下安全取得最小上下文；
3. `HandoffDecisionRevision` 追加 `accepted / rejected / request_more / returned` 领域决定，不覆盖 Envelope；
4. 唯一 `ModuleHandoffCompiler` 负责从 Module 语义编译 canonical refs，八个 BFF 不得各自拼 payload；
5. request-more 由来源重新授权并签发新 Envelope，不能复用 token 或把旧 Envelope 改回 issued。

2026-08-25 重新核验后，原结论中的多项“缺失”已被后续 m1 交付替代：canonical Handoff HTTP 与领域 Decision authority 已存在，Task Cockpit 也已有只读责任槽位/Handoff/Decision 投影；W3-05 exact ProductionContext 链已完成代码与浏览器闭环。当前实际缺口只剩唯一 `ModuleHandoffCompiler`、前端显式 issue/consume/decision 命令 SDK、以及工作台基于编译结果的受控命令入口。因此 W3-06 可以继续代码实现，但仍不得把 code GREEN 描述成 runtime、operational 或 release GREEN。

## 2. 当前平台事实

固定 m1 提交 `c48868b3f40c75fd625f9dac00e1c2cc9b02f6c0` 中，`AipHandoffService` 已提供 tenant-scoped PostgreSQL authority：

- issue 校验 exact Task/TaskRun、active sender/receiver AgentInstance、过期时间、allowlist 与 markings；
- bearer token 只返回一次，数据库只保存 hash；
- consume 校验 token、receiver exact revision、active instance，并重新授权全部 refs；
- consume 将 `issued` 原子推进为 `consumed`，重复消费失败关闭；
- revoke 使用 expected version CAS；consume 时可把已过期 Envelope 推进为 expired；
- issue 有幂等 Receipt，跨租户与错误 refs 由服务端拒绝。

这些是可复用的安全传输底座，不是完整跨 Module 协作闭环。

### 2.1 2026-08-25 当前 m1 增量事实

- `aip_handoffs.py` 已提供 canonical issue/get/consume/create-decision/list-decision/get-decision HTTP；
- `AipHandoffService` 已提供一次性 bearer、active instance、exact receiver、ref 再授权、Decision CAS/幂等和 Receipt；
- `aipAgentControl` 已有 Handoff/Decision 严格只读 parser，但缺 issue/consume/create-decision 命令类型、解析器和方法；
- Task Cockpit 已按 exact ResponsibilityPlan 读取 slot、assignee readiness、Handoff transport 与 Decision timeline，并明确 `consumed` 不等于 `accepted`；
- 尚无唯一 `ModuleHandoffCompiler` 把工作台的 TaskRun、source/target module、ResponsibilitySlot、最小披露 allowlist 编译为 canonical `IssueHandoffRequest`；
- 尚无工作台命令入口对 compiler 结果进行显式确认并调用 canonical authority。

本波不得建立第二套 Handoff/Decision store；所有 durable authority 仍由 AIP canonical service 独占。

## 3. 冻结的职责边界

### 3.1 传输 authority

`HandoffEnvelope` 只回答：谁在什么 TaskRun 上向谁披露了哪些 exact refs、字段与 markings，是否已送达、撤销或过期。它不回答接收方是否同意处理、还缺什么或是否完成工作。

目标 canonical 面至少覆盖 issue/get/list/consume/revoke/events，并同时进入 OpenAPI 与唯一前端 SDK。所有命令必须显式 tenant、权限、exact revision、幂等或 CAS；token 不得持久化在浏览器、日志、Receipt 或共享记忆。

### 3.2 ModuleHandoffCompiler

唯一 compiler 输入冻结为：source Module、Case/Batch/item exact ref、Task/TaskRun exact ref、requestedOutcome、purpose、deadline、allowed fields、markings、target Module、ResponsibilitySlot 与 correlation ref。它必须校验目标 Module 已安装、slot 可解析、sender/receiver binding operational-ready、字段披露在 allowlist 内；输出只能是 AIP Handoff issue command，不创建第二个 Handoff store 或 `HandoffContext`。

### 3.3 领域决定 authority

`HandoffDecisionRevision` 至少固定 Envelope exact ref、decision、typed reason/gap codes、actor/receiver exact ref、occurredAt、expected version、correlation ref 与 Receipt。语义如下：

| 决定 | 精确语义 | 明确禁止 |
|---|---|---|
| `accepted` | 接收方接受当前 scoped context | 冒充下游 Task 已启动或完成 |
| `rejected` | 接收方拒绝本次业务请求 | 自动取消来源 Task/TaskRun |
| `request_more` | 声明缺失的 context/evidence code | 回传裸正文、重开旧 Envelope、复用旧 token |
| `returned` | 返回 ReturnReceipt/Observation/EffectReview exact refs | 直接写来源 Module 领域表 |

同一 decision idempotency key 同 hash 重放返回原 Receipt，不同 hash 冲突；并发决定通过 expected version/CAS 保证单一当前决定。是否允许 rejected/request_more 后追加 returned，必须由冻结状态机显式定义，不能由页面猜测。

## 4. 目标命令与可见状态

1. `ecommerceWorkshopHandoffIssue`：经 ModuleHandoffCompiler 生成并调用 AIP issue，返回 Envelope、一次性 token 和 Receipt；浏览器只在当前操作所需时短暂持有 token。
2. 接收方执行 canonical consume；成功仅显示“上下文已安全接收”。
3. `ecommerceWorkshopHandoffDecisionCreate`：追加 accepted/rejected/request_more/returned 决定和 Receipt。
4. request-more 时，来源补齐并重新授权 refs，签发新 Envelope；新记录显式引用旧 Envelope/Decision。
5. timeline 合并展示 transport events 与 domain decisions，但不合并其状态或改写历史。

页面必须分别显示“已送达”“已接受”“待补资料”“已拒绝”“已返回结果”；任何一步的 unknown、expired、revoked、drifted 都给出 reasonCode 与恢复动作，不能合并成成功。

## 5. 依赖与停止门

| 依赖 | 当前事实 | W3-06 要求 |
|---|---|---|
| W3-01 / DEP-A6R | canonical HTTP 与 strict read parser 已存在 | 本波补齐 strict command SDK，不复制 authority |
| W3-05 | exact ProductionContext 链已 code/browser GREEN | compiler 固定 Task/TaskRun/ResponsibilityPlan exact lineage |
| DEP-AIP-ACTIVE-INSTANCES | authority 可校验 active；运行 readiness 仍按实时事实失败关闭 | 编译阶段返回 blocker，issue 阶段仍由 canonical service 复核 |
| DEP-MODULE-HANDOFF-COMPILER | 当前不存在 | 本波实现唯一 compiler 与 slot/allowlist/exact ref 校验 |
| DEP-HANDOFF-DECISION-AUTHORITY | append-only Decision、CAS、Receipt 已存在 | 本波只消费 canonical authority 并补命令 SDK/timeline 交互 |

任一依赖缺失时只展示 blocked reason，不创建本地假 Handoff、不降级到 raw payload，也不写真实租户数据。

## 6. 测试与验收矩阵

正向至少覆盖 issue → consume → accepted、issue → consume → request_more → 新 Envelope → consume → accepted、returned exact refs 回传与刷新重建。负向至少覆盖：

- token 过期、重复消费、错误 receiver、实例撤销或 revision 漂移；
- 跨租户 Task/Run/ref、超 allowlist 字段、marking 不兼容、缺权限；
- 同 key 不同 hash、并发决定 CAS 冲突、旧 Decision 版本；
- request-more 复用旧 token、修改 consumed Envelope、复制 Evidence 正文；
- reject 误取消来源 Task、accepted 误显示为 running/completed；
- org-org 正向与 dev-org 隔离，数量守恒、重启/刷新恢复和审计 timeline。

## 7. 两轮审查

第一轮发现：旧方案把 accept/reject/request-more 写成 Handoff Service 能力，并且主链仍写成 start 内编译。整改后，平台传输终态与领域决定分离，主链对齐 `prepare → Evidence Build → freeze → compile → Preview → Approval → start`。结论：`PASS_AFTER_REMEDIATION`。

第二轮反查发现：如果 request-more 只追加决定但继续沿用旧 token/Envelope，会破坏一次性传输、最新授权与可追溯性。整改后冻结“新 refs + 新 token + 新 Envelope + correlation/supersedes ref”，并明确 accepted/rejected 不等于下游执行或来源取消。结论：`PASS_AFTER_REMEDIATION`。

## 8. 2026-08-25 文件级实施清单

1. `services/aos-api/aos_api/ecommerce_workshop_handoff_contracts.py`：定义 compile 输入、exact lineage、最小披露、readiness/blocker 与 canonical issue command 输出；
2. `services/aos-api/aos_api/ecommerce_workshop_handoff_service.py`：实现唯一 `ModuleHandoffCompiler`，复用 TaskRun/ProductionContext/ResponsibilityPlan/assignee resolution 与 module manifest 事实，拒绝 slot、tenant、revision、allowlist、sender/receiver 漂移；
3. `services/aos-api/aos_api/routers/ecommerce_workshop.py`：增加只编译、不签发 token、不产生业务副作用的工作台 compile endpoint；实际 issue/consume/decision 继续调用 `/v1/aip/handoffs`；
4. `services/aos-api/tests/test_ecommerce_workshop_handoff.py`：覆盖 exact 正向、跨租户、slot/allowlist/instance/readiness 漂移和无副作用；
5. `apps/web/src/api/aipAgentControl/{contracts.ts,parser.ts,index.ts}`：补齐 issue/consume/create-decision strict command SDK；bearer 只由调用方短暂持有，不写 storage/log/Receipt；
6. `apps/web/src/api/ecommerceWorkshop/*` 与 `apps/web/src/components/workshop/TaskCockpitPage*`：消费 compiler 输出并分别展示 transport 与 domain decision，不把 consumed/accepted 映射成 running/completed；
7. `.evidence/workshop/2026-08-25-w3-06-*`：记录专项、累计、构建、内置浏览器与无外部副作用证据。

## 9. 当前决议

W3-06 已完成 code/control/browser 闭环：唯一 `ModuleHandoffCompiler`、canonical issue/consume/Decision 命令 SDK、Task Cockpit 显式受控入口和 transport/Decision 分层展示均已落地；compiler 自身保持零 durable side effect。专项前端 49 tests、后端累计 43 tests、Web 累计 220 files / 2066 tests、生产构建和 Python compile 全部通过。内置浏览器在 `/workshop/cockpit` 验收 1280px 无横向溢出；本地 `aos-api` 不可达时页面明确失败关闭，未伪造目录、空态或可执行命令。

实时 active/operational readiness 缺失时，页面和 compiler 继续给出精确 blocker；这不再构成代码缺口，但仍禁止将 code GREEN 描述成 runtime、operational 或 release GREEN。交付上限固定为 `CODE_CONTROL_BROWSER_GREEN / NO_RELEASE / NO_MIGRATION_APPLIED / NO_EXTERNAL_EFFECT`。

历史机器证据：`.evidence/workshop/2026-08-15-w3-06-handoff-decision-preflight.json` 与 `.evidence/workshop/2026-08-15-w3-06-handoff-decision-doc-ledger.json`；本波闭环证据：`.evidence/workshop/2026-08-25-w3-06-module-handoff-command.json`。
