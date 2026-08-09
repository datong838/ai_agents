# O1-A/P12 Payment 权威指标链补强与 D5 证据封板清单

> 状态：**P12 已实施并通过；D5-E1/E2 被前置门阻断**
> 日期：2026-08-09
> 上位方案：`O1-本体数字孪生层改造方案.md` v2.1 §5.2.11，`D5-E-G17G18G19证据闭合方案.md` v2.9
> 真实租户：仅 `org-org · dev-project`；真实租户全程不写测试 canary，不使用 Mock 伪造 GREEN。

## 1. 评审结论

本波不重新设计架构，只落实 O1 §5.2.11 已冻结的 Payment 权威读取链：

```text
P12 raw ns_pay
  -> 收集 relate_id
  -> 复用当前 P12 Source 的 source_id
  -> batch_read_public(payment_order_time)
  -> 参数化批读 ns_order(order_id, create_time)
  -> raw row 回填 _order_create_time
  -> normalize Payment
  -> apply pay_duration_min
  -> 权威存储 / Outbox / Projector
```

禁止继续使用当前“先 normalize，再通过 `store._engine` 反查已落库 Order”的偶然覆盖逻辑；禁止吞异常后让 P12 假成功。

## 2. 当前基线与根因

### 2.1 已存证据

- G17：RED。`Payment=100`，`pay_duration_min` 非空 `47`。
- 当前代码在 normalize 之后从 `ecom_object(Order)` 反查 `createdAt`，受历史 Order 落库完整性影响，不是 P12 的权威源数据链。
- 当前代码访问私有 `store._engine`，且 enrichment 失败只写 warning，违反公共契约和 fail-closed。
- 当前 `JdbcConnectorRuntime.read_rows()` 在全局缓存连接上裸设置 Session 只读，无 per-connection lease，无事务恢复/驱逐证据。

### 2.2 2026-08-09 真实源只读盘点

| 口径 | 数量 |
|---|---:|
| `ns_pay` 总数 / 有效数 | 206 / 206 |
| `pay_time > 0` 的 eligible Payment | 111 |
| eligible 中可匹配 `ns_order.relate_id = order_id` | 111 |
| eligible 中 `ns_order.create_time > 0` | 111 |
| eligible 中 `pay_time >= create_time` | 111 |

结论：源数据足以对 eligible Payment 达成 100%；当前 47/100 是执行链缺口，不是数据不可用。最终 G17 分母必须是本次权威重跑后 `Payment.properties.pay_time > 0` 的实际对象集，不得把全量 Payment 当 eligible。

### 2.3 真实写入前冲突预检（评审追加）

- 新 P12 将输入 206 个 Payment，其中已有 100 个。
- 已有 100 个全部为“同一 `source_updated_at`、不同 payload hash”，直接重跑必然 100/100 命中 `SOURCE_VERSION_CONFLICT`。
- 排除 `pay_duration_min`、`orderCreatedAt` 及其时区辅助字段后，100/100 基础源属性与新读取相同。
- 根因是旧执行器把派生指标和 enrichment 中间值写进了基础 `properties`，而代码库只有派生列/表迁移，尚无 O1 §5.2.10 冻结的派生 CAS 命令实现。

因此本波增加安全门：不得放宽同版本冲突规则；必须先完成“基础属性 / `derived_payload` 分离 + CAS + Receipt + 同事务 Outbox”，再执行 P12。

## 3. 最小实施范围

### P12-0：契约失败测试

- [x] `JdbcConnectorRuntime.read_rows_by_values()`：白名单标识符、DBAPI `%s`、500 分块、50,000 总上限、空集返回空。
- [x] 连接 lease：同连接串行，不同连接可并行。
- [x] 只读事务：成功、SQL 失败、成功三段序列的 autocommit/timeout/rollback 恢复；坏连接关闭并从缓存驱逐。
- [x] `batch_read_public()` 只接收 `spec_id + values`，调用方不能提供表名/列名。
- [x] 缺 P12 Source/source_id、未知 spec、连接错误均 fail-closed。
- [x] executor 断言 enrichment 发生在 normalize 之前，并且不访问 `store._engine`。

### P12-1：公共批读实现

- [x] 修改 `services/aos-api/aos_api/jdbc_connector_runtime.py`：增加连接 key/lease、受控批读、恢复和驱逐。
- [x] 修改 `services/aos-api/aos_api/ec_source_adapter.py`：增加不可变 `BatchReadSpec` 注册表及 `batch_read_public()`。
- [x] 修改 `services/aos-api/aos_api/ec_live_executor.py`：原始 P12 行批量丰富后再 normalize，删除对已落库 Order 和私有 engine 的依赖。

### P12-1B：派生命令和旧指标迁移（写入前新增必经门）

