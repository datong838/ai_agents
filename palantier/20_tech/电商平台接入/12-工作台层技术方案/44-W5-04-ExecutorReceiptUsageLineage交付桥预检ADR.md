# W5-04 Executor、Receipt、Usage、Lineage 交付桥预检 ADR

> 日期：2026-08-14
> 核查基线：Workshop `w2-workshop@f1c887c`，authority `AOS-000025`
> 状态：`IMPLEMENTED_CODE_CONTROL_GREEN / EXTERNAL_RESERVATION_BLOCKED / NO_EXTERNAL_EFFECT / NO_RELEASE`
> 边界：只读代码、专项测试与方案整改；未修改源代码、迁移、真实租户或外部 Provider

## 1. 结论

现有 Action Executor、不可变 ActionReceipt、AIP-4 UsageReceipt 与 Action lineage 都是可信的独立基础，后端 21 项、前端 18 项专项测试 GREEN。但它们尚未组成 W5 交付桥：Executor 在调用 Provider 前先提交 Lease consumed，崩溃可留下无 Receipt 的悬空 attempt；Action 不写 Usage；Receipt 不绑定联合依赖且 payload 未经过 Adapter output schema/脱敏；lineage 需要另行 reconcile，且当前 action receipt source hash 不覆盖完整 payload。

W5-04 的正确目标不是让数据库事务包住外部 HTTP，而是建立“调用前有 durable intent、调用后只追加事实、歧义必进 unknown/reconcile”的可恢复状态机。

## 2. Durable ExecutionAttempt

在任何 Provider I/O 前，以单事务创建不可变 `ActionExecutionAttempt` 与 dispatch outbox，并消费 Lease：

```text
prepared -> dispatch_claimed -> accepted/applied/failed/unknown
                                  \-> reconciliation_required
```

Attempt 固化 `leaseRef/proposalRef/actionBindingHash/adapterRevision/accountRef/idempotencyEnvelope/requestHash/requestArtifactRef/reservationRef`。worker 只领取 outbox，不重新解析账号或 Adapter。

外部调用无法与数据库原子提交，故采用以下失败语义：

- Provider 调用前崩溃：outbox 可安全领取；同一 attempt/envelope 不产生第二个逻辑请求。
- 调用已发出但响应未持久化：标记 `unknown`，只允许按 provider request/idempotency ref 查询；不得盲重试。
- Provider 不支持稳定幂等或状态查询：capability 必须降为 manual reconcile 或 disabled，不能用自动重试伪造 exactly-once。
- Attempt 已有终态 Receipt：任何 replay 只回读，不再次调用 Provider。

## 3. Adapter outcome 与 ActionReceipt

Adapter outcome 必须通过发布时锁定的 output/receipt schema。原始 Provider 响应先进入受控 Artifact，执行 secret/PII/marking/大小/恶意内容策略；ActionReceipt 只保存安全摘要和 exact refs/hash。

ActionReceipt 至少固定：

- `attemptRef/leaseRef/proposalRef/previewRef/actionBindingHash`；
- `capabilityBinding/accountBinding/adapterRevision/approvalSet/reservation` exact refs；
- provider/idempotency/request/response hashes 与 provider request ref；
- outcome、quality、occurredAt/observedAt、evidence/artifact refs；
- Usage receipt refs、lineage source ref、schema revision 和 redaction policy ref。

Receipt 继续 append-only；reconcile 或 adjustment 只能追加 superseding Receipt，不能修改历史。unknown 不携带伪造的 applied 结果或 0 成本。

## 4. Usage 与预算结算

Adapter contract 返回受 schema 约束的 Usage envelopes。Action delivery bridge 将 ActionReceipt、UsageReceipt/unknown Usage、reservation settlement command 与 lineage projection request 在同一数据库提交中登记：

- measured/estimated 使用正确 unit/currency/source hash；
- Provider 未返回用量时写 `quality=unknown`，不写 quantity=0；
- applied 与 cost-settled 是两个状态维度。外部动作已成功但 Usage 不完整时保留 applied 事实，同时将 settlement 标为 pending/unknown；
- measured Usage 结算 reservation，多退少补走策略；unknown 保留或转人工，不静默释放预算；
- 后续账单调整通过 UsageAdjustment 和 SettlementReceipt 追加，不改原 Receipt。

## 5. Lineage

ActionReceipt 成为 Action lineage 的权威 source。交付事务写入 deterministic lineage projection request；projector 以 Receipt 完整 canonical hash（含受控 payload/artifact hash和所有 exact refs）幂等追加事件。Projection 延迟不改变 Action delivery 状态，但 UI 显示 `lineagePending`，不能假装谱系已完成。

Action 页面直接携带 `rootType=action/rootId=proposalId/lineageId`，不让用户手工猜 ID。Action、Usage 和 settlement 通过 exact refs 汇合，不复制第二套事件事实。

