# 抖音电商开放平台 · AOS 数字孪生对接方案

| 字段 | 内容 |
|------|------|
| 状态 | **方案仅分析 · P0 阶段** · 2026-07-22 |
| 版本 | **v1.0** · 初始方案 |
| 目录 | `docs/palantier/20_tech/抖音电商接入方案/` |
| 覆盖范围 | **抖音电商（抖店）** + **抖音生活服务** + **精选联盟（达人/团长/抖客）** |
| 开放平台 | 抖店开放平台 (op.jinritemai.com) + 抖音开放平台 (developer.open-douyin.com) |
| 关联 | 微商城模板：[00-Niushop微商城AOS对接方案](../微商城电商接入方案/00-Niushop微商城AOS对接方案.md) · [淘宝天猫方案](../淘宝电商接入方案/00-淘宝天猫AOS对接方案-总体分析计划.md) · [新电商达人增长与控价任务](../228-新电商达人增长与控价任务产品方案.md) |
| 原则 | **先微商城打透 → 模板复用 → 仅适配抖音差异点** |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 | 全文 |
| 先方案后代码 | 通过前不写行业定制码；缺口回馈**通用平台** |
| 整体孪生 | 目标是抖音电商业务世界在 AOS 可运营、可感知、可治理 |
| 模板复用 | 微商城（Niushop）8 大领域模型为基线，仅适配抖音差异点 |
| 零行业定制码 | 平台差异通过 Connector 配置 / OT / OKF 映射消解，禁止 `douyin-*` Host 分支 |

抖音精选联盟现有 Creator/Commission 建模继续保留；新增需求重点是把达人发现、去重、短名单、邀约草稿、合作跟踪和效果复盘接入统一 `AgentTask`，不另建抖音专属任务系统。

---

## 1. 一句话目标

> 将抖音电商店铺（商品 · 订单 · 物流 · 售后 · 会员 · 达人带货 · 内容 · 营销）  
> **整体映射**为 AOS 数字孪生，**复用**微商城已验证的 8 大领域模型，  
> 仅针对抖店开放平台（内容+电商融合）的 **达人带货 · 全域兴趣电商 · 抖店云** 做适配。

```text
微商城（已打透）              抖音电商（待适配）
────────────────              ────────────────
JDBC 直连 MySQL ✅            REST API 网关 🔄 需要新的 Connector 类型
302 张表单表 Sync ✅           API 分页 + 100 次取整计费 🔄 特殊的计费模型
site_id 多租户 ✅              shop_id 单店铺 🔄 OAuth 2.0 店铺授权
商品/订单/会员/... 8 域 ✅    同样 8 域 + 内容+达人体系 🔄 模型大幅增强
Funnel 四阶段 Pipeline ✅     API → Dataset → OT → Workshop ✅ 可复用
```

---

## 2. 抖音电商平台画像

### 2.1 平台矩阵

```
抖音电商开放平台生态
├── 抖店开放平台 (op.jinritemai.com) ← 核心
│   ├── 商品 /product/*：发布/查询/编辑
│   ├── 订单 /order/*：查询/解密/发货
│   ├── 物流 /logistics/*：发货/电子面单/轨迹
│   ├── 售后 /afterSale/*：退款/退货/换货/仲裁
│   ├── 库存 /sku/* & /stock/*：多仓库存
│   ├── 会员 /member/*：会员通/积分/等级
│   ├── 营销 /promotion/*：优惠券/满减/秒杀
│   └── 账单 /bill/*：接口调用计费账单
│
├── 精选联盟 /alliance/* & /buyin/* ← 达人带货
│   ├── 达人：选品/带货/佣金/PID
│   ├── 团长：招商/活动/托管
│   ├── 抖客：CPS 分销/红包/口令
│   └── MCN：机构管理/达人绑定
│
├── 抖音开放平台 (developer.open-douyin.com) ← 内容
│   ├── 短视频/直播数据
│   ├── 用户粉丝数据
│   ├── 商品橱窗/Link
│   └── 小程序/生活服务
│
├── 抖店云
│   └── 云端部署 → API 费用降低 90%（0.018 vs 0.18 元/百次）
│
├── 即时零售
│   └── 商品/订单/门店/配送 独立 API 体系
│
└── 跨境
    └── 跨境商品/保税仓/清关（独立 API）
```

