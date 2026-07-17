---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/allArrayElementsSatisfyV1/",
  "title": "所有数组元素满足",
  "page_id": "allArrayElementsSatisfyV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/dateAddV2/",
  "next": "/zh/foundry/pb-functions-expression/allOfV1/",
  "scraped_at": "2026-07-13T05:52:08.951495+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 所有数组元素满足

> 支持于: 批处理，流处理

如果表达式对数组中的所有元素都为true，则返回true。

**表达式类别**: 数组

## 声明参数

* **数组** - 数组表达式。<br>*Expression\<Array\<AnyType>>*
* **布尔条件** - 每个数组元素应用一次的表达式。<br>*Expression\<Boolean>*

**输出类型:** *Boolean*

## 示例

### 示例 1: 基本情况

**参数值:**

* **数组**: `miles`
* **布尔条件**: <br>lessThan(<br> left: `element`,<br> right: `base_line`,<br>)

| miles | base\_line | **输出** |
| ----- | ----- | ----- |
| \[ 12300, 10150 ] | 20000 | true |

***

### 示例 2: 基本情况

**参数值:**

* **数组**: `miles`
* **布尔条件**: <br>isNull(<br> expression: `element`,<br>)

| miles | **输出** |
| ----- | ----- |
| \[ 12300, *null* ] | false |
| \[ *null*, *null* ] | true |

***

### 示例 3: 基本情况

**参数值:**

* **数组**: `boolean_array`
* **布尔条件**: `element`

| boolean\_array | **输出** |
| ----- | ----- |
| \[ true, false ] | false |
| \[ false, false ] | false |
| \[ true, true ] | true |

***

### 示例 4: 空值情况

**描述**: 空数组将返回空输出。
**参数值:**

* **数组**: `miles`
* **布尔条件**: <br>isNull(<br> expression: `element`,<br>)

| miles | **输出** |
| ----- | ----- |
| *null* | *null* |

***
