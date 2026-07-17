---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/bitShiftRightV1/",
  "title": "位移右移",
  "page_id": "bitShiftRightV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/bitShiftLeftV1/",
  "next": "/zh/foundry/pb-functions-expression/h3BufferV1/",
  "scraped_at": "2026-07-13T05:53:02.912071+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 位移右移

> 支持于: 批处理, 流处理

将给定值右移若干位。

**表达式类别**: 二进制

## 声明的参数

* **表达式** - 要右移的值。<br>*Expression\<E>*
* **位数** - 右移的位数。<br>*Literal\<Integer>*

**类型变量界限:** *E 接受 Byte | Integer | Long | Short*

**输出类型:** *E*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: 1
* **位数**: 1

**输出:** 0

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: 12345678910
* **位数**: 5

**输出:** 385802465

***

### 示例 3: 空值情况

**参数值:**

* **表达式**: `number`
* **位数**: 1

| number | **输出** |
| ----- | ----- |
| *null* | *null* |

***

### 示例 4: 边缘情况

**参数值:**

* **表达式**: 2147483647
* **位数**: 100

**输出:** 134217727

***

### 示例 5: 边缘情况

**参数值:**

* **表达式**: -2147483648
* **位数**: 10

**输出:** -2097152

***

### 示例 6: 边缘情况

**参数值:**

* **表达式**: 1
* **位数**: -10

**输出:** 0

***
