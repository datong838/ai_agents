---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/sensor-object-end-to-end-operational/",
  "title": "在 Workshop 和 Quiver 中使用传感器对象类型的时间序列数据",
  "page_id": "sensor-object-end-to-end-operational",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/sensor-object-end-to-end-ontology/",
  "next": "/zh/foundry/time-series/compute-usage/",
  "scraped_at": "2026-07-13T06:24:12.641957+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在 Workshop 和 Quiver 中使用传感器对象类型的时间序列数据

要开始使用传感器对象类型的时间序列数据，请在 Workshop 中打开 **航班传感器数据** 模块。您可以使用平台的 [快速搜索](/zh/foundry/getting-started/quicksearch/) 功能找到该模块。此示例模块将为您配置自己的 Workshop 模块提供参考，使用传感器对象类型的时间序列数据。

在本指南结束时，我们的模块将使您能够以起飞时间和机场筛选航班。从那里，[对象表微件](/zh/foundry/workshop/widgets-object-table/) 将显示您可以选择查看关联的传感器对象时间序列数据的航班列表。

![使用传感器对象时间序列数据的示例 Workshop 模块](../../../images/foundry/time-series/sensor-object-workshop-module-overview.png)

## 第 I 部分：在 Workshop 模块中设置初始微件

模块的 [地图](/zh/foundry/workshop/widgets-map/)、[对象表](/zh/foundry/workshop/widgets-object-table/) 和 [筛选](/zh/foundry/workshop/widgets-filter-list/) 微件是标准的 Workshop 功能。请按照以下步骤配置这些微件，然后再将时间序列特定的微件添加到模块中。

### 按航线 ID 筛选航班

[筛选列表微件](/zh/foundry/workshop/widgets-filter-list/) 应获取 `Flight` 对象集，并基于 `route id` 应用筛选。

1. 在您的 Workshop 模块中，选择 **+ 添加微件**，然后选择筛选列表微件。
2. 在筛选列表微件的右侧配置中，为 **对象集输入** 创建一个新变量，并将其命名为 "按航线 ID 筛选航班"。**起始对象集** 应使用 `Flights with linked flight sensors` 对象类型变量。

![筛选列表微件输入变量](../../../images/foundry/time-series/sensor-object-workshop-filter-list-variable.png)

3. 通过选择 **+ 添加筛选** 添加 `Route Id` 属性。
4. 向下移动到 **筛选输出** 字段，以找到已为您创建的筛选输出。给它一个描述性的名称，例如 "按航线 ID 筛选的航班"；无需其他配置。

![筛选列表微件输出变量](../../../images/foundry/time-series/sensor-object-workshop-filter-list-output.png)

### 配置对象表微件以选择航班进行比较

1. 在您的 Workshop 模块中，选择 **+ 添加微件**，然后选择对象表微件。
2. 在右侧的配置面板中的 **输入数据** 下拉菜单中，选择 **+ 新建对象集变量**。
3. 将变量命名为 `按航线 ID 筛选的航班`。
4. 选择 **起始对象集** 并选择现有变量 `Flights with linked flight sensors`。
5. 选择筛选器 **使用变量**，并选择 `Filter by route` 变量。

![对象表微件输入变量](../../../images/foundry/time-series/sensor-object-workshop-table-input.png)

6. 选择 **+ 添加列**，然后从下拉菜单中选择 **起飞时间戳**。
7. 向下滚动到 **选择** 部分并打开 **启用活动选择** 选项。这将配置表中所选对象的输出。
8. 从 **活动对象** 下拉菜单中选择 **新建对象集变量**，创建一个新变量。将变量重命名为 `表 1 中的选定航班`。无需其他配置。

![对象表微件输出变量](../../../images/foundry/time-series/sensor-object-workshop-table-widget-output.png)

9. 对于第二个表微件重复此过程，接收您在步骤 3-5 中创建的 `按航线 ID 筛选的航班`，并创建一个输出变量，命名为 `表 2 中的选定航班`。

## 第 II 部分：从根对象类型添加传感器对象类型的时间序列数据

### 创建传感器名称选择器

创建一个所需系列名称的下拉菜单，以传递到您将在后续步骤中创建的 Quiver 仪表盘中。

1. 在您的 Workshop 模块中，选择 **+ 添加微件**，然后选择字符串选择器微件。
2. 在微件配置面板中，选择 **选项生成** 下的 **+ 添加选择器选项**。
3. 添加 `heading`、`vertical_speed`、`speed` 以及您希望显示的任何其他传感器名称的选项。

![传感器名称字符串选择器微件配置](../../../images/foundry/time-series/sensor-object-workshop-sensor-name-select.png)

4. 在 **选择** 部分的下拉菜单中，选择 `选定的系列名称` 变量。
5. 在 **选择显示** 配置中保持默认的 **下拉菜单** 选项。

