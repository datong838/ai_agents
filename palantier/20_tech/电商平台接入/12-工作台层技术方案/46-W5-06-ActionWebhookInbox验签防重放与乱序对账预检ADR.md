# W5-06 Action Webhook Inbox 验签、防重放与乱序对账预检 ADR

> 日期：2026-08-14
> 核查基线：Workshop `w2-workshop@27c0712`，authority `AOS-000026`
> 状态：`PREFLIGHT_COMPLETED / RESEARCH_CALLBACK_PRIMITIVES_GREEN / ACTION_INBOX_BLOCKED`
> 边界：只读代码、专项测试与方案整改；未修改源代码、迁移、真实租户或外部 Provider

## 1. 结论

ResearchJob 已有可信的 HMAC、body hash、5 分钟时间窗、持久 nonce、provider revision、event sequence/gap 与 replay drift 原语，15 项邻接测试 GREEN。但 Action 侧没有 Canonical webhook inbox、provider-facing ingress、事件绑定或乱序 reducer。旧 `action_webhook` 只是可变内存请求映射工具，并可持有 bearer/basic 明文配置，不具备租户真源、不可变 Receipt 或 Secret 边界，明确禁止复用为 W5 authority。

## 2. Ingress 与租户解析

外部 Provider 不得通过 `X-Org-Id/X-Project-Id` 自报租户。每个 webhook endpoint 由不可变 `WebhookEndpointRevision` 发布，绑定 `AdapterRevision + AccountBinding + signaturePolicy + secretRef + eventSchema + maxBodyBytes + ratePolicy`。入口凭 endpoint identity/key revision 先解析唯一 tenant/account，再进入 tenant-scoped inbox；解析失败只写安全的全局拒绝指标，不回显租户存在性。

Canonical ingress 与内部 AOS Principal API 分离，具备独立限流、网络 allowlist/mTLS 可选项、超时和审计；不能为了 Provider 回调关闭内部鉴权或复用浏览器身份。

## 3. 验证前隔离

接收层先流式限制 body 大小并计算 hash，原始 bytes 只进入短期受控 quarantine；未验签内容不得 JSON 解析、路由到业务对象、写日志正文或触发状态变更。`WebhookInboxReceipt` 固化 endpoint/key revision、headers allowlist hash、body hash、receivedAt、verification result/reason 与 quarantine ref，Secret 值永不落盘。

签名策略由 Adapter revision 定义 canonical bytes、算法、headers、timestamp window、nonce/event id、key rotation overlap。Research callback 的 HMAC/nonce 原语可复用，但 Action nonce/event key 必须绑定 endpoint、provider、account 和 Adapter revision，不能共享 Research nonce 表或 authority。

## 4. 防重放与事件绑定

验签成功后以 Provider 支持的稳定键建立去重：`endpoint + providerEventId` 优先，其次 `nonce`，最后受政策允许的 `bodyHash + timeBucket`。相同键相同 hash 返回原 Receipt；相同键不同 hash 记录 drift conflict 并触发 Case，不覆盖旧事件。

解析器只消费已验证 inbox row，并通过 exact `providerRequestId/idempotencyRef/accountRef` 绑定一个 ActionExecutionAttempt。无法匹配、匹配多个、actionBindingHash 漂移或 Schema 不符进入 quarantine/ManualReconcileCase，不能猜测 Proposal。

## 5. 乱序 reducer

每个 `WebhookObservation` 同时保存 provider sequence（若有）、providerEventAt、receivedAt、event type、payload hash 与 Adapter schema revision。Reducer 按 Adapter 发布的状态偏序和 precedence 规则计算 observation view：

- 有连续 sequence：检测 gap，缺口未补齐前不越级终结；
- 无 sequence：以 provider event time + received time + event-id tie-breaker 排序，但终态冲突保持 disputed 并主动回查；
- 晚到 accepted 不得覆盖 applied/failed，重复 applied 幂等；applied 与 failed 冲突不靠“最后写入获胜”；
- Webhook 只追加 Observation/ReconcileAttempt，最终 Action/ReconcileReceipt 仍由 W5-05 reducer 写入。

## 6. 运维、留存与 UI

inbox/quarantine 设 TTL、大小上限、按 endpoint/backlog/gap/signature failure 的告警和 kill switch。删除原始 body 只按 retention policy，hash/Receipt/marking 继续保留。页面展示 verified/replayed/gap/quarantined/disputed 与回查路径，不显示原始 secret/PII；Webhook 到达不等于动作成功。

