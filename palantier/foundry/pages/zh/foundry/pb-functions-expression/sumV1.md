---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/sumV1/",
  "title": "求和",
  "page_id": "sumV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/dateSubV2/",
  "next": "/zh/foundry/pb-functions-expression/arraySumV1/",
  "scraped_at": "2026-07-13T05:57:30.722470+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 求和

> 支持于：批处理，流处理

对指定表达式进行求和。

**表达式类别**：数值

## 声明的参数

* **表达式** - 要求和的列。<br>*Expression\<Numeric>*

**输出类型：** *Decimal | Double | Long*

## 示例

### 示例 1: 基本情况

**参数值：**

* **表达式**: `values`

**给定输入表：**

| values |
| ----- |
| 2 |
| 4 |
| 3 |

**输出：** 9

***

### 示例 2: 空值情况

**参数值：**

* **表达式**: `values`

**给定输入表：**

| values |
| ----- |
| 2 |
| *null* |
| 3 |

**输出：** 5

***
