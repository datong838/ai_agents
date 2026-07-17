---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/transformMapValuesV1/",
  "title": "变换映射值",
  "page_id": "transformMapValuesV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/transformMapKeysV1/",
  "next": "/zh/foundry/pb-functions-expression/trimV1/",
  "scraped_at": "2026-07-13T05:57:53.361923+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 变换映射值

> 支持于: 批处理

通过对每个键值对应用表达式来变换映射的值。

**表达式类别**: 映射

## 声明的参数

* **要应用的表达式。** - 对映射的每个键值对应用一次的表达式。<br>*Expression\<V>*
* **映射** - 映射表达式。<br>*Expression\<Map\<K, AnyType>>*

**类型变量界限：** *K 接受 AnyType\*\*V 接受 AnyType*

**输出类型：** *Map\<K, V>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **要应用的表达式。**: <br>stringBeforeDelimiter(<br> delimiter: -,<br> expression: `value`,<br> ignoreCase: false,<br>)
* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| {<br> 1 -> XB-134,<br> 2 -> MT-111,<br>} | {<br> 1 -> XB,<br> 2 -> MT,<br>} |

***

### 示例 2: 基本情况

**参数值:**

* **要应用的表达式。**: <br>cast(<br> expression: `value`,<br> type: Integer,<br>)
* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| {<br> 1 -> 11,<br> 2 -> 22,<br>} | {<br> 1 -> 11,<br> 2 -> 22,<br>} |

***

### 示例 3: 基本情况

**参数值:**

* **要应用的表达式。**: <br>cast(<br> expression: `key`,<br> type: 字符串,<br>)
* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| {<br> 1 -> 11,<br> 2 -> 22,<br>} | {<br> 1 -> 1,<br> 2 -> 2,<br>} |

***

### 示例 4: 基本情况

**参数值:**

* **要应用的表达式。**: <br>concatStrings(<br> expressions: \[<br>stringBeforeDelimiter(<br> delimiter: -,<br> expression: `key`,<br> ignoreCase: false,<br>), `value`],<br> separator: -,<br>)
* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| {<br> MT-111 -> BB,<br> XB-134 -> AA,<br>} | {<br> MT-111 -> MT-BB,<br> XB-134 -> XB-AA,<br>} |

***
