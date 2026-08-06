# D4 Phase A 改动清单（冻结 · 编码依据）

> 配套：D4-12OT业务闭环与302表衔接执行规格.md §7 Phase A
> 基线：m1@c7725ae（aos-platform）；m1@f48551f（docs）
> 原则：所有修改为**追加和松绑**，不删除或改写旧逻辑。不破坏 D1/D1.5 的 478 条基线。
> 用户决策（2026-08-06）：
>   - Payment 的 pay_duration_min 跨表 → **管道内完成**（normalize 阶段关联查 Order.create_time）
>   - A5~A9 标准链路测试 → **放一个文件**（不分拆）

---

## 总体改动概览

| 类型 | 文件数 | 明细 |
|---|---|---|
| 追加（现有文件） | 4 | ecom_core_models.py / ec_normalizer.py / ec_derived_metrics.py / ec_live_executor.py |
| 松绑（现有测试） | 1 | test_ec_d1_5_customer_lite_ot.py（==8 → >=8） |
| 新增测试 | 6 | test_ec_d4_p09~p12（4份）+ test_ec_d4_e2e_validation + test_ec_d4_standard_pipeline_links |
| **合计** | **11** | 全部为追加/松绑/新增，0 删除 |

---

## A1 · CORE 契约注册（5 个文件）

| # | 文件路径 | 改动类型 | 具体内容 |
|---|---|---|---|
| A1-1 | aos-platform/services/aos-api/aos_api/ecom_core_models.py L27 | 追加 | CORE_OBJECT_TYPES frozenset +4：`Weapp`, `SystemConfig`, `ProductReview`, `Payment`（8 → 12） |
| A1-2 | 同上 L35 | 追加 | CORE_LINK_TYPES dict +6 条新 Link（8 → 14）：<br>- `Shop.hasWeapp`: (Shop, Weapp)，关联字段 site_id<br>- `Product.hasReview`: (Product, ProductReview)，关联字段 goods_id<br>- `ProductReview.ofSku`: (ProductReview, ProductSku)，关联字段 sku_id<br>- `ProductReview.byMember`: (ProductReview, CustomerLite)，关联字段 member_id<br>- `Order.hasPayment`: (Order, Payment)，关联字段 out_trade_no 或 relate_id≈order_id<br>- `Order.fromWeapp`: (Order, Weapp)，关联字段 weapp_id<br>**注**：规格 §3.5 列 7 条含 `Product.inCategory`，但该 Link 已在 D1 落地（代码 L40 已存在），D4 仅验证不重复注册 |
| A1-3 | 同上 L47 | 追加 | REQUIRED_PROPERTIES +4（保持 set(keys) == set(CORE_OBJECT_TYPES) 断言成立）：<br>- `Weapp`: frozenset({"appId", "name", "status", "updatedAt"})<br>- `SystemConfig`: frozenset({"siteId", "module", "key", "updatedAt"})<br>- `ProductReview`: frozenset({"productId", "memberId", "score", "updatedAt"})<br>- `Payment`: frozenset({"orderId", "outTradeNo", "payStatus", "updatedAt"}) |
| A1-4 | aos-platform/services/aos-api/aos_api/ec_normalizer.py L54 | 追加 | _PIPELINE_ID_TO_OT +4：`p09→Weapp`, `p10→SystemConfig`, `p11→ProductReview`, `p12→Payment` |
| A1-5 | aos-platform/services/aos-api/aos_api/ec_derived_metrics.py L52 | 追加 | _PIPELINE_ID_TO_OT +4（同上，两处保持一致） |
| A1-6 | aos-platform/services/aos-api/aos_api/ec_derived_metrics.py L106-L121 | 追加 | apply_derived_metrics if-elif +2 分支：<br>- `ProductReview → _apply_review_quality_bucket(row)`<br>- `Payment → _apply_pay_duration_min(row)` |
| A1-7 | 同上（文件末尾追加） | 新增 | 两个派生指标函数：<br>- `_apply_review_quality_bucket(row)`: score≥4.5→"high" / ≤3→"low" / 其他→"mid"，写入 row.properties.review_quality_bucket<br>- `_apply_pay_duration_min(row)`: (Payment.pay_time − Order.create_time) 分钟差，写入 row.properties.pay_duration_min；**管道内完成**：normalize 阶段关联 ns_pay.relate_id≈order_id 查 ns_order.create_time，结果挂到 row._order_create_time，派生函数直接读 |
| A1-8 | aos-platform/services/aos-api/tests/test_ec_d1_5_customer_lite_ot.py L56 | 松绑 | `assert len(CORE_OBJECT_TYPES) == 8` → `>= 8`（跨波累积契约语义，守护 D1.5 基线全注册即可） |

