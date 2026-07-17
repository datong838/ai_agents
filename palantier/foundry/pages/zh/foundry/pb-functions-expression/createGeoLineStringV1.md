---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/createGeoLineStringV1/",
  "title": "创建线段几何",
  "page_id": "createGeoLineStringV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/createGeodesicLineStringV1/",
  "next": "/zh/foundry/pb-functions-expression/mapFromArraysV1/",
  "scraped_at": "2026-07-13T05:54:07.377208+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建线段几何

> 支持于: 批处理, 流处理

从给定的点创建GeoJSON线段几何。

**表达式类别**: 地理空间

## 声明参数

* **Points（点）** - 构成线段的点。<br>*Expression\<Array\<T>>*

**类型变量界限:** *T 接受 Struct\<longitude:Double, latitude:Double>*

**输出类型:** *Geometry（几何）*

## 示例

### 示例 1: 基本情况

**参数值:**

* **Points（点）**: `points`

| points（点） | **输出** |
| ----- | ----- |
| \[ {<br> **latitude（纬度）**: 10.0,<br> **longitude（经度）**: 0.0,<br>}, {<br> **latitude（纬度）**: 10.0,<br> **longitude（经度）**: 10.0,<br>} ] | {"type":"LineString","coordinates":\[\[0.0,10.0],\[10.0,10.0]]} |
| \[ {<br> **latitude（纬度）**: 10.0,<br> **longitude（经度）**: 10.0,<br>}, {<br> **latitude（纬度）**: 20.0,<... | {"type":"LineString","coordinates":\[\[10.0,10.0],\[20.0,20.0],\[30.0,30.0]]} |
| \[ {<br> **latitude（纬度）**: 0.0,<br> **longitude（经度）**: 179.0,<br>}, {<br> **latitude（纬度）**: 0.0,<br> **longitude（经度）**: 181.0,<br>} ] | {"type":"MultiLineString","coordinates":\[\[\[179.0,0.0],\[180.0,0.0]],\[\[-180.0,0.0],\[-179.0,0.0]]]} |
| \[ {<br> **latitude（纬度）**: 0.0,<br> **longitude（经度）**: -179.0,<br>}, {<br> **latitude（纬度）**: 0.0,<br> **longitude（经度）**: -181.0,<br>} ] | {"type":"MultiLineString","coordinates":\[\[\[180.0,0.0],\[179.0,0.0]],\[\[-179.0,0.0],\[-180.0,0.0]]]} |

***

### 示例 2: 空值情况

**参数值:**

* **Points（点）**: `points`

| points（点） | **输出** |
| ----- | ----- |
| *null* | *null* |
| \[ {<br> **latitude（纬度）**: 0.0,<br> **longitude（经度）**: 0.0,<br>}, *null* ] | *null* |

***

### 示例 3: 边缘情况

**参数值:**

* **Points（点）**: `points`

| points（点） | **输出** |
| ----- | ----- |
| \[  ] | *null* |
| \[ {<br> **latitude（纬度）**: 0.0,<br> **longitude（经度）**: 0.0,<br>} ] | *null* |

***
