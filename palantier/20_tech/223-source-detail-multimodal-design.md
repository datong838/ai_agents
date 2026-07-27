# 223 · 数据源详情页多模态设计方案

> **版本**：v1.0 · 2026-07-26
> **定位**：数据源详情页（`sourceDetailPage.tsx`）按 Connector 类型差异化渲染探索视图
> **视觉稿基准**：`source-detail.html`（仅展示 JDBC/PostgreSQL 变体）
> **核心原则**：不同数据源结构完全不同，不能一刀切用 DB Explorer

---

## 1. 问题分析

### 1.1 视觉稿只画了一种

`source-detail.html` 的探索页是 **PostgreSQL DB Explorer** 模式：
- 左栏：Schema 树（📁 schema → 表 → 列定义 PK/FK/类型）
- 中栏：ER 关系图（表间连线）+ 数据预览表
- 右栏：已选表列表

这个布局**只适用于关系型数据库**。

### 1.2 系统实际支持 6 类数据源

| Connector | pluginId | 数据结构 | 探索视图应该是 |
|-----------|----------|---------|--------------|
| MySQL JDBC | `jdbc-mysql` | schema → table → column | DB Explorer（同视觉稿） |
| PostgreSQL JDBC | `jdbc-postgres` | schema → table → column | DB Explorer（同视觉稿） |
| SQL Server JDBC | `jdbc-sqlserver` | database → schema → table → column | DB Explorer（多一层 database） |
| 本地文件 | `file-local` | 目录 → 文件（CSV/JSON/Parquet） | File Browser（文件树+预览） |
| 对象存储 | `file-object-store` | bucket → prefix → 对象 | Object Browser（S3 风格） |
| 通用 REST | `rest-generic` | endpoint → JSON response | Endpoint Explorer（API 列表+响应预览） |

### 1.3 未来扩展（电商平台接入方案）

| 平台 | Connector 类型 | 数据结构 | 探索视图 |
|------|---------------|---------|---------|
| 淘宝/天猫 | REST + HMAC | API 方法 → 响应 JSON | Endpoint Explorer（含签名信息） |
| 拼多多 | REST + MD5 | API 方法 → 响应 JSON | Endpoint Explorer |
| 京东 | REST + HMAC | API 方法 → 响应 JSON | Endpoint Explorer |
| 抖音 | REST + 内容+电商 | API 方法 → 响应 JSON | Endpoint Explorer（含解密标记） |
| Shopify | GraphQL + Webhook | Query/Mutation → 响应 | GraphQL Explorer（Schema 文档） |
| Amazon | SP-API + AWS4 | API → 响应 JSON | Endpoint Explorer（多区域） |

---

## 2. 总体架构：Connector-Adaptive Explorer

### 2.1 渲染分发

```
SourceDetailPage
├── 顶部工具栏（统一：标题+连接器Badge+Refresh+Filter）
├── Tab 栏（统一：概览 | 探索 | 同步 | 凭证）
└── 探索 Tab 内容（按 connectorFamily 分发）
    ├── JDBC → <DbExplorer />     （DB 浏览器：Schema树+ER图+预览）
    ├── File → <FileExplorer />   （文件浏览器：目录树+文件预览）
    ├── REST → <EndpointExplorer />（API 浏览器：端点列表+响应预览）
    └── GraphQL → <GraphqlExplorer />（GraphQL 浏览器：Schema文档+查询）
```

### 2.2 共享组件

无论哪种模态，以下组件是共享的：

| 组件 | 用途 | 复用度 |
|------|------|--------|
| `SourceToolbar` | 顶部标题+Badge+Refresh+Filter | 所有模态 |
| `SourceTabs` | Tab 切换 | 所有模态 |
| `SourceInspector` | 右侧信息面板 | 所有模态（内容不同） |
| `PreviewTable` | 数据预览表格 | JDBC/File/REST/GraphQL 都用 |
| `JsonPreview` | JSON 响应预览 | REST/GraphQL/File(JSON) |
| `SchemaTree` | 左侧树形导航 | JDBC（DB列树）/ File（目录树）/ REST（端点树） |

