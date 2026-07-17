---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/management-show-hide-nodes/",
  "title": "显示和隐藏节点",
  "page_id": "management-show-hide-nodes",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/management-create-custom-functions/",
  "next": "/zh/foundry/pipeline-builder/management-file-tree/",
  "scraped_at": "2026-07-13T05:50:19.730712+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 显示和隐藏节点

为了高效管理大型数据管道，用户可以通过显示和隐藏节点来专注于数据管道的子部分。这可以更快地识别数据管道段并改善导航和编辑体验。

在图形视图中手动选择节点，或者通过选择左上角的区域选择图标使用**拖动选择模式**。

![Pipeline Builder中的区域选择图标。](../../../images/foundry/pipeline-builder/show-hide-selection.png)

选择相关节点后，右键点击并选择**隐藏节点**。这将为您提供**隐藏选定节点**或**隐藏其他节点**的选项，后者会隐藏所有未选定的节点。

![在数据管道中选择的青色节点示例，将被隐藏。](../../../images/foundry/pipeline-builder/show-hide-selected-nodes.png)

连接的节点之间会出现虚线，连接的圆形图标会从实心变为局部填充，以指示隐藏的节点，如下图所示：

![数据管道中隐藏节点的示例。](../../../images/foundry/pipeline-builder/show-hide-teal-hidden.png)

下图仅显示青色节点，所有其他节点都被隐藏：

![仅显示青色节点的数据管道示例。](../../../images/foundry/pipeline-builder/show-hide-only-teal.png)

## 显示和隐藏颜色组

您可以隐藏一个颜色组，或隐藏所有其他颜色组，以简化图形视图。要隐藏颜色组，请转到颜色**图例**，然后选择您选择的颜色旁边的眼睛图标。

![颜色图例和眼睛图标的示例。](../../../images/foundry/pipeline-builder/color-legend.png)

选择**隐藏此颜色**仅隐藏选定颜色组，或选择**隐藏其他颜色**以隐藏所有其他颜色组。

![颜色图例显示隐藏此颜色或隐藏其他颜色。](../../../images/foundry/pipeline-builder/color-legend-hide-this-color.png)

当颜色组被隐藏时，连接节点之间会出现虚线以通知用户隐藏的节点。要查看输入节点的隐藏数量，请在选定节点上选择左箭头，然后选择**显示节点输入**。**显示节点输入**旁边的数字是隐藏输入的数量。

![显示节点输入的弹出窗口。](../../../images/foundry/pipeline-builder/color-show-hidden-inputs.png)

在**图例**下选择**显示x个隐藏节点**以显示所有隐藏节点。X是隐藏节点的总数。颜色图例显示每个颜色组中的节点数量以及是否被隐藏。

![颜色图例下的按钮显示隐藏节点的数量。](../../../images/foundry/pipeline-builder/color-total-hidden-nodes.png)

## 在其他标签中显示和隐藏节点

您还可以在**变更**标签下的**提案**选项卡中显示和隐藏节点。选择**图例**以显示颜色组，并使用上述相同的方法显示或隐藏它们。

![变更视图中的显示隐藏功能](../../../images/foundry/pipeline-builder/show-hide-changes-view-with-legend.png)

当存在合并冲突时，您还可以在**解决变更**选项卡中显示和隐藏节点。

![解决变更视图中的显示隐藏功能](../../../images/foundry/pipeline-builder/show-hide-resolve-changes.png)
