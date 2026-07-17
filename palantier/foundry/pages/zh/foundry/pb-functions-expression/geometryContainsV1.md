---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geometryContainsV1/",
  "title": "几何包含",
  "page_id": "geometryContainsV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/geometryCentroidV1/",
  "next": "/zh/foundry/pb-functions-expression/geometryDifferenceV1/",
  "scraped_at": "2026-07-13T05:55:10.351732+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 几何包含

> 支持于: 批处理, 流处理

确定几何 a 是否包含几何 b。位于多边形边界上的点或线不包含在另一个几何内。

**表达式类别**: 地理空间

## 声明的参数

* **几何 a** - 几何 a。<br>*Expression\<Geometry>*
* **几何 b** - 几何 b。<br>*Expression\<Geometry>*

**输出类型:** *Boolean*

## 示例

### 示例 1: 基本情况

**参数值:**

* **几何 a**: `geometry_a`
* **几何 b**: `geometry_b`

| geometry\_a | geometry\_b | **输出** |
| ----- | ----- | ----- |
| {"coordinates":\[\[\[-112.94377956164206,34.81725414459382],\[-112.94377956164206,30.006795384733323], \[... | {"type":"Point","coordinates":\[-100.0,32.0]} | true |
| {"coordinates":\[\[\[-112.94377956164206,34.81725414459382],\[-112.94377956164206,30.006795384733323], \[... | {"type":"LineString","coordinates":\[\[-112.94377956164206,34.81725414459382],\[-112.94377956164206,30.006795384733323]]} | false |
| {"type":"LineString","coordinates":\[\[-112.94377956164206,34.81725414459382],\[-112.94377956164206,30.006795384733323]]} | {"type":"Point","coordinates":\[-112.94377956164206,34.81725414459382]} | false |
| {"type":"Point","coordinates":\[-112.94377956164206,34.81725414459382]} | {"type":"Point","coordinates":\[-112.94377956164206,34.81725414459382]} | true |
| {"coordinates":\[\[\[-112.94377956164206,34.81725414459382],\[-112.94377956164206,30.006795384733323], \[... | {"coordinates":\[\[\[-111.94377956164206,33.81725414459382],\[-111.94377956164206,31.006795384733323], \[... | true |

***

### 示例 2: 空值情况

**参数值:**

* **几何 a**: `geometry_a`
* **几何 b**: `geometry_b`

| geometry\_a | geometry\_b | **输出** |
| ----- | ----- | ----- |
| *null* | *null* | *null* |
| {"type":"Point","coordinates":\[-112.94377956164206,34.81725414459382]} | *null* | *null* |
| *null* | {"type":"Point","coordinates":\[-112.94377956164206,34.81725414459382]} | *null* |

***
