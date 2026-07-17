---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/sampleCovarianceV1/",
  "title": "样本协方差",
  "page_id": "sampleCovarianceV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/rowNumberV1/",
  "next": "/zh/foundry/pb-functions-expression/sampleVarianceV1/",
  "scraped_at": "2026-07-13T05:57:11.887067+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 样本协方差

> 支持于: 批处理, 流处理

计算两列中的值的样本协方差。

**表达式类别**: 聚合

## 声明参数

* **左侧** - 我们计算协方差的第一列。<br>*Expression\<Numeric>*
* **右侧** - 我们计算协方差的第二列。<br>*Expression\<Numeric>*

**输出类型:** *Double*

## 示例

### 示例 1: 基本案例

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

**输出:** -2.5

***

### 示例 2: 空值案例

**参数值:**

* **左侧**: `left`
* **右侧**: `right`

**给定输入表:**

| left | right |
| ----- | ----- |
| 1.0 | 2.0 |
| *null* | *null* |
| 2.0 | 1.0 |

**输出:** -0.5

***
