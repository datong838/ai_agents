---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/time-series-properties/",
  "title": "时间序列属性 (TSPs)",
  "page_id": "time-series-properties",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/create-or-select-ts-ot/",
  "next": "/zh/foundry/time-series/time-series-syncs/",
  "scraped_at": "2026-07-13T06:16:38.940755+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 时间序列属性 (TSPs)

![时间序列属性的可视化。](../../../images/foundry/time-series/time-series-setup-tsp-overview-graphic.svg)

[时间序列属性 (TSP)](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-property-tsp) 是使时间序列数据在 Foundry 应用程序中可用的属性。查看如何[使用时间序列](/zh/foundry/time-series/time-series-usage/)以获取更多详细信息。

当查看时间序列属性时，值将显示为相关时间序列值的图示。例如，下面的示例展示了一个 `temperature_id` 时间序列属性，使用 [Quiver](/zh/foundry/quiver/overview/) 中的基础时间序列数据进行可视化。

![添加时间序列属性](../../../images/foundry/time-series/time-series-setup-time-series-property.png)

## 时间序列属性设置

要获得以下步骤的指导式演练，请在平台中使用时间序列设置助手。通过直接导航到 `https://<domain>/workspace/ontology/home/overview/time-series-setup` 或通过导航到包含时间戳列的数据集预览并从**分析数据**操作菜单中选择**设置时间序列**来启动设置助手。

![时间序列设置助手。](../../../images/foundry/time-series/time-series-setup-setup-assistant.png)

有关设置时间序列对象类型的更多指导，请参阅关于[如何创建或选择时间序列对象类型](/zh/foundry/time-series/create-or-select-ts-ot/)的文档。

时间序列属性在 [Ontology Manager](/zh/foundry/ontology-manager/overview/) 应用程序的**功能**选项卡中进行配置。如果您正在跟随设置助手进行操作，创建新对象类型或选择现有对象类型后，您将自动转到**功能**选项卡。如果对象类型已经配置了时间序列属性，您将看到它们显示在表格视图中，您还可以在其中添加或删除时间序列属性。

![Ontology Manager 功能选项卡](../../../images/foundry/time-series/time-series-setup-ontology-capabilities-tab.png)

如果对象类型上没有现有的时间序列属性，您将被引导添加一个。

![在 Ontology Manager 中添加时间序列属性](../../../images/foundry/time-series/time-series-oma-get-started.png)

要添加时间序列属性，请选择**开始**。这将启动一个对话框，引导您完成以下步骤：

1. **确定对象类型：** 决定此对象类型是否为[传感器对象类型](/zh/foundry/time-series/time-series-concepts-glossary/#sensor-object-type)。

2. **选择属性：** 选择包含序列 ID 的 `字符串` 属性，然后选择**下一步**。

![添加时间序列属性的对话框。](../../../images/foundry/time-series/time-series-setup-add-tsp-dialog-2.png)

3. **选择时间序列同步：** 如果已经存在时间序列同步，则选择一个，或按照说明[创建新的时间序列同步](/zh/foundry/time-series/time-series-syncs/#create-a-time-series-sync)。您可以通过继续选择\*\*+ 添加同步\*\*来选择多个时间序列同步。如果您的 TSP 由多个时间序列同步支持，您将需要使用[合格的序列 ID](/zh/foundry/time-series/time-series-concepts-glossary/#qualified-series-id)。

![添加时间序列属性的对话框。](../../../images/foundry/time-series/time-series-setup-add-tsp-dialog-3.png)

:::callout{theme="neutral"}
如果您想添加或修改时间序列属性但已关闭设置助手，可以通过以下任一方式恢复进度：

* 在 Ontology Manager 中导航到您的对象类型，然后在左侧面板中导航到**功能**选项卡。
* 通过直接导航到 `https://<domain>/workspace/ontology/home/overview/time-series-setup` 或导航到包含 `timestamp` 列的数据集预览，并从**分析数据**操作菜单中选择**设置时间序列**来重新启动设置助手。
:::

## 时间序列格式化

时间序列格式化允许设置时间序列的所需内部插值和单位。像 Quiver 这样的应用程序将遵循提供的插值和单位值。

单位和插值格式化可以指向此对象类型上的其他 `字符串` 属性，以获得更细粒度的控制（例如，如果时间序列属性中包含的每个时间序列具有不同的单位和插值）。如果不需要细粒度控制，插值和单位都有一组标准值可供选择。

![时间序列格式化配置。](../../../images/foundry/time-series/time-series-setup-time-series-formatting.png)

传感器对象类型的内部插值和单位在[传感器对象配置部分](/zh/foundry/time-series/create-sensor-ot/)中配置。

:::callout{theme="neutral"}
时间序列格式化器中提供的单位主要用于视觉显示目的。例如，作为 Quiver 中图示的轴标签。
:::

## 默认时间序列属性

一个对象类型可以有一个时间序列属性被指定为默认时间序列属性。当为对象类型配置第一个时间序列属性时，该属性将被设置为默认时间序列属性。

![默认时间序列属性配置](../../../images/foundry/time-series/time-series-setup-default-tsp.png)

在某些应用程序中，默认时间序列属性在没有额外用户干预的情况下显示。例如，在 Quiver 中，对象属性时间序列卡片指向默认时间序列属性，除非另有指定。

![Quiver 中的默认时间序列属性。](../../../images/foundry/time-series/time-series-setup-default-tsp-quiver.png)

传感器对象类型的单个时间序列属性必须是默认时间序列属性。查看如何[设置传感器对象类型](/zh/foundry/time-series/create-sensor-ot/)以获取更多详细信息。
