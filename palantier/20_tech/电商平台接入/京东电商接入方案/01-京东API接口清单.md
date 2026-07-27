# 01 · 京东开放平台（JOS/open.jd.com）API 接口清单

> **版本**：v1.0 · 2026-07-23
> **状态**：P1 调研完成 · 筛选与 AOS 数字孪生对接相关的核心接口
> **来源**：京东开放平台文档（jos.jd.com / open.jd.com）+ 多源交叉验证
> **关联**：[00-总体分析计划](./00-京东AOS对接方案.md) · [02-POP与自营差异分析](./02-POP与自营差异分析.md)

---

## 1. 筛选原则

从京东开放平台 500+ 接口中按以下标准筛选：

| 原则 | 说明 |
|------|------|
| 数字孪生相关 | 仅选取与"将京东店铺映射为 AOS Ontology"相关的接口 |
| 读优先 | 优先 Source Sync（读），写回 Action（写）按需后置 |
| POP + 自营双覆盖 | 标注接口是 POP 专属 / 自营专属 / 两者共用 |
| 企业可用 | 标注权限要求（公开/商家授权/增值），避免不可达接口 |

**筛选结果**：500+ 接口 → **42 个核心接口**（8 域 × ~5 接口/域）

---

## 2. 接口分类总览

| 业务域 | 接口数 | POP | 自营(VC) | 共用 | AOS 对应环节 |
|--------|-------|-----|---------|------|-------------|
| 商品域 | 8 | 4 | 2 | 2 | Source Sync + OT + Action |
| 订单域 | 7 | 4 | — | 3 | Source Sync + OT + Action |
| 物流域 | 6 | 3 | — | 3 | Source Sync + Function |
| 售后域 | 6 | 5 | — | 1 | Source Sync + OT + Action |
| 会员域 | 4 | 3 | — | 1 | Source Sync（需增值权限） |
| 店铺域 | 3 | 1 | — | 2 | Source Sync（一次性） |
| 营销/评价域 | 5 | 5 | — | — | Source Sync + OT |
| 采购/入库(自营) | 3 | — | 3 | — | Source Sync（自营专属） |
| **合计** | **42** | 25 | 5 | 12 | |

---

## 3. 详细接口清单

### 3.1 商品域（8 接口）

| # | 接口 | 方向 | 阵营 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|------|---------|
| 1 | `jingdong.ware.list.get` | 读 | POP | 商家授权 | 商品列表（POP） | 分页 `page`+`page_size`；返回 `wareId`、`title`、`status`(1上架/2下架)、`cid`、`shopPrice` |
| 2 | `jingdong.ware.get` | 读 | POP | 商家授权 | 单商品详情（POP） | `wareId` 传入；返回 SPU 全量：`title`、`skuList`（含 `skuId`/`jdPrice`/`stockNum`）、`imgs`（最多7图）、`saleAttr`（销售属性） |
| 3 | `jingdong.ware.write.upOrDown` | 写 | POP | 商家授权 | 商品上下架 | `wareId` + `status`(1上架/2下架)；触发状态变更 |
| 4 | `jingdong.sku.price.update` | 写 | POP | 商家授权 | 修改 SKU 价格 | `skuId` + `jdPrice`；支持批量（max 20） |
| 5 | `jingdong.vc.item.list.get` | 读 | 自营 | 自营授权 | 自营商品列表 | 返回 `wareId`、`skuId`、`brandId`、`cid`；自营商品无上下架概念，由京东控制 |
| 6 | `jingdong.vc.item.detail.get` | 读 | 自营 | 自营授权 | 自营商品详情 | `wareId` 传入；返回含采购价 `purchasePrice` + 零售价 `jdPrice`（双价格） |
| 7 | `jingdong.getBrandByIds` | 读 | 共用 | 商家授权 | 品牌信息查询 | `brandId` 列表；返回 `brandId`、`name`、`logo`、`alias`；**品牌建独立 OT** |
| 8 | `jingdong.ware.bookbigfield.get` | 读 | POP | 商家授权 | 商品详情大字段（HTML） | `wareId` 传入；返回 `bookBigField`（富文本详情）；图书品类专用 |

### 3.2 订单域（7 接口）

