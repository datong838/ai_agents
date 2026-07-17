---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/time-series-properties-use-case-operational/",
  "title": "在 Workshop 模块和 Quiver 分析中使用时间序列属性",
  "page_id": "time-series-properties-use-case-operational",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/time-series-properties-use-case-ontology/",
  "next": "/zh/foundry/time-series/sensor-object-end-to-end/",
  "scraped_at": "2026-07-13T06:18:18.963820+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在 Workshop 模块和 Quiver 分析中使用时间序列属性

本示例中构建的 Workshop 模块（**\[示例] 对象上的时间序列属性 | 延迟 TSP**）基于参考Ontology中的航空Ontology构建，您的账户中可能并未提供此Ontology。有关这些Object之间关系的更多信息，请参阅[应用案例概述](/zh/foundry/time-series/time-series-properties-use-case/)。本示例模块将作为您使用时间序列属性配置自己的 Workshop 模块的参考。

## 在 Workshop 中选择对象

模块的**选择对象**部分包含两个标准的 Workshop 微件功能。下面简要描述了微件的功能，您可以在我们的[文档](/zh/foundry/workshop/overview/)中了解 Workshop 的一般功能。按照以下步骤在将时间序列属性添加到模块之前配置这些微件。

### 第 I 部分：添加筛选列表微件

[筛选微件](/zh/foundry/workshop/widgets-filter-list/)应获取 `Flight` 对象集并基于 `Airport` 属性应用筛选。筛选微件应输出一个 `Airport` 筛选，可用于 Object 表微件中。

1. 在您的 Workshop 模块中，选择 **+ 添加微件**，然后选择筛选列表微件。
2. 在筛选列表微件的右侧配置中，为 **对象集输入** 创建一个新变量，并命名为 "All airports"。**起始对象集**应使用 `[Example] Airport` 对象类型。

![筛选列表微件输入变量的配置](../../../images/foundry/time-series/time-series-properties-workshop-filter-input.png)

3. 通过选择 **+ 添加筛选**按钮，添加 `Airport`、`Complete Flight History`、`Airport State Name`、`Arriving Flight Count` 和 `Departing Flight Count` 属性。

![筛选列表微件列选择配置](../../../images/foundry/time-series/time-series-properties-workshop-filter-column.png)

4. 向下移动到**筛选输出**字段，您将看到一个筛选输出已为您创建。为其赋予一个描述性名称，如“airport filter”；无需其他配置。

### 第 II 部分：添加对象表微件

[对象表微件](/zh/foundry/workshop/widgets-object-table/)将使用户能够在对象集上进行筛选并选择一个机场进行进一步调查。

1. 在您的 Workshop 模块中，选择 **+ 添加微件**，然后选择对象表微件。
2. 在**输入数据**部分，创建一个新变量并命名为“filtered airports”。在**起始对象集**下，选择 **现有对象集变量**以 `all airports`。

![对象表微件选择筛选后的变量作为输入](../../../images/foundry/time-series/time-series-properties-workshop-object-filtered-airports-select-existing.png)

3. 在**筛选...** 部分，选择 **使用变量**并选择我们创建为筛选列表微件输出的 `airport_filter` 变量。

![对象表微件选择筛选器和创建输入](../../../images/foundry/time-series/time-series-properties-workshop-filter-input.png)

4. 在**列配置**中，通过选择 **+ 添加列**，添加 `Title`、`Daily Avg Arr Delay`、`Daily Avg Dep Delay` 和 `Daily count of flights` 列。

5. 将**默认排序**配置为一个属性，并选择**选择属性以进行排序**。然后，选择 `Arriving Flight Count`。

![对象表微件默认排序配置](../../../images/foundry/time-series/time-series-properties-workshop-object-view-sort.png)

6. 在对象表配置的**选择**部分中设置所选表的输出。配置输出以对所选机场的时间序列属性进行分析。

![对象表微件选定对象输出配置](../../../images/foundry/time-series/time-series-properties-workshop-object-view-selected-object.png)

## Workshop 中的 TSPs

模块的**Workshop 中的 TSPs**部分使用可用的[Workshop 中的时间序列变换](/zh/foundry/workshop/time-series-properties/)。按照以下说明设置仪表盘中显示的图表 XY 和指标卡微件。

![在 Workshop 中配置的图表 XY 和指标卡微件](../../../images/foundry/time-series/time-series-properties-workshop-widgets.png)

### 第 I 部分：添加图表 XY 微件

1. 在您的 Workshop 模块中，选择 **+ 添加微件**，然后选择图表 XY 微件。
2. 在右侧的配置菜单中，选择添加一个图层。

