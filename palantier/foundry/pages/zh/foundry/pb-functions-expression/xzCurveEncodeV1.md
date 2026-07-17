---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/xzCurveEncodeV1/",
  "title": "获取信封的XZ曲线索引",
  "page_id": "xzCurveEncodeV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/polygonToH3V1/",
  "next": "/zh/foundry/pb-functions-expression/getBearingV1/",
  "scraped_at": "2026-07-13T05:55:23.617448+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 获取信封的XZ曲线索引

> 支持于: 批处理, 流处理

将信封编码为XZ曲线。

**表达式类别**: 地理空间

## 声明的参数

* **曲线预设** - 指定要使用的曲线预设，分辨率越高的曲线查询成本越高，但产生的误报越少。<br>*枚举\<LonLat10km, LonLat150km, LonLat1km>*
* **信封** - 用于索引的几何信封，经度映射为x，纬度映射为y。<br>*表达式\<LatLonBoundingBox>*

**输出类型:** *长整型*

## 示例

### 示例 1: 基本情况

**参数值:**

* **曲线预设**: `LON_LAT_10KM`
* **信封**: `envelope`

| 信封 | **输出** |
| ----- | ----- |
| {<br> maxLat -> 2.0,<br> maxLon -> 3.0,<br> minLat -> 0.0,<br> minLon -> 1.0,<br>} | 16777222 |
| {<br> maxLat -> 2.0,<br> maxLon -> 3.0,<br> minLat -> *null*,<br> minLon -> 1.0,<br>} | *null* |
