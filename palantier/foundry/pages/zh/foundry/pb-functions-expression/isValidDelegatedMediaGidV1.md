---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/isValidDelegatedMediaGidV1/",
  "title": "是有效的委托媒体 gid",
  "page_id": "isValidDelegatedMediaGidV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/isValidOntologyGeopointV1/",
  "next": "/zh/foundry/pb-functions-expression/isValidMediaReferenceV1/",
  "scraped_at": "2026-07-13T05:56:04.173023+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 是有效的委托媒体 gid

> 支持于: 批处理, 流处理

如果输入是有效的 gotham 委托媒体 gid，则返回 true。有关更多详细信息，请查看 gotham 的委托媒体 rtfm。

**表达式类别**: 布尔

## 声明的参数

* **表达式** - 要检查是否为有效 gotham 委托媒体的字符串。<br>*Expression<字符串>*

**输出类型:** *布尔*

## 示例

### 示例 1: 基础情况

**参数值:**

* **表达式**: hello

**输出:** false

***

### 示例 2: 基础情况

**参数值:**

* **表达式**: ri.gotham-delegated-media.12345678-1234-1234-1234-123456789012.testaudiotype.testlocator

**输出:** true

***

### 示例 3: 空情况

**参数值:**

* **表达式**: *null*

**输出:** *null*

***
