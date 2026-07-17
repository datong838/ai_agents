---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/heartbeatDetectionV2/",
  "title": "心跳检测",
  "page_id": "heartbeatDetectionV2",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/loadMediaReferencesV1/",
  "next": "/zh/foundry/pb-functions-transform/complexInnerJoinV1/",
  "scraped_at": "2026-07-13T05:58:40.316076+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 心跳检测

> 支持于: 流式

检测在一组键中，当记录在可配置的时间内未被看到时。

**变换类别**: 其他

## 声明的参数

* **数据集** - 输入数据集。<br>*表格*
* **心跳时间单位** - 等待特定键的数据的时间单位。<br>*枚举<天, 小时, 毫秒, 分钟, 秒, 周>*
* **心跳时间值** - 等待特定键的数据的时间值。<br>*字面值<长整型>*
* **按列分区** - 用作检测心跳的键的列集合。<br>*集合<列<任何类型>>*
