---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/leadV1/",
  "title": "Lead",
  "page_id": "leadV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/lastDayV1/",
  "next": "/zh/foundry/pb-functions-expression/leastV1/",
  "scraped_at": "2026-07-13T05:56:12.155117+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Lead

> 支持于: 批处理

返回窗口中当前行之后在'lead'处输入的值。

**表达式类别**: 聚合

## 声明的参数

* **表达式** - 要引导的表达式。<br>*Expression\<T>*
* **非必填** 默认值 - 如果在当前行之前的行数小于偏移量，则为默认值。<br>*Literal\<T>*
* **非必填** Lead - 要引导的行数。<br>*Literal\<Integer>*

**类型变量界限:** *T 接受 AnyType*

**输出类型:** *T*
