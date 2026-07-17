---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/covarianceV1/",
  "title": "协方差",
  "page_id": "covarianceV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/cosineV1/",
  "next": "/zh/foundry/pb-functions-expression/createGeoPointFromCoordinateSystemV1/",
  "scraped_at": "2026-07-13T05:54:03.054467+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 协方差

> 支持于: 批处理, 流处理

计算两列值的总体协方差。

**表达式类别**: 聚合

## 声明的参数

* **左侧** - 计算协方差的第一列。<br>*表达式<数值>*
* **右侧** - 计算协方差的第二列。<br>*表达式<数值>*

**输出类型:** *双精度*

## 示例

### 示例 1: 基本情况

**参数值:**

* **左侧**: `left`
* **右侧**: `right`

**给定输入表:**

| left | right |
| ----- | ----- |
| 1 | 5 |
| 2 | 4 |
| 3 | 3 |
| 4 | 2 |
| 5 | 1 |

**输出:** -2.0

***

### 示例 2: 空值情况

**参数值:**

* **左侧**: `left`
* **右侧**: `right`

**给定输入表:**

| left | right |
| ----- | ----- |
| 1.0 | 2.0 |
| *null* | *null* |
| 2.0 | 1.0 |

**输出:** -0.25

***
