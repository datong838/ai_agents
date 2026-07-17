---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/dropDuplicatesV1/",
  "title": "删除重复项",
  "page_id": "dropDuplicatesV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/dropV1/",
  "next": "/zh/foundry/pb-functions-transform/emptyFileV1/",
  "scraped_at": "2026-07-13T05:58:14.774421+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 删除重复项

> 支持于: 批处理

从输入中删除重复行。

**变换类别**: 其他

## 声明参数

* **数据集** - 要去重的行数据集。<br>*表格*
* 非必填 **列子集** - 如果指定了任何列，则只有这些列在确定唯一性时会被使用。<br>*Set\<Column\<AnyType>>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **数据集**: ri.foundry.main.dataset.aggregate
* **列子集**: {`tail_number`}

**输入:**

| tail\_number | airline | miles | factor |
| ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 124 | 2 |
| MT-222 | new airline | 1123 | 5 |
| XB-123 | foundry airline | 335 | 5 |
| MT-222 | new air | 565 | 4 |
| KK-452 | new air | 222 | 1 |
| XB-123 | foundry airline | 1134 | 3 |

**输出:**

| tail\_number | airline | miles | factor |
| ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 124 | 2 |
| MT-222 | new airline | 1123 | 5 |
| KK-452 | new air | 222 | 1 |

***

### 示例 2: 基本情况

**描述**: 没有子集时查找完全重复项。
**参数值:**

* **数据集**: ri.foundry.main.dataset.aggregate
* **列子集**: {}

**输入:**

| tail\_number | airline | miles | factor |
| ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 124 | 2 |
| XB-123 | foundry air | 124 | 2 |
| XB-123 | foundry air | 124 | 2 |
| MT-222 | new airline | 1123 | 5 |
| MT-222 | new airline | 1123 | 5 |

**输出:**

| tail\_number | airline | miles | factor |
| ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 124 | 2 |
| MT-222 | new airline | 1123 | 5 |

***
