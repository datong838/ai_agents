# Shopify · AOS 数字孪生对接方案 — 总体分析计划

| 字段 | 内容 |
|------|------|
| 状态 | **方案 only · 调研阶段** · 2026-07-22 |
| 版本 | **v1.0** · 初始分析计划 |
| 目录 | `docs/palantier/20_tech/Shopify电商接入方案/` |
| 覆盖范围 | **Shopify 独立站商家** — Products · Orders · Customers · Inventory · Fulfillment · Payments · Discounts · Locations |
| 关联 | 微商城模板：[00-Niushop微商城AOS对接方案](../微商城电商接入方案/00-Niushop微商城AOS对接方案.md) · [220w 差距分析](../220w-与目标系统差距对照分析.md) · [220plan 开发计划](../220plan-分阶段开发与里程碑计划.md) |
| 原则 | **复用微商城 8 域 Ontology 模板 → Shopify 适配国际电商差异** — 多币种、多语言、GraphQL 优先 |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 | 全文 |
| 先方案后代码 | 通过前不写行业定制码；缺口回馈**通用平台** |
| 整体孪生 | 目标是 Shopify 独立站业务世界在 AOS 可运营、可感知、可治理 |
| 模板复用 | 微商城（Niushop）8 大领域模型为基线，仅适配国际电商差异 |
| 零行业定制码 | 平台差异通过 Connector 配置 / OT / OKF 映射消解，禁止 `shopify-*` Host 分支 |

---

## 1. 一句话目标

> 将 Shopify 独立站（Products · Orders · Customers · Inventory · Fulfillment · Payments）  
> **整体映射**为 AOS 数字孪生，**复用**微商城 8 大领域模型，  
> 针对 Shopify 的 **GraphQL Admin API + Webhook 事件驱动 + 多币种/多语言/多 Location** 做适配层。

```text
微商城（基准模板）              Shopify（适配增量）
────────────────              ────────────────────
JDBC 直连 MySQL               GraphQL Admin API（REST 已 Legacy）
302 张表单表 Sync              Webhook 事件驱动 + 按需查询
site_id 多租户                 Shop 单店 + multi-Location
商品/订单/会员 8 域            同 8 域 + Inventory 独立域 + 多币种
CNY 单一币种                   多币种（shopMoney/presentmentMoney）
```

---

## 2. Shopify 平台画像

### 2.1 平台概况

| 维度 | 内容 |
|------|------|
| 平台定位 | 全球最大独立站 SaaS（~400 万商家） |
| Admin API | **GraphQL 为主**（2024-10 起 REST 已 Legacy → 2025-04 新 App 必须 GraphQL） |
| 端点 | `https://{shop}.myshopify.com/admin/api/2026-01/graphql.json` |
| 认证 | OAuth 2.0 → `X-Shopify-Access-Token` header（permanent，需 scope 授权） |
| 版本 | 季度版本（2026-01 / 2026-04 / 2026-07），回退支持 12 个月 |
| 数据格式 | JSON（GraphQL 原生） |
| GID 命名 | `gid://shopify/{ObjectType}/{id}`，如 `gid://shopify/Product/1321540321336` |
| 速率限制 | **基于成本**：标准店铺 100 点 budget、50/s 恢复。GraphQL 查询含 `extensions.cost` |
| Webhook | 事件驱动（`orders/create`、`products/update` 等 60+ 事件），推荐替代轮询 |
| Bulk Operations | GraphQL `bulkOperationRunQuery`，支持大数据量导出 |
| SDK 支持 | Node.js / Ruby / Remix / cURL |

### 2.2 核心 GraphQL 对象（对应 8 域）

