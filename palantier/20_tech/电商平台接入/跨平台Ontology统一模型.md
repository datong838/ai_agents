# 跨平台 Ontology 统一模型映射

> **版本**：v1.0 · 2026-07-23
> **位置**：`跨平台Ontology统一模型.md`
> **定位**：将 7 个电商平台约 110 个 OT（Object Type）归约为 **35 个统一 OT + 22 个统一 LT（Link Type）**，定义跨平台主键映射规则与字段对齐策略
> **前置依赖**：各平台 P0 总体方案 + P1 API 接口清单

---

## 1. 设计目标

| 目标 | 说明 |
|------|------|
| **统一语义** | 不同平台对同一业务实体的命名差异消除（如淘宝 `num_iid` = 微商城 `goods_id` = Amazon `asin`） |
| **增量接入** | 新平台接入时只需填写"平台→统一模型"映射表，不修改 AOS 核心 Schema |
| **跨平台查询** | 支持跨平台聚合查询（如"所有平台昨日订单量"），按统一 OT 聚合 |
| **数据治理** | 字段级脱敏、Marking、审计统一在统一模型层处理，各平台 Connector 只管数据搬运 |

## 2. 设计原则

1. **基线对齐微商城**：微商城 18 OT 作为基准模板，其他平台尽量复用
2. **平台特有 OT 独立保留**：不强行归约（如抖音 Creator/Commission、Amazon FBAInventory）
3. **统一 OT = 语义 + 主键映射 + 核心字段集**：每个统一 OT 定义一组必填核心字段，平台可扩展
4. **Link Type 统一命名**：跨平台关系语义统一（如 `Order.lines` 在所有平台表示"订单包含订单行"）

---

## 3. 35 个统一 Object Type

### 3.1 全景总览

| 域 | 统一 OT | 微商城 | 淘宝/天猫 | 拼多多 | 京东 | 抖音 | Shopify | Amazon |
|----|---------|--------|----------|--------|------|------|---------|--------|
| **租户** | `Shop` | Site/Weapp | Shop | Shop | Shop | Shop | Shop | Marketplace |
| **租户** | `ShopCategory` | — | — | — | ShopCategory | — | — | — |
| **商品** | `Product` | Goods | Item | Goods | Product(SPU) | Product | Goods | Goods(ASIN) |
| **商品** | `ProductSku` | GoodsSku | Item.sku | GoodsSku | SKU | SKU | ProductVariant | GoodsSku(SellerSKU) |
| **商品** | `Category` | GoodsCategory | cid | GoodsCategory | Category | Category | Collection | ProductType |
| **商品** | `Brand` | (goods字段) | Brand | — | Brand | Brand | — | — |
| **商品** | `FreightTemplate` | — | — | — | — | FreightTemplate | — | — |
| **订单** | `Order` | Order | Trade | Order | Order(父单) | Order | Order | Order |
| **订单** | `OrderLine` | OrderLine | Trade.order | OrderLine | OrderLine(子单) | OrderLine | LineItem | OrderItem |
| **订单** | `Payment` | Payment | (嵌入) | (嵌入) | Payment | Payment | Transaction | FinanceEvent |
| **订单** | `Invoice` | — | — | Invoice | Invoice | — | — | — |
| **会员** | `Customer` | Member | Member(脱敏) | (隐含) | Member | Member | Customer | (有限) |
| **会员** | `CustomerAddress` | MemberAddress | — | — | — | — | CustomerAddress | — |
| **会员** | `CustomerLevel` | MemberLevel | — | — | MemberLevel | — | — | — |
| **物流** | `Shipment` | ExpressPackage | (物流字段) | ExpressPackage | Logistics+Package | Logistics | Fulfillment | Fulfillment |
| **物流** | `LogisticsTrace` | — | trace | LogisticsTrace | trace | track | — | — |
| **售后** | `AfterSales` | — | (子状态) | — | AfterSales | AfterSales | — | — |
| **售后** | `Refund` | — | (子状态) | Refund | Refund | (嵌入) | (嵌入) | — |
| **售后** | `Exchange` | — | — | — | — | ExchangeProcess | — | — |
| **库存** | `InventoryLevel` | (sku字段) | — | — | — | — | InventoryLevel | FBAInventory |
| **库存** | `Location` | Store | — | — | — | — | Location | Marketplace |
| **评价** | `Review` | — | Review | — | Comment | — | — | — |
| **营销** | `Promotion` | — | (Phase2) | Promotion | — | — | DiscountCode | — |
| **分销** | `Creator` | — | — | — | — | Creator | — | — |
| **分销** | `Commission` | CommissionLog | 淘宝客 | 多多进宝 | 京东联盟 | Commission | — | Associates |
| **分销** | `Distribution` | — | — | — | — | Distribution | — | — |
| **内容** | `LiveSession` | — | — | — | — | LiveSession | — | — |
| **内容** | `VideoContent` | — | — | — | — | VideoContent | — | — |
| **内容** | `Article` | Article | — | — | — | — | — | — |
| **内容** | `HelpDoc` | HelpDoc/PolicyDoc | — | — | — | — | — | — |
| **通知** | `Notice` | Notice | — | — | — | — | — | — |
| **Amazon** | `InboundShipment` | — | — | — | — | — | — | InboundShipment |
| **Amazon** | `Report` | — | — | — | — | — | — | Report |
| **Shopify** | `Metafield` | — | — | — | — | — | Metafield | — |
| **Shopify** | `DiscountCode` | — | — | — | — | — | DiscountCode | — |

