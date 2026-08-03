# 淘宝 + 天猫 · AOS 数字孪生对接方案 — 总体分析计划

| 字段 | 内容 |
|------|------|
| 状态 | **P0/P1 已完成 · P2 待平台就绪** · 2026-07-22 |
| 版本 | **v1.1** · P0 §3 字段级对照完成 + P1 API 清单 & Schema 分析已完成 |
| 目录 | `docs/palantier/20_tech/淘宝电商接入方案/` |
| 覆盖范围 | **淘宝（C 店）+ 天猫（品牌旗舰店）** — 合并分析（共用一个开放平台 TOP） |
| 关联 | 微商城模板：[00-Niushop微商城AOS对接方案](../微商城电商接入方案/00-Niushop微商城AOS对接方案.md) · [220w 差距分析](../../220w-与目标系统差距对照分析.md) · [220plan 开发计划](../../220plan-分阶段开发与里程碑计划.md) |
| 原则 | **先微商城打透 → 提炼模板 → 淘宝/天猫适配** — 不从头造轮子 |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 | 全文 |
| 先方案后代码 | 通过前不写行业定制码；缺口回馈**通用平台** |
| 整体孪生 | 目标是淘宝/天猫业务世界在 AOS 可运营、可感知、可治理 |
| 模板复用 | 微商城（Niushop）8 大领域模型为基线，仅适配差异点 |
| 零行业定制码 | 平台差异通过 Connector 配置 / OT / OKF 映射消解，禁止 `taobao-*` Host 分支 |

---

## 1. 一句话目标

> 将淘宝/天猫店铺（商品 · 订单 · 会员 · 支付 · 物流 · 营销 · 店铺 · 评价）
> **整体映射**为 AOS 数字孪生，**复用**微商城（Niushop）已验证的 8 大领域模型，
> 仅针对阿里开放平台（TOP）的 **API 网关接入模式** 做适配层。

```text
微商城（已打透）              淘宝/天猫（待适配）
────────────────              ────────────────
JDBC 直连 MySQL ✅            REST API 网关 🔄 需要新的 Connector 类型
302 张表单表 Sync ✅          API 分页 + 限流 🔄 需要新调度策略
site_id 多租户 ✅             app_key + access_token 🔄 OAuth 2.0 Token 管理
商品/订单/会员/... 8 域 ✅    同样 8 域，字段更丰富 🔄 模型增强
Funnel 四阶段 Pipeline ✅     API → Dataset → OT → Workshop ✅ 可复用
```

---

## 2. 淘宝/天猫平台画像

### 2.1 平台关系

```
淘宝开放平台（TOP）
├── 淘宝 C 店（taobao.* API）
│   └── 个人/企业卖家，类目更广，商品管理用 taobao.item.*
└── 天猫品牌店（tmall.* API）
    └── 企业品牌旗舰店，Schema 体系（XML 规范），商品管理用 tmall.item.schema.*
    └── 共用：订单（taobao.trades.*）、物流（taobao.logistics.*）、
            会员（taobao.crm.*）、店铺（taobao.shop.*）
```

| 维度 | 淘宝 C 店 | 天猫品牌店 |
|------|----------|-----------|
| 商品发布 | `taobao.item.add` / `taobao.item.update` | `tmall.item.schema.add`（XML 规范） |
| 商品查询 | `taobao.item.get` | **共用** |
| 商品搜索 | `taobao.items.search` | **共用** |
| SKU 管理 | `taobao.item.sku.*` | **共用** |
| 订单查询 | `taobao.trades.sold.get` | **共用** |
| 订单详情 | `taobao.trade.fullinfo.get` | **共用** |
| 物流 | `taobao.logistics.*` | **共用**（菜鸟统一） |
| 会员 | `taobao.crm.*` | **共用** |
| 店铺信息 | `taobao.shop.get` | **共用** |
| 类目 | `taobao.itemcats.get` / `taobao.itemprops.get` | **共用** |
| **差异面** | 无 Schema，field-level API | Schema 体系（XML 模板化） |
| **差异面** | C 店风控简单 | 品牌资质 + 行业管控 |

**结论：** 淘宝和天猫在 AOS 对接方案中完全可以合并。差异只出现在「商品写回」这一个环节（天猫需要 Schema XML 构建），读操作（同步到 AOS）完全一致。

### 2.2 TOP 平台技术架构

```
AOS Platform                    淘宝开放平台（TOP）
───────────                    ──────────────────

┌──────────────┐               ┌─────────────────────┐
│  REST API    │─── HTTP ───▶  │ gw.api.taobao.com   │
│  Connector   │    POST       │ (统一网关)           │
│  (新增类型)   │               │                     │
└──────────────┘               │  AppKey + Sign 验证  │
                               │  OAuth 2.0 Session   │
                               │  限流 (500次/秒)     │
                               │  分页 (page_no)      │
                               └──────────┬──────────┘
                                          │
                               ┌──────────▼──────────┐
                               │  淘宝业务系统         │
                               │  ├ 商品库 (亿级SPU)   │
                               │  ├ 订单库            │
                               │  ├ 会员库            │
                               │  └ 物流平台(菜鸟)    │
                               └─────────────────────┘
```

