---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arraySortV1/",
  "title": "数组排序",
  "page_id": "arraySortV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arrayReverseV1/",
  "next": "/zh/foundry/pb-functions-expression/arrayUnionV1/",
  "scraped_at": "2026-07-13T05:52:57.006740+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组排序

> 支持于: 批处理, 流处理

返回给定输入数组的排序后的数组。所有空值在降序数组的末尾和升序数组的开头。

**表达式类别**: 数组

## 声明的参数

* **方向** - 选择排序方向。<br>*枚举<升序, 降序>*
* **表达式** - 要排序的数组。<br>*表达式<数组\<T>>*

**类型变量边界:** *T 接受 ComparableType*

**输出类型:** *数组\<T>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **方向**: `ASCENDING`
* **表达式**: \[ 5, 3, 6 ]

**输出:** \[ 3, 5, 6 ]

***

### 示例 2: 基本情况

**参数值:**

* **方向**: `DESCENDING`
* **表达式**: \[ 5, 3, 6 ]

**输出:** \[ 6, 5, 3 ]

***

### 示例 3: 基本情况

**参数值:**

* **方向**: `ASCENDING`
* **表达式**: \[ 3, *null*, 1, 2 ]

**输出:** \[ *null*, 1, 2, 3 ]

***

### 示例 4: 基本情况

**参数值:**

* **方向**: `DESCENDING`
* **表达式**: \[ 3, *null*, 1, 2 ]

**输出:** \[ 3, 2, 1, *null* ]

***

### 示例 5: 空情况

**参数值:**

* **方向**: `ASCENDING`
* **表达式**: `array`

| array | **输出** |
| ----- | ----- |
| *null* | *null* |