### A1 风险
- **低**。全是追加，唯一松绑点 ==8→>=8，符合 project_memory 跨波累积契约规则。
- test_ec_d1_core_link_types.py 的断言已是 >=7 松绑语义，无需再改。

---

## A2 · 4 份 TDD 测试 RED（4 个新文件）

模板参考：test_ec_d1_p01_shop.py（FakeStore + mock 策略 + 6 case 结构）。
mock 策略：fetch_source_rows mock normalized 行（绕过 MySQL）；persist_dataset mock no-op；FakeStore 注入模拟一致性内核。

| # | 文件路径（新增） | 源表 → OT | 5 case 覆盖 | 额外覆盖 |
|---|---|---|---|---|
| A2-1 | aos-platform/services/aos-api/tests/test_ec_d4_p09_weapp.py | ns_weapp → Weapp<br>主键：weapp_id<br>唯一键：niushop:1:{weapp_id}<br>增量：每日快照（全表量小） | 初装(全量) / 增量(快照重跑) / 重跑(幂等) / 断点(checkpoint CAS) / 越租户(拒绝) | Link: Shop.hasWeapp（site_id 关联） |
| A2-2 | aos-platform/services/aos-api/tests/test_ec_d4_p10_system_config.py | ns_config → SystemConfig<br>逻辑键：site_id + app_module + config_key + (weapp_id?)<br>唯一键：niushop:1:{site_id}:{app_module}:{config_key}(:{weapp_id})<br>增量：每日快照 | 同上 5 case | Config JSON value 字段正确解析 |
| A2-3 | aos-platform/services/aos-api/tests/test_ec_d4_p11_product_review.py | ns_goods_evaluate → ProductReview<br>主键：id<br>唯一键：niushop:1:eval_{id}<br>增量：(create_time, id) + 每日重扫 24h 窗口 | 同上 5 case + 24h 回扫捕获追评 | 3 Link: hasReview / ofSku / byMember<br>派生指标: review_quality_bucket（score≥4.5→high / ≤3→low / 其他→mid） |
| A2-4 | aos-platform/services/aos-api/tests/test_ec_d4_p12_payment.py | ns_pay → Payment<br>主键：id<br>唯一键：niushop:1:pay_{id}；次要唯一键 out_trade_no<br>增量：(pay_time, id)→0 回退 create_time；每小时重扫 24h 捕获异步通知状态变更 | 同上 5 case + 24h 重扫 | Link: Order.hasPayment（out_trade_no 或 relate_id≈order_id）<br>派生指标: pay_duration_min（Order.create_time→Payment.pay_time 分钟差，**管道内关联完成**）<br>PII 脱敏：支付凭证号 / 真实流水号脱敏写入 |

---

## A3 · 管道配置工厂 + SourceAdapter normalize 映射（追加，4 个文件）

