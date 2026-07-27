# 02 · 京东 POP 与自营（VC）双模式差异分析

> **版本**：v1.0 · 2026-07-23
> **状态**：P1 分析完成
> **关联**：[00-总体分析计划](./00-京东AOS对接方案.md) · [01-京东API接口清单](./01-京东API接口清单.md)

---

## 1. 为什么京东有双模式

京东是唯一同时运营 **第三方商家平台（POP）** 和 **自营采购体系（VC/Vendor Center）** 的国内电商。两种模式的业务逻辑完全不同：

```text
POP 模式（第三方商家）
├── 商家自主上架、定价、发货
├── 京东仅提供平台（类似淘宝天猫）
├── API：jingdong.pop.* / jingdong.ware.*
└── 商家是交易主体，京东抽佣

自营模式（VC / Vendor Center）
├── 京东向供应商采购，入京东仓
├── 京东统一定价、发货、售后
├── API：jingdong.vc.* / jingdong.b2b.*
└── 京东是交易主体，供应商是上游
```

> **AOS 策略：** OT 层统一（一个 Product OT 覆盖两种模式），Connector 层分派（POP Source vs VC Source），OKF 映射层消解差异。

---

## 2. 全域字段级对照

### 2.1 商品域

| 维度 | POP（`jingdong.ware.*`） | 自营（`jingdong.vc.item.*`） | AOS 处理 |
|------|--------------------------|-------------------------------|---------|
| 标识 | `wareId` + `skuId` | `wareId` + `skuId`（共用 ID 体系） | OT 统一 string |
| 定价权 | 商家自主 `shopPrice` | 京东定价 `jdPrice` + 采购价 `purchasePrice` | OT 新增 `priceSource` Prop |
| 库存 | 商家自管 `stockNum` | 京东仓内库存（API 不直接暴露） | POP 有库存，自营查采购单 |
| 上下架 | `jingdong.ware.write.upOrDown` | **无此概念**（京东控制） | POP 映射 Event，自营无操作 |
| 商品发布 | `jingdong.ware.write.*` | `jingdong.vc.item.create`（提交给京东审核） | 两种 Source |
| 类目映射 | POP 类目 `cid` | 自营类目 `cid`（同一棵树，但权限不同） | 共用 Category OT |
| 品牌 | `jingdong.getBrandByIds` | 同上（共用品牌库） | Brand OT 共用 |
| 图片规格 | 最多 7 张主图 | 同上 | 共用 |
| 详情 | `bookBigField`（富文本） | 同上 | 共用 |

### 2.2 订单域

| 维度 | POP（`jingdong.pop.order.*`） | 自营（无独立 API，共用订单查询） | AOS 处理 |
|------|-------------------------------|-------------------------------|---------|
| 订单来源 | C 端下单 → POP 商家 | C 端下单 → 京东仓 | `orderSource` Prop 标记 |
| 履约模式 | SOP / SOPL / LBP / FBP | **全部 FBP**（京东仓发） | `fulfillmentType` Prop |
| 发货动作 | 商家调 `shipment.update` | **无发货动作**（京东自动配送） | POP 有 Action，自营无 |
| 拆单 | 一单可拆多子订单 | 更频繁拆单（多仓） | Order→OrderLine Link |
| 结算 | C 端付款 → 京东 → **账期结算给商家** | C 端付款 → 京东（供应商与京东另算采购结算） | `settlementType` Prop |
| 退款 | 走 POP 售后 API | 走京东售后（供应商不介入退款） | 售后 OT 区分来源 |

### 2.3 库存/采购域

| 维度 | POP | 自营 | AOS 处理 |
|------|-----|------|---------|
| 库存管理 | 商家自管 | 京东仓管理，供应商只看采购单 | 自营建 PurchaseOrder OT |
| 补货 | 商家自主补 | 京东下采购单（`jingdong.vc.po.*`） | 自营有 PurchaseOrder OT |
| 入库 | 商家自行入库 | 京东入库确认（`jingdong.b2b.inboundOrder`） | 自营有 InboundShipment OT |
| 安全库存 | 商家设定 | 京东根据销量算法设定 | 后置 |

### 2.4 售后域

| 维度 | POP（`jingdong.asc.*`） | 自营 | AOS 处理 |
|------|--------------------------|------|---------|
| 售后入口 | 商家处理 `jingdong.asc.audit` | **京东客服全权处理** | POP 有 Action，自营仅读取 |
| 退款流程 | 商家审核 → 退款 | 京东自动退款，后向供应商扣款 | 自营 `refundSource = jd` |
| 售后类型 | 退款/退货/换货/维修/赔付/价保 | 同上但由京东操作 | OT 枚举共用 |
| 平台仲裁 | `jingdong.asc.process.state` | 不存在（京东自营无仲裁概念） | 仅 POP 场景 |

### 2.5 营销/定价域

| 维度 | POP | 自营 | AOS 处理 |
|------|-----|------|---------|
| 促销活动 | 商家自主 `jingdong.seller.promotion.*` | 京东统一策划 | 后置 |
| 优惠券 | 京券/东券 | 京东统一 | 后置 |
| 价格变动 | 商家 `jingdong.sku.price.update` | 京东统一定价 | 自营无操作 |
| 广告 | 京准通（商家自助投放） | 京东运营投放 | 暂不接入 |

---

## 3. Ontology 统一模型

