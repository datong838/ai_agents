---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geoPointToGeometryV1/",
  "title": "将 GeoPoint 转换为几何",
  "page_id": "geoPointToGeometryV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/geoPointToMgrsV1/",
  "next": "/zh/foundry/pb-functions-expression/mgrsToGeoPointV1/",
  "scraped_at": "2026-07-13T05:53:31.356898+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将 GeoPoint 转换为几何

> 支持于：批处理，流处理

将 GeoPoint 转换为类型为点的 GeoJSON。

**表达式类别**：地理空间

## 声明的参数

* **表达式** - 一个有效的 GeoPoint。<br>*Expression\<GeoPoint>*

**输出类型：** *Geometry*

## 示例

### 示例 1：基本情况

**参数值：**

* **表达式**: `geoPoint`

| geoPoint | **输出** |
| ----- | ----- |
| {<br> latitude -> 58.0,<br> longitude -> 32.0,<br>} | {"type":"Point","coordinates": \[32.0, 58.0]} |
| *null* | *null* |
| {<br> latitude -> 40.753206,<br> longitude -> -73.989015,<br>} | {"type":"Point","coordinates": \[-73.989015, 40.753206]} |

***
