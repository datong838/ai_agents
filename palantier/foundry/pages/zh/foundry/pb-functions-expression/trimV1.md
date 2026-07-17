---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/trimV1/",
  "title": "删除空白字符",
  "page_id": "trimV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/transformMapValuesV1/",
  "next": "/zh/foundry/pb-functions-expression/dateTruncateV1/",
  "scraped_at": "2026-07-13T05:57:50.349527+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 删除空白字符

> 支持于: 批处理, 流处理

删除字符串起始和结尾的空白字符。空白字符定义为以下任意字符：1）Unicode的\p{whitespace} 集合中的字符，2）Java的String#trim()方法，或3）Java的Character#isWhitespace()方法。

**表达式类别**: 数据准备, 字符串

## 声明参数

* **表达式** - 要删除空白字符的输入字符串。<br>*Expression<字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**:    hello world

**输出:** hello world

***

### 示例 2: 空值情况

**参数值:**

* **表达式**: *null*

**输出:** *null*

***