| 项 | 内容 |
|----|------|
| 网关地址 | `https://gw.api.taobao.com/router/rest` |
| 协议 | HTTP POST（JSON/XML） |
| 认证 | AppKey + AppSecret + HMAC-SHA256 签名 + OAuth 2.0 Access Token |
| Token 有效期 | 24 小时（refresh_token 续期最长 30 天） |
| 限流 | ~500 次/秒（企业应用），~50 次/秒（个人应用） |
| 分页 | `page_no` + `page_size`（单次最大 200 条） |
| 沙箱 | `https://gw.api.tbsandbox.com/router/rest` |
| 官方 SDK | Python / Java / PHP / .NET / Node.js |

### 2.3 API 接口概览（与 AOS 对接相关）

| 业务域 | 核心接口 | TOP 接口名 | AOS 对应环节 |
|--------|---------|-----------|-------------|
| 商品 | 商品列表 | `taobao.items.onsale.get` | Source Sync |
| 商品 | 商品详情 | `taobao.item.get` | Source Sync |
| 商品 | SKU 详情 | `taobao.item.sku.get` | Source Sync |
| 订单 | 已售订单 | `taobao.trades.sold.get` | Source Sync |
| 订单 | 订单详情 | `taobao.trade.fullinfo.get` | Source Sync → OT |
| 物流 | 物流单号 | `taobao.logistics.orders.get` | Source Sync |
| 物流 | 物流轨迹 | `taobao.logistics.trace.search` | 实时查询（不落 Dataset） |
| 会员 | 会员信息 | `taobao.crm.members.get` | Source Sync（需增值权限） |
| 店铺 | 店铺信息 | `taobao.shop.get` | Source Sync（一次性） |
| 类目 | 标准类目 | `taobao.itemcats.get` | 配置参考 |
| 商品 | Schema 规则（天猫） | `tmall.item.add.schema.get` | 写回 Action（天猫专属） |
| 商品 | 商品发布（天猫） | `tmall.item.schema.add` | 写回 Action（天猫专属） |
| 商品 | 商品发布（淘宝） | `taobao.item.add` | 写回 Action（淘宝专属） |

---

## 3. 数据模型对照（淘宝/天猫 vs Niushop 微商城）— 字段级 · 已完成

> **复用策略：** Niushop 8 大领域模型为 AOS Ontology 基线，淘宝适配时在以下维度做增强。
> **状态**：✅ P0 完成 · 8 域字段级差异对照已完整填充

### 3.1 商品域（8 维度 × 字段级对照）

#### 3.1.1 基础标识

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `goods_id` | int(11) | `num_iid` | bigint(20) | ID 类型不同；淘宝为字符串形数字 | OT 统一 `String`，`goods_id` 加前缀 `niushop_` |
| `sku_id` | int(11) | `sku_id` | bigint(20) | 同上 | 同上，SKU Object 的 `external_id` 映射 |
| `goods_name` | varchar(255) | `title` | varchar(60) | Niushop 允许更长标题 | 直接用淘宝字段映射，截断告警 |
| `goods_code` | varchar(50) | `outer_id` | varchar(40) | 商家编码，语义相同 | 直接映射 |
| `goods_class` | int(11) | `cid` | bigint(20) | Niushop 自建类目 vs 淘宝统一类目树 | 需建立 `category_map` 表 |

#### 3.1.2 价格与库存

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `price` | decimal(10,2) | `price` | decimal(10,2) | 完全兼容 | 直接映射 |
| `market_price` | decimal(10,2) | `item_imgs.price` | — | 淘宝无"市场价"概念 | 使用 `reserve_price`（一口价原价）替代 |
| `cost_price` | decimal(10,2) | — | — | 淘宝不暴露成本价 | 弃用 |
| `stock` | int(11) | `num` | int(11) | 语义相同 | 直接映射 |
| `sku.stock` | int(11) | `sku.quantity` | int(11) | 语义相同 | 直接映射 |
| `min_buy` | int(11) | — | — | 淘宝无最小起购量概念 | 弃用或设默认值 1 |

#### 3.1.3 商品属性

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `goods_attr` | JSON自由KV | `props` + `props_name` | JSON(pid:vid) + 文本 | Niushop 自由 vs 淘宝规范（类目约束） | `props` 解析为 `{pid_value: vid_value}` 数组 |
| `brand_id` | int(11)（可选） | `brand_id` | bigint(20) | 淘宝品牌体系更完整（>50万品牌） | 映射到独立 Brand Object Type |
| `category_id` | int(11)（自建） | `cid` | bigint(20)（淘宝类目树 >20,000 节点） | 类目体系完全不同，尼ushop 为扁平自建 | 建 `category_map` 配置表映射 CID→AOS 类目 |
| `goods_unit` | varchar(20) | — | — | 淘宝无独立单位字段 | 作为商品 Prop 保留 |
| `introduction` | varchar(255) | `subtitle` | varchar(255) | 商品卖点/子标题 | 直接映射 |

#### 3.1.4 图片体系

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `pic_url` | varchar(500) | `pic_url` | varchar(500) | 主图 1:1 映射 | 直接映射 |
| — | — | `item_imgs` | JSON 数组（最多 5 张） | Niushop 无多主图概念 | OT 新增 `main_images` Prop（string[]） |
| `goods_gallery` | 多详情图 | `desc_imgs` | 多详情图 | 结构相似 | 新增 `detail_images` Prop（string[]） |
| — | — | `sku_imgs` | JSON 数组 | Niushop 无 SKU 维度图片 | OT SKU Object 新增 `sku_image` Prop |
| `video_url` | varchar(500)（如有） | `video` | JSON Object | 淘宝有完整商品短视频字段 | MediaReference 映射 |

