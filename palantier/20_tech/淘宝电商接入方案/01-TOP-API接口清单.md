# 01 · 淘宝开放平台（TOP）API 接口清单

> **版本**：v1.0 · 2026-07-22
> **状态**：P1 调研完成 · 筛选与 AOS 数字孪生对接相关的核心接口
> **来源**：淘宝开放平台文档 + 多源交叉验证
> **关联**：[00-总体分析计划](./00-淘宝天猫AOS对接方案-总体分析计划.md) · [02-天猫Schema体系分析](./02-天猫Schema体系分析.md)

---

## 1. 筛选原则

从 TOP 平台 200+ 接口中按以下标准筛选：

| 原则 | 说明 |
|------|------|
| 数字孪生相关 | 仅选取与"将淘宝天猫店铺映射为 AOS Ontology"相关的接口 |
| 读优先 | 优先 Source Sync（读），写回 Action（写）按需后置 |
| 企业可用 | 标注权限要求（公开/商家授权/增值权限），避免不可达接口 |
| 天猫兼容 | 标注淘宝 C 店 与天猫品牌店的接口差异 |

**筛选结果**：200+ 接口 → **37 个核心接口**（8 域 × ~4-5 接口/域）

---

## 2. 接口分类总览

| 业务域 | 接口数 | 读/写 | AOS 对应环节 |
|--------|-------|-------|-------------|
| 商品域 | 10 | 6 读 / 4 写 | Source Sync + OT |
| 订单域 | 6 | 5 读 / 1 写 | Source Sync + OT + Action |
| 物流域 | 5 | 4 读 / 1 写 | Source Sync + Function |
| 会员域 | 4 | 4 读 | Source Sync（需增值权限） |
| 店铺域 | 2 | 2 读 | Source Sync（一次性） |
| 评价域 | 3 | 3 读 | Source Sync + OT |
| 类目/属性 | 3 | 3 读 | 配置参考 |
| 天猫专属 | 4 | 2 读 / 2 写 | 天猫 Action 写回 |
| **合计** | **37** | | |

---

## 3. 详细接口清单

### 3.1 商品域（10 接口）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 1 | `taobao.items.onsale.get` | 读 | 商家授权 | 获取当前卖家出售中的商品列表 | 分页 `page_no` + `page_size`(max 200)；返回 `num_iid`、`title`、`price`、`num`、`pic_url`、`list_time` |
| 2 | `taobao.items.inventory.get` | 读 | 商家授权 | 获取仓库中的商品列表 | 同上分页；返回 `num_iid`、`title`、`price`、`num`、`approve_status` |
| 3 | `taobao.item.get` | 读 | 公开 | 获取单个商品全部详情 | `fields` 按需指定：`num_iid,title,price,desc,item_imgs,sku,props_name,has_discount` 等 |
| 4 | `taobao.item.sku.get` | 读 | 公开 | 获取商品 SKU 列表 | `fields`：`sku_id,properties,quantity,price,outer_id`；返回 SKU 规格+库存 |
| 5 | `taobao.items.seller.list.get` | 读 | 商家授权 | 批量获取商品详细信息 | 传入 `num_iids` 列表（逗号分隔），最多 20 个；返回完整商品详情数组 |
| 6 | `taobao.itemcats.get` | 读 | 公开 | 获取标准商品类目 | `parent_cid=0` 获取一级类目；递归获取子类目；类目树 >20,000 节点 |
| 7 | `taobao.itemprops.get` | 读 | 公开 | 获取类目属性 | `cid` 传入类目 ID；返回该类目下的属性列表（品牌、规格等） |
| 8 | `taobao.item.update` | 写 | 商家授权 | 修改商品信息（淘宝） | 支持改价格、标题、库存、描述；`num_iid` + 修改字段 |
| 9 | `taobao.item.quantity.update` | 写 | 商家授权 | 商品/SKU 库存修改 | `num_iid` + `quantity` + `type`（1全量/2增量）；或传 `sku_id` 精确改 SKU |
| 10 | `taobao.skus.quantity.update` | 写 | 商家授权 | 批量 SKU 库存修改 | `skuid_quantities` JSON 编码；每次最多 20 个 SKU |

