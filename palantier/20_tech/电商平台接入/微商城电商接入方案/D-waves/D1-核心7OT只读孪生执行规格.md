# D1：核心 7 OT 只读孪生 — 执行规格（Spec）

> 本文件冻结 D1 波次的具体动作、产物、退出门与边界。
> 上位方案：[228-微商城专项实施准备与FDE全链路规格.md](../228-微商城专项实施准备与FDE全链路规格.md) 第 8 节 D1。
> 前置：D0 GREEN（[D0-只读发现与配置冻结执行规格](./D0-只读发现与配置冻结执行规格.md)）+ D1 前置 G1+G2+G3+G7 完成（`aos-platform@9b83d5d`，37 passed）。
> 基线：`aos-platform@9b83d5d` / `docs@801faca` / TI-0~TI-6 全 GREEN。
> 状态：**设计方案 · 待用户批准**。批准后按 TDD 实施，不跳过测试。

---

## 1. 元数据

| 项 | 值 |
|---|---|
| 波次 | D1（228-微商城专项第 2 个实施波） |
| 前置基线 | D0 GREEN + D1 前置（G1+G2+G3+G7）已完成 |
| 剩余前置 | G4 DatasetSink + G5 OTWriter + G6 DLQ（本波次内补齐） |
| 预计产物 | G4/G5/G6 代码 + Niushop SourceAdapter + P01-P07 运行时配置 + 专项测试 |
| 编码原则 | TDD 红绿重构、最小更改、只读零写入、PII 不出库、失败不变成功 |
| 退出门 | 见第 6 节 |

---

## 2. 上下文与动机

D1 是栖月汇微商城从"规格冻结"走向"真实数据孪生"的第一波。目标是用最小代价把 Niushop 7 张核心表的只读镜像落地到 AOS 的 7 OT + Link + Dataset，为 D1.5 增长读模型和 L01-L03 Logic 提供可信数据底座。

**D1 做什么**：
- 把 `ec_live_executor` 从合成 fixture 模式切换到 Niushop 只读源（SourceAdapter）
- 实现 G4 DatasetSink（executor 输出 → `meta_dataset` + `DatasetBuild`）
- 实现 G5 OTWriter（executor 输出 → `ecom_object` + `ecom_link`，复用 BatchCommand 单事务）
- 实现 G6 DLQ（失败 run 自动入队，只存键/错误码/脱敏摘要）
- 创建 P01-P07 七条 Pipeline 运行时配置（通过 `/v1/pipelines` API）
- 落地 6 条核心 Link（hasSku/inCategory/contains/forProduct/forSku/ships；placedByLite 在 D1 侧保留 member_id 关联键，D1.5 落地）
- 计算并写入 4 个派生指标（quality_score/stock_health/risk_score/overdue_hours）

**D1 不做什么**（硬边界）：
- 不做写回微商城（D4 才考虑）
- 不做 P08 CustomerLite（D1.5 才落地）
- 不做多表 JOIN Sink（按 P 按 Link 独立落地，见上位方案 §5.3）
- 不做 L01-L06 Logic / W01-W04 Workshop（D1.5+）
- 不做完整 Customer/Payment/Refund（D2）
- 不修改 `phase5_pipeline_engine.py` 的 fail-closed 判定链路（`_preflight`/`_evidence_from_result`/`_valid_ref`）

---

## 3. 功能需求（FR，RFC 2119）

### FR-D1-1（MUST）G4 DatasetSink 实现

executor 的 sink 节点 MUST 调用 `data_os_store` 落地 Dataset：

```text
sink 节点输入: rows (transform 后的行流)
  │
  ├─ data_os_store.persist_dataset(scope, rid=gen_rid(), ...)
  ├─ data_os_store.persist_dataset_history(scope, ...)
  └─ engine.add_build(scope, dataset_id, DatasetBuild(...))
  → 产出 output_ref = "dataset://catalog/<rid>"
```

**约束**：
- `output_ref` 格式 MUST 为 `dataset://catalog/<rid>`（有 netloc、无 query/fragment、≤512 字符）
- `rows_read` / `rows_written` MUST 为非负整数
- scope 守门：落 `meta_dataset` 时带 `(org_id, project_id)`

**接入点**：`aos_api/ec_live_executor.py` sink 节点分发分支。

### FR-D1-2（MUST）G5 OTWriter 实现

executor 的 sink 节点 MUST 调用 `ecom_consistency_store` 落地 7 OT + Link：

