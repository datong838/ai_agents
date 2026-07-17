---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arrayPositionV1/",
  "title": "数组位置",
  "page_id": "arrayPositionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arrayMinV1/",
  "next": "/zh/foundry/pb-functions-expression/arrayRemoveV1/",
  "scraped_at": "2026-07-13T05:52:46.880037+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组位置

> 支持于: 批处理, 流处理

返回给定数组中首次出现的 'value' 的位置/索引。当未找到值或任何参数为 `null` 时返回 `null`。

**表达式类别**: 数组

## 声明的参数

* **数组** - 要从中返回元素位置的数组。<br>*Expression\<Array\<T>>*
* **值** - 要在数组中查找位置的值。<br>*Expression\<T>*

**类型变量界限:** *T 接受 AnyType*

**输出类型:** *Long*

## 示例

### 示例 1: 基本情况

**参数值:**

* **数组**: \[ 10, 11, 12 ]
* **值**: 10

**输出:** 1

***

### 示例 2: Null情况

**描述**: 如果未找到元素则输出null。
**参数值:**

* **数组**: \[ 1, 2, 4 ]
* **值**: 10

**输出:** *null*

***

### 示例 3: Null情况

**参数值:**

* **数组**: `array`
* **值**: `value`

| array | value | **输出** |
| ----- | ----- | ----- |
| \[ 1, 2, 3 ] | *null* | *null* |
| *null* | 1 | *null* |
| *null* | *null* | *null* |

***
