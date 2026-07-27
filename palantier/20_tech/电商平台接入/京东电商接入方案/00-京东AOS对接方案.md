# 京东开放平台 · AOS 数字孪生对接方案

| 字段 | 内容 |
|------|------|
| 状态 | **方案仅分析 · P0 阶段** · 2026-07-22 |
| 版本 | **v1.0** · 初始方案 |
| 目录 | `docs/palantier/20_tech/京东电商接入方案/` |
| 覆盖范围 | **京东 POP 开放平台**（pop 商家） + **京东自营 VC**（vendor center）|
| 开放平台 | 宙斯开发者中心 (jos.jd.com) → 京东商家开放平台 (open.jd.com) |
| 关联 | 微商城模板：[00-Niushop微商城AOS对接方案](../微商城电商接入方案/00-Niushop微商城AOS对接方案.md) · [淘宝天猫方案](../淘宝电商接入方案/00-淘宝天猫AOS对接方案-总体分析计划.md) |
| 原则 | **先微商城打透 → 模板复用 → 仅适配京东差异点** |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 | 全文 |
| 先方案后代码 | 通过前不写行业定制码；缺口回馈**通用平台** |
| 整体孪生 | 目标是京东店铺业务世界在 AOS 可运营、可感知、可治理 |
| 模板复用 | 微商城（Niushop）8 大领域模型为基线，仅适配京东差异点 |
| 零行业定制码 | 平台差异通过 Connector 配置 / OT / OKF 映射消解，禁止 `jd-*` Host 分支 |

---

## 1. 一句话目标

> 将京东商家店铺（商品 · 订单 · 物流 · 售后 · 会员 · 营销 · 店铺 · 评价）  
> **整体映射**为 AOS 数字孪生，**复用**微商城已验证的 8 大领域模型，  
> 仅针对京东开放平台（JOS/商家开放平台）的 **API 网关 + POP/自营双模式** 做适配。

```text
微商城（已打透）              京东（待适配）
────────────────              ────────────────
JDBC 直连 MySQL ✅            REST API 网关 🔄 需要新的 Connector 类型
302 张表单表 Sync ✅           API 分页 + 限流 🔄 按 app_key 粒度限流
site_id 多租户 ✅              access_token + app_key 🔄 OAuth 2.0 Code 模式
商品/订单/会员/... 8 域 ✅    同样 8 域 + 自营/POP 双模型 🔄 模型分层
Funnel 四阶段 Pipeline ✅     API → Dataset → OT → Workshop ✅ 可复用
```

---

## 2. 京东平台画像

### 2.1 平台架构

```
京东开放平台生态
├── 宙斯开发者中心 (jos.jd.com) ← 旧平台·2025年起迁移
│   └── 正迁移至 → 京东商家开放平台 (open.jd.com)
├── POP 开放平台（第三方商家）
│   ├── 商品：jingdong.ware.* / jingdong.sku.*
│   ├── 订单：jingdong.order.* / jingdong.pop.order.*
│   ├── 售后：jingdong.asc.* / jingdong.pop.afs.*
│   ├── 物流：jingdong.logistics.*
│   └── 会员：jingdong.crm.*
├── 自营 VC（Vendor Center）
│   ├── 商品：jingdong.vc.item.*
│   ├── 采购：jingdong.b2b.* / jingdong.vc.po.*
│   └── 与 POP 共享订单/物流接口
├── 京东物流开放平台 (open.jdl.com) ← 独立体系
│   └── 仓配一体化、B2B/B2C 物流全链路
├── 京准通营销平台 (jzt.jd.com)
│   └── 京东快车、购物触点、京东展位
└── 京东联盟 (union.jd.com)
    └── CPS 分销、推客
```

### 2.2 POP vs 自营核心差异

| 维度 | POP（第三方商家） | 自营 VC（Vendor Center） |
|------|------------------|------------------------|
| 商品发布 | `jingdong.ware.write.*` | `jingdong.vc.item.*` |
| 库存管理 | 商家自主管理 | 京东仓内库存 + 采购单驱动 |
| 订单履约 | 商家发货（SOP/SOPL/LBP） | 京东仓发货 + 采购单流转 |
| 结算 | 商家自主结算 | 采销结算（账期） |
| 定价权 | 商家自主定价 | 京东统一定价 + 采购价 |
| 物流 | 可选择京东物流/第三方 | 京东仓配一体（JDL） |
| 数据权限 | 只看自己店铺数据 | 全品类数据（受限） |