---

## 3. 模态 A：DB Explorer（JDBC 系列）

> **适用**：jdbc-mysql / jdbc-postgres / jdbc-sqlserver
> **视觉稿基准**：`source-detail.html`（完全对标）

### 3.1 布局

```
┌─────────────────────────────────────────────────────────┐
│  探索 · prod-postgresql-orders      [🐘 PostgreSQL]  [刷新] │
├──────────┬────────────────────────────┬──────────────────┤
│ Schema 树 │     ER 关系图               │  已选表          │
│          │  ┌─────┐    ┌──────────┐   │  ┌────────────┐ │
│ 📁 public │  │orders│───→│customers │   │  │orders      │ │
│  📋 orders│  │      │    └──────────┘   │  │ 6 列       │ │
│   🔑 id  │  └──┬───┘                    │  │ 12,345 行  │ │
│   🔗 cust│     │                        │  └────────────┘ │
│  📋 items│     ▼                        │  ┌────────────┐ │
│  📋 prod │  ┌──────────┐                │  │customers   │ │
│          │  │order_items│               │  │ 4 列       │ │
│ 搜索…     │  └──────────┘                │  └────────────┘ │
├──────────┴────────────────────────────┴──────────────────┤
│  数据预览 · orders (显示 50 行 / 共 12,345 行)        [刷新] │
│  ┌──────┬────────────┬────────┬────────┬────────┐       │
│  │ id   │ customer_id│ amount │currency│ status │       │
│  ├──────┼────────────┼────────┼────────┼────────┤       │
│  │ 1001 │ 502        │ 299.00 │ CNY    │ paid   │       │
│  └──────┴────────────┴────────┴────────┴────────┘       │
└─────────────────────────────────────────────────────────┘
```

### 3.2 左栏：Schema 树

```
📁 public (8)           ← schema 层（可折叠）
  📋 orders              ← 表层（点击选中）
    🔑 order_id    BIGINT PK   ← 列层（PK 标记）
    🔗 customer_id BIGINT FK   ← FK 标记（高亮）
       amount      DECIMAL(10,2)
       currency    VARCHAR(3)
       status      VARCHAR(20)
       created_at  TIMESTAMP
  📋 order_items
  📋 customers
  📋 products
  📋 inventory
  📋 shipments
  📋 refunds
  📋 reviews
📁 analytics (3)        ← 另一个 schema
  📋 daily_sales
  📋 top_products
  📋 customer_segments
```

**交互**：
- 表名点击 → 中栏 ER 图高亮该表 + 底部预览加载该表数据
- 表名展开 → 显示列定义（名称+类型+PK/FK 标记）
- FK 列点击 → 跳转到关联表并高亮
- 搜索框 → 模糊过滤表名和列名
- 多选模式（复选框）→ 选中的表进入右栏

**数据来源**：需要后端新增 `GET /v1/sources/{id}/schema` 接口返回完整 schema 元数据

### 3.3 中栏上：ER 关系图

选中表后自动展示其 1 跳关系（FK 引用的表 + 引用它的表）：

```
     ┌──────────┐         ┌──────────┐
     │ customers│←────────│ orders   │
     │ id (PK)  │  cust_id │ order_id │
     │ name     │  (FK)    │ cust_id  │
     └──────────┘         │ amount   │
                           └────┬─────┘
                                │ order_id
                                ▼
                          ┌────────────┐
                          │ order_items│
                          │ item_id PK │
                          │ order_id FK│
                          │ product_id │
                          └──────┬─────┘
                                 │ product_id
                                 ▼
                          ┌──────────┐
                          │ products │
                          │ id (PK)  │
                          └──────────┘
```

