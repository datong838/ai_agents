---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/isValidMimeTypeV1/",
  "title": "是否为有效MIME类型",
  "page_id": "isValidMimeTypeV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/isValidMgrsV1/",
  "next": "/zh/foundry/pb-functions-expression/isValidOntologyGeopointV1/",
  "scraped_at": "2026-07-13T05:56:16.246481+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 是否为有效MIME类型

> 支持于: 批处理, 流处理

如果输入是有效的MIME类型，则返回true。

**表达式类别**: 布尔型, 其他

## 声明的参数

* **表达式** - 表示MIME类型的字符串。<br>*表达式<字符串>*

**输出类型:** *布尔型*

## 例子

### 示例 1: 基本情况

**参数值:**

* **表达式**: `mimeType`

| mimeType | **输出** |
| ----- | ----- |
| application/pdf | true |
| not a MIME type | false |

***