| # | 接口 | 方向 | 阵营 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|------|---------|
| 9 | `jingdong.pop.order.list.get` | 读 | POP | 商家授权 | POP 订单列表 | `startTime`/`endTime` 时间范围；返回 `orderId`、`orderStatus`、`orderSource`、`payType`、`buyerPin`（脱敏） |
| 10 | `jingdong.pop.order.info.get` | 读 | POP | 商家授权 | POP 订单详情 | `orderId` 传入；返回完整：`orderItemList`（子订单行）、`payment`、`invoiceInfo`、`receiverInfo`（地址） |
| 11 | `jingdong.pop.order.shipment.update` | 写 | POP | 商家授权 | POP 发货 | `orderId` + `logisticsId`(快递公司) + `waybillCode`(运单号)；触发发货 |
| 12 | `jingdong.pop.order.memo.update` | 写 | POP | 商家授权 | 修改订单备注 | `orderId` + `memo` + `flag`(星标)；用于 Action 写回 |
| 13 | `jingdong.order.search` | 读 | 共用 | 商家授权 | 按条件搜索订单 | 支持 `orderId`/`buyerPin`/`startDate`/`endDate` 多条件；**POP+自营共用入口** |
| 14 | `jingdong.pop.order.en.search` | 读 | 共用 | 商家授权 | 增量订单搜索 | 按 `modified` 时间增量；**推荐用于定时 Sync** |
| 15 | `jingdong.pop.order.cancel` | 写 | 共用 | 商家授权 | 取消订单（商家主动） | `orderId` + `cancelReason`；仅限待付款状态 |

> **订单状态枚举：**
> - POP `orderStatus`：WAIT_SELLER_STOCK_OUT（待发货）/ WAIT_GOODS_RECEIVE_CONFIRM（已发货）/ WAIT_WRITE_WAYBILL（待写运单）/ RECEIPTS_CONFIRM（已收货）/ FINISHED_L（已完成）/ TRADE_CANCELED（已取消）
> - 履约模式：SOP / SOPL / LBP / FBP

### 3.3 物流域（6 接口）

| # | 接口 | 方向 | 阵营 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|------|---------|
| 16 | `jingdong.logistics.carriers.list` | 读 | 共用 | 公开 | 快递公司列表 | 返回 `carrierId`、`name`、`code`；含京东配送+合作物流 |
| 17 | `jingdong.ldop.abnormal.pickUpOrder.get` | 读 | 共用 | 商家授权 | 获取异常取件单 | 物流异常场景查询 |
| 18 | `jingdong.ldop.middle.waybill.Waybill2CTraceApi` | 读 | 共用 | 商家授权 | **物流轨迹（2C）** | `waybillCode` 传入；返回全程轨迹节点；**实时查询不落 Dataset** |
| 19 | `jingdong.ldop.alpha.waybill.receive` | 写 | POP | 商家授权 | 获取京东快递面单号 | 京东物流电子面单取号；中小件/大家电/生鲜多品类 |
| 20 | `jingdong.ldop.delivery.send` | 写 | POP | 商家授权 | 京东物流发货 | `deliveryId` + `boxList`（多包裹）；京东仓配送 |
| 21 | `jingdong.ldop.receive.trace.get` | 读 | 共用 | 商家授权 | 获取物流推送轨迹 | `deliveryId` 传入；批量轨迹查询 |

### 3.4 售后域（6 接口）

> **京东售后独立体系（`jingdong.asc.*`），与订单解耦。**

| # | 接口 | 方向 | 阵营 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|------|---------|
| 22 | `jingdong.pop.afs.soa.afterSale.list.get` | 读 | POP | 商家授权 | 售后单列表 | `state`（状态）+ 时间范围；返回 `serviceId`（售后单号）、`orderId`、`skuId`、`afsType`（退款/退货/换货/维修/赔付/价保） |
| 23 | `jingdong.pop.afs.soa.afterSale.detail.get` | 读 | POP | 商家授权 | 售后单详情 | `serviceId` 传入；返回 `reason`、`status`、`evidencePics`（凭证）、`refundAmount` |
| 24 | `jingdong.asc.audit.apply` | 写 | POP | 商家授权 | 商家审核售后申请 | `serviceId` + `auditResult`(同意/拒绝) + `remark`；触发审核流程 |
| 25 | `jingdong.pop.afs.soa.refundapply.queryById` | 读 | POP | 商家授权 | 查询退款申请详情 | `serviceId` 传入；返回退款单信息（独立退款单号） |
| 26 | `jingdong.pop.afs.soa.compensate.get` | 读 | POP | 商家授权 | 获取赔付/价保详情 | `serviceId` 传入；价保 7/15/30 天规则 |
| 27 | `jingdong.asc.process.state.get` | 读 | 共用 | 商家授权 | 售后处理状态查询 | 返回 `state`（待审核/待退货/待退款/已完成/已关闭）+ 平台仲裁标记 |

> **售后类型枚举（京东独有丰富度）：**
> - `afsType`：10 退款 / 20 退货退款 / 30 换货 / 40 维修 / 50 赔付 / 60 价保