> **统计**：35 个统一 OT，覆盖 7 个平台约 110 个平台级 OT。复用率最高的统一 OT 为 `Product` / `ProductSku` / `Order` / `OrderLine`（7/7 平台覆盖）。

### 3.2 核心 OT 字段规范（Top 10）

#### Order（订单）

| 统一字段 | 类型 | 微商城 | 淘宝 | 拼多多 | 京东 | 抖音 | Shopify | Amazon |
|----------|------|--------|------|--------|------|------|---------|--------|
| `orderId` | String | orderId | tid | orderSn | orderId | shopOrderId | id | amazonOrderId |
| `status` | Enum | order_status | status | order_status | orderState | orderStatus | financialStatus | orderStatus |
| `totalAmount` | Decimal | order_money | payment | pay_amount | orderPayment | payAmount | totalPrice | orderTotal |
| `createdAt` | DateTime | create_time | created | created_time | orderStartTime | createTime | createdAt | purchaseDate |
| `currency` | String | CNY(默认) | CNY | CNY | CNY | CNY | currencyCode | currencyId |
| `buyerId` | String | buyer_id | buyer_nick | — | pin | encryptedBuyer | customer.id | buyerEmail |
| `shippingAddress` | JSON | receiver_* | receiver_* | receiver_* | consigneeInfo | encryptPostAddress | shippingAddress | shippingAddress |
| `paymentMethod` | String | pay_type | pay_type | pay_type | payType | payType | gateway | paymentMethod |
| `remark` | String | buyer_message | buyer_message | buyer_remark | orderRemark | buyerWords | note | buyerInfo |

#### Product（商品 SPU）

| 统一字段 | 类型 | 微商城 | 淘宝 | 拼多多 | 京东 | 抖音 | Shopify | Amazon |
|----------|------|--------|------|--------|------|------|---------|--------|
| `productId` | String | goods_id | num_iid | goodsId | wareId | product_id | id | asin |
| `title` | String | goods_name | title | goodsName | title | name | title | itemName |
| `categoryId` | String | category_id | cid | catId | cid3 | category_id | collectionId | productType |
| `brandId` | String | brand_id | brandId | — | brandId | brand_id | vendor | — |
| `mainImage` | URL | goods_image | pic_url | image_url | imgDo | pic | featuredImage | mainImage |
| `images` | URL[] | sku_image_albums | small_images | image_url | imgDo | pics | images | images |
| `status` | Enum | goods_state | approveStatus | is_onsale | state | status | status | listingsStatus |
| `createdAt` | DateTime | create_time | — | — | — | create_time | createdAt | — |
| `skus` | Ref[] | sku_list | skus | sku_list | skuList | spec | variants | — |

#### Customer（会员/买家）

