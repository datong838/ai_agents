---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/distinctCountV1/",
  "title": "唯一计数",
  "page_id": "distinctCountV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/denseRankV1/",
  "next": "/zh/foundry/pb-functions-expression/divideV1/",
  "scraped_at": "2026-07-13T05:54:19.084679+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 唯一计数

> 支持于：批处理，流处理

计算列中唯一值的数量。

**表达式类别**：聚合

## 声明的参数

* **表达式** - 计算唯一计数的列。<br>*Expression\<AnyType>*

**输出类型：** *Long*

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

**输出：** 3

***

### 示例 2: 空值情况

**参数值：**

* **表达式**: `values`

**给定输入表：**

| values |
| ----- |
| 2 |
| 2 |
| *null* |

**输出：** 1

***
