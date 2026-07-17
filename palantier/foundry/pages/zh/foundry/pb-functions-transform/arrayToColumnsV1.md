---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/arrayToColumnsV1/",
  "title": "数组元素到列",
  "page_id": "arrayToColumnsV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/applyExpressionV1/",
  "next": "/zh/foundry/pb-functions-transform/assignTimestampsAndWatermarksV1/",
  "scraped_at": "2026-07-13T05:58:08.029071+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组元素到列

> 支持于: 批处理

从数组中提取元素到列中。

**变换类别**: 数组

## 声明的参数

* **数组** - 要从中提取列的数组。<br>*Expression\<Array\<AnyType>>*
* **要提取的列** - 列名列表。<br>*List\<Literal<字符串>>*
* **数据集** - 要删除列的数据集。<br>*Table*

## 示例

### 示例 1: 基本情况

**参数值:**

* **数组**: `stats`
* **要提取的列**: \[miles, id]
* **数据集**: ri.foundry.main.dataset.a

**输入:**

| stats |
| ----- |
| \[ 1000, 2 ] |

**输出:**

| miles | id | stats |
| ----- | ----- | ----- |
| 1000 | 2 | \[ 1000, 2 ] |

***

### 示例 2: 基本情况

**参数值:**

* **数组**: `stats`
* **要提取的列**: \[miles, id]
* **数据集**: ri.foundry.main.dataset.a

**输入:**

| stats |
| ----- |
| \[ 1000, 2, 10 ] |
| \[ 2000 ] |

**输出:**

| miles | id | stats |
| ----- | ----- | ----- |
| 1000 | 2 | \[ 1000, 2, 10 ] |
| 2000 | *null* | \[ 2000 ] |

***

### 示例 3: 空值情况

**参数值:**

* **数组**: `stats`
* **要提取的列**: \[miles, id]
* **数据集**: ri.foundry.main.dataset.a

**输入:**

| stats |
| ----- |
| \[ *null*, *null* ] |
| *null* |

**输出:**

| miles | id | stats |
| ----- | ----- | ----- |
| *null* | *null* | \[ *null*, *null* ] |
| *null* | *null* | *null* |

***
