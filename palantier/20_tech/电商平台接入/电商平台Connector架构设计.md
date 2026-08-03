# 电商平台 Connector 架构设计

> **版本**：v1.0 · 2026-07-23
> **位置**：`电商平台Connector架构设计.md`
> **定位**：基于现有 Connector 插件化框架（[97](../97-Connector插件化整改方案.md) / [100](../100-Connector运行时插件分发方案.md)），扩展设计 REST / GraphQL / Webhook / OAuth 四种新 Connector 类型
> **解决阻塞**：G1 REST Connector · G2 OAuth Manager · G3-G5 签名插件 · G6 GraphQL · G7 Webhook · G8 解密 · G9 计费

---

## 1. 现状与目标

### 1.1 当前 Connector 能力

| 类型 | 状态 | 示例 |
|------|------|------|
| **JDBC** | ✅ 已实现 | mysql / postgres / sqlserver |
| **File** | ✅ 已实现 | file-local / file-s3 |
| **REST** | ❌ 缺失（G1） | 淘宝/拼多多/京东/抖音/Amazon |
| **GraphQL** | ❌ 缺失（G6） | Shopify |
| **Webhook** | ❌ 缺失（G7） | Shopify 事件接收 |

### 1.2 目标

设计一套可扩展的 Connector 插件架构，使每个电商平台的接入只需 **配置**（映射表 + 签名方案 + 认证方案），无需改代码。

---

## 2. 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    AOS Platform                             │
│                                                             │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐     │
│  │  Pipeline   │   │  Funnel      │   │  Workshop    │     │
│  │  Builder    │──→│  Mapping     │   │  Dashboard   │     │
│  └──────┬──────┘   └──────┬───────┘   └──────────────┘     │
│         │                 │                                  │
│  ┌──────▼─────────────────▼──────┐                          │
│  │     Connector Registry        │                          │
│  │     (插件注册表)               │                          │
│  └──────┬────────────────────────┘                          │
│         │                                                   │
│    ┌────┼────┬────────┬────────┬────────┐                  │
│    ▼    ▼    ▼        ▼        ▼        ▼                  │
│  ┌───┐┌───┐┌──────┐┌──────┐┌──────┐┌──────┐               │
│  │JDBC││File││ REST ││GraphQL││Webhook││OAuth │               │
│  │   ││   ││      ││      ││      ││Mgr  │               │
│  └───┘└───┘└──┬───┘└──┬───┘└──┬───┘└──────┘               │
│               │       │       │                              │
│         ┌─────┴──┐    │       │                              │
│         ▼        ▼    ▼       ▼                              │
│  ┌──────────────────────────────────────┐                   │
│  │       签名插件 (G3/G4/G5)             │                   │
│  │  HMAC-SHA256 / MD5 / AWS4             │                   │
│  └──────────────────────────────────────┘                   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              电商平台 Connector 实例                  │   │
│  │                                                      │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │   │
│  │  │ 微商城  │ │ 淘宝   │ │ 拼多多  │ │ 京东   │       │   │
│  │  │ JDBC   │ │ REST   │ │ REST   │ │ REST   │       │   │
│  │  │ MySQL  │ │ HMAC   │ │ MD5    │ │ HMAC   │       │   │
│  │  └────────┘ └────────┘ └────────┘ └────────┘       │   │
│  │                                                      │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐                   │   │
│  │  │ 抖音   │ │ Shopify│ │ Amazon │                   │   │
│  │  │ REST   │ │GraphQL │ │ REST   │                   │   │
│  │  │ HMAC   │ │+Webhook│ │ AWS4   │                   │   │
│  │  │+解密   │ │        │ │        │                   │   │
│  │  └────────┘ └────────┘ └────────┘                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. REST API Connector（G1）

### 3.1 设计目标

| 目标 | 说明 |
|------|------|
| 通用 HTTP 请求 | 支持 GET/POST/PUT/DELETE |
| 分页自动化 | 支持 page/offset/cursor 三种分页模式 |
| 限流控制 | 内置 rate limiter（QPS 可配） |
| 重试机制 | 指数退避，可配最大重试次数 |
| 签名插拔 | 签名逻辑委托给 SignaturePlugin |

