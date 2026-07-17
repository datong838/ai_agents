---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/ontologyGeopointToGeopointV1/",
  "title": "从Ontology GeoPoint转换",
  "page_id": "ontologyGeopointToGeopointV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/jsonStringV2/",
  "next": "/zh/foundry/pb-functions-expression/UnhexV1/",
  "scraped_at": "2026-07-13T05:53:50.121977+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从Ontology GeoPoint转换

> 支持于: 批处理, 流处理

将一个Ontology GeoPoint转换为一个常规GeoPoint。Ontology GeoPoint是格式为'{lat},{lon}'的字符串，其中-90 <= lat <= 90 且 -180 <= lon <= 180。常规GeoPoint是格式为{"longitude": {long},"latitude": {lat}}的结构。

**表达式类别**: 地理空间

## 声明的参数

* **表达式** - 要转换的Ontology GeoPoint。<br>*表达式\<Ontology GeoPoint>*

**输出类型:** *GeoPoint*

## 例子

### 例子 1: 基本情况

**参数值:**

* **表达式**: `geopoint`

| geopoint | **输出** |
| ----- | ----- |
| -20.0000000,80.0000000 | {<br> **latitude**: -20.0,<br> **longitude**: 80.0,<br>} |
| 38.9031000,-77.0599000 | {<br> **latitude**: 38.9031,<br> **longitude**: -77.0599,<br>} |
| 41.9876543,-99.1234568 | {<br> **latitude**: 41.9876543,<br> **longitude**: -99.1234568,<br>} |

***

### 例子 2: 空值情况

**参数值:**

* **表达式**: `geopoint`

| geopoint | **输出** |
| ----- | ----- |
| 38.9031000, 41.9876543, 80.0000000 | *null* |
| A, 41.9876543 | *null* |
| this is a, test string | *null* |
| *null* | *null* |

***