### 2.2 核心差异化特征

| 特征 | 说明 | 对 AOS 的影响 |
|------|------|-------------|
| **全域兴趣电商** | 内容驱动（短视频/直播） + 货架电商（商品卡）双引擎 | 需要内容数据与商品数据联动 |
| **达人带货体系** | 达人→商品→佣金→订单 四角关系 | 新增 Talents/Commission Object Type |
| **抖店云** | 应用部署在抖店云内 API 费用降 90% | 架构上需支持云内部署方案 |
| **接口计费** | 按成功调用量收费，100次为最小计费单位 | Sync 策略需考虑成本优化 |
| **订单解密** | 敏感字段（手机/地址）需加密解密 | 需解密插件 + 抖店云内调用 |
| **数据推送** | 基于 RDS 推送（订单/售后直接入开发者数据库） | 可绕过 API 轮询，降低费用 |
| **供销平台** | 货源分销→铺货→代发 全链路 | 供应链孪生（后置） |

### 2.3 API 调用规范

| 维度 | 规范 |
|------|------|
| 认证方式 | OAuth 2.0，access_token 有效期约 15 天 |
| 签名算法 | HMAC-SHA256（推荐）/ MD5（即将下线） |
| 请求方式 | GET/POST，param_json 封装业务参数 |
| 计费 | 基础 API 云内 0.018 元/百次，云外 0.18 元/百次 |
| 限流 | app_key + api + shop 三维度限流 |
| 版本 | 当前 v2 |

---

## 3. 数据模型对照（抖音 vs Niushop 微商城基线）

> **复用策略：** Niushop 8 大领域模型为 AOS Ontology 基线，抖音适配时在以下维度做增强。

### 3.1 商品域（Product）

| 维度 | Niushop | 抖音 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 标识 | `goods_id` / `sku_id` (int) | `product_id` (long) / `sku_id` (long) | 相似 | 直接映射，OT 统一 string |
| 类目 | 自建 | 抖音三级类目树（`/shop/getShopCategory`） | 类目体系不同 | 需建抖音类目 Map 表 |
| SPU/SKU | 弱 SPU | 明确 SPU/SKU 分离（`product_id` vs `sku_id`） | 抖音更规范 | 显式 SPU OT |
| 商品发布 | 表单 | `/product/addV2`（JSON）+ `/product/addSchema`（Schema XML） | **抖音提供两种发布模式** | Connector 支持 Schema 模式 |
| 规格/属性 | 自由 KV | `spec_values`（规格）+ `product_format`（属性，含 `name`/`value` 标准列表） | 抖音规格标准化 | 品牌 + 规格 Prop |
| 图片 | 单主图 + 详情 | 主图（5张）+ 规格图 + 详情长图 + 白底图 | 抖音图片分层 | Prop 扩展图片组 |
| 视频 | 无 | 主图视频 | 抖音有视频字段 | MediaReference 映射 |
| 上下架 | `status=1/0` | `status`（0上架/1下架） | 方向相反 | 映射逻辑需翻转 |
| 价格 | 单一价格 | `price`（划线价）+ `spec_prices`（SKU 档位价） | 抖音价格层级 | 扩展 price Prop 组 |
| 限购 | 无 | `limit_per_buyer`（每人限购） | 抖音有限购属性 | 新增 Prop |
| 运费模板 | 内置 | `/freightTemplate/list`（独立运费模板 API） | 抖音运费模板独立 | 新增 FreightTemplate OT（后置） |