用 SVG 绘制（类似 Pipeline Canvas 的节点连线），支持：
- 节点拖拽重排
- 点击节点 → 加载该表数据预览
- 双击节点 → 跳转该表详情

### 3.4 底部：数据预览

选中表的采样数据（前 50 行），当前系统已有此功能（`apiPost("/v1/analytics/datasets/preview")`），保留。

### 3.5 右栏：已选表列表

多选模式下勾选的表汇总，可批量操作（创建管道、导出 schema）。

### 3.6 SQL Server 差异

SQL Server 多一层 `database`：
```
📁 OrderDB              ← database 层
  📁 dbo                ← schema 层
    📋 orders
  📁 sales
    📋 daily_revenue
📁 InventoryDB          ← 另一个 database
  📁 dbo
    📋 stock
```

---

## 4. 模态 B：File Explorer（file-local / file-object-store）

> **适用**：file-local / file-object-store (S3)
> **无视觉稿**，需新建

### 4.1 布局

```
┌─────────────────────────────────────────────────────────┐
│  探索 · sales-data-csv           [📁 本地文件]     [刷新] │
├──────────┬────────────────────────────────┬─────────────┤
│ 文件树    │  文件预览                       │ 文件信息    │
│          │                                │             │
│ 📁 /data  │  📄 orders_2024_q1.csv         │ 名称:       │
│  📁 raw   │  ┌────────────────────────┐    │ orders_...  │
│   📄 q1   │  │order_id,customer,amount│    │             │
│   📄 q2   │  │1001,张三,299.00        │    │ 大小: 2.3MB │
│  📁 clean │  │1002,李四,158.50        │    │ 格式: CSV   │
│   📄 q1   │  │1003,王五,1200.00       │    │ 行数: 8,234 │
│   📄 q2   │  │...                     │    │ 列数: 12    │
│  📁 schema│  └────────────────────────┘    │ 编码: UTF-8 │
│   📄 map  │                                │ 分隔符: ,   │
│           │  [📋 字段推断]                  │             │
│ 搜索…     │  order_id    INTEGER           │ 首行: 表头  │
│           │  customer    STRING            │             │
│           │  amount      DECIMAL           │ [创建管道]  │
└──────────┴────────────────────────────────┴─────────────┘
```

### 4.2 左栏：文件目录树

```
📁 /data                    ← 根目录
  📁 raw/                   ← 子目录（可折叠）
    📄 orders_q1.csv        ← 文件（图标按格式区分）
    📄 orders_q2.csv
    📄 products.json
    📄 events.parquet
  📁 clean/
    📄 orders_clean.csv
  📄 schema_map.json
```

**文件图标**：
- 📄 CSV → 表格图标
- 📋 JSON → 花括号图标
- 📦 Parquet → 包箱图标
- 📷 图片 → 图片图标（file-object-store 特有）

### 4.3 中栏：文件预览

根据文件格式自动选择预览方式：

| 格式 | 预览方式 |
|------|---------|
| CSV/TSV | 数据表格（前 50 行）+ 字段类型推断 |
| JSON | JSON Tree（可折叠）+ 原始视图切换 |
| Parquet | Schema 摘要 + 前 N 行表格 |
| 图片 | 缩略图 + 元数据（尺寸/格式/大小）|
| 其他文本 | 代码高亮预览（前 100 行）|

### 4.4 file-object-store (S3) 差异

- 左栏顶部多一个 **Bucket 选择器**
- 目录树前缀用 `/` 分隔（S3 的 prefix）
- 支持显示对象元数据（ETag、Last-Modified、Storage Class）
- 文件预览增加签名 URL 生成（临时下载链接）

---

## 5. 模态 C：Endpoint Explorer（rest-generic / 电商平台）

> **适用**：rest-generic / 淘宝 / 拼多多 / 京东 / 抖音 / Amazon
> **无视觉稿**，需新建

### 5.1 布局

