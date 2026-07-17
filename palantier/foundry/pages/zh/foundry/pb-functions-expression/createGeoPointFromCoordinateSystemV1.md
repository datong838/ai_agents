---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/createGeoPointFromCoordinateSystemV1/",
  "title": "从坐标系统创建GeoPoint",
  "page_id": "createGeoPointFromCoordinateSystemV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/covarianceV1/",
  "next": "/zh/foundry/pb-functions-expression/createEmptyArrayV1/",
  "scraped_at": "2026-07-13T05:54:03.306844+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从坐标系统创建GeoPoint

> 支持于: 批处理, 流式处理

从源坐标系统获取一对坐标并将其变换为WGS 84纬度/经度值。坐标系统（也称为坐标参考系统或空间参考系统）代表不同的系统，用于识别地球上某个点的位置，通常在标准化数据库（如EPSG）中通过键进行识别。如果给定的投影不支持或任一坐标为空，则返回空值。

**表达式类别**: 地理空间

## 声明的参数

* **源坐标系统** - 坐标系统标识符，格式为"authority:id"。例如，UTM区域18N可以通过EPSG:32618标识。<br>*Literal<字符串>*
* **X坐标** - 源坐标系统中的X坐标（通常为“东移”）。<br>*Expression\<Numeric>*
* **Y坐标** - 源坐标系统中的Y坐标（通常为“北移”）。<br>*Expression\<Numeric>*

**输出类型:** *GeoPoint*

## 示例

### 示例 1: 基本案例

**参数值:**

* **源坐标系统**: EPSG:32618
* **X坐标**: `x_coordinate`
* **Y坐标**: `y_coordinate`

| x\_coordinate | y\_coordinate | **输出** |
| ----- | ----- | ----- |
| 322190.2233952965 | 4306505.703879281 | {<br> latitude -> 38.88944258,<br> longitude -> -77.05014581,<br>} |
| 323243.1361536059 | 4318298.06539618 | {<br> latitude -> 38.99585379643137,<br> longitude -> -77.04105678275415,<br>} |
| 407063.63465300016 | 4764873.719585404 | {<br> latitude -> 43.03086518778498,<br> longitude -> -76.14077251822197,<br>} |

***

### 示例 2: 基本案例

**参数值:**

* **源坐标系统**: EPSG:28992
* **X坐标**: `x_coordinate`
* **Y坐标**: `y_coordinate`

| x\_coordinate | y\_coordinate | **输出** |
| ----- | ----- | ----- |
| 142735.75 | 470715.91 | {<br> latitude -> 52.22438577,<br> longitude -> 5.20771293,<br>} |
| 92891.44163 | 437357.50015 | {<br> latitude -> 51.9212285,<br> longitude -> 4.4843492,<br>} |
| 81047.96352 | 454913.24287 | {<br> latitude -> 52.0775512,<br> longitude -> 4.3084213,<br>} |

***