#### 3.1.5 上下架与状态

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `status` | tinyint(1) 1/0 | `approve_status` | string | 淘宝：`onsale` / `instock` | 枚举映射：`1 → onsale`, `0 → instock` |
| — | — | `list_time` | datetime | 上架时间 | OT 新增 `listed_at` Prop |
| — | — | `delist_time` | datetime | 下架时间 | OT 新增 `delisted_at` Prop |
| — | — | `created` | datetime | 商品创建时间 | OT 新增 `created_at` Prop（系统时间） |
| `is_free_shipping` | tinyint(1) | — | — | 淘宝通过运费模板控制 | 通过运费模板间接获取 |

#### 3.1.6 销量与评价统计

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `sale_num` | int(11)（自维护） | `sold_quantity` | int(11) | 淘宝有官方销量（30天+累计） | 新增 `sold_quantity_30d` Prop |
| — | — | `total_sold_quantity` | int(11) | 淘宝累计销量 | 新增 `sold_quantity_total` Prop |
| `evaluate` | int(11)（自维护） | `has_discount` | bool | — | 从 `traderates.get` 统计评价数 |
| `collects` | int(11)（自维护） | `favcount` | int(11) | 收藏数 | 新增 `favorite_count` Prop |

#### 3.1.7 运费

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `shipping_fee` | decimal(10,2) | — | — | 淘宝通过运费模板控制 | 调用 `taobao.delivery.templates.get` 获取模板 |
| `shipping_template_id` | int(11) | `delivery_template_id` | bigint(20) | 模板体系不同 | 新增 `delivery_template_id` Prop |

#### 3.1.8 天猫特有字段

| 字段 | 类型 | 来源 | 说明 | OT 映射 |
|------|------|------|------|--------|
| `product_id` | bigint | `tmall.product.schema.match` | 天猫商品需挂靠产品 | 新增 `tmall_product_id` Prop |
| `brand_id` | bigint | `taobao.itemcats.authorize.get` | 天猫强制品牌绑定 | 关联 Brand Object |
| Schema XML | text | `tmall.item.add.schema.get` | 发布规则动态下发 | 不存储，运行时获取 |
| `vertical_image` | string | Schema 增量更新 | 天猫竖图 | 新增 `vertical_image` Prop |

---

### 3.2 订单域（8 维度 × 字段级对照）

#### 3.2.1 基础标识与时间

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `order_no` | varchar(255) | `tid` | bigint(20) | Niushop 字符串 vs 淘宝全局唯一长整型 | OT 统一 `String`，加前缀区分来源 |
| `order_id` | int(11)（自增 PK） | — | — | 淘宝用 `tid` 同时作为业务标识 | `order_id` 仅内部使用，不暴露 |
| `site_id` | int(11) | — | — | 淘宝用 `seller_nick` 区分店铺 | OT Shop Object 关联 |
| `create_time` | int(11) | `created` | datetime | 时间戳 vs 标准时间 | OT 统一 `datetime` |
| `pay_time` | int(11) | `pay_time` | datetime | 同上 | 同上 |
| `consign_time` | int(11) | `consign_time` | datetime | 发货时间 | 同上 |
| `finish_time` | int(11) | `end_time` | datetime | 交易结束时间 | 同上 |
| — | — | `modified` | datetime | 淘宝增量同步关键字段 | 新增 `last_modified` Prop |

#### 3.2.2 订单状态机

| Niushop 状态 | 淘宝状态 | 映射 | 说明 |
|------------|---------|------|------|
| `0` 待付款 | `WAIT_BUYER_PAY` | → `pending_payment` | |
| `1` 待发货 | `WAIT_SELLER_SEND_GOODS` | → `pending_shipment` | |
| `2` 已发货 | `WAIT_BUYER_CONFIRM_GOODS` | → `shipped` | |
| `3` 已收货 | `TRADE_BUYER_SIGNED` | → `delivered` | |
| `4` 已完成 | `TRADE_FINISHED` | → `completed` | |
| — | `TRADE_CLOSED` | → `closed` | 淘宝独有：交易关闭 |
| — | `TRADE_CLOSED_BY_TAOBAO` | → `closed_by_platform` | 淘宝独有：平台关闭 |
| — | `PAY_PENDING` | → `payment_pending` | 淘宝独有：支付中 |

**退款子状态**（淘宝独有，可嵌入订单）：

| 退款状态 | 值 | OT 映射 |
|---------|-----|--------|
| `NO_REFUND` | 无退款 | `refund_status: none` |
| `WAIT_SELLER_AGREE` | 等待卖家同意 | `refund_status: pending` |
| `REFUND_SUCCESS` | 退款成功 | `refund_status: completed` |
| `REFUND_CLOSED` | 退款关闭 | `refund_status: closed` |

#### 3.2.3 买家信息

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `member_id` | int(11) | `buyer_open_uid` | string | 淘宝脱敏 ID | OT Link → Member Object |
| `buyer_nick` | varchar(50)（买家昵称） | `buyer_nick`（从订单） | string | 来源不同但语义相同 | 直接映射到 Member.buyer_nick |
| — | — | `buyer_alipay_no` | string | 支付宝账号（需权限） | 不采集（隐私） |
| `buyer_message` | text | `buyer_message` | text | 买家留言 | 直接映射 |

