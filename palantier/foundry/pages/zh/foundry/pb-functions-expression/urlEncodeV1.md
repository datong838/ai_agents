---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/urlEncodeV1/",
  "title": "Url 编码",
  "page_id": "urlEncodeV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/urlDecodeV1/",
  "next": "/zh/foundry/pb-functions-expression/useLlmV2/",
  "scraped_at": "2026-07-13T05:58:05.566054+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Url 编码

> 支持于: 批处理，流处理

对要在url中发送的字符串进行百分比编码。

**表达式类别**: 字符串

## 声明的参数

* **表达式** - 要进行url编码的表达式。<br>*表达式<字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `string`

| string | **输出** |
| ----- | ----- |
| raw\_string\_with\_no\_special\_characters | raw\_string\_with\_no\_special\_characters |
| test/api?string=3 | test%2Fapi%3Fstring%3D3 |

***

### 示例 2: 空值情况

**参数值:**

* **表达式**: *null*

**输出:** *null*

***
