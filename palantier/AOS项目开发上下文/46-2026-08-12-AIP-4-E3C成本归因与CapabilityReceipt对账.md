# AIP-4 E3C 成本归因与 Capability Receipt 对账

> 日期：2026-08-12
> 状态：**IMPLEMENTED_GREEN**
> 代码基线：`aos-platform/m1@f7179ce`
> 真实目标：`org-org / dev-project`
> 隔离 canary：`dev-org / dev-project`（仅负向验证）

## 1. 本波结果

1. 新增 `aip4_006`，建立 tenant-scoped、RLS/FORCE RLS、append-only 的 `aip_usage_attribution` 与 `aip_capability_receipt`。
2. UsageAttribution 只能引用同租户原始 UsageReceipt 与相同 lineage；同一收据、同一归因维度的权重总和不得超过 1。
3. CapabilityReceipt 必须绑定已批准 PlanStep 中 exact revision 的 capability；TaskRun、PlanRevision、PlanStep、lineage 任一不一致均失败关闭。
4. 成本读模型按 currency 以及 measured/estimated/unknown 分桶，Adjustment 追加复算且禁止产生负有效用量，不改写原始 Receipt。
5. 硬预算只接受 measured、无估算、无未知缺口的单币种汇总；AIP-6/AIP-7 registry 尚未落地的 model/tool/agent measured 归因明确拒绝。
6. canonical API 只允许既有运行角色写入，读写均使用认证后的组织与工作区，不接受请求体伪造租户。

## 2. 主要代码

- `services/aos-api/alembic/versions/aip4_006_cost_attribution_capability_receipt.py`
- `services/aos-api/aos_api/aip_cost_attribution_service.py`
- `services/aos-api/aos_api/aip_eval_authority_store.py`
- `services/aos-api/aos_api/aip_eval_contracts.py`
- `services/aos-api/aos_api/routers/aip_cost_attribution.py`
- `services/aos-api/tests/aip/test_aip4_cost_attribution_migration.py`
- `services/aos-api/tests/aip/test_aip_cost_attribution_service.py`
- `services/aos-api/tests/aip/test_aip_cost_attribution_api.py`

## 3. 验证证据

- E3C、domain router、OpenAPI 定向范围：20 项通过。
- AIP 累计范围：105 项收集并完成。
- ruff、compileall、OpenAPI exporter 确定性检查和固定路由契约通过。
- OpenAPI：2347 paths、1586 schemas、4112 route rows、4102 unique operation pairs。
- 运行时路由：4116；固定指纹 `b67bc67147c88c3646e8f56003f9498049736b264f129419df7b0146a8372e05`。
- 开发数据库从 `aip4_005` 线性升级到单 head `aip4_006`。
- `org-org/dev-project`：UsageAttribution=0、CapabilityReceipt=0。
- `dev-org/dev-project`：UsageAttribution=0、CapabilityReceipt=0。

上述零计数表示本波只交付权威能力，没有为了验收伪造真实租户或 canary 的成本/能力事实。

## 4. 风险与边界

- model/tool/agent 的 measured 成本归因要等待 AIP-6/AIP-7 权威 registry；当前拒绝比使用 legacy 内存目录更安全。
- E3C 提供成本事实与硬预算 eligibility 读模型，不代表已实现预算扣减或自动限流。
- PostgreSQL immutable Receipt 与 Adjustment 是真值；页面或估算趋势不得覆盖它们。
- 测试退出阶段仍可能出现既有 JDBC cache logger 的 closed-stream 噪声，不影响测试进程正常完成，但后续可独立清理。

## 5. 下一门：E3D

E3D 收口 ResearchJob provider、artifact、delivery、reconcile 权威链，并执行 E3 总回归。进入编码前先复核已评审 v1.2 方案和现有 TAOR Job 实现，优先兼容扩展；provider 未注册、回调重放、事件 gap、Artifact hash 错、capability 漂移或外部状态 unknown 均必须失败关闭或进入 reconcile，不得生成虚假成功。
