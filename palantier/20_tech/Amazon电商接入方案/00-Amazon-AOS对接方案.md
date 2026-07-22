# Amazon · AOS 数字孪生对接方案 — 总体分析计划

| 字段 | 内容 |
|------|------|
| 状态 | **方案 only · 调研阶段** · 2026-07-22 |
| 版本 | **v1.0** · 初始分析计划 |
| 目录 | `docs/palantier/20_tech/Amazon电商接入方案/` |
| 覆盖范围 | **Amazon Seller（3P 第三方卖家）** — Listings · Orders · FBA Inventory · Fulfillment · Reports · Payments · Catalog · Notifications |
| 关联 | 微商城模板：[00-Niushop微商城AOS对接方案](../微商城电商接入方案/00-Niushop微商城AOS对接方案.md) · 淘宝天猫方案：[00-淘宝天猫AOS对接方案](../淘宝电商接入方案/00-淘宝天猫AOS对接方案-总体分析计划.md) · [220w 差距分析](../220w-与目标系统差距对照分析.md) |
| 原则 | **复用微商城 8 域 Ontology 模板 → Amazon 适配全球多区域 + FBA/FBM 双轨物流 + ASIN 体系** |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 | 全文 |
| 先方案后代码 | 通过前不写行业定制码；缺口回馈**通用平台** |
| 整体孪生 | 目标是 Amazon 卖家业务世界在 AOS 可运营、可感知、可治理 |
| 模板复用 | 微商城（Niushop）8 大领域模型为基线，仅适配全球电商差异 |
| 零行业定制码 | 平台差异通过 Connector 配置 / OT / OKF 映射消解，禁止 `amazon-*` Host 分支 |

---

## 1. 一句话目标

> 将 Amazon 卖家业务（Listings · Orders · FBA Inventory · Fulfillment · Reports · Payments）  
> **整体映射**为 AOS 数字孪生，**复用**微商城 8 大领域模型，  
> 针对 Amazon SP-API 的 **LWAAuth + STS Token + 多区域（NA/EU/FE）+ FBA vs MFN 双轨 + ASIN 全球目录** 做适配层。

```text
微商城（基准模板）              Amazon（适配增量）
────────────────              ──────────────────
JDBC 直连 MySQL               SP-API（REST） + Feeds + Reports
302 张表单表 Sync              LWAAuth + STS Token（1h 轮换）
site_id 多租户                 Marketplace 多区域（NA/EU/FE）
商品/订单/会员 8 域            同 8 域 + FBA Inventory + ASIN Catalog
自建 SKU                      Seller SKU + ASIN 双标识
独立物流                        FBA（亚马逊配送）vs MFN（自发货）双轨
```

---

## 2. Amazon 平台画像

### 2.1 平台概况

| 维度 | 内容 |
|------|------|
| 平台定位 | **全球最大电商平台**（20+ 区域站点，140 万+ 卖家） |
| API 体系 | **Selling Partner API (SP-API)** — REST-based（替代旧 MWS） |
| 端点 | `https://sellingpartnerapi-{region}.amazon.com` |
| 区域 | **NA**（北美：US/CA/MX/BR）、**EU**（欧洲：UK/DE/FR/IT/ES/NL/SE/PL）、**FE**（远东：JP/AU/SG） |
| 认证 | **LWAAuth**（Login with Amazon）→ `access_token`（有效期 1h） + **STS Token**（AWS IAM 角色切换） |
| 签名 | AWS Signature Version 4（`Authorization: AWS4-HMAC-SHA256`） |
| 速率限制 | 各 API 独立限制，含 x-amzn-RateLimit-Limit header |
| 应用类型 | Private Seller（自研） / Public Seller（市场） / Private Vendor |
| SP-API Guard | 安全合规扫描（AWS 部署数据必须通过 Data Protection Policy） |

### 2.2 SP-API 核心模块（10+ 独立 API 组）

