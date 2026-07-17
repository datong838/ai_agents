---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/view-modify-schedules/",
  "title": "查看和修改计划",
  "page_id": "view-modify-schedules",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/create-schedule/",
  "next": "/zh/foundry/building-pipelines/find-manage-schedules/",
  "scraped_at": "2026-07-13T05:41:40.736708+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 查看和修改计划

## 查看指标

要查看现有计划的指标和运行历史：

1. 导航到数据集视图，打开**操作**菜单，选择**管理计划**。
2. 这将带您进入该数据集的数据沿袭图，计划面板在右侧打开。

   要查看计划的指标和搭建历史，请选择**指标**按钮。

   ![schedules-page-metrics]

## 查看计划编辑历史

每次编辑计划时，都会创建一个新版本。计划版本页面允许您：

* 查看计划的以前版本。
* 比较两个计划版本以查看更改了什么。

要查看计划的以前版本：

1. 导航到计划的指标页面。
2. 选择版本选项卡：

   ![schedules-versions](../../../images/foundry/building-pipelines/schedule-versions.png)

仅显示截至显示日期的版本。如果您需要查看较早的版本，请编辑页面右上角的日期选择器。

## 编辑计划

要编辑现有计划：

1. 导航到数据集视图，打开**操作**菜单，选择**管理计划**。

2. 这将带您进入该数据集的数据沿袭图，计划面板在右侧打开。

3. 要编辑计划，请点击该计划的条目。

   ![schedules-page-edit]

4. 要编辑计划，选择编辑按钮。[了解如何使用计划编辑器编辑计划。](/zh/foundry/building-pipelines/create-schedule/#define-the-schedule)

5. 完成计划编辑后，点击**保存**按钮。

## 暂停计划

要暂停计划：

1. 在数据沿袭中导航到数据集，并打开计划侧边栏，从侧边栏中选择计划。
2. 这将带您进入该数据集的计划页面。
3. 要暂停计划，请选择右上角的暂停图标。

   ![schedules-page-pause]

## 恢复计划

要恢复计划：

1. 在数据沿袭中导航到数据集，并打开计划侧边栏，从侧边栏中选择计划。
2. 这将带您进入该数据集的计划页面。
3. 要恢复计划，选择右上角的**恢复**。

   ![schedules-page-resume]

## 自动暂停的计划

Foundry 会自动暂停所有任务连续失败多次的计划。一旦计划成功运行，计划将自动解除暂停，失败计数器将被重置。如果您的计划被暂停并希望恢复，请按照以下步骤操作：

1. 通过点击发送给您的电子邮件中的链接导航到计划。
2. 调试计划。请参考[故障排除指南](/zh/foundry/optimizing-pipelines/troubleshoot-schedules/)。
3. 在应用修复后运行计划。当计划启动的任务成功完成后，计划将自动解除暂停。

如果您有特定的计划希望豁免暂停，请联系您的 Palantir 代表并提供计划 RID。

## 删除计划

要删除计划：

1. 在数据沿袭中导航到计划，并选择计划上的**编辑**按钮。
2. 要删除计划，请选择右上角的回收站图标。

   ![schedules-page-delete]

[actions-menu-manage-schedules]: ../../foundry-docs/building-pipelines/media/actions-menu-manage-schedules.png

[schedules-page-metrics]: ../../foundry-docs/building-pipelines/media/schedules-page-metrics.png

[schedules-page-edit]: ../../foundry-docs/building-pipelines/media/schedules-page-edit.png

[schedules-page-pause]: ../../foundry-docs/building-pipelines/media/schedules-page-delete-pause-buttons.png

[schedules-page-resume]: ../../foundry-docs/building-pipelines/media/schedules-page-resume.png

[schedules-page-delete]: ../../foundry-docs/building-pipelines/media/schedules-page-delete-pause-buttons.png
