---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/constructGeoPointV1/",
  "title": "构建 GeoPoint 列",
  "page_id": "constructGeoPointV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/concatStringsV1/",
  "next": "/zh/foundry/pb-functions-expression/constructDelegatedMediaGidV1/",
  "scraped_at": "2026-07-13T05:53:25.906239+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 构建 GeoPoint 列

> 支持于: 批处理, 流处理

从纬度和经度列构建 GeoPoint 列。验证纬度参数是否在-90和90之间（包括边界），以及经度参数是否在-180和180之间（包括边界）；如果不在范围内，则返回空值。

**表达式类别**: 地理空间

## 声明的参数

* **纬度** - 纬度列。<br>*Expression\<Double>*
* **经度** - 经度列。<br>*Expression\<Double>*

**输出类型:** *GeoPoint*

## 示例

### 示例 1: 基本情况

**参数值:**

* **纬度**: `lat`
* **经度**: `lon`

| lat | lon | **输出** |
| ----- | ----- | ----- |
| 32.0 | 58.0 | {<br> latitude -> 32.0,<br> longitude -> 58.0,<br>} |
| 320.0 | 58.0 | *null* |

***
