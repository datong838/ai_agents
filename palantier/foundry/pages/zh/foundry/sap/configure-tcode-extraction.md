---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/sap/configure-tcode-extraction/",
  "title": "事务代码和报告提取",
  "page_id": "configure-tcode-extraction",
  "category_id": "data-integration",
  "section_id": "sap",
  "previous": "/zh/foundry/sap/configure-functions/",
  "next": "/zh/foundry/sap/ingest-hana-views/",
  "scraped_at": "2026-07-13T05:39:10.919420+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 事务代码和报告提取

## 概述

Palantir Foundry Connector 2.0 以SAP应用程序 ("Connector") 提供了从SAP应用程序服务器中分配给ABAP报告的事务代码或ABAP报告中提取数据的方法。仅支持使用ABAP列表查看器的报告。

:::callout{theme="neutral"}
仅支持使用ABAP列表查看器（ALV）的报告。
:::

:::callout{theme="neutral"}
`tcode`同步只能从同步配置UI的高级选项卡创建。
:::

## 提取数据

使用`tcode`对象类型来提取由事务代码生成的数据。

如果您知道事务代码名称，请将其作为值提供给`obj`参数。
示例同步配置：
如果您只知道报告的程序名称，可以将程序名称作为`obj`参数提供，并将`programType`参数设置为`program`。
示例同步配置：

## 支持的参数

在配置事务代码提取时，支持附加参数：

* [筛选](#filter)
* [selectionVariant](#selectionVariant)
* [outputVariant](#outputVariant)
* [ingestionType](#ingestionType)

可以在同一个同步中定义多个参数。

### 筛选

`筛选`参数被用于在传递用户输入给选择屏幕变量。它不作用于报告的任何输出字段的任意筛选。

同步配置示例：

```yaml
type: magritte-sap-source-adapter
sapType: tcode  # SAP事务代码
obj: ZTEST_ALV  # 目标SAP对象
filter: p_spras=EN  # 过滤条件，语言参数设置为英文
```

### selectionVariant

`selectionVariant`参数被用于在程序中传递选择屏幕变体。选择屏幕变体是在程序的选择屏幕中创建的预定义筛选。

:::callout{theme="neutral"}
如果同时定义了`selectionVariant`和`筛选`参数，`筛选`将覆盖变体中选择屏幕参数的现有值。
:::

示例同步配置：

```yaml
type: magritte-sap-source-adapter
sapType: tcode  # SAP事务代码类型
obj: RSUSR200  # SAP对象名称，通常指代特定的程序或功能模块
programType: program  # 程序类型，表示该SAP对象是一个程序
selectionVariant: USER_DISKOVER  # 选择变体，用于指定程序的预定义选择标准
```

### outputVariant

`outputVariant` 参数被用于传递程序的设计名称，改变数据的输出。仅限在 SAP 的选择屏幕上定义了设计参数的程序。

示例同步配置：

```yaml
type: magritte-sap-source-adapter
sapType: tcode  # SAP事务代码类型
obj: ZTEST_ALV  # SAP中的事务代码对象
outputVariant: /COMMERCIAL  # 输出变体，指定为/COMMERCIAL
```

### ingestionType

`ingestionType`参数可以被用于在将报告的输出发送到打印队列之前进行导入，这通常被称为“假脱机请求”。建议将`ingestionType`设置为`spool`，用于生成超过SAP内部表限制的数据报告。

默认情况下（如果未指定`ingestionType`），报告的输出将被实时导入并发送到Foundry。

:::callout{theme="neutral"}
由于假脱机请求的性质，使用`spool`导入类型时，所有列在导入到Foundry时都将具有`字符串`类型。
:::

同步配置示例：

```yaml
type: magritte-sap-source-adapter
sapType: tcode  # SAP事务代码（Transaction Code）
obj: ZTEST_ALV  # 需要处理的SAP对象名
ingestionType: spool  # 数据提取的方式为输出缓冲（Spool）
```
