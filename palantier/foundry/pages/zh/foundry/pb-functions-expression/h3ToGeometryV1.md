---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/h3ToGeometryV1/",
  "title": "H3 转换为几何",
  "page_id": "h3ToGeometryV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/h3CellToParentV1/",
  "next": "/zh/foundry/pb-functions-expression/sha256V1/",
  "scraped_at": "2026-07-13T05:55:38.541348+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# H3 转换为几何

> 支持于: 批处理, 流处理

将 H3 索引转换为多边形。

**表达式类别**: 地理空间

## 声明的参数

* **表达式** - 一个有效的 H3 索引。<br>*Expression\<H3 Index>*

**输出类型:** *几何*

## 示例

### 示例 1: 基本案例

**参数值:**

* **表达式**: `h3`

| h3 | **输出** |
| ----- | ----- |
| 8029fffffffffff | {"type":"Polygon","coordinates":\[\[\[-121.3366283326517,28.653019311484535],\[-110.25748485653355,36.80... |
| 85283473fffffff | {"type":"Polygon","coordinates":\[\[\[-121.91508032705622,37.2713558667319],\[-121.86222328902491,37.353... |
| 8f2d55c256ac883 | {"type":"Polygon","coordinates":\[\[\[39.99999168658859,45.00000521415798],\[39.99999036498484,45.000000... |

***
