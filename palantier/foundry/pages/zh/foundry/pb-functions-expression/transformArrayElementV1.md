---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/transformArrayElementV1/",
  "title": "变换数组元素",
  "page_id": "transformArrayElementV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/audioTranscriptionV1/",
  "next": "/zh/foundry/pb-functions-expression/transformMapKeysV1/",
  "scraped_at": "2026-07-13T05:57:51.871690+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 变换数组元素

> 支持于: 批处理，流处理

使用表达式映射数组的每个元素。注意，数组索引从1开始。

**表达式类别**: 数组

## 声明的参数

* **数组** - 包含要应用表达式的元素的输入数组。<br>*Expression\<Array\<AnyType>>*
* **要应用的表达式。** - 对数组的每个元素应用一次的表达式。<br>*Expression\<T>*

**类型变量边界:** *T 接受 AnyType*

**输出类型:** *Array\<T>*

## 示例

### 示例 1: 基本案例

**参数值:**

* **数组**: `flight_number`
* **要应用的表达式。**: <br>stringBeforeDelimiter(<br> delimiter: -,<br> expression: `element`,<br> ignoreCase: false,<br>)

| flight\_number | **输出** |
| ----- | ----- |
| \[ XB-134, MT-111 ] | \[ XB, MT ] |

***

### 示例 2: 基本案例

**参数值:**

* **数组**: `miles`
* **要应用的表达式。**: <br>add(<br> expressions: \[`previous_miles`, `element`],<br>)

| miles | previous\_miles | **输出** |
| ----- | ----- | ----- |
| \[ 12300, 12342 ] | 10000 | \[ 22300, 22342 ] |

***

### 示例 3: 基本案例

**描述**: 将索引添加到数组元素。注意索引从1开始。
**参数值:**

* **数组**: `array`
* **要应用的表达式。**: <br>add(<br> expressions: \[`elementIndex`, `element`],<br>)

| array | **输出** |
| ----- | ----- |
| \[ 1, 1, 1 ] | \[ 2, 3, 4 ] |

***

### 示例 4: 基本案例

**参数值:**

* **数组**: `miles`
* **要应用的表达式。**: <br>cast(<br> expression: `element`,<br> type: 字符串,<br>)

| miles | **输出** |
| ----- | ----- |
| \[ 12300, 12342 ] | \[ 12300, 12342 ] |

***

### 示例 5: 基本案例

**描述**: 从结构数组中获取结构元素。
**参数值:**

* **数组**: `raw_data`
* **要应用的表达式。**: <br>getStructField(<br> locator: miles,<br> struct: `element`,<br>)

| raw\_data | **输出** |
| ----- | ----- |
| \[ {<br> **miles**: 22300,<br> **tail\_number**: XB-112,<br>}, {<br> **miles**: 22342,<br> **tail\_number**: XB-112,<br>} ] | \[ 22300, 22342 ] |

***

### 示例 6: 基本案例

**描述**: 从结构数组中获取结构元素。
**参数值:**

* **数组**: `raw_data`
* **要应用的表达式。**: <br>transformMapKeys(<br> expression: <br>uppercase(<br> expression: `key`,<br>),<br> map: `element`,<br>)

| raw\_data | **输出** |
| ----- | ----- |
| \[ {<br> miles -> 22300,<br> tail\_number -> XB-112,<br>}, {<br> miles -> 22342L,<br> tail\_number -> XB-112,<br>} ] | \[ {<br> MILES -> 22300,<br> TAIL\_NUMBER -> XB-112,<br>}, {<br> MILES -> 22342L,<br> TAIL\_NUMBER -> XB-112,<br>} ] |

***
