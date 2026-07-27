# 01 · 拼多多开放平台（PDD）API 接口清单

> **版本**：v1.0 · 2026-07-23
> **状态**：P1 调研完成 · 筛选与 AOS 数字孪生对接相关的核心接口
> **来源**：拼多多开放平台文档（open.pinduoduo.com）+ 多源交叉验证
> **关联**：[00-总体分析计划](./00-拼多多AOS对接方案.md)

---

## 1. 筛选原则

从拼多多开放平台 300+ 接口中按以下标准筛选：

| 原则 | 说明 |
|------|------|
| 数字孪生相关 | 仅选取与"将拼多多店铺映射为 AOS Ontology"相关的接口 |
| 读优先 | 优先 Source Sync（读），写回 Action（写）按需后置 |
| 商家可用 | 标注权限要求（公开/商家授权/需报备），避免不可达接口 |
| 拼团特有 | 标注拼团（group_status）相关接口与字段 |

**筛选结果**：300+ 接口 → **32 个核心接口**（9 域 × ~3-4 接口/域）

---

## 2. 接口分类总览

| 业务域 | 接口数 | 读/写 | AOS 对应环节 |
|--------|-------|-------|-------------|
| 店铺域 | 2 | 2 读 | Source Sync（一次性） |
| 商品域 | 5 | 3 读 / 2 写 | Source Sync + OT + Action |
| 订单域 | 6 | 5 读 / 1 写 | Source Sync + OT + Action |
| 物流域 | 4 | 3 读 / 1 写 | Source Sync + Function |
| 售后域 | 5 | 4 读 / 1 写 | Source Sync + OT + Action |
| 多多进宝域 | 4 | 4 读 | Source Sync + OT |
| 营销域 | 2 | 2 读 | Source Sync（后置） |
| 评价/店铺分 | 2 | 2 读 | Source Sync + OT |
| 发票域 | 2 | 2 读 | Source Sync（后置） |
| **合计** | **32** | | |

---

## 3. 详细接口清单

### 3.1 店铺域（2 接口）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 1 | `pdd.mall.info.get` | 读 | 商家授权 | 获取店铺基本信息 | 返回 `mall_id`、`mall_name`、`logo`、`mall_desc`、`merchant_type`（个人/企业/旗舰店） |
| 2 | `pdd.goods.cats.get` | 读 | 公开 | 获取标准商品类目树 | `parent_cat_id` 递归获取；返回 `cat_id`、`cat_name`、`level`、`is_parent`；类目树三级结构 |

### 3.2 商品域（5 接口）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 3 | `pdd.goods.list.get` | 读 | 商家授权 | 商品列表查询 | 分页 `page_number` + `page_size`(max 100)；返回 `goods_id`、`goods_name`、`goods_price`、`sku_list`、`goods_status`（1上架/2下架） |
| 4 | `pdd.goods.detail.get` | 读 | 商家授权 | 单商品详情 | `goods_id` 传入；返回 SPU+SKU 全量信息：`goods_name`、`cat_id`、`goods_gallery`（图组）、`sku_list`（含 `spec_specs`）、`goods_desc`、`cost_price` |
| 5 | `pdd.goods.quantity.update` | 写 | 商家授权 | 修改商品库存 | `goods_id` + `sku_id` + `quantity`；支持全量/增量两种模式 |
| 6 | `pdd.goods.update` | 写 | 商家授权 | 修改商品信息 | `goods_id` + 待修改字段（`goods_name`/`goods_price`/`cat_id`/`image_url`）；单个修改 |
| 7 | `pdd.goods.commit.detail.get` | 读 | 商家授权 | 查询商品发布规则 | `cat_id` 传入；返回该类目下商品发布必填/选填字段 Schema；**类似天猫 Schema 但为 JSON 格式** |