| 域 | GraphQL Object | 关键字段 |
|----|---------------|---------|
| 店铺 | `Shop` | name, currencyCode, plan, timezone |
| 商品 | `Product` → `ProductVariant` | id, title, status, variants { sku, price, inventoryQuantity }, images { url } |
| 订单 | `Order` | id, name, financialStatus, fulfillmentStatus, lineItems { title, quantity, variant { sku } }, totalPriceSet, shippingAddress |
| 会员 | `Customer` | id, email, firstName, lastName, numberOfOrders, addresses |
| 库存 | `InventoryItem` / `InventoryLevel` | location-based: available, onHand |
| 履约 | `Fulfillment` / `FulfillmentOrder` | status, trackingInfo, location |
| 支付 | `Order.transactions` | gateway, amount, currency, status |
| 折扣 | `DiscountCode` / `PriceRule` | code, usageCount, value |

### 2.3 与国内电商的关键差异

| 维度 | 国内电商（淘宝/拼多多） | **Shopify** |
|------|----------------------|-----------|
| API 风格 | REST（不同平台不同签名） | **GraphQL 统一端点** |
| 数据获取 | 轮询（或增量接口） | **Webhook 推送优先 + GraphQL 按需查询** |
| 货币 | CNY 单一 | **多币种**（shopMoney + presentmentMoney，分开记录） |
| 物流 | 菜鸟/快递公司编码 | 第三方 Carrier API（USPS/UPS/FedEx/DHL…）+ 自定承运商 |
| 会员 | 平台统一会员 | **独立站自有会员**（隐私可控，email/phone 全部可获取） |
| 库存模型 | 简单 SKU 数量 | **多 Location 库存**（warehouse/store/3PL 分仓追踪） |
| 支付 | 支付宝 | 多网关（Shopify Payments / PayPal / Stripe / 手动） |
| 店铺模型 | 1 平台 → 多店 | **1 店 = 1 myshopify.com 子域**（独立品牌站模式） |

---

## 3. 整体孪生范围（按域）

### 3.1 域分级

| 级 | 名称 | GraphQL Object | 说明 | 波次 |
|----|------|---------------|------|------|
| **T0** | 店铺 | `Shop` | 币种、时区、Plan、域名 | W1 |
| **T1** | 商品 | `Product` + `ProductVariant` + `Collection` | SPU/SKU/合集，支持 2000 变体 | W1 |
| **T2** | 订单 | `Order` + `LineItem` | 含多币种、shippingAddress | W1 |
| **T3** | 会员 | `Customer` + `Address` | email 直出（隐私可控） | W1 |
| **T4** | 库存 | `InventoryLevel`（per Location） | **多仓追踪**→ 新建 Inventory Object | W2 |
| **T5** | 履约 | `FulfillmentOrder` + `Fulfillment` | 国际物流 tracking | W2 |
| **T6** | 支付 | `Transaction`（内嵌 Order） | 多网关 + 多币种金额 | W2 |
| **T7** | 折扣 | `PriceRule` + `DiscountCode` | 独立营销域 | W3 |
| **T8** | Metafields | `Metafield`（自定义扩展） | 商家自定义属性 → OT 扩展 Prop | W3 |

### 3.2 Shopify 特有概念

| 概念 | GraphQL | 说明 | AOS 处理 |
|------|---------|------|---------|
| **Location** | `Location` | 物理仓库/门店/3PL，库存按 Location 分账 | 新建 Location Object Type |
| **Collection** | `Collection` | 商品分组（手动/智能规则） | Link: Goods → Collection |
| **Metafield** | `Metafield` | 商家自定义 KV 属性（namespace + key + value） | OT ExtraProps 映射 |
| **Shopify Payments** | `ShopPayments` | 内置支付网关 | Payment.gateway 枚举值 |
| **DraftOrder** | `DraftOrder` | 商家后台创建的草稿订单 | 可选入孪生（客服场景） |

---

## 4. Ontology 目标态（对象与关系）

### 4.1 Object Type 清单

