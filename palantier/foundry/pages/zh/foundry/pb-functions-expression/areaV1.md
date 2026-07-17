---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/areaV1/",
  "title": "区域",
  "page_id": "areaV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arctan2V1/",
  "next": "/zh/foundry/pb-functions-expression/arrayAddV1/",
  "scraped_at": "2026-07-13T05:52:25.618615+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 区域

> 支持于: 批处理, 流处理

使用球形近似法计算几何图形的面积，单位为平方米。对于线字符串或点，此值等于0。

**表达式类别**: 地理空间

## 声明的参数

* **表达式** - GeoJSON 字符串。<br>*表达式\<Geometry>*

**输出类型:** *Double*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"Polygon","coordinates":\[\[\[-1.0,-1.0],\[1.0,-1.0],\[1.0,1.0],\[-1.0,1.0],\[-1.0,-1.0]]]} | 4.945989326791108E10 |
| {"type":"Polygon","coordinates":\[\[\[-179.0,-1.0],\[179.0,-1.0],\[179.0,1.0],\[-179.0,1.0],\[-179.0,-1.0]]]} | 4.945989326791108E10 |
| {"type":"Polygon","coordinates":\[\[\[-102.05,41.0],\[-109.05,41.0],\[-109.05,37.0],\[-102.05,37.0],\[-102.05,41.0]]]} | 2.6893150148718735E11 |
| {"type":"MultiPolygon","coordinates":\[\[\[\[-102.05,41.0],\[-109.05,41.0],\[-109.05,37.0],\[-102.05,37.0],\[-102.05,41.0]]],\[\[\[-1.0,-1.0],\[1.0,-1.0],\[1.0,1.0],\[-1.0,1.0],\[-1.0,-1.0]]]]} | 3.1839139475509845E11 |
| {"type":"LineString","coordinates":\[\[0.0,0.0],\[1.0,0.0]]} | 0.0 |
| {"type":"Point","coordinates":\[0.0,0.0]} | 0.0 |
| *null* | *null* |
| not geoJson | *null* |

***