![图表 XY 微件配置以向图表添加图层](../../../images/foundry/time-series/time-series-properties-workshop-chartXY-add-plot-layer.png)

3. 在菜单中选择图层，将数据输入配置为**时间序列集**。
4. 创建一个包含 `daily count of flights for selected airport` 时间序列属性的新变量，其中所选机场是来自对象表微件的输出变量。请确保为您的新变量赋予一个易于理解的名称。

![图表 XY 微件的第一个图层配置。](../../../images/foundry/time-series/time-series-properties-workshop-chartXY.png)

5. 为 `daily dep delay for selected airport` TSP 添加另一个图层和变量。
6. 为 `Weekly Avg Dep delay` 属性添加第三个图层。这次，在设置时间序列集变量时，选择还要添加一个变换。在变换中，选择 **Rolling**，然后选择 **Average**，聚合方法为 1 周。请确保为您的新变量赋予一个易于理解的名称。

![图表 XY 微件的第三个图层配置。](../../../images/foundry/time-series/time-series-properties-workshop-chartxy-third-layer.png)

7. 确保轴设置正确，以便每个图层都有一个轴。您还可以选择每个图层的轴单位显示位置（在图表的左侧或右侧）。

![Workshop 中图表 XY 微件的 Y 轴配置。](../../../images/foundry/time-series/time-series-properties-workshop-chart-xy-axes.png)

### 第 II 部分：在图表 XY 微件旁添加指标卡

1. 添加一个 [指标卡微件](/zh/foundry/workshop/widgets-metric-card/)。
2. 在配置菜单中，选择 **添加指标**或使用首次添加微件时创建的默认指标。然后，将鼠标悬停在指标上以打开进一步的配置选项，并选择 **Number** 作为值类型。

![Workshop 指标卡微件，您可以在其中选择指标进行配置](../../../images/foundry/time-series/time-series-properties-workshop-hover-metric.png)

3. 选择 **选择数值...**，将鼠标悬停在 **新数值变量** 上，然后选择 **时间序列**。
4. 选择您在设置图表 XY 微件的第三个图层时创建的 `Max weekly average departure delay` 变量。
5. 选择 **Max** 聚合类型，在 **All time** 时间范围内作为单值指标。请确保为您的新变量赋予一个易于理解的名称。
6. 根据需要设置数字格式。

![Workshop 指标卡微件配置](../../../images/foundry/time-series/time-series-properties-metric-card.png)

## Quiver 中的 TSPs

以下指导假设对 Quiver 的基本导航知识。如需了解有关 Quiver 一般功能的更多信息，请查看[我们的文档](/zh/foundry/quiver/getting-started/)。

