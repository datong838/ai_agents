---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/stringAfterDelimiterV1/",
  "title": "分隔符后的字符串",
  "page_id": "stringAfterDelimiterV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/startsWithV1/",
  "next": "/zh/foundry/pb-functions-expression/stringBeforeDelimiterV1/",
  "scraped_at": "2026-07-13T05:57:31.951193+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 分隔符后的字符串

> 支持于：批处理，流处理

提取第一个分隔符后的字符串。如果未找到匹配项，则返回完整字符串。

**表达式类别**: 字符串

## 声明的参数

* **Delimiter（分隔符）** - 分隔符的正则表达式。<br>*正则表达式*
* **Expression（表达式）** - 执行正则表达式操作的输入。<br>*表达式<字符串>*
* **Ignore case（忽略大小写）** - 正则表达式是否忽略大小写。<br>*字面量<布尔值>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **Delimiter（分隔符）**: hello
* **Expression（表达式）**: ... Hello world
* **Ignore case（忽略大小写）**: false

**输出:** ... Hello world

***

### 示例 2: 基本情况

**参数值:**

* **Delimiter（分隔符）**: Hello
* **Expression（表达式）**: ... Hello world
* **Ignore case（忽略大小写）**: false

**输出:** world

***

### 示例 3: 基本情况

**参数值:**

* **Delimiter（分隔符）**: hello
* **Expression（表达式）**: ... Hello world
* **Ignore case（忽略大小写）**: true

**输出:** world

***

### 示例 4: 空情况

**参数值:**

* **Delimiter（分隔符）**: Hello
* **Expression（表达式）**: *null*
* **Ignore case（忽略大小写）**: false

**输出:** *null*

***

### 示例 5: 边缘情况

**参数值:**

* **Delimiter（分隔符）**: Hello
* **Expression（表达式）**: ... Hello Hello world
* **Ignore case（忽略大小写）**: false

**输出:** Hello world

***