| API 模块 | 版本 | 用途 | 适用阵营 |
|----------|------|------|---------|
| **Orders API** | v2026-01-01 | 订单查询（含 FBA + MFN） | 卖家 |
| **Catalog Items API** | v2022-04-01 | ASIN 商品目录查询 | 卖家 + 供应商 |
| **Listings Items API** | v2021-08-01 | Listing（SKU）管理：创建/编辑/删除 | 卖家 |
| **Product Type Definitions API** | v2021-08-01 | 商品分类 Schema 定义 | 卖家 |
| **FBA Inventory API** | v1 | FBA 库存查询（5 种状态：可售/在途/预留/不可售/研究） | 卖家（FBA） |
| **FBA Inbound Eligibility API** | v1 | 商品 FBA 入库资格校验 | 卖家（FBA） |
| **Fulfillment Inbound API** | v2024-03-20 | FBA 入库货件创建/管理 | 卖家（FBA） |
| **Fulfillment Outbound API** | v2020-07-01 | 多渠道配送（MCF）订单 | 卖家（FBA） |
| **Merchant Fulfillment API** | v0 | 自发货（MFN）购买配送 | 卖家（MFN） |
| **Easy Ship API** | v2022-03-23 | Easy Ship 配送管理 | 卖家（印度等特定区域） |
| **Finances API** | v2024-06-19 | 财务事件（收入/退款/索赔/服务费） | 卖家 |
| **Product Pricing API** | v2022-05-01 | 竞争价格查询 | 卖家 |
| **Product Fees API** | v2022-05-01 | 费用估算 | 卖家 |
| **Reports API** | v2021-06-30 | 批量报表（订单/库存/结算） | 卖家 + 供应商 |
| **Feeds API** | v2021-06-30 | 批量上传（商品/库存/价格变更） | 卖家 + 供应商 |
| **Notifications API** | v1 | 事件推送订阅（`ORDER_CHANGE` 等） | 卖家 + 供应商 |
| **A+ Content API** | v2020-11-01 | 品牌 A+ 图文 | 卖家（品牌注册） |
| **Data Kiosk API** | v2023-11-15 | GraphQL 销售/流量数据分析 | 卖家 + 供应商 |
| **Shipment Invoicing API** | v2021-12-28 | 巴西 FBA 发票 | 卖家（BR） |

> **筛选原则：** AOS 数字孪生重点接入 Orders + Catalog + Listings + FBA Inventory + Finances，其余按需后置。

### 2.3 与国内/Shopify 的关键差异

| 维度 | 国内电商 | Shopify | **Amazon** |
|------|---------|---------|-----------|
| 认证 | OAuth 2.0（简单） | OAuth 2.0（scope） | **LWAAuth + STS Token 双令牌**（1h 轮换） |
| 商品标识 | 自建 ID | GID | **双标识：Seller SKU + ASIN（全球统一）** |
| 物流 | 单一 | Carrier API | **FBA（亚马逊配送） vs MFN（自发货）双轨** |
| 库存模型 | 简单数量 | 多 Location | **FBA 库存 5 状态 + 预留/在途/研究** |
| 费率限制 | QPS 简单 | Cost-based | **各 API 独立 Rate-Limit + Burst** |
| 数据传输 | HTTP | HTTP | **Feeds（批量列表）+ Reports（批量报表）双通道** |
| 区域 | 单国家 | 全球 | **SP-API 三区域端点（NA/EU/FE），需分别接入** |
| 合规 | 基本 | GDPR | **SP-API Guard + AWS 数据保护策略（最严）** |

---

## 3. 整体孪生范围（按域）

### 3.1 域分级

| 级 | 名称 | SP-API 模块 | 说明 | 波次 |
|----|------|-----------|------|------|
| **T0** | 店铺/Marketplace | —（静态配置） | NA/EU/FE 多区域映射 | W1 |
| **T1** | 商品（Listings） | Listings Items + Catalog Items + Product Type Definitions | Seller SKU ↔ ASIN 双标识 | W1 |
| **T2** | 订单 | Orders API | 核心，含 FBA/MFN 标记 | W1 |
| **T3** | FBA 库存 | FBA Inventory API | 5 状态库存 + 入库/出库 | W1 |
| **T4** | 履行（Fulfillment） | Fulfillment Inbound/Outbound + Merchant Fulfillment | FBA vs MFN 双轨 | W2 |
| **T5** | 财务（Payments） | Finances API | 收入/退款/索赔/服务费事件 | W2 |
| **T6** | 定价 | Product Pricing + Fees | 竞争价格 + 费用估算 | W2 |
| **T7** | 批量数据 | Reports + Feeds | 报表 + 批量更新 | W2 |
| **T8** | 事件通知 | Notifications | ORDER_CHANGE 等推送 | W3 |
| **T9** | 营销内容 | A+ Content | 品牌图文 | W3 |

