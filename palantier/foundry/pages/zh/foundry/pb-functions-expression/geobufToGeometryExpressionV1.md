---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geobufToGeometryExpressionV1/",
  "title": "解码 Geobuf 为 GeoJSON",
  "page_id": "geobufToGeometryExpressionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/dateSequenceV1/",
  "next": "/zh/foundry/pb-functions-expression/denseRankV1/",
  "scraped_at": "2026-07-13T05:54:30.643716+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 解码 Geobuf 为 GeoJSON

> 支持于: 批处理, 流处理

将 Geobuf 几何解码为 GeoJSON。

**表达式类别**: 地理空间

## 声明的参数

* **表达式** - 要解码的 Geobuf 几何。<br>*表达式\<Geobuf>*

**输出类型:** *几何*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `geobuf`

| geobuf | **输出** |
| ----- | ----- |
| MgwIABoIgKDCHoCKqDc= | {"type":"Point","coordinates": \[32.0, 58.0]} |
| *null* | *null* |
| MgwIABoIre7HRuzg7iY= | {"type":"Point","coordinates": \[-73.989015, 40.753206]} |

***
