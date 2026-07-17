---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/createStructV2/",
  "title": "创建结构体列",
  "page_id": "createStructV2",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/createGeometryFromOrderedGeoPointRowsV1/",
  "next": "/zh/foundry/pb-functions-expression/createQualifiedTimeSeriesIdV1/",
  "scraped_at": "2026-07-13T05:54:15.597215+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建结构体列

> 支持于: 批处理, 流处理

将多个列合并为单个结构化列。

**表达式类别**: 结构体

## 声明的参数

* **结构体元素** - 用于创建结构体的列列表。<br>*List\<Expression\<AnyType>>*

**输出类型:** *结构体*

## 示例

### 示例 1: 基础案例

**参数值:**

* **结构体元素**: \[`tail_number`, `id`]

| tail\_number | id | **输出** |
| ----- | ----- | ----- |
| MT-112 | 1 | {<br> **id**: 1,<br> **tail\_number**: MT-112,<br>} |
| XB-123 | 2 | {<br> **id**: 2,<br> **tail\_number**: XB-123,<br>} |
| PA-654 | 3 | {<br> **id**: 3,<br> **tail\_number**: PA-654,<br>} |

***

### 示例 2: 基础案例

**参数值:**

* **结构体元素**: \[`tail_number`, `id`]

| tail\_number | id | **输出** |
| ----- | ----- | ----- |
| *null* | 1 | {<br> **id**: 1,<br> **tail\_number**: *null*,<br>} |
| XB-123 | *null* | {<br> **id**: *null*,<br> **tail\_number**: XB-123,<br>} |
| *null* | *null* | {<br> **id**: *null*,<br> **tail\_number**: *null*,<br>} |

***