| # | 文件路径 | 改动类型 | 具体内容 |
|---|---|---|---|
| A3-1 | aos-platform/services/aos-api/aos_api/ec_normalizer.py | 追加 | P09~P12 的 normalize 映射函数（源表字段 → OT properties），参考现有 P01~P08 的 _normalize_shop / _normalize_product 模式：<br>- _normalize_weapp: ns_weapp → Weapp properties<br>- _normalize_system_config: ns_config → SystemConfig properties（JSON value 字段保留原始 JSON）<br>- _normalize_product_review: ns_goods_evaluate → ProductReview properties（含 score 字段 → 派生 review_quality_bucket）<br>- _normalize_payment: ns_pay → Payment properties，**管道内关联 Order.create_time**：<br>&nbsp;&nbsp;· 读 ns_pay.relate_id（≈order_id）→ 查 ns_order.create_time<br>&nbsp;&nbsp;· 结果挂 row._order_create_time（内部字段，不进 properties）<br>&nbsp;&nbsp;· pay_time 和 create_time 都转 unix 秒计算分钟差，写入 row.properties.pay_duration_min |
| A3-2 | aos-platform/services/aos-api/aos_api/ec_live_executor.py | 追加 | SourceAdapter 为 4 个新源表加字段映射 + PII 脱敏：<br>- ns_weapp: 无需额外脱敏<br>- ns_config: value 是 JSON，内部可能含支付密钥？需检查：如果含 key=pay_key/secret/credentials 类键值，做脱敏标记（仅脱敏引用，不落明文）<br>- ns_goods_evaluate: member_id 不脱敏（member_id 是整数 ID，不是 PII）；评价文本如需脱敏，按 _PII_PATTERNS 顺序（长 pattern 先匹配：身份证 15-18 位 → 手机号 11 位）<br>- ns_pay: PII 重点：支付凭证号（如 bank_card_last4 仅保留后 4 位）、真实流水号脱敏，参考 _PII_PATTERNS |
| A3-3 | 在 A2 的 4 个测试文件内 | 新增 | 管道配置工厂（写在测试内不新建独立文件，最小更改），参考 test_ec_d1_p01_api_config.py 模式：<br>- define_p09_pipeline_config() → 5 节点 graph: source→normalize→validate→quality_gate→sink，target_ot=Weapp<br>- P10 / P11 / P12 同上<br>每节点配置：source 表名、游标字段（或快照模式）、target_ot、quality_gate 阈值 |
| A3-4 | aos-platform/services/aos-api/aos_api/ec_ot_writer.py（如有必要） | 追加 | 检查新 4 OT 的 Link sink 关联逻辑是否需要补全：<br>- Shop.hasWeapp: sink 时 site_id 匹配 Shop.niushop:1:{site_id}<br>- Product.hasReview / ProductReview.ofSku / ProductReview.byMember: sink 时 goods_id / sku_id / member_id 各自匹配已有 OT 唯一键<br>- Order.hasPayment: out_trade_no 匹配 Order.out_trade_no，或 relate_id≈order_id 匹配 Order.order_id<br>- Order.fromWeapp: weapp_id 匹配 Weapp.weapp_id<br>如 ec_ot_writer.py 已有通用逻辑（按 Link 定义自动关联）则不改；否则追加 6 个 Link 的 sink 关联函数 |

---

## A4 · 端到端测试（1 个新文件）

| # | 文件路径（新增） | 测试覆盖 | 退出门 |
|---|---|---|---|
| A4-1 | aos-platform/services/aos-api/tests/test_ec_d4_e2e_validation.py | 12 OT（8 已有 + 4 新增）全链路真实数据：<br>1. 12 OT 实例数 ≥ 1 条（ns_site / ns_weapp / ns_config / ns_goods / ns_goods_sku / ns_goods_category / ns_goods_evaluate / ns_order / ns_order_goods / ns_express_delivery_package / ns_pay / ns_member）<br>2. 15 条 Link 至少各 1 条：<br>&nbsp;&nbsp;D1(7): Order.lines / OrderLine.ofSku / OrderLine.ofProduct / ProductSku.ofProduct / Product.inCategory / Shop.sellsProduct / Order.fulfilledBy<br>&nbsp;&nbsp;D1.5(1): Order.placedByLite<br>&nbsp;&nbsp;D4(7): Shop.hasWeapp / Product.hasReview / ProductReview.ofSku / ProductReview.byMember / Order.hasPayment / Order.fromWeapp / Product.inCategory（已验证）<br>3. 8 派生指标非空率：<br>&nbsp;&nbsp;D1(4): quality_score / stock_health / risk_score / overdue_hours<br>&nbsp;&nbsp;D1.5(2): order_count / last_order_days<br>&nbsp;&nbsp;D4(2): review_quality_bucket / pay_duration_min → 非默认值/非 null 占比 ≥ 80%（G4）<br>mock 策略：fetch_source_rows 从真实 fixture（参考 D1 端到端），不连 SSH | G4（派生指标）、G5（Link 完整性）、G2/G3 覆盖率 |

