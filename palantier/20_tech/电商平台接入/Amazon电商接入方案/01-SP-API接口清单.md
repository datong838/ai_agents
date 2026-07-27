# 01 · Amazon SP-API 接口清单

> **版本**：v1.0 · 2026-07-23
> **状态**：P1 调研完成 · 筛选与 AOS 数字孪生对接相关的核心接口
> **来源**：Amazon Selling Partner API 文档（developer-docs.amazon.com/sp-api）+ 多源交叉验证
> **关联**：[00-总体分析计划](./00-Amazon-AOS对接方案.md)

---

## 1. 筛选原则

从 Amazon SP-API 100+ API 操作中按以下标准筛选：

| 原则 | 说明 |
|------|------|
| 数字孪生相关 | 仅选取与"将 Amazon 卖家业务映射为 AOS Ontology"相关的接口 |
| 读优先 | 优先 Source Sync（读），写回 Action（写）按需后置 |
| 核心优先 | MVP（T0-T4）域接口优先：Orders / Catalog / Listings / FBA Inventory / Finances |
| 区域标注 | 标注接口在 NA/EU/FE 三区域的差异 |

**筛选结果**：100+ 操作 → **40 个核心接口**（10 域 × ~4 接口/域）

---

## 2. 接口分类总览

| 业务域 | 接口数 | 读/写 | AOS 对应环节 |
|--------|-------|-------|-------------|
| 订单域 | 5 | 5 读 | Source Sync + OT |
| 商品目录域 | 4 | 4 读 | Source Sync + OT |
| Listing 域 | 4 | 2 读 / 2 写 | Source Sync + OT + Action |
| FBA 库存域 | 4 | 4 读 | Source Sync + OT |
| 履约域 | 5 | 3 读 / 2 写 | Source Sync + Function + Action |
| 财务域 | 3 | 3 读 | Source Sync + OT |
| 定价/费用域 | 3 | 3 读 | Source Sync（后置） |
| 报表域 | 4 | 4 读 | 批量数据（核心路径） |
| 批量操作域 | 3 | 1 读 / 2 写 | 批量上传/下载 |
| 通知域 | 5 | 5 读 | 事件驱动（推荐） |
| **合计** | **40** | | |

---

## 3. 详细接口清单

### 3.1 订单域（5 接口 · Orders API v0）

| # | 接口 | 方向 | 说明 | 响应要点 |
|----|------|------|------|---------|
| 1 | `GET /orders/v0/orders` | 读 | 订单列表（全量/增量） | `CreatedAfter`/`LastUpdatedAfter` 时间过滤；返回 `AmazonOrderId`、`OrderStatus`、`FulfillmentChannel`(AFN/MFN)、`MarketplaceId`、`OrderTotal` |
| 2 | `GET /orders/v0/orders/{orderId}` | 读 | 单笔订单详情 | 返回完整：`ShippingAddress`、`BuyerInfo`、`PaymentMethod`、`PurchaseDate` |
| 3 | `GET /orders/v0/orders/{orderId}/orderItems` | 读 | 订单行（SKU 明细） | 返回 `OrderItemId`、`ASIN`、`SellerSKU`、`Title`、`QuantityOrdered`、`ItemPrice` |
| 4 | `GET /orders/v0/orders/{orderId}/orderAddress` | 读 | 订单收货地址 | 仅返回地址（权限独立） |
| 5 | `GET /orders/v0/orders/{orderId}/orderBuyerInfo` | 读 | 买家信息 | `BuyerEmail`（部分脱敏）、`BuyerName` |

> **订单状态枚举：**
> - `OrderStatus`：Pending / Unshipped / PartiallyShipped / Shipped / Canceled / Unfulfillable / InvoiceUnconfirmed

### 3.2 商品目录域（4 接口 · Catalog Items API v2022-04-01）

| # | 接口 | 方向 | 说明 | 响应要点 |
|----|------|------|------|---------|
| 6 | `GET /catalog/2022-04-01/items/{asin}` | 读 | **ASIN 商品目录** | 返回 `attributes`（品牌/标题/图片/描述/规格）、`identifiers`（ASIN/UPC/EAN）、`summaries` |
| 7 | `GET /catalog/2022-04-01/items` | 读 | 批量 ASIN 查询 | `MarketplaceId` + `ASINs[]`（max 20）；批量获取商品信息 |
| 8 | `GET /catalog/2022-04-01/items/{asin}/searchRelatedItems` | 读 | 关联商品推荐 | 返回关联 ASIN（交叉销售/向上销售） |
| 9 | `GET /catalog/2022-04-01/productTypes` | 读 | 商品类型列表 | 返回 `productType` 枚举（用于 Listing 发布） |

### 3.3 Listing 域（4 接口 · Listings Items API v2021-08-01）

