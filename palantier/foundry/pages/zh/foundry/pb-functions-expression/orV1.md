---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/orV1/",
  "title": "或",
  "page_id": "orV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/nullifyEmptyStringV1/",
  "next": "/zh/foundry/pb-functions-expression/pdfTableOfContentsV1/",
  "scraped_at": "2026-07-13T05:56:37.958498+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 或

> 支持于: 批处理, 流处理

如果任何指定条件为true，则返回true。空值被视为false。

**表达式类别**: 布尔

## 声明的参数

* **条件** - 用于计算输出的条件列表。<br>*List\<Expression\<Boolean>>*

**输出类型:** *Boolean*

## 示例

### 示例 1: 基本情况

**参数值:**

* **条件**: \[`left_boolean`, `right_boolean`]

| left\_boolean | right\_boolean | **输出** |
| ----- | ----- | ----- |
| true | true | true |
| true | false | true |
| false | true | true |
| false | false | false |

***

### 示例 2: 空值情况

**参数值:**

* **条件**: \[*null*, true]

**输出:** true

***
