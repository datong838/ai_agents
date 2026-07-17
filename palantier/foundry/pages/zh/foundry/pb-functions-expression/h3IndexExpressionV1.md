---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/h3IndexExpressionV1/",
  "title": "获取H3索引",
  "page_id": "h3IndexExpressionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/geometryUnionV1/",
  "next": "/zh/foundry/pb-functions-expression/polygonToH3V1/",
  "scraped_at": "2026-07-13T05:55:11.640692+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 获取H3索引

> 支持于: 批处理, 流式处理

将GeoPoint转换为给定分辨率的H3索引。对于分辨率<0或>15返回null。

**表达式类别**: 地理空间

## 声明的参数

* **GeoPoint** - 要转换为H3索引的GeoPoint (lon,lat)。<br>*Expression\<GeoPoint>*
* **Resolution** - H3网格分辨率，范围在0到15之间（包括0和15）。<br>*Expression\<Byte | Integer | Long | Short>*

**输出类型:** *H3 索引*

## 示例

### 示例 1: 基本案例

**参数值:**

* **GeoPoint**: `point`
* **Resolution**: 5

| point | **输出** |
| ----- | ----- |
| {<br> **latitude**: -20.0,<br> **longitude**: 80.0,<br>} | 85aa614bfffffff |
| {<br> **latitude**: 38.9031,<br> **longitude**: -77.0599,<br>} | 852aa84ffffffff |

***

### 示例 2: 基本案例

**参数值:**

* **GeoPoint**: <br>constructGeoPoint(<br> latitude: 80.0,<br> longitude: -20.0,<br>)
* **Resolution**: 5

**输出:** 8507b297fffffff

***