### 3.2 订单域（6 接口）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 11 | `taobao.trades.sold.get` | 读 | 商家授权 | 查询已卖出订单列表 | 按 `start_created`/`end_created` 时间范围分页；返回 `tid`、`payment`、`status`、`buyer_nick`、`created` |
| 12 | `taobao.trades.sold.increment.get` | 读 | 商家授权 | 增量查询已卖出订单 | 按 `start_modified`/`end_modified` 获取变更订单；**推荐用于定时 Sync** |
| 13 | `taobao.trade.fullinfo.get` | 读 | **企业账号** | 获取订单完整详情 | `fields` 含 `receiver_*` 时需额外权限；返回订单行（`orders` 数组）、物流、支付、优惠全量 |
| 14 | `taobao.trade.get` | 读 | 商家授权 | 获取单笔订单基础信息 | 比 `fullinfo` 字段少，适合列表后批量补充；需传入 `tid` |
| 15 | `taobao.trade.memo.update` | 写 | 商家授权 | 修改订单备注/标星 | `tid` + `memo` + `flag`（1-5 星）；用于 Action 写回场景 |
| 16 | `taobao.trades.sold.query` | 读 | 商家授权 | 按收件人信息查询订单 | `receiver_name`/`receiver_mobile`/`receiver_phone` 三选一；用于售后查找 |

### 3.3 物流域（5 接口）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 17 | `taobao.logistics.orders.get` | 读 | 商家授权 | 获取物流订单列表 | `tid` 或 `fields` 过滤；返回 `out_sid`（运单号）、`company_name`、`status` |
| 18 | `taobao.logistics.trace.search` | 读 | 公开 | 物流轨迹实时查询 | `tid` 传入；返回 `transit_step_info`（轨迹节点数组）、`status`、`company_name`；**实时查询不落 Dataset** |
| 19 | `taobao.logistics.online.send` | 写 | 商家授权 | 在线发货（含货到付款） | `tid` + `out_sid` + `company_code`；触发发货状态变更 |
| 20 | `taobao.logistics.dummy.send` | 写 | 商家授权 | 无需物流（虚拟）发货 | `tid` 即可；适用虚拟商品 |
| 21 | `taobao.delivery.templates.get` | 读 | 商家授权 | 获取运费模板 | `fields`：`template_id,name,supports,created`；系统配置读取 |

### 3.4 会员域（4 接口）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 22 | `taobao.crm.members.get` | 读 | **增值权限** | 获取店铺会员列表 | 需 CRM 增值包；`grade`（等级 T1-T6）、`trade_amount`（消费额）、`trade_count`（交易次数）、`item_num`（购买商品数） |
| 23 | `taobao.user.seller.get` | 读 | 商家授权 | 获取卖家用户信息 | 返回 `nick`、`user_id`、`sex`、`avatar`；用于判断店铺类型 |
| 24 | `taobao.user.buyer.get` | 读 | 买家授权 | 获取买家信息 | `fields`：`nick,sex,buyer_credit,avatar`；**不返回手机号**（隐私保护） |
| 25 | `taobao.user.openuid.getbynick` | 读 | 商家授权 | nick → openuid 批量转换 | 最大查询 30 个；用于跨系统用户关联 |

### 3.5 店铺域（2 接口）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 26 | `taobao.shop.get` | 读 | 公开 | 获取店铺基本信息 | `nick` 传入卖家 nick；返回 `sid`、`title`、`desc`、`bulletin`、`pic_path`、`shop_score`（DSR 三项评分） |
| 27 | `taobao.sellercats.list.get` | 读 | 商家授权 | 获取店铺自定义类目 | `nick` 传入；返回店铺内自建的商品分组类目 |

### 3.6 评价域（3 接口）

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 28 | `taobao.traderates.get` | 读 | 商家授权 | 搜索评价信息 | `tid` 或 `num_iid` 传入；返回 `tid`、`oid`、`role`、`nick`、`result`、`content`、`created` |
| 29 | `tmall.traderate.feeds.get` | 读 | 商家授权 | 天猫评价/追评/语义标签 | 比 `traderates.get` 多追评内容和语义标签字段 |
| 30 | `taobao.traderate.add` | 写 | 商家授权 | 新增单个评价 | 卖家回评；`tid` + `oid` + `result`(good/neutral/bad) + `content` |

### 3.7 类目/属性域（已在 3.1 中计入）

> #6 `taobao.itemcats.get`（类目）、#7 `taobao.itemprops.get`（属性）已在商品域中计入，此处不再重复。
>
> 补充：

| # | 接口 | 方向 | 权限 | 说明 | 响应要点 |
|----|------|------|------|------|---------|
| 31 | `taobao.itemcats.authorize.get` | 读 | 商家授权 | 获取已授权类目及品牌 | 天猫商品发布前必查；返回品牌 `brand_id` + 类目 `cid` 列表 |