```text
sink 节点输入: rows (映射后的 OT 行)
  │
  ├─ ecom_consistency_store.batch_upsert(
  │     scope, platform="niushop",
  │     objects=[{ot, external_id, props, source_updated_at, ...}, ...],
  │     links=[{source_external_id, target_external_id, link_type, ...}, ...]
  │  )
  │  （复用 BatchCommand 单事务：upsert→link→checkpoint→receipt）
  └─ 产出 object_ref = "object://<ot>/<external_id>"
```

**约束**：
- 唯一键命名空间：`niushop:1:{source_pk}`
- 复合游标 `(watermark, primary_key)` 稳定二元组
- 旧版本不覆盖新版本；相同版本+相同 hash 为幂等；相同版本+不同 hash 返回冲突
- DELETE 写 tombstone，不物理删除
- 关联 Link 同事务、同租户；禁止悬挂或跨租户 Link
- 失败时整事务回滚，不前移 checkpoint

**接入点**：`aos_api/ec_live_executor.py` sink 节点分发分支。

### FR-D1-3（MUST）G6 DLQ 实现

executor 失败时 MUST 自动入 Pipeline DLQ：

- DLQ 条目只存：唯一键、错误码、脱敏错误摘要、时间戳
- 不存 PII 明细、输入数据正文、凭据
- 失败 run 的 `status` MUST 为 `failed`，不得变 `succeeded`
- 可重试：DLQ 条目带 `retry_count` 与 `max_retry=3`

**接入点**：`aos_api/ec_live_executor.py` 异常处理分支，复用 `wave_ext._dlq` 结构。

### FR-D1-4（MUST）Niushop SourceAdapter 实现

executor 的 source 节点 MUST 从合成 fixture 切换到 Niushop 只读源：

- 从 `node.config` 取 `source_id` → 查 `meta_source` 拿连接配置
- 用只读事务（`SET SESSION TRANSACTION READ ONLY`，复用 `qyh_discover_readonly.py` 模式）
- 按 `node.config.cursor` 做增量游标读取（复用 `ecom_consistency_store` 的复合游标语义）
- 连接级 `LIMIT 100` 行采样上限（初装不受限，增量受游标控制）
- 单查询超时 30s，隧道断开时 fail-closed

**约束**：
- SourceAdapter 强制走 `meta_source` 查连接配置，不接 config 直传连接串
- 软删行（`is_delete=1`）不入 OT，进 DLQ 计数
- `0` 时间转 `null`（Unix 秒 → UTC）

**接入点**：`aos_api/ec_live_executor.py` source 节点分发分支，新增 Niushop 只读源适配。

### FR-D1-5（MUST）P01-P07 运行时配置创建

按 [frozen/02-pipeline-manifest.yaml](../frozen/02-pipeline-manifest.yaml) 冻结的规格，通过 `/v1/pipelines` API 创建 P01-P07 七条 Pipeline 运行时配置：

| Pipeline | OT | 源表/主键 | 增量策略 | Link |
|---|---|---|---|---|
| P01 | Shop | `ns_site`/`site_id` | 每日快照 | — |
| P02 | Product | `ns_goods`/`goods_id` | `(modify_time, goods_id)` | — |
| P03 | ProductSku | `ns_goods_sku`/`sku_id` | `(modify_time, sku_id)` | `hasSku` |
| P04 | Category | `ns_goods_category`/`category_id` | 每日快照 | `inCategory` |
| P05 | Order | `ns_order`/`order_id` | `(create_time, order_id)` + 7天重扫 | `contains`/`forProduct`/`forSku`/`placedByLite` 关联键 |
| P06 | OrderLine | `ns_order_goods`/`order_goods_id` | 每日快照（修正，见 frozen/02 D-002） | `contains`/`forProduct`/`forSku` |
| P07 | Shipment | `ns_express_delivery_package`/`id` | 每日快照 | `ships` |

**通用骨架**（每条 Pipeline 统一使用）：
```text
Source → TenantFilter(site_id=1) → Normalize → Validate → Deduplicate
       → QualityGate ┬→ DatasetSink(G4) + OTWriter(G5)
                     └→ DLQ(G6)
```

**约束**：
- `org_id`/`project_id` 由实施上下文注入（栖月汇：`org-org`/`dev-project`）
- `site_id=1` 是源过滤与 Sink 租户键的一部分
- P05 的 `member_id` 仅保留关联键（不引 PII），为 D1.5 `placedByLite` Link 预留
- P06 增量游标修正：`create_time` 全为 0（frozen/02 D-002），改用 `refund_action_time` 为辅游标

