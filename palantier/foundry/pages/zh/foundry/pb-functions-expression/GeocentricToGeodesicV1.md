---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/GeocentricToGeodesicV1/",
  "title": "将地心坐标转换为WGS 84大地坐标",
  "page_id": "GeocentricToGeodesicV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/UnhexToStringV1/",
  "next": "/zh/foundry/pb-functions-expression/convertLegacyOffsetDateTimeV1/",
  "scraped_at": "2026-07-13T05:53:48.345014+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将地心坐标转换为WGS 84大地坐标

> 支持于: 批处理, 流处理

将地心笛卡尔坐标转换为大地极坐标。高度定义为椭球体上的高度。如果任何坐标为null，则输出将为null。

**表达式类别**: 地理空间

## 声明的参数

* **X坐标** - 源坐标系中的X坐标。<br>*表达式<数值>*
* **Y坐标** - 源坐标系中的Y坐标。<br>*表达式<数值>*
* **Z坐标** - 源坐标系中的Z坐标。<br>*表达式<数值>*

**输出类型:** *带高度的GeoPoint*

## 示例

### 示例1: 基本情况

**参数值:**

* **X坐标**: `x_coordinate`
* **Y坐标**: `y_coordinate`
* **Z坐标**: `z_coordinate`

| x\_coordinate | y\_coordinate | z\_coordinate | **输出** |
| ----- | ----- | ----- | ----- |
| 0.0 | 6378137.0 | 0.0 | {<br> altitude -> 0.0,<br> geoPoint -> {<br> latitude -> 0.0,<br> longitude -> 90.0,<br>},<br>} |
| 0.0 | -6378137.0 | 0.0 | {<br> altitude -> 0.0,<br> geoPoint -> {<br> latitude -> 0.0,<br> longitude -> -90.0,<br>},<br>} |
| -6378137.0 | 0.0 | 0.0 | {<br> altitude -> 0.0,<br> geoPoint -> {<br> latitude -> 0.0,<br> longitude -> 180.0,<br>},<br>} |
| -6378137.0 | -0.0 | 0.0 | {<br> altitude -> 0.0,<br> geoPoint -> {<br> latitude -> 0.0,<br> longitude -> -180.0,<br>},<br>} |
| 0.0 | 0.0 | 6356752.314245179 | {<br> altitude -> 0.0,<br> geoPoint -> {<br> latitude -> 90.0,<br> longitude -> 0.0,<br>},<br>} |
| 0.0 | 0.0 | -6356752.314245179 | {<br> altitude -> 0.0,<br> geoPoint -> {<br> latitude -> -90.0,<br> longitude -> 0.0,<br>},<br>} |

***

### 示例2: 空值情况

**参数值:**

* **X坐标**: `x_coordinate`
* **Y坐标**: `y_coordinate`
* **Z坐标**: `z_coordinate`

| x\_coordinate | y\_coordinate | z\_coordinate | **输出** |
| ----- | ----- | ----- | ----- |
| *null* | 0.0 | 0.0 | *null* |
| 0.0 | *null* | 0.0 | *null* |
| 0.0 | 0.0 | *null* | *null* |

***

### 示例3: 边缘情况

**参数值:**

* **X坐标**: `x_coordinate`
* **Y坐标**: `y_coordinate`
* **Z坐标**: `z_coordinate`

| x\_coordinate | y\_coordinate | z\_coordinate | **输出** |
| ----- | ----- | ----- | ----- |
| 1.0E-7 | 0.0 | 6356752.314245179 | {<br> altitude -> 0.0,<br> geoPoint -> {<br> latitude -> 89.9999999999991,<br> longitude -> 0.0,<br>},<br>} |
| 1.0E-7 | 0.0 | -6356752.314245179 | {<br> altitude -> 0.0,<br> geoPoint -> {<br> latitude -> -89.9999999999991,<br> longitude -> 0.0,<br>},<br>} |
| -6378137.0 | -1.0E-7 | 0.0 | {<br> altitude -> 0.0,<br> geoPoint -> {<br> latitude -> 0.0,<br> longitude -> -179.9999999999991,<br>},<br>} |
| -6378137.0 | 1.0E-7 | 0.0 | {<br> altitude -> 0.0,<br> geoPoint -> {<br> latitude -> 0.0,<br> longitude -> 179.9999999999991,<br>},<br>} |

***