示例 Workshop 模块的**Quiver 中的 TSPs**部分包含一个[嵌入的 Quiver 仪表盘](/zh/foundry/quiver/dashboards-overview/)。此 Quiver 仪表盘执行与[上述 Workshop 微件](#tsps-in-workshop)相同的计算。按照以下说明设置仪表盘中显示的时间序列图和指标卡。

一旦以下步骤完成，分析图和生成的仪表盘应如下例所示：

![Quiver 分析图视图](/resources/foundry/time-series/time-series-properties-quiver-graph.png)

![Quiver 仪表盘视图](../../../images/foundry/time-series/time-series-properties-quiver-dashboard.png)

### 第 I 部分：在 Quiver 分析中设置时间序列比较

1. 通过选择顶部菜单栏中的 **Objects**，使用 `Airport` 对象类型创建一个[新的 Quiver 分析](/zh/foundry/quiver/getting-started/)。
2. 通过选择顶部菜单栏中的 **搜索卡片**，然后搜索“对象选择器”，添加一个 [对象选择器卡片](/zh/foundry/quiver/cards-index-objects/#object-selector)，并选择 `Airport` 对象类型。因为您已经选择了 `Airport` 对象类型集，对象选择器卡片将自动应用于 `Airport` 对象。

![Quiver 选择对象选择器卡片](/resources/foundry/time-series/time-series-properties-quiver-select-object-selector.png)

3. 通过选择 **搜索卡片**，或者在对象选择器卡片底部悬停直到搜索栏出现，添加一个对象时间序列属性卡片。搜索“对象时间序列属性”，然后将其添加到分析中。

![选择对象时间序列属性卡片](/resources/foundry/time-series/time-series-properties-quiver-object-tsp-card.png)

4. 通过选择绘图名称旁边的齿轮图标来配置卡片，然后从卡片中选择每日平均出发延迟 TSP。

![Quiver 对象时间序列属性卡片配置](/resources/foundry/time-series/time-series-properties-quiver-object-tsp-configuration.png)

5. 使用右上角的下拉菜单，选择 **Graph** 以进入分析的图形视图。

![查看模式下拉菜单以导航到图形模式](../../../images/foundry/time-series/time-series-properties-quiver-toggle-graph.png)

注意，通过添加对象时间序列属性卡片，还生成了一个时间序列图表卡片和默认共享时间轴卡片。

![Quiver 生成的图形模式](../../../images/foundry/time-series/time-series-properties-quiver-generated-graph.png)

6. 选择 **搜索卡片** 或在对象时间序列属性卡片上悬停直到菜单出现。选择搜索按钮并搜索“滚动聚合”以将滚动聚合卡片添加到画布。

7. 从卡片右上角的设置菜单中，选择 **Average**，值为 7，表示每 1 周。注意，这生成了一个新的时间序列图表卡片。

![Quiver 滚动聚合卡片配置](../../../images/foundry/time-series/time-series-properties-quiver-rolling-aggregate.png)

8. 选择 **搜索卡片** 或在滚动聚合卡片上悬停直到菜单出现，并搜索“数值聚合”以将时间序列数值聚合卡片添加到画布。选择 **Maximum** 作为聚合类型。这代表了特定机场（在本例中为 `The Eastern Iowa Airport`）在滚动周期间的最大延迟分钟数。

![Quiver 时间序列数值聚合](../../../images/foundry/time-series/time-series-properties-quiver-numeric-aggregation.png)

9. 返回到画布模式。在左侧的**分析内容**部分，单击并拖动滚动聚合到您刚创建的时间序列图表中。

![将滚动聚合卡片拖入时间序列图表中。](/resources/foundry/time-series/time-series-properties-quiver-drag-plot.png)

10. 在包含滚动周聚合和机场平均出发延迟的时间序列图表上选择 **添加到新仪表盘**。

![Quiver 将绘图添加到仪表盘](/resources/foundry/time-series/time-series-properties-quiver-add-dashboard.png)

11. 从步骤 8 重新开始，添加另一个时间序列数值聚合，代表 Eastern Iowa Airport 在滚动周期间的最大延迟分钟数。将其添加到新的 Quiver 仪表盘中。

### 第 II 部分：设置 Quiver 仪表盘对象输入

1. 使用左侧边栏中的仪表盘图标打开您的仪表盘。您可以重命名部分和图表。例如，时间序列图表可以命名为“平均出发延迟与滚动聚合叠加”，数值聚合图表可以命名为“最大滚动平均延迟”。

2. 在右侧配置菜单中的**输入**部分，添加来自 `Airport` 对象集的对象选择变量。

![Quiver 仪表盘输入](../../../images/foundry/time-series/time-series-properties-quiver-dashboard-input.png)。

### 第 III 部分（非必填）：添加起始和结束时间戳

1. 从 Quiver 仪表盘菜单的左上角选择 **退出仪表盘**，然后导航到图形模式。

![退出 Quiver 仪表盘](/resources/foundry/time-series/time-series-properties-quiver-exit-dashboard.png)

2. 使用顶部横幅中的 **搜索卡片** 功能，添加两个日期/时间参数和一个时间范围参数卡片。切换 **选择单独的开始和结束日期参数** 选项，然后从下拉菜单中选择日期/时间参数（在我们的例子中，参数称为“开始时间”和“结束时间”）。

![时间范围参数卡片](/resources/foundry/time-series/time-series-properties-quiver-time-range-parameter.png)

3. 导航到默认共享时间轴，并从右上角的选项中选择 **配置**。

![配置共享轴](/resources/foundry/time-series/time-series-properties-quiver-configure-axis-cog.png)

4. 切换选项以添加 **受控** 时间范围，然后添加时间范围参数。确保 **更新时重新启用轴自动缩放** 也被切换为打开。

![将时间范围参数添加到共享轴](/resources/foundry/time-series/time-series-properties-configure-shared-axis.png)

5. 返回到您的仪表盘并将开始和结束时间作为输入添加到仪表盘中。仪表盘完成后，[发布仪表盘](/zh/foundry/quiver/dashboards-publish-share/)。

![Quiver 时间范围输入](/resources/foundry/time-series/time-series-properties-quiver-time-range-input.png)

### 第 IV 部分：在 Workshop 中嵌入您的仪表盘

1. 如果您创建了非必填的开始和结束时间输入，您必须在 Workshop 中添加两个[日期和时间选择器微件](/zh/foundry/workshop/widgets-date-time-picker/)。
2. 添加一个 Quiver 仪表盘微件，然后选择您的新仪表盘。
3. 选择适当的 Workshop 变量作为 Quiver 输入。

![Quiver 仪表盘微件输入在 Workshop 中](/resources/foundry/time-series/time-series-properties-workshop-inputs.png)