### FR-D1-6（MUST）四段实施策略

按 P01→P04→P05/P06→P07 分段实施，每段均做：

1. **初装**：首次全量读取源表 → 落地 OT + Link + Dataset
2. **增量**：基于复合游标增量读取 → 幂等 upsert
3. **重跑**：重复执行同一批次 → 验证幂等（相同 key+相同 hash 返回原结果）
4. **断点**：模拟中断后恢复 → 验证 checkpoint CAS 不前移
5. **重复**：相同版本+不同 hash → 验证冲突检测
6. **越租户**：跨 org/workspace 写入 → 验证拒绝（fail-closed）

### FR-D1-7（MUST）派生指标计算节点

Pipeline 的 Normalize/QualityGate 节点 MUST 计算以下派生指标并写入 OT（见上位方案 §5.4.1）：

| 派生指标 | OT | 计算口径（基于 frozen/01 schema fingerprint） |
|---|---|---|
| `quality_score Δ` | Product | `evaluate > 0` 时 `= evaluate_haoping / evaluate`；否则 `null` |
| `stock_health Δ` | ProductSku | `stock <= goods_stock_alarm` → `low`；`0 < stock <= alarm` → `watch`；否则 `ok` |
| `risk_score Δ` | Order | `base=0.0`；`commission_risk_flag=1` → +0.40；`refund_status∈{-3,3}` → +0.30；`is_lock=1` → +0.20；`order_status=0 AND pay_status=0 AND now-create_time>24h` → +0.10；截断 `[0,1]` |
| `overdue_hours Δ` | Shipment | SLA_HOURS=48；`delivery_time=0 AND Order.pay_time>0` 时 `= max(0, (now - Order.pay_time - 48h) / 3600)`；否则 `null` |

**约束**：
- 派生指标 MUST 由 Pipeline 的 Normalize/QualityGate 节点计算后写入 OT，不能由 Logic 自行计算
- 派生公式变更等同于 OT schema 变更，需走 [228-EC-核心本体与增量一致性方案](../../../228-EC-核心本体与增量一致性方案.md) 审批

### FR-D1-8（MUST）核心 Link 落地

6 条核心 Link MUST 在 Pipeline sink 节点同事务落地：

| Link | From → To | 来源字段 | 完整性门禁 |
|---|---|---|---|
| `hasSku` | Product → ProductSku | `goods_id` | SKU 不得指向不存在 Product |
| `inCategory` | Product → Category | `category_id` | 多分类字符串需先定义拆分契约 |
| `contains` | Order → OrderLine | `order_id` | 行必须有订单头 |
| `forProduct` | OrderLine → Product | `goods_id` | 缺失进 DLQ，不自动造对象 |
| `forSku` | OrderLine → ProductSku | `sku_id` | `sku_id=0` 规则需样本核验 |
| `ships` | Shipment → Order | `order_id` | 包裹必须有订单头 |

> `placedByLite`（Order → CustomerLite）在 D1 P05 侧保留 `member_id` 关联键，D1.5 才落地 Link。

---

## 4. 非功能需求（NFR）

| 项 | 阈值 |
|---|---|
| 源库写入 | 0（硬约束，负向测试覆盖） |
| PII 明细泄漏 | 0（扫描报告，正则匹配手机/身份证/银行卡 pattern） |
| 重跑幂等 | 相同 key+相同 hash 返回原结果，rows_written 不翻倍 |
| 跨租户写入 | 0（fail-closed，负向测试覆盖） |
| 单 Pipeline 初装 | p95 < 60s（7 表总计 < 300s） |
| 增量读取 | p95 < 10s |
| DLQ 条目 PII | 0（只存键/错误码/脱敏摘要） |
| 派生指标缺失率 | < 5%（源字段缺失时写 null，不阻塞 Pipeline） |

---

## 5. 验收标准（AC，Given/When/Then，每条追溯 FR）

### AC-D1-1（← FR-D1-1）G4 DatasetSink

- **Given** executor 已注册 `ec-live-v1` + dataset resolver 已注册
- **When** 运行 P01 Shop Pipeline（`execution_mode="live"`）
- **Then** `meta_dataset` 表新增 1 条记录，`output_ref` 格式为 `dataset://catalog/<rid>`，resolver 返回 `True`

### AC-D1-2（← FR-D1-2）G5 OTWriter

