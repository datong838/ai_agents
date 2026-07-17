---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geometrySetZCoordinateV1/",
  "title": "几何设置z坐标",
  "page_id": "geometrySetZCoordinateV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/geometryRotate2dV1/",
  "next": "/zh/foundry/pb-functions-expression/geometryShortestDistanceV1/",
  "scraped_at": "2026-07-13T05:55:50.578650+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 几何设置z坐标

> 支持于: 批处理, 流式处理

设置几何的z坐标。如果几何已有z坐标，将被覆盖。

**表达式类别**: 地理空间

## 声明的参数

* **Geometry** - 几何。<br>*Expression\<Geometry>*
* **Z coordinate** - Z坐标。<br>*Expression\<Double>*

**输出类型:** *Geometry*

## 示例

### 示例 1: 基本情况

**参数值:**

* **Geometry**: `geometry`
* **Z coordinate**: `zCoordinate`

| geometry | zCoordinate | **输出** |
| ----- | ----- | ----- |
| {"type":"Point","coordinates":\[1.0, 2.0]} | 1.0 | {"type":"Point","coordinates":\[1.0, 2.0, 1.0]} |
| {"type":"Point","coordinates":\[1.0, 2.0, 3.0]} | 1.0 | {"type":"Point","coordinates":\[1.0, 2.0, 1.0]} |

***

### 示例 2: 空值情况

**参数值:**

* **Geometry**: `geometry`
* **Z coordinate**: `zCoordinate`

| geometry | zCoordinate | **输出** |
| ----- | ----- | ----- |
| *null* | 0.0 | *null* |
| {"type":"Point","coordinates":\[1.0, 2.0]} | *null* | {"type":"Point","coordinates":\[1.0, 2.0]} |

***