### 3.3 订单域（6 接口）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 8 | `pdd.order.list.get` | 读 | 商家授权 | 订单列表查询（全量） | `order_status` + `start_confirm_at`/`end_confirm_at` 时间范围；返回 `order_sn`、`order_status`、`pay_amount`、`goods_list`、`country`、`province` |
| 9 | `pdd.order.information.get` | 读 | 商家授权 | 单笔订单详情 | `order_sn` 传入；返回完整：`goods_list`（SKU行）、`address`（收货人加密）、`logistics_id`、`pay_time`、`refund_status` |
| 10 | `pdd.order.number.list.increment.get` | 读 | 商家授权 | **增量订单号列表** | `start_updated_at`/`end_updated_at` 按 modified 时间；返回变动的 `order_sn` 列表 + `order_status`；**推荐用于定时 Sync**；粒度可选 15min/30min/1h/4h |
| 11 | `pdd.order.status.get` | 读 | 商家授权 | 批量查询订单状态 | `order_sns` 逗号分隔（max 100）；返回 `order_sn` + `order_status`；轻量级状态轮询 |
| 12 | `pdd.order.note.update` | 写 | 商家授权 | 修改订单备注 | `order_sn` + `note`（文本）+ `tag`（星标 1-5）；用于 Action 写回场景 |
| 13 | `pdd.order.basic.information.get` | 读 | 商家授权 | 批量订单基本信息 | `order_sns` 列表；返回轻量订单信息（不含地址详情）；适合列表页批量加载 |

> **拼团状态字段说明：**
> - `group_status`：0 未成团 / 1 已成团 / 2 拼团失败
> - `order_status`：0 待付款 / 1 待发货 / 2 已发货 / 3 已确认收货 / 4 已完成 / 5 已取消

### 3.4 物流域（4 接口）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 14 | `pdd.logistics.companies.get` | 读 | 公开 | 获取快递公司列表 | 返回 `id`、`code`、`name`；**拼多多需快递公司自己注册编码**（不同于淘宝菜鸟统一编码） |
| 15 | `pdd.logistics.online.send` | 写 | 商家授权 | 在线发货 | `order_sn` + `logistics_id`（快递公司编码）+ `tracking_no`（运单号）；触发发货状态变更 |
| 16 | `pdd.logistics.ordertrace.get` | 读 | 商家授权 | 物流轨迹实时查询 | `order_sn` 或 `tracking_no` 传入；返回 `trace_list`（轨迹节点数组）；**实时查询不落 Dataset** |
| 17 | `pdd.logistics.address.get` | 读 | 商家授权 | 获取发货地址列表 | 商家后台配置的仓库/发货地址簿；返回 `address_id`、`province`、`city`、`district`、`detail` |

### 3.5 售后域（5 接口）

> **拼多多售后为独立 API 群（`pdd.refund.*`），与订单解耦。**

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 18 | `pdd.refund.list.get` | 读 | 商家授权 | 售后单列表查询 | `after_sales_status` + 时间范围；返回 `refund_id`、`order_sn`、`goods_id`、`refund_amount`、`after_sales_type`（退款/退货退款/换货） |
| 19 | `pdd.refund.information.get` | 读 | 商家授权 | 单笔售后详情 | `refund_id` 传入；返回完整：`refund_reason`、`refund_status`、`evidence_list`（凭证图）、`buyer_remark`、`seller_remark` |
| 20 | `pdd.refund.agree` | 写 | 商家授权 | 商家同意退款 | `refund_id` + `address_id`（退货收货地址）；触发自动退款流程 |
| 21 | `pdd.refund.reject` | 写 | 商家授权 | 商家拒绝退款 | `refund_id` + `reject_reason` + `evidence_list`；拒绝需举证 |
| 22 | `pdd.refund.status.get` | 读 | 商家授权 | 批量查询售后状态 | `refund_ids` 列表；返回 `refund_id` + `after_sales_status`；轻量级状态轮询 |

> **售后状态枚举：**
> - `after_sales_status`：1 待商家处理 / 2 待买家退货 / 3 待商家确认收货 / 4 待平台处理 / 5 退款成功 / 6 退款关闭

### 3.6 多多进宝域（4 接口）

