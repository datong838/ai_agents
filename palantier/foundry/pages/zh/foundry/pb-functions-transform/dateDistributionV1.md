---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/dateDistributionV1/",
  "title": "日期分布",
  "page_id": "dateDistributionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/complexCrossJoinV1/",
  "next": "/zh/foundry/pb-functions-transform/dimensionalityReductionV1/",
  "scraped_at": "2026-07-13T05:58:15.709298+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 日期分布

> 支持于: 批处理

计算指定列中日期/时间戳的分布。

**变换类别**: 日期时间

## 声明参数

* **列** - 要计算分布的列。<br>*列<日期 | 时间戳>*
* **数据集** - 要应用分布的数据集。<br>*表*
* **结束时间** - 分布的结束时间。之后的时间将被忽略。<br>*文字<日期 | 时间戳>*
* **起始时间** - 分布的起始时间。之前的时间将被忽略。<br>*文字<日期 | 时间戳>*
* **时间桶** - 用于桶的时间单位。<br>*枚举<天, 小时, 分钟, 月, 秒, 周, 年>*
