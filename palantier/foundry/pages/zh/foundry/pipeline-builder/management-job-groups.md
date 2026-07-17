---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/management-job-groups/",
  "title": "任务组",
  "page_id": "management-job-groups",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/management-checkpoints/",
  "next": "/zh/foundry/pipeline-builder/export-pipeline/",
  "scraped_at": "2026-07-13T05:50:48.910926+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 任务组

在 Pipeline Builder 中，每次成功部署都会启动一个单独的搭建。默认情况下，每个批处理管道输出都作为其自己的任务进行搭建，这些任务将独立成功或失败。在流式管道中，所有输出都捆绑在单个任务中运行于一个 Flink 集群上，因此所有输出流要么一起成功，要么一起失败。

Pipeline Builder 中的任务分组允许您在批处理管道中将输出捆绑为一个任务，或在流式管道中将每个输出拆分为其自己的任务。您还可以为每个任务分组指定计算配置文件，以便对输出的搭建方式进行细粒度控制。

将输出分组为单个任务在您希望输出逻辑并行更新时非常有用。在批处理管道中，输出必须放置在同一任务组中，以通过检查点有效地计算共享逻辑。了解更多关于 Pipeline Builder 中的[检查点](/zh/foundry/pipeline-builder/management-checkpoints/)。

将输出划分为较小的组或单输出任务在您希望输出独立于其他输出运行时很有帮助。请记住，流式管道中的每个任务组将需要其自己的 Flink 集群，这将增加计算成本。

:::callout{theme="warning"}
在流式或增量管道中移动任务组之间的输出被视为重大更改，并将触发强制重播。了解更多关于 Pipeline Builder 中的[重大更改](/zh/foundry/pipeline-builder/breaking-changes/)。
:::

## 指派任务组

要指派任务组，请右键单击 Pipeline Builder 图中的任何输出节点以打开上下文菜单。然后，将鼠标悬停在 **指派任务组** 上。在批处理管道中，输出将默认为单个任务。在流式管道中，输出将默认为一个任务组。

**批处理视图** | **流式视图**
\--------       |------------------
![批处理管道节点菜单视图](../../../images/foundry/pipeline-builder/assign-job-group-batch.png) | ![流式管道节点菜单视图。](../../../images/foundry/pipeline-builder/assign-job-group-stream.png)

选择 **新建组** 以将输出指派到新的任务组。一个 **搭建设置** 面板将在右侧打开，并自动为任务组指派颜色，以便在图中轻松识别。

**批处理视图** | **流式视图**
\------         |------------------
![批处理管道中的搭建设置面板视图](../../../images/foundry/pipeline-builder/build-settings-batch.png) | ![流式管道中的搭建设置面板视图。](../../../images/foundry/pipeline-builder/build-settings-stream.png)

继续编辑其他输出以将它们添加到现有或新建的任务组中。或者，使用侧面板将输出移动到新组。

![在搭建设置面板中将任务移动到组。](../../../images/foundry/pipeline-builder/move-to-group.png)

默认计算配置文件显示在面板顶部。要为每个任务组添加自定义配置文件，请在每个组的标题中选择 **添加配置文件**。在下面的示例中，默认计算配置文件为 `Small`，但组1配置为 `Medium` 计算配置文件。

![在搭建设置面板中配置其他计算配置文件。](../../../images/foundry/pipeline-builder/add-compute-profiles.png)

创建任务组后，选择面板右上角的 **应用** 以保存更改。

![搭建设置面板顶部的应用按钮。](../../../images/foundry/pipeline-builder/apply-job-groups.png)

您现在可以部署您的管道了。

## 任务分组和权限标记

:::callout{theme="neutral"}
在一个任务组中，所有输入的权限标记将被同一任务组内的所有输出继承，即使输出未直接连接到被标记的输入。了解更多关于[权限标记继承](/zh/foundry/security/markings/#inheritance)。
:::

在以下示例中，**Input\_A** 有权限标记，而 **Input\_B** 没有。**Output\_X** 和 **Output\_Y** 位于同一任务组中。尽管 **Output\_Y** 未直接连接到 **Input\_A**，但在部署时将继承 **Input\_A** 的所有权限标记。

![搭建设置面板顶部的应用按钮。](../../../images/foundry/pipeline-builder/job-groups-markings.png)

如果您不希望在 **Output\_Y** 上保留权限标记，可以[预先移除任务分组继承的权限标记](/zh/foundry/pipeline-builder/outputs-remove-markings-and-organizations/)。
