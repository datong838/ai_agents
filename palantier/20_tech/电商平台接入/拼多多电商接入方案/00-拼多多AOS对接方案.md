# 拼多多 · AOS 数字孪生对接方案 — 总体分析计划

| 字段 | 内容 |
|------|------|
| 状态 | **方案 only · 调研阶段** · 2026-07-22 |
| 版本 | **v1.0** · 初始分析计划 |
| 目录 | `docs/palantier/20_tech/拼多多电商接入方案/` |
| 覆盖范围 | **拼多多商家后台系统** — 商品 · 订单 · 物流 · 售后 · 店铺 · 营销 · 多多进宝 |
| 关联 | 微商城模板：[00-Niushop微商城AOS对接方案](../微商城电商接入方案/00-Niushop微商城AOS对接方案.md) · [220w 差距分析](../220w-与目标系统差距对照分析.md) · [220plan 开发计划](../220plan-分阶段开发与里程碑计划.md) |
| 原则 | **复用微商城 8 域 Ontology 模板 → 拼多多仅做适配增量** — 不从头建模 |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 | 全文 |
| 先方案后代码 | 通过前不写行业定制码；缺口回馈**通用平台** |
| 整体孪生 | 目标是拼多多商家业务世界在 AOS 可运营、可感知、可治理 |
| 模板复用 | 微商城（Niushop）8 大领域模型为基线，仅适配差异点 |
| 零行业定制码 | 平台差异通过 Connector 配置 / OT / OKF 映射消解，禁止 `pdd-*` Host 分支 |

---

## 1. 一句话目标

> 将拼多多店铺（商品 · 订单 · 物流 · 售后 · 营销 · 多多进宝 · 店铺 · 评价）  
> **整体映射**为 AOS 数字孪生，**复用**微商城（Niushop）已验证的 8 大领域模型，  
> 仅针对拼多多开放平台（`pdd.*` API）的 **MD5 签名 + OAuth 2.0 模式** 做适配层。

```text
微商城（基准模板）              拼多多（适配增量）
────────────────              ────────────────
JDBC 直连 MySQL               REST API 网关 + MD5 签名
302 张表单表 Sync              OAuth 2.0 + access_token 轮换
site_id 多租户                 mall_id 多店铺隔离
商品/订单/会员/... 8 域        同 8 域，增量接口 + 售后独立域
Funnel 订单状态机              更复杂：待成团 → 已成团 → 待发货...
```

---

## 2. 拼多多平台画像

### 2.1 平台概况

