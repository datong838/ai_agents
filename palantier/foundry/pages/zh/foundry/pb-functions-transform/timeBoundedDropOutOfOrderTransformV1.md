---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/timeBoundedDropOutOfOrderTransformV1/",
  "title": "有时间限制的乱序丢弃",
  "page_id": "timeBoundedDropOutOfOrderTransformV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/timeBoundedDropDuplicatesV2/",
  "next": "/zh/foundry/pb-functions-transform/timeBoundedEventTimeSortV1/",
  "scraped_at": "2026-07-13T05:59:22.765046+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 有时间限制的乱序丢弃

> 支持于: 流式处理

丢弃具有相同键列值且乱序的行。如果某行在基于排序列和方向的情况下应该排在已经接收的具有相同键值的行之前，那么该行就是乱序的。比较两行时，首先评估第一个排序列和方向，然后只有在平局的情况下才继续下一个排序列和方向，直到确定顺序或所有排序列都相等，此时行被视为相等。每个键的当前最大值会被存储，直到在事件时间大于或等于过期时间的情况下没有收到该键的新行为止。在一个键在过期时间内未收到新行后，该键的任何新行都不会被丢弃，并总是被存储为新的当前最大值。

**变换类别**: 其他

## 声明的参数

* **Dataset** - 数据集以丢弃乱序的行。<br>*Table*
* **Key expiration time unit** - 存储给定键的最大记录的时间单位。如果状态存储在一个键上，并且处理的不同键的水印大于此过期时间，则该键的状态过期，并且相同键的任何新记录将不会被丢弃。对于任何键，新记录将过期时间推至未来的此时间量，无论其是否具有最高的排序优先级。<br>*Enum\<Days, Hours, Milliseconds, Minutes, Seconds, Weeks>*
* **Key expiration time value** - 存储给定键的最大记录的时间值。如果状态存储在一个键上，并且处理的不同键的水印大于此过期时间，则该键的状态过期，并且相同键的任何新记录将不会被丢弃。对于任何键，新记录将过期时间推至未来的此时间量，无论其是否具有最高的排序优先级。<br>*Literal\<Long>*
* **Sort specification** - 数据集排序的规范。此列表为每个列用于排序两个记录的优先级。第一个列和排序方向用于比较两个记录，如果有平局，则使用第二个列和排序方向，依此类推。<br>*List\<Tuple\<Column\<ComparableType>, Enum\<Ascending, Descending>>>*
* 非必填 **Key by columns** - 用于按键分区输入的列。共享相同键列值的行按接收顺序处理。具有相同键列的行处理顺序可能与排序规范定义的顺序不同。根据排序规范，当一行应该放在已处理的具有相同键的最高优先级行之前时，该行被认为是乱序的。对于这样的乱序行，只要该键的状态存在且未过期，它们将在过程中被丢弃。<br>*Set\<Column\<AnyType>>*
