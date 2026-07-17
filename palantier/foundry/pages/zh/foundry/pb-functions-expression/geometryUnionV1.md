---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geometryUnionV1/",
  "title": "几何联合",
  "page_id": "geometryUnionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/geometryTranslateV1/",
  "next": "/zh/foundry/pb-functions-expression/h3IndexExpressionV1/",
  "scraped_at": "2026-07-13T05:55:09.305495+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 几何联合

> 支持于: 批处理, 流处理

合并两个几何图形以创建一个单一的几何图形。

**表达式类别**: 地理空间

## 声明的参数

* **几何 a** - 几何 a。<br>*Expression\<Geometry>*
* **几何 b** - 几何 b。<br>*Expression\<Geometry>*

**输出类型:** *Geometry*

## 示例

### 示例 1: 基本案例

**参数值:**

* **几何 a**: `geometry_a`
* **几何 b**: `geometry_b`

| geometry\_a | geometry\_b | **输出** |
| ----- | ----- | ----- |
| {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[0.0,1.0],\[1.0,1.0],\[1.0,0.0],\[0.0,0.0]]]} | {"type":"Polygon","coordinates":\[\[\[0.5,0.0],\[1.5,0.0],\[1.5,1.0],\[0.5,1.0],\[0.5,0.0]]]} | {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[0.0,1.0],\[0.5,1.0],\[1.0,1.0],\[1.5,1.0],\[1.5,0.0],\[1.0,0.0],\[0.5,0.0],\[0.0,0.0]]]} |
| {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[0.0,1.0],\[1.0,1.0],\[1.0,0.0],\[0.0,0.0]]]} | {"type":"Polygon","coordinates":\[\[\[5.0,5.0],\[5.0,6.0],\[6.0,6.0],\[6.0,5.0],\[5.0,5.0]]]} | {"type":"MultiPolygon","coordinates":\[\[\[\[0.0,0.0],\[0.0,1.0],\[1.0,1.0],\[1.0,0.0],\[0.0,0.0]]],\[\[\[5.0,5.0],\[5.0,6.0],\[6.0,6.0],\[6.0,5.0],\[5.0,5.0]]]]} |
| {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[0.0,1.0],\[1.0,1.0],\[1.0,0.0],\[0.0,0.0]]]} | {"type":"Polygon","coordinates":\[\[\[1.0,0.0],\[1.0,1.0],\[2.0,1.0],\[2.0,0.0],\[1.0,0.0]]]} | {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[0.0,1.0],\[1.0,1.0],\[2.0,1.0],\[2.0,0.0],\[1.0,0.0],\[0.0,0.0]]]} |
| {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[0.0,1.0],\[1.0,1.0],\[1.0,0.0],\[0.0,0.0]]]} | {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[0.0,1.0],\[1.0,1.0],\[1.0,0.0],\[0.0,0.0]],\[\[0.25,0.25],\[0.5,0.25],\[0.5,0.5],\[0.25,0.5],\[0.25,0.25]]]} | {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[0.0,1.0],\[1.0,1.0],\[1.0,0.0],\[0.0,0.0]]]} |
| {"type":"LineString","coordinates":\[\[0.0,0.0],\[1.0,0.0]]} | {"type":"Polygon","coordinates":\[\[\[1.0,0.0],\[1.0,1.0],\[2.0,1.0],\[2.0,0.0],\[1.0,0.0]]]} | {"type":"GeometryCollection","geometries":\[{"type":"LineString","coordinates":\[\[0.0,0.0],\[1.0,0.0]]},{"type":"Polygon","coordinates":\[\[\[1.0,0.0],\[1.0,1.0],\[2.0,1.0],\[2.0,0.0],\[1.0,0.0]]]}]} |