### 2.3 API 版本演进

| 里程碑 | 变化 |
|--------|------|
| 2025 Q2 | 宙斯平台 jos.jd.com 整体迁移至 open.jd.com |
| 2025+ | 新接入统一通过商家开放平台 |
| API 版本 | v2.0（当前主流），部分旧接口仍为 v1.0 |
| 签名方式 | MD5（旧）/ HMAC-SHA256（推荐） |
| 认证方式 | OAuth 2.0 Authorization Code 模式 |

---

## 3. 数据模型对照（京东 vs Niushop 微商城基线）

> **复用策略：** Niushop 8 大领域模型为 AOS Ontology 基线，京东适配时在以下维度做增强。

### 3.1 商品域（Ware / SKU）

| 维度 | Niushop | 京东 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 标识 | `goods_id` / `sku_id` (int) | `wareId` (long) / `skuId` (long) | 均为长整型 | 直接映射，OT 统一 string |
| 类目 | 自建 `category_id` | `cid`（京东类目树，四级结构） | 类目体系不同 | 需建京东类目 Map 表 |
| SPU 概念 | 弱（goods ≈ SPU） | 明确：ware = SPU, sku = SKU | 京东更规范 | OT 显式建 SPU OT |
| 商品属性 | 自由 KV | 销售属性（`saleAttr`，dim=1）+ 非销售属性（`features`） | 京东属性规范化强 | 品牌建独立 OT + 销售属性 Prop |
| POP vs 自营 | N/A | POP：`jingdong.ware.*` / 自营：`jingdong.vc.item.*` | **双 API 体系** | OT 统一，Connector 层分派 |
| 图片 | 单主图 + 详情图 | 7 主图（最多）+ SKU 图 + 白底图 + 透明图 | 京东图片规格更多 | Prop 扩展图片组字段 |
| 视频 | 无 | `jingdong.pop.video.*`（主图视频 + SKU 视频） | 京东有官方视频 API | 新增 MediaReference Prop |
| 上下架 | `status=1/0` | `jingdong.ware.write.upOrDown`（1上架/2下架） | 相似 | 映射到 Event |
| 销量 | 无累计 | `sales`（SPU/SKU 双维度） | 京东有官方销量字段 | 新增 `sales_quantity` Prop |
| 好评率 | 无 | `jingdong.pop.getCommentSummarys`（SPU/SKU 维度） | 京东有官方好评率 API | 新增 `good_comment_rate` Prop |
| 京东价 | 无 | `jdPrice`（sku 维度京东价） | 京东定价独立 | 新增 `jd_price` Prop |

### 3.2 订单域（Order）

| 维度 | Niushop | 京东 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 订单号 | `order_no`（自增） | `orderId`（全局唯一长整型） | 位数不同 | OT 统一 string |
| 父/子单 | 弱（order → order_goods） | 明确：父订单 `orderId` + 子订单 `orderItemId`（拆单模型） | **京东有父子拆单** | OT 建 Order（父）+ OrderLine（子）Link |
| 履约模式 | 商家发货 | SOP/SOPL/LBP/FBP（4 种）→ 自营模式更多 | **京东履约模式复杂** | OT 新增 `fulfillment_type` Prop |
| 状态机 | 待付款→已付款→已发货→已收货→完成 | 更复杂：`orderStatus`（多状态）+ `paymentType` + `payStatus` + `deliveryStatus` | 京东子状态极细 | 扩展 OT 状态枚举 |
| 买家 | `member_id` | `buyerPin`（脱敏后） | 京东用 PIN | OT Link to 会员 OT |
| 地址 | 平铺 `receiver_*` | 同样平铺 | 结构相似 | 直接映射 |
| 支付 | 独立 `pay` 表 | `payment` + `payType`（在线/货到付款/白条） + `payTime`（嵌入订单） | 京东支付方式更多（白条） | 扩展 payment_method 枚举 |
| SKU 行 | `order_goods` 独立表 | `orderItemId` + `skuId` + `wareId`（嵌入订单响应） | 结构相似 | 解析为 OrderLine Object |
| 优惠 | 优惠券独立表 | `couponPrice`（京券/东券）+ `promiseServicePrice`（延保等）+ `orderSopPrice` | **京东优惠层级极多** | 需多级折扣字段 |
| 发票 | 无 | `invoiceType`（电子/纸质/增值税） + `invoiceTitle` | 京东发票信息丰富 | 新增 Invoice Prop Group |

