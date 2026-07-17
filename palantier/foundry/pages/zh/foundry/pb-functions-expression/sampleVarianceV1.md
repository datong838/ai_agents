---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/sampleVarianceV1/",
  "title": "样本方差",
  "page_id": "sampleVarianceV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/sampleCovarianceV1/",
  "next": "/zh/foundry/pb-functions-expression/secantV1/",
  "scraped_at": "2026-07-13T05:57:18.219839+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 样本方差

> 支持于: 批处理, 流处理

计算列中值的样本方差。

**表达式类别**: 聚合

## 声明的参数

* **表达式** - 计算此表达式的样本方差。<br>*表达式<数字>*

**输出类型:** *双精度*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `values`

**给定输入表:**

| values |
| ----- |
| 2 |
| 2 |
| 3 |

**输出:** 0.33333333333

***

### 示例 2: 空值情况

**参数值:**

* **表达式**: `values`

**给定输入表:**

| values |
| ----- |
| 2 |
| *null* |
| 3 |

**输出:** 0.5

***
