---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/haversineV1/",
  "title": "计算haversine距离",
  "page_id": "haversineV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/inverseHaversineV1/",
  "next": "/zh/foundry/pb-functions-expression/caseV2/",
  "scraped_at": "2026-07-13T05:53:04.863061+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 计算haversine距离

> 支持于: 批处理, 流处理

计算两对经纬度点之间的haversine距离，单位为米。

**表达式类别**: 地理空间

## 声明的参数

* **点a** - 点b的经度和纬度。<br>*表达式\<GeoPoint>*
* **点b** - 点a的经度和纬度。<br>*表达式\<GeoPoint>*

**输出类型:** *Double*

## 示例

### 示例1: 基本情况

**参数值:**

* **点a**: `point_a`
* **点b**: `point_b`

| point\_a | point\_b | **输出** |
| ----- | ----- | ----- |
| {<br> **纬度**: 41.507483,<br> **经度**: -99.436554,<br>} | {<br> **纬度**: 38.504048,<br> **经度**: -98.315949,<br>} | 347328.82778977347 |
| {<br> **纬度**: 22.308919,<br> **经度**: 113.914603,<br>} | {<br> **纬度**: -33.946111,<br> **经度**: 151.177222,<br>} | 7393894.00134442 |

***
