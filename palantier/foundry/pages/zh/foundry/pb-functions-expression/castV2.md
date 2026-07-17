---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/castV2/",
  "title": "转换",
  "page_id": "castV2",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/caseV2/",
  "next": "/zh/foundry/pb-functions-expression/ceilV1/",
  "scraped_at": "2026-07-13T05:53:13.073078+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 转换

> 支持于: 批处理, 流处理

将表达式转换为给定类型。

**表达式类别**: 转换, 常用

## 声明参数

* **Expression** - 要转换的表达式。<br>*Expression\<AnyType>*
* **Type** - 要转换为的类型。<br>*Type\<C>*

**类型变量界限:** *C 接受 AnyType*

**输出类型:** *C*

## 示例

### 示例 1: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: Array\<String>

| a | **输出** |
| ----- | ----- |
| \[ 12.3, 20.1 ] | \[ 12.3, 20.1 ] |

***

### 示例 2: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: String

| a | **输出** |
| ----- | ----- |
| \[ {<br> **date**: 2020-01-01,<br> **foo**: false,<br> **time**: 2020-10-01T00:00:01Z,<br>} ] | \[{false, 2020-10-01 00:00:01, 2020-01-01}] |

***

### 示例 3: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: Array\<Float>

| a | **输出** |
| ----- | ----- |
| \[ 12.3, 20.1 ] | \[ 12.3, 20.1 ] |

***

### 示例 4: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: String

| a | **输出** |
| ----- | ----- |
| \[ true, false ] | \[true, false] |

***

### 示例 5: 基本情况

**描述**: 将字符串转换为长整型
**参数值:**

* **Expression**: 1234
* **Type**: Long

**输出:** 1234

***

### 示例 6: 基本情况

**描述**: 将长整型转换为字符串
**参数值:**

* **Expression**: 1234
* **Type**: String

**输出:** 1234

***

### 示例 7: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: String

| a | **输出** |
| ----- | ----- |
| true | true |
| false | false |
| *null* | *null* |

***

### 示例 8: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: Date

| a | **输出** |
| ----- | ----- |
| 2020-01-01 | 2020-01-01 |
| *null* | *null* |

***

### 示例 9: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: String

| a | **输出** |
| ----- | ----- |
| {<br> 1 -> true,<br> 2 -> false,<br>} | {1 -> true, 2 -> false} |

***

### 示例 10: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: String

| a | **输出** |
| ----- | ----- |
| \[ \[ true, false ], \[ true ] ] | \[\[true, false], \[true]] |

***

### 示例 11: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: String

| a | **输出** |
| ----- | ----- |
| {<br> foo -> {<br> 1 -> true,<br> 2 -> false,<br>},<br>} | {foo -> {1 -> true, 2 -> false}} |

***

### 示例 12: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: String

| a | **输出** |
| ----- | ----- |
| {<br> **a**: {<br> **bar**: false,<br> **foo**: 1,<br>},<br>} | {{1, false}} |

***

### 示例 13: 基本情况

**描述**: 将字符串转换为小数
**参数值:**

* **Expression**: 1234
* **Type**: Decimal(4, 0)

**输出:** 1234

***

### 示例 14: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: Integer

| a | **输出** |
| ----- | ----- |
| 1 | 1 |
| 1.0 | *null* |
| *null* | *null* |

***

### 示例 15: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: Long

| a | **输出** |
| ----- | ----- |
| 1 | 1 |
| 1.0 | *null* |
| *null* | *null* |

***

### 示例 16: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: String

| a | **输出** |
| ----- | ----- |
| {<br> **bar**: *null*,<br> **foo**: 1,<br>} | {1, null} |

***

### 示例 17: 基本情况

**参数值:**

* **Expression**: `a`
* **Type**: String

| a | **输出** |
| ----- | ----- |
| {<br> **bar**: false,<br> **foo**: 1,<br>} | {1, false} |

***

### 示例 18: 空值情况

**参数值:**

* **Expression**: `a`
* **Type**: String

| a | **输出** |
| ----- | ----- |
| \[ true, *null* ] | \[true, null] |
| *null* | *null* |

***

### 示例 19: 空值情况

**参数值:**

* **Expression**: `a`
* **Type**: String

| a | **输出** |
| ----- | ----- |
| {<br> 1 -> *null*,<br> 2 -> false,<br>} | {1 -> null, 2 -> false} |

***

### 示例 20: 空值情况

**参数值:**

* **Expression**: `a`
* **Type**: Date

| a | **输出** |
| ----- | ----- |
| *null* | *null* |

***
