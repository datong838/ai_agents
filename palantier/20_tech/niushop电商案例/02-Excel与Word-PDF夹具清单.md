# Niushop 案例 · 数字孪生数据文件（Excel / Word / PDF）

| 字段 | 内容 |
|------|------|
| 状态 | **数字孪生数据源**（线上真实数据 · 全字段）· 非测试抽样 |
| 版本 | **v1.2** · 2026-07-19 |
| 目录 | `docs/palantier/20_tech/niushop电商案例/` |
| 关联 | [00 整体孪生主方案 v2.0](00-Niushop微商城AOS对接方案.md) · [01 JOIN与路径](01-Pipeline多表JOIN能力核查与接入路径调整.md) |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 | 全文 |
| **孪生真实性** | 订单/商品等走线上库 **全列全行**；禁止「为测 parsers 只导 10 列」当交付 |
| PII | 默认导出真实值（本机私有、gitignore）；需要时 `.env` 设 `NIUSHOP_EXCEL_MASK_PII=1` |
| 零定制码 | 导出脚本只做通用 SELECT * + 写 xlsx；不改商城 |

---

## 0. 口径（必读）

本案例用线上微商城做 **AOS 数字孪生**，不是造测试夹具：

| 对 | 错 |
|----|-----|
| Excel = 订单孪生的一种接入载体（全字段真实行） | Excel = 随便抽样几列验一下解析插件 |
| 字段与 `ns_order` / `ns_order_goods` **列对齐** | 只保留 order_id/状态等「演示列」 |
| 商品主数据优先 JDBC；Excel 可作全量对照/离线孪生包 | 商品也缩成 6 列「样例」 |

Word / PDF / PPT：同样是真实业务文档进 MediaSet，不是假数据。

---

## 1. 目录结构

```text
niushop电商案例/
  .env
  export_fixtures_excel.py     ← 全字段孪生导出
  fixtures/
    excel/
      mall-order.xlsx          ← ns_order 全列 + ns_order_goods 全列（主文件）
      mall-goods.xlsx          ← goods / sku / weapp / category 全列
      mall-catalog.xlsx        ← article / help / document / store / notice 全列
      mall-order-sample.xlsx   ← 与 mall-order 同内容（兼容旧名）
      mall-sku-master.xlsx     ← 与 mall-goods 同内容（兼容旧名）
      mall-catalog-index.xlsx  ← 与 mall-catalog 同内容（兼容旧名）
    word/   ppt/   pdf/...
```

**连接：** `127.0.0.1:13306`（SSH 隧道）→ 库 `niushop_b2c_v5`，凭据见 `.env`。

**重导：**

```powershell
python docs/palantier/20_tech/niushop电商案例/export_fixtures_excel.py
```

---

## 2. Excel · 订单孪生（全字段）

| Sheet | 表 | 列数（实导） | 行数（实导） |
|-------|-----|--------------|--------------|
| `orders` | `ns_order` | **130** | **167** |
| `order_lines` | `ns_order_goods` | **71** | **216** |

文件：`fixtures/excel/mall-order.xlsx`

含支付、履约、分享/分润扩展、发票等全部业务列；与线上表结构一致。

> Excel 单格约 32KB 上限：若某 HTML 超长会截断并写 `twin-excel-truncations.txt`（本次全字段导出 **无截断**）。超长正文以 JDBC/Media 为准。

---

## 3. Excel · 商品孪生（全字段 · 可与 JDBC 对照）

| Sheet | 表 | 列数 | 行数 |
|-------|-----|------|------|
| `goods` | `ns_goods` | 90 | 65 |
| `goods_sku` | `ns_goods_sku` | 87 | 73 |
| `goods_weapp` | `ns_goods_weapp` | 7 | 93 |
| `goods_category` | `ns_goods_category` | 22 | 11 |

文件：`fixtures/excel/mall-goods.xlsx`  
运行态孪生主路径仍建议 **JDBC**（见 01）；本文件用于离线包与对照。

---

## 4. Excel · 内容/门店孪生

| Sheet | 表 |
|-------|-----|
| `articles` / `help` / `documents` / `stores` / `notices` | 对应 `ns_*` 全列 |

文件：`fixtures/excel/mall-catalog.xlsx`

---

## 5. Word / PPT / PDF

由你放入 `fixtures/word` · `ppt` · `pdf/...`，进 AOS MediaSet 做文档孪生；协议/文章亦可从 `ns_document` / `ns_article` 另存。

---

## 6. 安全

- `.env`、xlsx **gitignore**，勿提交远端。  
- 默认 `NIUSHOP_EXCEL_MASK_PII=0`（真实孪生）。外传或共享前改为 `1` 再重导。

---

## 7. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-19 | 初版抽样列 SQL |
| v1.1 | 2026-07-19 | 隧道导出（抽样列） |
| v1.2 | 2026-07-19 | **纠正口径**：数字孪生全字段；订单 130+71 列实导 |

---

*v1.2 · 数字孪生数据文件说明*
