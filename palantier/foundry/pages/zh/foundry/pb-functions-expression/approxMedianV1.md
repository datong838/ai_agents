---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/approxMedianV1/",
  "title": "近似中位数",
  "page_id": "approxMedianV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/anyOfV1/",
  "next": "/zh/foundry/pb-functions-expression/approximatePercentileV1/",
  "scraped_at": "2026-07-13T05:52:17.636680+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 近似中位数

> 支持于: 批处理

计算列中值的近似中位数。

**表达式类别**: 聚合

## 声明的参数

* **表达式** - 要计算近似中位数的列。<br>*表达式<数字>*

**输出类型:** *数字*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `values`

**给定输入表:**

| values |
| ----- |
| 2 |
| 4 |
| 3 |

**输出:** 3

***

### 示例 2: 空值情况

**参数值:**

* **表达式**: `values`

**给定输入表:**

| values |
| ----- |
| 2 |
| 3 |
| 4 |
| *null* |

**输出:** 3

***
