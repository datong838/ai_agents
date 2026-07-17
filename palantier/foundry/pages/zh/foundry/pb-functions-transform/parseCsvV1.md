---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/parseCsvV1/",
  "title": "从CSV文件中提取行",
  "page_id": "parseCsvV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/getManyStructFieldsV1/",
  "next": "/zh/foundry/pb-functions-transform/parseGeoJsonV1/",
  "scraped_at": "2026-07-13T05:58:19.509361+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从CSV文件中提取行

> 支持于: 批处理

读取文件的数据集并将每个CSV文件解析为行。

**变换类别**: 文件

## 声明的参数

* **数据集** - 要处理的文件数据集。<br>*文件*
* **模式** - 解析CSV文件时使用的模式定义。<br>*类型\<Struct>*
* *非必填* **列分隔符** - 提供CSV文件中使用的分隔符。默认分隔符是逗号。<br>*字面量<字符串>*
* *非必填* **包含最后修改的时间戳** - 指定输出数据集是否应包含文件的最后修改时间戳。默认值是false。<br>*字面量<布尔>*
* *非必填* **包含头部** - 指定CSV文件是否包含头部。默认值是false。<br>*字面量<布尔>*
