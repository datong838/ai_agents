---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/geospatial/types_of_geospatial_data/",
  "title": "地理空间数据的类型",
  "page_id": "types_of_geospatial_data",
  "category_id": "data-integration",
  "section_id": "geospatial",
  "previous": "/zh/foundry/geospatial/overview/",
  "next": "/zh/foundry/geospatial/coordinate_reference_systems_and_projections/",
  "scraped_at": "2026-07-13T06:19:27.076873+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 地理空间数据的类型

在Foundry中，您可能会处理多种类型的地理空间数据。在规划如何使用数据时，了解您拥有的数据类型非常重要。

地理空间数据主要有两种类型：[**栅格数据**](#raster-data) 和 [**矢量数据**](#vector-data)。具有时间组件的地理空间数据被称为 [**时空数据**](#geotemporal-data)。

所有示例图像均使用概念性或开源数据。

## 栅格数据

栅格数据由组织成行和列的单元格矩阵组成，其中每个单元格代表特定信息。栅格数据的示例包括卫星图像源、扫描地图和数字高程模型 (DEMs)。

了解更多关于[处理栅格数据](/zh/foundry/geospatial/raster_data/)。

<img src="../../foundry-docs/geospatial/media/data_type_raster_example.png" alt="栅格数据示例：卫星气象图像" width="500" />

## 矢量数据

矢量数据用于存储具有离散边界的数据，并将这些数据表示为点、线和多边形。矢量数据的示例包括在美国地图上代表城市的点、在一个州中代表道路的线，以及代表选区边界的多边形。

了解更多关于[在变换中处理矢量数据](/zh/foundry/geospatial/vector_data_in_transforms/)。

<img src="../../foundry-docs/geospatial/media/data_type_vector_example.png" alt="矢量数据示例：俄勒冈州的分级统计图与叠加的电力传输线" width="500" />

## 时空数据

此外，一些地理空间数据可能具有时间组件，例如车辆随时间的位置信息或在不同时间拍摄的卫星图像。这些数据可以称为**时空数据**。