### 3.2 订单域（Order）

| 维度 | Niushop | 抖音 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 订单号 | `order_no`（自增） | `order_id`（全局唯一，以 `4730` 或 `5120` 开头） | 位数不同 | OT 统一 string |
| 状态机 | 5 状态 | 更复杂：`order_status`（待付款/待发货/已发货/已完成/已取消）+ `pay_status` + `delivery_status` + `refund_status` | 抖音子状态丰富 | 扩展状态枚举 |
| 买家 | `member_id` | `buyer_words`（加密昵称） + `post_addr`（加密地址） | **抖音隐私脱敏极严** | 需解密插件，OT 存储脱敏 ID |
| 地址 | 平铺明文 | 加密字段，需 `/order/batchDecrypt` 实时解密 | **重大差异：地址加密** | 解密 Function + 抖店云内调用 |
| 支付 | 独立表 | `pay_amount` + `pay_type`（0微信/1支付宝/2抖音支付...）+ `pay_time` | 抖音支付渠道丰富 | 扩展 payment_method 枚举 |
| SKU 行 | `order_goods` 独立 | `/order/orderDetail` 内嵌 `sku_order_list` 数组 | 嵌入响应 | 解析为 OrderLine |
| 优惠 | 优惠券独立 | `coupon_amount`（平台券/店铺券）+ `shop_discount`（商家优惠）+ `platform_discount`（平台补贴） | **抖音优惠分三层：平台 · 商家 · 达人** | 多级折扣字段 |
| 佣金 | 无 | `author_amount` / `shop_amount` / `platform_amount`（达人佣金/商家所得/平台扣佣） | **抖音独有：佣金四角模型** | 新增 Commission OT |
| 加密解密 | 无 | `batchDecrypt` → 敏感信息解密（需在抖店云内调用） | 安全合规要求 | 解密插件 |

### 3.3 物流域（Logistics）

| 维度 | Niushop | 抖音 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 发货接口 | 手动 | `/order/logisticsAdd`（单包裹）/ `/order/logisticsAddMultiPack`（多包裹） | 抖音支持一键多包裹 | 物流 OT 扩展 |
| 电子面单 | 无 | `/waybill/*`（取号/打印/取消）+ 多物流商 | 抖音面单体系完整 | 后置 |
| 物流轨迹 | 无实时 | `/logistics/track` 实时轨迹 | 抖音有 API 轨迹 | Function 实时查询 |
| 运费模板 | 内置 | `/freightTemplate/list` + `/freightTemplate/create` | 抖音运费模板独立 | FreightTemplate 独立 OT |
| 供应商代发 | 无 | `/supply/*`（供销平台代发） | **抖音独有：供应商代发链路** | 后置 |

### 3.4 售后域（After-Sales）

| 维度 | Niushop | 抖音 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 售后入口 | 紧耦合 | `/afterSale/*`（独立售后体系，与订单解耦） | 抖音售后独立 | 独立 AfterSales OT |
| 售后类型 | 退款/退货 | 退款/退货/换货/仅退款 | 抖音类型多 | 扩展枚举 |
| 审核操作 | 商家处理 | `/afterSale/Operate`（商家审核）+ 平台仲裁 | 抖音有平台仲裁 | Action 含审核/仲裁 |
| 换货流程 | 无 | `/afterSale/buyerExchange` + `/afterSale/buyerExchangeConfirm` | **抖音独有：完整换货闭环** | 新增 ExchangeProcess OT |
| 举证 | 无 | `/aftersale/submitEvidence`（最多 4 张凭证） | 抖音有举证机制 | Action 含举证上传 |
| BIC 质检 | 无 | `/bic/*`（质检 API） | **抖音独有：商品入仓质检** | 后置 |

### 3.5 会员域（Member / 会员通）