---

## A5~A9 · 标准链路验证（1 个文件，用户拍板：放一个文件）

平台能力已实现（phase5_pipeline_engine.py L633/L657/L678/L719/L888/L668/L672），只跑通验证不新增平台代码。

| # | 文件路径（新增） | 子步骤 | 测试覆盖 | 退出门 |
|---|---|---|---|---|
| A5-1 | aos-platform/services/aos-api/tests/test_ec_d4_standard_pipeline_links.py | A5 管道提案与审批 | P09~P12 各创建 1 份 PipelineProposal：<br>1. create_proposal(pipeline_id=P09, title="P09 Weapp OT 管道提案", diff_summary="新增 OT Weapp + Link Shop.hasWeapp") → status=pending<br>2. 审批：proposal.approve() → status=approved<br>3. merge_proposal(pipeline_id=P09, pp_id=...) → status=merged<br>4. 验证 merge 后 GET /v1/pipelines/{pl_id}/graph 包含 Weapp OT 节点<br>对 P10/P11/P12 重复上述流程 | G6 |
| A6-1 | 同上 | A6 同步计划编辑器（1h cron） | P01~P12 共 12 条管道各创建 1 个 Schedule：<br>1. create_schedule(name="P01 Shop 1h", trigger_type="cron", cron_expr="0 * * * *", status="active", pipeline_id=P01)<br>2. run_schedule(sc_id) → ScheduleRun.status=success<br>3. 验证：Schedule.status=active，ScheduleRun.rows_read>0, rows_written>0<br>对 P02~P12 重复 | G7 |
| A7-1 | 同上 | A7 管道执行历史 | run_schedule 后：<br>1. list_history(pipeline_id) → action=run 记录 ≥1 条<br>2. history 记录数 = run_schedule 次数（同一管道跑 N 次应有 N 条 action=run） | G8 |
| A8-1 | 同上 | A8 数据沿袭 | run_schedule 后：<br>1. ScheduleRun.lineage_ref 非空（格式合法，如 lineage_{run_id}）<br>2. GET /v1/lineage/graph → 查到 source 表（如 ns_weapp）→ OT sink（如 Weapp）的沿袭边<br>3. GET /v1/lineage/{node_id}/upstream → 能追溯到 source 表 | G9 |
| A9-1 | 同上 | A9 数据健康检查 | pipeline sink 产出 Dataset 后：<br>1. trigger check_health(ds_id)<br>2. HealthCheck.status ∈ {"healthy", "warning"}（≠critical）<br>3. null_rate < 10%<br>4. freshness_hours ≤ 1h | G10 |

---

## 风险评估与规避