#### 3.2.4 收货地址

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `receiver_name` | varchar(50) | `receiver_name` | string | 完全一致 | 直接映射 |
| `receiver_mobile` | varchar(20) | `receiver_mobile` | string | 完全一致 | 直接映射 |
| `receiver_phone` | varchar(20) | `receiver_phone` | string | 完全一致 | 直接映射 |
| `receiver_province` | int(11) | `receiver_state` | string（中文名） | 淘宝返回中文名非编码 | OT 统一为中文 province/city/district |
| `receiver_city` | int(11) | `receiver_city` | string（中文名） | 同上 |
| `receiver_district` | int(11) | `receiver_district` | string（中文名） | 同上 |
| `receiver_address` | varchar(255) | `receiver_address` | string | 完全一致 | 直接映射 |
| `receiver_zip` | varchar(6) | `receiver_zip` | string | 完全一致 | 直接映射 |

#### 3.2.5 金额与支付

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `order_money` | decimal(10,2) | `payment` | decimal(10,2) | 实付金额 | 直接映射 |
| `goods_money` | decimal(10,2) | `total_fee` | decimal(10,2) | 商品总价（不含邮费） | 新增 `goods_total` Prop |
| `pay_money` | decimal(10,2) | `payment` | decimal(10,2) | 淘宝将实付放在 `payment` | 直接映射 |
| `coupon_money` | decimal(10,2) | `discount_fee` | decimal(10,2) | 折扣总额 | 新增 `discount_fee` Prop |
| `shipping_money` | decimal(10,2) | `post_fee` | decimal(10,2) | 邮费 | 直接映射 |
| `point` | int(11) | `point_fee` | decimal(10,2) | 淘宝为积分抵扣金额 | 映射为 `point_fee` Prop |
| — | — | `received_payment` | decimal(10,2) | 卖家实收（含平台优惠） | 新增 `seller_received` Prop |
| — | — | `commission_fee` | decimal(10,2) | 平台佣金（如有） | 新增 `commission_fee` Prop |
| — | — | `alipay_no` | string | 支付宝交易号 | 新增 `alipay_transaction_id` Prop |

#### 3.2.6 订单明细行（SKU 行）

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `order_goods.goods_id` | int(11) | `orders[].num_iid` | bigint | 直接外键 vs 嵌入数组 | OT Link → Product Object |
| `order_goods.sku_id` | int(11) | `orders[].sku_id` | bigint | 同上 | OT Link → SKU Object |
| `order_goods.price` | decimal(10,2) | `orders[].price` | decimal(10,2) | 单价 | 直接映射 |
| `order_goods.num` | int(11) | `orders[].num` | int(11) | 数量 | 直接映射 |
| `order_goods.goods_money` | decimal(10,2) | `orders[].total_fee` | decimal(10,2) | 小计 | 新增 `line_total` Prop |
| `order_goods.goods_name` | varchar(255) | `orders[].title` | string | 商品名称 | 直接映射 |
| `order_goods.sku_name` | varchar(255) | `orders[].sku_properties_name` | string | SKU 规格描述 | 直接映射 |
| — | — | `orders[].oid` | bigint | 淘宝子订单号 | 新增 `oid` Prop（子订单号唯一标识） |
| — | — | `orders[].pic_path` | string | SKU 图片 | 新增 `sku_image` Prop |
| — | — | `orders[].refund_status` | string | 子订单退款状态 | 新增 `refund_status` Prop |

#### 3.2.7 优惠层级（淘宝独有）

| 层级 | 字段 | 说明 | OT 映射 |
|------|------|------|--------|
| 平台优惠 | `discount_fee`（含平台） | 淘宝/天猫平台的满减、补贴 | `platform_discount` Prop |
| 店铺优惠 | `seller_discount` | 店铺自己的优惠券/活动 | `shop_discount` Prop |
| 单品优惠 | `orders[].discount_fee` | 单个 SKU 的折扣 | `line_discount` Prop |
| 积分抵扣 | `point_fee` | 积分抵扣金额 | `point_deduction` Prop |

#### 3.2.8 物流（嵌入订单）

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `delivery_type` | varchar(50) | `shipping_type` | string | 发货方式 | 枚举映射 |
| `express_no` | varchar(50) | `out_sid` | string | 运单号 | 链接 Logistics Object |
| `express_company` | int(11) | `company_code` | string | 快递公司编码（菜鸟标准） | OT 统一使用 `company_code` |

---

### 3.3 会员域（4 维度 × 字段级对照）

#### 3.3.1 基础标识

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `member_id` | int(11) | `buyer_open_uid` | string | 淘宝脱敏 UID，不暴露原始 ID | OT 主键 `external_id` = `buyer_open_uid` |
| `nickname` | varchar(50) | `buyer_nick` | string | 语义相同 | 直接映射 |
| `mobile` | varchar(20) | — | — | **淘宝不可获取**（隐私保护） | ❌ 不建 `mobile` Prop |
| `email` | varchar(50) | — | — | 淘宝不返回 | ❌ 弃用 |
| `avatar` | varchar(255) | `avatar` | string | 用户头像 URL | 直接映射 |

#### 3.3.2 等级体系

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `member_level` | int(11)（自建 0-9） | `grade`（T1-T6） | int | 等级体系完全不同 | 映射为通用 `member_tier` Prop（枚举：T1~T6） |
| — | — | `tmall_grade`（天猫专属） | int | 天猫独立会员等级 | 新增 `tmall_member_tier` Prop |
| — | — | `trade_amount` | decimal | 累计消费额（CRM接口） | 新增 `total_spend` Prop |
| — | — | `trade_count` | int | 累计交易次数（CRM接口） | 新增 `total_orders` Prop |
| — | — | `item_num` | int | 累计购买商品数（CRM接口） | 新增 `total_items` Prop |