```
┌─────────────────────────────────────────────────────────┐
│  探索 · taobao-top-api           [🌐 REST+HMAC]   [刷新]  │
├──────────┬────────────────────────────────┬─────────────┤
│ 端点列表  │  响应预览                       │ 端点信息    │
│          │                                │             │
│ 📁 订单   │  POST taobao.trades.sold.get  │ Action:     │
│  ◉ 列表   │  ┌──────────────────────────┐ │ trades.sold │
│  ○ 详情   │  │{                         │ │   .get      │
│  ○ 发货   │  │  "trades_sold_get_resp": │ │             │
│ 📁 商品   │  │    "trades": {            │ │ Method:     │
│  ○ 列表   │  │      "trade": [          │ │ POST        │
│  ○ 详情   │  │        {"tid":"12345",   │ │             │
│ 📁 物流   │  │         "status":"paid", │ │ 分页:       │
│  ○ 查询   │  │         "payment":"299"} │ │ page 模式   │
│ 📁 评价   │  │        }                  │ │ page_no     │
│  ○ 列表   │  │      ]                    │ │ page_size   │
│           │  │    }                      │ │             │
│ 搜索…     │  │  }                        │ │ 签名:       │
│           │  └──────────────────────────┘ │ HMAC-SHA256 │
│           │  [原始 JSON] [映射后]          │             │
│           │                                │ QPS 限制:   │
│           │                                │ 40/s        │
└──────────┴────────────────────────────────┴─────────────┘
```

### 5.2 左栏：端点分组树

按业务领域分组（来自 Connector 配置的 `endpoints` schema）：

```
📁 订单 (6)                ← 领域分组
  ◉ Order.list            ← 端点（●=有数据 ○=未调用过）
  ○ Order.get
  ○ Order.ship
  ○ Order.close
  ○ Order.refund
  ○ Order.remark
📁 商品 (4)
  ○ Product.list
  ○ Product.get
  ○ Product.update
  ○ Product.delete
📁 物流 (2)
  ○ Logistics.query
  ○ Logistics.trace
📁 评价 (2)
  ○ Review.list
  ○ Review.reply
```

### 5.3 中栏：响应预览

双视图切换：
- **原始 JSON**：API 返回的原始响应（语法高亮+可折叠）
- **映射后**：按 `platform_mapping/*.json` 映射规则转换后的标准化数据（表格形式）

**响应信息条**：
- 状态码：200 OK
- 耗时：234ms
- 分页：第 1 页 / 共 312 页（has_next=true）
- 限流：剩余 38 次/s

### 5.4 右栏：端点信息

```
Action:     taobao.trades.sold.get
Method:     POST
签名方案:    HMAC-SHA256
认证类型:    OAuth2
分页模式:    page (page_no + page_size)
QPS 限制:   40/s
重试策略:    指数退避 × 3
映射文件:    taobao_order.json

[调用测试]  [查看映射]  [创建管道]
```

### 5.5 电商平台差异表

| 平台 | Badge | 特殊信息 |
|------|-------|---------|
| 淘宝/天猫 | `🌐 REST+HMAC` | OAuth2 + HMAC-SHA256 |
| 湖北多 | `🌐 REST+MD5` | OAuth2 + MD5 |
| 京东 | `🌐 REST+HMAC` | POP/自营差异标注 |
| 抖音 | `🌐 REST+解密` | 含内容(视频)+电商双域 + 数据解密 |
| Amazon | `🌐 SP-API+AWS4` | 多区域选择器 (us-east-1 / eu-west-1 / ...) |

---

## 6. 模态 D：GraphQL Explorer（Shopify）

> **适用**：Shopify（GraphQL + Webhook）
> **无视觉稿**，需新建

### 6.1 布局

