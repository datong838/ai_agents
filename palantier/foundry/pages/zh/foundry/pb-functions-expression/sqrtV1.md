---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/sqrtV1/",
  "title": "平方根",
  "page_id": "sqrtV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/splitStringV2/",
  "next": "/zh/foundry/pb-functions-expression/standardDeviationV1/",
  "scraped_at": "2026-07-13T05:57:24.811530+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 平方根

> 支持于：批处理，流处理

计算列的平方根。

**表达式类别**：数值

## 声明的参数

* **表达式** - *无描述*<br>*Expression\<Numeric>*

**输出类型:** *Double*

## 示例

### 示例 1：基本情况

**参数值:**

* **表达式**: 9.0

**输出:** 3.0

***

### 示例 2：基本情况

**参数值:**

* **表达式**: 16.3216

**输出:** 4.04

***

### 示例 3：空值情况

**参数值:**

* **表达式**: `value`

| value | **输出** |
| ----- | ----- |
| *null* | *null* |

***
