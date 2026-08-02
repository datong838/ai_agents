# Niushop 案例 · 数字孪生数据文件（Excel / Word / PDF）

> **2026-08-02 安全校准：** 本文旧版“默认真实值、全列全行导出”不得执行。实施前所有导出必须默认脱敏、最小字段、显式行数上限，并经数据负责人批准；真实全量明细不能进入 Git、测试夹具或普通实施报告。当前脚本已隔离，详见 [228-微商城专项实施准备与FDE全链路规格](228-微商城专项实施准备与FDE全链路规格.md)。

| 字段 | 内容 |
|------|------|
| 状态 | **数字孪生数据源**（线上真实数据 · 全字段）· 非测试抽样 |
| 版本 | **v1.3** · 2026-07-19（表头中文名 + `_字段词典`；重导全字段） |
| 目录 | `docs/palantier/20_tech/niushop电商案例/` |
| 关联 | [00 整体孪生主方案 v2.0](00-Niushop微商城AOS对接方案.md) · [01 JOIN与路径](01-Pipeline多表JOIN能力核查与接入路径调整.md) |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 | 全文 |
| **孪生真实性** | 订单/商品等走线上库 **全列全行**；禁止「为测 parsers 只导 10 列」当交付 |
| PII | **默认脱敏且最小化**；只有经专项审批的受控环境才能处理真实值，且不得进入 Git/普通报告 |
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

## 2. Excel · 订单孪生（全字段 · 中文表头）

| Sheet | 表 | 列数（实导） | 行数（实导） |
|-------|-----|--------------|--------------|
| `订单` | `ns_order` | **130** | **167** |
| `订单行` | `ns_order_goods` | **71** | **216** |
| `_字段词典` | — | 英文字段↔中文名 | 供 Ontology 中文显示 |

文件：`fixtures/excel/mall-order.xlsx`

### 2.1 表头约定（数字孪生）

每个数据 Sheet：

| 行 | 内容 | 用途 |
|----|------|------|
| **第 1 行** | **中文名**（取自 MySQL `COLUMN COMMENT`；无 COMMENT 则用英文字段名） | 孪生属性中文显示名 |
| **第 2 行** | 英文字段名（`order_id` 等） | 稳定技术键 / OKF 映射 |
| **第 3 行起** | 真实数据 | 全量行、全量列 |

另有 `_字段词典`（工作簿首页）：`物理表 · Sheet · 英文字段 · 中文名 · 类型 · COMMENT原文 · 无中文COMMENT`。

> Excel 单格约 32KB 上限：超长会截断并写 `twin-excel-truncations.txt`。  
> 少数列库内无 COMMENT（如部分主键）→ 中文名暂等于英文字段，可在词典中人工补中文后再进 Ontology。

---

## 3. Excel · 商品孪生（全字段 · 可与 JDBC 对照）

| Sheet | 表 | 列数 | 行数 |
|-------|-----|------|------|
| `商品` | `ns_goods` | 90 | 65 |
| `商品SKU` | `ns_goods_sku` | 87 | 73 |
| `商品端可见` | `ns_goods_weapp` | 7 | 93 |
| `商品分类` | `ns_goods_category` | 22 | 11 |
| `_字段词典` | — | 同上 | |

文件：`fixtures/excel/mall-goods.xlsx`  
运行态孪生主路径仍建议 **JDBC**（见 01）；本文件用于离线包与对照。

---

## 4. Excel · 内容/门店孪生

| Sheet | 表 |
|-------|-----|
| `文章` / `帮助` / `协议文档` / `门店` / `公告` | 对应 `ns_*` 全列 + `_字段词典` |

文件：`fixtures/excel/mall-catalog.xlsx`

---

## 5. Word / PPT / PDF

由你放入 `fixtures/word` · `ppt` · `pdf/...`，进 AOS MediaSet 做文档孪生；协议/文章亦可从 `ns_document` / `ns_article` 另存。

---

## 6. 安全

- `.env`、xlsx **gitignore**，勿提交远端。  
- 安全目标是默认 `NIUSHOP_EXCEL_MASK_PII=1` 且显式限量；当前脚本默认值仍为 `0`，因此在修复并通过审计前禁止运行。任何外传、共享或入库前都必须复核脱敏结果。

---

## 7. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-19 | 初版抽样列 SQL |
| v1.1 | 2026-07-19 | 隧道导出（抽样列） |
| v1.2 | 2026-07-19 | **纠正口径**：数字孪生全字段；订单 130+71 列实导 |
| v1.3 | 2026-07-19 | 表头中文名（COMMENT）+ 第2行英文字段 + `_字段词典`；Sheet 中文名 |

---

*v1.2 · 数字孪生数据文件说明*
