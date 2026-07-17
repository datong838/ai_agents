---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/selectV1/",
  "title": "选择列",
  "page_id": "selectV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/rowSizeV1/",
  "next": "/zh/foundry/pb-functions-transform/complexSemiJoinV1/",
  "scraped_at": "2026-07-13T05:58:57.093230+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 选择列

> 支持于：批处理，流处理

从输入数据集中选择一组列。

**变换类别**：流行

## 声明的参数

* **要选择的列** - 要选择的列列表。<br>*List\<Column\<AnyType>>*
* **输入数据集** - 包含要选择列的源数据集。<br>*Table*
