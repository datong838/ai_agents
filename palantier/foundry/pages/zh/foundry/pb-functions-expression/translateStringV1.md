---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/translateStringV1/",
  "title": "字符逐个翻译字符串",
  "page_id": "translateStringV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/changeTimestampTimeZoneV1/",
  "next": "/zh/foundry/pb-functions-expression/chunkStringV1/",
  "scraped_at": "2026-07-13T05:53:12.422928+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 字符逐个翻译字符串

> 支持于: 批处理, 流处理

将输入列中与匹配字符串中的字符相同的字符替换为替换字符串中的对应字符。如果匹配字符串比替换字符串长，匹配字符串末尾的字符将被丢弃。

**表达式类别**: 字符串

## 声明的参数

* **表达式** - 要翻译的表达式。<br>*Expression\<AnyType>*
* **匹配字符串** - 包含匹配输入字符串字符的字符串。<br>*Literal<字符串>*
* **替换字符串** - 包含用于替换匹配字符的字符的字符串。<br>*Literal<字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: translate
* **匹配字符串**: rnlt
* **替换字符串**: 123

**输出:** 1a2s3ae

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: abc
* **匹配字符串**: aab
* **替换字符串**: de

**输出:** dc

***

### 示例 3: 基本情况

**参数值:**

* **表达式**: abc
* **匹配字符串**: acb
* **替换字符串**: de

**输出:** de

***

### 示例 4: 基本情况

**参数值:**

* **表达式**: abc
* **匹配字符串**: ac
* **替换字符串**: df

**输出:** dbf

***

### 示例 5: 空值情况

**参数值:**

* **表达式**: *null*
* **匹配字符串**: a
* **替换字符串**: b

**输出:** *null*

***
