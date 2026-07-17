---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/inverseHaversineV1/",
  "title": "计算目的地点",
  "page_id": "inverseHaversineV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/h3BufferV1/",
  "next": "/zh/foundry/pb-functions-expression/haversineV1/",
  "scraped_at": "2026-07-13T05:53:19.762685+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 计算目的地点

> 支持于: 批处理, 流处理

根据起始点、航向和距离，计算沿指定路径的目的地点。

**表达式类别**: 地理空间

## 声明的参数

* **航向** - 当前航向（以度为单位）。<br>*Expression\<Double>*
* **距离** - 到目的地的距离（以米为单位）。<br>*Expression\<Double>*
* **起始点** - 点a的经度和纬度。<br>*Expression\<GeoPoint>*
* **非必填** **计算方法。** - 沿地球球面近似的路径。默认为大圆航线。<br>*Enum\<Great Circle, Loxodrome/Rhumb Line>*

**输出类型:** *GeoPoint*

## 示例

### 示例 1: 基础案例

**参数值:**

* **航向**: `course`
* **距离**: `distance`
* **起始点**: `point_a`
* **计算方法。**: `GREAT_CIRCLE`

| point\_a | 航向 | 距离 | **输出** |
| ----- | ----- | ----- | ----- |
| {<br> **纬度**: 48.8567,<br> **经度**: 2.3508,<br>} | 225.0 | 32000.0 | {<br> **纬度**: 48.65279552300661,<br> **经度**: 2.0427666779658806,<br>} |

***

### 示例 2: 基础案例

**参数值:**

* **航向**: `course`
* **距离**: `distance`
* **起始点**: `point_a`
* **计算方法。**: `LOXODROME`

| point\_a | 航向 | 距离 | **输出** |
| ----- | ----- | ----- | ----- |
| {<br> **纬度**: 48.8567,<br> **经度**: 2.3508,<br>} | 225.0 | 32000.0 | {<br> **纬度**: 48.65320703115239,<br> **经度**: 2.0421403965968183,<br>} |

***

### 示例 3: 空值案例

**参数值:**

* **航向**: `course`
* **距离**: `distance`
* **起始点**: `point_a`
* **计算方法。**: *null*

| point\_a | 航向 | 距离 | **输出** |
| ----- | ----- | ----- | ----- |
| {<br> **纬度**: 48.8567,<br> **经度**: 2.3508,<br>} | 225.0 | 32000.0 | {<br> **纬度**: 48.65279552300661,<br> **经度**: 2.0427666779658806,<br>} |

***

### 示例 4: 边缘案例

**参数值:**

* **航向**: `course`
* **距离**: `distance`
* **起始点**: `point_a`
* **计算方法。**: `LOXODROME`

| point\_a | 航向 | 距离 | **输出** |
| ----- | ----- | ----- | ----- |
| {<br> **纬度**: 42.779577,<br> **经度**: -156.581761,<br>} | 10.0 | 8000000.0 | {<br> **纬度**: 90.0,<br> **经度**: 0.0,<br>} |

***