- **Given** P01 Shop Pipeline 运行完成
- **When** 查询 `ecom_object` WHERE `ot="Shop"` AND `scope` 匹配
- **Then** 记录数 = 源表有效行数（`site_id=1`），唯一键 `niushop:1:1` 存在，`source_updated_at` 非空

### AC-D1-3（← FR-D1-3）G6 DLQ

- **Given** P02 Product Pipeline 运行中模拟源连接断开
- **When** executor 捕获异常
- **Then** `status="failed"`（不变 `succeeded`），DLQ 有 1 条记录（含错误码、脱敏摘要、无 PII），`rows_written` 不前移

### AC-D1-4（← FR-D1-4）Niushop SourceAdapter

- **Given** `meta_source` 已注册 Niushop 只读源（`recommend_ro` 账号）
- **When** 运行 P02 Product Pipeline
- **Then** 读取 `ns_goods` WHERE `site_id=1 AND is_delete=0`，有效行数=57（frozen/02 数据现状），软删 8 行进 DLQ 计数

### AC-D1-5（← FR-D1-5）P01-P07 运行时配置完整

- **Given** `/v1/pipelines` API 可用
- **When** 检查 P01-P07 配置
- **Then** 每条含 `source_table`/`pk`/`cursor`/`site_filter`/`target_ot`/`unique_key`/`time_rule` 七个必填键（与 frozen/02 一致）

### AC-D1-6（← FR-D1-6）四段实施负向测试

- **Given** P01 Shop Pipeline 已初装
- **When** 重跑同一批次
- **Then** `rows_written` 不变（幂等），`ecom_ingest_receipt` 返回原结果（相同 key+相同 hash）
- **When** 模拟跨租户写入（scope 不匹配）
- **Then** 被拒绝（fail-closed），`ecom_object` 无跨租户记录

### AC-D1-7（← FR-D1-7）派生指标落地

- **Given** P02 Product Pipeline 运行完成
- **When** 查询 `ecom_object` WHERE `ot="Product"`
- **Then** `props.quality_score` 字段存在：`evaluate > 0` 时为 `evaluate_haoping / evaluate`；否则为 `null`

### AC-D1-8（← FR-D1-8）核心 Link 完整性

- **Given** P03 ProductSku Pipeline 运行完成
- **When** 查询 `ecom_link` WHERE `link_type="hasSku"`
- **Then** 每条 Link 的 source 指向已存在的 Product，target 指向已存在的 ProductSku，无悬挂 Link
- **When** 检查 P06 OrderLine 的 `forProduct` Link 中 `goods_id` 指向不存在的 Product
- **Then** 进 DLQ，不自动造对象

### AC-D1-9 专项测试通过

- **Given** `tests/test_ec_d1_*.py`
- **When** pytest 运行
- **Then** 全部 passed，覆盖：SourceAdapter 只读、DatasetSink 落地、OTWriter 单事务、DLQ 脱敏、派生指标计算、Link 完整性、重跑幂等、跨租户拒绝

---

## 6. 退出门（D1 GREEN 的判定）

全部为真才判 GREEN：

1. G4 DatasetSink 实现 + 测试通过
2. G5 OTWriter 实现 + 测试通过（BatchCommand 单事务幂等）
3. G6 DLQ 实现 + 测试通过（失败不变成功、无 PII）
4. Niushop SourceAdapter 实现 + 测试通过（只读零写入）
5. P01-P07 运行时配置创建 + 初装通过
6. 四段实施每段 6 项负向测试通过（初装/增量/重跑/断点/重复/越租户）
7. 派生指标 4 个全部落地到 OT props
8. 6 条核心 Link 落地 + 完整性门禁通过
9. D1 前置 37 tests 零回归（honesty + resolver + executor）
10. 全程对微商城源库零写入、对 AOS 只增不删

---

## 7. 实施顺序（批准后按序）

