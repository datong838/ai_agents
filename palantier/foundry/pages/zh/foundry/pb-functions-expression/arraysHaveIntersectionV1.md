---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arraysHaveIntersectionV1/",
  "title": "数组有交集",
  "page_id": "arraysHaveIntersectionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arrayUnionV1/",
  "next": "/zh/foundry/pb-functions-expression/arraysZipV1/",
  "scraped_at": "2026-07-13T05:52:57.920576+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组有交集

> 支持于：批处理，流处理

检查给定数组是否至少有一个共享元素。

**表达式类别**：数组，布尔

## 声明的参数

* **表达式** - 要检查的数组列表。<br>*List\<Expression\<Array\<T>>>*

**类型变量界限：** *T 接受 AnyType*

**输出类型：** *布尔*

## 示例

### 示例 1：基本情况

**参数值：**

* **表达式**: \[\[ 1, 2, 3 ], \[ 3, 4 ]]

**输出：** true

***

### 示例 2：基本情况

**参数值：**

* **表达式**: \[\[ 1, 2 ], \[ 3, 4 ]]

**输出：** false

***

### 示例 3：基本情况

**参数值：**

* **表达式**: \[\[ 1, 2, 3 ], \[ 3, 4 ], \[ 2, 3 ]]

**输出：** true

***

### 示例 4：空值情况

**参数值：**

* **表达式**: \[`first_array`, `second_array`]

| first\_array | second\_array | **输出** |
| ----- | ----- | ----- |
| \[ 1, 2, 3 ] | *null* | false |
| *null* | *null* | false |

***