> **多多进宝（`pdd.ddk.*`）是拼多多的 CPS 分销体系，类似淘宝客。**

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 23 | `pdd.ddk.goods.recommend.get` | 读 | 商家授权 | 多多进宝商品推荐列表 | 返回 `goods_id`、`goods_name`、`goods_price`、`min_group_price`（拼团价）、`promotion_rate`（佣金比例%）、`coupon_price`（优惠券） |
| 24 | `pdd.ddk.goods.search` | 读 | 商家授权 | 多多进宝商品搜索 | 关键词 + 类目筛选；返回带佣金信息的商品列表 |
| 25 | `pdd.ddk.order.list.increment.get` | 读 | 商家授权 | **多多进宝订单增量** | `start_update_time`/`end_update_time`；返回 CPS 归因订单：`order_sn`、`goods_id`、`promotion_amount`（佣金金额）、`p_id`（推广位ID） |
| 26 | `pdd.ddk.goods.pid.generate` | 读 | 商家授权 | 生成推广位 PID | `number`（批量生成数）；返回 `pid` 列表用于渠道追踪 |

### 3.7 营销域（2 接口 · 后置）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 27 | `pdd.promotion.limit.discount.list.get` | 读 | 商家授权 | 限时秒杀活动列表 | 返回 `activity_id`、`goods_id`、`activity_price`、`start_time`、`end_time`、`stock_limit` |
| 28 | `pdd.promotion.coupon.list.get` | 读 | 商家授权 | 店铺优惠券列表 | 返回 `coupon_id`、`coupon_name`、`denomination`、`min_consumption`、`validity_type`、`quantity` |

### 3.8 评价/店铺评分域（2 接口）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 29 | `pdd.mall.rating.get` | 读 | 商家授权 | 店铺 DSR 评分 | 返回 `desc_score`（描述相符）、`service_score`（服务态度）、`logistics_score`（物流服务）；三维 + 综合分 |
| 30 | `pdd.goods.comment.list.get` | 读 | 商家授权 | 商品评价列表 | `goods_id` + 分页；返回 `comment_id`、`star`（1-5）、`content`、`images`、`is_append`（是否追评）、`created_at` |

### 3.9 发票域（2 接口 · 后置）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 31 | `pdd.invoice.apply.get` | 读 | 商家授权 | 获取发票申请列表 | 返回 `invoice_id`、`order_sn`、`invoice_type`（电子/增值税）、`title`、`tax_no` |
| 32 | `pdd.invoice.detail.get` | 读 | 商家授权 | 发票详情 | `invoice_id` 传入；返回完整开票信息 + PDF 下载地址 |

---

## 4. 权限分级

| 级别 | 要求 | 接口数 | 代表接口 |
|------|------|-------|---------|
| **公开** | AppKey 即可 | 2 | `pdd.goods.cats.get`、`pdd.logistics.companies.get` |
| **商家授权** | OAuth 2.0 access_token | 28 | `pdd.order.list.get`、`pdd.goods.list.get`、`pdd.refund.list.get` |
| **多多进宝** | 多多进宝权限包 | 4 | `pdd.ddk.*` 系列 |
| **需报备** | 高频调用需提前报备 | 部分 | 单接口 QPS > 100 时需向平台申请 |

---

## 5. 与 AOS Source Sync 的对接映射

```
AOS Source Sync 阶段            PDD API                               备注
─────────────────            ────────                               ────
全量拉取（首次）               pdd.goods.list.get                     分页遍历
                              pdd.order.list.get                     按时间窗口分批（90天内）
                              pdd.goods.detail.get                   逐商品获取SKU
                              
增量同步（定时）               pdd.order.number.list.increment.get    ★ 按 updated_at 增量（核心）
                              pdd.refund.list.get                    按状态过滤
                              pdd.ddk.order.list.increment.get       多多进宝增量

实时查询（不落 Dataset）       pdd.logistics.ordertrace.get           物流轨迹
                              pdd.order.information.get              订单详情 On-Demand

配置参考（一次性）             pdd.mall.info.get                      店铺信息
                              pdd.goods.cats.get                     类目树
                              pdd.logistics.companies.get            快递公司编码
```