| # | 接口 | 方向 | 说明 | 响应要点 |
|----|------|------|------|---------|
| 10 | `GET /listings/2021-08-01/items/{sellerId}/{sku}` | 读 | **Seller SKU Listing** | 返回 `summaries`（状态/价格）、`attributes`（完整 Listing 数据） |
| 11 | `GET /listings/2021-08-01/items/{sellerId}` | 读 | 卖家 Listing 列表 | `MarketplaceId` + 分页；返回 SKU + 状态 |
| 12 | `PUT /listings/2021-08-01/items/{sellerId}/{sku}` | 写 | **创建/更新 Listing** | 全量或部分更新；支持 `PATCH` 操作（增/删/替换属性） |
| 13 | `DELETE /listings/2021-08-01/items/{sellerId}/{sku}` | 写 | 删除 Listing | 下架商品 |

> **双标识体系：** Amazon 同时使用 **ASIN**（全球统一目录 ID）和 **Seller SKU**（卖家自定义）。一个 ASIN 可对应多个 Seller SKU（不同卖家/不同成色）。

### 3.4 FBA 库存域（4 接口 · FBA Inventory API v1）

| # | 接口 | 方向 | 说明 | 响应要点 |
|----|------|------|------|---------|
| 14 | `GET /fba/inventory/v1/summaries` | 读 | **FBA 库存汇总**（5 状态） | `details` 含：`fulfillable`(可售) / `inboundWorking`(在途处理) / `inboundShipped`(在途运输) / `reserved`(预留) / `researching`(研究中) |
| 15 | `GET /fba/inventory/v1/items` | 读 | FBA 库存明细 | 按 ASIN + MarketplaceId 查询 |
| 16 | `GET /fba/inbound/v1/eligibility/itemSelection` | 读 | FBA 入库资格校验 | 检查商品是否可入库（需要 eligibility） |
| 17 | `GET /fba/inbound/2024-03-20/ inboundPlans` | 读 | FBA 入库计划列表 | 返回入库货件状态 |

> **FBA 库存 5 状态详解：**
> 
> | 状态 | 含义 |
> |------|------|
> | `fulfillable` | 可售库存（立即配送） |
> | `inboundWorking` | 在亚马逊处理中（刚到仓） |
> | `inboundShipped` | 在途运输（卖家→亚马逊仓） |
> | `reserved` | 预留（已被订单锁定/转运中） |
> | `researching` | 研究中（库存差异调查中） |

### 3.5 履约域（5 接口）

| # | 接口 | 方向 | 说明 | 响应要点 |
|----|------|------|------|---------|
| 18 | `GET /fba/outbound/2020-07-01/fulfillmentOrders` | 读 | FBA 多渠道配送订单(MCF) | FBA 为非 Amazon 订单配送 |
| 19 | `POST /fba/outbound/2020-07-01/fulfillmentOrders` | 写 | 创建 MCF 订单 | 从 FBA 库存发货给非 Amazon 客户 |
| 20 | `GET /mfn/v0/shipments/{shipmentId}` | 读 | MFN 自发货详情 | Merchant Fulfilled Network |
| 21 | `POST /mfn/v0/shipments` | 写 | 创建 MFN 配送（购买配送） | 购买承运商配送服务 |
| 22 | `GET /easyship/2022-03-23/packages` | 读 | Easy Ship 包裹查询 | 印度等特定区域配送 |

### 3.6 财务域（3 接口 · Finances API v2024-06-19）

| # | 接口 | 方向 | 说明 | 响应要点 |
|----|------|------|------|---------|
| 23 | `GET /finances/v2024-06-19/financialEvents` | 读 | 财务事件列表 | `PostedAfter`/`PostedBefore` 时间过滤；返回多类事件 |
| 24 | `GET /finances/v2024-06-19/orders/{orderId}/financialEvents` | 读 | **按订单查询财务事件** | 返回该订单的：`ProductFee`(佣金)、`ShipmentEvent`(运费)、`RefundEvent`(退款)、`ServiceFee`(服务费) |
| 25 | `GET /finances/v2024-06-19/financialEventsGroups` | 读 | 财务事件组（按结算周期） | 用于对账 |

> **财务事件类型：** ProductFee(销售佣金) / ShipmentEvent(运费) / RefundEvent(退款) / AdjustmentEvent(调整) / ServiceFeeEvent(月度服务费) / TaxWithholdingEvent(预扣税) / TrialShipmentEvent(Prime试发)

### 3.7 定价/费用域（3 接口 · 后置）

| # | 接口 | 方向 | 说明 | 响应要点 |
|----|------|------|------|---------|
| 26 | `GET /products/pricing/v2022-05-01/price` | 读 | **竞争价格** | 返回 `FeaturedBuyingOptions`（Buy Box 价格 + 其他卖家报价） |
| 27 | `GET /products/pricing/v2022-05-01/competitiveSummary` | 读 | 竞争摘要 | ASIN 维度的竞品价格 |
| 28 | `GET /products/fees/v0/feesEstimate` | 读 | **费用估算** | 预估 Listing 费用（佣金+FBA配送费+仓储费） |