**整体孪生退出（MVP）** = **T0～T4 在 AOS 可检索、可关联**（商品 + 订单 + FBA 库存 + 履行状态）。

### 3.2 Amazon 特有概念

| 概念 | 说明 | AOS 处理 |
|------|------|---------|
| **ASIN** | Amazon Standard Identification Number（全球统一商品 ID） | Goods 新增 `asin` Prop，Catalog Object 独立建模 |
| **Seller SKU** | 卖家自定义 SKU（per marketplace） | GoodsSku 主键 |
| **FBA** | Fulfillment by Amazon（亚马逊配送） | Order.fulfillChannel = "AFN" |
| **MFN** | Merchant Fulfilled Network（自发货） | Order.fulfillChannel = "MFN" |
| **FBA Inventory States** | 可售/在途/预留(FC transfer+processing)/不可售/研究 | InventoryStatus Object（5 状态分型） |
| **Marketplace** | NA（US/CA/MX/BR） / EU（8 国） / FE（JP/AU/SG） | Marketplace Object → Workspace mapping |
| **Feed Type** | JSON_LISTING_FEED / POST_PRODUCT_DATA 等 | 不纳入孪生（运营反向写，可选后置） |
| **Report Type** | GET_FLAT_FILE_ALL_ORDERS_DATA_* 等 100+ 种 | Sync 定时 Download + Parse → Dataset |

---

## 4. Ontology 目标态（对象与关系）

### 4.1 Object Type 清单

| Object Type | 主键 | SP-API 源 | 说明 | vs 微商城增量 |
|-------------|------|----------|------|-------------|
| **Marketplace** | marketplaceId | Static | 区域（US/CA/UK/DE/JP…） | **新建**（Amazon 独有） |
| **Goods** | asin | Catalog Items | ASIN 全球统一商品 | **双标识**（ASIN + Seller SKU） |
| **GoodsSku** | sellerSku | Listings Items | 卖家 Listing | 对齐 |
| **GoodsCategory** | productTypeId | Product Type Definitions | 商品类型 Schema | 对齐 |
| **Order** | amazonOrderId | Orders API | 故事核 | `fulfillChannel`（AFN/MFN）+ `marketplaceId` |
| **OrderLine** | orderItemId | Orders（内嵌 OrderItems） | 订单行 | 含量税/净税拆分 |
| **FBAInventory** | asin+sellerSku+warehouseCondition | FBA Inventory | FBA 库存（5 状态） | **新建** |
| **InboundShipment** | shipmentId | Fulfillment Inbound | FBA 入库货件 | **新建** |
| **Fulfillment** | fulfillmentId | Fulfillment Outbound / Merchant Fulfillment | 订单履单 | 对齐（FBA Web vs MFN Buy Shipping） |
| **FinanceEvent** | eventId | Finances API | 收入/退款/费用事件 | **新建** |
| **Report** | reportId | Reports API | 批量报表记录 | 新建（可薄） |

### 4.2 Link Type（核心）

| Link | from → to |
|------|-----------|
| `Order.onMarketplace` | Order → Marketplace |
| `Order.lines` | Order → OrderLine |
| `OrderLine.ofSku` | OrderLine → GoodsSku |
| `GoodsSku.ofAsin` | GoodsSku → Goods |
| `Goods.ofCategory` | Goods → GoodsCategory |
| `GoodsSku.inMarketplace` | GoodsSku → Marketplace |
| `GoodsSku.hasInventory` | GoodsSku → FBAInventory |
| `FBAInventory.inMarketplace` | FBAInventory → Marketplace |
| `Order.hasShipment` | Order → InboundShipment（FBA） |
| `Order.hasFulfillment` | Order → Fulfillment |
| `Order.hasFinanceEvent` | Order → FinanceEvent |

