---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/perimeterV1/",
  "title": "周长",
  "page_id": "perimeterV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/percentRankV1/",
  "next": "/zh/foundry/pb-functions-expression/pivotExpressionV1/",
  "scraped_at": "2026-07-13T05:57:05.606901+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 周长

> 支持于: 批处理, 流处理

使用球形近似计算几何体的周长，单位为米。对于线字符串或点，这等于0。

**表达式类别**: 地理空间

## 声明的参数

* **表达式** - GeoJSON字符串。<br>*Expression\<Geometry>*

**输出类型:** *Double*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"Polygon","coordinates":\[\[\[-102.05,41.0],\[-109.05,41.0],\[-109.05,37.0],\[-102.05,37.0],\[-102.05,41.0]]]} | 2098333.448556529 |

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"MultiPolygon","coordinates":\[\[\[\[-102.05,41.0],\[-109.05,41.0],\[-109.05,37.0],\[-102.05,37.0],\[-102.05,41.0]]],\[\[\[-1.0,-1.0],\[1.0,-1.0],\[1.0,1.0],\[-1.0,1.0],\[-1.0,-1.0]]]]} | 2987826.341349821 |

***

### 示例 3: 基本情况

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"Polygon","coordinates":\[\[\[-1.0,-1.0],\[1.0,-1.0],\[1.0,1.0],\[-1.0,1.0],\[-1.0,-1.0]]]} | 889492.8927932923 |

***

### 示例 4: 空值情况

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| *null* | *null* |

***

### 示例 5: 边缘情况

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| not geoJson | *null* |

***

### 示例 6: 边缘情况

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"LineString","coordinates":\[\[0.0,0.0],\[1.0,0.0]]} | 0.0 |

***

### 示例 7: 边缘情况

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"Point","coordinates":\[0.0,0.0]} | 0.0 |

***

### 示例 8: 边缘情况

**参数值:**

* **表达式**: `geometry`

| geometry | **输出** |
| ----- | ----- |
| {"type":"Polygon","coordinates":\[\[\[-179.0,-1.0],\[179.0,-1.0],\[179.0,1.0],\[-179.0,1.0],\[-179.0,-1.0]]]} | 889492.8927932923 |

***