#### 3.3.3 会员标签与权益

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `member_label` | varchar(255)（自建） | `tag`（CRM 接口） | string[] | 需 CRM 增值权限 | 增值接口独立 Source Sync |
| `point` | int(11)（自建积分） | — | — | 淘宝积分在买家侧 | 不采集 |
| — | — | `close_trade_count` | int | 近 3 月完成交易数 | 新增 `recent_trade_count` Prop |
| — | — | `group_ids` | string | 会员分组（CRM 增值） | 新增 `crm_groups` Prop |

#### 3.3.4 收货地址（差异巨大）

| 维度 | Niushop | 淘宝/天猫 | AOS 处理 |
|------|---------|----------|---------|
| 地址存储 | `member_address` 独立表，可多条 | 无独立地址簿 API | 不建地址 Object |
| 地址获取 | 会员维度读取 | 仅订单内 `receiver_*` 返回 | 地址作为订单 Prop，不绑定会员 |
| 地址修改 | 会员自行管理 | 淘宝内修改，不通过 API 暴露 | 不可在 AOS 中管理地址 |

---

### 3.4 支付域（字段级对照）

| Niushop 字段 (`pay`) | 类型 | 淘宝/天猫字段（嵌入 trade） | 类型 | 差异 | OT 映射 |
|---------------------|------|---------------------------|------|------|--------|
| `out_trade_no` | varchar(50) | `tid` | bigint | Niushop 用支付流水号，淘宝用订单号 | OT 中 `payment_ref` = `alipay_no` |
| `pay_money` | decimal(10,2) | `payment` | decimal(10,2) | 实付金额 | 订单 Prop：`amount_paid` |
| `pay_type` | varchar(10) | — | — | Niushop 微信，淘宝支付宝 | 订单 Prop：`payment_channel` (alipay/wechat) |
| `pay_status` | tinyint | `status` | string | 状态体系不同 | 订单 Prop 子状态 |
| `pay_time` | int(11) | `pay_time` | datetime | 格式差异 | 订单 Prop：`paid_at` |
| — | — | `alipay_no` | string | 支付宝交易流水号 | 订单 Prop：`alipay_transaction_id` |
| — | — | `alipay_url` | string | 支付宝收银台 URL | 不采集 |
| — | — | `commission_fee` | decimal | 平台佣金 | 后置 Phase 2 |

**模型差异总结**：
- Niushop：`order` ↔ `pay` = 1:1 独立表关系
- 淘宝：支付信息嵌入 `trade.fullinfo.get` 响应，与订单平级
- AOS：支付不建独立 Object Type，作为订单的 `payment_*` 属性组

---

### 3.5 物流域（字段级对照）

| Niushop 字段 (`express`) | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------------------|------|-------------|------|------|--------|
| `company_id` | int(11) | `company_code` | string | Niushop 自维护 ID vs 菜鸟标准编码 | OT 统一使用 `company_code`（菜鸟标准） |
| `company_name` | varchar(100) | `company_name` | string | 快递公司名称 | 直接映射 |
| `tracking_no` | varchar(50) | `out_sid` | string | 运单号 | 直接映射 → `tracking_number` |
| `status` | tinyint(1) | `status` | string | Niushop 简单状态 vs 淘宝物流状态码 | OT 枚举扩展 |
| `trace_data` | — (无) | `transit_step_info[]` | JSON Array | 轨迹节点 | **实时 API 查询**，不落 Dataset |
| `send_time` | int(11) | `consign_time` | datetime | 发货时间 | 直接映射 |
| `sign_time` | int(11) | — | — | 淘宝轨迹接口返回签收状态 | 从轨迹节点解析最后一站 |

**物流轨迹处理策略**：
- 轨迹是**实时性数据**（时效性高、数据量大），不适合 Source Sync 全量拉取
- 设计为 AOS Function：用户点击 "查物流" 时实时调用 `taobao.logistics.trace.search`
- 落地的 `logistics_status` 只在订单同步时拉取当前简略状态

---

### 3.6 店铺域（字段级对照）

| Niushop 字段 | 类型 | 淘宝/天猫字段 | 类型 | 差异 | OT 映射 |
|-------------|------|-------------|------|------|--------|
| `site_id` | int(11) | `shop_id` | bigint | Niushop 多租户隔离的主键 | OT Shop Object.`external_id` |
| `site_name` | varchar(255) | `shop_title` | string | 店铺名称 | 直接映射 → `shop_name` |
| — | — | `seller_nick` | string | 卖家昵称（用于 API 调用身份） | 新增 `seller_nick` Prop |
| — | — | `shop_type` | enum(C/B/tmall) | 店铺类型 | 新增 `shop_type` Prop |
| `logo` | varchar(255) | `pic_path` | string | 店铺 Logo URL | 直接映射 |
| `desc` | text | `bulletin` | string | 店铺介绍/公告 | 直接映射 |
| — | — | `shop_score.item_score` | decimal | 宝贝描述评分 | 新增 `dsr_item_score` Prop |
| — | — | `shop_score.service_score` | decimal | 卖家服务评分 | 新增 `dsr_service_score` Prop |
| — | — | `shop_score.delivery_score` | decimal | 物流服务评分 | 新增 `dsr_delivery_score` Prop |
| `shop_status` | tinyint(1) | — | — | Niushop 开店/关店状态 | 根据淘宝 API 返回判断，新增 `is_active` Prop |
| — | — | `created` | datetime | 开店时间 | 新增 `created_at` Prop |

