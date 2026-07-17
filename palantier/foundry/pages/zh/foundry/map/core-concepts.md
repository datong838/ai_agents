---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/map/core-concepts/",
  "title": "核心概念",
  "page_id": "core-concepts",
  "category_id": "ontology",
  "section_id": "map",
  "previous": "/zh/foundry/map/getting-started/",
  "next": "/zh/foundry/map/map-overview/",
  "scraped_at": "2026-07-14T04:50:09.677335+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 核心概念

## 图层

**图层**是用于搭建地图的地理数据集合。Foundry Map应用支持多种图层，这些图层可以组合形成强大的地理空间可视化：

* **基础图层：**基础图层通过渲染包括道路、城市、边界、地名等世界地理特征，为地图提供基础。可用的基础图层包括浅色主题、深色主题和卫星图像等。使用**图层**面板中的选择器更改基础图层。

  ![基础图层选择器](../../../images/foundry/map/core-concepts-base-layer.png)

您还可以选择使用不同类型的图层，如下所示：

* \*\*Object图层：\*\*用于利用来自您的Ontology的[对象的地理空间数据](/zh/foundry/map/integrate-objects/)。
* \*\*链接图层：\*\*在执行周围搜索后显示对象之间的关系。
* \*\*覆盖图层：\*\*使用[地图图层编辑器](/zh/foundry/map/layer-editor/)创建高质量的可视化，只需创建一次即可导入一个或多个地图。
* \*\*注释图层：\*\*绘制形状以突出显示并提供有关地图特定区域的上下文信息。阅读更多关于[创建注释](/zh/foundry/map/annotations/)。

## Object样式

您应用于对象的[样式](/zh/foundry/map/visualize-objects/)定义了它们在地图上的外观。

## 时间选择

每个地图都有一个**选定时间**，该时间始终在当前选定的**时间窗口**内。时间窗口决定了地图加载和显示[时间序列](/zh/foundry/map/time-series/)数据的时间段。[基于时间的样式](/zh/foundry/map/visualize-objects/#opacity-styling)可以使用时间选择来选择性地控制具有时间数据的对象的不透明度。阅读更多关于操作[时间选择](/zh/foundry/map/time-selection/)的信息。