### 3.8 天猫专属 Schema 体系（4 接口）

> 天猫商品发布/更新走 Schema XML 体系，详见 [02-天猫Schema体系分析.md](./02-天猫Schema体系分析.md)。

| # | 接口 | 方向 | 权限 | 说明 | AOS 适用场景 |
|----|------|------|------|------|------------|
| 32 | `tmall.item.add.schema.get` | 读 | 天猫授权 | 获取商品发布规则（Schema XML） | 天猫 Action 写回 — 获取规则 |
| 33 | `tmall.item.schema.add` | 写 | 天猫授权 | 天猫商品发布（Schema XML） | 天猫 Action 写回 — 创建商品 |
| 34 | `tmall.item.update.schema.get` | 读 | 天猫授权 | 获取商品全量更新规则 | 天猫 Action 写回 — 获取全量更新规则 |
| 35 | `tmall.item.schema.update` | 写 | 天猫授权 | 天猫商品全量更新 | 天猫 Action 写回 — 全量更新商品 |
| 36 | `tmall.item.increment.update.schema.get` | 读 | 天猫授权 | 获取增量更新规则 | 天猫 Action 写回 — 获取增量规则 |
| 37 | `tmall.item.schema.increment.update` | 写 | 天猫授权 | 天猫商品增量更新（标题/描述等） | 天猫 Action 写回 — 增量更新商品 |

---

## 4. 权限分级

| 级别 | 要求 | 接口数 | 代表接口 |
|------|------|-------|---------|
| **公开** | AppKey 即可 | 6 | `taobao.item.get`、`taobao.item.sku.get`、`taobao.itemcats.get`、`taobao.shop.get`、`taobao.logistics.trace.search` |
| **商家授权** | OAuth 2.0 SessionKey | 22 | `taobao.trades.sold.get`、`taobao.items.onsale.get`、`taobao.logistics.orders.get` |
| **企业账号** | 企业认证 + 业务场景说明 | 1 | `taobao.trade.fullinfo.get` |
| **增值权限** | 需购买 CRM 增值包 | 1 | `taobao.crm.members.get` |
| **天猫专属** | 天猫店铺授权 | 6 | `tmall.item.add.schema.get` 等 Schema 接口 |

---

## 5. 与 AOS Source Sync 的对接映射

```
AOS Source Sync 阶段            TOP API                       备注
─────────────────            ────────                       ────
全量拉取（首次）               taobao.items.onsale.get        分页遍历
                              taobao.trades.sold.get          按时间窗口分批
                              taobao.item.sku.get             逐商品获取
                              
增量同步（定时）               taobao.trades.sold.increment.get  按 modified 时间
                              taobao.items.onsale.get (按 list_time 过滤)

实时查询（不落 Dataset）       taobao.logistics.trace.search   物流轨迹
                              taobao.trade.fullinfo.get        订单详情 On-Demand

配置参考（一次性）             taobao.shop.get                 店铺信息
                              taobao.itemcats.get              类目树
                              taobao.itemcats.authorize.get    授权类目
```

---

## 6. 风险与注意

| # | 风险点 | 说明 | 缓解措施 |
|----|-------|------|---------|
| R1 | `trade.fullinfo.get` 需企业账号 | 个人/自用型应用无法调用 | AOS 对接前先完成企业认证 |
| R2 | CRM 接口需要增值包 | 会员数据（T1-T6 等级）需额外购买 | Phase 1 可跳过会员域，Phase 2 再补齐 |
| R3 | 限流（500 次/秒企业、50 次/秒个人） | 全量拉取时容易触发 | Source Sync 中内置速率控制 + 退避重试 |
| R4 | Access Token 24 小时过期 | 定时 Sync 可能因 Token 过期中断 | OAuth Token Manager 自动续期 |
| R5 | 接口可能下线/变更 | 淘宝 API 版本迭代快（如 Schema 接口取代旧接口） | 变更检测 + 文档持续追踪 |
| R6 | 数据隐私合规 | 买家手机号/地址仅订单内可用，不可独立获取 | 不建独立地址 Object；地址仅作为订单 Prop |

---

> **版本**：v1.0 · 2026-07-22 · P1 调研完成
>
> **变更日志**：
>
> | 版本 | 日期 | 说明 |
> | --- | --- | --- |
> | v1.0 | 2026-07-22 | 初版 · 37 核心接口 · 8 域分类 · 权限分级 · AOS Sync 映射 |