| 维度 | Niushop | 抖音 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 标识 | `member_id` | `open_id`（加密匿名） | 抖音 Open ID 多 App 隔离 | OT 用 Open ID |
| 会员通 | 无 | `/member/*`（品牌会员通：打通外部 CRM 与抖音会员） | **抖音独有：会员通体系** | 新增 MemberBridge OT |
| 积分 | 无 | 抖音积分体系 | 抖音有积分 | 后置 |
| 粉丝 | 无 | 达人粉丝（抖音开放平台） | 可通过开放平台获取 | 后置 |

### 3.6 达人/内容域（Creator & Content）🆕

> **这是抖音区别于所有其他电商平台的核心领域。**

| 维度 | 说明 | AOS 适配 |
|------|------|---------|
| 达人（Kol） | 带货达人/主播，通过精选联盟选品带货 | 🆕 Creator Object Type |
| 佣金（Commission） | 达人佣金、商家结算、平台扣佣 四角模型 | 🆕 Commission Object Type |
| 达人 PID | 渠道标识（dy_xxxx_xxxx_xxxx），用于分销追踪 | 新增 Prop |
| 直播带货 | 直播预告/直播间商品列表/实时数据 | 🆕 LiveSession Object Type（后置） |
| 短视频带货 | 短视频挂商品链接 | 🆕 VideoContent Object Type（后置） |
| 抖客分销 | CPS 分销（口令/红包/活动页） | 🆕 Distribution Object Type（后置） |
| 团长/机构 | 团长招商、MCN 机构管理 | 🆕 Agency Object Type（后置） |
| 商品卡 | 货架式商品卡片（非直播/短视频） | 映射到 Product 的 attribute |

### 3.7 店铺域（Shop）

| 维度 | Niushop | 抖音 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 标识 | `site_id` | `shop_id`（全局唯一） | 相似 | 直接映射 |
| 店铺名称 | 自由命名 | `shop_name` | 相似 | 直接映射 |
| 店铺评分 | 无 | DSR（商品体验/服务体验/物流体验） + 综合分 | 抖音有 DSR | 新增评分 Prop |
| 认证类型 | 无 | 个人/企业/品牌 | 抖音有认证体系 | 新增 auth_type Prop |
| 店铺装修 | 无 | `/shopDecoration/*`（装修组件 API） | 抖音有装修 API | 后置 |

### 3.8 营销域（Promotion）

| 维度 | Niushop | 抖音 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 优惠券 | `ns_promotion_coupon` | `/promotion/*`（平台券/店铺券/达人券） | 抖音票据体系丰富 | Phase 2 后置 |
| 秒杀 | 无 | 限时秒杀 | 抖音有秒杀 | Phase 2 |
| 拼团 | 无 | 平台拼团 | 抖音有拼团 | Phase 2 |
| 达人专属券 | 无 | 抖客专属券 `buyin/doukeProductExclusiveCoupon` | 抖音独有 | Phase 2 |

---

## 4. Ontology 目标态

### 4.1 Object Type 清单

> **基线复用**微商城 18 个 Object Type。新增/增强用 🆕 标注。

