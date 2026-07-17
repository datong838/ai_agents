---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/h3NeighborsV1/",
  "title": "获取H3索引的邻居",
  "page_id": "h3NeighborsV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/latLonBoundingBoxV1/",
  "next": "/zh/foundry/pb-functions-expression/getStructFieldV2/",
  "scraped_at": "2026-07-13T05:55:23.100471+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 获取H3索引的邻居

> 支持于: 批处理, 流处理

获取一个H3索引的所有邻居。

**表达式类别**: 地理空间

## 声明的参数

* **表达式** - 一个有效的H3索引。<br>*Expression\<H3 Index>*

**输出类型:** *Array\<H3 Index>*

## 示例

### 示例 1: 基本案例

**参数值:**

* **表达式**: `h3Index`

| h3Index | **输出** |
| ----- | ----- |
| 8843a13687fffff | \[ 8843a13681fffff, 8843a13683fffff, 8843a13685fffff, 8843a136abfffff, 8843a136b9fffff, 8843a136bdfffff ] |
| 85283473fffffff | \[ 8528340bfffffff, 8528340ffffffff, 85283447fffffff, 85283463fffffff, 85283477fffffff, 8528347bfffffff ] |
| 860800007ffffff | \[ 860800017ffffff, 86080001fffffff, 860800027ffffff, 86080002fffffff, 860800037ffffff ] |
| 无效的h3索引 | *null* |
| *null* | *null* |

***