### 4.3 Funnel（订单 · FBA/MFN 双轨）

```text
                ┌── FBA ───────────────────────────────┐
Pending → Unshipped → Shipped → Delivered → Completed
                │                                       │
                └── MFN ───────────────────────────────┘
                       Merchant 自行发货/购买配送

        Cancelled / Refunded（任意阶段可跳转）
```

> SP-API Orders API 返回 `OrderStatus` + `FulfillmentChannel` 两个字段。  
> FBA 订单状态由亚马逊自动推进（Seller 无发货动作）；  
> MFN 订单需卖家确认发货（`ConfirmShipment`）。

---

## 5. 数据接入策略

### 5.1 总原则

| 路径 | 用途 | Amazon 用法 |
|------|------|-----------|
| **A. Orders API（实时/准实时）** | 订单全量/增量拉取 | `getOrders`（by LastUpdatedTime）+ `getOrderItems` |
| **B. Reports API（批量）** | 订单/库存/结算批量报表 | 请求 `GET_FLAT_FILE_ALL_ORDERS_DATA_*` → 轮询 → Download → Parse |
| **C. FBA Inventory API** | FBA 库存实时 | `getInventorySummaries`（5 状态） |
| **D. Finances API** | 财务事件准实时 | `listFinancialEventsByOrderId` |
| **E. Notifications（实时）** | 事件驱动（推荐） | `ORDER_CHANGE`, `REPORT_PROCESSING_FINISHED` 等 |
| **F. Feeds API（反向写）** | 更新 Listing/库存（可后置） | 非孪生主链路，运营 Action 触发 |

### 5.2 区域接入架构

```text
Amazon SP-API（三区域）
      │
      ├── NA Endpoint（US/CA/MX/BR）
      ├── EU Endpoint（UK/DE/FR/IT/ES/NL/SE/PL）
      └── FE Endpoint（JP/AU/SG）
      │
      │ LWAAuth + STS Token（每区域独立）
      ▼
  AOS REST API Connector（通用平台能力 · 待建）
      │
      ├── Orders Sync（按 LastUpdatedTime 增量）
      ├── FBA Inventory Sync（定时轮询）
      ├── Reports Poll（定时 request → download → parse）
      └── Finance Events（按 OrderId 补查）
      ▼
  Dataset（按 Marketplace 分 Dataset）
      ▼
  OKF → Object / Link（按区域隔离或统一，由项目决策）
```

### 5.3 AOS 平台缺口（接入前提）

| 编号 | 缺口 | 影响 | 优先级 |
|------|------|------|--------|
| **G-REST-01** | REST API Connector 类型 | 所有电商共用 | 🔴 阻塞 |
| **G-OAUTH-01** | OAuth 2.0 Token Manager（通用） | 所有电商共用 | 🔴 阻塞 |
| **G-AWS4-01** | **AWS Signature V4 签名插件** | Amazon 专属（SP-API 签名） | 🟡 Amazon 专属 |
| **G-LWAAUTH-01** | **LWAAuth Token 轮换（1h 有效期 + STS Role）** | Amazon 专属（双令牌机制） | 🟡 Amazon 专属 |
| **G-REPORT-01** | **报表下载 + 解析 Pipeline** | Amazon Reports → CSV/FlatFile → Parse → Dataset | 🟡 Amazon 专属 |
| **G-MULTI-REGION-01** | 多区域 Connector 路由（NA/EU/FE 不同端点） | SP-API 三区域独立接入 | 🟢 通用增强 |

---

## 6. 从物理到孪生的主链路