### 3.3 物流域（Logistics / JDL）

| 维度 | Niushop | 京东 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 物流体系 | 自维护 | **京东物流 JDL 独立体系**（open.jdl.com） | **最大差异：京东物流是独立开放平台** | 需独立 JDL Connector（后置） |
| 快递公司 | 自维护 | `jingdong.logistics.carriers.list`（京东配送 + 合作物流） | 京东官方下发表单 | 物流 OT 基本相同 |
| 包裹拆分 | 独立表 | 子订单维度拆包（一单多包） | 京东拆包模型更复杂 | 映射为 OrderLine → Package Link |
| 物流轨迹 | 无实时 | `jingdong.ldop.middle.waybill.Waybill2CTraceApi`（全程 2C 轨迹） | 京东有实时轨迹 | 功能型 Function 实时查询 |
| 电子面单 | 无 | `jingdong.ldop.alpha.*`（中小件/大家电/生鲜多品类） | 京东面单体系全品类 | 后置（远期待办） |
| 仓配一体 | 无 | 京东仓 → 京东配送（FBP 模式）+ 7 大区域仓 | 京东独有 | 后置，需 Location Inventory 模型 |

### 3.4 售后域（After-Sales）

| 维度 | Niushop | 京东 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 售后入口 | 紧耦合订单 | `jingdong.asc.*`（独立售后体系） | **京东售后与订单解耦** | 独立 AfterSales Object Type |
| 售后类型 | 退款/退货 | 退款/退货/换货/维修/赔付/价保 | 京东售后类型更多 | 扩展类型枚举 |
| 审核流程 | 商家自行处理 | `jingdong.asc.audit.*` + 平台仲裁 | 京东有平台介入 | Action Type 含审核/仲裁 |
| 退款单 | 无独立 | `jingdong.pop.afs.soa.refundapply.*`（独立退款单号） | 京东有独立退款单 | 建 Refund Object Type |
| 售前退款 | N/A | `jingdong.pop.afs.soa.refundapply.queryById`（下单未完成取消） | 京东区分售前/售后 | Prop 区分 `refund_stage` |
| 价保 | 无 | 京东价保（7/15/30 天） | 京东独有 | 后置（Phase 3） |

### 3.5 会员域（CRM）

| 维度 | Niushop | 京东 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 标识 | `member_id` | `buyerPin`（经过脱敏） | 京东用 PIN 标识 | OT 用脱敏 ID |
| 会员等级 | 自建 | 京东会员体系（注册/铜牌/银牌/金牌/钻石/PLUS） | 京东会员等级丰富 | 映射到通用等级 Prop |
| 标签 | 自建 | `jingdong.crm.member.scan`（分页查询） | 相似 | CRM API 独立 Source |
| 积分 | 无 | 京豆（jingBean）体系 | 京东有积分体系 | 后置 |
| PLUS 会员 | 无 | 京东 PLUS 联合会员 | 京东独有 | 后置（远期待办） |

### 3.6 店铺域（Shop / Vender）

| 维度 | Niushop | 京东 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 标识 | `site_id` + `weapp_id` | `venderId` + `shopId` | 相似 | 直接映射 |
| 店铺名称 | 自由命名 | `shopName` | 相似 | 直接映射 |
| 店铺类型 | 无 | POP 个人/企业 + 自营（SOP/SOPL/LBP/FBP） | **京东店铺类型极多** | 新增 `shop_type` / `biz_type` Prop |
| 店内分类 | 无 | `jingdong.vender.shopcategory.*`（自定义店内分类） | 京东有店内分类 API | 新增 ShopCategory Object Type |
| 评分 | 无 | DSR 三项（商品描述/卖家服务/物流履约）+ 综合评分 | 京东有 DSR | 新增评分 Prop |
| 资质 | 无 | `jingdong.seller.qua.center.*`（商品资质上传） | 京东有独立资质体系 | 后置 |
| 多店铺 | `site_id` 隔离 | 一个 app_key 可授权多店铺 | 模型差异 | AOS Workspace ↔ 京东店铺 1:1 |

### 3.7 营销域（Promotion / 京准通）

