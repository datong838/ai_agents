# W5-01 Adapter Capability Contract Suite 预检 ADR

> 日期：2026-08-14（2026-08-25 于 `m1` 开始实施）  
> 核查基线：`m1@c785f15`，项目 authority `AOS-000235`  
> 状态：`CODE_CONTROL_GREEN / PURE_CONTRACT_AND_ZERO_SIDE_EFFECT_SUITE / NO_PRODUCTION_PUBLICATION`  
> 边界：只读代码审查、测试与方案收敛；未修改源代码、迁移、数据库、真实租户或外部 Provider

## 1. 结论

现有代码有三组可复用安全片段：Action 的单次 Lease/Receipt/unknown-reconcile，ResearchJob 的 callback 签名/nonce/provider reread，以及 UsageReceipt 的质量分桶。但 `ActionAdapter` 当前只有 `execute(payload, idempotency_key)` 与 `reconcile(provider_request_id, request_fingerprint)`，没有不可变定义、dry validation、账号解析、Schema、Usage、Webhook、partial/cancel 或发布门。

因此 W5-01 不是为某个平台写几项单测，而是建立一个领域中立、参数化、生产发布强制执行的 Adapter conformance harness。69 项邻接测试通过只证明上述片段稳定，不能证明任何真实电商 Adapter 合规。

## 2. 两层契约

### 2.1 不可变 `AdapterCapabilityRevision`

至少固定：

```text
adapterId / revision / contentHash / lifecycle
provider / accountKind / capabilityRef / actionTypeFamily
inputSchemaRef / outputSchemaRef / receiptSchemaRef / usageSchemaRef
riskFloor / idempotencyDomain / timeoutPolicy
dryValidateMode / reconcileMode / cancelMode / partialMode
webhookContractRef / ratePolicyRef / capacityPolicyRef
licensePolicyRef / redactionPolicyRef / readinessPolicyRef
```

它作为 PlatformAdapterPack 的签名资产进入 installation lock。CapabilityBinding 只引用已发布且 hash 一致的 revision；测试类注册、进程内对象和 provider 名称不能成为版本 authority。

### 2.2 运行接口

```text
resolveAccount(exact AccountRef) → AuthorizedAccountContext
dryValidate(exact proposal/preview/account/binding) → DryValidationReceipt
execute(exact lease, validated fingerprint, idempotency key) → ProviderOutcome
reconcile(provider request ref, fingerprint) → ReconcileOutcome
cancel(...) → CancelOutcome           # 仅声明支持时
verifyWebhook(signed envelope) → InboxEventCandidate
normalizeUsage(...) → UsageReceiptCandidate
```

Adapter 不接收裸 TenantScope、Secret、任意账号选择器或浏览器 Cookie；Secret 由受控 resolver 在最后一跳解析，且不进入 DTO、日志、Receipt 或测试快照。

## 3. 参数化 Contract Suite

每个 production Adapter revision 必须以相同 fixture 接口运行以下套件：

| 组 | 必测内容 |
|---|---|
| 定义 | Schema/hash/lifecycle/exact refs；unknown 字段与 drift 失败关闭 |
| 账号安全 | 同租户、错租户、账号禁用、Secret ref、marking/purpose、无 Cookie 泄漏 |
| Dry validation | 权限、对象范围、quota、capacity、rate、成本、可逆性、reconcile 模式 |
| 输入输出 | 输入、Provider 响应、Receipt payload 和状态严格 Schema；恶意/超大 payload |
| 幂等 | 同 envelope 重放一次执行；同 key 不同 payload 冲突；Provider 幂等域一致 |
| 生命周期 | accepted/applied/failed/unknown；timeout 后不自动重发 |
| Reconcile | 仅受信 Provider reread；request fingerprint 对齐；非终态保持 unknown |
| Partial/cancel | capability 声明与实际一致；部分结果、取消竞态和 Receipt 守恒 |
| Webhook | tenant inbox、签名、时间窗、nonce、防重放、乱序、重复和晚到事件 |
| Usage/预算 | measured/estimated/unknown、币种/单位、reservation、结算、对账漂移 |
| Kill/容量 | org/project/account/action type kill、执行前复验、并发与限流 |
| 回滚 | 新 revision 失败时回到 prior installed revision；历史 Receipt/Lineage 保留 |

套件必须包含零外部副作用的 deterministic fake provider，以及由 provider owner 在隔离 sandbox 执行的认证测试；真实租户 canary 不属于 W5-01，留到 W5-07。

## 4. 统一状态与错误语义

Provider 原始状态只能归一为 `accepted/applied/failed/unknown`，批量能力另附 item-level partial，不允许 Adapter 自造“success-like”值。错误至少分 validation、auth/account、rate/capacity、provider rejected、timeout/transport unknown、schema drift、signature/replay、reconcile unavailable、usage unknown；返回安全 reasonCode，原始敏感响应进入受控 Artifact/Evidence。

重试安全是 revision 契约，不由调用者猜测。unknown 永远先 reconcile；没有 provider request ref 或可靠查询时保持 unknown/manual reconcile，不以失败或成功收口。

## 5. 发布门

1. Suite 结果绑定 `adapterId/revision/hash + capability revision + provider sandbox identity`。
2. 全部必需项 GREEN 才能发布 revision；部分能力用声明关闭，而不是跳过测试后冒充支持。
3. CapabilityBinding 只有在发布结果、账号 health、网络/配额与政策均 GREEN 时才可 `available`。
4. 测试报告过期、Adapter/Schema/Provider API revision 漂移立即使 readiness stale。
5. Workshop 只消费 capability readiness、DryValidation/Receipt/Usage refs 和稳定 blocker，不识别具体 Provider 分支。

## 6. 禁止替代

