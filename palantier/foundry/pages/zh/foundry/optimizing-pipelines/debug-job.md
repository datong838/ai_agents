---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/optimizing-pipelines/debug-job/",
  "title": "调试失败任务",
  "page_id": "debug-job",
  "category_id": "data-integration",
  "section_id": "optimizing-pipelines",
  "previous": "/zh/foundry/optimizing-pipelines/overview/",
  "next": "/zh/foundry/optimizing-pipelines/debug-pipeline/",
  "scraped_at": "2026-07-13T05:43:44.301285+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 调试失败任务

在Foundry中编写数据变换代码时，您可能会遇到任务失败的情况，无论是起始时还是运行一段时间后。此页面记录了调试失败任务的推荐工作流程，以及Foundry中可用的工具，帮助您理解任务为何会开始失败。

## 推荐工作流程

下图提供了调试变换任务失败的推荐工作流程。

![调试任务](../../../images/foundry/optimizing-pipelines/debugging-jobs.png)

* \[1] 使用下面记录的[任务比较](#compare-jobs)。
* \[2] 您可以通过导航任务报告，选择 **操作** > **重新运行为调试任务** > 选择先前成功构建的模块版本来测试您的搭建。
* \[3] [排查OOM错误](/zh/foundry/optimizing-pipelines/troubleshoot-ooms/)。
* \[4] [代码库升级](/zh/foundry/code-repositories/repository-upgrades/)。
* \[5] 您可以通过导航到任务报告并选择 **日志** > `_driver.log` > **下载** 来下载您的任务的驱动日志。

## 比较任务

任务比较工具允许您将当前任务与之前成功运行的任务进行比较。它对调查更改和排查搭建问题非常有用。它可以从任何具有输出事务的任务的搭建报告页面在Builds应用中访问。为了访问任务比较工具，点击任何任务行上的“比较”按钮：

![打开任务比较工具](../../../images/foundry/optimizing-pipelines/job-comparison-open-compare.png)

### 比较摘要

此标签提供了任务期间发生的更改概述。点击任何数据集将打开一个新标签，使用数据集应用的比较工具探索事务更改。点击代码库将重定向您的浏览器到任务发生时的提交源代码库，允许探索整个代码库而不仅仅是与此任务输出关联的文件。

![任务比较摘要](../../../images/foundry/optimizing-pipelines/job-comparison-summary.png)

### 输入更改

此标签提供输入数据集更改的高级概览，突出显示元数据、模式和统计信息的更改。如果数据集有任何显著的列更改，选择该行将展开这些更改的摘要。要详细探讨更改，选择任何数据集将重定向到数据集应用进行进一步比较。

![任务比较输入](../../../images/foundry/optimizing-pipelines/job-comparison-inputs.png)

### 代码更改

代码更改将突出显示此任务运行与先前成功运行之间在定义输出的文件中的任何代码更改。为了获取更多详细信息，提供了按钮以在提交时重定向到源代码库（仅在源代码库是代码库时可用）。代码差异适用于基于代码库或代码工作簿的任何任务。

![任务比较代码](../../../images/foundry/optimizing-pipelines/job-comparison-code.png)

## 挂起的搭建

如果您的搭建挂起，请遵循上述工作流程。如果这是第一次运行此任务，很可能是由于用户代码导致搭建挂起。

与失败任务的一个重要区别是，当搭建被取消时，驱动日志会丢失。在取消搭建之前，通过选择 **日志** > `_driver.log` > **下载** 下载流式驱动日志。您还可以在[了解Spark详情](/zh/foundry/optimizing-pipelines/understand-spark-details/#executors-tab)的**执行器** > **快照**中拍摄运行中的搭建快照。这些将允许您在取消后排查挂起的搭建。

## AI错误增强器 (AIP)

如果您的堆栈中启用了AIP，[AI错误增强器微件](/zh/foundry/code-repositories/aip-features/#error-enhancer)补充了失败任务的详细视图，帮助您更好地理解和解决出现的问题。

![任务追踪器中AI错误增强器的动画截图](../../../images/foundry/optimizing-pipelines/error-enhancer-in-job-tracker.gif)