---

### 3.7 营销域（后置 · Phase 2）

> **状态**：🟡 框架级对照，字段级在 Phase 2 补充。淘宝营销体系极复杂（30+ 营销工具 × 多层级活动）。

| 维度 | Niushop | 淘宝/天猫 | Phase 1 | Phase 2 字段级 |
|------|---------|----------|---------|---------------|
| 优惠券 | `ns_promotion_coupon` 自建 | `taobao.promotion.coupon.*` | ❌ 不采集 | `coupon_id` / `denominations` / `start_time` / `end_time` / `user_type` |
| 满减 | 自建促销规则 | 平台级 + 店铺级 | ❌ 不采集 | `promotion_id` / `threshold` / `discount` / `participating_items` |
| 活动 | 自建 | 聚划算/百亿补贴/618/双11 | ❌ 不采集 | 后置 |
| 直播 | 无 | 淘宝直播 API | ❌ 不采集 | 后置 |

---

### 3.8 评价 / 内容域（字段级对照）

| Niushop 字段 | 类型 | 淘宝/天猫字段（`traderates.get`） | 类型 | 差异 | OT 映射 |
|-------------|------|--------------------------------|------|------|--------|
| — | — | `tid` | bigint | 订单号 | Review Object.`order_id` |
| — | — | `oid` | bigint | 子订单号 | Review Object.`order_line_id` |
| — | — | `nick` | string | 评价人昵称 | Review Object.`reviewer_nick` |
| — | — | `role` | string (buyer/seller) | 评价角色 | Review Object.`reviewer_role` |
| — | — | `result` | string (good/neutral/bad) | 好评/中评/差评 | Review Object.`rating` (enum) |
| — | — | `content` | string | 评价内容 | Review Object.`content` |
| — | — | `reply` | string | 卖家回复 | Review Object.`seller_reply` |
| — | — | `created` | datetime | 评价时间 | Review Object.`created_at` |
| — | — | `item_title` | string | 商品标题 | Review Object Link → Product |
| — | — | `item_price` | decimal | 商品价格 | Review Object.`item_price_at_purchase` |
| — | — | `num_iid` | bigint | 商品 ID | Review Object Link → Product |
| — | — | `valid_score` | bool (天猫) | 是否计入评分 | （天猫专属）Review Object.`score_valid` |

---

### 3.9 跨域总结：Niushop → 淘宝差异矩阵

| 域 | 直接复用度 | 关键差异点 | Phase 1 交付 |
|----|----------|----------|------------|
| 商品 | 70% | 类目体系、图片分层、天猫 Schema、属性规范 | 商品 Object + SKU Object + 图片组 |
| 订单 | 75% | 状态机复杂度、优惠层级、支付嵌入 | 订单 Object + 状态枚举 + 优惠 Prop 组 |
| 会员 | 50% | 隐私脱敏 ID、无手机号、无地址簿 | 会员 Object（精简版） |
| 支付 | 40% | 模型差异（独立 vs 嵌入） | 作为订单 Prop，不建独立 Object |
| 物流 | 60% | 菜鸟标准编码、实时轨迹 | 物流 Object + 实时查询 Function |
| 店铺 | 70% | DSR 三项评分、店铺类型 | 店铺 Object + 评分 Prop |
| 营销 | 10% | 体系极复杂 | Phase 2 后置 |
| 评价 | 0%（Niushop 无） | 淘宝独有 | 评价 Object Type（新增） |

---

## 4. AOS 对接路径（分 4 个子阶段）

> **前提：** 微商城（Niushop）全链路已跑通，产出「电商孪生标准模板」。

### 4.1 子阶段 A：分析准备（✅ P0/P1 已完成）

| 步骤 | 内容 | 产出 | 状态 |
|------|------|------|------|
| A1 | 调研 TOP API 接口清单（200+ → 37 核心接口） | `01-TOP-API接口清单.md` | ✅ 已完成 |
| A2 | 调研 Schema 体系（天猫商品发布专属） | `02-天猫Schema体系分析.md` | ✅ 已完成 |
| A3 | 注册开发者账号 + 创建自用型应用 + 沙箱测试 | `.env` + API Key 配置 | ⏸ 待平台就绪（需企业认证） |
| A4 | 对照微商城 8 域模型，标记淘宝/天猫的字段级差异 | 本文 §3 | ✅ 已完成（v1.1 字段级完整对照） |

### 4.2 子阶段 B：数据接入（依赖 220plan Phase 2）

> **前置：** 220plan W1-5（Funnel 四阶段管道）+ W1-8（Transform 算子库）完成

| 步骤 | 内容 | 产出 | 平台需求 |
|------|------|------|---------|
| B1 | 实现「REST API Connector」类型（新增，区别于现有 JDBC Connector） | 平台代码 | **回馈通用平台** |
| B2 | 实现 OAuth 2.0 Token Manager（自动续期 + 刷新） | 平台代码 | **回馈通用平台** |
| B3 | 对接 TOP API → 商品 Source Sync | 淘宝商品 Dataset | — |
| B4 | 对接 TOP API → 订单 Source Sync（含分页 + 限流） | 淘宝订单 Dataset | — |
| B5 | 对接 TOP API → 物流/会员/店铺 Source Sync | 淘宝物流/会员/店铺 Dataset | — |
| B6 | 基于微商城模板，建立淘宝 8 域 Ontology（Object + Link） | OT 定义文件 | — |

