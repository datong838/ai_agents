---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geometryToGeobufExpressionV1/",
  "title": "将GeoJSON编码为Geobuf",
  "page_id": "geometryToGeobufExpressionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/divideV1/",
  "next": "/zh/foundry/pb-functions-expression/endsWithV1/",
  "scraped_at": "2026-07-13T05:54:22.973764+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将GeoJSON编码为Geobuf

> 支持于：批处理，流式处理

将GeoJSON几何体编码为Geobuf。

**表达式类别**：地理空间

## 声明的参数

* **Geometry** - 要转换为Geobuf的几何体。<br>*Expression\<Geometry>*
* **非必填** **Dimensions** - 在Geobuf中编码的每个坐标的维度数量。<br>*Expression\<Integer>*
* **非必填** **Precision** - 小数点后保留的小数位数。<br>*Expression\<Integer>*

**输出类型：** *Geobuf*

## 示例

### 示例 1：基本案例

**参数值：**

* **Geometry**: `geojson`
* **Dimensions**: *null*
* **Precision**: *null*

| geojson | **输出** |
| ----- | ----- |
| {"type":"Point","coordinates": \[32.0, 58.0]} | MgwIABoIgKDCHoCKqDc= |
| *null* | *null* |
| {"type":"Point","coordinates": \[-73.989015, 40.753206]} | MgwIABoIre7HRuzg7iY= |
