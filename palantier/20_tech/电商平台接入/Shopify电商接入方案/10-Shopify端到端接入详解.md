# Shopify · 端到端接入详解

> **版本**：v1.0 · 2026-07-23
> **参照**：`000-电商平台接入总方案.md` Stage 1-6 框架
> **定位**：Phase 2 跨境平台，验证 **GraphQL Connector** + **Webhook 事件驱动** + **多币种**
> **依赖**：G2（OAuth Token Manager）+ G3（Webhook 监听）+ G4（GraphQL Connector）
> **复杂度**：⭐⭐⭐

---

## Stage 1 · 数据接入（Data Connection）

### 1.1 连接器配置

| 项 | 配置 |
|----|------|
| 连接器类型 | **GraphQL Connector**（AOS 新增类型，区别于 REST） |
| 端点 | `https://{shop}.myshopify.com/admin/api/2026-01/graphql.json` |
| 认证方式 | **OAuth 2.0** → `X-Shopify-Access-Token` header（permanent token） |
| 数据格式 | JSON（GraphQL 原生） |
| 速率限制 | **基于成本**：标准店铺 100 点 budget，每秒恢复 50 点 |
| 版本管理 | 季度版本（2026-01 / 2026-04 / 2026-07），回退支持 12 个月 |
| GID 命名 | `gid://shopify/{ObjectType}/{id}` |
| **Webhook** | 事件驱动（`orders/create` 等 60+ 事件），**推荐替代轮询** |
| **Bulk Op** | `bulkOperationRunQuery`，支持大数据量批量导出 |

### 1.2 GraphQL 与 REST 的根本差异

```
REST（淘宝/拼多多/京东）：
  GET /orders?page=1&status=paid → 返回固定字段集
  需要 N 次 API 调用获取关联数据

GraphQL（Shopify）：
  POST /graphql.json
  query {
    orders(first: 50, query: "financial_status:paid") {
      edges {
        node {
          id
          name
          totalPriceSet { shopMoney { amount currencyCode } }
          customer { id email displayName }
          lineItems(first: 10) {
            edges {
              node { title quantity variant { sku price } }
            }
          }
          fulfillments { trackingInfo { number url } }
        }
      }
    }
  }
  → 一次查询获取订单+客户+商品+物流（嵌套关联）
```

### 1.3 速率限制：成本模型

```json
// 每个 GraphQL 响应包含成本信息
{
  "extensions": {
    "cost": {
      "requestedQueryCost": 52,    // 本次查询消耗
      "actualQueryCost": 48,
      "throttleStatus": {
        "maximumAvailable": 1000.0,  // 最大余额
        "currentlyAvailable": 952,   // 当前可用
        "restoreRate": 50.0          // 每秒恢复
      }
    }
  }
}
```

AOS Connector 策略：监控 `currentlyAvailable`，低于阈值时自动降速。

### 1.4 Webhook 事件驱动

| 事件 | 触发 | AOS 动作 |
|------|------|----------|
| `orders/create` | 新订单创建 | 立即同步到 Order Dataset |
| `orders/updated` | 订单更新 | 增量更新 |
| `orders/paid` | 订单支付 | 触发态势更新 |
| `orders/cancelled` | 订单取消 | 状态更新 |
| `products/create` | 新商品 | 同步 Product Dataset |
| `products/update` | 商品更新 | 更新库存/价格 |
| `customers/create` | 新客户 | 同步 Customer Dataset |
| `fulfillments/create` | 发货创建 | 更新物流状态 |
| `refunds/create` | 退款创建 | 同步 AfterSales |

**AOS Webhook 监听服务（G3）**：监听 Webhook 回调 → 实时推送到 Dataset，**无需轮询**。

### 1.5 Source 创建

```
Step 1 · 选择类型：GraphQL（Shopify 模板）
Step 2 · 连接方式：直连 + Webhook 回调
Step 3 · 命名：prod-graphql-shopify-{shop-name}
Step 4 · 配置：
  Shop URL: https://{shop}.myshopify.com
  Access Token: ****（OAuth permanent token）
  API Version: 2026-01
  Webhook Endpoint: https://aos.example.com/webhooks/shopify
  Webhook Secret: ****（HMAC 验签）
```

### 1.6 探索源（GraphQL Schema）

| GraphQL Object | 对应 8 域 | 关键字段 |
|----------------|----------|---------|
| `Shop` | 店铺 | name, currencyCode, plan, timezone |
| `Product` → `ProductVariant` | 商品 | id, title, status, variants{sku, price, inventoryQuantity} |
| `Order` | 订单 | id, name, financialStatus, fulfillmentStatus, lineItems, totalPriceSet |
| `Customer` | 会员 | id, email, displayName, numberOfOrders |
| `InventoryItem` / `InventoryLevel` | 库存 | location-based: available |
| `Fulfillment` / `FulfillmentOrder` | 履约 | status, trackingInfo, location |
| `Transaction` | 支付 | gateway, amount, currency, status |
| `DiscountCode` / `PriceRule` | 折扣 | code, usageCount, value |

---

## Stage 2 · 数据同步（Sync）

### 2.1 同步策略（Webhook 优先 + GraphQL 轮询补全）

