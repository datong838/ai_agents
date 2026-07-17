---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/geotemporal-series/overview/",
  "title": "概述",
  "page_id": "overview",
  "category_id": "data-integration",
  "section_id": "geotemporal-series",
  "previous": "/zh/foundry/geospatial/add-ontology-data-to-gaia/",
  "next": "/zh/foundry/geotemporal-series/concepts-glossary/",
  "scraped_at": "2026-07-13T06:19:07.596110+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

:::callout{theme="warning" title="Beta"}
地理时间序列处于测试状态，可能在所有注册中不可用。在产品普遍可用之前，一些功能可能会更改。
:::

地理时间序列数据用于跟踪实体随时间的地理位置。地理时间序列在概念上类似于[时间序列](/zh/foundry/time-series/time-series-overview/)，但它们包含一个地理空间组件。

以下是一些可以自然建模的地理时间序列数据示例：

* 飞机在起点和目的地之间飞行的地点和时间
* 鸟类迁徙穿越北美洲每天发出的GPS信号
* 从分发到交付的包裹跟踪

您可以使用地理时间序列数据在地图上实现实时位置数据或分析历史数据，以获得随时间和空间变化的趋势洞察。

## 使用地理时间序列数据

要在Foundry中使用地理时间序列数据，您必须设置以下两个组件：

* [地理时间序列Object类型](/zh/foundry/geotemporal-series/concepts-glossary/#geotemporal-series-object-type)：将地理时间序列与元数据关联，并允许Foundry应用程序访问序列数据。例如，您可以在Object类型上包括起点和目的地机场，以及存储为地理时间序列的飞行路径。
* [地理时间序列同步](/zh/foundry/geotemporal-series/concepts-glossary/#geotemporal-series-sync)：由数据集或流支持的资源，将地理时间序列数据索引到优化数据库中，并为[地理时间序列引用](/zh/foundry/geotemporal-series/concepts-glossary/#geotemporal-series-reference-gtsr)提供值。您可以使用[Pipeline Builder](/zh/foundry/pipeline-builder/outputs-overview/#geotemporal-series-syncs)配置地理时间序列同步。

了解更多关于[如何在Ontology中存储地理时间序列](/zh/foundry/geotemporal-series/integrating-geotemporal-series-with-the-ontology/)。
