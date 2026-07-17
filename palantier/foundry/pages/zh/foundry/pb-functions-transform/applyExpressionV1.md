---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/applyExpressionV1/",
  "title": "应用表达式",
  "page_id": "applyExpressionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/complexAntiJoinV1/",
  "next": "/zh/foundry/pb-functions-transform/arrayToColumnsV1/",
  "scraped_at": "2026-07-13T05:58:10.802821+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 应用表达式

> 支持于: 批处理，流处理

通过应用单个表达式变换输入数据集。

**变换类别**: 其它

## 声明的参数

* **数据集** - 需要应用表达式的数据集。<br>*Table*
* **表达式** - 要应用的表达式。<br>*Expression\<AnyType>*

## 示例

### 示例 1: 基本案例

**参数值:**

* **数据集**: ri.foundry.main.dataset.a
* **表达式**: <br>alias(<br> alias: kilometers,<br> expression: <br>convertDistance(<br> amount: `miles`,<br> currentUnit: `mile`,<br> targetUnit: `kilometer`,<br>),<br>)

**输入:**

| airline | miles |
| ----- | ----- |
| foundry airways | 2500 |
| new air | 3000 |

**输出:**

| kilometers | airline | miles |
| ----- | ----- | ----- |
| 4023.36 | foundry airways | 2500 |
| 4828.03 | new air | 3000 |

***
