---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/groupedLatLonBoundingBoxV1/",
  "title": "分组经纬度边界框",
  "page_id": "groupedLatLonBoundingBoxV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/groupedGeometryUnionV1/",
  "next": "/zh/foundry/pb-functions-expression/gzipDecompressV1/",
  "scraped_at": "2026-07-13T05:55:29.047631+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 分组经纬度边界框

> 支持于: 批处理

返回一个结构体，其中包含给定列中所有有效几何形状的整个边界框。无效几何形状被视为null并被忽略。

**表达式类别**: 地理空间

## 声明的参数

* **表达式** - 要计算整个边界框的几何形状列。<br>*Expression\<Geometry>*

**输出类型:** *LatLonBoundingBox*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `geometry`

**给定输入表:**

| geometry |
| ----- |
| {"type":"LineString","coordinates":\[\[1,0],\[0,8.4]]} |
| {"type":"Point","coordinates":\[125.6, -92.3]} |
| {"type":"Polygon","coordinates":\[\[\[0,0],\[1,6.3],\[-6,1],\[0,0]]]} |

**输出:** {<br> maxLat -> 8.4,<br> maxLon -> 125.6,<br> minLat -> -92.3,<br> minLon -> -6.0,<br>}

***

### 示例 2: 空情况

**参数值:**

* **表达式**: `geometry`

**给定输入表:**

| geometry |
| ----- |
| *null* |

**输出:** *null*

***

### 示例 3: 边缘情况

**参数值:**

* **表达式**: `geometry`

**给定输入表:**

| geometry |
| ----- |
| Invalid GeoJSON |
| {"type":"LineString","coordinates":\[\[2,0],\[0,4.8]]} |

**输出:** {<br> maxLat -> 4.8,<br> maxLon -> 2.0,<br> minLat -> 0.0,<br> minLon -> 0.0,<br>}

***
