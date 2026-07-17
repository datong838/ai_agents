---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/linearRegressionGradientV1/",
  "title": "线性回归梯度",
  "page_id": "linearRegressionGradientV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/levenshteinDistanceV1/",
  "next": "/zh/foundry/pb-functions-expression/logV1/",
  "scraped_at": "2026-07-13T05:56:20.388206+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 线性回归梯度

> 支持于: 批处理

计算右侧（输出变量）和左侧（输入变量）的线性回归梯度。

**表达式类别**: 聚合

## 声明的参数

* **Left** - 独立/输入变量。<br>*Expression\<Numeric>*
* **Right** - 依赖/输出变量。<br>*Expression\<Numeric>*

**输出类型:** *Double*

## 示例

### 示例 1: 基本情况

**参数值:**

* **Left**: `left`
* **Right**: `right`

**给定输入表:**

| left | right |
| ----- | ----- |
| 1 | 5 |
| 2 | 4 |
| 3 | 3 |
| 4 | 2 |
| 5 | 1 |

**输出:** -1.0

***

### 示例 2: 基本情况

**参数值:**

* **Left**: `left`
* **Right**: `right`

**给定输入表:**

| left | right |
| ----- | ----- |
| 9.0 | 2.0 |
| 27.0 | 2.0 |
| 34.0 | 2.0 |
| 14.0 | 2.0 |
| 51.0 | 2.0 |

**输出:** 0.0

***

### 示例 3: 基本情况

**参数值:**

* **Left**: `left`
* **Right**: `right`

**给定输入表:**

| left | right |
| ----- | ----- |
| 9.0 | 8.0 |
| 9.0 | 2.0 |
| 9.0 | 1.0 |
| 9.0 | 3.0 |
| 9.0 | 2.0 |

**输出:** NaN

***

### 示例 4: 空值情况

**参数值:**

* **Left**: `left`
* **Right**: `right`

**给定输入表:**

| left | right |
| ----- | ----- |
| 1.0 | 2.0 |
| *null* | *null* |
| 2.0 | 1.0 |

**输出:** -1.0

***
