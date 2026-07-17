---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/timeBoundedEventTimeSortV1/",
  "title": "有时间限制的事件时间排序",
  "page_id": "timeBoundedEventTimeSortV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/timeBoundedDropOutOfOrderTransformV1/",
  "next": "/zh/foundry/pb-functions-transform/topRowV2/",
  "scraped_at": "2026-07-13T05:59:07.782708+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 有时间限制的事件时间排序

> 支持于: 流式处理

以升序的事件时间按键发出行，允许延迟到达的记录至少到允许的延迟时间为止。超过允许延迟时间加上一些小的缓冲间隔后到达的记录将被丢弃。

**变换类别**: 其他

## 声明的参数

* **允许的延迟时间单位** - 等待延迟到达记录进行排序的时间单位。<br>*枚举<天, 小时, 毫秒, 分钟, 秒, 周>*
* **允许的延迟时间值** - 等待延迟到达记录进行排序的时间值。<br>*字面值<长整型>*
* **数据集** - 用于排序行的数据集。<br>*表格*
* **按列键分区** - 输入按键分区的列。每个键值的排序将分别计算。<br>*集合<列<任意类型>>*
