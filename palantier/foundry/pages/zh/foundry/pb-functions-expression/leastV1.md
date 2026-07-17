---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/leastV1/",
  "title": "Least",
  "page_id": "leastV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/leadV1/",
  "next": "/zh/foundry/pb-functions-expression/leftStringV1/",
  "scraped_at": "2026-07-13T05:56:14.805772+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Least

> 支持于: 批处理, 流处理

计算所有输入列中最小的值，跳过空值。

**表达式类别**: 布尔, 数字

## 声明的参数

* **表达式** - *无描述*<br>*List\<Expression\<T>>*

**类型变量界限:** *T 接受 ComparableType*

**输出类型:** *T*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: \[`a`, `b`, `c`]

| a | b | c | **输出** |
| ----- | ----- | ----- | ----- |
| 1 | 2 | 3 | 1 |
| 1 | 3 | 2 | 1 |
| 3 | 2 | 1 | 1 |

***

### 示例 2: 空值情况

**描述**: 如果所有输入的值都是空，则返回空。
**参数值:**

* **表达式**: \[`a`, `b`]

| a | b | **输出** |
| ----- | ----- | ----- |
| *null* | *null* | *null* |

***

### 示例 3: 空值情况

**描述**: 任何空值在比较时都会被忽略。
**参数值:**

* **表达式**: \[`a`, `b`]

| a | b | **输出** |
| ----- | ----- | ----- |
| *null* | -2147483648 | -2147483648 |
| *null* | 0 | 0 |
| *null* | 2147483647 | 2147483647 |

***