### 3.2 REST Connector 配置 Schema

```json
{
  "connectorType": "rest",
  "pluginId": "taobao-top",
  "displayName": "淘宝 TOP API",
  "baseUrl": "https://eco.taobao.com/router/rest",
  "auth": {
    "type": "oauth2",
    "tokenManager": "default",
    "appKey": "${TAOBAO_APP_KEY}",
    "appSecret": "${TAOBAO_APP_SECRET}",
    "tokenEndpoint": "https://oauth.taobao.com/token",
    "refreshEndpoint": "https://oauth.taobao.com/refreshToken"
  },
  "signature": {
    "plugin": "hmac-sha256",
    "params": {
      "algorithm": "HMAC-SHA256",
      "encoding": "hex",
      "signFields": ["method", "timestamp", "format", "app_key", "v", "sign_method"]
    }
  },
  "rateLimit": {
    "qps": 40,
    "burst": 50
  },
  "retry": {
    "maxAttempts": 3,
    "backoff": "exponential",
    "initialDelayMs": 1000,
    "retryableStatusCodes": [429, 500, 502, 503]
  },
  "pagination": {
    "mode": "page",
    "pageParam": "page_no",
    "pageSizeParam": "page_size",
    "defaultPageSize": 40,
    "maxPageSize": 100,
    "hasMoreField": "has_next"
  },
  "endpoints": {
    "Order.list": {
      "method": "POST",
      "action": "taobao.trades.sold.get",
      "params": { "fields": "tid,status,payment,created,buyer_nick,receiver_name,receiver_mobile,receiver_state,receiver_city,receiver_district,receiver_address" },
      "responsePath": "trades_sold_get_response.trades.trade",
      "mapping": "platform_mapping/taobao_order.json"
    },
    "Order.get": {
      "method": "POST",
      "action": "taobao.trade.fullinfo.get",
      "params": { "fields": "tid,oid,status,payment,orders,type,shipping_type,receiver_name" },
      "responsePath": "trade_fullinfo_get_response.trade",
      "mapping": "platform_mapping/taobao_order_detail.json"
    }
  }
}
```

### 3.3 分页策略适配

| 模式 | 适用平台 | 参数 |
|------|---------|------|
| **page** | 淘宝 / 拼多多 / 京东 | `page_no` + `page_size` |
| **offset** | Amazon SP-API | `NextToken` (cursor) |
| **cursor** | 抖音 / Shopify GraphQL | `cursor` + `has_more` |
| **none** | 微商城（JDBC LIMIT） | — |

### 3.4 各 REST 平台签名配置

| 平台 | 签名插件 | 签名方式 | 关键参数 |
|------|---------|---------|---------|
| 淘宝 | `hmac-sha256` | HMAC-SHA256 | sign_fields + app_secret |
| 拼多多 | `md5` | MD5(params_sorted + secret) | sort + uppercase |
| 京东 | `hmac-sha256` | HMAC-SHA256-MD5 混合 | md5 后再 hmac |
| 抖音 | `hmac-sha256` | HMAC-SHA256 | app_secret + method+timestamp+param |
| Amazon | `aws4` | AWS4-HMAC-SHA256 | region + service + amz_date |

---

## 4. OAuth 2.0 Token Manager（G2）

### 4.1 设计目标

| 目标 | 说明 |
|------|------|
| 统一令牌存储 | 所有平台 Token 集中加密存储（AES-256） |
| 自动刷新 | Token 过期前 5 分钟自动刷新 |
| 租户隔离 | 每个组织/工作区独立 Token 池 |
| 多类型支持 | Authorization Code / Client Credentials / Refresh Token |
| 审计日志 | 所有 Token 获取/刷新/失效记录可审计 |

### 4.2 Token Manager 架构