| 统一字段 | 类型 | 微商城 | 淘宝 | 拼多多 | 京东 | 抖音 | Shopify | Amazon |
|----------|------|--------|------|--------|------|------|---------|--------|
| `customerId` | String | member_id | buyerId(脱敏) | — | pin | open_id | id | buyerEmail |
| `nickname` | String | nickname | buyer_nick | — | pin | nick | displayName | — |
| `phone` | String(脱敏) | mobile | — | — | — | encryptMobile | phone | — |
| `level` | String | level_id | — | — | level | — | — | — |
| `registeredAt` | DateTime | reg_time | — | — | — | — | createdAt | — |
| `totalOrders` | Integer | (计算) | — | — | — | — | ordersCount | — |

#### Shipment（物流包裹）

| 统一字段 | 类型 | 微商城 | 淘宝 | 拼多多 | 京东 | 抖音 | Shopify | Amazon |
|----------|------|--------|------|--------|------|------|---------|--------|
| `shipmentId` | String | package_id | — | logisticsId | waybillCode | package_id | id | fulfillmentId |
| `orderId` | Ref | order_id | tid | orderSn | orderId | order_id | order_id | amazonOrderId |
| `carrier` | String | express_company_id | company_code | expressCode | waybillType | company_code | trackingCompany | carrier |
| `trackingNo` | String | express_no | out_sid | trackingNo | waybillCode | trackingNo | trackingNumber | trackingNumber |
| `status` | Enum | status | status | — | state | — | status | fulfillmentStatus |
| `shippedAt` | DateTime | shipping_time | — | shippingTime | — | — | createdAt | shipDate |

#### Refund（退款）

| 统一字段 | 类型 | 微商城 | 拼多多 | 京东 | 抖音 |
|----------|------|--------|--------|------|------|
| `refundId` | String | — | refundId | refundId | aftersalesId |
| `orderId` | Ref | order_id | orderSn | orderId | order_id |
| `orderLineId` | Ref | order_goods_id | orderSn+skuId | orderLineId | order_line_id |
| `amount` | Decimal | refund_real_money | refund_amount | refundMoney | refundMoney |
| `reason` | String | refund_reason | refund_reason | reason | reason |
| `status` | Enum | refund_action | handle_status | state | status |
| `type` | Enum | — | after_sales_type | type | aftersales_type |

---

## 4. 22 个统一 Link Type

### 4.1 通用 Link Type（7/7 平台）

