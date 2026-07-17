---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/mgrsToGeoPointV1/",
  "title": "将 MGRS 转换为 GeoPoint",
  "page_id": "mgrsToGeoPointV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/geoPointToGeometryV1/",
  "next": "/zh/foundry/pb-functions-expression/stringToDateV2/",
  "scraped_at": "2026-07-13T05:53:36.914515+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将 MGRS 转换为 GeoPoint

> 支持于: 批处理, 流处理

将 MGRS（军事网格参考系统）坐标转换为遵循 WGS84 坐标系统（即 EPSG:4326）的 GeoPoint。

**表达式类别**: 地理空间

## 声明的参数

* **表达式** - 要转换的 MGRS（军事网格参考系统）坐标。<br>*Expression\<MGRS>*

**输出类型:** *GeoPoint*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `mgrs`

| mgrs | **输出** |
| ----- | ----- |
| ZAF0193788990 | {<br> **纬度**: 88.99999659707431,<br> **经度**: 0.9996456505181999,<br>} |

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: `mgrs`

| mgrs | **输出** |
| ----- | ----- |
| 4Q FJ 12345 67890 | {<br> **纬度**: 21.409796671597924,<br> **经度**: -157.91608117421092,<br>} |
| 4Q FJ 1 6 | {<br> **纬度**: 21.338665624760598,<br> **经度**: -157.93921670599434,<br>} |
| 4Q FJ 123 678 | {<br> **纬度**: 21.40898645576642,<br> **经度**: -157.91652127483704,<br>} |

***

### 示例 3: 空值情况

**参数值:**

* **表达式**: `mgrs`

| mgrs | **输出** |
| ----- | ----- |
| *null* | *null* |

***
