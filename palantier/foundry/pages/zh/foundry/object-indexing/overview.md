---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/object-indexing/overview/",
  "title": "概述",
  "page_id": "overview",
  "category_id": "ontology",
  "section_id": "object-indexing",
  "previous": "/zh/foundry/object-permissioning/multi-datasource-objects/",
  "next": "/zh/foundry/object-indexing/funnel-batch-pipelines/",
  "scraped_at": "2026-07-14T05:08:23.939888+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

在Ontology中，**索引**是通过专用数据库使Foundry数据源中的表格数据或其他形式的数据可用于更快速的数据检索操作的过程。

本节文档描述了Object Storage V2的索引过程，其中索引由Object数据漏斗服务（“漏斗”）监督。漏斗服务负责协调创建和修改Ontology中Object实例的漏斗管道，并确保数据和元数据的更新。

漏斗管道主要有两种类型，**漏斗批处理管道**和**漏斗流处理管道**，用户可以根据其数据源情况、延迟和工作流需求以及成本考虑选择其中一种索引机制。

[了解更多关于漏斗批处理管道的信息。](/zh/foundry/object-indexing/funnel-batch-pipelines/)

[了解更多关于漏斗流处理管道的信息。](/zh/foundry/object-indexing/funnel-streaming-pipelines/)

有关Object Storage V1（Phonograph）索引的信息，请查看[旧版文档](/zh/foundry/object-databases/object-storage-v1/)。
