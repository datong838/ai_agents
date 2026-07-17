---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/titleCaseV1/",
  "title": "标题大小写",
  "page_id": "titleCaseV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/timestampToEpochSecondsV1/",
  "next": "/zh/foundry/pb-functions-expression/cpuJsonAudioTranscriptionV1/",
  "scraped_at": "2026-07-13T05:57:47.972321+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 标题大小写

> 支持于: 批处理, 流处理

将每个单词的第一个字符转换为大写，其余字符为小写。

**表达式类别**: 字符串

## 声明的参数

* **表达式** - *无描述*<br>*Expression<字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本案例

**参数值:**

* **表达式**: hello world

**输出:** Hello World

***

### 示例 2: 空值案例

**参数值:**

* **表达式**: *null*

**输出:** *null*

***
