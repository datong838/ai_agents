---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/standardDeviationV1/",
  "title": "标准差",
  "page_id": "standardDeviationV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/sqrtV1/",
  "next": "/zh/foundry/pb-functions-expression/startsWithV1/",
  "scraped_at": "2026-07-13T05:57:20.367291+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 标准差

> 支持于: 批处理

计算列中值的标准差。

**表达式类别**: 数值

## 声明参数

* **表达式** - 计算标准差的列。<br>*Expression\<Numeric>*

**输出类型:** *Double*

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

**输出:** 0.81649658092773

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