| 域 | Object Type | 基线来源 | 抖音适配说明 |
|----|------------|---------|-------------|
| 商品 | **Product** (SPU) | 微商城 goods → 微调 | product_id，支持 Schema 发布 |
| 商品 | **SKU** | 微商城 goods_sku → 微调 | sku_id + spec_prices 多档位 |
| 商品 | **Category** | 微商城 category → 重映射 | 抖音三级类目树 |
| 商品 | **Brand** 🆕 | 微商城无 → 新增 | 品牌独立 OT |
| 商品 | **FreightTemplate** 🆕 | 微商城无 → 新增 | 独立运费模板 |
| 订单 | **Order** | 微商城 order → 微调 | 抖音多状态 + 加密字段 |
| 订单 | **OrderLine** | 微商城 order_goods → 微调 | 嵌入 sku_order_list |
| 订单 | **Payment** | 微商城 pay → 合并 | 抖音微信/支付宝/抖音支付 |
| 物流 | **Logistics** | 微商城 express → 微调 | 多包裹 + 电子面单 |
| 售后 | **AfterSales** 🆕 | 微商城无 → 新增 | 抖音独立售后体系 |
| 售后 | **ExchangeProcess** 🆕 | 微商城无 → 新增 | 换货闭环 |
| 会员 | **Member** | 微商城 member → 微调 | Open ID + 会员通 |
| 达人 | **Creator** 🆕 | 微商城无 → 新增 | 带货达人/主播 |
| 达人 | **Commission** 🆕 | 微商城无 → 新增 | 四角佣金模型 |
| 店铺 | **Shop** | 微商城 site → 微调 | shop_id + DSR |
| 内容 | **LiveSession** 🆕 | 微商城无 → 新增 | 直播场次（后置） |
| 内容 | **VideoContent** 🆕 | 微商城无 → 新增 | 短视频带货（后置） |
| 分销 | **Distribution** 🆕 | 微商城无 → 新增 | 抖客 CPS（后置） |

**共计：20 Object Type（8 复用 + 12 新增）**— 是八个平台中 OT 数量最多的。

### 4.2 Link Type 清单

| 源 OT | 目标 OT | 关系 | 备注 |
|-------|--------|------|------|
| Product | SKU | has_many | SPU→SKU |
| Product | Category | belongs_to | 商品→类目 |
| Product | Brand | belongs_to | 商品→品牌 |
| Product | FreightTemplate | has_one | 运费模板 |
| Order | OrderLine | has_many | 订单→子行 |
| OrderLine | SKU | references | 子行→SKU |
| Order | Member | belongs_to | 订单→会员 |
| Order | Payment | has_one | 订单→支付 |
| Order | AfterSales | has_many | 订单→售后 |
| Order | Commission | has_many | **抖音独有：订单→佣金** |
| Commission | Creator | belongs_to | 佣金→达人 |
| Commission | Order | belongs_to | 佣金→订单 |
| Creator | Product | promotes | **抖音独有：达人→推广商品** |
| Creator | LiveSession | hosts | 达人→直播 |
| Creator | VideoContent | creates | 达人→短视频 |
| Shop | Product | has_many | 店铺→商品 |
| Shop | Creator | employs | 店铺→绑定达人 |
| OrderLine | Logistics | has_many | 子行→物流 |
| Creator | Distribution | has_many | 达人→抖客分销 |

**共计：19 Link Type**— 覆盖了达人带货的核心关系网。

---

## 5. 对接路径与实施波次

### 5.1 前置依赖

```
阻塞项（需平台侧先支持）：
├── G1 REST API Connector（现有 JDBC，需 HTTP Client 类型）
├── G2 OAuth 2.0 Token Manager（抖音 access_token 有效期 ~15 天）
├── G3 HMAC-SHA256 签名引擎（抖音签名规范）
├── G4 敏感数据解密插件（订单地址/手机号解密，需抖店云）
└── G5 接口计费控制器（抖音按调用量计费，需成本核算 + 调用量监控）
```

### 5.2 五波次执行计划

