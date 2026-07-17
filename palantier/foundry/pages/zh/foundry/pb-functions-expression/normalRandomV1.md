---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/normalRandomV1/",
  "title": "正态随机数",
  "page_id": "normalRandomV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/negateV1/",
  "next": "/zh/foundry/pb-functions-expression/notV1/",
  "scraped_at": "2026-07-13T05:56:45.482100+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 正态随机数

> 支持于: 批处理, 流处理

返回零均值和单位方差的正态分布随机数列。这不是确定性的，即使使用种子，在重复的搭建中也不会产生相同的结果。

**表达式类别**: 数值

## 声明的参数

* *非必填* **种子** - 添加种子意味着每次搭建时，随机数将从相同的序列中生成。如果您需要true随机数，则不应提供种子。由于计算可能是分布式的，且不保证抽取行随机数的顺序，种子不会产生完全确定性的结果。<br>*Literal\<Long>*

**输出类型:** *Double*
