---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/overview/",
  "title": "概述",
  "page_id": "overview",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/maintaining-pipelines/monitoring-views-intro/",
  "next": "/zh/foundry/pipeline-builder/core-concepts/",
  "scraped_at": "2026-07-13T05:45:44.100506+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

Pipeline Builder 是 Foundry 主要的用于数据集成的应用程序。您可以使用 Pipeline Builder 搭建数据集成管道，将原始数据源转换为准备好进行进一步分析的干净输出。

通过 Pipeline Builder 和强大的后端模型，编写代码的用户和不编写代码的用户可以共同协作在一个管道工作流中。与其编写需要长时间健康检查的代码，Pipeline Builder 允许用户通过简化的构建器界面应用数据变换。

Pipeline Builder 使用专为在逻辑创建和执行之间充当中介而设计的新一代数据变换后端。当用户描述他们想要搭建的管道时，后端编写变换代码并执行管道完整性检查，识别重构出错并提供解决方案以确保健康的搭建。后端作为逻辑创建和执行之间的中间层，构建者可以在搭建管道之前解决模式问题，节省以前用于计算和代码检查的时间。

![管道截图](../../../images/foundry/pipeline-builder/pipe-overview@2x.png)

## 功能

Pipeline Builder 包括专注于全面管道创建、维护和控制的功能。

* **直观的用户界面：** 用户使用基于图形和表单的界面来编写管道，这些界面提供反馈，包括合并键和列转换建议。
* **类型安全函数：** 函数是强类型的，可以立即标记出错，而不是在搭建时。
* **严格的输出检查：** 如果不满足预期的输出检查，将阻止搭建以避免无意的下游中断。
* **自动搭建路径修剪：** Pipeline Builder 将修剪未连接到输出的变换路径，以避免在搭建中不必要的计算。
* **抽象实现细节：** 用户专注于描述他们的端到端管道和期望的输出。搭建、同步和其他编排由 Pipeline Builder 后端自动处理。
* **独立的管道逻辑：** Pipeline Builder 可以连接到不同的逻辑执行引擎，包括 Spark、Flink、Azure 实例等。
* **可重用性：** 管道逻辑可以轻松提取并用于不同的管道。
* **完整版本控制：** 用户可以单独起草一个管道，协作在一个管道上，或恢复到以前的版本。
* **流功能：** Pipeline Builder 提供编写以实时延迟执行的管道的能力。此功能在所有 Foundry 环境中不可用。如果您的工作流需要流式管道的可用性，请联系您的 Palantir 代表。

## 工作流

Pipeline Builder 遵循一个从导入数据到交付健康搭建的工作流，包含以下步骤。

* **输入：** 添加新的数据源或额外的数据集。
* **变换：** 变换、合并或合并数据以获得期望的输出。
* **预览：** 应用变换后，预览输出。
* **交付：** 一旦管道完成，搭建管道输出。
* **输出：** 为您的管道添加一个对象类型、链接类型或数据集输出。

![管道流程图截图](../../../images/foundry/pipeline-builder/overview-flowchart@2x.png)

在 Pipeline Builder 图上可视化时，这些步骤可能会这样展示：

![管道截图，其中分离的列指示不同步骤](../../../images/foundry/pipeline-builder/workflow-graph@2x.png)

了解如何[创建一个简单的批处理管道](/zh/foundry/building-pipelines/create-batch-pipeline-pb/)，或了解更多关于在 Pipeline Builder 中搭建和管理管道的[核心概念](/zh/foundry/pipeline-builder/core-concepts/)。
