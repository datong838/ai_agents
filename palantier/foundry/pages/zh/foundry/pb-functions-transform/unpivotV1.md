---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/unpivotV1/",
  "title": "反透视",
  "page_id": "unpivotV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/unionByNameV1/",
  "next": "/zh/foundry/pb-functions-transform/wideUnionByNameV1/",
  "scraped_at": "2026-07-13T05:59:09.762716+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 反透视

> 支持于：批处理，流处理

执行与透视相反的操作...

**变换类别**: 聚合, 流行

## 声明参数

* **要反透视的列** - 要反透视的列列表。<br>*List\<Column\<T>>*
* **数据集** - 要执行反透视的数据集。<br>*Table*
* **输出反透视列名** - 提供给包含反透视列的输出列的列名。<br>*Literal<字符串>*
* **反透视值输出列名** - 提供给包含反透视值的输出列的列名。<br>*Literal<字符串>*

**类型变量界限:** *T 接受 AnyType*

## 示例

### 示例 1: 基本情况

**参数值:**

* **要反透视的列**: \[`new_york_miles`, `london_miles`]
* **数据集**: ri.foundry.main.dataset.a
* **输出反透视列名**: city
* **反透视值输出列名**: miles

**输入:**

| airline | new\_york\_miles | london\_miles |
| ----- | ----- | ----- |
| foundry airways | 1000 | 6000 |
| new air | *null* | 8000 |

**输出:**

| city | miles | airline |
| ----- | ----- | ----- |
| new\_york\_miles | 1000 | foundry airways |
| london\_miles | 6000 | foundry airways |
| new\_york\_miles | *null* | new air |
| london\_miles | 8000 | new air |

***
