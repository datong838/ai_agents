---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geometryRotate2dV1/",
  "title": "几何旋转2D",
  "page_id": "geometryRotate2dV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/geometryLengthV1/",
  "next": "/zh/foundry/pb-functions-expression/geometrySetZCoordinateV1/",
  "scraped_at": "2026-07-13T05:55:03.604203+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 几何旋转2D

> 支持于: 流式

将提供的几何图形以提供的GeoPoint为中心进行顺时针二维旋转。此旋转发生在提供的坐标参考系中，然后投影回WGS84。

**表达式类别**: 地理空间

## 声明的参数

* **角度（度）** - 顺时针旋转的角度（度）。<br>*Literal\<Double>*
* **中心GeoPoint** - 旋转围绕发生的中心GeoPoint。假定为WGS84。<br>*Expression\<GeoPoint>*
* **几何列** - 应用旋转的几何图形。<br>*Expression\<Geometry>*
* **投影坐标系统** - 格式为"authority:id"的坐标系统标识符。例如，UTM带18N可通过EPSG:32618识别。几何图形将被投影到源坐标系统，应用旋转，然后投影回WGS84。<br>*Literal<字符串>*

**输出类型:** *Geometry*

## 示例

### 示例 1: 基本案例

**参数值:**

* **角度（度）**: 90.0
* **中心GeoPoint**: `geoPoint`
* **几何列**: `geometry`
* **投影坐标系统**: EPSG:4326

| geometry | geoPoint | **输出** |
| ----- | ----- | ----- |
| {"type":"Point","coordinates":\[1.0, 0.0]} | {<br> latitude -> 0.0,<br> longitude -> 0.0,<br>} | {"type":"Point","coordinates":\[6.123233995736766E-17, -1.0]} |

***

### 示例 2: 基本案例

**参数值:**

* **角度（度）**: 270.0
* **中心GeoPoint**: `geoPoint`
* **几何列**: `geometry`
* **投影坐标系统**: EPSG:32618

| geometry | geoPoint | **输出** |
| ----- | ----- | ----- |
| {"type":"Point","coordinates":\[-77.0, 20.0]} | {<br> latitude -> 22.0,<br> longitude -> -76.0,<br>} | {"type":"Point","coordinates":\[-73.8719606865239, 21.041418391118174]} |

***

### 示例 3: 基本案例

**参数值:**

* **角度（度）**: 180.0
* **中心GeoPoint**: `geoPoint`
* **几何列**: `geometry`
* **投影坐标系统**: EPSG:4326

| geometry | geoPoint | **输出** |
| ----- | ----- | ----- |
| {"type":"LineString","coordinates":\[\[0.0, 0.0], \[1.0, 0.0]]} | {<br> latitude -> 1.0,<br> longitude -> 1.0,<br>} | {"type":"LineString","coordinates":\[\[2.0, 2.0], \[0.9999999999999999, 2.0]]} |

***

### 示例 4: 空案例

**参数值:**

* **角度（度）**: 90.0
* **中心GeoPoint**: `geoPoint`
* **几何列**: `geometry`
* **投影坐标系统**: EPSG:4326

| geometry | geoPoint | **输出** |
| ----- | ----- | ----- |
| *null* | *null* | *null* |

***
