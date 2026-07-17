---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/cbacStringToGroupNamesV1/",
  "title": "解析分类字符串",
  "page_id": "cbacStringToGroupNamesV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/parseGeoJsonAsGeometryV1/",
  "next": "/zh/foundry/pb-functions-expression/parseDurationV1/",
  "scraped_at": "2026-07-13T05:56:45.666611+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 解析分类字符串

> 支持于：批处理

返回从给定分类字符串解析出的权限标记。此输出格式为结构体，其中结构体的第一个元素是相关权限标记的字符串列表。如果分类字符串无效，则此列表为空。结构体的第二个元素是错误消息的字符串。如果没有这样的消息（即分类字符串有效），则此字符串为空。如果分类字符串为空，则返回空。

**表达式类别**：其他

## 声明的参数

* **表达式** - 一个分类字符串。<br>*Expression<字符串>*

**输出类型:** *Struct\<groupNames:Array<字符串>, errors:字符串>*