![传感器名称字符串选择器输出](../../../images/foundry/time-series/sensor-object-workshop-sensor-name-selection-output.png)

### 创建航班 ID 变量

现在，您将创建两个变量，分别表示从左右表中选定的航班的航班 ID。每个变量都是由对象表微件中配置的 `表 1 中的选定航班` 和 `表 2 中的选定航班` 变量的 `Flight Id` 属性支持的字符串。您将把这些变量传递到 Quiver 仪表盘中。

1. 从 Workshop 模块的左侧导航到 **变量**，并选择 **+** 添加新变量。
2. 从下拉菜单中选择 **字符串**。
3. 从下一个下拉菜单中选择 **对象属性**。

![从对象属性创建新字符串变量](../../../images/foundry/time-series/sensor-object-workshop-create-flight-id-variable.png)

1. 选择 `表中的选定航班` 变量作为带有单一选项的对象集，然后选择 `Flight Id` 作为 `选定航班 ID` 变量的属性。

![航班 ID 变量配置](../../../images/foundry/time-series/sensor-object-workshop-flight-id.png)

## 第 III 部分：创建一个 Quiver 仪表盘

以下指南假设对 Quiver 的基本导航有一定了解。要了解更多关于 Quiver 一般功能的信息，请查阅[我们的文档](/zh/foundry/quiver/getting-started/)。

这个 Workshop 模块包含一个[嵌入的 Quiver 仪表盘](/zh/foundry/quiver/dashboards-overview/)。请按照下面的说明设置仪表盘中显示的时间序列图表和指标卡片。

### 1. 使用 `Flight Sensor` 对象类型创建一个 Quiver 分析

#### 使用航班传感器对象集

通过从顶端菜单栏中选择 **对象** 并搜索 `Flight Sensor` 对象类型，创建一个[新的 Quiver 分析](/zh/foundry/quiver/getting-started/)，并设置 `Flight Sensor` 对象类型。选择 **添加对象集** 将对象集表添加到画布中。

![将对象添加到 Quiver 分析](../../../images/foundry/time-series/sensor-object-quiver-add-objects.png)

![选择航班传感器对象集](../../../images/foundry/time-series/sensor-object-quiver-add-flight-sensor-set.png)

#### 为航班 ID 添加两个字符串参数

1. 从屏幕左侧选择 **(x)** 打开 **参数** 配置。
2. 选择 **+** 添加一个参数，然后从下拉菜单中选择 **字符串**。字符串参数将代表航班 ID，您将使用该 `flight_id` 属性检索 `Flight Sensor` 对象。
3. 将字符串参数重命名为 "航班 ID" 以便于跟踪。
4. 对第二个航班 ID 重复步骤 1-3，并将其标记为 "航班 ID 2"。

![将字符串参数添加到 Quiver 分析](../../../images/foundry/time-series/sensor-object-quiver-text-parameter.png)

#### 为传感器名称添加字符串参数

1. 导航到屏幕的左侧。
2. 选择 **+** 添加一个参数，然后从下拉菜单中选择 **字符串**。字符串参数将代表传感器名称，您将筛选与从 Workshop 模块传递的传感器名称匹配的 `Flight Sensor` 对象。
3. 将字符串参数重命名为 "传感器名称" 以便于跟踪。

#### 为所有参数添加对象集筛选

1. 将鼠标悬停在 `Flight Sensor` 对象集表上以显示 **搜索** 菜单，或选择 **搜索卡片** 以添加筛选对象集卡片。此卡片将根据选定的 `flight id` 筛选传感器对象。查看我们的 [对象集筛选文档](/zh/foundry/quiver/objects-filter/) 以获取更多信息。

![添加对象集筛选卡片](../../../images/foundry/time-series/sensor-object-quiver-filter-object-set-card.png)

2. 通过选择 **添加筛选以限制结果对象集** 添加一个筛选，然后选择 **...where flight id is** 选项。

3. 在下拉菜单中选择 **字符串** 变量，并选择您在上一步中创建的 `Flight Id 1` 字符串参数。

4. 通过选择 **添加筛选以限制结果对象集** 再次添加一个筛选，然后选择 **...where series name is** 选项。

5. 从下拉菜单中选择 **is(exact match)**，然后选择 **字符串** 变量。

6. 选择您之前创建的 `传感器名称` 字符串参数。

![配置筛选对象集卡片](../../../images/foundry/time-series/sensor-object-quiver-filter-cards.png)

#### 添加航班 ID 的分组时间序列图

1. 将鼠标悬停在筛选对象集卡片上以显示 **搜索** 菜单，或选择 **搜索卡片** 以添加分组时间序列图。这将把对象上的所有时间序列属性绘制在图上。在这种情况下，您期望这个分组时间序列图只包含一个传感器对象的一个时间序列。

