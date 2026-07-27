# 01 · Shopify GraphQL Admin API Schema 探索

> **版本**：v1.0 · 2026-07-23
> **状态**：P1 调研完成 · GraphQL Query/Mutation 分类清单 + Webhook 事件清单
> **来源**：Shopify Admin GraphQL API 文档（2026-01 版本）+ 多源交叉验证
> **关联**：[00-总体分析计划](./00-Shopify-AOS对接方案.md)

---

## 1. API 版本与端点

| 维度 | 内容 |
|------|------|
| 当前版本 | `2026-01`（季度发布，12 个月回退支持） |
| 端点 | `https://{shop}.myshopify.com/admin/api/2026-01/graphql.json` |
| 认证 | `X-Shopify-Access-Token` header（OAuth 2.0 permanent token） |
| 请求方式 | POST，Content-Type: application/json |
| GID 格式 | `gid://shopify/{ObjectType}/{id}` |

### 速率限制（基于成本）

```
标准店铺：100 点 budget，每秒恢复 50 点
查询成本 = 1 + 字段数 × 0.25（近似）
响应含 extensions.cost：
{
  "extensions": {
    "cost": {
      "requestedQueryCost": 12,
      "actualQueryCost": 10,
      "throttleStatus": {
        "maximumAvailable": 1000,
        "currentlyAvailable": 990,
        "restoreRate": 50
      }
    }
  }
}
```

---

## 2. Query 分类清单（按域）

### 2.1 商品域

| # | Query | 关键字段 | 分页 | 说明 |
|----|-------|---------|------|------|
| 1 | `products(first:N, after:$cursor)` | `id` `title` `status` `vendor` `productType` `tags` `variants{...}` `images{...}` | Relay cursor | 商品列表（SPU） |
| 2 | `product(id:$gid)` | 全量字段 + `metafields` + `options` | — | 单商品详情 |
| 3 | `productVariants(first:N)` | `id` `sku` `price` `compareAtPrice` `inventoryQuantity` `selectedOptions` | Relay cursor | SKU 列表 |
| 4 | `collections(first:N)` | `id` `title` `handle` `productsCount` `rule` `sortOrder` | Relay cursor | 商品合集（手动/智能） |
| 5 | `productTags` | `tags[]` | — | 商品标签列表 |

### 2.2 订单域

| # | Query | 关键字段 | 分页 | 说明 |
|----|-------|---------|------|------|
| 6 | `orders(first:N, query:$filter)` | `id` `name` `financialStatus` `fulfillmentStatus` `displayFinancialStatus` `displayFulfillmentStatus` `lineItems{...}` `totalPriceSet` `shippingAddress` `customer` | Relay cursor | 订单列表（核心） |
| 7 | `order(id:$gid)` | 全量字段 + `transactions` + `shippingLines` + `discountApplications` + `metafields` | — | 单订单详情 |
| 8 | `orders(first:N, query:"updated_at:>2026-07-01")` | 同 #6 | Relay cursor | **增量查询**（按更新时间过滤） |
| 9 | `draftOrders(first:N)` | `id` `name` `status` `lineItems` `totalPrice` | Relay cursor | 草稿订单（客服创建） |

### 2.3 会员域

| # | Query | 关键字段 | 分页 | 说明 |
|----|-------|---------|------|------|
| 10 | `customers(first:N, query:$filter)` | `id` `email` `firstName` `lastName` `phone` `numberOfOrders` `totalSpent` `addresses{...}` `tags` | Relay cursor | 会员列表 |
| 11 | `customer(id:$gid)` | 全量 + `orders(first:5)` `metafields` | — | 单会员详情 |

### 2.4 库存域

| # | Query | 关键字段 | 分页 | 说明 |
|----|-------|---------|------|------|
| 12 | `inventoryItems(first:N)` | `id` `sku` `tracked` `unitCost` `inventoryLevel(locationId:$gid){available}` | Relay cursor | 库存条目 |
| 13 | `locations(first:N)` | `id` `name` `address` `isActive` `fulfillsOnlineOrders` | Relay cursor | 仓库/门店列表 |
| 14 | `inventoryLevels(first:N, inventoryItemId:$gid)` | `available` `location{name}` | — | 按商品查分仓库存 |

### 2.5 履约域

