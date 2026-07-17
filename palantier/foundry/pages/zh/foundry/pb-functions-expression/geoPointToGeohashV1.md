---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geoPointToGeohashV1/",
  "title": "将 GeoPoint 转换为 Geohash",
  "page_id": "geoPointToGeohashV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/dmsToGeoPointV1/",
  "next": "/zh/foundry/pb-functions-expression/geoPointToMgrsV1/",
  "scraped_at": "2026-07-13T05:53:30.367515+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将 GeoPoint 转换为 Geohash

> 支持于: 批处理, 流处理

将 GeoPoint 转换为包含该 GeoPoint 的指定精度的 base32 编码 Geohash。有关 Geohash 的更多信息，请参见: https://en.wikipedia.org/wiki/Geohash 。

**表达式类别**: 地理空间

## 声明的参数

* **GeoPoint** - 要转换的 GeoPoint。<br>*Expression\<GeoPoint>*
* **输出 Geohash 精度** - 输出 Geohash 字符串中返回的 base32 字符数。<br>*Expression\<Integer>*

**输出类型:** *Geohash*

## 示例

### 示例 1: 基本案例

**参数值:**

* **GeoPoint**: `point`
* **输出 Geohash 精度**: 5

| point | **输出** |
| ----- | ----- |
| {<br> **latitude**: -20.0,<br> **longitude**: 80.0,<br>} | mu2yh |
| {<br> **latitude**: -77.0599,<br> **longitude**: 38.9031,<br>} | hf79t |
| *null* | *null* |

***

### 示例 2: 基本案例

**参数值:**

* **GeoPoint**: `point`
* **输出 Geohash 精度**: `precision`

| point | precision | **输出** |
| ----- | ----- | ----- |
| {<br> **latitude**: -20.0,<br> **longitude**: 80.0,<br>} | 5 | mu2yh |
| {<br> **latitude**: -77.0599,<br> **longitude**: 38.9031,<br>} | 3 | hf7 |
| {<br> **latitude**: -82.77450568,<br> **longitude**: -179.55742495,<br>} | 12 | 0123456789zb |
| {<br> **latitude**: 1.0,<br> **longitude**: -1.0,<br>} | 12 | ebpm9npc6m9b |
| {<br> **latitude**: 1.0,<br> **longitude**: -1.0,<br>} | *null* | *null* |

***
