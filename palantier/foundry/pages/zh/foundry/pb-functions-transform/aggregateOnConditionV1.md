---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/aggregateOnConditionV1/",
  "title": "条件下的聚合",
  "page_id": "aggregateOnConditionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/aggregateV1/",
  "next": "/zh/foundry/pb-functions-transform/aggregateOverWindowV2/",
  "scraped_at": "2026-07-13T05:58:00.060459+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 条件下的聚合

> 支持于：批处理

基于条件语句的聚合表达式。

**变换类别**: 聚合

## 声明的参数

* **用于聚合的列的条件** - 将测试输入模式中的所有列，查看它们是否匹配此条件。如果匹配，将对它们应用给定的表达式。<br>*ColumnPredicate*
* **数据集** - 需要操作的数据集。<br>*Table*
* **要聚合的表达式** - 对每个匹配条件的列应用一次的聚合表达式。<br>*List\<Expression\<AnyType>>*
* **非必填** **按列分组** - 聚合时按列分组的数据集列表。如果为空，则不应用分组。<br>*List\<Column\<AnyType>>*

## 示例

### 示例 1: 边缘情况

**描述**: 统计所有列中非空行的数量。
**参数值:**

* **用于聚合的列的条件**: <br>allColumns(<br><br>)
* **数据集**: ri.foundry.main.dataset.a
* **要聚合的表达式**: \[<br>dynamicAlias(<br> expression: <br>rowCount(<br> expression: `column`,<br>),<br> transformer: <br>columnNameConcat(<br> inputs: \[`column`, `_non_null`],<br>),<br>)]
* **按列分组**: *null*

**输入:**

| id | value | distance |
| ----- | ----- | ----- |
| 1 | 100 | 2000 |
| 2 | *null* | 100 |
| 3 | 500 | 300 |

**输出:**

| id\_non\_null | value\_non\_null | distance\_non\_null |
| ----- | ----- | ----- |
| 3 | 2 | 3 |

***

### 示例 2: 边缘情况

**描述**: 统计非空整数列的数量和均值。
**参数值:**

* **用于聚合的列的条件**: <br>columnHasType(<br> type: Integer,<br>)
* **数据集**: ri.foundry.main.dataset.a
* **要聚合的表达式**: \[<br>dynamicAlias(<br> expression: <br>rowCount(<br> expression: `column`,<br>),<br> transformer: <br>columnNameConcat(<br> inputs: \[`column`, `_non_null`],<br>),<br>), <br>dynamicAlias(<br> expression: <br>mean(<br> expression: `column`,<br>),<br> transformer: <br>columnNameConcat(<br> inputs: \[`column`, `_mean`],<br>),<br>)]
* **按列分组**: *null*

**输入:**

| id | value | distance |
| ----- | ----- | ----- |
| 1 | 100 | 2000 |
| 2 | *null* | 100 |
| 3 | 500 | 300 |

**输出:**

| id\_non\_null | id\_mean | value\_non\_null | value\_mean |
| ----- | ----- | ----- | ----- |
| 3 | 2.0 | 2 | 300.0 |

***

### 示例 3: 边缘情况

**参数值:**

* **用于聚合的列的条件**: <br>columnHasType(<br> type: Integer,<br>)
* **数据集**: ri.foundry.main.dataset.a
* **要聚合的表达式**: \[<br>dynamicAlias(<br> expression: <br>mean(<br> expression: `column`,<br>),<br> transformer: <br>columnNameConcat(<br> inputs: \[`column`, `_mean`],<br>),<br>)]
* **按列分组**: \[`id`]

**输入:**

| id | value | distance | airline |
| ----- | ----- | ----- | ----- |
| 1 | 100 | 2000 | new air |
| 1 | 200 | 3000 | new air |
| 2 | 500 | 3000 | foundry air |
| 2 | 400 | 1000 | foundry air |

**输出:**

| id | id\_mean | value\_mean | distance\_mean |
| ----- | ----- | ----- | ----- |
| 1 | 1.0 | 150.0 | 2500.0 |
| 2 | 2.0 | 450.0 | 2000.0 |

***

### 示例 4: 边缘情况

**描述**: 所有整数列的均值。
**参数值:**

* **用于聚合的列的条件**: <br>columnHasType(<br> type: Integer,<br>)
* **数据集**: ri.foundry.main.dataset.a
* **要聚合的表达式**: \[<br>dynamicAlias(<br> expression: <br>mean(<br> expression: `column`,<br>),<br> transformer: <br>columnNameConcat(<br> inputs: \[`column`, `_mean`],<br>),<br>)]
* **按列分组**: *null*

**输入:**

| id | value | distance |
| ----- | ----- | ----- |
| 1 | 100 | 2000 |
| 3 | 500 | 300 |

**输出:**

| id\_mean | value\_mean |
| ----- | ----- |
| 2.0 | 300.0 |