| # | Query | 关键字段 | 分页 | 说明 |
|----|-------|---------|------|------|
| 15 | `fulfillmentOrders(first:N)` | `id` `status` `assignedLocation` `lineItems{...}` `deliveryMethod` | Relay cursor | 履约订单 |
| 16 | `fulfillments(first:N, orderId:$gid)` | `id` `status` `trackingInfo` `createdAt` | — | 物流履单 |

### 2.6 店铺/配置域

| # | Query | 关键字段 | 说明 |
|----|-------|---------|------|
| 17 | `shop` | `id` `name` `currencyCode` `plan{displayName}` `timezoneAbbreviation` `primaryDomain{url}` | 店铺信息（一次性） |
| 18 | `metafields(namespace:$ns, ownerType:$type)` | `id` `namespace` `key` `value` `type` | 自定义属性 |

---

## 3. Mutation 分类清单（写回操作 · 后置）

| # | Mutation | 说明 | AOS Action 场景 |
|----|---------|------|-----------------|
| M1 | `productCreate` / `productUpdate` | 创建/更新商品 | 商品管理 |
| M2 | `productVariantCreate` / `productVariantUpdate` | 创建/更新 SKU | 库存/价格管理 |
| M3 | `inventoryAdjust` / `inventorySetQuantities` | 调整库存 | 库存同步 |
| M4 | `orderClose` / `orderCancel` | 关闭/取消订单 | 订单运营 |
| M5 | `fulfillmentCreateV2` | 创建发货 | 发货操作 |
| M6 | `customerCreate` / `customerUpdate` | 创建/更新会员 | 会员管理 |
| M7 | `draftOrderComplete` | 草稿订单转正式 | 客服场景 |

---

## 4. Webhook 事件清单

> **Webhook 是 Shopify 数据实时同步的核心路径（替代轮询）。**

### 4.1 核心 Webhook 事件

| # | 事件 Topic | 触发时机 | AOS 处理 |
|----|-----------|---------|---------|
| W1 | `orders/create` | 新订单创建 | 增量同步 → Order OT |
| W2 | `orders/updated` | 订单变更（状态/地址/物流） | 增量更新 Order OT |
| W3 | `orders/cancelled` | 订单取消 | Order 状态变更 |
| W4 | `orders/fulfilled` | 订单完成发货 | Order 状态 → fulfilled |
| W5 | `orders/paid` | 订单付款 | Order.payment 更新 |
| W6 | `products/create` | 新商品创建 | 增量同步 → Product OT |
| W7 | `products/update` | 商品变更 | 更新 Product OT |
| W8 | `products/delete` | 商品删除 | 标记 Product 删除 |
| W9 | `inventory_levels/update` | 库存变更 | 更新 InventoryLevel OT |
| W10 | `customers/create` | 新会员注册 | 增量同步 → Customer OT |
| W11 | `customers/update` | 会员信息变更 | 更新 Customer OT |
| W12 | `fulfillments/create` | 新发货创建 | 创建 Fulfillment OT |
| W13 | `refunds/create` | 退款创建 | 创建 Refund 记录 |

### 4.2 Webhook 验证

```
每个 Webhook POST 包含 header：
  X-Shopify-Topic: orders/create
  X-Shopify-Hmac-Sha256: <HMAC签名>
  X-Shopify-Shop-Domain: <shop>.myshopify.com
  X-Shopify-API-Version: 2026-01

验证：
  HMAC-SHA256(webhook_body, client_secret) == X-Shopify-Hmac-Sha256
```

### 4.3 Webhook 接入架构

```text
Shopify Store
  │
  │  HTTPS POST（Webhook 事件）
  ▼
AOS Webhook Receiver（需新建 · 公网可达端点）
  │
  ├── HMAC 验证（防伪造）
  ├── 去重处理（X-Shopify-Webhook-Id）
  ├── 写入 Ingestion Queue
  │
  ▼
Ingestion Pipeline → Dataset（增量）→ OKF → Object/Link
```

---

## 5. Bulk Operations（大数据量导出）

> 对于万级以上商品/订单的首次全量同步，推荐使用 Bulk Operations。

