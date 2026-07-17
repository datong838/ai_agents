---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/geometryIntersectsV1/",
  "title": "几何图形相交",
  "page_id": "geometryIntersectsV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/timestampToStringV2/",
  "next": "/zh/foundry/pb-functions-expression/geometry3dAffineTransformationV1/",
  "scraped_at": "2026-07-13T05:54:52.893208+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 几何图形相交

> 支持于: 批处理, 流式处理

判断两个几何图形是否相交。

**表达式类别**: 地理空间

## 声明的参数

* **几何图形 a** - 几何图形 a。<br>*Expression\<Geometry>*
* **几何图形 b** - 几何图形 b。<br>*Expression\<Geometry>*

**输出类型:** *Boolean*

## 示例

### 示例 1: 基本情况

**参数值:**

* **几何图形 a**: `geometry_a`
* **几何图形 b**: `geometry_b`

| geometry\_a | geometry\_b | **输出** |
| ----- | ----- | ----- |
| {"coordinates":\[\[\[-112.94377956164206,34.81725414459382],\[-112.94377956164206,30.006795384733323], \[... | {"coordinates":\[\[\[-103.78627755867336,33.162750522563925],\[-103.78627755867336,28.29724741894266],\[-... | true |
| {"coordinates":\[\[\[0.3651446504365481,15.159518507965103],\[0.3651446504365481,13.427462911044273],\[3.... | {"coordinates":\[\[\[5.656394524666183,13.405417496831944],\[5.656394524666183,11.29869961209053],\[8.551... | false |

***
