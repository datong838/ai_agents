---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/schedules-overview/",
  "title": "概述",
  "page_id": "schedules-overview",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/branches-fallback-branches/",
  "next": "/zh/foundry/pipeline-builder/schedules-create-schedule/",
  "scraped_at": "2026-07-13T05:50:56.700934+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

Pipeline Builder 中的**调度**用于定期运行[构建](/zh/foundry/data-integration/builds/)。配置调度是确保管道数据保持最新，以供最终用户和下游工作流使用的重要部分。

调度的构建可以配置为在以下情况下运行：

* 在特定时间
* 当数据已更新
* 当逻辑已更新
* *以上条件的任意组合*

调度的构建可以配置为搭建：

* 单个数据集
* 单个数据集及其所有依赖项
* 所有依赖于某个数据集的数据集
* 所有连接两个数据集的数据集
* *以上配置的任意组合*

您可以直接在 Pipeline Builder 中设置基本的搭建调度，并在数据集视图中导航到高级设置和状态报告。随时编辑或删除调度，并查看我们的[最佳实践](/zh/foundry/building-pipelines/scheduling-best-practices/)以优化管道管理。

了解如何在 Pipeline Builder 中[创建调度](/zh/foundry/pipeline-builder/schedules-create-schedule/)，或了解更多关于在数据集视图中[查看和修改调度](/zh/foundry/building-pipelines/view-modify-schedules/)的信息。
