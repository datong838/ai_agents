---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arraySumV1/",
  "title": "数组元素之和",
  "page_id": "arraySumV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/sumV1/",
  "next": "/zh/foundry/pb-functions-expression/tangentV1/",
  "scraped_at": "2026-07-13T05:57:40.321346+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组元素之和

> 支持于: 批处理, 流处理

对数组中的元素求和。

**表达式类别**: 数组

## 声明的参数

* **表达式** - 要求和的数值类型数组。<br>*Expression\<Array\<T>>*
* *非必填* **将null视为零。** - 如果为true，数组中的null被视为零，包含null的数组可以求和。如果为false，存在null会使整个数组为null。<br>*Literal\<Boolean>*

**类型变量界限:** *T 接受 DefiniteNumeric*

**输出类型:** *T*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: \[ 1, 2, 3 ]
* **将null视为零。**: true

**输出:** 6

***

### 示例 2: Null情况

**参数值:**

* **表达式**: \[ 1, 2, 3, *null* ]
* **将null视为零。**: false

**输出:** *null*

***

### 示例 3: Null情况

**参数值:**

* **表达式**: \[ 1, 2, 3, *null* ]
* **将null视为零。**: true

**输出:** 6

***

### 示例 4: Null情况

**参数值:**

* **表达式**: `array`
* **将null视为零。**: true

| array | **输出** |
| ----- | ----- |
| *null* | *null* |