## 6. UI 与状态诚实性

审批台分别显示：`executionAttemptStatus`、`providerOutcome`、`usageSettlementStatus`、`lineageProjectionStatus`。只有不可变 ActionReceipt 可证明 Provider outcome；只有 Usage/Settlement Receipt 可证明费用结算；只有 lineage event 可证明谱系已投影。任一 pending/unknown 保持可见并给出 reconcile 路径。

## 7. 验收

1. 在 consume Lease、claim outbox、Provider 调用前后、Receipt 提交前后注入 crash，均无盲重试或无主悬空状态。
2. 相同 attempt/envelope 并发只产生一次逻辑 Provider 请求；不支持幂等/查询的 Adapter 自动 disabled/manual。
3. output schema、secret/PII、hash、marking 或 exact binding 不合格时失败关闭，同时不丢失已发生的外部事实。
4. ActionReceipt、UsageReceipt、SettlementReceipt 与 lineage 可回到同一 attempt/actionBindingHash。
5. unknown usage 不写 0；applied 与 settlement pending 可并存且 UI 不混淆。
6. lineage source hash 覆盖完整受控 Receipt 内容，重复投影幂等、漂移冲突失败关闭。
7. 当前没有生产 Adapter 或 W5-00～03 GREEN 前，不做真实正向执行。

机器证据见 `.evidence/workshop/2026-08-14-w5-04-executor-receipt-usage-lineage-preflight.json`。

## 8. 2026-08-25 实施切片与文件级清单

本轮在 `m1@7c6975c`、authority `AOS-000238` 上实施，保持既有 AIP-3B API 兼容，不把内部测试 Adapter 当成生产 Adapter，不触发真实 Provider。实现遵循“原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图”：Executor 仅消费已经由上游 Action Logic 固化的 Proposal/Lease，新增的 Attempt、Receipt、Usage 与 lineage request 都是可追溯贡献事实，不新增第二套业务 authority。

- [x] `services/aos-api/alembic/versions/w5_003_action_delivery_bridge.py`：新增 tenant-scoped durable Attempt/outbox、delivery bridge 状态与 exact Receipt 字段；不可变事实禁止更新/删除，降级遇事实失败关闭。
- [x] `services/aos-api/aos_api/aip_action_execution.py`：先持久化 intent/outbox 再 claim；近期 in-flight 重入诚实显示 claimed，claim 超过恢复窗口仍无 Receipt 才进入 unknown，且不自动二次调用；Receipt、Usage、settlement 与 lineage projection request 同事务登记。
- [x] `services/aos-api/aos_api/aip_action_models.py`：兼容扩展执行视图，分别公开 attempt/provider/usage-settlement/lineage 状态及 exact refs/hash。
- [x] `scripts/export_openapi.py`、`packages/contracts/openapi/v1.generated.json`、`v1.inventory.json`：消费 W5-03 已新增但尚未进入快照的 3 个 Draft command routes，并确定性导出本波执行视图 schema；核查没有其他 route drift。
- [x] `services/aos-api/aos_api/aip_lineage_service.py`：ActionReceipt source hash 覆盖完整受控 Receipt 内容及联合 binding；重复投影幂等、内容漂移失败关闭。
- [x] `services/aos-api/tests/aip/test_w5_04_action_delivery_bridge.py` 与相邻回归：覆盖 crash window、幂等 replay、unknown usage 非 0、三状态分离、tenant isolation、完整 lineage hash 与迁移约束。
- [x] `.evidence/workshop/2026-08-25-w5-04-executor-receipt-usage-lineage.json`：专项 5、累计 99、OpenAPI 13、Alembic head、编译和 diff 全 GREEN；本波无页面改动，浏览器为 `N/A_NO_UI_CHANGE`。

实现判定仍分层：代码与测试 GREEN 只允许标记 `CODE_CONTROL_GREEN`；W5 external Lease 仍由 W5-03 的预算 reservation authority 门失败关闭，因此不得由本波推导 operational GREEN、真实外部效果或 release。

## 9. 完成复审

方案与实现一致：Provider I/O 前已有 durable intent；近期并发 replay 不误判 unknown，stale claim 不盲重试；Receipt/Usage/settlement/lineage 的 exact refs 与状态各自可读，unknown Usage 为 `quantity=NULL`；响应 secret/token 字段进入受控 Artifact 前脱敏；exact external Adapter 只接受 suite-GREEN published revision。既有内部 Action API 与 99 项累计回归未倒退。结论为 `W5_04_DURABLE_ATTEMPT_EXACT_DELIVERY_BRIDGE_CODE_GREEN_EXTERNAL_RESERVATION_BLOCKED_NO_EXTERNAL_EFFECT_NO_RELEASE`，下一入口为 W5-05。
