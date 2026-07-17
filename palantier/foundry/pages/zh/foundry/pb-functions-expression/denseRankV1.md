---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/denseRankV1/",
  "title": "Dense rank",
  "page_id": "denseRankV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/geobufToGeometryExpressionV1/",
  "next": "/zh/foundry/pb-functions-expression/distinctCountV1/",
  "scraped_at": "2026-07-13T05:54:20.396729+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Dense rank

> 支持于: 批处理

返回窗口分区内行的排名，没有任何间隙。在平局的情况下，行获得相同的排名。rank 和 dense\_rank 之间的区别在于，当存在平局时，dense\_rank 在排名序列中不留下间隙。

**表达式类别**: 聚合

## 声明的参数

此函数不接受任何参数。

**输出类型:** *整数*
