---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arraysCartesianProductV1/",
  "title": "数组笛卡尔积",
  "page_id": "arraysCartesianProductV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arrayAddV1/",
  "next": "/zh/foundry/pb-functions-expression/arrayConcatV1/",
  "scraped_at": "2026-07-13T05:52:29.221370+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组笛卡尔积

> 支持于: 批处理, 流处理

计算数组的笛卡尔积。

**表达式类别**: 数组

## 声明的参数

* **表达式** - 要转换的列。<br>*List\<Expression\<Array\<AnyType>>>*

**输出类型:** *Array\<Struct>*

## 示例

### 示例 1: 基本案例

**参数值:**

* **表达式**: \[`first`, `second`]

| first | second | **输出** |
| ----- | ----- | ----- |
| \[ \[ {<br> **s1**: 1,<br>}, {<br> **s1**: 2,<br>} ], \[ {<br> **s1**: 3,<br>} ] ] | \[ \[ {<br> **s2**: 4,<br>}, {<br> **s2**: 5,<br>} ], \[ {<br> **s2**: 6,<br>} ] ] | \[ {<br> **first**: \[ {<br> **s1**: 1,<br>}, {<br> **s1**: 2,<br>} ],<br> **second**: ... |

***

### 示例 2: 基本案例

**参数值:**

* **表达式**: \[`first`, `second`]

| first | second | **输出** |
| ----- | ----- | ----- |
| \[ 1, 2 ] | \[ 3, 4 ] | \[ {<br> **first**: 1,<br> **second**: 3,<br>}, {<br> **first**: 1,<br> **second**: ... |

***

### 示例 3: 基本案例

**参数值:**

* **表达式**: \[`first`, `second`, `third`]

| first | second | third | **输出** |
| ----- | ----- | ----- | ----- |
| \[ 1, 2 ] | \[ word, a ] | \[ {<br> **s1**: 1,<br>}, {<br> **s1**: 2,<br>} ] | \[ {<br> **first**: 1,<br> **second**: word,<br> **third**: {<br> **s1**: 1,<br>}... |

***

### 示例 4: 空值案例

**参数值:**

* **表达式**: \[`first`, `second`]

| first | second | **输出** |
| ----- | ----- | ----- |
| \[ 1, *null* ] | \[ *null*, 4 ] | \[ {<br> **first**: 1,<br> **second**: *null*,<br>}, {<br> **first**: 1,<br> **second**: ... |
| \[ 1, 2 ] | *null* | \[  ] |
| \[  ] | \[  ] | \[  ] |
| *null* | *null* | \[  ] |

***