### 4.3 子阶段 C：孪生可视化（依赖 220plan Phase 3）

> **前置：** 220plan W1-6（Action 写回） + W1-7（壳核模式）完成

| 步骤 | 内容 | 产出 |
|------|------|------|
| C1 | Workshop 态势大屏：店铺概览仪表盘 | 店铺 Dashboard |
| C2 | Workshop 运营台：商品管理 + 库存监控 | 运营台页面 |
| C3 | Workshop 告警 Inbox：差评/库存预警/物流异常 | 告警规则 |
| C4 | OKF Funnel 编辑器：商品 → 订单 Join 映射 | 电商 Funnel 模板 |

### 4.4 子阶段 D：写回闭环（依赖 220plan Phase 4+）

> **前置：** 220plan W1-2（Logic 编排）完成

| 步骤 | 内容 | 产出 | 备注 |
|------|------|------|------|
| D1 | Action 写回：商品改价/上下架 → TOP API | 商品 Action | 天猫需 Schema XML 构建 |
| D2 | Action 写回：订单备注/发货 → TOP API | 订单 Action | — |
| D3 | AIP Logic：自动差评预警 → 通知商家 | Logic 编排模板 | — |
| D4 | 天猫 Schema 自动构建（Funnel → Schema XML） | 天猫专属能力 | 可选推进 |

---

## 5. 平台能力缺口（需回馈通用平台）

基于淘宝/天猫接入过程将暴露以下通用平台缺口：

| # | 缺口 | 优先级 | 可复用性 | 说明 |
|----|------|-------|---------|------|
| G1 | **REST API Connector 类型** | 🔴 W1 | 全部 8 平台 | 现有 JDBC Connector 不支持 API 源，需新增通用 REST Connector（含 Auth/OAuth 子类型） |
| G2 | **OAuth 2.0 Token Manager** | 🔴 W1 | Shopfiy/Amazon/抖音 | 通用 Token 生命周期管理（自动续期/刷新/过期告警） |
| G3 | **API 分页 + 限流策略** | 🟡 W2 | 全部 API 平台 | Source Sync 需支持游标分页 + 速率控制 |
| G4 | **多源异构 Join（API + JDBC）** | 🟡 W2 | 京东/拼多多 | 不同 Connector 类型的 Dataset Join |
| G5 | **类目 Map 配置** | 🟢 W2 | 全部电商 | 不同平台类目体系映射到统一 AOS 类目树 |
| G6 | **定时 Sync Schedule** | 🟡 W1 | 全部平台 | 现有 Schedule 为 demo 壳，需真调度（API 源按间隔拉取） |

---

## 6. 与微商城模板的复用清单

以下模型/配置可直接从微商城（Niushop）模板复用：

| 复用项 | 复用度 | 说明 |
|-------|-------|------|
| 8 域 Ontology 对象类型（Object Type） | 90% | 商品/订单/会员/支付/物流 Object Type 结构直接复用，仅增字段 |
| Link 类型定义 | 85% | 会员→订单、商品→SKU 等 Link 直接复用 |
| Workshop 态势大屏布局 | 70% | Dashboard 卡片布局复用，数据源切换 |
| OKF 映射模板 | 60% | Funnel 映射逻辑复用，数据源 Connector 类型变更 |
| MediaSet 文件夹具 | 50% | 商品详情图/订单Excel夹具格式复用 |
| AIP Logic 模板 | 80% | 运营告警/异常检测逻辑复用 |

---

## 7. 下一步行动

| 优先级 | 行动 | 阻塞条件 | 预计产出 | 状态 |
|-------|------|---------|---------|------|
| **P0 立即** | 完成本文 §3 的 8 域字段级差异对照表 | — | 本文 §3 完善 | ✅ 已完成（v1.1） |
| **P1 本周** | 调研 TOP API 全量接口清单（200+ → 筛选 37 核心） | — | `01-TOP-API接口清单.md` | ✅ 已完成 |
| **P1 本周** | 天猫 Schema 体系分析（XML 模板结构） | — | `02-天猫Schema体系分析.md` | ✅ 已完成 |
| **P2 待平台就绪** | REST API Connector 设计文档 | 220plan W2+ REST Connector 开发 | 平台设计文档 | ⬜ 待执行 |
| **P2 待平台就绪** | 淘宝沙箱数据接入验证 | 220plan Phase 2 完成 + 企业开发者账号 | Demo 跑通 | ⬜ 待执行 |
| **P2 待平台就绪** | 注册开发者账号 + 创建自用型应用 | 淘宝企业认证 | `.env` + API Key | ⏸ 暂停 |

## 8. OpenAPI 限制与应对策略

> **新增日期**：2026-07-31 · v1.2
> **背景**：第一步"后台数据接入"（子阶段 B）直接依赖 TOP OpenAPI，存在多层限制需提前规划应对

### 8.1 应用类型选择决策

