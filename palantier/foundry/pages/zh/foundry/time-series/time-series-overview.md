---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/time-series-overview/",
  "title": "概述",
  "page_id": "time-series-overview",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/transforms-common/transforms-versions/",
  "next": "/zh/foundry/time-series/time-series-concepts-glossary/",
  "scraped_at": "2026-07-13T06:08:59.846202+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

## 什么是时间序列数据？

时间序列数据是一系列在时间上进行测量的数据，通常以固定间隔进行。

一些时间序列数据的例子包括：

* 每日航班总数
* 每小时的生产输出
* 亚秒级分辨率的高频温度读数

您可以使用 Foundry 应用程序（如 Quiver、Vertex 和 Workshop）可视化和分析随时间发生的更改。[了解有关在 Foundry 中使用时间序列的更多信息](/zh/foundry/time-series/time-series-usage/)。

## 过程概述

要使用您的数据进行时间序列分析，您必须设置两个主要组件：一个时间序列对象类型和一个时间序列同步。

[时间序列对象类型](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-object-type) 定义您的时间序列数据集的元数据，并允许 Foundry 应用程序访问底层时间序列数据。[时间序列同步](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-sync) 是一个由数据集或流支持的资源，用于索引时间序列数据并为[时间序列属性](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-property-tsp)提供值。

## 在Ontology中存储时间序列

在 Ontology 中设置[时间序列对象类型](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-object-type)有两种方法。最常见的方法是将[时间序列属性 (TSP)](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-property-tsp)直接添加到对象类型中。只要该对象类型的所有对象都有该 TSP 的时间序列数据，就应该使用此选项。这些对象类型应构成您的分析或操作的基础。

了解有关[创建时间序列对象类型](/zh/foundry/time-series/create-or-select-ts-ot/)和[配置 TSP](/zh/foundry/time-series/time-series-properties/)的更多信息。

第二种更高级的配置选项是设置一个[传感器对象类型](/zh/foundry/time-series/time-series-concepts-glossary/#sensor-object-type)，该类型链接到其记录数据的根对象类型。根对象类型也可以直接在其自身上设置其他 TSP，如第一个选项中所述。当您的组织有大量配置选项的设备时，此设置非常有用。

Foundry 中的终端用户应用程序可以在统一视图中获取和显示位于对象类型或链接传感器对象上的 TSP。如果您在对象上执行搜索以查找其链接的传感器对象，您应该返回一组具有唯一传感器名称的传感器。由于每个传感器对象都具有唯一名称，通常您可以拥有单个传感器对象类型。

在第一个配置选项中，您可以通过向时间序列对象类型支持的数据集中添加额外的\_\_列\_\_来添加时间序列属性。在第二个选项中，您可以通过向传感器对象类型的时间序列对象类型支持的数据集中添加额外的\_\_行\_\_来添加更多有效链接到根对象类型的时间序列属性。

在下面的示例中，因为所有机器都有`Temperature`的值，我们应该将`Temperature`设置为`Machine`对象类型上的 TSP。

由于`Flow rate`仅与某些机器相关，我们建议将 TSP 放在传感器对象类型上。这将有助于防止在[时间序列对象类型支持的数据集](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-object-type-backing-dataset)中出现大量空条目。

### 传感器对象类型

传感器对象类型通过允许对象类型的每个对象拥有自己的一组时间序列数据（即，每个链接传感器一个时间序列）为您的 Ontology 提供灵活性。使用传感器对象类型的其他一些优点包括：

* 创建更健壮的[时间序列对象类型支持的数据集](/zh/foundry/time-series/time-series-concepts-glossary/#time-series-object-type-backing-dataset)。
* 在一个地方维护每个特定传感器的元数据，如单位或插值。
* 将补充对象类型（如警报或注释）链接到传感器对象类型，以便从任何链接对象中更轻松地发现。

例如，考虑一个`Equipment`对象类型，其中每个`Equipment`可能是`Pump`或`Reactor`。前者有一个`Pressure`读数，后者有一个`Temperature`读数。您可以创建单独的`Pump`和`Reactor`对象类型，但更通用的`Equipment`对象类型可能是更好的选择。在这种情况下，没有传感器对象，`Equipment`对象将需要两个 TSP；然而，实际上只有一个会有给定`Equipment`的时间序列数据。随着`Equipment`的专业化增长，您将需要管理具有传感器对象类型的传感器以保持易读性，即不为每个对象显示大多为空的 TSP。

当您配置传感器对象类型时，特殊元数据将应用于您的 Ontology 的某些部分，以指示此对象类型是一个传感器，并正在为指定的根对象类型记录数据。在更高层次上，前端应用程序想要加载对象集的所有相关时间序列数据时执行以下操作：

* 获取对象集上的所有 TSP。
* 对对象集执行搜索以查找与此特殊元数据的任何链接。
* 获取链接传感器对象的传感器名称。

了解有关[在 Quiver 中访问传感器对象类型](/zh/foundry/quiver/timeseries-visualize/#time-series-charts)或[使用它们创建派生序列](/zh/foundry/time-series/setup-derived-series/)的更多信息。