| 统一 LT | 语义 | 微商城 | 淘宝 | 拼多多 | 京东 | 抖音 | Shopify | Amazon |
|---------|------|--------|------|--------|------|------|---------|--------|
| `Order.lines` | 订单→订单行 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `OrderLine.ofSku` | 订单行→SKU | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ProductSku.ofProduct` | SKU→商品 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `Product.inCategory` | 商品→分类 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `Order.placedBy` | 订单→会员 | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| `Order.paidBy` | 订单→支付 | ✅ | — | — | ✅ | ✅ | ✅ | ✅ |
| `Order.fulfilledBy` | 订单→物流 | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ |

### 4.2 高频 Link Type（4+ 平台）

| 统一 LT | 语义 | 平台覆盖 |
|---------|------|---------|
| `Product.ofBrand` | 商品→品牌 | 淘宝/京东/抖音 (+ 微商城字段) |
| `OrderLine.shippedBy` | 订单行→物流 | 拼多多/京东/抖音/Shopify |
| `Order.hasRefund` | 订单→退款 | 拼多多/京东/抖音 (+ 微商城嵌入) |
| `Shop.sellsProduct` | 店铺→商品 | 淘宝/京东/抖音/Shopify |
| `Customer.inShop` | 会员→店铺 | 微商城/Shopify/Amazon |

### 4.3 平台特有 Link Type

| 统一 LT | 语义 | 平台 |
|---------|------|------|
| `Product.hasFreightTemplate` | 商品→运费模板 | 抖音 |
| `Order.hasInvoice` | 订单→发票 | 拼多多/京东 |
| `Order.hasAfterSales` | 订单→售后 | 京东/抖音 |
| `Order.hasCommission` | 订单→佣金 | 抖音 |
| `Commission.toCreator` | 佣金→达人 | 抖音 |
| `Creator.promotes` | 达人→商品 | 抖音 |
| `Creator.hostsLive` | 达人→直播 | 抖音 |
| `Creator.makesVideo` | 达人→视频 | 抖音 |
| `ProductSku.inventoriedAt` | SKU→库存水位 | Shopify/Amazon |
| `InventoryLevel.atLocation` | 库存→仓库 | Shopify |
| `GoodsSku.inMarketplace` | SKU→市场 | Amazon |
| `Order.onMarketplace` | 订单→市场 | Amazon |
| `Order.hasShipment(FBA)` | 订单→入库 | Amazon |
| `Order.hasFinanceEvent` | 订单→财务 | Amazon |
| `FBAInventory.inMarketplace` | FBA库存→市场 | Amazon |

---

## 5. 平台映射表使用指南

### 5.1 新平台接入映射流程

```text
Step 1: 确定平台的业务域覆盖（商品/订单/会员/物流/售后/营销/分销/内容）
Step 2: 为每个域的核心实体选择统一 OT
Step 3: 填写「平台主键 → 统一 OT 主键」映射表
Step 4: 填写「平台字段 → 统一 OT 核心字段」映射表（字段级）
Step 5: 确定平台特有 OT（无法归约的独立实体）
Step 6: 定义 Link Type 映射
Step 7: 输出 platform_mapping.json → 注册到 AOS Ontology Manager
```

### 5.2 平台映射表 JSON Schema（示例）

```json
{
  "platform": "taobao",
  "version": "1.0",
  "objectTypes": {
    "Order": {
      "platformType": "Trade",
      "primaryKey": { "tid": "orderId" },
      "fieldMapping": {
        "tid": "orderId",
        "status": "status",
        "payment": "totalAmount",
        "created": "createdAt",
        "buyer_nick": "buyerId"
      },
      "customFields": {
        "adjust_fee": "调整费",
        "auction_sku": "SKU快照"
      }
    }
  },
  "linkTypes": {
    "Order.lines": {
      "sourceKey": "oid",
      "targetType": "OrderLine",
      "targetKey": "oid"
    }
  }
}
```

---

## 6. 跨平台聚合查询示例

### 6.1 统一 OT 的 AOS Function 查询

```python
# 跨平台查询：所有平台昨日订单
@function(output=Order)
def cross_platform_orders(platforms: list[str], date: str) -> ObjectSet:
    results = ObjectSet()
    for platform in platforms:
        # Connector 自动处理平台主键 → 统一 OT 主键映射
        orders = connectors[platform].query(
            "Order",
            filter={"createdAt": {"$gte": date}}
        )
        results.union(orders)
    return results

# 跨平台聚合：全渠道GMV
@function(output=Decimal)
def total_gmv(platforms: list[str], date_range: tuple) -> Decimal:
    orders = cross_platform_orders(platforms, date_range)
    return orders.sum("totalAmount")
```

### 6.2 Workshop 跨平台看板

```text
Workshop Workshop:
  ┌──────────────────────────────────────────┐
  │  全渠道GMV总览（跨平台聚合看板）              │
  │                                          │
  │  ┌────────┐ ┌────────┐ ┌────────┐      │
  │  │ 微商城  │ │ 淘宝   │ │ 拼多多  │      │
  │  │ ¥12,340│ │ ¥45,600│ │ ¥23,100│      │
  │  └────────┘ └────────┘ └────────┘      │
  │  ┌────────┐ ┌────────┐ ┌────────┐      │
  │  │ 京东   │ │ 抖音   │ │ Amazon │      │
  │  │ ¥38,900│ │ ¥15,600│ │ $2,340 │      │
  │  └────────┘ └────────┘ └────────┘      │
  │                                          │
  │  [跨平台Top 10热销商品表]                   │
  │  [跨平台售后率趋势图]                      │
  └──────────────────────────────────────────┘
