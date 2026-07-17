---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/overview/",
  "title": "概述",
  "page_id": "overview",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/data-integration/streaming-profiles/",
  "next": "/zh/foundry/building-pipelines/pipeline-types/",
  "scraped_at": "2026-07-13T05:39:49.404098+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

创建[数据管道](/zh/foundry/data-integration/data-pipeline/)的第一步是将组织的数据源连接到Foundry，并让数据流动通过系统。最初，重点应放在验证数据是否具有高质量，并能作为应用案例开发、模型开发和分析的可靠基础。

本节文档侧重于创建管道的初始阶段，此时业务需求可能仍在变化，管道逻辑的更改频繁发生。在这个阶段，重点是打下坚实的基础——既支持目标应用案例，也能够在未来进行管道维护。

## 初始步骤

在大多数情况下，您在管道开发中应遵循以下初始步骤：

* 设置[推荐的项目结构](/zh/foundry/building-pipelines/recommended-project-structure/)，以便从开发过程的最初阶段就组织好数据安全和治理。
* 在[管道构建器](/zh/foundry/building-pipelines/create-batch-pipeline-pb/)或[代码库](/zh/foundry/building-pipelines/create-batch-pipeline-cr/)中创建批处理管道，以处理输入数据集，进行数据清理和筛选，并与其他数据集合并，创建可以输入到[Ontology](/zh/foundry/ontology/overview/)中的高质量数据集，以支持工作流开发。
* 将最终数据集映射到Ontology中的[对象类型](/zh/foundry/object-link-types/object-types-overview/)和[链接类型](/zh/foundry/object-link-types/link-types-overview/)。
* 设置[计划](/zh/foundry/building-pipelines/scheduling-overview/)，以便数据开始定期流动。

除了这些步骤外，还有许多步骤可以使您的管道更稳健和可扩展，包括添加单元测试、设置分支和发布流程、定义健康检查。[了解管道开发的最佳实践](/zh/foundry/building-pipelines/development-best-practices/)。

## 增量管道

如果流入管道的输入数据更改规模较大，最好创建一个[增量管道](/zh/foundry/building-pipelines/incremental-overview/)以高效处理更改的数据。在大多数情况下，您可以从批处理管道开始，然后设置增量管道以提高性能和减少延迟。

在某些情况下，最好从一开始就设计您的管道为增量，特别是当您知道流入管道的新数据规模会很大时。然而，编写和维护增量管道比批处理管道复杂得多。[了解Foundry中不同类型管道的更多信息](/zh/foundry/building-pipelines/pipeline-types/)。

## 流式管道

如果对数据延迟的要求很低，最好创建一个[流式管道](/zh/foundry/building-pipelines/streaming-overview/)以高效处理输入数据。由于流式管道的速度取决于其最慢的组件，因此管道应从一开始就设计，以确保管道达到目标延迟和吞吐量。查看我们关于[流式与批处理过程的比较](/zh/foundry/building-pipelines/stream-vs-batch/)，以获得更细致的分析。