| 维度 | Niushop | 京东 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 促销引擎 | 基础优惠券 | `jingdong.seller.promotion.*`（直降/满减/赠品/套装/N元任选） | 京东促销规则极丰富 | Phase 2 后置 |
| 优惠券 | `ns_promotion_coupon` | 京券（平台）/ 东券（店铺）/ 品类券 | 京东票据体系复杂 | Phase 2 后置 |
| 广告营销 | 无 | 京准通（jzt.jd.com）：京东快车/购物触点/京东展位 | **京东有独立广告平台** | 暂不接入 |
| CPS 分销 | 无 | 京东联盟（union.jd.com）：推客/CPS/社群 | 京东联盟体系完整 | 后置 |
| 秒杀 | 无 | 京东秒杀/品牌闪购/新品首发 | 京东活动分层多 | Phase 3 |

### 3.8 评价域（Comment）

| 维度 | Niushop | 京东 | 差异 | AOS 适配 |
|------|---------|------|------|---------|
| 评价 | 无独立接口 | `jingdong.pop.getCommentSummarys`（批量查询 SPU/SKU 好评率） | 京东有评价 API | 新增 Comment Object Type |
| 商品描述 | HTML 详情 | `jingdong.ware.bookbigfield.get`（图书品类）/ 通用详情 | 相似 | 直接映射 |
| 问答 | 无 | 京东问答（独立社区模块） | 京东有问答 API | 后置 |

---

## 4. Ontology 目标态

### 4.1 Object Type 清单

> **基线复用**微商城 18 个 Object Type。新增/增强用 🆕 标注。

| 域 | Object Type | 基线来源 | 京东适配说明 |
|----|------------|---------|-------------|
| 商品 | **Product** (SPU) | 微商城 goods → 微调 | SPU 显式建模，wareId |
| 商品 | **SKU** | 微商城 goods_sku → 微调 | 自营/POP 双源，skuId |
| 商品 | **Category** | 微商城 category → 重映射 | 京东四级类目树 |
| 商品 | **Brand** 🆕 | 微商城无 → 新增 | 品牌独立 OT，`jingdong.getBrandByIds` |
| 订单 | **Order** (父单) 🆕 | 微商城 order → 拆分 | 父订单 + 子订单模型 |
| 订单 | **OrderLine** (子单/行) 🆕 | 微商城 order_goods → 微调 | 京东子订单模型 |
| 订单 | **Payment** | 微商城 pay → 合并 | 嵌入订单，京东支付方式枚举 |
| 订单 | **Invoice** 🆕 | 微商城无 → 新增 | 京东独立发票信息 |
| 物流 | **Logistics** | 微商城 express → 微调 | JDL 轨迹 + 电子面单 |
| 物流 | **Package** 🆕 | 微商城无 → 新增 | 京东一单多包模型 |
| 售后 | **AfterSales** 🆕 | 微商城无 → 新增 | 京东独立售后体系 |
| 售后 | **Refund** 🆕 | 微商城无 → 新增 | 独立退款单 |
| 会员 | **Member** | 微商城 member → 微调 | buyerPin 脱敏 + PLUS 标记 |
| 会员 | **MemberLevel** 🆕 | 微商城无 → 新增 | 京东会员等级枚举 |
| 店铺 | **Shop** | 微商城 site → 微调 | venderId + 店铺类型 |
| 店铺 | **ShopCategory** 🆕 | 微商城无 → 新增 | 京东自定义店内分类 |
| 评价 | **Comment** 🆕 | 微商城无 → 新增 | 京东好评率数据 |

**共计：18 Object Type（11 复用 + 7 新增）**

### 4.2 Link Type 清单

| 源 OT | 目标 OT | 关系 | 备注 |
|-------|--------|------|------|
| Product | SKU | has_many | SPU → SKU |
| Product | Category | belongs_to | 商品 → 类目 |
| Product | Brand | belongs_to | 商品 → 品牌 |
| Order | OrderLine | has_many | 父单 → 子单 |
| OrderLine | SKU | references | 子单 → SKU |
| Order | Member | belongs_to | 订单 → 会员 |
| Order | Payment | has_one | 订单 → 支付 |
| Order | Invoice | has_one | 订单 → 发票 |
| Order | AfterSales | has_many | 订单 → 售后单 |
| AfterSales | Refund | has_one | 售后单 → 退款单 |
| OrderLine | Logistics | has_many | 子单 → 物流包裹 |
| Logistics | Package | has_many | 物流 → 包裹 |
| Shop | Product | has_many | 店铺 → 商品 |
| Shop | ShopCategory | has_many | 店铺 → 店内分类 |
| Product | Comment | has_many | 商品 → 评价 |

**共计：15 Link Type**

---

## 5. 对接路径与实施波次

### 5.1 前置依赖