### 3.8 报表域（4 接口 · Reports API v2021-06-30）

> **报表是 Amazon 大数据量同步的核心路径（替代频繁 API 调用）。**

| # | 接口 | 方向 | 说明 | 响应要点 |
|----|------|------|------|---------|
| 29 | `POST /reports/2021-06-30/reports` | 读 | **请求报表** | 传 `reportType` + `marketplaceIds`；返回 `reportId` |
| 30 | `GET /reports/2021-06-30/reports/{reportId}` | 读 | 查询报表状态 | `processingStatus`：CANCELLED / DONE / FATAL / IN_PROGRESS / IN_QUEUE |
| 31 | `GET /reports/2021-06-30/documents/{documentId}` | 读 | **下载报表** | 返回 `url`（报表下载链接，CSV/TXT 格式） |
| 32 | `GET /reports/2021-06-30/schedules` | 读 | 查询报表定时计划 | 返回已配置的定时报表 |

**核心报表类型：**

| reportType | 说明 | AOS 用途 |
|-----------|------|---------|
| `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL` | 全量订单报表 | 订单全量同步 |
| `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL` | 按下单日期订单 | 订单分析 |
| `GET_FBA_FULFILLED_INVENTORY_DATA` | FBA 库存报表 | 库存同步 |
| `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` | 结算报表 | 财务对账 |
| `GET_MERCHANT_LISTINGS_ALL_DATA` | 全量 Listing | 商品同步 |

### 3.9 批量操作域（3 接口 · Feeds API v2021-06-30）

| # | 接口 | 方向 | 说明 | 响应要点 |
|----|------|------|------|---------|
| 33 | `POST /feeds/2021-06-30/feeds` | 写 | **提交批量上传** | 传 `feedType` + 文件 URL；批量更新 Listing/库存/价格 |
| 34 | `GET /feeds/2021-06-30/feeds/{feedId}` | 读 | 查询上传状态 | `processingStatus` |
| 35 | `GET /feeds/2021-06-30/documents/{documentId}` | 读 | 下载上传结果 | 返回处理结果报告 |

### 3.10 通知域（5 接口 · Notifications API v1）

> **通知是 Amazon 推荐的实时事件驱动路径。**

| # | 接口 | 方向 | 说明 | 响应要点 |
|----|------|------|------|---------|
| 36 | `GET /notifications/v1/subscriptions/{notificationType}` | 读 | 查询通知订阅 | 返回已订阅的通知类型 |
| 37 | `POST /notifications/v1/subscriptions/{notificationType}` | 读 | **创建通知订阅** | 订阅事件推送（SQS/SQS队列） |
| 38 | `DELETE /notifications/v1/subscriptions/{notificationType}` | 读 | 取消订阅 | — |
| 39 | `GET /notifications/v1/destinations` | 读 | 查询通知目的地 | SQS 队列 URL |
| 40 | `POST /notifications/v1/destinations` | 读 | 创建通知目的地 | 创建 SQS 队列 |

**核心通知类型：**

| notificationType | 说明 | AOS 用途 |
|-----------------|------|---------|
| `ORDER_CHANGE` | 订单变更 | 增量订单同步 |
| `ORDER_STATUS_CHANGE` | 订单状态变更 | 状态更新 |
| `FEED_PROCESSING_FINISHED` | 批量上传完成 | Feeds 结果通知 |
| `REPORT_PROCESSING_FINISHED` | 报表处理完成 | Reports 下载通知 |
| `FBA_INVENTORY_AVAILABILITY_CHANGES` | FBA 库存变更 | 库存同步 |
| `ANY_OFFER_CHANGED` | Buy Box 价格变更 | 竞争价格监控 |

---

## 4. 认证与签名

### 4.1 双令牌机制

```
1. LWAAuth（Login with Amazon）
   POST https://api.amazon.com/auth/o2/token
   → access_token（有效期 1h）
   → refresh_token

2. STS Token（AWS IAM）
   AssumeRole → 临时 AWS 凭证
   → accessKeyId / secretAccessKey / sessionToken
```

### 4.2 AWS Signature V4

```text
签名步骤：
1. 创建 Canonical Request
2. 创建 String to Sign
3. 计算 HMAC-SHA256 签名
4. 添加 Authorization header：
   AWS4-HMAC-SHA256
   Credential=AKID/20260723/us-east-1/execute-api/aws4_request,
   SignedHeaders=host;x-amz-date,
   Signature=...
```

> **注意：** 每小时 LWAAuth token 过期 → 自动用 refresh_token 获取新 access_token → 重新签名。