```text
┌──────────────────────────────────────────────┐
│           OAuth Token Manager                │
│                                              │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │ Token Store │  │  Refresh Scheduler   │  │
│  │ (AES-256)   │  │  (Cron 每5min扫描)    │  │
│  └──────┬──────┘  └──────────┬───────────┘  │
│         │                     │              │
│  ┌──────▼─────────────────────▼──────────┐  │
│  │        Provider Adapters              │  │
│  │                                       │  │
│  │  ┌────────┐ ┌────────┐ ┌───────────┐ │  │
│  │  │ 淘宝   │ │ 拼多多  │ │ 京东      │ │  │
│  │  │ OAuth2 │ │ OAuth2 │ │ OAuth2    │ │  │
│  │  └────────┘ └────────┘ └───────────┘ │  │
│  │  ┌────────┐ ┌────────┐ ┌───────────┐ │  │
│  │  │ 抖音   │ │ Shopify│ │ Amazon    │ │  │
│  │  │ OAuth2 │ │ OAuth2 │ │ LWAAuth   │ │  │
│  │  └────────┘ └────────┘ └───────────┘ │  │
│  └───────────────────────────────────────┘  │
│                                              │
│  ┌──────────────────────────────────────┐  │
│  │  API: /v1/oauth/tokens               │  │
│  │                                       │  │
│  │  POST   /tokens          创建/授权    │  │
│  │  GET    /tokens/{id}     查询状态     │  │
│  │  POST   /tokens/{id}/refresh  刷新    │  │
│  │  DELETE /tokens/{id}     吊销         │  │
│  └──────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

### 4.3 Token 生命周期

| 平台 | 授权方式 | Access Token 有效期 | Refresh Token 有效期 | 刷新策略 |
|------|---------|-------|---------|---------|
| 淘宝 | Authorization Code | 24h | 365天 | 过期前5min自动刷新 |
| 拼多多 | Authorization Code | 24h | 30天 | 过期前5min自动刷新 |
| 京东 | Authorization Code | 24h | 30天 | 过期前5min自动刷新 |
| 抖音 | Authorization Code | **15天** | 30天 | 过期前1天自动刷新 |
| Shopify | Authorization Code | **永久** | 不需刷新 | 仅在卸载App时失效 |
| Amazon | Authorization Code (LWA) | **1h** | 永久 | 过期前5min自动刷新 |

### 4.4 Token 存储结构

```json
{
  "tokenId": "tok_taobao_org1_proj1",
  "orgId": "org-001",
  "projectId": "proj-001",
  "platform": "taobao",
  "accessToken": "AES256(xxxxxx)",
  "refreshToken": "AES256(yyyyyy)",
  "expiresAt": "2026-07-24T10:00:00Z",
  "refreshExpiresAt": "2027-07-23T10:00:00Z",
  "scope": ["trade", "item", "logistics"],
  "shopName": "栖月汇旗舰店",
  "shopId": "shop_12345",
  "status": "active",
  "lastRefreshedAt": "2026-07-23T09:55:00Z",
  "createdAt": "2026-07-23T10:00:00Z"
}
```

---

## 5. GraphQL Connector（G6）

### 5.1 设计目标

Shopify 是唯一使用 GraphQL 的平台。GraphQL Connector 需要：
- 动态构造 GraphQL query/mutation
- 处理 `cursor` 分页（Connections 模式）
- 处理 `cost` / `throttleStatus` 限流（Shopify 点数系统）
- 支持 Bulk Operation（大数据量异步导出）

### 5.2 Shopify GraphQL Connector 配置

```json
{
  "connectorType": "graphql",
  "pluginId": "shopify-admin",
  "baseUrl": "https://{shop}.myshopify.com/admin/api/2024-07/graphql.json",
  "auth": {
    "type": "bearer",
    "tokenManager": "default",
    "header": "X-Shopify-Access-Token"
  },
  "rateLimit": {
    "type": "cost",
    "bucketSize": 1000,
    "leakRate": 50,
    "queryCostField": "extensions.cost.throttleStatus"
  },
  "queries": {
    "Order.list": {
      "query": "query orders($first: Int!, $after: String) { orders(first: $first, after: $after) { edges { node { id name createdAt totalPrice displayFinancialStatus customer { id displayName } lineItems(first: 50) { edges { node { id quantity title variant { id sku price } } } } } } pageInfo { hasNextPage endCursor } } }",
      "pagination": "cursor",
      "pageSize": 250,
      "responsePath": "data.orders.edges",
      "mapping": "platform_mapping/shopify_order.json"
    },
    "Product.list": {
      "query": "query products($first: Int!, $after: String) { products(first: $first, after: $after) { edges { node { id title status vendor variants(first: 100) { edges { node { id sku price compareAtPrice inventoryQuantity } } } } } pageInfo { hasNextPage endCursor } } }",
      "pagination": "cursor",
      "pageSize": 250,
      "responsePath": "data.products.edges",
      "mapping": "platform_mapping/shopify_product.json"
    }
  }
}
```

---

## 6. Webhook Receiver（G7）

### 6.1 设计目标

| 目标 | 说明 |
|------|------|
| 端点注册 | 每个平台 Connector 可注册自定义 Webhook 端点 |
| 签名验证 | HMAC 验签（Shopify 使用 `X-Shopify-Hmac-SHA256`） |
| 事件分发 | 接收的 Webhook 事件分发到 Pipeline / Function |
| 幂等处理 | 基于 event_id 去重 |
| 重试 | 事件处理失败自动重入队列 |

### 6.2 Shopify Webhook 事件

```json
{
  "webhookConfig": {
    "endpoint": "/v1/webhooks/shopify",
    "signatureHeader": "X-Shopify-Hmac-SHA256",
    "signatureSecret": "${SHOPIFY_WEBHOOK_SECRET}",
    "events": {
      "orders/create": { "pipeline": "shopify-order-ingest", "mapping": "shopify_order" },
      "orders/updated": { "pipeline": "shopify-order-update", "mapping": "shopify_order" },
      "orders/cancelled": { "pipeline": "shopify-order-cancel", "mapping": "shopify_order" },
      "orders/fulfilled": { "pipeline": "shopify-fulfillment", "mapping": "shopify_fulfillment" },
      "products/create": { "pipeline": "shopify-product-create", "mapping": "shopify_product" },
      "products/update": { "pipeline": "shopify-product-update", "mapping": "shopify_product" },
      "inventory_levels/update": { "pipeline": "shopify-inventory", "mapping": "shopify_inventory" }
    }
  }
}
```

---

## 7. 抖音解密插件（G8）

### 7.1 问题

抖音电商订单的收货人姓名、手机、地址均为**全加密**密文，需通过抖店云 Agent 代理解密。

### 7.2 解密架构

```text
┌──────────────┐      加密订单数据       ┌──────────────┐
│  AOS Hub     │ ──────────────────────→ │  抖店云      │
│  Connector   │                         │  Cloud Agent │
│              │ ←────────────────────── │              │
│              │      解密明文           │  解密引擎     │
└──────────────┘                         └──────────────┘
```

| 配置项 | 说明 |
|--------|------|
| `decryptMode` | `cloud_agent`（推荐）/ `local_api`（需申请资质） |
| `cloudAgentUrl` | 抖店云内网地址 |
| `decryptFields` | `["buyer_name", "buyer_mobile", "shipping_address"]` |
| `fallbackPolicy` | `skip`（跳过）/ `store_encrypted`（存储密文待后续解密） |

### 7.3 解密 Pipeline

```text
1. Connector 拉取加密订单 → 存储 encrypted_order
2. 发送解密请求 → 抖店云 Cloud Agent
3. Cloud Agent 调用抖音解密 API → 返回明文
4. 明文写入 Order OT（仅 buyer_name / buyer_mobile / shipping_address）
5. 原始密文记录在 audit_log（审计需要）
```

---

## 8. 接口计费控制器（G9）

### 8.1 抖音接口收费

抖音部分 API 按调用量收费（如 `trade.list` 超过免费额度后 0.001 元/次）。

### 8.2 计费控制设计

```json
{
  "billingConfig": {
    "platform": "douyin",
    "freeQuota": {
      "daily": 10000,
      "monthly": 300000
    },
    "pricing": {
      "trade.list": { "pricePerCall": 0.001, "freeDaily": 500 },
      "trade.detail": { "pricePerCall": 0.0005, "freeDaily": 2000 },
      "logistics.track": { "pricePerCall": 0.002, "freeDaily": 100 }
    },
    "alertThreshold": {
      "dailyCost": 50.0,
      "monthlyCost": 1000.0
    },
    "actionOnExceed": "throttle"
  }
}
```

| 控制项 | 说明 |
|--------|------|
| 配额追踪 | 实时统计每日/每月调用量和费用 |
| 告警 | 超过 `alertThreshold` 时发通知 |
| 限流 | `actionOnExceed: throttle` 时降频或暂停同步 |
| 成本报告 | Workshop 看板展示各平台 API 成本趋势 |

---

## 9. 签名插件规范（G3/G4/G5）

### 9.1 签名插件接口

```python
from abc import ABC, abstractmethod

