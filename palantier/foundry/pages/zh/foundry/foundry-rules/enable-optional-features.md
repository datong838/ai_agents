---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/foundry-rules/enable-optional-features/",
  "title": "启用非必填功能",
  "page_id": "enable-optional-features",
  "category_id": "ontology",
  "section_id": "foundry-rules",
  "previous": "/zh/foundry/foundry-rules/customization/",
  "next": "/zh/foundry/foundry-rules/add-a-custom-property/",
  "scraped_at": "2026-07-14T04:48:28.183220+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 启用非必填功能

通过编辑[规则工作坊应用程序](/zh/foundry/foundry-rules/workshop-application/)中规则编辑器微件的配置，可以启用或禁用非必填功能，如下图所示。

![非必填功能配置](../../../images/foundry/foundry-rules/enable_optional_features.png)

Foundry Rules 可以启用或禁用一系列非必填逻辑面板：

* **窗口面板：** 支持[窗口函数 ↗](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-window.html)。
* **聚合面板：** 计算分组列上的聚合。
* **合并面板：** 合并其他数据集或对象。
* **表达式面板：** 执行任意表达式以添加列或筛选。
* **选择列面板：** 选择部分列以传递到下一个逻辑面板。
* **联合面板：** 联合其他数据集或对象。

此外，还有一个选项可以启用或禁用从 Contour 导入规则。

* **Contour 导入：** 导入并转换存储在[Contour 分析](/zh/foundry/contour/core-concepts/)中的逻辑为规则。

最后，Foundry Rules 支持直接在时间序列数据上编写规则。

* **时间序列：** 添加[时间序列面板](/zh/foundry/foundry-rules/timeseries-concepts/#add-timeseries-board)，可以直接作为规则的一部分操作时间序列。