| 风险 | 等级 | 规避措施 |
|---|---|---|
| D1.5 基线 478 tests 回归 | 低 | 唯一松绑点 ==8→>=8，符合跨波累积契约；其余全追加不改旧逻辑。编码前先跑基线确认 PASS，编码后再跑一次确认 0 回归 |
| review_quality_bucket 口径偏移 | 中 | 严格按规格 §3.6：score≥4.5→"high" / score≤3→"low" / 其他→"mid"。边界值 3.0 和 4.5 用单测专项覆盖 |
| pay_duration_min 跨表关联失败 | 中 | **管道内完成**：normalize 阶段 ns_pay.relate_id（≈order_id）查 ns_order.create_time。关联失败（relate_id 为空或查不到 order）时写 null，不阻塞 Pipeline。单测覆盖关联成功和失败两种场景 |
| PII 脱敏泄漏（ns_pay / ns_config） | 高 | ns_pay 的支付凭证字段 / ns_config 的 JSON value 内含密钥类，严格按 _PII_PATTERNS 顺序（长 pattern 先：身份证15-18→手机号11→openid→密钥）。单测断言 DLQ.sanitized_summary / Payment.properties 中不含明文 |
| A5 Proposal merge 后 graph 不更新 | 低 | 先检查 phase5_pipeline_engine.merge_proposal 的实现（代码 L657）：如果只是改 DB 不改内存缓存，需要调 get_pipeline 刷新缓存，或在 proposal.merge 时自动 refresh |
| A6 Schedule 的 cron 触发要手动 run 验证 | 低 | D4 Phase A 只验证 create_schedule → 手动 run_schedule → ScheduleRun 成功。真 cron 触发留给 Phase B 的 Schedule→SyncTask→Pipeline 链路验证（B3） |
| A9 HealthCheck.freshness_hours 超限 | 低 | 测试内 NOW 固定（datetime(2026,8,6,10,0,tzinfo=UTC)），run_schedule 后立即 check_health，数据新鲜度应为 0h，必满足 ≤1h |

---

## 编码顺序（严格 A1→A10）

1. **A1**：CORE 契约注册 + 松绑 → 先跑 D1/D1.5 基线（478 tests）→ 0 回归后进 A2
2. **A2**：4 份 RED 测试 → 预期 FAIL（TDD 红绿循环）
3. **A3**：实现 4 份管道配置 + normalize 映射 + SourceAdapter → RED→GREEN
4. **A4**：端到端测试（12 OT + 15 Link + 8 派生指标）→ GREEN
5. **A5~A9**：标准链路测试（一个文件内 5 子步骤）→ GREEN
6. **A10**：退出门 G1~G10 全过 + 533 tests 100% PASS

---

## 改动文件索引（11 个文件，完整路径）

| 类型 | 编号 | 绝对路径 |
|---|---|---|
| 追加 | A1-1 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/aos_api/ecom_core_models.py |
| 追加 | A1-2 | 同上 |
| 追加 | A1-3 | 同上 |
| 追加 | A1-4 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/aos_api/ec_normalizer.py |
| 追加 | A1-5 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/aos_api/ec_derived_metrics.py |
| 追加 | A1-6 | 同上 |
| 新增 | A1-7 | 同上（文件末尾加两个函数） |
| 松绑 | A1-8 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/tests/test_ec_d1_5_customer_lite_ot.py |
| 新增 | A2-1 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/tests/test_ec_d4_p09_weapp.py |
| 新增 | A2-2 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/tests/test_ec_d4_p10_system_config.py |
| 新增 | A2-3 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/tests/test_ec_d4_p11_product_review.py |
| 新增 | A2-4 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/tests/test_ec_d4_p12_payment.py |
| 追加 | A3-1 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/aos_api/ec_normalizer.py（P09~P12 normalize 函数） |
| 追加 | A3-2 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/aos_api/ec_live_executor.py |
| 新增 | A3-3 | 内嵌在 A2 的 4 个测试文件内（管道配置工厂，不新建独立文件） |
| 追加 | A3-4 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/aos_api/ec_ot_writer.py（如有必要补 Link sink 关联） |
| 新增 | A4-1 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/tests/test_ec_d4_e2e_validation.py |
| 新增 | A5-1~A9-1 | /Users/ddt/work/projects/ai_agent/aos-platform/services/aos-api/tests/test_ec_d4_standard_pipeline_links.py（单文件含 A5~A9 五子步骤） |

> 备注：有些是同一文件多次追加（如 ecom_core_models.py 追加 3 个块、ec_derived_metrics.py 追加 2~3 个块），编码时合并为一次 Edit 操作，减少 tool 调用次数。