class SignaturePlugin(ABC):
    """签名插件基类"""

    @abstractmethod
    def sign(self, params: dict, secret: str, config: dict) -> str:
        """对请求参数签名，返回签名字符串"""
        pass

    @abstractmethod
    def verify(self, body: bytes, signature: str, secret: str, config: dict) -> bool:
        """验证 Webhook 签名（用于 G7）"""
        pass
```

### 9.2 三种签名实现

| 插件 ID | 算法 | 适用平台 | 核心步骤 |
|---------|------|---------|---------|
| `hmac-sha256` | HMAC-SHA256 | 淘宝/京东/抖音 | params排序 → 拼接 → HMAC-SHA256 → hex/base64 |
| `md5` | MD5 | 拼多多 | params排序 → 拼接key=value → 追加secret → MD5 → uppercase |
| `aws4` | AWS4-HMAC-SHA256 | Amazon | canonicalRequest → stringToSign → deriveSigningKey → HMAC链式 |

### 9.3 签名插件注册

```json
{
  "signaturePlugins": {
    "hmac-sha256": {
      "entryPath": "plugins/signatures/hmac_sha256.py",
      "class": "HmacSha256Signature",
      "configSchema": "schemas/hmac_config.json"
    },
    "md5": {
      "entryPath": "plugins/signatures/md5.py",
      "class": "Md5Signature",
      "configSchema": "schemas/md5_config.json"
    },
    "aws4": {
      "entryPath": "plugins/signatures/aws4.py",
      "class": "Aws4Signature",
      "configSchema": "schemas/aws4_config.json"
    }
  }
}
```

---

## 10. 220plan 对接

| 220plan 编号 | 本文档章节 | 实施状态 |
|-------------|----------|---------|
| W2+ #G1 REST API Connector | §3 | 🔴 待开发 |
| W2+ #G2 OAuth Token Manager | §4 | 🔴 待开发 |
| W2+ #G3 HMAC 签名 | §9.2 | 🟡 可与 G1 同步 |
| W2+ #G4 MD5 签名 | §9.2 | 🟡 可与 G1 同步 |
| W2+ #G5 AWS4 签名 | §9.2 | 🟡 可与 G1 同步 |
| W2+ #G6 GraphQL Connector | §5 | 🔴 待开发 |
| W2+ #G7 Webhook Receiver | §6 | 🔴 待开发 |
| W2+ #G8 抖音解密 | §7 | 🔴 待开发 |
| W2+ #G9 接口计费 | §8 | 🟡 低优先 |
| W2+ #G10 Amazon 报表 Pipeline | (各平台方案) | 🟡 低优先 |

---

## 11. 版本与变更

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-23 | 初版：REST + OAuth + GraphQL + Webhook + 解密 + 计费 + 签名 七大模块架构设计 · 220plan G1-G10 对接 |
