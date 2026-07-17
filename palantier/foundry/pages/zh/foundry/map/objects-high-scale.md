---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/map/objects-high-scale/",
  "title": "显示高规模对象数据",
  "page_id": "objects-high-scale",
  "category_id": "ontology",
  "section_id": "map",
  "previous": "/zh/foundry/map/visualize-tracks/",
  "next": "/zh/foundry/map/integrate-objects/",
  "scraped_at": "2026-07-14T05:03:27.481540+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 显示高规模对象数据 \[Beta]

:::callout{theme="neutral"}
高规模对象渲染是一个beta功能，可能在您的注册中不可用。联系Palantir支持以获取更多信息。
:::

默认情况下，地图应用程序会加载图层中的所有对象以将它们渲染在地图上。这本质上创建了一个规模限制，因为您只能渲染从Ontology加载到浏览器中的数据量。**启用高规模渲染**功能通过限制应用程序仅加载显示地图可见范围所需的数据，促进了广泛对象集的展示。

## 启用高规模渲染

如果在您的实例中可以使用高规模渲染，您可以在图层的样式面板中使用**启用高规模渲染**切换为每个图层启用它。

![启用高规模切换](/resources/foundry/map/objects-high-scale.png)

高规模渲染仅在以下情况下可用于图层：

* 图层的对象类型至少有一个[geohash](/zh/foundry/map/integrate-objects/#points)或[geoshape](/zh/foundry/map/integrate-objects/#polygons-and-lines)属性。
* 高规模渲染已为对象类型启用。联系Palantir支持以获取更多信息。

## 添加具有高规模渲染的对象

对于支持以高规模模式显示的对象类型，搜索对话框不会限制可以添加到地图的对象数量。因此，**添加所有**选项将始终启用。

## 高规模渲染功能兼容性

在高规模图层中渲染的对象由于以下几个原因无法与许多其他地图应用功能正确互操作：

* 作为开发生命周期中[Beta](/zh/foundry/platform-overview/development-life-cycle/#beta)阶段的功能，下面列出的许多缺失能力正在积极开发中，并将在功能达到[普遍可用性](/zh/foundry/platform-overview/development-life-cycle/#generally-available-ga)时可用。
* 许多与高规模渲染不兼容的功能需要从无法支持高规模图层中渲染数据的服务加载数据。

### 样式选项

Geohash和geoshape属性是[对象图层几何](/zh/foundry/map/visualize-objects/#geometries)唯一支持的几何来源，并且所有[基于值的样式选项](/zh/foundry/map/visualize-objects/#value-based-styling)仅支持属性值。

因此，以下选项不支持：

* 基于时间序列的样式（测量和TSPs）
* 派生属性函数
* [按时间调整不透明度](/zh/foundry/map/visualize-objects/#opacity-styling)
* [标签](/zh/foundry/map/visualize-objects/#labels-and-tooltips)
* [时间线样式器](/zh/foundry/map/timeline/#style-the-timeline)

### 筛选

在高规模图层中显示的对象不遵循在[直方图](/zh/foundry/map/histogram/#filtering)或[时间线](/zh/foundry/map/timeline/#filter-time-events)中应用的筛选。

### 形状

在高规模图层中显示的对象在[从活动选择创建形状](/zh/foundry/map/shapes/#from-selection)时不会被包括在内。