## 7. 验收

1. 伪造 tenant headers、未知 endpoint/key、过期时间、错签名、超大 body 在解析前失败关闭。
2. key rotation 新旧窗口、nonce/event replay、同 key 漂移、并发重复有确定性 Receipt。
3. unmatched/multi-match/schema drift 进入 quarantine/Case，绝不猜 Proposal。
4. 顺序、乱序、缺口、迟到、重复和终态冲突按 Adapter reducer 收敛；无 last-write-wins。
5. Webhook 不直接修改 Proposal/Receipt；最终状态仍经 exact provider reread/reconcile authority。
6. `dev-org/dev-project` 无法发现或注入 `org-org/dev-project` endpoint/event。
7. 旧 action_webhook helper 不进入 Canonical 路由、Secret、Inbox 或完成证据。

机器证据见 `.evidence/workshop/2026-08-14-w5-06-webhook-inbox-replay-ordering-preflight.json`。

## 8. 2026-08-25 实施切片与文件级清单

本轮承接 `m1@84acc76` 与 authority `AOS-000240`，只实现 canonical Action callback 控制面，不接收真实 Provider 回调、不解析真实 Secret、不执行真实迁移。实现继续遵循“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图”：Webhook Observation 只是 Action Logic 的外部观察事实，必须先绑定原 Attempt/Receipt，才能进入 W5-05 对账贡献链；它本身无权直接改写 Action 结果。

- [ ] `services/aos-api/alembic/versions/w5_005_action_webhook_inbox.py`：新增 immutable `WebhookEndpointRevision`、tenant-scoped Inbox Receipt/Observation、持久 replay key、reducer view 与 quarantine Case；endpoint public key 唯一解析租户，Secret 只存 `secretRef`，Receipt/Observation append-only，存在事实时降级失败关闭。
- [ ] `services/aos-api/aos_api/aip_action_webhook_models.py`：定义 endpoint exact refs、验签结果、Inbox Receipt、Observation、gap/disputed reducer view 与安全响应模型；禁止原始 Secret/body/PII 出现在返回合同。
- [ ] `services/aos-api/aos_api/aip_action_webhook_service.py`：按 endpoint identity 解析唯一 tenant；先限制 body 大小并计算 hash、再按 exact signature policy 与 key revision 验签，验签前不 JSON parse；稳定 providerEventId/nonce 去重，同键同 hash 幂等、不同 hash drift quarantine；verified 事件按 providerRequestId/account/actionBindingHash 精确绑定单一 Attempt。
- [ ] `services/aos-api/aos_api/aip_action_webhook_service.py`：实现无 last-write-wins 的 reducer；连续 sequence 才推进，gap 保持 awaiting_gap，迟到 accepted 不覆盖终态，applied/failed 冲突进入 disputed；只追加 Observation/Case，不直接更新 Proposal 或既有 Receipt。
- [ ] `services/aos-api/aos_api/routers/aip_action_webhooks.py` 与 `routers/domain_aggregates.py`：新增独立 provider ingress，不依赖浏览器 Principal，也不接受 `X-Org-Id/X-Project-Id` 作为租户 authority；未知 endpoint/key 使用非枚举式失败响应。
- [ ] `services/aos-api/tests/aip/test_w5_06_action_webhook_inbox.py` 与迁移测试：覆盖伪造 tenant header、未知 endpoint/key、过期/错签名/超大 body、rotation、并发 replay/drift、unmatched/multi/schema drift、顺序/乱序/gap/迟到/重复/终态冲突和跨租户隔离；验证旧 `action_webhook` 未进入 canonical authority。
- [ ] `packages/contracts/openapi/v1.generated.json`、`v1.inventory.json` 与 `.evidence/workshop/2026-08-25-w5-06-action-webhook-inbox.json`：确定性导出并封存专项、累计、compileall、Alembic、diff 证据；本波若无页面变化，浏览器明确记 `N/A_NO_UI_CHANGE`。

本波代码 GREEN 仍不等于 endpoint operational GREEN。真实 endpoint/key 发布、Secret resolver、网络入口、Provider callback、live migration、Canary、外部副作用与 release 全部保持 blocked；任何 endpoint、key、schema、account、Attempt 或 sequence 不能 exact resolve 时必须 quarantine/disputed，不得猜测租户或 Action。
