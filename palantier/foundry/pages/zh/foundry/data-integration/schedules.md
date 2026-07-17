---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-integration/schedules/",
  "title": "调度",
  "page_id": "schedules",
  "category_id": "data-integration",
  "section_id": null,
  "previous": "/zh/foundry/data-integration/builds/",
  "next": "/zh/foundry/data-integration/health-checks/",
  "scraped_at": "2026-07-13T05:30:13.282015+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 调度

**调度**用于定期运行[搭建](/zh/foundry/data-integration/builds/)，以确保数据在Foundry中持续流动。在调度中，**触发器**定义了必须满足的条件才能运行相关的搭建。

当触发器满足条件并执行搭建时，我们称之为调度**运行**。如果在上一次运行仍在操作中时触发了一个调度，那么它将保持触发状态，并仅在上一个调度完成后运行。

运行历史记录提供了调度何时运行的记录以及每次运行中执行的任务的信息。调度运行可以是以下几种类型之一：

* **成功**。运行成功启动了一个搭建。请注意，成功的运行仅表示搭建成功启动。搭建本身可能仍在运行，或者可能已失败。
* **忽略**。尝试了运行，但没有创建搭建。被忽略的运行可能表示一切都是最新的，没有需要做的工作。有关更多详细信息，请参阅[陈旧性](/zh/foundry/data-integration/builds/#staleness)。
* **失败**。调度运行失败。

要了解有关调度的更多信息，请参考以下资源：

* 学习[创建调度](/zh/foundry/building-pipelines/create-schedule/)。
* 了解[调度最佳实践](/zh/foundry/building-pipelines/scheduling-best-practices/)。
* 探索[可用的触发器类型](/zh/foundry/building-pipelines/triggers-reference/)。

### 查找和管理调度

调度可以在[数据沿袭](/zh/foundry/data-lineage/manage-schedules/)应用程序的调度侧边栏中进行编辑、管理和更新。围绕查找调度的工作流可以在**搭建调度**应用程序中进行，该应用程序可以从您的应用程序侧边栏中获得。您可以运行的查询包括但不限于以下内容：

* “由某用户暂停的调度”
* “查找限定于某个项目的调度，按名称筛选，并按最新运行排序”
* “查找名称中包含'TESTING\_PROJECT\_1'的调度”
* “查找暂停的调度”

您可以使用以下搜索标准：

* \*\*文件：\*\*按Foundry中它们搭建的数据集或其他资产查找调度。如果未指定分支，将使用默认分支。
* \*\*用户：\*\*按选择的用户查找最近更新的调度。
* \*\*项目：\*\*查找限定于特定项目的项目范围调度。目前在此参数中不支持用户范围调度。

进入页面时，您将首先看到自己的调度。然后，您可以按名称筛选调度、暂停或排序。搜索参数存储在页面链接中，允许您书签页面或与其他用户共享链接。

调度列表可以通过**调度名称**（如果调度上存在）和**暂停状态**进一步细化。还可以按调度的**名称**、**创建日期**、**最后运行日期**或**最后更新日期**进行排序。

### 暂停调度

可以[暂停](/zh/foundry/building-pipelines/view-modify-schedules/#pause-a-schedule)调度，以暂时防止其运行。

当调度暂停时，其触发器状态将被重置，所有观察到的事件将被遗忘。调度暂停时，无法触发，并且将忽略所有观察到的事件。

可以[恢复](/zh/foundry/building-pipelines/view-modify-schedules/#resume-a-schedule)暂停的调度，以允许其重新开始运行。

### 项目范围

调度有权搭建的数据集是由调度是使用用户对数据集的权限保存的，还是使用包含所搭建数据集的项目集合保存的来决定的。前者（用户模式）如果用户的权限发生变化，由于调度运行时就像用户在运行搭建一样，容易发生意外更改。后者（项目范围模式）更为一致，因为调度独立于用户权限运行，只有在调度所范围的项目集合更改时才会更改。
