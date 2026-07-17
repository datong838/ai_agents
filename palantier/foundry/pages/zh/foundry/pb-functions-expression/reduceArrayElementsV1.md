---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/reduceArrayElementsV1/",
  "title": "缩减数组元素",
  "page_id": "reduceArrayElementsV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/rankV1/",
  "next": "/zh/foundry/pb-functions-expression/regexExtractV1/",
  "scraped_at": "2026-07-13T05:57:12.241725+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 缩减数组元素

> 支持于: 批处理, 流式处理

使用表达式缩减数组元素。

**表达式类别**: 数组

## 声明的参数

* **数组** - 要缩减的数组。<br>*Expression\<Array\<Array\<Boolean | Byte | Date | Double | Float | Integer | Long | Map\<AnyType, AnyType> | Short | 字符串 | Timestamp> | Boolean | Byte | Date | Double | Float | Integer | Long | Map\<AnyType, AnyType> | Short | 字符串 | Timestamp>>*
* **缩减的表达式** - 每个数组元素应用一次的表达式。<br>*Expression\<T>*
* **初始值** - 用于初始化累加器的起始值，如果数组长度为0，则返回此值。<br>*Expression\<T>*

**类型变量界限:** *T 接受 Array\<Boolean | Byte | Date | Double | Float | Integer | Long | Map\<AnyType, AnyType> | Short | 字符串 | Timestamp> | Boolean | Byte | Date | Double | Float | Integer | Long | Map\<AnyType, AnyType> | Short | 字符串 | Timestamp*

**输出类型:** *T*

## 示例

### 示例 1: 基本案例

**参数值:**

* **数组**: `miles`
* **缩减的表达式**: <br>add(<br> expressions: \[`accumulator`, `element`],<br>)
* **初始值**: 0

| miles | **输出** |
| ----- | ----- |
| \[ 12300, 12342 ] | 24642 |

***

### 示例 2: 基本案例

**描述**: 返回数组中第一个非空元素。
**参数值:**

* **数组**: `miles`
* **缩减的表达式**: <br>firstNonNull(<br> expressions: \[`accumulator`, `element`],<br>)
* **初始值**: `init`

| miles | init | **输出** |
| ----- | ----- | ----- |
| \[ *null*, *null*, 12300, 12111 ] | *null* | 12300 |

***

### 示例 3: 基本案例

**参数值:**

* **数组**: `miles`
* **缩减的表达式**: <br>concatStrings(<br> expressions: \[`accumulator`, <br>cast(<br> expression: `element`,<br> type: 字符串,<br>)],<br> separator: -,<br>)
* **初始值**: *空字符串*

| miles | **输出** |
| ----- | ----- |
| \[ 12300, 12342 ] | -12300-12342 |

***

### 示例 4: 空案例

**描述**: 空数组将返回空输出。
**参数值:**

* **数组**: `miles`
* **缩减的表达式**: <br>firstNonNull(<br> expressions: \[`accumulator`, `element`],<br>)
* **初始值**: `init`

| miles | init | **输出** |
| ----- | ----- | ----- |
| *null* | *null* | *null* |

***

### 示例 5: 边缘案例

**描述**: 空数组将返回初始值。
**参数值:**

* **数组**: `miles`
* **缩减的表达式**: <br>add(<br> expressions: \[`accumulator`, `element`],<br>)
* **初始值**: 0

| miles | **输出** |
| ----- | ----- |
| \[  ] | 0 |

***
