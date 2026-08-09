# O1-UX7：对象探索真实有效对象与字段语义修复清单

> **版本**：v1.1 · 2026-08-10  
> **状态**：GREEN  
> **目标范围**：`org-org` · `dev-project`（栖月汇商贸有限公司 · 默认工作区）  
> **上位方案**：`O1-PLAN-本体数字孪生层全量编码任务与实施顺序.md`、`O1-UX-本体数字孪生九菜单与知识图谱补强方案.md`

## 0. Rules

1. 本波不重开 O1 架构，只修复对象探索的选择交互、字段语义和真实数据展示。
2. 只使用栖月汇线上真实源数据；禁止 Mock、演示订单或演示商品混入。
3. Product 口径固定为 `site_id=1 AND is_delete=0 AND goods_state=1`；Order 口径固定为 `site_id=1 AND is_delete=0`。
4. 前端列必须绑定对象实例真实存在的 Canonical 属性；不得继续展示整列不存在的旧 snake_case 演示字段。
5. 任何数据回填必须通过既有 P02/P05 Pipeline 和 OTWriter 幂等链执行，不直改业务对象表，不改变源商城数据。
6. 页面改动沿用现有 AOS 设计系统并做最小调整；完成后必须用内置浏览器逐项点击验证。

## 1. 现状核查

| 项目 | 实时事实 | 结论 |
|---|---|---|
| Order API | 61 条，`status=active`、`isDelete=0`；`orderNo/memberId/createdAt/totalAmount/payStatus` 均 61/61 非空 | 数据真实有效，页面空白由 Schema/实例属性命名错位造成 |
| Order Schema | 仍为 `order_no/customer_id/customer_name/order_date/total_amount` 等旧演示字段 | 与 Canonical `orderNo/memberId/createdAt/totalAmount` 不一致，不能直接驱动列 |
| Product API | 旧执行 57 条，其中实时核查发现 `goods_state=0` 18 条、`goods_state=1` 39 条 | 旧对象集混入下架商品；不能继续把 57 条称为“实际上架” |
| Product Pipeline | YAML 为 `site_id=1 AND is_delete=0 AND goods_state=1`，但 JDBC SSH SourceAdapter 未执行该过滤 | 代码口径与方案不一致，必须先补过滤再重跑 P02 |
| 顶部探索名称 | 自由输入“栖月汇对象探索” | 主任务是选对象类型，应改为下拉选择，探索资产名自动按类型生成 |

## 2. 实施任务

### UX7-A：对象类型选择下拉化

- [x] 顶部自由输入改为“选择对象类型”下拉，选项来自 `/v1/ontology/object-types`。
- [x] 移除搜索栏重复的类型选择，保留唯一清晰入口。
- [x] 类型切换同步清空旧选择、重载真实对象，并自动生成保存名称。

### UX7-B：真实字段语义

- [x] Object Explorer 在展示层执行线上有效口径：Order 仅保留 `isDelete=0/status=active`，Product 仅保留 `state=1/isDelete=0/status=active`；结果数必须是过滤后的真实数量。
- [x] Object Explorer 增加 Order/Product 的权威展示列配置，并且只展示当前对象集合实际存在的字段。
- [x] Order 至少展示：订单 ID、订单号、会员 ID、下单时间、订单金额、订单状态、支付状态、发货状态。
- [x] Product 至少展示：商品 ID、商品名称、销售价、库存、销量、类目、上架状态、更新时间。
- [x] 对金额、时间和业务状态做只读格式化，不改变底层 Canonical 值。
- [x] 其他 OT 继续使用 Schema/字段并集合同，不受本波影响。

### UX7-C：P02 商品经营字段补齐

