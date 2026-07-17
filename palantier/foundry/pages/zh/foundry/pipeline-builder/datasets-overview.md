---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/datasets-overview/",
  "title": "概述",
  "page_id": "datasets-overview",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/functions-index/",
  "next": "/zh/foundry/pipeline-builder/datasets-add/",
  "scraped_at": "2026-07-13T05:45:15.640740+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

要创建一个管道，您需要数据集。**数据集**被添加到管道中，可以被清理、变换，并与其他数据集合并，以便于进一步使用，通常作为 Foundry Ontology 的一部分。

Pipeline Builder 支持*结构化*和*半结构化*数据集。

结构化数据集由包含开源表格数据和关于数据集中列的元数据的文件组成。列的元数据与数据集一起存储为[模式](/zh/foundry/data-integration/datasets/#schemas)。

Pipeline Builder 还支持*半结构化*数据集，包括 XML、JSON 和 CSV 文件。您可以使用解析变换函数将半结构化文件转换为表格形式，并从模式安全中获益。了解如何[在您的管道中变换数据](/zh/foundry/pipeline-builder/transforms-transform-data/)。

在 Pipeline Builder 中定义工作流的第一步是将一个或多个数据集添加到您的工作区。请参阅以下文档，了解如何[添加数据集](/zh/foundry/pipeline-builder/datasets-add/)或[更改输入计算模式](/zh/foundry/pipeline-builder/datasets-computation-modes-for-batch/)，并通过访问[数据集成](/zh/foundry/data-integration/datasets/#datasets)了解更多关于 Foundry 中的数据集的信息。
