---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/sap/extract-long-text/",
  "title": "从SAP提取长文本",
  "page_id": "extract-long-text",
  "category_id": "data-integration",
  "section_id": "sap",
  "previous": "/zh/foundry/sap/sap-dynamic-filters/",
  "next": "/zh/foundry/sap/configure-custom-authorizations/",
  "scraped_at": "2026-07-13T05:38:56.604762+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从SAP提取长文本

## 概述

长文本（也称为SAPscript文本或文本对象）是附加到SAP ERP对象上的容器，用于在SAP系统中容纳长文本。用户可以添加自由文本，甚至可以在不受常见数据库或应用程序限制的情况下应用格式化。用户可以将长文本添加到常见的SAP对象，如销售订单、材料或通知。

长文本以压缩格式存储在`STXL`表中。该表保存所有SAP对象的长文本。需要解压缩才能在Foundry中可读。

## 先决条件

* [Palantir Foundry Connector 2.0 以SAP应用程序](/zh/foundry/sap/overview/) SP16或以上版本

## 提取长文本

Foundry SAP Connector具有在将`STXL`表发送到Foundry之前解压缩长文本的功能。需要在配置表中添加一条新记录以激活此功能。要添加新记录：

1. 运行事务`/n/PALANTIR/DECOMPRESS`

2. 在配置表中，填写以下Connector参数：
   1. `OBJECT TYPE`：`SLT`，`TABLE`或`REMOTETABLE`（取决于您的设置）
   2. `OBJECT`：`STXL`
   3. `FIELD`：`CLUSTD`
   4. `ITEM NO`：`1`
   5. `INTERFACE COMPONENT`：`DECOMPRESSION_LRAW`

3. 创建一个新的同步并导入长文本表。由于`STXL`表通常非常大，最好按对象名称筛选表。

   同步配置的格式如下：

   ```yaml
   type: magritte-sap-source-adapter
   sapType: <slt>/<table>/<remotetable>
   obj: STXL
   context: <SLT_Context>/<Remote_Agent_Context>
   filter: <筛选>
   ```

   示例同步：

   ```yaml
   type: magritte-sap-source-adapter
   sapType: table
   obj: STXL
   filter: TDOBJECT=QMEL
   ```

   您可以通过对象名称和文本ID筛选`STXL`表。例如：

   * 通知对象：`TDOBJECT=QMEL`
   * 通知对象头长文本：`TDOBJECT=QMEL;TDID=LTXT`
   * 采购订单头文本：`TDOBJECT=EKKO`
   * 采购订单项目文本：`TDOBJECT=EKPO`