```
Wave 1「打通基础数据链路」（P0·当前阻塞于 G1/G2）
  ├ ─ 注册开发者账号 + 创建应用（电商工具型·ERP 类目）
  ├ ─ OAuth2 店铺授权 → access_token
  ├ ─ 商品/订单/物流 三个核心域 API 接入
  ├ ─ 35+ 核心 API 封装为 Connector Source
  └ ─ Funnel 第一关：API → Dataset（JSON 落地）

Wave 2「Ontology 建模」（P1）
  ├ ─ 14 核心 OT（不含内容/分发）创建
  ├ ─ 15 Link Type 建模
  ├ ─ Dataset → OT Mapping 字段级规则
  └ ─ 解密插件集成（订单敏感信息）

Wave 3「达人带货网络」（P1）
  ├ ─ Creator + Commission 核心 OT & Link
  ├ ─ 精选联盟数据接入（达人 PID/佣金/选品）
  ├ ─ 佣金四角模型（达人·商家·平台·机构）
  └ ─ Workshop: 达人带货看板

Wave 4「内容电商融合」（P2）
  ├ ─ 抖音开放平台接入（短视频/直播数据）
  ├ ─ LiveSession + VideoContent OT
  ├ ─ 内容数据与商品数据联动分析
  └ ─ Workshop: 内容电商全景看板

Wave 5「深度链路」（P2）
  ├ ─ 抖客 CPS 分销体系
  ├ ─ 供销平台代发链路
  ├ ─ 会员通（外部 CRM ↔ 抖音会员）
  └ ─ 即时零售 / 跨境
```

---

## 6. 平台缺口与平台需求

### 6.1 通用平台缺口（回馈 220plan）

| 缺口 | 严重度 | 描述 | 关联 220plan 项 |
|------|--------|------|---------------|
| REST API Connector | 🔴 G1 | 无法对接任何 REST 电商平台 | W2+ #G1 |
| OAuth 2.0 Token Manager | 🔴 G2 | 抖音 access_token 需自动续期 | W2+ #G2 |
| HMAC-SHA256 签名 | 🟡 G3 | 抖音签名规范 | 通用签名插件 |
| 敏感数据解密 | 🔴 G4 | 抖音订单地址/手机加密，需解密插件 | 安全合规模块 |
| API 计费控制器 | 🟡 G5 | 抖音按调用成功计费，需成本监控 | Connector 调度增强 |
| Ontology 动态 OT 创建 | 🟡 G6 | 抖音 20 个 OT + 19 Link，远超微商城 18+15 | OT 创建工具增强 |

### 6.2 抖音特有平台差异

| 差异 | 应对 |
|------|------|
| 接口按调用计费 | Sync 策略需考虑成本：优先使用 Data Push（RDS 推送），减少 API 轮询 |
| 订单数据加密 | 解密插件 + 强制抖店云内调用（合规要求） |
| 达人带货四角模型 | 新增 Creator + Commission OT，扩展 Link 网络 |
| 全域兴趣电商 | 内容数据（短视频/直播）与商品数据联动，需跨域关联分析 |
| 抖店云部署 | 降低 90% API 费用，架构上支持云内部署方案 |
| 供销平台代发 | 供应链领域新增代发链路（Phase 5） |

---

## 7. 下一步行动

| 优先级 | 行动 | 阻塞条件 | 预计产出 |
|-------|------|---------|---------|
| **P0** | 补充抖音 8 域字段级对照（API Response → OT Prop 映射） | — | 本文 §3 持续完善 |
| **P1** | 抖音 API 接口清单（全量 300+ → 筛选核心 ~40 个） | 需开发者账号 | `01-抖音API接口清单.md` |
| **P1** | 达人带货四角佣金模型详解 | — | `02-达人佣金模型分析.md` |
| **P1** | 抖店云部署方案（含解密链路） | — | `03-抖店云部署与解密方案.md` |
| **P2** | REST API Connector + 解密插件 | 220plan G1/G2/G4 完成 | 平台代码 |
| **P2** | 沙箱环境数据接入验证 | 220plan Phase 2 | Demo 跑通 |

> **版本**：v1.0 · 2026-07-22 · 抖音电商开放平台 AOS 数字孪生方案

> **变更日志**：
>
> | 版本 | 日期 | 说明 |
> | --- | --- | --- |
> | v1.0 | 2026-07-22 | 初版 · 基于抖店开放平台调研 · 内容+电商双引擎 · 20 OT + 19 Link（8 平台最多）· 达人带货四角模型 · 5 波次对接路径 · 6 项平台缺口 |
