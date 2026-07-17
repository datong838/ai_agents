---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/coalesceV1/",
  "title": "合并数据",
  "page_id": "coalesceV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/assignTimestampsAndWatermarksV1/",
  "next": "/zh/foundry/pb-functions-transform/computeExpressionIfAbsentV1/",
  "scraped_at": "2026-07-13T05:58:07.631151+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 合并数据

> 支持于: 批处理

用于减少分区数量的操作。如果您有1000个分区并合并为100个，将不会发生洗牌，而是每个新的100个分区将承接当前10个分区。如果请求的分区数量较多，则将保持当前的分区数量。

**变换类别**: 其他

## 声明的参数

* **数据集** - 要进行合并操作的数据集。<br>*Table*
* **分区数量** - 要合并到的分区数量。<br>*Literal\<Integer>*
