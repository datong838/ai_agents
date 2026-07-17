---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arraysZipV1/",
  "title": "数组 zip",
  "page_id": "arraysZipV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arraysHaveIntersectionV1/",
  "next": "/zh/foundry/pb-functions-expression/base64DecodeToStringV1/",
  "scraped_at": "2026-07-13T05:52:56.851350+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组 zip

> 支持于: 批处理, 流处理

将给定数组列表压缩成一个合并的结构体数组，其中第 n 个结构体包含输入数组的所有第 n 个值。

**表达式类别**: 数组

## 声明的参数

* **表达式** - 要压缩的数组列表。<br>*List\<Expression\<Array\<AnyType>>>*

**输出类型:** *Array\<Struct>*

## 示例

### 示例 1: 基本案例

**参数值:**

* **表达式**: \[`first_array`, `second_array`]

| first\_array | second\_array | **输出** |
| ----- | ----- | ----- |
| \[ 1, 2, 3 ] | \[ 4, 5, 6 ] | \[ {<br> **first\_array**: 1,<br> **second\_array**: 4,<br>}, {<br> **first\_array**: 2,<... |

***

### 示例 2: 空值案例

**参数值:**

* **表达式**: \[`first_array`, `second_array`]

| first\_array | second\_array | **输出** |
| ----- | ----- | ----- |
| \[ 1, 2, 3 ] | *null* | \[ {<br> **first\_array**: 1,<br> **second\_array**: *null*,<br>}, {<br> **first\_array**... |
| *null* | *null* | \[  ] |
| \[  ] | \[  ] | \[  ] |

***

### 示例 3: 边缘案例

**描述**: 使用最长长度的数组。
**参数值:**

* **表达式**: \[`first_array`, `second_array`]

| first\_array | second\_array | **输出** |
| ----- | ----- | ----- |
| \[ 1, 2, 3 ] | \[ 4, 5 ] | \[ {<br> **first\_array**: 1,<br> **second\_array**: 4,<br>}, {<br> **first\_array**: 2,<... |

***
