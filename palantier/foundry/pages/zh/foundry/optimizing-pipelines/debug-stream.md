---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/optimizing-pipelines/debug-stream/",
  "title": "调试失败的流",
  "page_id": "debug-stream",
  "category_id": "data-integration",
  "section_id": "optimizing-pipelines",
  "previous": "/zh/foundry/optimizing-pipelines/debug-pipeline/",
  "next": "/zh/foundry/optimizing-pipelines/troubleshoot-ooms/",
  "scraped_at": "2026-07-13T05:44:14.365453+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 调试失败的流

在构建流式数据管道时，您可能会遇到流式任务失败的情况。本页面提供了调试失败流的建议工作流程，并讨论了 Foundry 中可用的工具，以帮助您理解流失败的原因。

## 失败类型

失败可以分类为不同的类型，每种失败类型可能指向不同的根本原因。以下是一些最常见的失败类型及其可能发生的原因。

* **立即失败:** 流在起始5分钟内失败。
* **瞬时失败:** 流运行一段时间后失败一次，然后成功重启并继续运行。
* **持续失败:** 流运行一段时间后出现一系列立即失败，每次在流重启后的5-10分钟内发生。

### 立即失败

快速失败的流通常存在用户编写的逻辑问题。例如，失败可能来自无效的类型转换、解析异常或其他阻止流式集群成功启动的问题。

如果之前成功的流现在失败，检查逻辑和上游流的任何更改以发现潜在问题。

要确定这些问题的根本原因，请按照下面[检查流式集群日志](#check-streaming-cluster-logs)工作流程中概述的步骤进行操作。

### 瞬时失败

之前运行成功但重启后再次运行失败的流通常指向由网络中断引起的基础设施问题。中断通常是由运行 Foundry 实例的云提供商引起的（例如，AWS、Azure 或 GCP 的中断）。为流应用计划将使 Foundry 自动重新运行您的流并从中断点继续处理。

### 持续失败

之前成功运行但现在在没有任何逻辑更改的情况下反复失败的流通常最难识别。然而，它们通常由两个因素之一引起：新的输入数据阻止流进展（例如，无效类型、损坏数据等），或存在持续的基础设施问题（AWS 中断等）。

要检查错误是否由管道中的逻辑引起，请按照下面[检查流式集群日志](#check-streaming-cluster-logs)工作流程中概述的步骤进行操作。

## 常见调试工作流程

下面，我们概述了一些可用于解决常见流式问题的工作流程。这些检查不需要按特定顺序进行。

### 检查流式集群日志

按照[检索流日志](#retrieve-stream-logs)的步骤操作，并在日志中搜索任何异常、错误或“throwable”。这些日志通常通过“ERROR”、“throwable”或“Exception”等关键词提供潜在根本问题的描述。

### 检查管道逻辑

管道逻辑的更改通常会因用户编写代码中的错误而导致中断。通常，在前一步获取的日志中的异常会指向导致问题的特定代码。如果是这样，您可以尝试回滚任何更改，看看是否能解决问题。

### 检查输入数据

有时，流式管道中的逻辑在遇到意外数据时会抛出异常。例如，如果管道将两列相除并返回除数为`0`或`null`的值，这种行为就会出现。检查输入流末尾的记录，看看数据是否发生了可能导致流式管道问题的变化。如果发现数据更改了，考虑添加筛选或逻辑以清理数据或将其删除。

### 检查流详情

Foundry 检测到流失败时的常见异常并在流详情页面显示出来。检查详情以查看是否有任何错误出现。

:::callout{theme="neutral"}
有时您可以在流日志中找到比详情页面更多的错误信息。我们建议检查这两个位置以获取有关流失败的信息。
:::

<img alt="流失败页面" src="../../foundry-docs/optimizing-pipelines/media/stream-failure@2x.png">

<img alt="流搭建错误输出" src="../../foundry-docs/optimizing-pipelines/media/stream-build-error@2x.png">

## 检索流日志

您可能会在流过程中遇到失败，并需要访问搭建日志以确定原因。搭建日志通常是确定不同类型流失败原因的最佳地点。

要检索流任务的日志，首先在[数据集预览](/zh/foundry/dataset-preview/overview/)中导航到流详情页面。

接下来，找到您要查看的任务，然后点击**下载日志**。

<img alt="流视图" src="../../foundry-docs/optimizing-pipelines/media/stream-view@2x.png">

选择您希望首先下载日志的最早或最新日志行。

<img alt="下载日志按钮" src="../../foundry-docs/optimizing-pipelines/media/stream-logs-download@2x.png">

## 流错误

### 任务反复失败且不可恢复

```
Caused by: com.palantir.logsafe.exceptions.SafeIllegalStateException: Start transaction rid is not part of the current view.
```

这个错误信息表示：在尝试开始一个事务时，给定的事务ID（rid）不在当前视图中。这通常意味着事务ID的状态或上下文与当前系统所期望的不一致，可能需要检查事务的创建或管理逻辑。
此错误通常是由于输入数据集的新快照在流式处理中运行所导致的。

流式处理在记录接收到后立即将其发送到下游，这使得记录不可逆。当创建新的快照时，流式任务会忽略以前的事务，只使用新的事务。为了丢弃旧记录并使用新快照，请运行手动重播。

通过执行新的管道部署并在**部署管道**向导中选择**部署时重播**选项，可以解决此问题。

!["部署管道"窗口显示"部署时重播"选项的复选框已选中。](../../../images/foundry/optimizing-pipelines/stream-troubleshoot-1.png)
