# 01 · 抖店开放平台 API 接口清单

> **版本**：v1.0 · 2026-07-23
> **状态**：P1 调研完成 · 筛选与 AOS 数字孪生对接相关的核心接口
> **来源**：抖店开放平台文档（op.jinritemai.com）+ 多源交叉验证
> **关联**：[00-总体分析计划](./00-抖音电商AOS对接方案.md) · [02-达人佣金模型分析](./02-达人佣金模型分析.md) · [03-抖店云部署与解密方案](./03-抖店云部署与解密方案.md)

---

## 1. 筛选原则

从抖店开放平台 400+ 接口中按以下标准筛选：

| 原则 | 说明 |
|------|------|
| 数字孪生相关 | 仅选取与"将抖店映射为 AOS Ontology"相关的接口 |
| 读优先 | 优先 Source Sync（读），写回 Action（写）按需后置 |
| 内容+电商双覆盖 | 包含电商基础域 + 达人/内容/精选联盟特有域 |
| 计费标注 | 标注接口是否免费/收费（抖音按调用量计费） |

**筛选结果**：400+ 接口 → **42 个核心接口**（10 域 × ~4 接口/域）

---

## 2. 接口分类总览

| 业务域 | 接口数 | 读/写 | AOS 对应环节 |
|--------|-------|-------|-------------|
| 商品域 | 5 | 3 读 / 2 写 | Source Sync + OT + Action |
| 订单域 | 6 | 5 读 / 1 写 | Source Sync + OT + Action |
| 物流域 | 4 | 2 读 / 2 写 | Source Sync + Function |
| 售后域 | 5 | 4 读 / 1 写 | Source Sync + OT + Action |
| 会员域 | 3 | 3 读 | Source Sync + OT |
| 店铺域 | 2 | 2 读 | Source Sync（一次性） |
| 达人/精选联盟域 | 7 | 7 读 | Source Sync + OT（核心差异化） |
| 内容/直播域 | 4 | 4 读 | Source Sync + OT（后置） |
| 营销域 | 3 | 3 读 | Source Sync（后置） |
| 账单/计费域 | 3 | 3 读 | 监控 + 成本核算 |
| **合计** | **42** | | |

---

## 3. 详细接口清单

### 3.1 商品域（5 接口）

| # | 接口路径 | 方向 | 计费 | 说明 | 响应要点 |
|----|---------|------|------|------|---------|
| 1 | `/product/listV2` | 读 | 是 | 商品列表（分页） | `page`+`size`(max 100)；返回 `product_id`、`title`、`status`(0上架/1下架)、`skus`（含 `spec_prices`） |
| 2 | `/product/detail` | 读 | 是 | 单商品详情 | `product_id` 传入；返回完整：`title`、`category_leaf_id`、`skus`（含 `spec_values`）、`imgs`、`description`、`freight_template_id` |
| 3 | `/product/addV2` | 写 | 是 | 商品发布（JSON 模式） | 传 JSON 格式商品数据；返回 `product_id` |
| 4 | `/product/setOnline` | 写 | 是 | 商品上架 | `product_id` 列表（max 100 批量） |
| 5 | `/sku/price/update` | 写 | 是 | 修改 SKU 价格 | `product_id` + `sku_id` + `price`；支持批量（max 100） |

### 3.2 订单域（6 接口）

> **⚠️ 抖音订单地址/手机号加密，需解密接口（见 03-抖店云部署与解密方案.md）。**

| # | 接口路径 | 方向 | 计费 | 说明 | 响应要点 |
|----|---------|------|------|------|---------|
| 6 | `/order/searchList` | 读 | 是 | 订单列表（全量/增量） | `order_status` + `create_time_start`/`create_time_end` 或 `update_time_*`；返回 `order_id`（以 `4730`/`5120` 开头）、`order_status`、`pay_amount` |
| 7 | `/order/orderDetail` | 读 | 是 | 单笔订单详情 | `shop_order_id` 传入；返回 `sku_order_list`（子订单）、`post_addr`（**加密地址**）、`pay_type`、`coupon_amount`、`author_amount`(佣金) |
| 8 | `/order/batchDecrypt` | 读 | **免费** | **敏感信息批量解密** | `order_id` + `addr_anonymous`(密文)；返回明文地址/手机号；**仅限抖店云内调用** |
| 9 | `/order/logisticsAdd` | 写 | 是 | 单包裹发货 | `order_id` + `logistics_code`(快递公司) + `tracking_no` |
| 10 | `/order/logisticsAddMultiPack` | 写 | 是 | 多包裹发货 | 支持一单多包；`order_id` + `packages[]` |
| 11 | `/order/searchListByTime` | 读 | 是 | 按时间范围增量查询 | 按 `update_time` 增量；**推荐用于定时 Sync** |