```
阻塞项（需平台侧先支持）：
├── G1 REST API Connector（现有 JDBC，需 HTTP Client 类型）
├── G2 OAuth 2.0 Token Manager（Code 模式 + Refresh Token 自动续期）
├── G3 HMAC-SHA256 签名引擎（京东签名规范）
└── G4 API 限流控制器（京东 app_key 粒度限流 + 重试策略）
```

### 5.2 四波次执行计划

```
Wave 1「打通数据链路」（P0·当前阻塞于 G1/G2）
  ├ ─ 注册企业开发者账号 + 创建应用
  ├ ─ 基础认证流程（OAuth2 Code → access_token → refresh_token）
  ├ ─ POP 商品/订单/物流三个核心域数据接入
  ├ ─ 30+ 核心 API 封装为 Connector Source
  └ ─ Funnel 第一关：API → Dataset（JSON 落地）

Wave 2「Ontology 建模」（P1）
  ├ ─ 18 Object Type + 15 Link Type 创建
  ├ ─ Dataset → OT Mapping 字段级规则
  ├ ─ 父子订单模型正确链入
  └ ─ DSR 评分 / 好评率 / 发票 等京东独有字段入 Ontology

Wave 3「业务闭环」（P1）
  ├ ─ 售后体系接入（AfterSales + Refund OT）
  ├ ─ 京东物流 JDL 轨迹实时查询 Function
  ├ ─ Action：售后审核/操作
  └ ─ Workshop：订单满意度看板 + 履约分析

Wave 4「深度覆盖」（P2）
  ├ ─ 自营 VC API 接入（与 POP 并行）
  ├ ─ 京东联盟 CPS 数据
  ├ ─ 京准通广告数据（ROI/点击/转化）
  └ ─ 京东 PLUS 会员体系
```

---

## 6. 平台缺口与平台需求

### 6.1 通用平台缺口（回馈 220plan）

| 缺口 | 严重度 | 描述 | 关联 220plan 项 |
|------|--------|------|---------------|
| REST API Connector | 🔴 G1 | 无法对接任何 REST 电商平台 | W2+ #G1 |
| OAuth 2.0 Token Manager | 🔴 G2 | 京东 OAuth Code 模式需自动续期 | W2+ #G2 |
| HMAC-SHA256 签名 | 🟡 G3 | 京东签名规范不同于淘宝 MD5 和 Amazon AWS4 | 通用签名插件 |
| 父子订单模型 | 🟡 G4 | Ontology 需支持自引用 Link（Order→OrderLine） | OT 建模增强 |
| API 限流控制器 | 🟢 G5 | 京东 app_key 粒度 QPS 限流 | Connector 调度增强 |

### 6.2 京东特有平台差异

| 差异 | 应对 |
|------|------|
| 宙斯→商家开放平台迁移 | 统一对接新平台（open.jd.com），旧 jos 作为回退 |
| POP/自营双 API 体系 | Connector 层分派，OT 层统一；需两套 Source 配置 |
| 京东物流 JDL 独立体系 | JDL 作为独立 Connector Type（open.jdl.com），不与电商绑定 |
| 京准通营销独立 | 广告数据暂不接入数字孪生，Phase 3 再议 |
| 接口按调用量收费 | 需成本核算：基础 API 调用量预估（商品/订单同步频次 × QPS） |

---

## 7. 下一步行动

| 优先级 | 行动 | 阻塞条件 | 预计产出 |
|-------|------|---------|---------|
| **P0** | 补充京东 8 域字段级对照（API Response → OT Prop 映射） | — | 本文 §3 持续完善 |
| **P1** | 京东 API 接口清单（全量分类 → 筛选核心 ~40 个） | 需企业开发者账号 | `01-京东API接口清单.md` |
| **P1** | POP/自营双模式数据模型差异对照 | — | `02-POP与自营差异分析.md` |
| **P2** | REST API Connector 设计 + OAuth 实现 | 220plan G1/G2 完成 | 平台代码 |
| **P2** | 沙箱环境数据接入验证 | 220plan Phase 2 | Demo 跑通 |

> **版本**：v1.0 · 2026-07-22 · 京东开放平台 AOS 数字孪生方案

> **变更日志**：
>
> | 版本 | 日期 | 说明 |
> | --- | --- | --- |
> | v1.0 | 2026-07-22 | 初版 · 基于京东开放平台（JOS→open.jd.com）调研 · POP/自营双模式 · 18 OT + 15 Link · 4 波次对接路径 · 5 项平台缺口 |