### 3.1 Product OT（统一覆盖 POP + 自营）

```yaml
Object Type: Product
  primaryKey: wareId (string)
  props:
    title: string
    cid: string              # 类目ID（共用类目树）
    brandId: string          # 品牌ID
    saleAttr: json           # 销售属性
    imgs: string[]           # 图片组（最多7张）
    descHtml: text           # 详情富文本
    # ─── POP 专属 ───
    shopPrice: decimal       # 商家售价（POP 有，自营无）
    stockNum: int            # 商家库存（POP 有，自营从采购单推算）
    status: enum             # 上下架（POP 有，自营恒为上架）
    # ─── 自营专属 ───
    purchasePrice: decimal   # 采购价（自营有，POP 无）
    jdPrice: decimal         # 京东零售价（自营有）
    # ─── 统一字段 ───
    sourceMode: enum         # pop / vc  ← 关键区分字段
```

### 3.2 Order OT（统一覆盖 POP + 自营）

```yaml
Object Type: Order
  primaryKey: orderId (string)
  props:
    orderStatus: enum        # 状态枚举
    buyerPin: string         # 买家PIN（脱敏）
    payType: enum            # 支付方式
    payTime: timestamp
    invoiceInfo: json        # 发票信息
    receiverInfo: json       # 收货信息
    # ─── 履约模式 ───
    fulfillmentType: enum    # SOP / SOPL / LBP / FBP
    fulfillChannel: enum     # pop_self / jd_fulfill
    # ─── 来源标记 ───
    sourceMode: enum         # pop / vc  ← 关键区分字段
    orderSource: string      # 订单来源（APP/PC/M站）
```

### 3.3 自营专属 OT

| OT | 主键 | 来源 API | 说明 |
|----|------|---------|------|
| **PurchaseOrder** | purchaseId | `jingdong.vc.po.*` | 京东向供应商下的采购单 |
| **InboundShipment** | inboundId | `jingdong.b2b.inboundOrder` | 京东入库确认单 |

> POP 模式无这两个 OT。

---

## 4. Connector 层分派架构

```text
京东电商（一个 Workspace）
      │
      ├── POP Connector Source
      │     ├── OAuth: POP 商家授权 access_token
      │     ├── 签名: HMAC-SHA256 (POP app_key)
      │     ├── API: jingdong.pop.* / jingdong.ware.*
      │     └── Sync: 全量(ware.list) + 增量(order.en.search)
      │
      └── VC Connector Source
            ├── OAuth: Vendor Center 专属授权
            ├── 签名: HMAC-SHA256 (VC app_key)
            ├── API: jingdong.vc.* / jingdong.b2b.*
            └── Sync: 全量(vc.item.list) + 采购单(po.list)

      │
      ▼
  OKF 映射层
      ├── POP Dataset → Product OT (sourceMode=pop)
      ├── VC Dataset  → Product OT (sourceMode=vc)
      ├── POP Dataset → Order OT (sourceMode=pop, fulfillmentType=SOP...)
      ├── VC Dataset  → Order OT (sourceMode=vc, fulfillmentType=FBP)
      ├── VC Dataset  → PurchaseOrder OT (自营专属)
      └── VC Dataset  → InboundShipment OT (自营专属)
```

---

## 5. 实施优先级

| 阶段 | 内容 | 理由 |
|------|------|------|
| **Phase 1** | POP 全域接入（商品/订单/物流/售后） | POP API 更成熟、文档更全、第三方商家是主要客户 |
| **Phase 2** | 自营 VC 商品+订单接入 | VC API 相对简单（无发货动作），但需 Vendor Center 权限 |
| **Phase 3** | 自营采购单 + 入库管理 | 供应链场景，需与仓库系统联动 |
| **Phase 4** | 营销/评价/PLUS 会员 | 非核心链路，增值权限 |

---

## 6. 数据隔离策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| **统一 Workspace** | POP + 自营在同一 AOS Workspace，用 `sourceMode` Prop 区分 | 需要全店视角分析 |
| **分 Workspace** | POP 和自营各开一个 Workspace | 需要严格权限隔离 |
| **推荐** | **统一 Workspace + sourceMode Prop** | 默认推荐，减少重复建模 |

---

## 7. 风险与注意

| # | 风险 | 说明 | 缓解 |
|----|------|------|------|
| R1 | 双 app_key 认证 | POP 和 VC 用不同的 app_key + access_token | Connector 配置两套认证参数 |
| R2 | 价格双轨 | POP 商家自主定价 vs 自营京东定价，同一 wareId 可能价格不同 | OT 存储时按 sourceMode 分别记录 |
| R3 | 库存模型不一致 | POP 有库存字段，自营无直接库存 API（需从采购单/入库推算） | 自营库存作为后置功能 |
| R4 | 售后流程不对称 | POP 商家需操作售后 API，自营售后完全由京东处理 | Action 仅对 POP 生效 |
| R5 | 类目权限差异 | 同一类目在 POP 和 VC 中可能权限不同 | Connector 配置中分别校验 |

---

> **版本**：v1.0 · 2026-07-23 · 京东 POP/自营双模式差异分析
>
> **变更日志**：
>
> | 版本 | 日期 | 说明 |
> | --- | --- | --- |
> | v1.0 | 2026-07-23 | 初版 · 5 域字段级对照 · 统一 OT 模型 · Connector 分派架构 · 数据隔离策略 |
