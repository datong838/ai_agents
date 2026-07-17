---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/projectOnConditionV1/",
  "title": "项目条件",
  "page_id": "projectOnConditionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/projectV1/",
  "next": "/zh/foundry/pb-functions-transform/windowedProjectV1/",
  "scraped_at": "2026-07-13T05:59:02.610621+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 项目条件

> 支持于: 批处理, 流处理

通过选择列或将函数应用于列来变换输入数据集。

**变换类别**: 流行

## 声明的参数

* **条件以筛选列** - 输入模式中的所有列将被测试以查看它们是否符合此条件。如果符合，给定表达式将应用于它们。<br>*ColumnPredicate*
* **数据集** - 要应用操作的数据集。<br>*Table*
* **要应用的表达式** - 每个符合条件的列应用一次的表达式。<br>*Expression\<AnyType>*
* **保留剩余列** - 保留数据集中未投影的所有列。<br>*Literal\<Boolean>*
* *非必填* **保留匹配的列** - 保留由条件匹配的原始列。如果投影列具有相同名称，原始列将被覆盖。<br>*Literal\<Boolean>*

## 示例

### 示例 1: 基本情况

**描述**: 根据正则表达式重命名匹配的列。
**参数值:**

* **条件以筛选列**: <br>columnHasType(<br> type: String,<br>)
* **数据集**: ri.foundry.main.dataset.a
* **要应用的表达式**: <br>dynamicAlias(<br> expression: <br>cast(<br> expression: `column`,<br> type: Integer,<br>),<br> transformer: <br>columnNameRegexReplace(<br> input: `column`,<br> pattern: str,<br> replace: int,<br>),<br>)
* **保留剩余列**: true
* **保留匹配的列**: false

**输入:**

| id | distance\_str | factor\_str |
| ----- | ----- | ----- |
| 1 | 2000 | 1265 |

**输出:**

| distance\_int | factor\_int | id |
| ----- | ----- | ----- |
| 2000 | 1265 | 1 |

***

### 示例 2: 边缘情况

**描述**: 您可以选择保留匹配和剩余列。
**参数值:**

* **条件以筛选列**: <br>columnHasType(<br> type: String,<br>)
* **数据集**: ri.foundry.main.dataset.a
* **要应用的表达式**: <br>dynamicAlias(<br> expression: <br>cast(<br> expression: `column`,<br> type: Integer,<br>),<br> transformer: <br>columnNameConcat(<br> inputs: \[`column`, `_as_integer`],<br>),<br>)
* **保留剩余列**: true
* **保留匹配的列**: true

**输入:**

| id | distance |
| ----- | ----- |
| 1 | 2000 |

**输出:**

| distance\_as\_integer | id | distance |
| ----- | ----- | ----- |
| 2000 | 1 | 2000 |

***

### 示例 3: 边缘情况

**描述**: 您可以选择保留条件匹配的列，以及创建的新列。
**参数值:**

* **条件以筛选列**: <br>columnHasType(<br> type: String,<br>)
* **数据集**: ri.foundry.main.dataset.a
* **要应用的表达式**: <br>dynamicAlias(<br> expression: <br>cast(<br> expression: `column`,<br> type: Integer,<br>),<br> transformer: <br>columnNameConcat(<br> inputs: \[`column`, `_as_integer`],<br>),<br>)
* **保留剩余列**: false
* **保留匹配的列**: true

**输入:**

| id | distance |
| ----- | ----- |
| 1 | 2000 |

**输出:**

| distance\_as\_integer | distance |
| ----- | ----- |
| 2000 | 2000 |

***

### 示例 4: 边缘情况

**描述**: 当保留匹配列但投影列覆盖现有列时，匹配列将不会被保留。为了保留原始列，您必须将投影列重命名为新名称。
**参数值:**

* **条件以筛选列**: <br>columnHasType(<br> type: String,<br>)
* **数据集**: ri.foundry.main.dataset.a
* **要应用的表达式**: <br>cast(<br> expression: `column`,<br> type: Integer,<br>)
* **保留剩余列**: false
* **保留匹配的列**: true

**输入:**

| id | distance |
| ----- | ----- |
| 1 | 2000 |

**输出:**

| distance |
| ----- |
| 2000 |

***

### 示例 5: 边缘情况

**描述**: 您可以选择仅保留投影的列。
**参数值:**

* **条件以筛选列**: <br>columnHasType(<br> type: String,<br>)
* **数据集**: ri.foundry.main.dataset.a
* **要应用的表达式**: <br>dynamicAlias(<br> expression: <br>cast(<br> expression: `column`,<br> type: Integer,<br>),<br> transformer: <br>columnNameConcat(<br> inputs: \[`column`, `_as_integer`],<br>),<br>)
* **保留剩余列**: false
* **保留匹配的列**: false

**输入:**

| id | distance |
| ----- | ----- |
| 1 | 2000 |

**输出:**

| distance\_as\_integer |
| ----- |
| 2000 |

***

### 示例 6: 边缘情况

**描述**: 您可以选择仅保留未匹配条件的剩余列。
**参数值:**

* **条件以筛选列**: <br>columnHasType(<br> type: String,<br>)
* **数据集**: ri.foundry.main.dataset.a
* **要应用的表达式**: <br>cast(<br> expression: `column`,<br> type: Integer,<br>)
* **保留剩余列**: true
* **保留匹配的列**: false

**输入:**

| id | distance |
| ----- | ----- |
| 1 | 2000 |

**输出:**

| distance | id |
| ----- | ----- |
| 2000 | 1 |

***
