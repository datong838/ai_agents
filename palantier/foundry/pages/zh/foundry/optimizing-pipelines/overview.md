---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/optimizing-pipelines/overview/",
  "title": "概述",
  "page_id": "overview",
  "category_id": "data-integration",
  "section_id": "optimizing-pipelines",
  "previous": "/zh/foundry/building-pipelines/remove-inherited-markings/",
  "next": "/zh/foundry/optimizing-pipelines/debug-job/",
  "scraped_at": "2026-07-13T05:42:44.322156+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

在 Foundry 中创建[数据管道](/zh/foundry/data-integration/data-pipeline/)的过程中，您可能会遇到需要了解计算背后工作原理的细节，以便有效调试任务失败或提高计算性能的情况。通常，当您遇到意外的计算问题或性能问题时，应遵循以下步骤。

请注意，如果您的管道是[批处理管道](/zh/foundry/building-pipelines/pipeline-types/#batch)，您可以通过更好地利用 Foundry 中的 Spark 引擎来加速某些计算任务。然而，这种性能调优是有局限的。如果您的管道输入随着时间快速增长，您可能需要将管道调整为[增量](/zh/foundry/building-pipelines/pipeline-types/#incremental)模式，以便仅处理实际更改的数据行或文件。

如果您想从调试一个意外失败的任务或端到端管道开始，请参考以下指南：

* [调试失败的任务](/zh/foundry/optimizing-pipelines/debug-job/)
* [调试失败的管道](/zh/foundry/optimizing-pipelines/debug-pipeline/)

如果您有兴趣了解 Foundry 中计算的底层工作原理，请从[探索 Spark 核心概念](/zh/foundry/optimizing-pipelines/spark-concepts/)开始。
