---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/management-color-groups/",
  "title": "颜色组",
  "page_id": "management-color-groups",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/management-file-tree/",
  "next": "/zh/foundry/pipeline-builder/management-checkpoints/",
  "scraped_at": "2026-07-13T05:52:50.516337+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 颜色组

在Pipeline Builder中，您可以使用节点颜色组来更好地组织和管理您的管道。颜色组可以帮助识别节点并提高图形的可读性。颜色组也可以被折叠或隐藏，以简化图形视图并清理您的管道可视化。

![Pipeline Builder中八种不同颜色组的示例。](../../../images/foundry/pipeline-builder/color-groups.png)

在Pipeline Builder中，管道通常按颜色分组，可以是垂直或水平的。当划分为垂直部分时，颜色可以清晰地区分从原始输入到ontology输出的不同集成阶段。

水平划分时，颜色可以用于分组单个Object或几个紧密相关的Object的上游谱系。

在下面的示例中，颜色组既垂直又水平划分：垂直划分以分隔原始输入的迭代阶段，水平划分以分组管道的Object输出。

![两个不同垂直输入颜色组和八个不同水平输出颜色组的示例。](../../../images/foundry/pipeline-builder/color-groups-graph.png)

## 创建并添加到颜色组

要创建新的颜色组，请在图形右上角的图例中选择**添加颜色**。然后，设置组的名称和颜色。
要将节点添加到组中，右键单击节点并选择**颜色节点**。然后，选择您创建的组以添加所选节点。

![Pipeline Builder中图例的视图和添加颜色及创建颜色组的按钮。](../../../images/foundry/pipeline-builder/add-color-group.png)

您还可以直接在图形上创建新的颜色组。选择您要分组的节点，然后右键单击并选择**颜色节点 > 新颜色**。

![一个节点，菜单打开以指派到颜色组。](../../../images/foundry/pipeline-builder/add-node-to-color-group.png)

## 折叠和展开颜色组

您可以选择将颜色组折叠为单个组节点，以简化您的图形视图。如果您未在给定颜色组内的节点中积极工作，此选项特别有用。

要折叠颜色组，右键单击颜色组中的任意节点并选择**折叠颜色**。或者，使用图形右上角的**折叠颜色**菜单（在图例旁边），并选择您要折叠的组。

![折叠颜色菜单已展开，显示在图形上折叠的几个颜色组。](../../../images/foundry/pipeline-builder/collapse-color-group.png)

要展开组，右键单击组节点并选择**展开颜色**，或者双击已折叠的组节点。

![一个包含十四个节点的航空摄影颜色节点示例。](../../../images/foundry/pipeline-builder/collapsed-color-group-example.png)

## 显示和隐藏颜色组

您可以选择隐藏单个颜色组或隐藏所有其他颜色组，以简化图形视图。要隐藏颜色，请转到颜色**图例**并选择您选择的颜色旁边的眼睛图标。有关更多详细信息，请参见[显示和隐藏颜色组](/zh/foundry/pipeline-builder/management-show-hide-nodes/#show-and-hide-color-groups)。

![颜色图例和眼睛图标的示例。](../../../images/foundry/pipeline-builder/color-legend.png)

## 修改颜色组

### 从颜色组中移除节点

要从颜色组中移除节点，右键单击节点，选择**颜色节点**，然后选择组名称。

![节点及其菜单已展开以从航空摄影颜色组中移除。](../../../images/foundry/pipeline-builder/remove-node-from-color-group.png)

### 编辑或删除节点组

要编辑颜色组，请在图例中将鼠标悬停在组名称上时选择铅笔图标。您可以选择重命名、更改颜色或删除该组。

![使用图例编辑颜色节点名称的示例。](../../../images/foundry/pipeline-builder/edit-color-group.png)

### 选择颜色组中的节点

要选择颜色组内的所有节点，请在图例中选择组名称。

![使用图例选择航空摄影颜色组中所有节点的示例。](../../../images/foundry/pipeline-builder/select-color-group-nodes.png)

### 查看节点组的更改

当[提交管道更改提案](/zh/foundry/pipeline-builder/branches-approve-a-change/)时，任何受更改影响的颜色组将被标记为不同的颜色边框。

![将影响颜色节点内节点的管道提案。节点的边框是橙色的。](../../../images/foundry/pipeline-builder/color-group-proposal.png)

选择**查看更改**以查看颜色组内的节点。任何有提议更改的单个节点将被突出显示。

![颜色组的扩展视图，提案影响的节点以橙色突出显示。](../../../images/foundry/pipeline-builder/color-group-nodes-proposal.png)

选择**返回到管道图形**以返回到主要提案更改视图。