### 增量同步推荐策略

| 数据域 | 推荐接口 | 频率 | 说明 |
|--------|---------|------|------|
| 订单 | `pdd.order.number.list.increment.get` | 15 min | 拼团订单状态变更频繁 |
| 商品 | `pdd.goods.list.get` | 1 h | 商品变更频率较低 |
| 售后 | `pdd.refund.list.get` | 30 min | 售后状态变更 |
| 多多进宝 | `pdd.ddk.order.list.increment.get` | 30 min | CPS 归因订单 |
| 物流轨迹 | `pdd.logistics.ordertrace.get` | On-Demand | 实时查询，不落表 |

---

## 6. 签名算法详解（MD5）

> **拼多多使用 MD5 签名，区别于淘宝的 HMAC-SHA256。**

```text
签名步骤：
1. 将所有请求参数（不含 sign）按 key 首字母 ASCII 升序排列
2. 拼接所有 keyvalue（不含分隔符）：
   key1value1key2value2...keyNvalueN
3. 在拼接串前后各追加 client_secret：
   client_secret + 步骤2结果 + client_secret
4. MD5 哈希 → 转为大写 32 位十六进制字符串
5. 将 sign 放入请求参数中发送

请求参数示例（POST open-api.pinduoduo.com）：
{
  "type": "pdd.order.list.get",
  "client_id": "xxx",
  "timestamp": 1721696400,
  "data_type": "JSON",
  "access_token": "xxx",
  "page_number": 1,
  "page_size": 100,
  "order_status": 1,
  "sign": "A1B2C3D4E5F6..."
}
```

---

## 7. 风险与注意

| # | 风险点 | 说明 | 缓解措施 |
|----|-------|------|---------|
| R1 | MD5 签名安全性较低 | MD5 已被认为不安全，但拼多多接口侧稳定 | AOS Connector 层需支持 MD5 签名插件 |
| R2 | access_token 24h 过期 | 定时 Sync 可能因 Token 过期中断 | OAuth Token Manager 自动刷新（refresh_token） |
| R3 | 地址/手机号加密 | 收货人信息需解密后使用 | 需解密插件（类似抖音） |
| R4 | 拼团超时关闭 | 24h 未成团订单自动关闭，状态变更需及时同步 | 增量 Sync 频率 ≥ 15 min |
| R5 | 多多进宝佣金结算延迟 | CPS 订单佣金有结算周期（T+15） | 佣金数据标注 `pending` 状态，结算后回写 |
| R6 | 限流（默认较低，需报备提升） | 全量拉取易触发 | Source Sync 内置速率控制 + 退避重试 |

---

## 8. 与其他电商平台接口对比

| 维度 | 微商城 | 淘宝/天猫 | **拼多多** | Shopify | Amazon |
|------|--------|----------|-----------|---------|--------|
| 协议 | HTTP (ThinkPHP) | REST | REST | GraphQL | REST |
| 签名 | — | HMAC-SHA256 | **MD5（大写32位）** | Access Token | AWS4-HMAC-SHA256 |
| 核心接口数 | 341 | 37 | **32** | ~25 query | ~40 |
| 增量接口 | SQL diff | 无原生 | **有（15min粒度）** | Webhook | Notifications |
| 售后体系 | 内嵌订单 | 内嵌订单 | **独立 API 群** | 内嵌订单 | 内嵌订单 |
| CPS 分销 | 无 | 淘宝客 | **多多进宝** | 无 | Amazon Associates |

---

> **版本**：v1.0 · 2026-07-23 · P1 调研完成
>
> **变更日志**：
>
> | 版本 | 日期 | 说明 |
> | --- | --- | --- |
> | v1.0 | 2026-07-23 | 初版 · 32 核心接口 · 9 域分类 · MD5 签名详解 · 增量同步策略 · 权限分级 |
