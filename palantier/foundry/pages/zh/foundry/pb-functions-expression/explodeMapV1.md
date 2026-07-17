---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/explodeMapV1/",
  "title": "展开映射",
  "page_id": "explodeMapV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/explodeArrayWithPositionV1/",
  "next": "/zh/foundry/pb-functions-expression/exponentialV1/",
  "scraped_at": "2026-07-13T05:54:31.550214+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 展开映射

> 支持于: 批处理, 流处理

将映射展开为每个键值对一行。

**表达式类别**: 映射

## 声明的参数

* **表达式** - *无描述*<br>*表达式<映射\<TKey, TValue>>*

**类型变量界限:** *TKey 接受 AnyType\*\*TValue 接受 AnyType*

**输出类型:** *结构<非必填\[key]:TKey, 非必填\[value]:TValue>*
