---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/rowCountV1/",
  "title": "行计数",
  "page_id": "rowCountV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/roundV1/",
  "next": "/zh/foundry/pb-functions-expression/rowNumberV1/",
  "scraped_at": "2026-07-13T05:57:09.878529+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 行计数

> 支持于: 批处理, 流式处理

计算组中非空行的数量。

**表达式类别**: 聚合

## 声明的参数

* *非必填* **表达式** - *无描述*<br>*Expression\<AnyType>*

**输出类型:** *Long*

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
| *null* |
| 3 |

**输出:** 2

***
