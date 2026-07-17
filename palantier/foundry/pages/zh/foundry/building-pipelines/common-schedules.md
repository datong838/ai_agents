---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/common-schedules/",
  "title": "常见调度配置",
  "page_id": "common-schedules",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/find-manage-schedules/",
  "next": "/zh/foundry/building-pipelines/triggers-reference/",
  "scraped_at": "2026-07-13T05:41:54.847560+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 常见调度配置

从一些常见的调度示例开始：

* [定期搭建数据集](#build-datasets-regularly)
* [在新数据可用时搭建数据集](#build-datasets-when-new-data-is-available)
* [高级（多重）触发器配置](#advanced-multiple-trigger-configurations)
* [仅当父数据集已更新时在特定时间更新数据集](#update-a-dataset-at-a-specific-time-only-if-its-parent-has-been-updated)

## 定期搭建数据集

在此示例中，我们希望**raw\_taxi (cleaned)**在每个工作日上午9点更新，并且我们希望不仅搭建**raw\_taxi (cleaned)**，还搭建其所有上游依赖项。我们应该按以下方式配置我们的调度：

![image-time-based-full-page]

## 在新数据可用时搭建数据集

在此示例中，我们希望调度在另一个数据集更新时运行。我们可以使用与上一节相同的配置，只需一个小的修改。应该选择一个[事件触发器](/zh/foundry/building-pipelines/triggers-reference/#event-trigger)，选择您希望在图中触发更新的数据集。

![when-datasets-update]

有关基于事件的调度的更多详细信息，请参阅[事件触发器](/zh/foundry/building-pipelines/triggers-reference/#event-trigger)文档。

## 高级（多重）触发器配置

![image-of-any-trigger-config]
![image-of-or-trigger-config]

在此示例中，我们希望**数据集D**在每天上午9点更新，同时在其依赖的数据集**父A**发生更改时也更新。根据[复合触发器组合表](/zh/foundry/building-pipelines/triggers-reference/#compound-trigger)，如果我们通过OR将基于时间的触发器与基于事件的触发器结合，数据集将在时间T时搭建，并在事件E发生时搭建。因此，我们将要调度搭建的数据集设置为**数据集D**，并添加一个上午9点的基于时间的触发器和一个监视**父A**上任何更新的基于事件的触发器。选择“任一触发器”或高级配置并在条件之间添加OR在此情况下是等效的。

## 仅当父数据集已更新时在特定时间更新数据集

![image-of-all-trigger-config]
![image-of-and-trigger-config]

在此示例中，我们希望**数据集D**在每天上午9点更新，但仅当其依赖的数据集**父A**发生更改时。根据[复合触发器组合表](/zh/foundry/building-pipelines/triggers-reference/#compound-trigger)，如果我们通过AND将基于时间的触发器与基于事件的触发器结合，数据集将在时间T时搭建*如果*事件E先前已发生。因此，我们将要调度搭建的数据集设置为**数据集D**，并添加一个上午9点的基于时间的触发器和一个监视**父A**上任何更新的基于事件的触发器。选择“所有触发器”或高级配置并在条件之间添加AND在此情况下是等效的。

:::callout{theme="neutral"}
此配置不限制**父A**更新的时间窗口。无论是在当天上午8:55更新还是在前一天上午9:10更新，基于事件的触发器将在上午9点评估为TRUE，导致所有条件被满足并运行调度。这意味着如果**父A**在上午9点*之后*持续更新，例如每天上午9:10更新，那么**数据集D**将在每天上午9点搭建，使用**父A**的数据，该数据是23小时50分钟前的数据。
:::

[image-time-based-full-page]: ../../foundry-docs/building-pipelines/media/time-based-full-page.png

[when-datasets-update]: ../../foundry-docs/building-pipelines/media/when-datasets-update.png

[image-of-all-trigger-config]: ../../foundry-docs/building-pipelines/media/T1_AND_E1.png

[image-of-and-trigger-config]: ../../foundry-docs/building-pipelines/media/T1_AND_E1_advanced.png

[image-of-or-trigger-config]: ../../foundry-docs/building-pipelines/media/T1_OR_E1_advanced.png

[image-of-any-trigger-config]: ../../foundry-docs/building-pipelines/media/T1_OR_E1.png