![分组时间序列卡片](../../../images/foundry/time-series/sensor-object-quiver-grouped-tsp.png)

2. 将鼠标悬停在时间序列图配置上以找到 **配置图表** 图标并打开配置面板。
3. 在 **批量时间序列选项** 下，找到 **时间序列列** 下拉菜单并选择 **默认时间序列属性**。这将确保图表显示的是对象名称而不是系列 ID 列的名称。

![为传感器对象的分组时间序列图选择默认 TSP](../../../images/foundry/time-series/sensor-object-quiver-grouped-time-series-plot-tsp-selection.png)

4. 对为 `Flight Id 2` 参数创建的筛选卡片重复这些步骤。然后您应该有两个单独的分组时间序列图。

![添加第二个分组时间序列卡片](../../../images/foundry/time-series/sensor-object-quiver-grouped-tsp-cards.png)

#### 覆盖图表并添加相对时间偏移

1. 选择分组时间序列图以访问快速操作菜单。
2. 选择 **变换** 并搜索 **相对时间序列** 卡片。

![相对时间序列卡片](../../../images/foundry/time-series/sensor-object-quiver-select-relative-time-series.png)

3. 对第二个分组时间序列图重复操作。
4. 然后，在第二个分组时间序列图中，选择 **配置图表** 选项并导航到配置面板的 **显示** 选项卡。
5. 在 **颜色** 下，选择一种颜色以区分它与前一个图表。在此示例中，选择橙色以优化与蓝色的视觉对比。

![为图表添加对比度](../../../images/foundry/time-series/sensor-object-quiver-relative-time-series-contrast.png)

6. 选择其中一个分组时间序列图并将其拖动到另一个图表上以合并为一个图表。您可能会注意到图表似乎消失了。您需要使图表使用正确的范围才能一起显示。

![相对时间图中缺少的图表](../../../images/foundry/time-series/sensor-object-quiver-relative-time-no-plot.png)

7. 选择 **相对时间序列** 卡片的图表配置。在 **相对时间选项** 下，打开 **使用源范围** 设置。确保 **相对于** 下拉菜单设置为 **开始**。

![带有两个图表的相对时间序列卡片](../../../images/foundry/time-series/sensor-object-quiver-completed-relative-time-series-card.png)

#### 将图表添加到新仪表盘

1. 从左侧的 **仪表盘** 选项卡中选择 **+ 创建新仪表盘**。
2. 通过选择各自卡片的 **添加到新仪表盘** 将时间序列图表添加到仪表盘中。

![添加到仪表盘](../../../images/foundry/time-series/sensor-object-quiver-add-to-dashboard.png)

### 2. 配置新仪表盘

通过选择 **查看仪表盘** 导航到仪表盘，或从屏幕左侧的 **仪表盘** 选项卡中访问它。

![导航到 Quiver 仪表盘](../../../images/foundry/time-series/sensor-object-quiver-dashboard-icon.png)

#### 调整卡片大小并命名

确保对象选择卡片位于仪表盘的顶部，并将微件重命名为有用的名称。例如，“选择一个对象”和“航班传感器滚动10分钟聚合”。

#### 为仪表盘添加字符串输入

选择仪表盘中的 **设置** 齿轮图标以打开仪表盘配置面板，并添加以下字符串输入：

* `Flight Id 1` 的输入。
* `Flight Id 2` 的输入。
* `Sensor name` 的输入。

![为仪表盘添加字符串输入](../../../images/foundry/time-series/sensor-object-quiver-text-inputs.png)

#### 发布仪表盘

重命名您的仪表盘，以便可以从 Workshop 模块中轻松搜索。在此示例中，仪表盘命名为 `[示例] 传感器对象时间序列数据 | 航班传感器读取比较`。

![发布 Quiver 仪表盘](../../../images/foundry/time-series/sensor-object-quiver-publish.png)

查阅我们的 [Quiver 仪表盘文档](/zh/foundry/quiver/dashboards-overview/) 以获取有关如何创建和自定义 Quiver 仪表盘的更多信息。

## 第 IV 部分：在 Workshop 中嵌入您的仪表盘

1. 返回到您在本指南前面创建的 [Workshop 模块](#part-i-set-up-initial-widgets-in-a-workshop-module)。
2. 选择添加一个 Quiver 仪表盘微件，然后选择您的新仪表盘。

如有必要，您可以导航回仪表盘并通过编辑 Workshop 模块、选择 Quiver 仪表盘微件的配置并选择查看 Quiver 仪表盘来开始分析。然后选择 **编辑** 以查看支持的分析。

![在 Workshop 模块中嵌入仪表盘](../../../images/foundry/time-series/sensor-object-workshop-embed-dashboard.png)

查阅[我们的文档](/zh/foundry/quiver/dashboards-workshop/) 以获取有关如何在 Workshop 中自定义 Quiver 仪表盘的更多信息。