```text
Amazon Seller Account（NA / EU / FE）
      │
      │ LWAAuth + STS Token（每区域）
      ▼
  SP-API REST Connector（AWS Signature V4）
      │
      ├── Orders API（增量：LastUpdatedTime）
      ├── Reports API（批量：request→poll→download→parse CSV）
      ├── FBA Inventory API（定时轮询）
      └── Finances API（按 OrderId 补查）
      ▼
  Source → Sync → Dataset（按 Marketplace 分区）
      ▼
  OKF 映射 → Funnel 水合（双轨 FBA/MFN） → Object / Link
      ▼
  ┌─────────┬──────────┬────────────┬───────────┐
  ▼         ▼          ▼            ▼
 COP态势   Inbox运营  Graph/Buddy  Analytics
 新单/缺货/      库存预警/      跨区域查询    多 Market-
 FBA滞留         索赔事件                    place 汇总
```

---

## 7. 实施波次

| 波次 | 内容 | 依赖 | 状态 |
|------|------|------|------|
| **P0** | 本方案通过（本文） | — | ✅ v1.0 |
| **P1** | Amazon Seller Central 开发者注册 + SP-API 角色申请 | 卖家账号 | ⬜ 待执行 |
| **P1** | SP-API 沙箱测试（NA 单区域，Orders + FBA Inventory） | 开发者注册通过 | ⬜ 待执行 |
| **P2** | REST API Connector（通用） | 220plan W2+ 基础设施 | 🔴 阻塞 |
| **P2** | OAuth 2.0 / LWAAuth Token Manager（通用框架） | 同上 | 🔴 阻塞 |
| **P2** | AWS Signature V4 签名插件 | Connector 可插拔 | 🟡 阻塞 |
| **P2** | Report Download + Parse Pipeline | — | 🟡 阻塞 |
| **W1** | NA 区域沙箱验证（Orders + FBA Inventory） | P2 完成 | ⬜ 待执行 |
| **W2** | EU + FE 多区域接入 | W1 通过 | ⬜ 待执行 |
| **W3** | 全域接入 + 态势/分析上线 | W2 通过 | ⬜ 待执行 |

---

## 8. 五大电商平台总览

| 维度 | 微商城 | 淘宝/天猫 | 拼多多 | Shopify | **Amazon** |
|------|--------|----------|--------|---------|-----------|
| API 协议 | JDBC MySQL | REST（HMAC-SHA256） | REST（MD5） | GraphQL | REST（AWS4-HMAC-SHA256） |
| 认证 | 数据库密码 | OAuth 2.0 | OAuth 2.0 | OAuth 2.0（scope） | **LWAAuth + STS Token（1h 轮换）** |
| 增量机制 | SQL diff | 无原生 | `increment.get` | Webhook | Notifications + Reports |
| 商品 ID | 自建 SKU | num_iid | goodsId | GID | **Seller SKU + ASIN（双标识）** |
| 物流 | 自维护 | 菜鸟 | 快递公司 | Carrier API | **FBA + MFN 双轨** |
| 会员 | 完整（自营） | 脱敏 | 基本 | 完整 | 脱敏（Buyer Info 有限） |
| 区域 | 单站 | 单区（中国） | 单区（中国） | 全球（单店） | **多区域（NA/EU/FE 三端点）** |
| 合规 | 基本 | 基本 | 基本 | GDPR | **SP-API Guard + AWS DPP（最严）** |
| 复杂性 | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 9. 下一步行动

| 优先级 | 行动 | 阻塞条件 |
|-------|------|---------|
| **P0 ✅** | 本方案完成 | — |
| **P1** | Amazon Seller Central 开发者账号注册 | 卖家账号（可用于沙箱） |
| **P1** | SP-API 沙箱 Orders + FBA Inventory 探活脚本 | 开发者注册 |
| **P2** | REST API Connector + Token Manager（通用） | 220plan W2+ 基础设施 |
| **P2** | AWS Signature V4 签名 + LWAAuth 插件 | Connector 架构就绪 |
| **P2** | Report Download + Parse Pipeline | — |

> **版本**：v1.0 · 2026-07-22 · 总体分析计划  
> **变更日志**：  
> | 版本 | 日期 | 说明 |  
> | --- | --- | --- |  
> | v1.0 | 2026-07-22 | 初版 · 基于 Amazon SP-API 调研 · 20+ API 模块筛选 · LWAAuth + STS 双令牌 · FBA/MFN 双轨物流 · ASIN 全球目录 · 5 大平台对比总览 |