| 应用类型 | 认证要求 | QPS 上限 | API 可用范围 | 适用场景 | AOS 推荐 |
|---------|---------|---------|-------------|---------|---------|
| 个人开发者 | 实名认证（身份证 + 人脸） | ≤10 次/分钟 | 仅基础商品查询 | 开发调试 | ❌ 不可用于生产 |
| **自用型** | 企业认证 | 500 次/秒 | 大部分 API（仅接入自有店铺） | AOS 接入自有店铺 | ✅ **首选** |
| 定制型 | 企业认证 + 上架审核 | 500 次/秒 | 需逐个申请权限包 | 给特定商家使用 | 后续扩展 |
| 工具型 | 企业认证 + 服务市场审核 | 500 次/秒 | 需审核 | 多商家 SaaS | 远期 |

**决策结论**：AOS 首期选择**自用型应用**（企业认证），仅接入自有店铺数据。若后续需给其他商家使用，须重新注册为定制型/工具型应用并重新申请权限包。

### 8.2 权限包申请清单与审批周期

> 37 接口完整权限包矩阵详见 [01-TOP-API接口清单 §7](./01-TOP-API接口清单.md#7-openapi-限制详情)

核心阻塞点：

| 接口 | 权限级别 | 审批周期 | 阻塞影响 |
|------|---------|---------|---------|
| `taobao.trade.fullinfo.get` | 企业账号 + 业务场景说明 | **3-7 个工作日** | 订单详情含收货地址，无此接口订单域不完整 |
| `taobao.crm.members.get` | CRM 增值包（**需购买**） | 购买后即时 | 会员等级/消费额数据，不购买则会员域不可用 |
| `tmall.item.schema.*`（6 个） | 天猫店铺授权 | 1-3 个工作日 | 天猫商品写回，Phase 1 读操作不受影响 |

**策略**：应用创建后**立即并行申请所有权限包**，不等审批完才开始开发。Connector 开发与权限审批可并行推进。

### 8.3 日调用配额与全量拉取分批策略

**两层限制**：

| 限制类型 | 说明 | 超限行为 | 可否重试 |
|---------|------|---------|---------|
| **QPS 限制**（500 次/秒） | 瞬时速率 | 返回 `isp.traffic-limit` | ✅ 指数退避重试 |
| **日调用配额** | 每日总量，按 API 分类 | 返回 `isp.ratelimit-exceed` | ❌ 直接拒绝 |

| 数据域 | 数据量级 | 单次返回 | 日配额估算 | 分批策略 | 断点续传字段 |
|--------|---------|---------|----------|---------|------------|
| 商品 | 万级 SKU | 200 条/页 | ~10 万次/日 | `page_no` 分页，每批 200 条，间隔 200ms | `last_page_no` |
| 订单 | 千-万级/日 | 100 条/页 | ~5 万次/日 | 时间窗口分批（每 15 分钟增量，每批 1 小时数据） | `last_modified` |
| 会员 | 千-万级 | 100 条/页 | CRM 独立配额 | 每 1 小时全量分页 | `last_page_no` |
| 物流轨迹 | 实时 | 单条 | 不落 Dataset | On-Demand 调用 | — |

### 8.4 沙箱能力边界

| 能力 | 沙箱环境 | 生产环境 |
|------|---------|---------|
| QPS | 50 次/秒 | 500 次/秒 |
| 数据量 | 极少（几条测试数据） | 全量 |
| OAuth 连通性 | ✅ 可验证 | ✅ |
| 签名正确性 | ✅ 可验证 | ✅ |
| `taobao.item.get` | ✅ 可用 | ✅ |
| `taobao.items.onsale.get` | ✅ 可用（数据少） | ✅ |
| `taobao.trades.sold.get` | ✅ 可用（数据少） | ✅ |
| `taobao.trade.fullinfo.get` | ❌ **不可用** | 需企业权限 |
| `taobao.crm.members.get` | ❌ **不可用** | 需增值包 |
| `tmall.item.schema.*` | ❌ **不可用** | 需天猫授权 |

**结论**：沙箱仅用于验证 OAuth 连通性 + 签名正确性 + 基础商品/订单列表拉取。`trade.fullinfo.get` 和 CRM 接口只能在生产环境验证。沙箱覆盖率仅 **46%**（17/37 接口可用），详见 [01-API清单 §7.3](./01-TOP-API接口清单.md#73-沙箱能力边界清单)。

---

> **版本**：v1.2 · 2026-07-31 · P0/P1 已完成 + §8 OpenAPI 限制
>
> **变更日志**：
>
> | 版本 | 日期 | 说明 |
> | --- | --- | --- |
> | v1.2 | 2026-07-31 | 新增 §8 OpenAPI 限制与应对策略（应用类型决策/权限包审批/日配额分批/沙箱边界）· 三文件 Sources 补齐 |
> | v1.1 | 2026-07-22 | P0/P1 完成 · §3 8 域字段级完整对照（Niushop vs 淘宝字段 × OT 映射）· 新增 §3.9 跨域差异矩阵 · §4.1/§7 更新进展 |
> | v1.0 | 2026-07-22 | 初版 · 基于 TOP 开放平台调研 · 淘宝+天猫合并分析 · 8 域数据模型对照框架 · 4 子阶段对接路径 · 6 项平台缺口 |

---

## Sources

- [淘宝平台API权限申请与使用教程](https://juejin.cn/post/7463399034830864396)
- [淘宝商品详情API全解析：从合规接入到智能选品](https://juejin.cn/post/7548707467113136166)
- [淘宝天猫API接口的调用频率有限制吗?](https://m.sohu.com/a/805863866_121384343/)
- [淘宝开放平台(TOP)API 入门教程：从原理到实战](https://juejin.cn/post/7559068227641589779)
