---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/getStructFieldV2/",
  "title": "获取结构体字段",
  "page_id": "getStructFieldV2",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/h3NeighborsV1/",
  "next": "/zh/foundry/pb-functions-expression/geometryConvexHullV1/",
  "scraped_at": "2026-07-13T05:55:22.955551+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 获取结构体字段

> 支持于: 批处理, 流处理

从结构体中提取字段。

**表达式类别**: 结构体

## 声明的参数

* **定位器** - 提取多个条目中的内部元素，如 \['author', 'email']。<br>*StructLocator*
* **结构体** - *无描述*<br>*Expression\<Struct>*

**输出类型:** *AnyType*

## 示例

### 示例 1: 基本情况

**参数值:**

* **定位器**: airline.id
* **结构体**: `struct`

| 结构体 | **输出** |
| ----- | ----- |
| {<br> **airline**: {<br> **id**: NA,<br>},<br>} | NA |
| {<br> **airline**: {<br> **id**: FE,<br>},<br>} | FE |

***

### 示例 2: 基本情况

**参数值:**

* **定位器**: airline.id
* **结构体**: `struct`

| 结构体 | **输出** |
| ----- | ----- |
| {<br> **airline**: *null*,<br>} | *null* |
| {<br> **airline**: {<br> **id**: *null*,<br>},<br>} | *null* |
| *null* | *null* |

***