### 3.5 会员域（4 接口）

| # | 接口 | 方向 | 阵营 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|------|---------|
| 28 | `jingdong.crm.member.scan` | 读 | POP | **增值权限** | 会员列表分页查询 | `pin` 或 `mobile` 过滤；返回 `pin`（脱敏）、`level`(铜/银/金/钻/PLUS)、`tradeAmount`、`tradeCount` |
| 29 | `jingdong.crm.member.get` | 读 | POP | **增值权限** | 单会员详情 | `pin` 传入；返回 `level`、`jingBean`(京豆)、`registerTime`、`lastTradeTime` |
| 30 | `jingdong.crm.member.label.update` | 写 | POP | **增值权限** | 更新会员标签 | `pin` + `labels`（标签 KV）；用于会员运营 |
| 31 | `jingdong.user.basic.info.get` | 读 | 共用 | 商家授权 | 基础用户信息 | 返回 `pin`、`nickname`、`avatar`、`plusStatus`(PLUS 会员标记) |

### 3.6 店铺域（3 接口）

| # | 接口 | 方向 | 阵营 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|------|---------|
| 32 | `jingdong.vender.shop.get` | 读 | 共用 | 商家授权 | 店铺基本信息 | 返回 `shopId`、`venderId`、`shopName`、`shopType`(POP个人/企业/自营)、`bizType`(SOP/SOPL/LBP/FBP) |
| 33 | `jingdong.vender.shopcategory.list` | 读 | POP | 商家授权 | 店铺自定义分类 | 返回 `categoryId`、`name`、`order`；店铺内商品分组 |
| 34 | `jingdong.seller.qua.center.detail` | 读 | POP | 商家授权 | 商品资质详情 | `skuId` 传入；返回资质上传记录（质检报告/授权书） |

### 3.7 营销/评价域（5 接口）

| # | 接口 | 方向 | 阵营 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|------|---------|
| 35 | `jingdong.seller.promotion.list.get` | 读 | POP | 商家授权 | 促销活动列表 | 返回 `promotionId`、`type`(直降/满减/赠品/套装/N元任选)、`beginTime`、`endTime`、`skuList` |
| 36 | `jingdong.pop.coupon.list.get` | 读 | POP | 商家授权 | 优惠券列表 | 返回 `couponId`、`type`(京券/东券/品类券)、`denomination`、`beginTime`、`endTime` |
| 37 | `jingdong.pop.getCommentSummarys` | 读 | POP | 商家授权 | **商品好评率**（SPU/SKU 维度） | `wareId` 或 `skuId` 列表；返回 `goodRate`、`generalRate`、`poorRate`、`commentCount` |
| 38 | `jingdong.pop.comment.list.get` | 读 | POP | 商家授权 | 商品评价列表 | `wareId` + 分页；返回 `commentId`、`score`(1-5)、`content`、`images`、`created` |
| 39 | `jingdong.pop.comment.reply.add` | 写 | POP | 商家授权 | 商家回复评价 | `commentId` + `content`；用于 Action 写回 |

### 3.8 采购/入库域（3 接口 · 自营专属）

> **自营 VC（Vendor Center）独有 API，与 POP 完全不同的业务模型。**

| # | 接口 | 方向 | 阵营 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|------|---------|
| 40 | `jingdong.vc.po.list.get` | 读 | 自营 | 自营授权 | 采购单列表 | 返回 `purchaseId`、`wareId`、`quantity`、`purchasePrice`、`state`(待确认/已确认/已发货/已入库) |
| 41 | `jingdong.vc.po.detail.get` | 读 | 自营 | 自营授权 | 采购单详情 | `purchaseId` 传入；返回完整采购信息 + 仓配指令 |
| 42 | `jingdong.b2b.inboundOrder.get` | 读 | 自营 | 自营授权 | 入库单查询 | 返回 `inboundId`、`warehouseCode`、`status`、`items`（SKU+数量） |

---

## 4. 权限分级

| 级别 | 要求 | 接口数 | 代表接口 |
|------|------|-------|---------|
| **公开** | AppKey 即可 | 1 | `jingdong.logistics.carriers.list` |
| **商家授权** | OAuth 2.0 access_token | 30 | `jingdong.pop.order.list.get`、`jingdong.ware.list.get` |
| **增值权限** | 需购买 CRM 增值包 | 3 | `jingdong.crm.member.*` 系列 |
| **自营授权** | Vendor Center 专属权限 | 5 | `jingdong.vc.*` 系列 |
| **PLUS 数据** | 需额外申请 PLUS 权限 | 部分 | PLUS 会员相关字段 |

---

## 5. 与 AOS Source Sync 的对接映射