| Object Type | 主键 | GraphQL Object | 说明 | vs 微商城增量 |
|-------------|------|---------------|------|-------------|
| **Shop** | shopId | `Shop` | 独立站根 | 新增（微商城 site 对齐） |
| **Goods** | productId | `Product` | SPU | 对齐 |
| **GoodsSku** | variantId | `ProductVariant` | SKU（交易落点） | 对齐 |
| **GoodsCollection** | collectionId | `Collection` | 商品合集 | **新增** |
| **Order** | orderId | `Order` | 故事核 | 新增 `presentmentCurrency` / `shopMoney` 双币种 Prop |
| **OrderLine** | lineItemId | `LineItem` | 订单行 | 对齐 |
| **Customer** | customerId | `Customer` | 会员 | **含 email/phone 完整信息**（国内平台脱敏） |
| **CustomerAddress** | addressId | `CustomerAddress` | 收货地址簿 | 含 countryCode 国际化 |
| **InventoryLevel** | inventoryItemId+locationId | `InventoryLevel` | 分仓库存 | **新建**（国内无此模型） |
| **Location** | locationId | `Location` | 仓库/门店 | **新建** |
| **Fulfillment** | fulfillmentId | `Fulfillment` | 国际物流履单 | 对齐 express_package |
| **Payment** | transactionId | `Transaction` | 支付 | 多币种金额 |
| **DiscountCode** | codeId | `DiscountCode` | 折扣码 | 新建 |
| **Metafield** | metafieldId | `Metafield` | 自定义属性 | 新建（可薄） |

### 4.2 Link Type（核心）

| Link | from → to |
|------|-----------|
| `Order.onShop` | Order → Shop |
| `Order.placedBy` | Order → Customer |
| `Order.lines` | Order → OrderLine |
| `OrderLine.ofVariant` | OrderLine → GoodsSku |
| `GoodsSku.ofProduct` | GoodsSku → Goods |
| `Goods.inCollection` | Goods → GoodsCollection |
| `GoodsSku.inventoriedAt` | GoodsSku → InventoryLevel |
| `InventoryLevel.atLocation` | InventoryLevel → Location |
| `Order.fulfilledBy` | Order → Fulfillment |
| `Order.paidBy` | Order → Payment |
| `Customer.inShop` | Customer → Shop |

### 4.3 Funnel（订单 · 国际化状态）

```text
pending → confirmed → fulfilled → completed
  ↘ refunded → cancelled
```

> Shopify 订单状态通过 `displayFinancialStatus`（pending/authorized/paid/partially_paid/refunded/voided）  
> + `displayFulfillmentStatus`（unfulfilled/partial/fulfilled/restocked）组合描述。  
> OKF 需配置双纬度映射。

---

## 5. 数据接入策略

### 5.1 总原则

| 路径 | 用途 | Shopify 用法 |
|------|------|-------------|
| **A. Webhook 事件驱动（主路径）** | 实时订单/商品变更 | `orders/create`、`products/update` → Push → AOS Ingestion Endpoint |
| **B. GraphQL 按需查询** | 首次全量同步 / 对账 / 补查 | 单条 `order(id:)`、分页 `orders(first:50)` |
| **C. Bulk Operations** | 大数据量导出（万级订单） | `bulkOperationRunQuery` → JSONL → file-local → Dataset |
| **D. REST（Legacy）** | 仅旧商户过渡 | 不推荐新接入 |

### 5.2 接入架构

```text
Shopify Merchant Store
      │
      ├── Webhook Subscription（实时）
      │     orders/create, products/update, customers/create,
      │     inventory_levels/update, fulfillments/create ...
      │     ↕ HTTPS POST → AOS Webhook Receiver（需新建）
      │
      └── GraphQL Admin API（按需 / 首次全量）
            X-Shopify-Access-Token header
            ↕ POST https://{shop}.myshopify.com/admin/api/2026-01/graphql.json
```

### 5.3 AOS 平台缺口（接入前提）

| 编号 | 缺口 | 影响 | 优先级 |
|------|------|------|--------|
| **G-REST-01** | REST API Connector 类型 | 国内电商阻塞 | 🔴 阻塞 |
| **G-OAUTH-01** | OAuth 2.0 Token Manager | 通用 | 🔴 阻塞 |
| **G-GQL-01** | **GraphQL Connector 类型** | Shopify 专属（GraphQL 端点） | 🟡 Shopify 专属 |
| **G-WEBHK-01** | **Webhook Receiver 端点** | Shopify 实时推送落点 | 🟡 Shopify 专属 |
| **G-CURR-01** | 多币种字段支持 | OT Prop 需支持 `CurrencyAmount` 类型 | 🟢 通用增强 |