| 维度 | 内容 |
|------|------|
| 开放平台 | [open.pinduoduo.com](https://open.pinduoduo.com) |
| API 命名 | 全部 `pdd.*` 前缀，如 `pdd.order.list.get` |
| 网关地址 | `https://open-api.pinduoduo.com/` |
| 沙箱地址 | `https://open-api.pinduoduo.com/sandbox` |
| 认证方式 | OAuth 2.0（authorization_code）→ `access_token`（有效期 ~24h） |
| 签名算法 | **MD5**（参数首字母升序 + 前后追加 client_secret → 大写 32 位） |
| 时间戳要求 | 与服务器时间差值 ≤ 5 分钟 |
| 数据格式 | JSON（推荐）或 XML，`data_type=JSON` |
| 速率限制 | 单接口 500 QPS（需报备），默认较低 |
| 增量接口 | `pdd.order.number.list.increment.get`（增量订单号） |
| 应用类型 | 自研系统（商家后台）/ ISV（服务市场） |

### 2.2 与淘宝/天猫的关键差异

| 维度 | 淘宝/天猫（TOP） | 拼多多（PDD） |
|------|-----------------|-------------|
| 签名算法 | HMAC-SHA256 | **MD5**（安全等级较低，但接口侧稳定） |
| 类目体系 | 统一类目树 20,000+ 节点 | `pdd.goods.cats.get` 标准类目 |
| 商品发布 | Schema XML 体系（天猫） | 扁平 JSON 提交 `pdd.goods.add` |
| 订单状态 | trade_status 枚举 | 数字编码（0/1/2...）+ 拼团特有状态 |
| 售后体系 | 退款/退货退款 | **独立售后 API 群**（`pdd.refund.*`）+ 客服介入 |
| 物流体系 | 菜鸟统一编码 | 快递公司自己注册 + `pdd.logistics.*` |
| 增量机制 | 无原生增量 | **有增量接口**（15min/30min/1h/4h 粒度） |
| 分销体系 | 淘宝客 | **多多进宝**（`pdd.ddk.*` 独立 API 群） |

---

## 3. 整体孪生范围（按域）

> **原则：** 拼多多开放平台 API 一一对应商家后台功能。  
> 不是所有 API 都要进孪生，**按业务对象建模**。

### 3.1 域分级

| 级 | 名称 | 业务含义 | API 源头 | AOS 目标 | 波次 |
|----|------|----------|----------|----------|------|
| **T0** | 店铺基础 | 店铺信息、授权、类目 | `pdd.mall.info.get` 等 | Shop / Category | W1 |
| **T1** | 商品 | SPU/SKU/类目/上下架/库存 | `pdd.goods.list.get` / `detail.get` / `cats.get` | Goods / GoodsSku / Category | W1 |
| **T2** | 订单 | 订单头、SKU 行、拼团、地址 | `pdd.order.list.get` / `information.get` / `increment.get` | Order / OrderLine | W1 |
| **T3** | 物流 | 发货、快递公司、轨迹 | `pdd.logistics.online.send` / `companies.get` / `ordertrace.get` | ExpressPackage / Logistics | W1 |
| **T4** | 售后 | 退款/退货退款/换货（独立体系） | `pdd.refund.list.get` / `information.get` / `agree` | Refund / ReturnOrder | W2 |
| **T5** | 店铺与评分 | 店铺信息、DSR 评分 | `pdd.mall.info.get` | ShopScore | W2 |
| **T6** | 多多进宝 | 推广位、佣金、订单归因 | `pdd.ddk.*` | Promotion / Commission | W2 |
| **T7** | 营销活动 | 限时秒杀、品牌清仓 | `pdd.promotion.*` | Campaign（可薄） | W3 |
| **T8** | 发票与仓储 | 电子发票、仓配管理 | `pdd.invoice.*` / `pdd.stock.*` | Invoice / Warehouse | W3 |

**整体孪生退出（MVP）** = **T0～T4 在 AOS 可检索、可关联、可上态势**；T5～T8 有清单与接入策略。

---

## 4. Ontology 目标态（对象与关系）

### 4.1 Object Type 清单（核心 · 复用微商城模型 + 拼多多增量）

| Object Type | 主键 | 来源 API | 说明 | vs 微商城增量 |
|-------------|------|----------|------|-------------|
| **Shop** | mallId | `pdd.mall.info.get` | 店铺根对象 | 无（微商城无此概念，多 mall 权限） |
| **Goods** | goodsId | `pdd.goods.list.get` | SPU | 基本对齐 |
| **GoodsSku** | skuId | goods 内嵌 `sku_list` | 交易落点 | 基本对齐 |
| **GoodsCategory** | catId | `pdd.goods.cats.get` | 类目树 | 单独 API 获取，非自建 |
| **Order** | orderSn | `pdd.order.list.get` | **故事核** | 新增 `group_status`（拼团状态）Prop |
| **OrderLine** | orderSn+skuId | order 内嵌 `item_list` | 订单行 | 基本对齐 |
| **ExpressPackage** | logisticsId | `pdd.logistics.online.send` | 包裹 | 快递编码从 `pdd.logistics.companies.get` 获取 |
| **LogisticsTrace** | tracingId | `pdd.logistics.ordertrace.get` | 物流轨迹 | 实时查询（不落表，Function 型） |
| **Refund** | refundId | `pdd.refund.list.get` | 售后单 | **独立域**，微商城退款嵌在 Pay 内 |
| **Promotion** | goodsId | `pdd.ddk.*` | 多多进宝 | 微商城无对应，新建 |
| **Invoice** | invoiceId | `pdd.invoice.*` | 电子发票 | 微商城无对应 |

### 4.2 Link Type（核心）

| Link | from → to |
|------|-----------|
| `Order.onShop` | Order → Shop |
| `Order.lines` | Order → OrderLine |
| `OrderLine.ofSku` | OrderLine → GoodsSku |
| `GoodsSku.ofGoods` | GoodsSku → Goods |
| `Goods.inCategory` | Goods → GoodsCategory |
| `Order.hasPackage` | Order → ExpressPackage |
| `ExpressPackage.hasTrace` | ExpressPackage → LogisticsTrace（实时） |
| `Order.hasRefund` | Order → Refund |
| `Order.promotedBy` | Order → Promotion（多多进宝归因） |

### 4.3 Funnel（订单 · 拼多多特有状态）

```text
待成团 (grouping) → 已成团 (paid) → 待发货 → 已发货 → 已收货 → 已完成
  ↘ 拼团失败 → 已关闭            ↘ 退款中 → 退款完成/关闭
```

> **关键差异：** 拼多多有「拼团」状态机——待成团 vs 已成团，而淘宝/微商城无此状态。  
> Funnel 需增加 `grouping` 和 `group_failed` 两个节点。

---

## 5. 数据接入策略

### 5.1 总原则

| 路径 | 用途 | 拼多多用法 |
|------|------|-----------|
| **A. REST API 主路径** | 运行态孪生 | OAuth 2.0 → access_token → HTTP POST `open-api.pinduoduo.com` |
| **B. 增量轮询** | 订单/售后增量同步 | `pdd.order.number.list.increment.get`（15min/30min 粒度推荐） |
| **C. 全量兜底** | 首次同步/对账 | `pdd.order.list.get`（90 天内）+ `pdd.goods.list.get` |
| **D. 文件导出** | 离线孪生包 | 商家后台 Excel 导出 → file-local → Dataset |

### 5.2 认证与签名流程

```text
1. 商家在拼多多后台授权应用 → 获取 authorization_code
2. 后端用 code 换取 access_token（有效期 ~24h）
3. 每次 API 调用：
   a. 参数按 key 首字母升序排列
   b. 拼接所有 keyvalue（不含 sign）+ 前后追加 client_secret
   c. MD5 → 大写 32 位 = sign
   d. POST {type, client_id, timestamp, data_type, sign, access_token, ...业务JSON参数}
```

### 5.3 AOS 平台缺口（接入前提）

| 编号 | 缺口 | 影响 | 优先级 |
|------|------|------|--------|
| **G-REST-01** | REST API Connector 类型 | 拼多多无法直连 | 🔴 阻塞 |
| **G-OAUTH-01** | OAuth 2.0 Token Manager（含轮换） | 所有国内电商（淘宝/拼多多/抖音）共用 | 🔴 阻塞 |
| **G-SIGN-01** | MD5 签名插件（非 HMAC-SHA256） | 拼多多签名算法特殊 | 🟡 拼多多专属 |
| **G-INCR-01** | 增量轮询调度策略 | 淘宝/拼多多均有增量接口 | 🟡 通用增强 |

> **淘宝+拼多多 共用**：REST Connector + OAuth Manager 一经验收，两平台同时解锁。

---

## 6. 从物理到孪生的主链路

```text
拼多多商家（线上店铺）
      │ OAuth 2.0 授权
      ▼
  REST API Connector（通用平台能力 · 待建）
      │ HTTP POST → pdd.* 接口
      │ MD5 签名 + access_token
      ▼
  Source → Sync（增量轮询 + 全量兜底）
      │
      ▼
  Pipeline/Build → Dataset（按域）
      │
      ▼
  OKF 映射 → Funnel 水合 → Object / Link
      ▼
  ┌─────────┬──────────┬────────────┬───────────┐
  ▼         ▼          ▼            ▼
 COP态势   Inbox运营  Graph/Buddy  Analytics
```

---

## 7. 实施波次

| 波次 | 内容 | 依赖 | 状态 |
|------|------|------|------|
| **P0** | 本方案通过（本文） | — | ✅ v1.0 |
| **P1** | 注册开发者 + 创建自用型应用 + 沙箱 Test | 企业营业执照 | ⬜ 待执行 |
| **P1** | API 接口明细清单（筛选 ~30 个核心接口） | PDD 开放平台文档 | ⬜ 待执行 |
| **P2** | REST API Connector（平台通用） | 220plan W2+ 基础设施 | 🔴 阻塞 |
| **P2** | OAuth 2.0 Token Manager（平台通用） | 同上 | 🔴 阻塞 |
| **P2** | MD5 签名插件 | Connector 可插拔架构 | 🟡 阻塞 |
| **W1** | 沙箱数据接入验证（商品 + 订单） | P2 全部完成 | ⬜ 待执行 |
| **W2** | 全 8 域接入 + 态势上线 | W1 通过 | ⬜ 待执行 |

---

## 8. 与其他电商平台对比总览

| 维度 | 微商城 | 淘宝/天猫 | **拼多多** | Shopify | Amazon |
|------|--------|----------|-----------|---------|--------|
| API 协议 | JDBC MySQL | REST（HMAC-SHA256） | REST（**MD5**） | GraphQL（OAuth 2.0） | REST（LWAAuth） |
| 签名 | — | HMAC-SHA256 | **MD5（大写 32 位）** | Access Token Header | STS Token |
| Token | 数据库密码 | OAuth 2.0 | OAuth 2.0（~24h） | OAuth 2.0（permanent） | OAuth 2.0（1h rotate） |
| 增量 | SQL 增量 | 无原生增量 | **有增量接口** | Webhook 推送 | Notifications |
| 商品体系 | 自建类目 | 统一类目树 | 标准类目 | 自建 Collection | ASIN（全球目录） |
| 订单状态 | 5 状态 | 多子状态 | **含拼团状态** | 含多币种 | 含 FBA/MFN |
| 物流 | 自维护 | 菜鸟编码 | 快递公司注册 | 第三方 Carrier API | FBA + MFN 双轨 |

---

## 9. 下一步行动

| 优先级 | 行动 | 阻塞条件 |
|-------|------|---------|
| **P0 ✅** | 本方案完成 | — |
| **P1** | API 接口明细清单（~30 个核心 pdd.* 接口） | 需开发者账号查看全部文档 |
| **P1** | 注册拼多多开放平台开发者账号 | 企业营业执照 |
| **P2** | REST API Connector + OAuth Manager（平台通用） | 220plan W2+ 基础设施 |

> **版本**：v1.0 · 2026-07-22 · 总体分析计划  
> **变更日志**：  
> | 版本 | 日期 | 说明 |  
> | --- | --- | --- |  
> | v1.0 | 2026-07-22 | 初版 · 基于拼多多开放平台（pdd.* API）调研 · 9 域数据模型 · 拼团状态机 · MD5 签名差异 · 平台缺口 4 项 |
