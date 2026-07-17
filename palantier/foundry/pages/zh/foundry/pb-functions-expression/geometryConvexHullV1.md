---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geometryConvexHullV1/",
  "title": "获取几何体的凸包",
  "page_id": "geometryConvexHullV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/getStructFieldV2/",
  "next": "/zh/foundry/pb-functions-expression/greaterThanV1/",
  "scraped_at": "2026-07-13T05:55:24.804483+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 获取几何体的凸包

> 支持于: 批处理, 流处理

给定一个有效的GeoJSON输入字符串，返回一个GeoJSON字符串，该字符串是几何体的凸包。凸包是包含几何体的最小凸多边形。

**表达式类别**: 地理空间

## 声明的参数

* **表达式** - 计算凸包的GeoJSON值。<br>*Expression\<Geometry>*

**输出类型:** *Geometry*

## 示例

### 示例 1: 基础案例

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[2.0,0.0],\[2.0,1.0],\[1.0,1.0],\[1.0,2.0],\[0.0,2.0],\[0.0,0.0]]]} | {"type":"Polygon", "coordinates":\[\[\[0.0, 0.0], \[0.0, 2.0], \[1.0, 2.0], \[2.0, 1.0], \[2.0, 0.0], \[0.0, 0.0]]]} |
| *null* | *null* |

***

### 示例 2: 基础案例

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"Polygon","coordinates":\[\[\[0.0,0.0],\[1.0,0.0],\[0.0,1.0],\[0.0,0.0]]]} | {"type":"Polygon","coordinates":\[\[\[0.0, 0.0], \[0.0, 1.0], \[1.0, 0.0], \[0.0, 0.0]]]} |

***

### 示例 3: 基础案例

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"MultiPolygon","coordinates":\[\[\[\[0.0,0.0],\[1.0,0.0],\[1.0,1.0],\[0.0,1.0],\[0.0,0.0]]],\[\[\[2.0,0.0],\[3.0,0.0],\[3.0,1.0],\[2.0,1.0],\[2.0,0.0]]]]} | {"type":"Polygon", "coordinates":\[\[\[0.0, 0.0], \[0.0, 1.0], \[3.0, 1.0], \[3.0, 0.0],\[0.0, 0.0]]]} |

***

### 示例 4: 基础案例

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"MultiPoint","coordinates":\[\[0.0,0.0],\[0.0,1.0],\[2.0,0.0], \[2.0,1.0]]} | {"type":"Polygon","coordinates":\[\[\[0.0, 0.0], \[0.0, 1.0], \[2.0, 1.0], \[2.0, 0.0], \[0.0, 0.0]]]} |

***
