# frozen/03 — OpenAPI 写契约（D0 只校验不执行）

> 上位方案：[228-微商城专项](../228-微商城专项实施准备与FDE全链路规格.md) 第 8 节 D0。
> 重要边界：**D0 只校验请求体 schema，不发任何写请求**（POST/PUT/PATCH/DELETE）到 yanpanji.com 或微商城后台。
> 落点说明：本文件是规格文档，**非 niushop bundle 资产**（边界门禁 [test_m5_ecommerce_boundaries.py](../../../../../aos-platform/services/aos-api/tests/asset_registry/test_m5_ecommerce_boundaries.py) 禁止 niushop bundle 携带网络端点）。

---

## 1. D0 范围内行为

D0 **不发送任何写请求**。本文件只冻结"未来可能用到的写接口请求体 schema"，作为 D1.5+ 草稿生成（Draft-only）的契约依据。

写接口的真实调用最早发生在 **D4 生产 Action**，且必须满足前置：
- C0.2 全部完成（Action adapter / 审批 / 幂等 / 审计 / 补偿 / 回滚）
- 仅低风险可逆动作首批
- 支付/退款/库存扣减需专项安全评审

---

## 2. 微商城后台写接口契约（冻结请求体，不执行）

> 来源：[niushop 代码](file:///Users/ddt/work/projects/ai_agent/niushop) app/controller/shop + CDP 后台观察（待 D1.5 补全）。
> 标注 `[TBC]` 的项表示待 CDP 实际抓包确认，当前不编造。

### 2.1 商品上下架（D4 低风险候选）

| 项 | 值 |
|---|---|
| 端点 | `POST /shop/goods/setGoodsStatus` `[TBC: 待 CDP 抓包]` |
| 请求体 | `{"goods_id": int, "state": 0\|1}` |
| 幂等键 | `niushop:goods_status:{goods_id}:{state}:{day}` |
| 风险等级 | 低（可逆） |
| D0 行为 | **不调用**，只冻结 schema |

### 2.2 库存调整（D4 需专项评审）

| 项 | 值 |
|---|---|
| 端点 | `POST /shop/goods/editStock` `[TBC]` |
| 请求体 | `{"sku_id": int, "stock_num": int}` |
| 幂等键 | `niushop:stock:{sku_id}:{stock_num}:{nonce}` |
| 风险等级 | **中高**（影响可售性） |
| D0 行为 | **不调用**，D4 需专项安全评审 |

### 2.3 订单发货（D4 需专项评审）

| 项 | 值 |
|---|---|
| 端点 | `POST /shop/order/delivery` `[TBC]` |
| 请求体 | `{"order_id": int, "express_company_id": int, "delivery_no": string}` |
| 幂等键 | `niushop:delivery:{order_id}:{delivery_no}` |
| 风险等级 | **高**（触发物流） |
| D0 行为 | **不调用** |

---

## 3. D0 校验规则（只读，不发请求）

D0 脚本对上述契约只做静态校验：
- 请求体 schema 字段类型完整性（不发送）
- 幂等键命名空间与 P01~P07 一致（`niushop:` 前缀）
- 风险等级标注齐全
- `[TBC]` 项登记为 D1.5 待补全项，不编造端点

---

## 4. 禁止行为（硬约束）

- ❌ D0 发送任何 POST/PUT/PATCH/DELETE 到 yanpanji.com
- ❌ D0 调用微商城后台任何写接口
- ❌ D0 把 OpenAPI spec 塞进 niushop bundle（边界门禁禁止）
- ❌ D0 读取/导出真实凭据到报告
- ❌ 把 `[TBC]` 项编造成已确认端点

---

## 5. 与平台-电商域-微商城三层自洽性

| 层 | 契约来源 | 本规格对齐点 |
|---|---|---|
| 平台（AOS 通用） | 边界门禁禁止 bundle 携带网络端点 | 写契约落规格文档，不入 bundle |
| 电商域 | [228-AIP 生产写回 C0 安全方案](../../228-AIP生产写回C0租户与审批安全闭环方案.md) | Draft-only / 幂等键 / 审批 / 可逆 |
| 微商城 | [228-微商城专项](../228-微商城专项实施准备与FDE全链路规格.md) 第 3 节"生产写回 C0.2 未完成" | 全部 Draft-only，D4 才考虑真实调用 |
