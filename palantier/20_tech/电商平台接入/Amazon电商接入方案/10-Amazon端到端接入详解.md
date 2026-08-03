# Amazon · 端到端接入详解

> **版本**：v1.0 · 2026-07-23
> **参照**：`../000-电商平台接入总方案.md` Stage 1-6 框架
> **定位**：Phase 2 最后接入平台，**最复杂的全球平台**（20+ 区域、SP-API、AWS Sig V4、FBA 状态机）
> **依赖**：G2（OAuth Token Manager）+ G5（AWS Signature V4）
> **复杂度**：⭐⭐⭐⭐⭐

---

## Stage 1 · 数据接入（Data Connection）

### 1.1 连接器配置

| 项 | 配置 |
|----|------|
| 连接器类型 | **REST API Connector**（SP-API 专用模板） |
| 端点（NA） | `https://sellingpartnerapi-na.amazon.com` |
| 端点（EU） | `https://sellingpartnerapi-eu.amazon.com` |
| 端点（FE） | `https://sellingpartnerapi-fe.amazon.com` |
| 认证方式 | **LWAAuth**（Login with Amazon）→ `access_token`（有效期 **1h**）+ **STS Token**（AWS IAM） |
| 签名算法 | **AWS Signature Version 4**（`AWS4-HMAC-SHA256`） |
| 数据格式 | JSON |
| 速率限制 | 各 API 独立限制，响应头含 `x-amzn-RateLimit-Limit` |
| 区域 | **NA**（US/CA/MX/BR）· **EU**（UK/DE/FR/IT/ES/NL/SE/PL）· **FE**（JP/AU/SG） |
| 安全合规 | **SP-API Guard**（AWS 部署数据必须通过 Data Protection Policy） |

### 1.2 双重认证流程（LWAAuth + AWS Sig V4）

```
Step 1 · LWAAuth 获取 access_token（1h 有效期）
  POST https://api.amazon.com/auth/o2/token
  Body: grant_type=refresh_token&refresh_token=****&client_id=****&client_secret=****
  → access_token（Bearer，1h 过期）

Step 2 · STS Token 获取 AWS 临时凭证（如果使用 IAM Role）
  POST https://sts.amazonaws.com
  Action: AssumeRole
  → AWS_SECRET_ACCESS_KEY + AWS_SESSION_TOKEN

Step 3 · AWS Signature V4 签名每个 API 请求
  Authorization: AWS4-HMAC-SHA256
    Credential=AKID****/20260723/us-east-1/execute-api/aws4_request,
    SignedHeaders=host;x-amz-date,
    Signature=****
  x-amz-access-token: {access_token from Step 1}

⚠️ Token 轮换：
  LWAAuth access_token 1h 过期 → refresh_token 自动刷新（G2）
  STS Token 1h 过期 → AssumeRole 自动刷新
```

### 1.3 Source 创建

```
Step 1 · 选择类型：REST API（SP-API 模板）
Step 2 · 连接方式：直连
Step 3 · 命名：
  prod-spapi-amazon-na（北美）
  prod-spapi-amazon-eu（欧洲）
  prod-spapi-amazon-fe（远东）
Step 4 · 配置：
  LWA Client ID: ****
  LWA Client Secret: ****
  Refresh Token: ****
  AWS Access Key: ****
  AWS Secret Key: ****
  SP-API Endpoint: https://sellingpartnerapi-na.amazon.com
  Marketplace IDs: ATVPDKIKX0DER (US), A2EUQ1WTGCTBG2 (CA), A1AM78C64UM0Y8 (MX)
```

### 1.4 区域与 Marketplace 映射

| 区域 | Marketplace ID | 国家 | 端点 |
|------|---------------|------|------|
| NA | `ATVPDKIKX0DER` | 🇺🇸 美国 | sellingpartnerapi-na |
| NA | `A2EUQ1WTGCTBG2` | 🇨🇦 加拿大 | sellingpartnerapi-na |
| NA | `A1AM78C64UM0Y8` | 🇲🇽 墨西哥 | sellingpartnerapi-na |
| EU | `A1F83G8C2ARO7P` | 🇬🇧 英国 | sellingpartnerapi-eu |
| EU | `A1PA6795UKMFR9` | 🇩🇪 德国 | sellingpartnerapi-eu |
| EU | `A13V1IB3VIYZZH` | 🇫🇷 法国 | sellingpartnerapi-eu |
| FE | `A1VC38T7YXB528` | 🇯🇵 日本 | sellingpartnerapi-fe |
| FE | `A39IBJ37TRP1C6` | 🇦🇺 澳大利亚 | sellingpartnerapi-fe |