- [x] 严格按 O1 §5.2.10 实现 `DerivedMetricCommand` 和 `update_derived_metrics()`：完整 identity、expected revision、input revision/hash、calculator version、computed_at、actor 和 idempotency key。
- [x] 派生更新在同一数据库事务内完成 CAS、`ecom_derived_receipt`、`derived_upsert` Outbox；任一失败整体回滚。
- [x] `effective_properties = properties || derived_payload`，基础对象写入不得清空派生列。
- [x] Payment 基础写入排除 `pay_duration_min`和 `_order_create_time/orderCreatedAt`中间值；这些只作为派生计算输入/结果。
- [x] 旧 Payment 基础属性通过限定键白名单兼容迁移；结果证明基础层指标泄漏为 0、派生层 206 条齐全。
- [x] 同版本基础对象仍保持 fail-closed；只允许“移除旧派生/中间字段后基础载荷完全相同”的限定迁移，不放宽其他冲突。

### P12-2：定向验证

- [x] 契约与回归测试 GREEN：本波定向集合 69 项通过；更大相关集合此前 84/56/145 项通过。
- [x] P12 真实 Source 只读执行：206 条 Payment，111 条 eligible 全部匹配 `_order_create_time`。
- [x] 连续两次通过真实 API 重跑 P12；修复 CAS 期望版本未进入幂等键导致的真实冲突。
- [x] 新鲜证据：权威层 eligible `111/111`、投影层 canonical eligible `111/111`、负值 0、Outbox pending 0、基础属性泄漏 0。
- [ ] O1-D 别名迁移：`obj_instance.Payment` 仍有 100 条裸 ID 历史别名，导致投影总数 306、canonical 总数 206；P12 指标链通过，但 D5 封板不得通过。

### P12-3：D5-E1 / E2 与证据封板

- [ ] 先验证 `G17-SPEC`、`D4-SPEC-SYNC`、`PROJECTION-OWNERSHIP`，任一未通过禁止 `overall_pass=true`。
- [ ] D5-E1：仅运行级临时 scope 执行三类真实失败注入和 30 条 DLQ 脱敏/持久化验证。
- [ ] 跨租户 canary：覆盖 D5 §6.1/§6.4 冻结矩阵；只写临时 scope，真实 scope 仅做前后 canonical hash 和测试标识零写扫描。
- [ ] D5-E2：全量回归 G17/G18/G19，对任一 `RED/INCONCLUSIVE/NO_DATA/EXTERNAL_WRITE` 保持封板失败。
- [ ] 证据每份包含 git SHA、方案 hash、scope、UTC 时间、输入口径、计数、判定、清理状态。

### P12-4：本轮新鲜证据与 D5 阻断结论

- 证据：`services/aos-api/tests/d5e/evidence/O1-P12_Payment_20260809T093646Z.json`。
- P12 局部门：**PASS**。源端 206 条、eligible 111 条；权威层和 canonical 投影层均为 111/111（100%）。
- D5 总门：**BLOCKED**。当前不可执行并宣称 D5-E1/E2 GREEN，原因如下：
  1. O1-D 规定的 `scripts/o1_alias_migration.py` 尚不存在，100 条裸 ID 历史 Payment 投影别名尚未迁移；
  2. `G17-SPEC` 与 `D4-SPEC-SYNC` 尚未 PASS；D4 仍保留固定 `org-other/proj-other`，且未冻结 8 项指标完整 denominator/null/空集口径；
  3. `tests/d5e/` 当前只有 D5-E0 只读基线，尚无 `@pytest.mark.write` 的 30 条真实失败注入和 23 类资源 canary 实现；直接运行 `-m write` 会“零测试假通过”。

因此本轮不执行会污染真实租户或产生假 GREEN 的占位命令。下一波必须先完成 O1-D、D4 规格同步和 D5-E1 harness，再进入真实临时 scope 验证。

## 4. 回滚与风险门

- 代码回退只回退公共批读路径，不恢复私有 `store._engine` 反查。
- P12 重跑前保存 Payment 计数、有效属性 hash、Receipt/Outbox/Projector 水位；若 CAS/冲突/回退检查失败立即停止。
- 任何 canary 清理失败都是 RED；输出残留清单，不使用宽泛 SQL 清理。
- 真实 scope 发现本轮 `test_run_id` 成功写入立即 RED，不用事后删除掩盖。

## 5. 退出门

1. Payment 权威批读契约和缓存连接恢复测试 GREEN。
2. `org-org/dev-project` 本次 P12 权威重跑后，`pay_time>0` eligible Payment 的 `pay_duration_min` 非空率为 100%。
3. D5-E1 失败注入、30 条 DLQ、跨租户 canary 和真实租户零测试写入证据齐全。
4. D5-E2 仅在所有规格门、所有权门及 G17/G18/G19 全部 PASS 时封板 GREEN；否则保持 RED/BLOCKED 并给出精确下一波清单。