```graphql
mutation {
  bulkOperationRunQuery(
    query: """
    {
      products {
        edges {
          node {
            id title status variants { edges { node { id sku price inventoryQuantity } } }
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

**流程：**

```text
1. 发起 bulkOperationRunQuery → 返回 bulkOperation.id
2. 轮询 bulkOperation(id:) 状态 → COMPLETED
3. 下载结果 JSONL 文件（在 url 字段）
4. 解析 JSONL → Dataset
```

| 优势 | 说明 |
|------|------|
| 不受 Rate Limit 影响 | Bulk 查询在后台执行 |
| 支持大数据量 | 万级订单一次性导出 |
| JSONL 格式 | 行分隔 JSON，易解析 |
| 成本低 | 消耗极少的 API cost |

---

## 6. 多币种字段处理

> **Shopify 的每个金额字段都是 MoneyBag 结构。**

```json
{
  "totalPriceSet": {
    "shopMoney": { "amount": "99.00", "currencyCode": "USD" },
    "presentmentMoney": { "amount": "720.00", "currencyCode": "CNY" }
  }
}
```

| 字段 | 含义 | 用途 |
|------|------|------|
| `shopMoney` | 店铺基础币种（结算用） | 商家结算金额 |
| `presentmentMoney` | 消费者展示币种（支付用） | 消费者实付金额 |

> **AOS OT Prop 设计：** 金额 Prop 支持 `MoneyBag` 类型，存储 `{amount, currencyCode}` 对象。

---

## 7. GID 格式说明

所有 Shopify 资源使用 GID（Global ID）格式：

```text
gid://shopify/Product/1321540321336      → 商品
gid://shopify/ProductVariant/39588734156  → SKU
gid://shopify/Order/4507894630            → 订单
gid://shopify/Customer/553459803          → 会员
gid://shopify/Collection/841564295        → 合集
gid://shopify/Location/48753489           → 仓库
gid://shopify/InventoryItem/457924678     → 库存条目
gid://shopify/Metafield/1077823424        → 自定义字段
```

> **AOS OT 主键统一使用 string 存储 GID。** OKF 映射时直接透传 GID。

---

## 8. 与 AOS Source Sync 的对接映射

```
AOS Source Sync 阶段          Shopify GraphQL                        备注
─────────────────            ────────────────                       ────
全量拉取（首次）               bulkOperationRunQuery                 万级数据一次性导出
                              products / orders / customers

增量同步（实时）               Webhook 事件推送                      ★ 核心路径（免轮询）
                              orders/create, products/update ...

增量同步（定时）               orders(query:"updated_at:>$last")     按 update_time 增量
                              customers(query:"updated_at:>$last")

实时查询（不落 Dataset）       fulfillment → trackingInfo            物流追踪
                              order(id:$gid)                        On-Demand

配置参考（一次性）             shop                                  店铺信息
                              locations                             仓库列表
```

---

## 9. 风险与注意

| # | 风险 | 说明 | 缓解 |
|----|------|------|------|
| R1 | Rate Limit（cost-based） | GraphQL 按成本限流，复杂查询易超限 | 监控 `extensions.cost` + 退避 |
| R2 | Webhook 可靠性 | 网络问题导致 Webhook 丢失 | 定期全量对账 + 去重 |
| R3 | 版本迁移 | 季度版本，12 个月后旧版下线 | 监控版本 + 提前迁移 |
| R4 | 多 Location 复杂性 | 多仓库存追踪复杂 | 先单仓 → 后多仓 |
| R5 | Metafield 无限扩展 | 商家可自定义任意 Metafield | 按 namespace 过滤 + 白名单 |
| R6 | permanent token 安全 | Access Token 不过期 | 安全存储 + 权限最小化 |

---

## 10. 与其他电商平台 API 风格对比

| 维度 | 国内电商 | **Shopify** | Amazon |
|------|---------|-----------|--------|
| API 风格 | REST | **GraphQL** | REST |
| 端点数 | 多端点 | **单端点** | 多端点 |
| 数据获取 | 轮询 | **Webhook + 按需** | Reports + Notifications |
| 限流模型 | QPS | **Cost-based** | 各 API 独立 |
| 大数据量 | 分页 | **Bulk Operations** | Reports |
| 金额 | 单币种 | **MoneyBag 双币种** | 多币种 |
| 自定义字段 | 无/弱 | **Metafields** | 无 |

---

> **版本**：v1.0 · 2026-07-23 · GraphQL Schema 探索文档
>
> **变更日志**：
>
> | 版本 | 日期 | 说明 |
> | --- | --- | --- |
> | v1.0 | 2026-07-23 | 初版 · 18 Query + 7 Mutation + 13 Webhook 事件 · Bulk Operations · MoneyBag 多币种 · GID 格式 · Webhook 验证 |