> **订单状态枚举：**
> - `order_status`：待付款 / 待发货 / 已发货 / 已完成 / 已取消
> - 加密字段：`post_addr.encrypted_*`（姓名/手机/地址全加密）

### 3.3 物流域（4 接口）

| # | 接口路径 | 方向 | 计费 | 说明 | 响应要点 |
|----|---------|------|------|------|---------|
| 12 | `/logistics/companyList` | 读 | 是 | 快递公司列表 | 返回 `code`、`name`；含抖音签约快递 |
| 13 | `/logistics/track` | 读 | 是 | 物流轨迹实时查询 | `tracking_no` 传入；返回 `tracks`（轨迹节点数组）；**实时查询不落 Dataset** |
| 14 | `/waybill/getWaybill` | 写 | 是 | 电子面单取号 | 快递商电子面单 API |
| 15 | `/waybill/cancel` | 写 | 是 | 取消电子面单 | `waybill_id` 传入 |

### 3.4 售后域（5 接口）

| # | 接口路径 | 方向 | 计费 | 说明 | 响应要点 |
|----|---------|------|------|------|---------|
| 16 | `/afterSale/list` | 读 | 是 | 售后单列表 | `type`(退款/退货/换货) + 状态 + 时间；返回 `aftersale_id`、`order_id`、`sku_id`、`refund_amount` |
| 17 | `/afterSale/detail` | 读 | 是 | 售后单详情 | `aftersale_id` 传入；返回 `reason`、`status`、`evidence_pics`、`buyer_remark`、`seller_remark` |
| 18 | `/afterSale/Operate` | 写 | 是 | **商家审核售后** | `aftersale_id` + `operate_type`(同意/拒绝/仲裁) + `remark`；触发审核流程 |
| 19 | `/aftersale/submitEvidence` | 写 | 是 | 商家提交举证 | `aftersale_id` + `evidence_urls[]`（最多4张凭证） |
| 20 | `/afterSale/buyerExchangeConfirm` | 读 | 是 | 换货确认（买家发回确认） | 换货特有流程 |

> **售后类型枚举：**
> - `type`：退款 / 退货退款 / 换货 / 仅退款

### 3.5 会员域（3 接口）

| # | 接口路径 | 方向 | 计费 | 说明 | 响应要点 |
|----|---------|------|------|------|---------|
| 21 | `/member/list` | 读 | 是 | 会员列表（会员通） | `mobile` 或 `open_id` 过滤；返回 `open_id`、`nick_name`(加密)、`level`、`points`、`total_paid_amount` |
| 22 | `/member/detail` | 读 | 是 | 单会员详情 | `open_id` 传入；返回完整会员画像（需会员通授权） |
| 23 | `/member/tag/update` | 写 | 是 | 更新会员标签 | `open_id` + `tags[]`；用于会员运营 |

### 3.6 店铺域（2 接口）

| # | 接口路径 | 方向 | 计费 | 说明 | 响应要点 |
|----|---------|------|------|------|---------|
| 24 | `/shop/getShopCategory` | 读 | 否 | 获取店铺类目 | 返回三级类目树 `category_leaf_id` |
| 25 | `/shop/getShopInfo` | 读 | 否 | 获取店铺基本信息 | 返回 `shop_id`、`shop_name`、`shop_type`(个人/企业/品牌)、`dsr`（三维评分） |

### 3.7 达人/精选联盟域（7 接口 · 核心差异化）

> **这是抖音区别于所有其他电商平台的核心领域。详见 [02-达人佣金模型分析](./02-达人佣金模型分析.md)。**

