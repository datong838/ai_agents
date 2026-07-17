---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-integration/builds/",
  "title": "搭建",
  "page_id": "builds",
  "category_id": "data-integration",
  "section_id": null,
  "previous": "/zh/foundry/data-integration/branching/",
  "next": "/zh/foundry/data-integration/schedules/",
  "scraped_at": "2026-07-13T05:30:11.042836+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 搭建

**搭建**是Foundry中用于计算[数据集](/zh/foundry/data-integration/datasets/)新版本的机制。搭建提供计算的编排和协调，确保读取适当的输入数据，并将输出数据写入适当的位置。

一个搭建由多个**任务**组成，每个任务是一个由共享逻辑定义的工作单元，计算一个或多个输出数据集。请注意，如果一个任务定义了多个输出数据集，它们将始终一起更新，无法在不运行完整任务的情况下仅搭建某些数据集。任务规范或**JobSpec**是关于如何构建任务的定义。当Foundry中的数据变换逻辑发生更改时，例如当数据工程师在[代码仓库](/zh/foundry/code-repositories/overview/)中提交新的变换代码时，会发布JobSpecs。

运行一次搭建会导致一组输出数据集的一次性计算。为了保持数据在系统中的流动，使用[调度](/zh/foundry/data-integration/schedules/)来随时间运行搭建。

您可以使用[搭建应用程序](/zh/foundry/data-integration/application-reference/#builds)在Foundry中探索搭建。

## 任务和JobSpecs

一个*任务*封装了从一组输入数据集的数据中计算一个或多个*输出数据集*的新版本。*JobSpec*通过详细说明输入数据集依赖关系和应作为任务的一部分执行的逻辑来定义如何构建任务。

输入数据集依赖关系被声明为一组*InputSpecs*，每个InputSpec指定一个特定的输入数据集。InputSpecs指定要从数据集中读取的视图数据子集。

在Foundry中，可以表示为任务的逻辑类型包括但不限于：

* 数据连接[同步](/zh/foundry/data-connection/core-concepts/#syncs)定义了如何从外部数据源读取数据。
* 在[代码仓库](/zh/foundry/code-repositories/overview/)中编写的变换允许您编写变换数据集的代码。
* [健康检查](/zh/foundry/data-integration/health-checks/)被定义为在数据集上生成的任务，以验证数据集的特征。
* [分析应用](/zh/foundry/analytics/datasets-object-sets/)支持定义变换数据集的逻辑。
* 一个[导出](/zh/foundry/data-connection/export-overview/)定义了如何将输入数据发送到Foundry之外。

### 任务状态

在任何给定时间，任务总是在以下状态之一：

* `WAITING`：任务的初始状态；任务正在等待其依赖的任务完成且尚未被调用。
* `RUN_PENDING`：任务正在等待运行，但其执行环境尚未确认状态。
* `RUNNING`：任务已被调用并正在计算中。
* `ABORT_PENDING`：任务已被中止，但其执行环境尚未确认中止状态。
* `ABORTED`：任务被用户请求中止或由于依赖任务失败而中止。
* `FAILED`：任务被调用，但计算失败。
* `COMPLETED`：任务被调用，计算成功完成。

## 搭建生命周期

当一个搭建运行时，会执行几个步骤来验证提交的搭建，确保数据一致性，并仅运行必要的任务以生成新输出。

### 搭建解析

作为第一步，搭建：

* 检测指定输入数据集中的循环，如果存在循环则失败搭建。
* 验证所有输入数据集是否存在并识别每个输入数据集的适当模式。
* 在每个输出数据集上打开新的[事务](/zh/foundry/data-integration/datasets/#transactions)，以确保只有活动的搭建可以写入输出数据集。这称为*搭建锁定*。
* 检测是否有其他搭建正在进行中，会更改搭建的输入数据集。如果是这样，搭建可能会*排队*等待其他搭建完成。

### 任务执行

完成上述步骤后，搭建中的任务将被执行。相互不依赖的任务将并行运行。当任务通过[任务状态](#job-states)时，整个搭建的状态将相应更新：

* 如果搭建中的某个任务失败，则该搭建中所有直接依赖的任务和输出数据集上的事务将被终止。非必填地，可以将搭建配置为同时中止所有非依赖任务。
* 如果搭建中的所有任务都已完成，则认为搭建已完成。

请注意，如果搭建中的某个任务失败，先前完成的任务可能仍然已将数据写入其输出数据集。

### 陈旧性

如果[搭建解析](#build-resolution)步骤确定输入数据集和JobSpec中指定的逻辑自上次构建输出数据集以来没有更改，则输出数据集被认为是*新鲜的*。如果输出数据集是新鲜的，则不会在后续搭建中重新计算。

要覆盖搭建系统的默认陈旧性行为，您可以运行一个**强制搭建**，无论数据集是否已更新，都会重新计算所有数据集。

## 分支

Foundry中的搭建实现了**分支**以支持数据管道上的协作工作流。要了解有关分支的更多信息：

* 请参阅[分支概述](/zh/foundry/data-integration/branching/)以获得高级别的解释。
* 请参阅[搭建中的分支](/zh/foundry/data-integration/branching/#branches-in-builds)部分以了解分支在搭建中的工作原理。

## 实时日志

实时日志提供对运行任务的实时可见性，允许您监控任务的进展并检查长时间运行的任务，例如流或计算模块。

![Builds应用程序中的实时日志视图。](../../../images/foundry/data-integration/live-logs-overview.png)

您可以通过搭建应用程序访问实时日志。在查看任务时，选择日志查看器右上角的**查看实时**按钮以开始生成。

![Builds应用程序中任务的日志查看器页面上的"查看实时"选项。](../../../images/foundry/data-integration/live-logs-build-page.png)

实时日志的一个关键特性是按日志级别内置的颜色编码，使识别和优先处理警告和出错更容易：

![实时日志提要中各种颜色编码指示器的示例。](../../../images/foundry/data-integration/live-logs-color-coding.png)

* **信息：** 蓝色
* **严重/出错：** 红色
* **警告：** 橙色
* **调试/跟踪：** 灰色

此外，安全参数和参数以JSON块形式可见，为您的数据提供结构化和可读格式。

![实时日志提要中的"格式化为JSON"选项。](../../../images/foundry/data-integration/live-logs-json.png)

您可以通过从界面右上角选择**暂停**随时停止实时日志提要，并从同一位置恢复。

![实时日志提要中的"暂停"选项。](../../../images/foundry/data-integration/live-logs-pause.png)

请注意，时间范围选择不适用于实时日志，因为它们是从任务中实时流式传输的。

:::callout{theme="neutral"}
启用后，界面中实时日志可见之前可能会有十秒钟的延迟。
:::
