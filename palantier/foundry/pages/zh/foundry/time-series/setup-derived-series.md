---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/setup-derived-series/",
  "title": "设置派生序列",
  "page_id": "setup-derived-series",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/derived-series-overview/",
  "next": "/zh/foundry/time-series/manual-ontology-saving/",
  "scraped_at": "2026-07-13T06:10:57.644010+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 设置派生序列

本页面将指导您创建一个派生序列，用于计算假设的 `Machine` 根对象类型上的机器压力损失。

## 1. 选择一个根对象

在[Quiver](/zh/foundry/quiver/overview/)中，选择相关的对象类型（在本例中为`Machine`），并使用[**对象选择器**](/zh/foundry/quiver/cards-index-objects/#object-selector)卡片从列表中选择一个单独的根对象。下面，我们选择了 `Machine 1` 对象。

![在Quiver中选择一个根对象类型。](/resources/foundry/time-series/derived-series-creation-object-select.png)

## 2. 选择时间序列属性作为输入

在我们的示例中，`Machine` 对象类型有两个时间序列属性（TSPs）：`Inlet pressure` 和 `Outlet pressure`。使用**对象时间序列属性**卡片将您想要的TSP添加到您的Quiver画布中，或直接从对象集卡片中弹出时间序列属性。这些TSP将成为我们在下一步中进行派生序列计算的输入。

:::callout{theme="neutral"}
使用**对象时间序列属性**卡片搜索链接的传感器，而不是使用**链接对象集**卡片进行手动搜索。
:::

![Quiver中的"对象时间序列属性"卡片。](/resources/foundry/time-series/derived-series-add-time-series-1.png)

![代表"Inlet pressure"和"Outlet pressure"属性的两个"时间序列图表"卡片。](/resources/foundry/time-series/derived-series-add-time-series-2.png)

:::callout{theme="neutral"}
原始序列和派生序列都可以用作派生序列的输入。这意味着派生序列逻辑可以嵌套。对派生序列的更改将影响任何下游派生序列的执行。因此，我们建议在应用更改之前测试所有依赖于派生序列的下游工作流。 <br><br>
特别要注意以下更改可能导致下游逻辑中断：

* 输入TSP或传感器对象被删除。
* 在派生序列中引用的输入传感器名称被更改。
* 输入TSP类型从数值更改为分类。
:::

## 3. 应用时间序列变换

Quiver提供了多种时间序列变换，例如导数和滚动平均。了解更多关于[Quiver变换](/zh/foundry/quiver/cards-transform-table-index-timeseries-operations/)。

在我们的示例中，我们将使用**时间序列公式**卡片添加一个变换，以计算`Machine 1`对象的进口和出口压力之间的差异。

![在Quiver中选择"时间序列公式"卡片。](/resources/foundry/time-series/derived-series-time-series-transform.png)

## 4. 将派生序列保存为逻辑资源

从"时间序列公式"卡片配置面板，导航到**派生序列选项**部分并选择**保存派生序列**。将出现一个对话框，引导您将派生序列保存为逻辑资源。

![从"时间序列卡片"配置面板中选择"保存派生序列"。](../../../images/foundry/time-series/derived-series-save-derived-series.png)

:::callout{theme="neutral"}
请务必在**时间序列图表**卡片的右上角选择**时间序列公式**节点以查看保存派生序列的选项。如果您选择图表节点，则不会有保存派生序列的选项。
:::

### 步骤1：配置Ontology保存选项

选择**自动** Ontology保存以将派生序列直接保存到Ontology。

选择将绑定到派生序列的对象类型。这可以是您创建派生序列逻辑的[根对象类型](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-object-type)，或者其任何[链接的传感器对象类型](/zh/foundry/time-series/time-series-concepts-glossary/#sensor-object-type)。此绑定对象类型是派生序列可以解析的唯一对象类型。保存后您将无法更改绑定对象类型。

:::callout{theme="neutral"}
自动Ontology保存仅支持传感器对象类型。请遵循[手动Ontology保存步骤](/zh/foundry/time-series/manual-ontology-saving/)以应用于根对象类型的派生序列。您可以选择在创建后配置自动Ontology保存；但是，您将无法更改所选对象类型。
:::

![“保存派生序列”对话框的“Ontology”选项卡。](../../../images/foundry/time-series/derived-series-create-dialog-1a.png)

继续通过配置范围、操作类型和非必填属性值部分来设置自动Ontology保存。

\*\*范围选择：\*\*此部分允许您选择要为其保存此派生序列的根对象。将为每个选定的根对象创建一个传感器对象。目前，范围选择限制为5000个对象。

\*\*操作类型选择：\*\*自动Ontology保存利用操作将派生序列保存到Ontology。为此，您必须为对象类型配置`Create object`、`Modify object`和`Delete object`操作类型。了解更多关于为自动Ontology保存设置操作类型的信息，请参阅[派生序列要求](/zh/foundry/time-series/derived-series-overview/#automatic-ontology-saving-requirements)文档。

\*\*属性映射：\*\*为传感器对象属性提供值。这些值将在所有创建的传感器对象中使用。目前，仅支持字符串或布尔值。

![“保存派生序列”对话框的“Ontology”选项卡。](../../../images/foundry/time-series/derived-series-create-dialog-1b.png)

有关存储派生序列的指导，请查阅时间序列[Ontology设置文档](/zh/foundry/time-series/time-series-overview/#store-time-series-in-the-ontology)。

### 步骤2：选择资源位置

选择名称、描述和文件夹位置以保存生成的派生序列资源。

![“保存派生序列”对话框的“资源文件”选项卡。](../../../images/foundry/time-series/derived-series-create-dialog-2.png)

### 步骤3：审查

最后，在保存之前审查Ontology输出和资源位置信息。

:::callout{theme="neutral"}
在删除派生序列资源之前，首先移除Ontology选项，然后从[派生序列管理界面](/zh/foundry/time-series/manage-derived-series/)保存并部署更改。
:::

![“保存派生序列”对话框的“审查”选项卡。](../../../images/foundry/time-series/derived-series-create-dialog-3.png)

保存派生序列后，任何未来的更改都必须从[派生序列管理页面](/zh/foundry/time-series/manage-derived-series/)进行。