- 不复用 legacy `action-webhook` 进程内引擎作为 Canonical inbox；只借鉴签名/防重放思想。
- 不把 ResearchJob callback 直接当 Action Webhook authority；两者共享安全原语但保持各自事件真源。
- 不以测试中 `ACTION_ADAPTERS.register(fake)` 证明生产注册完成。
- 不让每个 Module 建自己的 Adapter interface、错误码、重试或 Usage 表。
- 不在 W5-00 未 GREEN、W4-08 未通过时进入生产 Adapter 编码或真实账号验证。

## 7. AOS-000235 实施决策

W5-00 已将“矩阵合同冻结”与“真实外部行可执行”拆开。W5-01 只交付可被后续持久 authority 复用的纯合同、严格 exact-ref 解析边界和 deterministic conformance harness；不建立生产 Adapter 已发布或外部行已可执行的虚假结论。

### 7.1 不变量

1. 旧 `ActionAdapter.execute/reconcile` 和 `ACTION_ADAPTERS.register/get` 保持兼容，现有 Proposal/Lease/Receipt 测试不倒退。
2. 新合同必须 immutable、`extra=forbid`、camelCase 序列化，并对 exact ref 类型、hash 和声明的支持能力做服务端校验。
3. 合规 harness 只允许 `deterministic://` sandbox identity 且 adapter 显式声明 `side_effect_free=true`；否则在任何 execute 之前失败关闭。
4. timeout/transport 不允许自动重发；`unknown` 必须有 provider request ref 才可 reconcile，非终态仍保持 unknown。
5. Account 只暴露 opaque secret ref，合同和测试不接收 Secret/Token/Cookie 明文。
6. Workshop 后续只消费 contract/report/readiness blocker，不为 Provider 分支建第二套状态机；与 163/164 的“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图”保持单向消费。

### 7.2 文件级清单

- 新增 `services/aos-api/aos_api/aip_adapter_contracts.py`：定义 `AdapterCapabilityRevision`、`AuthorizedAccountContext`、`AdapterInvocationEnvelope`、`DryValidationReceipt`、`NormalizedUsageCandidate` 及严格枚举。
- 新增 `services/aos-api/aos_api/aip_adapter_conformance.py`：定义 deterministic fixture/protocol/report 和失败关闭的 suite runner。
- 最小修改 `services/aos-api/aos_api/aip_action_adapters.py`：在不破坏 legacy registry 的前提下，增加仅接受 GREEN conformance report 的 exact in-memory revision registry，它只是后续持久 authority 的运行边界原型。
- 新增 `services/aos-api/tests/aip/test_w5_01_adapter_capability_contracts.py`：覆盖 immutable/unknown-field/hash-drift/exact-type/account isolation/dryValidate/idempotency/unknown-reconcile/usage/非 deterministic 拒绝/registry drift。
- 更新本 ADR、D-waves、机器证据、Delivery Receipt、authority 与 Prime 投影。

### 7.3 明确排除

- 不新增数据库迁移或 HTTP 写路由；
- 不解析真实账号、Secret 或网络配置；
- 不调用 Provider，不创建 Proposal/Approval/Lease/Action/AgentRun/Handoff；
- 不把 in-memory conformant registry 写成 production publication authority；
- 不执行 canary、kill drill、发布或真实租户业务变更。

历史预检证据见 `.evidence/workshop/2026-08-14-w5-01-adapter-contract-suite-preflight.json`；实施证据将写入 `.evidence/workshop/2026-08-25-w5-01-adapter-capability-contract-suite.json`。

## 8. 实施与验收结论

### 8.1 已交付

1. `AdapterCapabilityRevision` 为 frozen/strict/camelCase 合同，自身 `contentHash` 从排除 hash 字段的规范 JSON 计算，任何定义漂移都会拒绝。
2. Capability/Schema/Rate/Capacity/License/Redaction/Readiness 全部使用 exact revision ref；`dryValidate` 必须 required，`reconcile` 不得 unsupported。
3. `AuthorizedAccountContext` 只接受 `AccountRevision` 和 `secret://` opaque ref；`AdapterInvocationEnvelope` 固定 Proposal/Lease/Capability/Account，并递归拒绝 secret/token/cookie/password/authorization/apiKey 字段。
4. deterministic harness 在执行前校验 sandbox identity、`side_effect_free`、adapter revision 和 capability exact ref；然后校验账号租户/用途/marking、dry validation fingerprint、状态归一、同 key 幂等重放、unknown reconcile 和 usage request ref。
5. `ActionAdapterRegistry` 保留旧 name-based API，新 exact registry 只接受与 revision 精确对齐的 GREEN report；不得冒充持久发布 authority。

### 8.2 验证

- W5-01 专项：`19 passed`；
- Action 累计回归：`84 passed`，覆盖 Action control/execution/tool exits/growth connectors/binding 及新 contract suite；
- Python `compileall`、JSON/文档/patch `diff --check`：GREEN；
- 新增逻辑无 HTTP route 和页面，故内置浏览器验收不适用；不以 fixture 冒充生产 Provider 或账号证据。

### 8.3 一致性与剩余边界

- 与 163/164 一致：Adapter 是原子 Skill 进入 Logic/Agent/Workshop 前的受控运行资产，不是新的数字同事或工作台 authority。
- 本次 GREEN 只证明合同与 deterministic conformance code-control；生产 Adapter publication、Account resolver、持久绑定、Action budget、Webhook、canary 和发布仍未 GREEN。
- 下一任务为 W5-02 ImpactPreview exact binding，必须继续保留旧 Action 链回归与无外部副作边界。

实施证据：`.evidence/workshop/2026-08-25-w5-01-adapter-capability-contract-suite.json`。
