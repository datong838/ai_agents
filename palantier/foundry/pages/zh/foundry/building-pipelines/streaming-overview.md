---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/streaming-overview/",
  "title": "流式管道：概述",
  "page_id": "streaming-overview",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/maintaining-incremental-performance/",
  "next": "/zh/foundry/building-pipelines/stream-vs-batch/",
  "scraped_at": "2026-07-13T05:40:51.125994+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 流式管道：概述

流式管道提供了基于实时数据进行即时关键决策的能力。通过专用计算将数据流式处理，流式管道能够以[非常低的延迟](/zh/foundry/building-pipelines/streaming-performance-considerations/)处理记录。平均而言，流式数据可以在不到15秒的时间内在Ontology中访问，并可用于时间序列应用程序的分析，例如[Quiver](/zh/foundry/quiver/overview/)或[Foundry Rules](/zh/foundry/foundry-rules/overview/)。为了实现这种低延迟，流是建立在[持续运行的计算](/zh/foundry/building-pipelines/streaming-compute-usage/)之上的，并且与批处理管道相比需要不同的架构和维护考虑。

## 最佳实践

在搭建流式管道时，请考虑以下因素：

* 流通常支持高度操作性的工作流，需要仔细规划停机时间、维护和逻辑更改，以确保高正常运行时间和可用性。
* 流式计算持续运行。这可能导致比定期批处理任务更高的计算成本。与批处理管道类似，考虑从可用的最小配置开始，如果数据规模需要，则进行调整。
* 流按每行操作，并且对最大行大小有约束，以确保低延迟的数据传输。此约束设置为每行1mb。
* 使用状态（例如窗口或聚合）的流需要设计考虑，以确保在更改流逻辑时状态不会被破坏。

## 入门

要在Foundry中使用流式管道，请查看如何[创建简单的流式管道](/zh/foundry/building-pipelines/create-stream-pipeline-pb/)，并在[Pipeline Builder](/zh/foundry/pipeline-builder/overview/)中了解流式变换。如果您想了解如何将数据源连接到Foundry，请查看[如何将数据推送到流中](/zh/foundry/data-connection/push-based-ingestion/)，或[如何设置流式同步](/zh/foundry/data-connection/set-up-streaming-sync/)。
