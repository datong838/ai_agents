---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/lagV1/",
  "title": "滞后",
  "page_id": "lagV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arrayJoinV1/",
  "next": "/zh/foundry/pb-functions-expression/lastV1/",
  "scraped_at": "2026-07-13T05:56:07.704193+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 滞后

> 支持于: 批处理

返回窗口中当前行之前'滞后'的输入值。

**表达式类别**: 聚合

## 声明的参数

* **表达式** - 滞后的表达式。<br>*Expression\<T>*
* **非必填** 默认值 - 如果在当前行之前的行数少于偏移量，则使用默认值。<br>*Literal\<T>*
* **非必填** 滞后 - 滞后的行数。<br>*Literal\<Integer>*

**类型变量界限:** *T 接受 AnyType*

**输出类型:** *T*
