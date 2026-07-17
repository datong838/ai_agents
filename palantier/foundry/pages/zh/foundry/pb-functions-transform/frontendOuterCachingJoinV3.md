---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/frontendOuterCachingJoinV3/",
  "title": "外部缓存合并",
  "page_id": "frontendOuterCachingJoinV3",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/numericDistributionV2/",
  "next": "/zh/foundry/pb-functions-transform/outerCachingJoinV3/",
  "scraped_at": "2026-07-13T05:58:54.559899+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 外部缓存合并

> 支持于: 流式处理

符合所有匹配条件并在缓存窗口内的左侧和右侧输入行，以及来自两个输入的不匹配行。

**变换类别**: 合并

## 声明的参数

* **默认缓存时间单位** - 数据在逐出前缓存的默认时间单位，适用于lhs和rhs缓存。<br>*Enum\<Days, Hours, Milliseconds, Minutes, Seconds, Weeks>*
* **默认缓存时间值** - 数据在逐出前缓存的默认时间值，适用于lhs和rhs缓存。<br>*Literal\<Long>*
* **合并键** - 从左侧和右侧输入中用于合并的列列表。<br>*List\<Tuple\<Column\<AnyType>, Column\<AnyType>>>*
* **保留左侧列** - 保留的左侧列。<br>*List\<Column\<AnyType>>*
* **左侧数据集** - 在合并中使用的左侧数据集。<br>*Table*
* **保留右侧列** - 保留的右侧列。<br>*List\<Column\<AnyType>>*
* **右侧数据集** - 在合并中使用的右侧数据集。<br>*Table*
* **非必填** **右侧列的前缀** - 右侧列的前缀。<br>*Literal<字符串>*
* **非必填** **rhs缓存时间覆盖** - rhs数据集在逐出前缓存的时间值和单位。<br>*Tuple\<Literal\<Long>, Enum\<Days, Hours, Milliseconds, Minutes, Seconds, Weeks>>*