```

---

## 7. 35 OT × 7 平台覆盖矩阵

| 统一 OT | 微商城 | 淘宝 | 拼多多 | 京东 | 抖音 | Shopify | Amazon | 覆盖率 |
|---------|:------:|:----:|:------:|:----:|:----:|:-------:|:------:|:------:|
| `Shop` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| `Product` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| `ProductSku` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| `Category` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| `Order` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| `OrderLine` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| `Customer` | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | 86% |
| `Shipment` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| `Payment` | ✅ | — | — | ✅ | ✅ | ✅ | ✅ | 71% |
| `Brand` | — | ✅ | — | ✅ | ✅ | — | — | 29% |
| `Refund` | — | — | ✅ | ✅ | ✅ | — | — | 43% |
| `AfterSales` | — | — | — | ✅ | ✅ | — | — | 29% |
| `Invoice` | — | — | ✅ | ✅ | — | — | — | 29% |
| `Review` | — | ✅ | — | ✅ | — | — | — | 29% |
| `Promotion` | — | — | ✅ | — | — | ✅ | — | 29% |
| `Commission` | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | 86% |
| `Creator` | — | — | — | — | ✅ | — | — | 14% |
| `LiveSession` | — | — | — | — | ✅ | — | — | 14% |
| `VideoContent` | — | — | — | — | ✅ | — | — | 14% |
| `Distribution` | — | — | — | — | ✅ | — | — | 14% |
| `FreightTemplate` | — | — | — | — | ✅ | — | — | 14% |
| `InventoryLevel` | — | — | — | — | — | ✅ | ✅ | 29% |
| `Location` | ✅ | — | — | — | — | ✅ | ✅ | 43% |
| `LogisticsTrace` | — | ✅ | ✅ | ✅ | ✅ | — | — | 57% |
| `Article` | ✅ | — | — | — | — | — | — | 14% |
| `HelpDoc` | ✅ | — | — | — | — | — | — | 14% |
| `Notice` | ✅ | — | — | — | — | — | — | 14% |
| `ShopCategory` | — | — | — | ✅ | — | — | — | 14% |
| `CustomerAddress` | ✅ | — | — | — | — | ✅ | — | 29% |
| `CustomerLevel` | ✅ | — | — | ✅ | — | — | — | 29% |
| `Exchange` | — | — | — | — | ✅ | — | — | 14% |
| `InboundShipment` | — | — | — | — | — | — | ✅ | 14% |
| `Report` | — | — | — | — | — | — | ✅ | 14% |
| `Metafield` | — | — | — | — | — | ✅ | — | 14% |
| `DiscountCode` | — | — | — | — | — | ✅ | — | 14% |

> **覆盖率统计**：
> - **100% 覆盖**（7/7 平台）：Shop, Product, ProductSku, Category, Order, OrderLine, Shipment — 这 7 个是电商本体核心
> - **86% 覆盖**（6/7 平台）：Customer, Commission
> - **57% 覆盖**（4/7 平台）：LogisticsTrace
> - **43% 覆盖**（3/7 平台）：Refund, Location
> - **29% 覆盖**（2/7 平台）：Brand, AfterSales, Invoice, Review, Promotion, InventoryLevel, CustomerAddress, CustomerLevel
> - **14% 覆盖**（1/7 平台）：Creator, LiveSession, VideoContent, Distribution, FreightTemplate, Exchange, Article, HelpDoc, Notice, ShopCategory, InboundShipment, Report, Metafield, DiscountCode

---

## 8. 与 220plan 的对接

| 220plan 任务 | 统一模型关联 |
|-------------|------------|
| W2+ #G1 REST API Connector | `Order` / `Product` 等核心 OT 的 `fieldMapping` 通过 Connector 配置注入 |
| W2+ #G2 OAuth Token Manager | 所有需要 OAuth 的平台 Connector 均依赖 Token Manager 注入认证信息 |
| Ontology Manager（W2 c） | 统一 OT Schema 注册在 Ontology Manager，平台映射表作为 OT 的 `customFields` 配置 |
| Pipeline Builder | 增量同步 Pipeline 读取平台 Connector 数据 → 按映射表转换为统一 OT → 写入 Ontology |
| Funnel 行业模板 | 每个平台的映射表 `platform_mapping.json` 作为 Funnel 模板的配置文件 |

---

## 9. 版本与变更

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-23 | 初版：35 统一 OT + 22 统一 LT + 7 平台覆盖矩阵 + Top 10 OT 字段规范 + 映射流程 + 聚合查询示例 |
