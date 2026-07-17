---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/convertLegacyOffsetDateTimeV1/",
  "title": "转换旧版 OffsetDateTime",
  "page_id": "convertLegacyOffsetDateTimeV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/GeocentricToGeodesicV1/",
  "next": "/zh/foundry/pb-functions-expression/linestringToPolygonV1/",
  "scraped_at": "2026-07-13T05:53:49.657223+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 转换旧版 OffsetDateTime

> 支持于: 批处理

将旧版 OffsetDateTime 列转换为可用于所有 Foundry 流水线的时间戳。时间戳以 UTC 返回。

**表达式类别**: 日期时间

## 声明的参数

* **表达式** - *无描述*<br>*表达式\<Struct\<timestamp:Timestamp, offset:Integer>>*

**输出类型:** *时间戳*