| 数据域 | 获取方式 | 事务类型 | 调度 | 说明 |
|--------|----------|----------|------|------|
| **订单** | **Webhook** `orders/create` + `orders/updated` | **实时** | **实时推送** | 无需轮询 |
| 商品 | GraphQL 查询 + Webhook `products/*` | SNAPSHOT | 每 6 小时全量 | Webhook 做增量 |
| 会员 | GraphQL 查询 + Webhook `customers/create` | APPEND | 每 1 小时 | |
| 库存 | GraphQL `inventoryLevels` | SNAPSHOT | 每 30 分钟 | Location 维度 |
| 履约 | Webhook `fulfillments/create` | 实时 | 实时推送 | |
| 退款 | Webhook `refunds/create` | 实时 | 实时推送 | |

### 2.2 Bulk Operations（大数据量导出）

```graphql
mutation {
  bulkOperationRunQuery(
    query: """
    {
      products {
        edges {
          node {
            id title status
            variants { edges { node { sku price inventoryQuantity } } }
          }
        }
      }
    }
    """
  ) {
    bulkOperation { id status }
    userErrors { field message }
  }
}
```

→ 异步执行 → 返回 JSONL 文件 URL → AOS 下载解析

---

## Stage 3 · 管道清洗（Pipeline Builder）

### 3.1 多币种处理（Shopify 独有挑战）

```sql
-- Shopify 订单金额有两个币种维度
Expression:
  totalPriceSet.shopMoney.amount AS amount_shop_currency   -- 店铺本币种（如 USD）
  totalPriceSet.presentmentMoney.amount AS amount_customer  -- 客户结算币种（如 EUR）
  totalPriceSet.presentmentMoney.currencyCode AS customer_currency

-- 汇率标记
Expression:
  CASE WHEN customer_currency != shop_currency 
       THEN 'multi_currency' 
       ELSE 'single_currency' 
  END AS currency_flag
```

### 3.2 GraphQL 嵌套数据展平（Explode 组件）

```sql
-- GraphQL 返回的嵌套 JSON 需要展平
Explode: order.lineItems.edges
  一个订单（含 N 个 line item）展开为 N 行
  每行: order_id, order_name, line_title, line_quantity, line_sku, line_price

Explode: order.fulfillments
  一个订单（含 M 个包裹）展开为 M 行
  每行: order_id, tracking_number, tracking_url, carrier
```

### 3.3 GID 解析

```sql
-- Shopify GID 格式：gid://shopify/Product/1321540321336
Expression:
  REGEXP_EXTRACT(id, 'gid://shopify/(\\w+)/(\\d+)') AS object_type, object_id
  -- 'Product', '1321540321336'
```

---

## Stage 4 · OKF 映射（Funnel）

### 4.1 OT 映射表

| Shopify Object | 统一 OT | 主键 | 关键映射 |
|----------------|---------|------|----------|
| `Order` | **Order** | GID | name→order_no, financialStatus→pay_status, fulfillmentStatus→ship_status |
| `Order.LineItem` | **OrderLine** | GID | quantity, variant{sku}→variant_id |
| `Product` | **Product** | GID | title→name, status→status |
| `ProductVariant` | **ProductVariant** | GID | sku, price, inventoryQuantity→stock |
| `Customer` | **Customer** | GID | email, displayName→name |
| `Fulfillment` | **Shipment** | GID | trackingInfo.number→tracking_no |
| `Transaction` | **Payment** | GID | gateway→method, amount |
| `InventoryLevel` | **Inventory** | GID+locationId | available→stock, location→warehouse |
| `DiscountCode` | **Coupon** | GID | code→coupon_code, usageCount→used_count |
| `Location` | **Store** | GID | name→warehouse_name |

### 4.2 Funnel 状态机

```
财务状态：pending → authorized → paid → partially_paid → refunded → voided
履约状态：unfulfilled → partial → fulfilled → restocked
```

---

## Stage 5 · 本体实例化（Ontology）

### 5.1 Shopify 特有扩展

| OT | 说明 | 特有字段 |
|----|------|----------|
| **Location**（新） | 仓库/门店 | **Shopify 独有**：multi-Location 库存，每个 Location 有独立库存量 |
| **Transaction** | 支付交易 | gateway, currency, status |
| **PriceRule** | 价格规则 | 分层折扣规则 |

### 5.2 特有 Link

| Link | from → to | 基数 | 说明 |
|------|-----------|------|------|
| `stockedAt` | ProductVariant → Location | N:M | **多仓库存**（同一 SKU 在不同仓库有不同库存） |
| `fulfilledFrom` | Order → Location | N:1 | 订单从哪个仓库发货 |
| `paidVia` | Order → Transaction | 1:N | 一笔订单可能有多次交易（部分付款） |

---

## Stage 6 · 上层消费

### 6.1 Shopify 特色场景

| 场景 | 说明 |
|------|------|
| **多仓库存看板** | 各 Location 的库存量、调拨建议 |
| **多币种收入** | 按客户结算币种分组的收入看板 |
| **Webhook 事件流** | 实时事件大屏（订单/商品/退款事件流） |
| **Bulk Op 状态** | 大数据量导出任务状态监控 |
| **折扣 ROI** | PriceRule → 订单归因 → ROI 分析 |

### 6.2 平台缺口

| 缺口 ID | 描述 | 优先级 |
|---------|------|--------|
| **G2** | OAuth Token Manager | P0 |
| **G3** | Webhook 监听服务 | **P0（实时性核心依赖）** |
| **G4** | GraphQL Connector | **P0（唯一 API 方式）** |
| G-SH-01 | 多币种汇率转换管道 | P1 |
| G-SH-02 | Bulk Operation 异步任务管理 | P2 |
