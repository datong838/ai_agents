# W7-08 Capacity、Budget、Usage、取消与最终对账预检 ADR

> 日期：2026-08-15  
> 决策：`IMPLEMENTATION_ACTIVE / CONTRACT_BASELINE_APPROVED / NO_EXTERNAL_EFFECT / NO_RELEASE`  
> 当前基线：`AOS-000263`；`m1@e9a6278a`；W7-07 已按 `W7_07_MEDIA_PROVIDER_ADAPTER_MALICIOUS_ASSET_CODE_CONTRACT_BROWSER_GREEN_SECURITY_SCOPED_GREEN_REPO_BASELINE_RED_NO_REAL_PROVIDER_NO_EXTERNAL_EFFECT_NO_RELEASE` 闭合  
> 前置：W7-07 code/control/browser GREEN；AIP Capacity、Budget、Usage 与媒体 Provider attempt 只按 exact ref 接缝复用，不建立 Workshop 第二真源

## 1. 审查问题与事实

W7-08 不是“已经有 Capacity 和 Usage 服务，所以把字段接到页面”。它要求一次媒体收费 attempt 从资源与预算预留、Provider 调用、取消/迟到回包，到最终用量成熟和差异解释都可追踪、可干预、可对账。

基于 `m1@e9a6278a39299f048a25994e41e280f78ec64fa1` 与 `AOS-000263` 的重新核查：

- AIP-7 Capacity 能按租户、Route、Model、Provider 防止池超卖，AgentRun 转移失败可释放未消费预留；
- UsageReceipt 支持 measured/estimated/unknown，UsageAdjustment append-only，Provider usage bridge 要求 Provider Receipt；
- Cost attribution 不把 unknown 冒充 hard-budget eligible measured cost；
- 22 项容量、状态转移、Usage、归因与 Provider bridge 定向测试通过。

这些是四套可复用基础，不是媒体结算闭环。当前 Capacity 以 AgentRun 为键且仅覆盖并发/token，未绑定 `TaskRun + stepKey + attempt + requestFingerprint`；BudgetRevision 只有限额 authority、没有媒体 attempt 预留；UsageReceipt 没有媒体 binding；最终 Settlement authority 和 Media Studio 成本视图仍不存在。W7-07 已 GREEN，但其 `usageReceiptRef` 仍只是 Provider Receipt 上的可选 exact ref，尚未形成容量、预算、取消与结算守恒，因此 W7-08 必须继续实现，不能把 W7-07 冒充本波完成。

## 2. 决策

### 2.1 联合绑定但不合并 authority

以不可变 `MediaAttemptBindingHash` 联合以下事实：tenant、TaskRun、stepKey、attempt、request fingerprint、Artifact/partial refs、Capability/Route/Provider/Price/Policy exact refs。四类 authority 各自负责：

1. CapacityReservation：资源供应能力；
2. BudgetReservation：获批的按币种风险敞口；
3. UsageReceipt：Provider 使用事实；
4. SettlementDecision/UsageAdjustment：成熟、调整、退款、争议与核销。

任一 authority 不得反推或覆盖另一 authority。

### 2.2 收费提交组合门

收费 Stage 必须同时满足有效 Stage lease/fence、CapacityReservation、BudgetReservation 和 durable Attempt/outbox。Capacity scope 固定 TaskRun/step/attempt/request，并使用版本化适用维度；Budget 固定 confirmed recommendation、ProjectedCostRange、币种、价格、数量/Stage、重试/冗余、税费/许可证 unknown、审批和 expiry。提交后不明必须先 reconcile，禁止换幂等键重发。

### 2.3 Usage、取消与迟到事实

每个 Provider Receipt 追加 UsageReceipt，并绑定 exact attempt、Artifact/partial、request、Capacity/Budget refs。取消拆成 CancelIntent、Adapter 响应、Provider 最终状态和费用结论；本地 cancelled 不等于 Provider 停止或零费用。迟到 webhook/Receipt 通过 request fingerprint、provider sequence、attempt fence 去重归并，不能删除原 Usage 或覆盖旧事件。

### 2.4 最终对账

SettlementDecision 与 UsageAdjustment append-only 地推进 measured/estimated/unknown、adjusted/refunded/disputed/written-off。unknown 在成熟前计入组织可配置风险敞口；partial、失败、取消和失效 Stage 的费用不得隐藏。最终差异按币种分桶展示 projection、measured、estimated、unknown、adjustment、refund、tax、residual dispute，不自动换汇。

## 3. UI 与验收