### 1.5 探索源（SP-API 模块）

| API 模块 | 用途 | 版本 |
|----------|------|------|
| **Orders API** | 订单查询（FBA+MFN） | v2026-01-01 |
| **Catalog Items API** | ASIN 商品目录 | v2022-04-01 |
| **Listings Items API** | Listing(SKU) 管理 | v2021-08-01 |
| **FBA Inventory API** | **FBA 库存**（5 种状态） | v1 |
| **Fulfillment Inbound API** | FBA 入库货件 | v2024-03-20 |
| **Fulfillment Outbound API** | MCF 多渠道配送 | v2020-07-01 |
| **Merchant Fulfillment API** | MFN 自发货 | v0 |
| **Finances API** | 财务事件 | v2024-06-19 |
| **Product Pricing API** | 竞争价格 | v2022-05-01 |
| **Reports API** | **批量报表** | v2021-06-30 |
| **Feeds API** | **批量上传** | v2021-06-30 |
| **Notifications API** | **事件推送** | v1 |

---

## Stage 2 · 数据同步（Sync）

### 2.1 同步策略

| 数据域 | API | 事务类型 | 增量方式 | 调度 |
|--------|-----|----------|----------|------|
| **订单** | Orders API `GET /orders/v0/orders` | APPEND | `LastUpdatedAfter` | 每 30 分钟 |
| 商品目录 | Catalog Items API | SNAPSHOT | 全量 | 每日 |
| **FBA 库存** | FBA Inventory API | SNAPSHOT | 全量 | **每 1 小时** |
| Listing | Listings Items API | SNAPSHOT | 全量 | 每 6 小时 |
| 财务 | Finances API | APPEND | `PostedAfter` | 每 1 小时 |
| **批量报表** | Reports API | — | 异步报表 | 每日/每周 |
| 事件推送 | Notifications API | 实时 | `ORDER_CHANGE` 订阅 | 实时 |

### 2.2 FBA 库存 5 种状态

```
Amazon FBA 库存状态（其他平台没有的状态机）：
  ┌──────────────┐
  │ research     │ → 亚马逊正在研究该库存（异常调查）
  └──────┬───────┘
         │
  ┌──────▼───────┐
  │ fulfillable  │ → 可售库存（正常）
  └──────┬───────┘
         │
  ┌──────▼───────┐    ┌──────────────┐
  │ unfulfillable│    │ inbound      │ → 在途库存（正在入库）
  │ (不可售)     │    │ working      │ → 在处理中
  └──────────────┘    └──────────────┘

AOS 库存同步需处理全部 5 种状态的转换：
  GET /fba/inventory/v1/summaries
  → granular=true（按 SKU 粒度返回）
  → 每种状态独立计数
```

### 2.3 Reports API（批量报表替代 API 轮询）

```
对于大批量数据（如全量库存、结算报告），使用 Reports API 异步获取：

Step 1: POST /reports/2021-06-30/reports
  Body: { "reportType": "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL" }

Step 2: 轮询 GET /reports/2021-06-30/reports/{reportId}
  → 状态：CREATING → PROCESSING → DONE

Step 3: GET report document URL → 下载报告文件（TSV/JSON）
```

---

## Stage 3 · 管道清洗（Pipeline Builder）

### 3.1 ASIN + Seller SKU 双标识

```sql
-- Amazon 商品有两个标识：ASIN（全球目录）和 Seller SKU（卖家自定义）
Expression:
  asin AS global_id,         -- ASIN 全球唯一
  seller_sku AS merchant_id  -- 卖家 SKU（同一 ASIN 可能多个 SKU）

-- 多区域合并
Union:
  SELECT *, 'NA' as region FROM na_products
  UNION ALL
  SELECT *, 'EU' as region FROM eu_products
  UNION ALL
  SELECT *, 'FE' as region FROM fe_products
```

### 3.2 FBA vs MFN 双轨物流处理

```sql
-- Amazon 有两种配送方式
Expression:
  CASE
    WHEN fulfillment_channel = 'AFN' THEN 'FBA'  -- Amazon 配送
    WHEN fulfillment_channel = 'MFN' THEN 'FBM'  -- 卖家自发货(MFN)
    ELSE 'unknown'
  END AS fulfillment_type

-- FBA 订单：tracking_info 可能不完整（Amazon 自己配送）
-- MFN 订单：需要卖家自己发货并上传 tracking
```

### 3.3 多区域价格合并

