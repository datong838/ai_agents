---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/manuallyEnteredTableV1/",
  "title": "手动输入表",
  "page_id": "manuallyEnteredTableV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/leftLookupJoinV1/",
  "next": "/zh/foundry/pb-functions-transform/mappingJoinV1/",
  "scraped_at": "2026-07-13T05:58:58.133096+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 手动输入表

> 支持于: 批处理, 流式处理

使用手动输入的表数据创建输出。

**变换类别**: 其他

## 声明的参数

* **Rows** - 代表行的结构列表，结构字段代表列名和值。<br>*List\<Literal\<Struct>>*
* **Schema**（非必填） - 如果存在，将被用于在列名和类型的模式。如果未定义，行必须是非空的并将用于推断模式。<br>*Type\<Struct>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **Rows**: \[{<br> **airline**: foundry airlines,<br> **flight\_code**: 112,<br> **flight\_number**: XB-123,<br>}, {<br> **airline**: foundry airlines,<br> **flight\_code**: 533,<br> **flight\_number**: MT-444,<br>}, {<br> **airline**: new air,<br> **flight\_code**: 934,<br> **flight\_number**: KK-123,<br>}]
* **Schema**: Struct\<flight\_code:Integer, flight\_number:String, airline:String>

**输入:**

| flight\_code | flight\_number | airline |
| ----- | ----- | ----- |
| 112 | XB-123 | foundry airlines |
| 533 | MT-444 | foundry airlines |
| 934 | KK-123 | new air |

**输出:**

| flight\_code | flight\_number | airline |
| ----- | ----- | ----- |
| 112 | XB-123 | foundry airlines |
| 533 | MT-444 | foundry airlines |
| 934 | KK-123 | new air |

***