- [x] 修复 JDBC SSH SourceAdapter 未执行 YAML `site_filter` 的缺口；只接受可参数化的简单等值 AND 白名单表达式，禁止任意 SQL 拼接。
- [x] P02 实时口径重新以源事实核准：`site_id=1 AND is_delete=0 AND goods_state=1`，数量以本次真实执行为准，不沿用旧“57 条均上架”的错误结论。
- [x] `ec_normalizer.to_product` 按已冻结 P02 mapping 补写真实 `price/marketPrice/costPrice/stock/saleNum/unit/state/isDelete/goodsClassName`。
- [x] Product Canonical Schema 升至 v2；同一真实源时间只允许“Schema 版本递增 + 旧基础属性值完全不变 + 纯新增字段”的受控升级。
- [x] `EcomConsistencyStore` 为上述 additive schema evolution 增加窄门；任何删字段、改旧值、同版本差异或版本倒退仍返回 `SOURCE_VERSION_CONFLICT`。
- [x] 增加 normalizer 单元测试，覆盖实际源字段到 Canonical properties 的映射。
- [x] 仅重跑 P02，验证源读取只返回满足上架口径的商品；真实数量与关键字段非空率均以本次源事实为准，禁止沿用旧 57 条结论。

### UX7-D：验证与证据

- [x] 前端列解析与格式化测试先失败后通过；后端 P02 映射测试通过。
- [x] 前端定向测试、TypeScript、production build 通过；后端定向测试通过。
- [x] 内置浏览器验证 Order 与 Product 下拉切换、表格字段、搜索和选择，无阻断交互错误。
- [x] 跨租户 canary 验证 `dev-org/dev-project` 不可见栖月汇真实数据。
- [x] 更新 `AOS项目开发上下文`，记录代码 SHA、数据执行结果、浏览器证据和残余风险。

## 2.1 实施证据

| 证据 | 结果 |
|---|---|
| P02 真实执行 | `build-d58591af77`，`status=succeeded`，`rowsWritten=124`；SourceAdapter 已按参数化 `site_id=1 AND is_delete=0 AND goods_state=1` 读取 |
| Order 实时 API | 61 条；`status=active/isDelete=0/orderNo/createdAt/totalAmount` 均 61/61 |
| Product 实时 API | Canonical 保留 57 条历史对象，其中 39 条当前上架、18 条历史下架；Object Explorer 按有效口径只展示 39 条 |
| Product 经营字段 | 57/57 均有 `title/price/stock`；浏览器显示的 39 条全部标记“已上架”，无空白单元格 |
| 后端定向回归 | 84 passed |
| 前端全量回归 | 158 files / 2039 tests passed；TypeScript 与 production build 通过 |
| 租户 canary | `dev-org/dev-project` 对 Order、Product 均返回 `object type is not installed`，不可见栖月汇对象 |
| 浏览器交互 | 下拉切换 Order→Product、商品搜索（“面膜”=2 条）、勾选后对象集按钮启用均通过 |

> 说明：57 条是历史 Canonical 对象总量，不再作为“实际上架商品数”。本波不物理删除 18 条历史下架对象；对象探索按当前线上有效口径展示 39 条，后续增量读取也只接收上架源行。

## 3. 退出门

1. Order 页面不再出现由旧字段名造成的批量“—”，关键经营列均来自 61 条真实有效订单。
2. Product 页面只展示实时源中满足 `site_id=1 AND is_delete=0 AND goods_state=1` 的实际上架商品，并能看到真实商品名称、价格、库存等经营字段；数量以实时源事实为准。
3. 对象类型通过下拉选择；不存在两个重复类型入口。
4. 不修改源商城，不引入 Mock，不污染其他组织/工作区。
5. 测试、浏览器和实时 API 三类证据一致后，状态才可改为 GREEN。

## 4. 回滚

- 代码回滚：回退本波前端列配置与 `to_product` 的新增 properties；不回退 O1-UX1～UX6。
- 数据回滚：P02 为幂等投影；若回填异常，停止调度并保留执行证据，不直删源数据或其他 OT。
- 若实际源字段非空率低于预期，按真实数据标记 INCONCLUSIVE，不用占位值伪造完整度。
- 不得通过伪造 `source_updated_at` 绕过一致性门；Schema 补强必须保留真实源版本并显式提升 `schema_version`。