```
┌─────────────────────────────────────────────────────────┐
│  探索 · shopify-store-myshop    [🔷 GraphQL+Webhook][刷新]│
├──────────┬────────────────────────────────┬─────────────┤
│ Schema   │  查询构建器                      │ 查询信息    │
│ 文档     │                                │             │
│          │  query {                       │ Operation:  │
│ 📁 Query │    orders(first: 10) {         │ Query       │
│  ◉ orders│      edges {                   │             │
│  ○ produc│        node {                  │ 类型:       │
│ 📁 Mutn  │          id                    │ OrderConnection │
│  ○ orderC│          name                  │             │
│  ○ prodU │          totalPrice            │ 分页:       │
│ 📁 Subsc │          displayFulfillmentSta │ cursor      │
│  ○ order │          customer {            │ hasNextPage │
│           │            displayName         │             │
│ 搜索…     │            email               │ Webhook:    │
│           │          }                     │ orders/create│
│           │        }                       │ orders/paid │
│           │      }                         │             │
│           │    }                           │ [运行查询]  │
│           │  }                             │ [注册Webhook]│
│           │  ┌──────────────────────────┐ │             │
│           │  │{"data":{"orders":{...}}}| │             │
│           │  └──────────────────────────┘ │             │
└──────────┴────────────────────────────────┴─────────────┘
```

### 6.2 左栏：Schema 文档树

从 Shopify GraphQL Schema 自动提取（introspection）：

```
📁 Query                  ← 根查询类型
  ◉ orders(first,after,query) → OrderConnection
  ○ products(first,after) → ProductConnection
  ○ customers(first) → CustomerConnection
  ○ inventoryLevels → InventoryLevelConnection
📁 Mutation               ← 变更类型
  ○ orderCreate(input) → OrderCreatePayload
  ○ productUpdate(input) → ProductUpdatePayload
  ○ inventoryAdjustQuantity → InventoryAdjustPayload
📁 Subscription           ← 订阅（Webhook 映射）
  ○ orderCreated → webhook: orders/create
  ○ orderPaid → webhook: orders/paid
  ○ fulfillmentCreated → webhook: fulfillments/create
```

### 6.3 中栏：查询构建器 + 响应

- 上半区：GraphQL 查询编辑器（代码高亮，支持 introspection 自动补全）
- 下半区：响应 JSON（折叠树视图）

### 6.4 右栏：查询信息 + Webhook 管理

显示选中 Query/Mutation 的参数、返回类型，以及对应的 Webhook 主题列表。

---

## 7. 后端 API 需求

### 7.1 通用 API（所有模态共享）

| API | 方法 | 用途 | 状态 |
|-----|------|------|------|
| `/v1/sources` | GET | 数据源列表 | ✅ 已有 |
| `/v1/sources/{id}` | GET | 单个数据源详情 | ✅ 已有 |
| `/v1/pipelines` | GET | 关联管道 | ✅ 已有 |
| `/v1/datasets` | GET | 关联数据集 | ✅ 已有 |
| `/v1/syncs` | GET | 同步记录 | ✅ 已有 |
| `/v1/analytics/datasets/preview` | POST | 数据预览 | ✅ 已有 |
| `/v1/analytics/objects/list` | POST | 对象列表预览 | ✅ 已有 |

### 7.2 新增 API（按模态）

#### DB Explorer 模态

| API | 方法 | 用途 |
|-----|------|------|
| `/v1/sources/{id}/schema` | GET | 返回完整 schema（database→schema→table→column，含 PK/FK/类型） |
| `/v1/sources/{id}/tables/{table}/columns` | GET | 单表列定义 |
| `/v1/sources/{id}/tables/{table}/relations` | GET | 表的外键关系（用于 ER 图） |

