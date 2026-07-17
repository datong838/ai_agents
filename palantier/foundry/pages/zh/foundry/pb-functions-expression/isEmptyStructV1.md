---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/isEmptyStructV1/",
  "title": "是否为空结构",
  "page_id": "isEmptyStructV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/isNaNV1/",
  "next": "/zh/foundry/pb-functions-expression/isInV1/",
  "scraped_at": "2026-07-13T05:55:50.339732+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 是否为空结构

> 支持于: 批处理

如果输入是一个空结构，则返回true，并递归检查内部数组和结构。

**表达式类别**: 布尔

## 声明的参数

* **表达式** - 计算此结构是否为空或具有非空字段。<br>*Expression\<Struct>*

**输出类型:** *布尔*

## 示例

### 示例 1: 基础案例

**参数值:**

* **表达式**: `struct`

| struct | **输出** |
| ----- | ----- |
| {<br> **airline**: {<br> **id**: *null*,<br> **name**: *null*,<br>},<br> **tail\_no**: *null*,<br>} | true |
| {<br> **airline**: {<br> **id**: NA,<br> **name**: *null*,<br>},<br> **tail\_no**: *null*,<br>} | false |

***

### 示例 2: 基础案例

**参数值:**

* **表达式**: `struct`

| struct | **输出** |
| ----- | ----- |
| {<br> **airline**: {<br> **ids**: *null*,<br> **name**: *null*,<br>},<br> **tail\_no**: *null*,<br>} | true |
| {<br> **airline**: {<br> **ids**: \[ *null* ],<br> **name**: *null*,<br>},<br> **tail\_no**: *null*,<br>} | true |
| {<br> **airline**: {<br> **ids**: \[ foo, bar ],<br> **name**: *null*,<br>},<br> **tail\_no**: *null*,<br>} | false |
| {<br> **airline**: {<br> **ids**: \[ foo, *null* ],<br> **name**: *null*,<br>},<br> **tail\_no**: *null*,<br>} | false |

***

### 示例 3: 基础案例

**参数值:**

* **表达式**: `struct`

| struct | **输出** |
| ----- | ----- |
| {<br> **airline**: {<br> **name**: *null*,<br>},<br> **ids**: *null*,<br> **tail\_no**: *null*,<br>} | true |

***

### 示例 4: 基础案例

**参数值:**

* **表达式**: `struct`

| struct | **输出** |
| ----- | ----- |
| {<br> **airline**: {<br> **ids**: {<br> foo -> *null*,<br>},<br> **name**: *null*,<br>},<br> **tail\_no**: *null*,<br>} | true |
| {<br> **airline**: {<br> **ids**: {<br> foo -> bar,<br>},<br> **name**: *null*,<br>},<br> **tail\_no**: *null*,<br>} | false |
| {<br> **airline**: {<br> **ids**: {<br> foo -> bar,<br> foo1 -> *null*,<br>},<br> **name**: *null*,<br>},<br> **tail\_no**: *null*,<br>} | false |

***

### 示例 5: 基础案例

**参数值:**

* **表达式**: `struct`

| struct | **输出** |
| ----- | ----- |
| {<br> **airline**: {<br> **ids**: \[ {<br> **airline**: {<br> **ids**: \[ *null* ]... | true |
| {<br> **airline**: {<br> **ids**: \[ {<br> **airline**: {<br> **ids**: \[ foo, bar... | false |

***
