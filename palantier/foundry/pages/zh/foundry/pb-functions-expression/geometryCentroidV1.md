---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geometryCentroidV1/",
  "title": "几何中心",
  "page_id": "geometryCentroidV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/geometryBufferV1/",
  "next": "/zh/foundry/pb-functions-expression/geometryContainsV1/",
  "scraped_at": "2026-07-13T05:55:01.298781+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 几何中心

> 支持于: 批处理, 流处理

使用地球的球面近似值返回几何图形的质心或“质心”。如果几何图形是混合维度的集合，则只有最高维度的元素会对质心产生贡献（例如，在点、线和多边形的集合中，点和线将被忽略）。

**表达式类别**: 地理空间

## 声明参数

* **表达式** - 有效的GeoJSON输入。<br>*Expression\<Geometry>*

**输出类型:** *GeoPoint*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"Polygon","coordinates":\[\[\[-1.0,-1.0],\[1.0,-1.0],\[1.0,1.0],\[-1.0,1.0],\[-1.0,-1.0]]]} | {<br> **纬度**: 0.0,<br> **经度**: 0.0,<br>} |
| {"type":"LineString","coordinates":\[\[30.0,0.0],\[35.0,0.0],\[50.0,0.0]]} | {<br> **纬度**: 0.0,<br> **经度**: 40.0,<br>} |
| {"type":"MultiPoint","coordinates":\[\[0.0,0.0],\[0.0,1.0]]} | {<br> **纬度**: 0.5,<br> **经度**: 0.0,<br>} |
| {"type":"MultiPoint","coordinates":\[\[160.0,0.0],\[-170.0,0.0]]} | {<br> **纬度**: 0.0,<br> **经度**: 175.0,<br>} |
| {"type":"GeometryCollection","geometries":\[{"type":"Polygon","coordinates":\[\[\[0.0,-0.017981],\[0.0017... | {<br> **纬度**: 0.0,<br> **经度**: 0.0,<br>} |
| *null* | *null* |

***