---

## 5. 区域端点

| 区域 | 端点 | 覆盖 Marketplace |
|------|------|-----------------|
| **NA**（北美） | `sellingpartnerapi-na.amazon.com` | US / CA / MX / BR |
| **EU**（欧洲） | `sellingpartnerapi-eu.amazon.com` | UK / DE / FR / IT / ES / NL / SE / PL |
| **FE**（远东） | `sellingpartnerapi-fe.amazon.com` | JP / AU / SG |

> **接入策略：** 每个区域需独立认证（LWAAuth + STS），独立 Source 配置。

---

## 6. 与 AOS Source Sync 的对接映射

```
AOS Source Sync 阶段          SP-API                                备注
─────────────────            ──────                                ────
全量拉取（首次）               Reports API (request→poll→download)   ★ 核心路径
                              GET_FLAT_FILE_ALL_ORDERS_DATA         CSV → Parse → Dataset
                              GET_MERCHANT_LISTINGS_ALL_DATA

增量同步（定时）               GET /orders/v0/orders                 按 LastUpdatedAfter 增量
                              (LastUpdatedAfter)

实时同步（推荐）               Notifications (ORDER_CHANGE)          ★ SQS 推送
                              ORDER_CHANGE / REPORT_FINISHED

批量上传（写回）               Feeds API (submit feed)               后置 Action
```

---

## 7. 数据接入推荐策略

| 数据域 | 推荐路径 | 频率 | 说明 |
|--------|---------|------|------|
| 订单 | Reports（全量）+ Notifications（增量） | 全量 1 次 + 实时推送 | 首次用 Reports，日常用通知 |
| 商品 Listing | Reports（全量） | 1 次/天 | 全量同步 |
| FBA 库存 | API（轮询）+ Notifications | 1 h | 库存变更实时感知 |
| 财务 | API（按 OrderId 补查） | 按需 | 订单完成后补查 |
| 价格 | API（竞争价格） | 1 h | Buy Box 监控 |

---

## 8. 风险与注意

| # | 风险 | 说明 | 缓解 |
|----|------|------|------|
| R1 | **LWAAuth 1h 轮换** | access_token 每小时过期 | 自动 refresh_token 刷新 |
| R2 | **AWS4 签名复杂** | 每个请求需 AWS Signature V4 | Connector 内置签名引擎 |
| R3 | 三区域独立 | NA/EU/FE 各需独立认证 | 三套 Source 配置 |
| R4 | SP-API Guard 合规 | 数据保护策略（DPP）审计 | 部署在 AWS 环境内 |
| R5 | 报表处理延迟 | 大报表可能需 10-30 分钟 | 异步等待 + 超时重试 |
| R6 | Rate Limit 复杂 | 各 API 独立限制 + Burst | x-amzn-RateLimit-Limit header 监控 |
| R7 | ASIN 变更 | 商品目录 ASIN 可能合并/拆分 | 定期 Catalog 对账 |
| R8 | 多 Marketplace 汇率 | 不同区域不同币种 | OT 存储时标记 currencyCode |

---

## 9. 与其他电商平台接口对比

| 维度 | 微商城 | 淘宝/天猫 | 拼多多 | 京东 | 抖音 | Shopify | **Amazon** |
|------|--------|----------|--------|------|------|---------|-----------|
| 协议 | HTTP | REST | REST | REST | REST | GraphQL | **REST** |
| 签名 | — | HMAC | MD5 | HMAC | HMAC | Token | **AWS4-HMAC-SHA256** |
| 认证 | DB密码 | OAuth2 | OAuth2 | OAuth2 | OAuth2 | OAuth2 | **LWAAuth+STS** |
| Token有效期 | — | 24h | 24h | 24h | 15天 | 永久 | **1h** |
| 核心接口数 | 341 | 37 | 32 | 42 | 42 | ~25 | **40** |
| 增量机制 | SQL | 无原生 | 有 | 有 | RDS推送 | Webhook | **Reports+Notifications** |
| 区域 | 单站 | 单区 | 单区 | 单区 | 单区 | 全球单店 | **三区域(NA/EU/FE)** |
| 合规严格度 | 低 | 中 | 中 | 中 | 高 | 中 | **最高(DPP)** |
| 复杂度 | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | **⭐⭐⭐⭐⭐** |

---

> **版本**：v1.0 · 2026-07-23 · P1 调研完成
>
> **变更日志**：
>
> | 版本 | 日期 | 说明 |
> | --- | --- | --- |
> | v1.0 | 2026-07-23 | 初版 · 40 核心接口 · 10 域分类 · 双令牌认证 + AWS4 签名 · 5 种 FBA 库存状态 · Reports/Notifications 双路径 · 三区域端点 · 5 核心报表类型 + 6 通知类型 |
