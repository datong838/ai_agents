---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/map/time-overview/",
  "title": "地图中的时间和时间数据",
  "page_id": "time-overview",
  "category_id": "ontology",
  "section_id": "map",
  "previous": "/zh/foundry/map/actions/",
  "next": "/zh/foundry/map/time-selection/",
  "scraped_at": "2026-07-14T04:58:01.412298+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 地图中的时间和时间数据

地图具有一系列用于可视化和处理随时间变化数据的功能。时间数据有多种形式，每种形式都可以以不同的方式使用和可视化。地图应用程序中显示的所有时间数据都遵循当前[选择的时间](/zh/foundry/map/time-selection/)，以帮助您了解数据随时间的变化并检查过去的特定时间。

## 时间序列

[时间序列](/zh/foundry/map/time-series/)是随时间变化的测量值。您可以在Ontology中将时间序列值配置为[时间序列属性](/zh/foundry/time-series/time-series-setup/)。使用时间序列在地图上[样式化Objects](/zh/foundry/map/visualize-objects/#value-based-styling)，并在[序列面板](/zh/foundry/map/time-series/#explore-related-time-series)中查看它们。

## 事件

![按时间样式化事件。](../../../images/foundry/map/events-style-by-time.gif)

[事件](/zh/foundry/map/events/)是与特定时间或时间范围关联的具有附加元数据的Objects。事件可以被用于[控制Objects的不透明度](/zh/foundry/map/visualize-objects/#opacity-styling)在您的地图上，并在[时间轴](/zh/foundry/map/timeline/#style-the-timeline)中可视化。

## 轨迹

![轨迹几何示例。](../../../images/foundry/map/styling-tracks.png)

使用[轨迹](/zh/foundry/map/integrate-objects/#tracks)来表示位置随时间变化的Objects。[轨迹样式选项](/zh/foundry/map/visualize-tracks/)允许您自定义Objects随时间变化的位置的可视化方式。
