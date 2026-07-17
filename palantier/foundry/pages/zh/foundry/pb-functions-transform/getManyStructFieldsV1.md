---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/getManyStructFieldsV1/",
  "title": "提取多个结构字段",
  "page_id": "getManyStructFieldsV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/extractFileMetadataAsRowsV1/",
  "next": "/zh/foundry/pb-functions-transform/parseCsvV1/",
  "scraped_at": "2026-07-13T05:58:19.016985+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 提取多个结构字段

> 支持于: 批处理

从结构中提取多个字段。原始结构将被删除。

**变换类别**: 结构

## 声明的参数

* **Dataset** - 包含结构列的数据集。<br>*表*
* **Locators** - 用于访问结构中字段的定位器。<br>*列表<元组<结构定位器, 字面量<字符串>>>*
* **Struct** - 输入结构。<br>*列<结构>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **Dataset**: ri.foundry.main.dataset.a
* **Locators**: \[(airline.name, airline), (tail\_no, tail\_number)]
* **Struct**: `raw`

**输入:**

| raw |
| ----- |
| {<br> **airline**: {<br> **id**: NA,<br> **name**: new air,<br>},<br> **tail\_no**: NA-123,<br>} |
| {<br> **airline**: {<br> **id**: FA,<br> **name**: foundry airways,<br>},<br> **tail\_no**: FA-123,<br>} |

**输出:**

| airline | tail\_number |
| ----- | ----- |
| new air | NA-123 |
| foundry airways | FA-123 |

***
