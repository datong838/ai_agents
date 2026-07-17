---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arrayIntersectV1/",
  "title": "数组交集",
  "page_id": "arrayIntersectV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arrayFlattenV2/",
  "next": "/zh/foundry/pb-functions-expression/arrayMaxV1/",
  "scraped_at": "2026-07-13T05:52:52.972506+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组交集

> 支持于: 批处理，流处理

移除重复项并对多个数组进行交集运算。

**表达式类别**: 数组

## 声明参数

* **表达式** - 要进行交集运算的数组列表。<br>*List\<Expression\<Array\<T>>>*

**类型变量界限:** *T 接受 AnyType*

**输出类型:** *Array\<T>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: \[\[ 1, 2, 3 ], \[ 3, 4 ]]

**输出:** \[ 3 ]

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: \[\[ 1, 2, 3 ], \[ 3, 4 ], \[ 2, 3 ]]

**输出:** \[ 3 ]

***

### 示例 3: 基本情况

**描述**: 移除了重复项。
**参数值:**

* **表达式**: \[\[ 1, 1 ], \[ 1 ]]

**输出:** \[ 1 ]

***

### 示例 4: 空值情况

**参数值:**

* **表达式**: \[`first_array`, `second_array`]

| first\_array | second\_array | **输出** |
| ----- | ----- | ----- |
| \[ 1, 2, 3 ] | *null* | \[  ] |
| *null* | *null* | \[  ] |

***