**响应示例** `/v1/sources/{id}/schema`：
```json
{
  "connectorFamily": "jdbc",
  "dialect": "postgresql",
  "databases": ["public"],
  "schemas": [
    {
      "name": "public",
      "tables": [
        {
          "name": "orders",
          "columns": [
            {"name": "order_id", "type": "BIGINT", "primaryKey": true, "nullable": false},
            {"name": "customer_id", "type": "BIGINT", "foreignKey": {"table": "customers", "column": "id"}, "nullable": false},
            {"name": "amount", "type": "DECIMAL(10,2)", "nullable": false},
            {"name": "currency", "type": "VARCHAR(3)"},
            {"name": "status", "type": "VARCHAR(20)"},
            {"name": "created_at", "type": "TIMESTAMP"}
          ],
          "rowCount": 12345
        }
      ]
    }
  ]
}
```

#### File Explorer 模态

| API | 方法 | 用途 |
|-----|------|------|
| `/v1/sources/{id}/files` | GET | 目录树（参数 `?prefix=` 指定路径） |
| `/v1/sources/{id}/files/preview` | GET | 文件预览（参数 `?path=` + `?format=csv\|json\|parquet`） |
| `/v1/sources/{id}/files/infer-schema` | POST | 推断文件字段类型（CSV/Parquet） |

#### Endpoint Explorer 模态

| API | 方法 | 用途 |
|-----|------|------|
| `/v1/sources/{id}/endpoints` | GET | 端点列表（从 Connector 配置的 `endpoints` schema 生成） |
| `/v1/sources/{id}/endpoints/{action}/test` | POST | 测试调用单个端点（带分页参数） |
| `/v1/sources/{id}/endpoints/{action}/mapping` | GET | 查看映射规则 |

#### GraphQL Explorer 模态

| API | 方法 | 用途 |
|-----|------|------|
| `/v1/sources/{id}/graphql/schema` | GET | GraphQL introspection 结果 |
| `/v1/sources/{id}/graphql/query` | POST | 执行 GraphQL 查询 |
| `/v1/sources/{id}/webhooks` | GET | Webhook 订阅列表 |

---

## 8. 前端组件设计

### 8.1 组件树

```
SourceDetailPage (路由: /data/sources/:sourceId)
├── SourceToolbar          ← 统一工具栏
│   ├── SourceBadge        ← 连接器类型标签（🐘PG / 📁File / 🌐REST / 🔷GraphQL）
│   └── SourceActions      ← 刷新/筛选/创建管道
├── SourceTabs             ← 概览|探索|同步|凭证
└── ExploreTab             ← 探索 Tab（按 family 分发）
    ├── DbExplorer         ← 模态A: JDBC
    │   ├── SchemaTree     ← schema→table→column 树
    │   ├── ErGraph        ← SVG 关系图
    │   └── DataPreview     ← 数据预览表
    ├── FileExplorer       ← 模态B: File
    │   ├── FileTree       ← 目录树
    │   ├── FilePreview    ← 文件内容预览（CSV表/JSON树/图片）
    │   └── SchemaInfer    ← 字段类型推断面板
    ├── EndpointExplorer  ← 模态C: REST
    │   ├── EndpointList   ← 端点分组列表
    │   ├── ResponseView   ← 响应预览（原始/映射后切换）
    │   └── EndpointInfo   ← 端点元信息（签名/分页/QPS）
    └── GraphqlExplorer   ← 模态D: GraphQL
        ├── SchemaDoc      ← GraphQL Schema 文档树
        ├── QueryBuilder   ← 查询编辑器
        └── WebhookPanel   ← Webhook 订阅管理
```

### 8.2 family 判定逻辑

```typescript
function getConnectorFamily(source: SourceRow): "jdbc" | "file" | "rest" | "graphql" {
  const type = source.type || source.pluginId || "";
  if (type.includes("jdbc") || type.includes("mysql") || type.includes("postgres") || type.includes("sqlserver"))
    return "jdbc";
  if (type.includes("file") || type.includes("s3") || type.includes("object-store"))
    return "file";
  if (type.includes("graphql"))
    return "graphql";
  return "rest"; // rest-generic + 电商平台都走这里
}
```

### 8.3 Badge 图标映射

