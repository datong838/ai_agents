---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/geospatial/coordinate_reference_systems_and_projections/",
  "title": "坐标参考系统和投影",
  "page_id": "coordinate_reference_systems_and_projections",
  "category_id": "data-integration",
  "section_id": "geospatial",
  "previous": "/zh/foundry/geospatial/types_of_geospatial_data/",
  "next": "/zh/foundry/geospatial/example_workflows/",
  "scraped_at": "2026-07-13T06:14:30.768824+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 坐标参考系统和投影

地理空间数据可以存储在各种[参考系统和投影 ↗](https://en.wikipedia.org/wiki/Spatial_reference_system)中。不同的投影可以使处理人工输入的数字或执行面积/长度计算更容易或更困难。所有二维地图投影通过将地球这一三维椭球体平面化为屏幕/纸张这一二维表面而扭曲了现实世界的数据。这些扭曲可能发生在*形状*、*面积*、*距离*和*方向*上（统称为*SADD*）。

所有标准投影的库可在欧洲石油测量组 (EPSG) [公共注册表 ↗](https://epsg.io/)中找到。最常见的投影是“标准”经纬度（[WGS 84 又称 EPSG:4326 ↗](https://epsg.io/4326)）。然而，源数据通常基于当地条件和规范采用不同的投影。例如，许多美国客户使用根据北美基准 1983 (NAD83) 捕获的数据，该数据使用的地球表面基础模型与 WGS 84 使用的不同。

了解您的数据使用的坐标参考系统 (CRS) 非常重要，尤其是在您处理其他存储在不同 CRS 中的数据时。如果您有来自同一地点的数据，这些数据存储在不同的坐标参考系统中，*这些数据将在您的地图上无法对齐*。您应始终咨询关键利益相关者和主题专家，以澄清与 CRS、数据准确性和其他最佳实践相关的重要问题。

Foundry中的所有地图都期望使用WGS 84，并使用[Web Mercator Projection ↗](https://en.wikipedia.org/wiki/Web_Mercator_projection)。

了解更多关于在PySpark变换中[操作CRS](/zh/foundry/geospatial/vector_data_in_transforms/)的信息。