---

## 6. 从物理到孪生的主链路

```text
Shopify Store（独立站）
      │
      ├── Webhook Push（实时）
      │     HTTPS POST → AOS Webhook Receiver
      │     ↓
      │   Ingestion Pipeline → Dataset（增量）
      │
      └── GraphQL Query（首次 + 对账）
            Connector → Source → Sync → Dataset（全量）
      │
      ▼
  OKF 映射 → Funnel 水合 → Object / Link
      ▼
  ┌─────────┬──────────┬────────────┬───────────┐
  ▼         ▼          ▼            ▼
 COP态势   Inbox运营  Graph/Buddy  Analytics
  多店全局   新单/缺货/      独立站运营  多币种报表
            履约异常
```

---

## 7. 实施波次

| 波次 | 内容 | 依赖 | 状态 |
|------|------|------|------|
| **P0** | 本方案通过（本文） | — | ✅ v1.0 |
| **P1** | Shopify Partner 账号 + 开发店创建 | — | ⬜ 待执行 |
| **P1** | GraphQL Schema 探索（query/mutation 清单） | 开发店 | ⬜ 待执行 |
| **P2** | GraphQL Connector 类型（平台通用能力） | 220plan W2+ | 🟡 阻塞 |
| **P2** | Webhook Receiver 端点 | 220plan W2+ | 🟡 阻塞 |
| **P2** | OAuth 2.0 Token Manager（通用） | 220plan W2+ | 🔴 阻塞 |
| **W1** | 沙箱数据接入验证（商品 + 订单 + 会员） | P2 完成 | ⬜ 待执行 |
| **W2** | 全域接入 + 多 Location 库存 + 态势上线 | W1 通过 | ⬜ 待执行 |

---

## 8. 与国内电商的关键差异总结

| 维度 | 国内电商 | Shopify | AOS 需要做什么 |
|------|---------|---------|-------------|
| API 协议 | REST + 各平台不同签名 | **GraphQL 统一 + Webhook** | 新增 GraphQL Connector + Webhook Receiver |
| 货币 | CNY 单一 | **多币种**（每订单记录两个币种） | OT Prop 支持 `MoneyBag` 类型 |
| 库存 | 简单 SKU 数量 | **多 Location 分仓** | 新建 Location + InventoryLevel Object |
| 会员数据 | 脱敏（手机/email 不可见） | **完整**（email 直出） | 多出 email 等 PII 字段 |
| 物流 | 菜鸟统一 | Carrier API（USPS/UPS…） | 物流追踪接口不同，但模型可比 |
| 事件机制 | 无/弱 | **Webhook 60+ 事件** | 需要事件驱动的数据接入路径 |

---

## 9. 下一步行动

| 优先级 | 行动 | 阻塞条件 |
|-------|------|---------|
| **P0 ✅** | 本方案完成 | — |
| **P1** | Shopify Partner 账号注册 + 开发店创建 | — |
| **P1** | GraphQL Schema 探索文档（query/mutation 清单） | 开发店 |
| **P2** | OAuth 2.0 Token Manager（通用） | 220plan W2+ 基础设施 |
| **P2** | GraphQL Connector + Webhook Receiver | 220plan W2+ 基础设施 |

> **版本**：v1.0 · 2026-07-22 · 总体分析计划  
> **变更日志**：  
> | 版本 | 日期 | 说明 |  
> | --- | --- | --- |  
> | v1.0 | 2026-07-22 | 初版 · 基于 Shopify Admin GraphQL API 调研 · 全球独立站模型 · 多币种/多 Location/Webhook 事件驱动 · GraphQL Connector + Webhook Receiver 缺口 |
