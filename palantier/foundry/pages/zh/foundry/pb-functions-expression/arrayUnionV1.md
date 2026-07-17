---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arrayUnionV1/",
  "title": "数组合并",
  "page_id": "arrayUnionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arraySortV1/",
  "next": "/zh/foundry/pb-functions-expression/arraysHaveIntersectionV1/",
  "scraped_at": "2026-07-13T05:52:55.074412+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组合并

> 支持于: 批处理, 流处理

移除重复项并合并数组列表。

**表达式类别**: 数组

## 声明的参数

* **表达式** - 要合并的数组列表。<br>*List\<Expression\<Array\<T>>>*

**类型变量界限:** *T 接受任意类型*

**输出类型:** *Array\<T>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: \[\[ 1, 2, 3 ], \[ 3, 4 ]]

**输出:** \[ 1, 2, 3, 4 ]

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: \[\[ 1, 2, 3 ], \[ 3, 4 ], \[ 4, 5 ]]

**输出:** \[ 1, 2, 3, 4, 5 ]

***

### 示例 3: 基本情况

**描述**: 移除重复项。
**参数值:**

* **表达式**: \[\[ 1, 1 ], \[ 1 ]]

**输出:** \[ 1 ]

***

### 示例 4: 空值情况

**参数值:**

* **表达式**: \[`first_array`, `second_array`]

| first\_array | second\_array | **输出** |
| ----- | ----- | ----- |
| \[ 1, 2, 3 ] | *null* | \[ 1, 2, 3 ] |
| *null* | *null* | \[  ] |

***
