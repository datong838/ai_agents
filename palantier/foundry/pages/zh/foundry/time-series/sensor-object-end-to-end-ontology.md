---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/sensor-object-end-to-end-ontology/",
  "title": "使用Ontology Manager创建传感器Object类型",
  "page_id": "sensor-object-end-to-end-ontology",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/sensor-object-end-to-end-pipeline/",
  "next": "/zh/foundry/time-series/sensor-object-end-to-end-operational/",
  "scraped_at": "2026-07-13T06:14:08.564716+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用Ontology Manager创建传感器Object类型

本指南解释了如何使用Ontology Manager创建传感器Object类型并将其链接到根Object类型。完成以下步骤后，您将能够在平台中与传感器Object类型进行交互。在此示例中，您将创建一个`Flight Sensor` Object类型，并将其链接到一个`Flight`根Object类型。

## 第一部分：创建传感器Object类型

1. 导航到Ontology Manager，并从左侧面板中选择**Object类型**。
2. 从屏幕右上角选择[**新建Object类型**](/zh/foundry/object-link-types/create-object-type/#create-a-new-object-type-with-the-helper)。
3. 在出现的配置对话框中，配置您的Object类型元数据。
4. 在**属性**步骤中，选择使用您通过[传感器数据管道](/zh/foundry/time-series/sensor-object-end-to-end-pipeline/)创建的`[Example] Sensors`数据集作为Object类型的支持。
5. 然后，在**属性**字段中，选择字符串类型`unique_sensor_flight_id`属性作为主键。如果这些选项可用，您也可以选择**从数据源同步所有列**或**映射所有列**。
6. 选择`Title`列作为标题属性，这使得`Flight Sensor` Object类型在应用中以人类可读的名称出现。

![传感器Object属性对话框](../../../images/foundry/time-series/sensor-object-om-object-creation.png)

7. 根据您平台的版本，您可能会看到配置`Flight Sensor` Object类型权限和操作的选项。我们的示例不需要额外的权限或操作配置。

8. 完成对话框中的所有步骤后，选择**创建**。

在新`[Example] Sensors` Object类型的**属性**标签中，属性应如下图所示：

![Ontology Manager中的传感器Object类型属性](../../../images/foundry/time-series/sensor-object-om-properties-in-progress.png)

## 第二部分：为传感器Object类型配置时间序列属性

1. 导航到Ontology Manager中的`[Example] Flight Sensor` Object类型，并从左侧面板中选择**能力**标签。
2. 从**时间序列属性**部分选择\*\*+ 添加\*\*。
3. 选择现有的`Flight Sensor Series Id`属性作为时间序列属性，然后选择**设置为默认时间序列属性**，以便它自动出现在Quiver中。

![为Flight Sensors Object类型选择时间序列属性](../../../images/foundry/time-series/sensor-object-om-setup-time-series-sync.png)

4. 选择您在[Pipeline Builder中](/zh/foundry/time-series/sensor-object-end-to-end-pipeline/)创建的时间序列同步。在我们的示例中，它被称为`[Example] Time Series Sync | Sensor Readings`。

![选择时间序列同步以将属性添加到传感器Object类型](../../../images/foundry/time-series/sensor-object-om-selected-time-series-sync.png)

5. 选择**添加属性**以保存时间序列属性配置。

## 第三部分：将传感器Object类型链接到根Object类型

使用以下步骤在`[Example] Flight Sensor`和`[Example] Flight` Object类型之间添加链接。

1. 在Ontology Manager的`[Example] Flight Sensor`视图中，选择**新建**下拉菜单并选择**链接类型**。
2. 在链接的左侧，选择`[Example] Flight Sensor` Object类型。在右侧，选择`[Example] Flight` Object类型。
3. 设置左侧`Flight Sensor` Object类型的基数为**多个**，右侧`Flight` Object类型的基数为**一个**，这意味着`Flight` Object类型与`Flight Sensor` Object类型具有一对多关系。
4. 将`flight_id`列设置为`Flight Sensor` Object类型的外键，这将设置`flight_id`为`Flight` Object类型的主键。

了解更多关于[链接类型](/zh/foundry/object-link-types/link-types-overview/)的信息。

![在Fight Sensor和Flight Object类型之间创建链接类型](../../../images/foundry/time-series/sensor-object-om-link-object.png)

## 第四部分：配置传感器Object类型

在时间序列部分，确保传感器Object类型切换为开启状态。设置`Sensor link`以使用最近创建的`Flight`到`Flight Sensor`链接。

![传感器Object类型配置](../../../images/foundry/time-series/sensor-object-om-configuration.png)

1. 将**链接**名称设置为`Series Name`列。应用程序将在该系列名称下显示传感器Object数据。

2. 通过在传感器Object类型设置中选择**单位**下拉菜单来配置**单位**。

**是否分类**和**内部插值**可以从传感器Object类型上的属性推断，但对于此应用案例不是必需的。只有在需要将分类时间序列值与数值时间序列值区分开时，才需要**是否分类**。

**内部插值**用于启用像Quiver这样的应用程序推断相邻数据点之间的系列值。查看我们的[Quiver插值文档](/zh/foundry/quiver/timeseries-visualize/#interpolation-options)以获取更多信息。

3. 从屏幕右上角选择**保存**以查看Ontology和整个平台中的更改。

现在，您已准备好在操作环境中使用`Flight Sensor`和`Flight` Object类型。继续阅读文档以了解如何[在Workshop和Quiver中使用传感器Object类型时间序列数据](/zh/foundry/time-series/time-series-properties-use-case-operational/)。

:::callout{theme="neutral"}
我们的示例应用案例不需要配置**是否为枚举**。`Is deprecated`和`Sparkline preview`属性应被忽略。
:::
