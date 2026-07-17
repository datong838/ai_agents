---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/subtractManyV1/",
  "title": "减去多个表达式",
  "page_id": "subtractManyV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/substringV1/",
  "next": "/zh/foundry/pb-functions-expression/subtractV1/",
  "scraped_at": "2026-07-13T05:57:39.246317+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 减去多个表达式

> 支持于: 批处理, 流处理

计算一个数与所有输入列之间的差值。

**表达式类别**: 数值

## 声明的参数

* **表达式列表** - 用于减法的表达式列表。<br>*List\<Expression\<Numeric>>*
* **要减去的值** - 要减去的表达式。<br>*Expression\<Numeric>*

**输出类型:** *Numeric*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式列表**: \[`col_b`, `col_c`]
* **要减去的值**: `col_a`

| col\_a | col\_b | col\_c | **输出** |
| ----- | ----- | ----- | ----- |
| 5 | 3 | 2 | 0 |
| 2 | 4 | 0 | -2 |
| -2 | -4 | -2 | 4 |

***

### 示例 2: 基本情况

**参数值:**

* **表达式列表**: \[`col_b`]
* **要减去的值**: `col_a`

| col\_a | col\_b | **输出** |
| ----- | ----- | ----- |
| *null* | *null* | *null* |
| 1 | *null* | *null* |
| *null* | 10 | *null* |

***
