---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/projectV1/",
  "title": "项目",
  "page_id": "projectV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/pivotV1/",
  "next": "/zh/foundry/pb-functions-transform/projectOnConditionV1/",
  "scraped_at": "2026-07-13T05:59:09.162863+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 项目

> 支持于: 批处理, 流处理

通过选择列或对列应用函数来变换输入数据集。

**变换类别**: 其他

## 声明的参数

* **列** - 要应用于数据集的列变换列表。<br>*List\<Expression\<AnyType>>*
* **数据集** - 要应用操作的数据集。<br>*Table*
* **保留剩余列** - 保留数据集中未投影的所有列。<br>*Literal\<Boolean>*

## 示例

### 示例 1: 基本案例

**参数值:**

* **列**: \[<br>alias(<br> alias: airline,<br> expression: `airlin`,<br>)]
* **数据集**: ri.foundry.main.dataset.a
* **保留剩余列**: false

**输入:**

| airlin | miles |
| ----- | ----- |
| foundry airways | 2500 |
| new air | 3000 |

**输出:**

| airline |
| ----- |
| foundry airways |
| new air |

***