```
AOS Source Sync 阶段            JOS API                              备注
─────────────────            ────────                              ────
全量拉取（首次）               jingdong.ware.list.get                POP 商品分页
                              jingdong.pop.order.list.get           POP 订单分批
                              jingdong.vc.item.list.get             自营商品

增量同步（定时）               jingdong.pop.order.en.search          ★ 按 modified 时间增量
                              jingdong.pop.afs.soa.afterSale.list   售后增量
                              jingdong.crm.member.scan              会员增量（增值权限）

实时查询（不落 Dataset）       jingdong.ldop.middle.waybill...       物流轨迹
                              jingdong.pop.order.info.get           订单详情 On-Demand

配置参考（一次性）             jingdong.vender.shop.get              店铺信息
                              jingdong.logistics.carriers.list      快递公司
                              jingdong.getBrandByIds                品牌库
```

---

## 6. 签名算法

> **京东支持 MD5（旧）和 HMAC-SHA256（推荐），新应用必须用 HMAC-SHA256。**

```text
HMAC-SHA256 签名步骤：
1. 参数按 key ASCII 升序排列
2. 拼接：key1value1key2value2...
3. 拼接 app_secret：app_secret + 步骤2结果
4. HMAC-SHA256 哈希 → Base64 编码 → sign
5. sign 放入请求参数

请求示例（POST api.jd.com/routerjson）：
{
  "method": "jingdong.pop.order.list.get",
  "app_key": "xxx",
  "access_token": "xxx",
  "timestamp": "2026-07-23 12:00:00",
  "format": "json",
  "v": "2.0",
  "sign_method": "hmac-sha256",
  "360buy_param_json": "{\"orderId\":\"xxx\"}",
  "sign": "BASE64_ENCODED_SIGN"
}
```

---

## 7. 限流策略

| 维度 | 规则 |
|------|------|
| 限制粒度 | **app_key + API 方法** 级别 |
| 默认 QPS | 依赖口类型，一般 40-200 QPS |
| 突发 | 支持 burst，但持续超限会降频 |
| 超限响应 | HTTP 200 + JSON body `code=1004` |
| 建议 | Source Sync 内置令牌桶 + 退避重试 |

---

## 8. 风险与注意

| # | 风险点 | 说明 | 缓解措施 |
|----|-------|------|---------|
| R1 | 宙斯→商家开放平台迁移中 | 2025 Q2 起 jos.jd.com 接口逐步迁移至 open.jd.com | 统一对接新平台，旧 jos 作为回退 |
| R2 | POP/自营双 API 体系 | 同一业务在 POP 和 VC 中用不同接口 | Connector 层分派，OT 层统一 |
| R3 | 父子订单拆单模型 | 京东一单可拆多个子订单（不同仓库/不同批次） | Order → OrderLine Link 模型 |
| R4 | access_token 有效期 | 授权码模式 ~24h，需刷新 | OAuth Token Manager 自动续期 |
| R5 | 售后类型极多 | 6 种售后类型（退款/退货/换货/维修/赔付/价保） | OT 状态枚举需完整覆盖 |
| R6 | 京东物流 JDL 独立 | open.jdl.com 是独立平台，不与电商 API 共用认证 | JDL 需独立 Connector（后置） |
| R7 | 接口按调用量收费 | 部分高价值接口（如评价、CRM）需额外购买 | 成本核算 + 调用频次监控 |

---

## 9. 与其他电商平台接口对比

| 维度 | 微商城 | 淘宝/天猫 | 拼多多 | **京东** | Shopify | Amazon |
|------|--------|----------|--------|---------|---------|--------|
| 协议 | HTTP | REST | REST | REST | GraphQL | REST |
| 签名 | — | HMAC-SHA256 | MD5 | **HMAC-SHA256** | Access Token | AWS4 |
| 核心接口数 | 341 | 37 | 32 | **42** | ~25 | ~40 |
| 增量接口 | SQL diff | 无原生 | 有 | **有（en.search）** | Webhook | Notifications |
| 售后体系 | 内嵌 | 内嵌 | 独立 | **独立(6类型)** | 内嵌 | 内嵌 |
| 双模式 | — | C+B | — | **POP+自营** | — | 3P+1P |
| 物流独立平台 | — | — | — | **JDL** | — | — |

---

> **版本**：v1.0 · 2026-07-23 · P1 调研完成
>
> **变更日志**：
>
> | 版本 | 日期 | 说明 |
> | --- | --- | --- |
> | v1.0 | 2026-07-23 | 初版 · 42 核心接口 · 8 域分类 · POP/自营标注 · 父子拆单 · HMAC-SHA256 签名 · JDL 独立体系 |
