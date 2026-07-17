---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arrayReverseV1/",
  "title": "数组反转",
  "page_id": "arrayReverseV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arrayRepeatV1/",
  "next": "/zh/foundry/pb-functions-expression/arraySortV1/",
  "scraped_at": "2026-07-13T05:52:55.332291+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组反转

> 支持于: 批处理, 流式处理

反转“数组”中元素的顺序。

**表达式类别**: 数组

## 声明的参数

* **表达式** - 要反转的数组。<br>*Expression\<Array\<T>>*

**类型变量界限:** *T 接受 AnyType*

**输出类型:** *Array\<T>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: \[ 1, 2, 3 ]

**输出:** \[ 3, 2, 1 ]

***

### 示例 2: 空值情况

**参数值:**

* **表达式**: `array`

| 数组 | **输出** |
| ----- | ----- |
| *null* | *null* |
| \[ 1, *null* ] | \[ *null*, 1 ] |

***