```
Phase A：剩余前置代码（G4/G5/G6 + SourceAdapter）
  Step 1  RED：写 test_ec_d1_dataset_sink.py 失败测试（G4）
  Step 2  GREEN：ec_live_executor.py sink 节点加 DatasetSink 调用
  Step 3  RED：写 test_ec_d1_ot_writer.py 失败测试（G5）
  Step 4  GREEN：ec_live_executor.py sink 节点加 OTWriter 调用
  Step 5  RED：写 test_ec_d1_dlq.py 失败测试（G6）
  Step 6  GREEN：ec_live_executor.py 异常分支加 DLQ 投递
  Step 7  RED：写 test_ec_d1_source_adapter.py 失败测试（SourceAdapter）
  Step 8  GREEN：ec_live_executor.py source 节点加 Niushop 只读源
  Step 9  回归：D1 前置 37 tests + Phase A 新增 tests 全 GREEN

Phase B：P01-P07 运行时配置 + 四段实施
  Step 10 创建 P01 Shop Pipeline 配置 + 初装/增量/重跑/断点/重复/越租户
  Step 11 创建 P04 Category Pipeline 配置 + 六项测试
  Step 12 创建 P02 Product + P03 ProductSku Pipeline 配置 + 六项测试（hasSku/inCategory Link）
  Step 13 创建 P05 Order + P06 OrderLine Pipeline 配置 + 六项测试（contains/forProduct/forSku Link）
  Step 14 创建 P07 Shipment Pipeline 配置 + 六项测试（ships Link）
  Step 15 派生指标 4 个落地验证 + Link 完整性门禁
  Step 16 全量回归 + PII 扫描 + 提交
```

**分段理由**：P01（Shop）最简单（1 行），用于验证全链路；P04（Category）无依赖，验证 Link 拆分；P02+P03 有 hasSku 依赖关系；P05+P06 有 contains/forProduct/forSku 依赖关系；P07 有 ships 依赖关系。

---

## 8. 文件清单（本次 D1 产出）

### 新增

| 路径 | 类型 | 说明 |
|---|---|---|
| `services/aos-api/tests/test_ec_d1_dataset_sink.py` | 测试 | G4 DatasetSink 专项 |
| `services/aos-api/tests/test_ec_d1_ot_writer.py` | 测试 | G5 OTWriter 单事务专项 |
| `services/aos-api/tests/test_ec_d1_dlq.py` | 测试 | G6 DLQ 脱敏与投递专项 |
| `services/aos-api/tests/test_ec_d1_source_adapter.py` | 测试 | Niushop SourceAdapter 只读专项 |
| `services/aos-api/tests/test_ec_d1_pipelines.py` | 测试 | P01-P07 端到端 + 四段负向测试 |

### 修改

| 路径 | 改动 | 说明 |
|---|---|---|
| `services/aos-api/aos_api/ec_live_executor.py` | 扩展 source/sink/异常分支 | G4 DatasetSink + G5 OTWriter + G6 DLQ + Niushop SourceAdapter |

### 不改

- `aos_api/phase5_pipeline_engine.py` 的 fail-closed 判定逻辑
- `aos_api/ecom_consistency_store.py`（BatchCommand 接口已有，复用）
- `aos_api/data_os_store.py`（CRUD 已有，复用）
- `aos_api/ec_pipeline_resolvers.py`（D1 前置已完成，复用）
- `aos_api/main.py`（lifespan 注册已完成，复用）
- Pipeline Builder（W1-14 DAG 编辑器）
- Connector / OAuth / OpenAPI 生成物 / CI
- 4 个电商 bundle fixture

---

## 9. Out of Scope（明确不做）

- P08 CustomerLite（D1.5 才落地）
- 完整 Customer / Payment / Refund（D2）
- 栖月汇特色能力：分润/分享体验码/超级卡（D3）
- 生产写回微商城（D4）
- L01-L06 Logic / W01-W04 Workshop（D1.5+）
- 多表 JOIN Sink（上位方案 §5.3 明确排除）
- 自定义 SQL 节点（诚实执行方案已排除）
- LLM 节点的生产执行（独立波次）
- lineage/quality/artifact resolver 注册（D2+，D1 只用 dataset+object 两类）

---

## 10. 自审（Self-Review）

- [x] 10 章节齐全
- [x] 每条 AC 追溯到 FR
- [x] NFR 有可测阈值
- [x] Out of Scope 非空
- [x] 与上位方案 §5/§8 一致（7 Pipeline 骨架、D1 通过标准、四段实施）
- [x] 与 frozen/02 一致（P01-P07 源表/主键/增量策略/Link）
- [x] 与 D1 前置方案 §4.4 一致（G4/G5 调用框架）
- [x] 与诚实执行方案 §二 一致（evidence 契约、失败不变成功）
- [x] 与核心本体方案 §二/§三 一致（复合游标、幂等、tombstone、单事务）
- [x] 无占位符
- [x] 路径引用已按 D-waves/ 子目录修正（`../` 主方案、`../frozen/`、`../../../` 228-EC-*）