| # | 接口路径 | 方向 | 计费 | 说明 | 响应要点 |
|----|---------|------|------|------|---------|
| 26 | `/alliance/product/list` | 读 | 是 | 精选联盟商品列表（商家端） | 商家可查看达人推广的商品；返回 `product_id`、`commission_rate`(佣金比例)、`pid`(推广位) |
| 27 | `/alliance/product/detail` | 读 | 是 | 精选联盟商品详情 | `product_id` 传入；返回佣金设置、达人推广数、销量归因 |
| 28 | `/alliance/order/list` | 读 | 是 | **精选联盟 CPS 订单** | 返回 CPS 归因订单：`order_id`、`product_id`、`author_amount`(达人佣金)、`shop_amount`(商家所得)、`platform_amount`(平台扣佣) |
| 29 | `/buyin/author/list` | 读 | 是 | 达人列表（商家可合作的） | 返回 `author_id`、`nick_name`、`fan_count`、`category_match`（品类匹配度）、`avg_gmv` |
| 30 | `/buyin/productExclusiveCoupon/list` | 读 | 是 | 抖客专属优惠券 | 抖客 CPS 场景专用 |
| 31 | `/buyin/doukeProductExclusive` | 读 | 是 | 抖客商品配置 | CPS 分销渠道配置 |
| 32 | `/alliance/elite/list` | 读 | 是 | 精英达人列表（高带货能力） | 筛选头部达人；返回 GMV、ROI、粉丝画像 |

### 3.8 内容/直播域（4 接口 · 后置）

| # | 接口路径 | 方向 | 计费 | 说明 | 响应要点 |
|----|---------|------|------|------|---------|
| 33 | `/live room/info` | 读 | 是 | 直播间信息 | `room_id` 传入；返回 `title`、`status`(直播中/已结束)、`watch_count`、`like_count` |
| 34 | `/live room/productList` | 读 | 是 | 直播间商品列表 | `room_id` 传入；返回该场次推广的商品 + 实时销量 |
| 35 | `/video/product/list` | 读 | 是 | 短视频带货商品 | `video_id` 传入；返回挂车商品列表 |
| 36 | `/data/external/shop` | 读 | 是 | 抖音开放平台数据 | 粉丝画像、内容数据（需额外授权） |

### 3.9 营销域（3 接口 · 后置）

| # | 接口路径 | 方向 | 计费 | 说明 | 响应要点 |
|----|---------|------|------|------|---------|
| 37 | `/promotion/coupon/list` | 读 | 是 | 优惠券列表 | 返回 `coupon_id`、`type`(平台券/店铺券/达人券)、`denomination`、`usage_count` |
| 38 | `/promotion/seckill/list` | 读 | 是 | 限时秒杀活动 | 返回 `activity_id`、`product_id`、`seckill_price`、`start_time` |
| 39 | `/promotion/groupBuy/list` | 读 | 是 | 平台拼团活动 | 返回拼团配置 |

### 3.10 账单/计费域（3 接口）

| # | 接口路径 | 方向 | 计费 | 说明 | 响应要点 |
|----|---------|------|------|------|---------|
| 40 | `/bill/detail` | 读 | 否 | 接口调用账单明细 | 返回按天/API 维度的调用量 + 费用 |
| 41 | `/bill/summary` | 读 | 否 | 账单汇总 | 月度费用汇总 |
| 42 | `/app/rateLimit` | 读 | 否 | 当前限流状态 | 返回各 API 当前 QPS 使用情况 |

---

## 4. 计费模型详解

> **⚠️ 抖音是唯一按调用量收费的电商平台（非免费 API）。**

| 场景 | 单价 | 说明 |
|------|------|------|
| **抖店云外**（普通部署） | 0.18 元/百次 | 标准 API 价格 |
| **抖店云内**（部署在抖店云） | **0.018 元/百次** | 降低 90% |
| 解密接口 `/order/batchDecrypt` | **免费** | 合规要求，不收费 |
| 部分配置接口（类目/店铺信息） | **免费** | 只读配置不收费 |
| RDS 数据推送 | **免费** | 订单/售后直接推送到开发者数据库 |

### 成本优化策略

