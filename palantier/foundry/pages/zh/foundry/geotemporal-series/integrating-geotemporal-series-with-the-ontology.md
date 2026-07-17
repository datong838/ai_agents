---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/geotemporal-series/integrating-geotemporal-series-with-the-ontology/",
  "title": "将地理时间序列与Ontology集成",
  "page_id": "integrating-geotemporal-series-with-the-ontology",
  "category_id": "data-integration",
  "section_id": "geotemporal-series",
  "previous": "/zh/foundry/geotemporal-series/data-modeling/",
  "next": "/zh/foundry/geotemporal-series/faq/",
  "scraped_at": "2026-07-13T06:20:08.361832+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将地理时间序列与Ontology集成

在您的Ontology中设置地理时间序列需要创建一个[地理时间序列Object类型](/zh/foundry/geotemporal-series/concepts-glossary/#geotemporal-series-object-type)，该类型引用[地理时间序列同步](/zh/foundry/geotemporal-series/concepts-glossary/#geotemporal-series-sync)中的单个序列，并具有[地理时间序列引用属性](/zh/foundry/geotemporal-series/concepts-glossary/#geotemporal-series-reference-gtsr)。这些Object类型将支持在Foundry应用中的分析和可视化。

地理时间序列同步在[Pipeline Builder](/zh/foundry/pipeline-builder/outputs-overview/)中使用[地理时间序列输出类型](/zh/foundry/pipeline-builder/outputs-add-geotemporal-series-output/)进行配置，并可能使用[Object输出类型](/zh/foundry/pipeline-builder/outputs-add-ontology-output/)。
