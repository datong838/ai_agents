---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/parseGeoJsonV1/",
  "title": "从GeoJSON文件中提取行",
  "page_id": "parseGeoJsonV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/parseCsvV1/",
  "next": "/zh/foundry/pb-functions-transform/parseJsonV1/",
  "scraped_at": "2026-07-13T05:58:19.790492+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从GeoJSON文件中提取行

> 支持于: 批量

读取一个文件的数据集并将每个GeoJSON文件解析为行。输出数据集将有一个几何列，以及用户列出的每个属性的列，除了 \_error 和 \_file 列。如果用户没有提供要提取的属性，整个属性结构体将以字符串形式提取到一个属性列中。文件中的所有GeoJSON必须是：
a) 多行FeatureCollection：整个文件为一个类型为FeatureCollection的GeoJSON
b) 单行Feature：每行都是一个完全有效的类型为Feature的GeoJSON。

**变换类别**: 文件, 地理空间

## 声明的参数

* **数据集** - 要处理的GeoJSON文件的数据集。<br>*文件*
* **属性列表** - 需要从这些GeoJSON文件中提取的属性及其类型列表。如果提供了一个空结构体，将在一个属性列中提取所有'properties'作为字符串。<br>*类型\<Struct>*
* **多行** - 如果每个文件中的每一行都是一个完全有效的类型为Feature的GeoJSON，则将其设置为false。如果整个文件是一个有效的类型为FeatureCollection的GeoJSON，则将其设置为true。<br>*字面量\<Boolean>*
* *非必填* **源坐标系** - 格式为"authority:id"的坐标系标识符。例如，UTM 18N区可以通过EPSG:32618识别。如果未指定，将默认为WGS84，即EPSG:4326。<br>*字面量<字符串>*
