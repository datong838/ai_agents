---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/windowedProjectV1/",
  "title": "窗口内的项目",
  "page_id": "windowedProjectV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/projectOnConditionV1/",
  "next": "/zh/foundry/pb-functions-transform/renameColumnsV1/",
  "scraped_at": "2026-07-13T05:59:19.558102+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 窗口内的项目

> 支持于: 批处理, 流处理

对窗口内的数据执行指定的聚合操作。每次收到新行时发出一行。

**变换类别**: 聚合

## 声明的参数

* **数据集** - 要执行聚合的数据集。<br>*表格*
* **表达式** - 要在窗口上评估的表达式列表。<br>*列表<表达式<任何类型>>*
* **窗口** - 用于按窗口对数据进行分组。<br>*窗口*
