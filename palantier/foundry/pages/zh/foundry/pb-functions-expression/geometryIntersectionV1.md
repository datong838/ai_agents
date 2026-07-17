---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geometryIntersectionV1/",
  "title": "几何交集",
  "page_id": "geometryIntersectionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/geometryExplodeToArrayV1/",
  "next": "/zh/foundry/pb-functions-expression/geometryLengthV1/",
  "scraped_at": "2026-07-13T05:55:20.333864+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 几何交集

> 支持于: 批处理，流处理

计算几何a与几何b相交的部分。

**表达式类别**: 地理空间

## 声明的参数

* **几何a** - 几何a。<br>*Expression\<Geometry>*
* **几何b** - 几何b。<br>*Expression\<Geometry>*

**输出类型:** *Geometry*

## 示例

### 示例 1: 基本案例

**参数值:**

* **几何a**: `geometry_a`
* **几何b**: `geometry_b`

| geometry\_a | geometry\_b | **输出** |
| ----- | ----- | ----- |
| {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[0.0,1.0],\[1.0,1.0],\[1.0,0.0],\[0.0,0.0]]]} | {"type":"Polygon","coordinates":\[\[\[0.5,0.0],\[1.5,0.0],\[1.5,1.0],\[0.5,1.0],\[0.5,0.0]]]} | {"type":"Polygon","coordinates":\[\[\[0.5,1.0],\[1.0,1.0],\[1.0,0.0],\[0.5,0.0],\[0.5,1.0]]]} |
| {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[0.0,1.0],\[1.0,1.0],\[1.0,0.0],\[0.0,0.0]]]} | {"type":"Polygon","coordinates":\[\[\[5.0,5.0],\[5.0,6.0],\[6.0,6.0],\[6.0,5.0],\[5.0,5.0]]]} | {"type":"Polygon","coordinates":\[\[]]} |
| {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[0.0,1.0],\[1.0,1.0],\[1.0,0.0],\[0.0,0.0]]]} | {"type":"Polygon","coordinates":\[\[\[1.0,0.0],\[1.0,1.0],\[2.0,1.0],\[2.0,0.0],\[1.0,0.0]]]} | {"type":"LineString","coordinates":\[\[1.0,1.0],\[1.0,0.0]]} |
| {"type":"Point","coordinates":\[0.0,0.0]} | {"type":"LineString","coordinates":\[\[0.0,0.0],\[1.0,0.0]]} | {"type":"Point","coordinates":\[0.0,0.0]} |
| {"type":"LineString","coordinates":\[\[0.0,0.0],\[1.0,0.0]]} | {"type":"Polygon","coordinates":\[\[\[2.0,0.0],\[2.0,1.0],\[3.0,1.0],\[3.0,0.0],\[2.0,0.0]]]} | {"type":"LineString","coordinates":\[]} |

***
