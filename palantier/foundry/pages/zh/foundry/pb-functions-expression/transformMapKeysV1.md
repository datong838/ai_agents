---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/transformMapKeysV1/",
  "title": "变换映射键",
  "page_id": "transformMapKeysV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/transformArrayElementV1/",
  "next": "/zh/foundry/pb-functions-expression/transformMapValuesV1/",
  "scraped_at": "2026-07-13T05:57:49.689240+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 变换映射键

> 支持于: 批处理, 流处理

通过对每个键值对应用表达式来变换映射的键。

**表达式类别**: 映射

## 声明的参数

* **要应用的表达式。** - 对映射的每个键值对应用一次的表达式。<br>*Expression\<K>*
* **映射** - 映射表达式。<br>*Expression\<Map\<AnyType, V>>*

**类型变量界限:** *K 接受 AnyType\*\*V 接受 AnyType*

**输出类型:** *Map\<K, V>*

## 示例

### 示例 1: 基础案例

**参数值:**

* **要应用的表达式。**: <br>stringBeforeDelimiter(<br> delimiter: -,<br> expression: `key`,<br> ignoreCase: false,<br>)
* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| {<br> MT-111 -> 2,<br> XB-134 -> 1,<br>} | {<br> MT -> 2,<br> XB -> 1,<br>} |

***

### 示例 2: 基础案例

**参数值:**

* **要应用的表达式。**: <br>cast(<br> expression: `key`,<br> type: Integer,<br>)
* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| {<br> 11 -> 1,<br> 22 -> 2,<br>} | {<br> 11 -> 1,<br> 22 -> 2,<br>} |

***

### 示例 3: 基础案例

**参数值:**

* **要应用的表达式。**: <br>cast(<br> expression: `value`,<br> type: 字符串,<br>)
* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| {<br> 11 -> 1,<br> 22 -> 2,<br>} | {<br> 1 -> 1,<br> 2 -> 2,<br>} |

***

### 示例 4: 基础案例

**参数值:**

* **要应用的表达式。**: <br>concatStrings(<br> expressions: \[<br>stringBeforeDelimiter(<br> delimiter: -,<br> expression: `key`,<br> ignoreCase: false,<br>), `value`],<br> separator: -,<br>)
* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| {<br> MT-111 -> BB,<br> XB-134 -> AA,<br>} | {<br> MT-BB -> BB,<br> XB-AA -> AA,<br>} |

***