| 策略 | 节省 | 说明 |
|------|------|------|
| 部署在抖店云内 | 90% | API 单价从 0.18 → 0.018 |
| 使用 RDS 数据推送 | ~50% | 订单/售后免轮询，直接推送 |
| 降低 Sync 频率 | ~30% | 非实时数据 1h 同步一次 |
| 缓存配置数据 | ~10% | 类目/快递公司等缓存 |

---

## 5. 与 AOS Source Sync 的对接映射

```
AOS Source Sync 阶段            抖店 API                            备注
─────────────────            ────────                            ────
全量拉取（首次）               /product/listV2                     商品分页
                              /order/searchList                   订单分批
                              /alliance/order/list                CPS 订单

增量同步（定时）               /order/searchListByTime             ★ 按 update_time 增量
                              /afterSale/list                     售后增量
                              /alliance/order/list                CPS 增量
                              或 RDS 数据推送                      ★ 免费，免轮询

实时查询（不落 Dataset）       /logistics/track                    物流轨迹
                              /order/orderDetail                  订单详情 On-Demand
                              /order/batchDecrypt                 ★ 解密（免费，云内）

配置参考（一次性）             /shop/getShopCategory               类目树
                              /shop/getShopInfo                   店铺信息
                              /logistics/companyList              快递公司
```

---

## 6. 签名算法（HMAC-SHA256）

```text
签名步骤：
1. 抽取业务参数到 param_json（JSON 字符串）
2. 系统参数：app_key、method、timestamp、v、sign_method、param_json
3. 参数按 key ASCII 升序排列
4. 拼接：app_key + key1value1...+ app_secret
5. HMAC-SHA256 → 十六进制小写 → sign

请求示例（POST op.jinritemai.com）：
{
  "app_key": "xxx",
  "method": "/order/searchList",
  "timestamp": "1721696400",
  "v": "2",
  "sign_method": "hmac-sha256",
  "param_json": "{\"order_status\":1,\"page\":1,\"size\":50}",
  "access_token": "xxx",
  "sign": "a1b2c3d4e5f6..."
}
```

---

## 7. 风险与注意

| # | 风险点 | 说明 | 缓解措施 |
|----|-------|------|---------|
| R1 | **接口按量计费** | 抖音是唯一收费平台（0.18 元/百次） | 部署抖店云内（降 90%）+ RDS 推送 |
| R2 | **订单地址加密** | 手机号/地址全加密，需解密接口 | batchDecrypt 免费但仅限云内 |
| R3 | access_token ~15天 | 有效期较短（比其他平台短） | OAuth Token Manager 频繁刷新 |
| R4 | 限流三维度 | app_key + API + shop 三维度限流 | 令牌桶 + 分 API 限流控制 |
| R5 | 达人数据完整性 | 达人带货数据依赖精选联盟权限 | 需申请精选联盟权限包 |
| R6 | 换货闭环复杂 | 抖音有完整换货 API 闭环 | 后置 Phase 3 接入 |

---

## 8. 与其他电商平台接口对比

| 维度 | 微商城 | 淘宝/天猫 | 拼多多 | 京东 | **抖音** | Shopify | Amazon |
|------|--------|----------|--------|------|---------|---------|--------|
| 协议 | HTTP | REST | REST | REST | REST | GraphQL | REST |
| 签名 | — | HMAC | MD5 | HMAC | **HMAC** | Token | AWS4 |
| 核心接口数 | 341 | 37 | 32 | 42 | **42** | ~25 | ~40 |
| 增量接口 | SQL diff | 无原生 | 有 | 有 | **有+RDS推送** | Webhook | Notifications |
| 售后体系 | 内嵌 | 内嵌 | 独立 | 独立 | **独立(含换货)** | 内嵌 | 内嵌 |
| 接口计费 | — | — | — | — | **⚠️ 按量收费** | — | — |
| 数据加密 | — | — | 部分 | — | **⚠️ 全加密** | — | — |
| 达人体系 | — | 淘宝客 | 多多进宝 | — | **精选联盟** | — | — |

---

> **版本**：v1.0 · 2026-07-23 · P1 调研完成
>
> **变更日志**：
>
> | 版本 | 日期 | 说明 |
> | --- | --- | --- |
> | v1.0 | 2026-07-23 | 初版 · 42 核心接口 · 10 域分类 · 达人/精选联盟 7 接口 · 计费模型详解 · 解密链路 · RDS 推送策略 |