```sql
-- 同一 ASIN 在不同区域有不同价格
Aggregate GROUP BY asin:
  COLLECT_LIST(MAP(region, price)) AS prices_by_region
  → [{NA: 29.99}, {EU: 24.99}, {FE: 3500}]  -- 多币种

MIN(price_usd) AS min_price_global  -- 全球最低价（统一换算 USD 后）
MAX(price_usd) AS max_price_global
```

---

## Stage 4 · OKF 映射（Funnel）

### 4.1 OT 映射表（含 Amazon 特有 OT）

| SP-API 对象 | 统一 OT | 主键 | 关键映射 |
|-------------|---------|------|----------|
| `Order` | **Order** | `amazonOrderId` | orderStatus→status, orderTotal→amount |
| `OrderItem` | **OrderLine** | `orderItemId` | quantityOrdered→quantity, itemPrice→unit_price |
| `CatalogItem` | **Product** | `asin`（ASIN） | summaries[0].itemName→title, brand→brand |
| `ListItem` | **Listing** | `sku`（Seller SKU） | price, quantity→stock |
| `FbaInventorySummary` | **FbaInventory**（**新**） | `asin+marketplaceId` | **5 种状态分别映射** |
| `FulfillmentShipment` | **Shipment** | `shipmentId` | trackingItems→tracking_no |
| `FinancialEvent` | **Transaction** | `postedDate+eventId` | transactionType, amount |
| `BuyerInfo` | **Customer** | `buyerEmail`（匿名） | **Amazon 不暴露买家真实 ID** |
| `BuyableOffer` | **CompetitorPrice**（**新**） | `asin` | price, isFulfilledByAmazon |

### 4.2 Funnel 状态机

```
订单状态：Pending → Unshipped → PartiallyShipped → Shipped → Canceled / Delivered

FBA 库存状态：research → fulfillable → (unfulfillable | inbound | reserved)
```

---

## Stage 5 · 本体实例化（Ontology）

### 5.1 Amazon 特有 OT（3 个新增）

| OT | 说明 | 特有属性 |
|----|------|----------|
| **FbaInventory** | FBA 库存（5 状态） | **Amazon 独有**：researchable, fulfillable, unfulfillable, inbound_working, reserved |
| **InboundShipment** | FBA 入库货件 | **Amazon 独有**：shipmentId, destinationFulfillmentCenterId, shipmentStatus |
| **CompetitorPrice** | 竞品价格 | buyBoxPrice, lowestPrice, isFulfilledByAmazon |

### 5.2 特有 Link

| Link | from → to | 基数 | 说明 |
|------|-----------|------|------|
| `listedAs` | Listing → Product | N:1 | Seller SKU → ASIN（**双标识关联**） |
| `storedIn` | FbaInventory → Warehouse | N:1 | FBA 仓库存（Amazon 履约中心 ID） |
| `competesWith` | Product → CompetitorPrice | N:M | 同一 ASIN 的竞品定价 |
| `inboundTo` | InboundShipment → Warehouse | N:1 | 入库货件目标仓 |

### 5.3 Action Type

| Action | 函数 | 模式 | 说明 |
|--------|------|------|------|
| `updateListing` | amazon/listing.py | Write Back | 调用 Listings Items API 更新 SKU |
| `adjustPrice` | amazon/pricing.py | Write Back | 调用 Pricing API 调价 |
| `createInbound` | amazon/inbound.py | Write Back | 创建 FBA 入库货件 |
| `buyShipping` | amazon/mfn.py | Write Back | MFN 购买配送标签 |

---

## Stage 6 · 上层消费

### 6.1 Amazon 特色场景

| 场景 | 说明 |
|------|------|
| **FBA 库存 5 状态大屏** | 各状态的库存量、异常预警（research 增多） |
| **全球多区域看板** | NA/EU/FE 各区域销量、库存、定价对比 |
| **FBA 入库追踪** | 入库货件从创建到收货全链路 |
| **竞品价格监控** | Buy Box 价格变化、竞争态势 |
| **结算报表** | Finances API + Reports API 的结算对账 |
| **ASIN→SKU 映射审计** | 全球目录与卖家 SKU 的映射完整性 |

### 6.2 平台缺口

| 缺口 ID | 描述 | 优先级 |
|---------|------|--------|
| **G2** | OAuth Token Manager（1h 轮换） | **P0** |
| **G5** | AWS Signature V4 签名 | **P0（认证必需）** |
| G-AMZ-01 | 多区域 Source 管理（3 套配置） | P1 |
| G-AMZ-02 | FBA 库存 5 状态机 OT | P1 |
| G-AMZ-03 | Reports API 异步报表管道 | P2 |
| G-AMZ-04 | SP-API Guard 合规审计 | P2 |
| G-AMZ-05 | 多币种全球合并分析 | P2 |