```typescript
const CONNECTOR_BADGE: Record<string, { icon: string; label: string }> = {
  "jdbc-mysql":      { icon: "🐬", label: "MySQL" },
  "jdbc-postgres":   { icon: "🐘", label: "PostgreSQL" },
  "jdbc-sqlserver":  { icon: "🟦", label: "SQL Server" },
  "file-local":      { icon: "📁", label: "本地文件" },
  "file-object-store":{ icon: "☁️", label: "对象存储" },
  "rest-generic":    { icon: "🌐", label: "REST" },
  "taobao-top":      { icon: "🛒", label: "REST+HMAC" },
  "pdd-api":         { icon: "🛒", label: "REST+MD5" },
  "jd-pop":          { icon: "🛒", label: "REST+HMAC" },
  "douyin-ec":       { icon: "🎵", label: "REST+解密" },
  "shopify-graphql": { icon: "🔷", label: "GraphQL+Webhook" },
  "amazon-spapi":    { icon: "📦", label: "SP-API+AWS4" },
};
```

---

## 9. 实施计划

### Phase 1：JDBC 模态对标视觉稿（P0，3-5 天）

**目标**：把当前 `sourceDetailPage.tsx` 改造为视觉稿的 DB Explorer 布局

| 任务 | 类型 | 工作量 |
|------|------|--------|
| 后端 `GET /v1/sources/{id}/schema` | 新增 | M |
| 后端 `GET /v1/sources/{id}/tables/{t}/relations` | 新增 | S |
| 前端 `SchemaTree` 组件（含列定义展开） | 新建 | M |
| 前端 `ErGraph` 组件（SVG 关系图） | 新建 | L |
| 前端 `SourceDetailPage` 改为三栏布局 | 改造 | M |
| 前端 connector family 分发逻辑 | 新增 | S |

### Phase 2：File 模态（P1，2-3 天）

| 任务 | 类型 | 工作量 |
|------|------|--------|
| 后端 `GET /v1/sources/{id}/files` | 新增 | M |
| 后端 `GET /v1/sources/{id}/files/preview` | 新增 | M |
| 前端 `FileExplorer` 组件 | 新建 | M |
| 前端 `FilePreview`（CSV/JSON/Parquet 三种） | 新建 | M |

### Phase 3：REST 模态（P1，2-3 天）

| 任务 | 类型 | 工作量 |
|------|------|--------|
| 后端 `GET /v1/sources/{id}/endpoints` | 新增 | S |
| 后端 `POST /v1/sources/{id}/endpoints/{a}/test` | 新增 | M |
| 前端 `EndpointExplorer` 组件 | 新建 | M |
| 前端 `ResponseView`（原始/映射切换） | 新建 | S |

### Phase 4：GraphQL 模态（P2，3-5 天）

| 任务 | 类型 | 工作量 |
|------|------|--------|
| 后端 `GET /v1/sources/{id}/graphql/schema` | 新增 | M |
| 后端 `POST /v1/sources/{id}/graphql/query` | 新增 | M |
| 前端 `GraphqlExplorer` 组件 | 新建 | L |
| 前端 `QueryBuilder`（带补全） | 新建 | L |

**总工作量：10-16 人天**

---

## 10. 共享设计 Token（所有模态统一）

```css
/* 探索页统一变量 */
--src-toolbar-height: 44px;
--src-left-width: 240px;
--src-right-width: 280px;
--src-preview-height: 240px;
--src-tree-item-height: 28px;
--src-tree-indent: 16px;
--src-table-header-bg: #F9FAFB;
--src-table-row-hover: #F3F4F6;
--src-badge-radius: 4px;
--src-badge-font-size: 11px;
--src-col-pk-color: #7C3AED;   /* PK 紫色 */
--src-col-fk-color: #2563EB;   /* FK 蓝色 */
--src-er-line-color: #D1D5DB;  /* ER 图连线 */
--src-er-node-bg: #FFFFFF;
--src-er-node-border: #E5E7EB;
```
