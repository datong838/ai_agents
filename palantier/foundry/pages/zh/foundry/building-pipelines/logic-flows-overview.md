---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/logic-flows-overview/",
  "title": "概述",
  "page_id": "logic-flows-overview",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/marketplace-schedules/",
  "next": "/zh/foundry/building-pipelines/create-a-connected-flow/",
  "scraped_at": "2026-07-13T05:41:48.004522+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

逻辑流允许您在 Foundry 中自动化常见工作流程。逻辑流与 Foundry 搭建和调度基础设施集成，以将其纳入您的数据管道中。

:::callout{theme="warning" title="逻辑流日落期"}
截至2024年8月，逻辑流处于[日落](/zh/foundry/platform-overview/development-life-cycle/)阶段，不应用于新的开发。
:::

## 核心概念

**自动化**是一个与 Foundry 服务 API 交互的脚本，使用搭建来替代平台中手动重复的操作。它的作用类似于 Foundry 中的其他任务，只是它不使用数据集作为输入或输出。Palantir 维护着一个精心策划的自动化库。

自动化将资源作为*参数*和一个 JSON *配置*。

自动化的特定实例称为**连接流**。连接流是通过项目、参数和配置创建的。

连接流：

* 在单个[项目](/zh/foundry/projects/overview/)中定义和执行
* 根据参数和配置运行，并在创建连接流时进行验证
* 可以作为[计划](/zh/foundry/data-integration/schedules/)的一部分运行
* 可以通过逻辑流 UI、数据沿袭或搭建应用程序手动运行
* 在运行之间不存储信息，因此创建新的连接流不会更改即将运行的结果
* 无法编辑
* 可以存档

## 可用自动化

* [**Compass 文件列出器**](/zh/foundry/building-pipelines/compass-file-lister/)
