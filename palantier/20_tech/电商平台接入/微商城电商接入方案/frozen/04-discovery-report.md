# frozen/04 — D0 发现差异报告

> 上位方案：[228-微商城专项](../228-微商城专项实施准备与FDE全链路规格.md) 第 5 节。
> 对照基准：frozen/01 真实 schema fingerprint。
> 闭环要求：每条差异都有 disposition，无空值。

---

## 差异清单

| ID | 差异 | 上位方案描述 | 真实情况 | 处置（disposition） | 影响波次 |
|---|---|---|---|---|---|
| **D-001** | 订单状态字段名不符 | P05 关键映射写"`shipping_status`"（状态四元组含 shipping_status） | `ns_order.shipping_status` **字段不存在**；真实履约状态字段是 `ns_order.delivery_status` + `ns_order_goods.delivery_status` | **spec-fix**：[frozen/02 P05](./02-pipeline-manifest.yaml) 已修正为 `delivery_status` | D1 实施时按修正后规格 |
| **D-002** | OrderLine 增量游标不可用 | P06 增量游标 `(create_time, order_goods_id)` | `ns_order_goods.create_time` 227 行**全为 0**（100% 空），无法做增量游标 | **spec-fix**：[frozen/02 P06](./02-pipeline-manifest.yaml) 改用每日快照 + order_id 关联重扫；`refund_action_time` 作为退款状态变更辅游标 | D1 实施时按修正后规格 |
| **D-003** | 软删除行未在过滤条件显式登记 | P02/P05 源过滤写 `is_delete=0`（正确） | 实际存在大量软删行：`ns_goods` 8/65、`ns_order` 60/177 | **risk-logged**：软删行比例较高（order 34%），D1 需确认是否进 DLQ 计数还是完全跳过；当前规格按"进 DLQ 计数"处置 | D1 实施时确认 DLQ 策略 |
| **D-004** | goods modify_time 部分空 | P02 增量游标 `(modify_time, goods_id)`，`modify_time=0` 回退 `create_time` | `ns_goods.modify_time` 23/65 行为 0（35%），回退逻辑会频繁触发；`ns_goods_sku.modify_time` 26/73 为 0（36%） | **risk-logged**：回退 `create_time` 可行（全非空），但增量频率会受影响；D1 需做范围重扫补仅状态变化行 | D1 增量策略调优 |
| **D-005** | pay_time 大量空 | P05 隐含 pay_time 可用于支付完成时间 | `ns_order.pay_time` 75/177 为 0（42%，未支付订单） | **risk-logged**：未支付订单无 pay_time 是正常业务语义，非数据问题；D1 映射 `0→null` 即可 | D1 已覆盖 |
| **D-006** | Pipeline 无法落 bundle 资产 | 上位方案第 4 节 FDE 结构写 `platform.ecommerce.niushop` 含 "P01~P07 Pipeline 模板" | `BundleExports` 是 StrictContract，**不支持 pipeline 字段**；边界门禁禁止 niushop bundle 携带可执行资产 | **spec-fix**：P01~P07 落到 [frozen/02](./02-pipeline-manifest.yaml) 规格文档，D1 通过 `/v1/pipelines` 运行时创建 | D1 运行时创建 |

---

## 闭环状态

- 差异总数：**6**
- spec-fix（已修正规格）：**3**（D-001 / D-002 / D-006）
- risk-logged（登记为风险，D1 处理）：**3**（D-003 / D-004 / D-005）
- d1-defer（延后 D1）：**0**
- 空处置：**0**
- **闭环结论：全部差异已处置，无孤儿项。**

---

## D0 范围内 PII 风险评估

| 项 | 结论 |
|---|---|
| 7 表内 PII_DIRECT 字段 | **0**（姓名/手机/地址/OpenID/支付号均不在 7 表） |
| 7 表内 PII_QUASI 字段 | **0**（email/nickname/avatar 均不在 7 表） |
| PII 集中位置 | `ns_member`/`ns_member_address`/`ns_member_bank_account`/`ns_user`/`ns_pay`，延后 D1.5/D2 |
| D0 PII 泄漏风险 | **可控**（7 表无 PII_DIRECT，且脚本强制只聚合不取值） |

---

## 上位方案一致性核对

| 上位方案要求 | D0 落实 | 一致 |
|---|---|---|
| 专用只读账号 + 负向测试 | recommend_ro（7/7 表 + SHOW VIEW + 写权限被拒） | ✅ |
| 冻结 schema/索引/状态字典/PII 分类 | frozen/01 | ✅ |
| 冻结 7 Pipeline manifest | frozen/02（落规格文档而非 bundle，D-006 已登记） | ✅ |
| 校验 OpenAPI 请求体 | frozen/03 | ✅ |
| 不发写请求 | 全程零写 | ✅ |
| 零明细泄漏 / 零生产写入 | PII 扫描零命中 + 只读事务 | ✅ |
| 差异清单闭环 | 本报告 6 条全处置 | ✅ |

**D0 退出门核验：8/8 通过。** 待专项测试 + 全量回归后判 GREEN。
