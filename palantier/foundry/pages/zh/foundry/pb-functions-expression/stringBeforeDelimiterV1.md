---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/stringBeforeDelimiterV1/",
  "title": "分隔符前的字符串",
  "page_id": "stringBeforeDelimiterV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/stringAfterDelimiterV1/",
  "next": "/zh/foundry/pb-functions-expression/stringContainsV1/",
  "scraped_at": "2026-07-13T05:57:24.524807+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 分隔符前的字符串

> 支持于: 批处理, 流处理

提取第一个分隔符之前的字符串。如果未找到匹配项，则返回完整字符串。

**表达式类别**: 字符串

## 声明的参数

* **Delimiter** - 分隔符的正则表达式。<br>*Regex*
* **Expression** - *无描述*<br>*Expression<字符串>*
* **Ignore case** - *无描述*<br>*Literal\<Boolean>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **Delimiter**: hello
* **Expression**: ... Hello world
* **Ignore case**: false

**输出:** ... Hello world

***

### 示例 2: 基本情况

**参数值:**

* **Delimiter**: Hello
* **Expression**: ... Hello world
* **Ignore case**: false

**输出:** ...

***

### 示例 3: 基本情况

**参数值:**

* **Delimiter**: hello
* **Expression**: ... Hello world
* **Ignore case**: true

**输出:** ...

***

### 示例 4: 空值情况

**参数值:**

* **Delimiter**: Hello
* **Expression**: *null*
* **Ignore case**: false

**输出:** *null*

***
