---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/modeV1/",
  "title": "模式",
  "page_id": "modeV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/minV1/",
  "next": "/zh/foundry/pb-functions-expression/moduloV1/",
  "scraped_at": "2026-07-13T05:56:30.281749+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 模式

> 支持于: 批处理

计算列中值的众数。

**表达式类别**: 聚合

## 声明的参数

* **表达式** - 计算众数的列。<br>*Expression<字符串>*

**类型变量界限:** *字符串接受字符串*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `values`

**给定输入表:**

| values |
| ----- |
| a |
| b |
| b |
| b |
| c |
| c |
| d |

**输出:** b

***

### 示例 2: 空情况

**参数值:**

* **表达式**: `values`

**给定输入表:**

| values |
| ----- |

**输出:** *null*

***

### 示例 3: 空情况

**参数值:**

* **表达式**: `values`

**给定输入表:**

| values |
| ----- |
| a |
| *null* |
| *null* |
| *null* |
| c |
| c |
| d |

**输出:** c

***
