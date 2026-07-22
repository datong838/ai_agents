# 跨境 Shopify · AOS 对接方案（补充）

| 字段 | 内容 |
|------|------|
| 状态 | **参考文档 · 主方案在 Shopify 方案中** · 2026-07-22 |
| 版本 | **v1.0** · 补充方案 |
| 目录 | `docs/palantier/20_tech/跨境shopify接入方案/` |
| 主方案 | [00-Shopify-AOS对接方案.md](../Shopify电商接入方案/00-Shopify-AOS对接方案.md) |
| 关联 | [Amazon 方案](../Amazon电商接入方案/00-Amazon-AOS对接方案.md) |

---

## 使用说明

跨境 Shopify 的 AOS 对接**已完整记录在 Shopify 主方案中**。

### 为什么没有独立出跨境方案？

| 维度 | 标准 Shopify | 跨境场景 | 结论 |
|------|-------------|---------|------|
| API 协议 | GraphQL Admin API + REST Admin API | 完全相同 | ✅ 统一接入 |
| OAuth 认证 | OAuth 2.0 Access Token | 完全相同 | ✅ 统一认证 |
| 核心数据模型 | Products/Orders/Customers/Inventory | 完全相同 | ✅ 统一 OT |
| 多币种 | 支持（presentmentPrices） | 跨境核心需求 | ✅ 主方案 §3.4 已覆盖 |
| 多语言 | 支持（Shopify Markets 自动翻译） | 跨境核心需求 | ✅ 主方案 §3.1 已覆盖 |
| 多 Location 库存 | 支持（Location Object Type） | 跨境核心需求 | ✅ 主方案 §3.2 已覆盖 |

### 跨境特有的补充内容

主方案尚未详细覆盖的跨境独有差异：

| 差异点 | 说明 | 影响 |
|--------|------|------|
| **Shopify Markets** | 2022 年推出的跨境一站式方案（货币/语言/税费/域名） | OT 中新增 Market 维度 |
| **Duties & Import Taxes** | 关税/进口税预估（结账时展示） | 订单 OT 新增关税 Prop |
| **Harmonized System (HS) Codes** | 跨境商品需填写 HS 编码 | Product OT 新增 hs_code Prop |
| **Country of Origin** | 商品原产地 | Product OT 新增 origin_country Prop |
| **Google & Meta Channel** | 跨境广告投放渠道（Google Shopping / Facebook Shop） | 后置（Phase 4） |
| **Shopify Fulfillment Network** | Shopify 官方仓储物流（美/加/欧） | 物流 OT 扩展 |
| **Global-e** | Shopify 收购的跨境物流方案（端到端跨境履约） | 后置（Phase 4） |

### 何时升级为独立方案？

当以下任一条件成立时，将跨境 Shopify 升级为独立方案：
- 跨境业务涉及 **多个 Shopify 实例**（多地区独立店铺）
- 需要与 **Amazon 全球开店** 做跨平台跨境对比分析
- 关税/合规/数据驻留（GDPR）成为核心关注点
- 上述 7 项跨境特有内容中有 3 项以上需要深入建模

**当前阶段：直接使用 Shopify 主方案，跨境差异作为补充字段在主方案对应域内追加。**

> **版本**：v1.0 · 2026-07-22 · 跨境 Shopify 接入方案指向文档
