---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arrayDifferenceV1/",
  "title": "数组差异",
  "page_id": "arrayDifferenceV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arrayContainsNullV1/",
  "next": "/zh/foundry/pb-functions-expression/arrayDistinctV1/",
  "scraped_at": "2026-07-13T05:52:45.641318+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组差异

> 支持于: 批处理，流处理

返回`left`数组中所有不在`right`数组中的唯一元素。

**表达式类别**: 数组

## 声明的参数

* **Left array** - *无描述*<br>*Expression\<Array\<T>>*
* **Right array** - *无描述*<br>*Expression\<Array\<T>>*

**类型变量界限:** *T 接受 AnyType*

**输出类型:** *Array\<T>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **Left array**: \[ 1, 2, 3 ]
* **Right array**: \[ 2, 3, 4 ]

**输出:** \[ 1 ]

***

### 示例 2: 空值情况

**参数值:**

* **Left array**: `first_array`
* **Right array**: `second_array`

| first\_array | second\_array | **输出** |
| ----- | ----- | ----- |
| \[ 1, 2, 3 ] | *null* | \[ 1, 2, 3 ] |
| *null* | \[ 1, 2, 3 ] | *null* |
| *null* | *null* | *null* |

***

### 示例 3: 边缘情况

**描述**: 左数组中的重复项将被移除。
**参数值:**

* **Left array**: \[ 1, 1, 2, 3 ]
* **Right array**: \[ 2, 3, 4 ]

**输出:** \[ 1 ]

***
