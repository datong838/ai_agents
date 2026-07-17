---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/explodeArrayV1/",
  "title": "拆分数组",
  "page_id": "explodeArrayV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/equalsV1/",
  "next": "/zh/foundry/pb-functions-expression/explodeArrayWithPositionV1/",
  "scraped_at": "2026-07-13T05:54:29.088874+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 拆分数组

> 支持于: 批处理, 流处理

将数组拆分为每个值的一行。

**表达式类别**: 数组

## 声明的参数

* **表达式** - *无描述*<br>*Expression\<Array\<T>>*
* *非必填* **保留空/空值数组** - 如果为true，空数组和空值将在输出中保留为空值，否则它们将被筛选。<br>*Literal\<Boolean>*

**类型变量界限:** *T 接受 AnyType*

**输出类型:** *T*
