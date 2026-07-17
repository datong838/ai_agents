---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/sentenceCaseV1/",
  "title": "句子大小写",
  "page_id": "sentenceCaseV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/secantV1/",
  "next": "/zh/foundry/pb-functions-expression/sequenceV2/",
  "scraped_at": "2026-07-13T05:57:28.896567+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 句子大小写

> 支持于: 批处理, 流处理

将第一个单词的第一个字符转换为大写。

**表达式类别**: 字符串

## 声明的参数

* **表达式** - 要应用句子大小写的字符串表达式。<br>*表达式<字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: hello world

**输出:** Hello world

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: this is a test. another test? yes, another test!

**输出:** This is a test. Another test? Yes, another test!

***

### 示例 3: 基本情况

**参数值:**

* **表达式**: *空字符串*

**输出:** *空字符串*

***

### 示例 4: 基本情况

**参数值:**

* **表达式**: hello world! how are you? have a nice day.

**输出:** Hello world! How are you? Have a nice day.

***

### 示例 5: 基本情况

**参数值:**

* **表达式**: hELLO WORLD

**输出:** HELLO WORLD

***

### 示例 6: 基本情况

**参数值:**

* **表达式**: how many people? 100 people!

**输出:** How many people? 100 people!

***

### 示例 7: 基本情况

**参数值:**

* **表达式**: no punctuation

**输出:** No punctuation

***

### 示例 8: 空值情况

**参数值:**

* **表达式**: *空值*

**输出:** *空值*

***
