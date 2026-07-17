---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/parseJsonV1/",
  "title": "从JSON文件中提取行",
  "page_id": "parseJsonV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/parseGeoJsonV1/",
  "next": "/zh/foundry/pb-functions-transform/extractEmailDataAsRowsV1/",
  "scraped_at": "2026-07-13T05:58:32.189877+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从JSON文件中提取行

> 支持于: 批处理

读取文件的数据集，并将每个JSON文件解析成行。

**变换类别**: 文件, 字符串, 结构

## 声明的参数

* **允许JSON值跨多行** - 如果关闭，单个JSON记录必须完全在一行上。如果开启，单个JSON记录可以跨多行。<br>*Literal\<Boolean>*
* **数据集** - 要处理的文件数据集。<br>*Files*
* **模式** - 解析JSON文件时使用的模式定义。<br>*Type\<Struct>*