Media Studio 应展示双预留、Stage/attempt Usage、取消结果、迟到 Receipt、Adjustment/Settlement 和最终按币种差异；unknown/争议/待对账不可合并进成功态。验收至少覆盖：容量超卖、预算并发、submit crash window、cancel too-late、迟到回包、partial Artifact、unknown 成熟、退款/调整、多币种、重试/接管、`org-org/dev-project` 正向与 `dev-org/dev-project` 隔离 canary。

## 4. 两轮审查

### 第一轮：边界与一致性

- Capacity 与 Budget 已分离；预计成本与实际账单不混用；
- Usage、取消和最终结算均有独立、append-only 事实；
- attempt/Provider/Artifact/price/policy exact refs 能形成联合 binding；
- 对取消、迟到回包、unknown、partial、多币种均失败关闭。

结论：`PASS`。

### 第二轮：可实现性与防越门

- 复用现有通用 Capacity/Usage/Attribution authority，不建立 Workshop 第二真源；
- 新增媒体维度、BudgetReservation、atomic join、settlement reducer 前保持 disabled；
- W7-07、后端专项、前端投影与双租户证据未闭合时不勾选 W7-08；
- 不以 22 项基础测试冒充 W7-08 交付测试。

结论：`PASS_WITH_IMPLEMENTATION_BLOCKED`。

## 5. 2026-08-25 文件级实施清单

本轮只新增媒体 attempt 的治理 authority 与只读贡献投影，不调用真实 Provider、不 live apply migration、不修改真实业务数据：

1. `services/aos-api/alembic/versions/w7_006_media_finance_settlement.py`：新增 tenant-scoped、RLS/FORCE RLS、append-only 的媒体预留、取消事实、Usage binding、Settlement decision 与幂等 Receipt 表；迁移可逆检查必须拒绝有 authority 数据的降级。
2. `services/aos-api/aos_api/aip_media_finance_contracts.py`：冻结 `MediaAttemptBindingHash`、Capacity/Budget 双预留、CancelObservation、UsageBinding、SettlementDecision、币种分桶与风险敞口守恒；unknown 不得伪造金额，跨币种不得相加。
3. `services/aos-api/aos_api/aip_media_finance_store.py`：以 Principal 派生租户、exact refs、幂等键与 expected version/CAS 写入 append-only authority；列表读取必须按租户隔离。
4. `services/aos-api/aos_api/aip_media_finance_service.py`：组合 W7-07 Job exact refs，prepare 只冻结预留；Provider submit 前要求同 attempt 双预留有效；取消只追加 intent/observation，不推导零费用；Settlement 只消费 canonical Usage exact refs。
5. `services/aos-api/aos_api/routers/aip_media_finance.py` 与 API 路由注册：提供受角色约束的 prepare/cancel/usage/settle 命令和 GET-only 回读；保持 `NO_REAL_PROVIDER`。
6. `services/aos-api/aos_api/ecommerce_workshop_media_studio_contracts.py`、`ecommerce_workshop_media_studio.py`：增加按 Job 的 Capacity/Budget/Usage/Cancel/Settlement 贡献视图，继续展示“原子 Skill → Logic → 数字同事绑定 → 工作台贡献”，unknown/争议/币种分桶分轴可见。
7. `apps/web/src/.../media-studio*`：strict parser 与只读 UI 增量；不增加执行、取消、结算按钮。
8. `services/aos-api/tests/aip/test_w7_08_media_finance_settlement.py`、Workshop/API/OpenAPI/Web 测试与浏览器证据：覆盖双预留、并发/CAS、取消 too-late、迟到 Usage、partial、unknown 成熟、退款/调整、多币种、跨租户、刷新恢复与零外部副作用。

兼容规则：W7-07 ProviderJob、旧 v1/v2 Media Studio 响应和既有 AIP Capacity/Budget/Usage authority 均保持；新增合同采用可选贡献区与新 v3 schema，旧 strict parser 明确兼容 v1/v2，不隐式提升运行许可。

## 6. 最终裁决

产品与技术合同已收敛，W7-07 前置已满足，W7-08 进入最小实现。代码 GREEN 仍只表示合同、离线迁移、测试与浏览器投影闭合；在真实 Provider、真实租户 migration apply、运营批准与发布门之前，必须保持 `NO_EXTERNAL_EFFECT / NO_RELEASE`。历史预检证据仍保留在 `.evidence/workshop/2026-08-15-w7-08-capacity-budget-usage-cancel-settlement-preflight.json`，不得覆盖。
