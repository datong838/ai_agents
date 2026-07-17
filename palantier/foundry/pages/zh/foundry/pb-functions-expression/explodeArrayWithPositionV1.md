---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/explodeArrayWithPositionV1/",
  "title": "位置展开数组",
  "page_id": "explodeArrayWithPositionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/explodeArrayV1/",
  "next": "/zh/foundry/pb-functions-expression/explodeMapV1/",
  "scraped_at": "2026-07-13T05:54:42.570393+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 位置展开数组

> 支持于: 批处理, 流式处理

将数组展开为每个值一行，作为包含元素在数组中的相对位置和元素本身的结构。

**表达式类别**: 数组

## 声明的参数

* **数组** - 要展开的值数组。<br>*Expression\<Array\<T>>*
* **非必填** 保留空/空值数组 - 如果为true，空数组和空值将在输出中保留为空值，否则将被筛选。<br>*Literal\<Boolean>*

**类型变量界限：** *T接受AnyType*

**输出类型：** *Struct<非必填\[position]:Integer, 非必填\[element]:T>*
