---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/time-series-properties-use-case-ontology/",
  "title": "使用 Ontology Manager 为 Object 添加时间序列属性",
  "page_id": "time-series-properties-use-case-ontology",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/time-series-properties-use-case-pipeline/",
  "next": "/zh/foundry/time-series/time-series-properties-use-case-operational/",
  "scraped_at": "2026-07-13T06:12:33.497316+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用 Ontology Manager 为 Object 添加时间序列属性

本指南参考了[在时间序列 Object 类型上设置时间序列属性](/zh/foundry/time-series/time-series-properties/)的文档。您可以根据需要向 Object 类型添加任意多的时间序列属性，假设每个 Object 始终会关联一个时间序列集合。请查阅我们的文档以了解选择[时间序列 Object 类型或传感器 Object 类型](/zh/foundry/time-series/time-series-overview/#store-time-series-in-the-ontology)的依据。

您必须为 `Route` 和 `Airport` Object 类型重复以下步骤。在本指南结束时，`Carrier`、`Route` 和 `Airport` Object 类型将各有三个时间序列属性，分别为 `Daily Count of Flights`、`Daily Average Arrival Delay` 和 `Daily Average Departure Delay`。

1. 在 Ontology Manager 中导航到 `Carrier` Object 类型，并选择 **Capabilities** 选项卡。
2. 在 **Time series property** 部分中选择 **+ Add**。

![在 Ontology Manager 中为 Object 添加时间序列属性](../../../images/foundry/time-series/time-series-properties-om-add-tsp.png)

3. 选择现有的 `Daily Count of Flights` 属性作为时间序列属性，然后选择 **Set as default time series property** 以便它在 Quiver 中自动出现。

![选择每日航班次数属性并设置为默认 TSP](../../../images/foundry/time-series/time-series-properties-om-select-sync-and-default.png)

4. 选择您在[Pipeline Builder](/zh/foundry/time-series/time-series-properties-use-case-pipeline/)中创建的时间序列同步。在我们的示例中，它被称为 `[Example] Time Series Sync | Event Pipeline`。

![为时间序列属性选择时间序列同步](../../../images/foundry/time-series/time-series-properties-om-add-sync.png)

5. 对 `Daily Average Arrival Delay` 和 `Daily Average Departure Delay` 时间序列属性重复此过程。

现在时间序列属性已添加到 Object 类型中，我们准备在操作环境中使用时间序列属性。请继续阅读文档以了解如何[在 Workshop 和 Quiver 中使用 Object 的时间序列属性](/zh/foundry/time-series/time-series-properties-use-case-operational/)。
