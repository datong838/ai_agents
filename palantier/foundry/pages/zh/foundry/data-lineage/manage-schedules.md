---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-lineage/manage-schedules/",
  "title": "管理计划",
  "page_id": "manage-schedules",
  "category_id": "data-integration",
  "section_id": "data-lineage",
  "previous": "/zh/foundry/data-lineage/build-datasets/",
  "next": "/zh/foundry/data-lineage/check-permissions/",
  "scraped_at": "2026-07-13T06:03:47.808626+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 管理计划

数据沿袭允许您轻松管理沿袭图中的搭建计划。在右侧边栏中，选择**管理计划**以打开计划详情窗格。

![在数据沿袭中管理计划](../../../images/foundry/data-lineage/manage-schedules.png)

您将看到与图中选定数据集相关的计划。点击某个计划以查看更多详情：

![在数据沿袭侧边栏中管理计划详情](../../../images/foundry/data-lineage/manage-schedule-details.png)

* **最新运行：** 计划最新一次运行的状态。
* **最后更新：** 最后一次更新的时间戳以及进行更改的用户
* **目标数据集：** 搭建计划中包含的下游数据集列表。
* **搭建时机：** 显示创建搭建计划时确定的搭建计划触发器。例如，可以将搭建计划设置为在**特定数据集更新时**运行。
* **搭建范围：** 定义搭建中包含的项目或用户数据集及运行搭建所使用的权限。

在[**搭建管道**](/zh/foundry/building-pipelines/scheduling-overview/)文档中了解更多关于计划搭建的信息。
