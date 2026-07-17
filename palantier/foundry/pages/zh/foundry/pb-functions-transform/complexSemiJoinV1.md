---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/complexSemiJoinV1/",
  "title": "半连接",
  "page_id": "complexSemiJoinV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/selectV1/",
  "next": "/zh/foundry/pb-functions-transform/sortV2/",
  "scraped_at": "2026-07-13T05:59:10.355524+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 半连接

> 支持于: 批处理

半连接将左侧和右侧的数据集输入合并在一起。这会删除所有不符合连接条件的行。

**变换类别**: 合并

## 声明的参数

* **左侧选择列的条件** - 所有左侧输入模式中的列将被测试以查看它们是否符合此条件。如果符合，列将在输出中被选择。<br>*ColumnPredicate*
* **连接条件** - 用于连接的条件。<br>*Expression\<Boolean>*
* **左侧数据集** - 用于合并的左侧数据集。<br>*Table*
* **右侧数据集** - 用于合并的右侧数据集。<br>*Table*

## 示例

### 示例 1: 基本情况

**参数值:**

* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[tail\_number, airline],<br>)
* **连接条件**: <br>equals(<br> left: `tail_number`,<br> right: `tail_number`,<br>)
* **左侧数据集**: ri.foundry.main.dataset.left
* **右侧数据集**: ri.foundry.main.dataset.right

**输入:**
ri.foundry.main.dataset.left

| tail\_number | airline | miles | factor |
| ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 124 | 2 |
| MT-222 | new airline | 1123 | 5 |
| XB-123 | foundry airline | 335 | 5 |
| MT-222 | new air | 565 | 4 |
| KK-452 | new air | 222 | 1 |
| PA-452 | new air | 212 | 2 |
| XB-123 | foundry airline | 1134 | 2 |

ri.foundry.main.dataset.right

| tail\_number | home\_airport |
| ----- | ----- |
| XB-123 | LHR |
| MT-222 | CPH |
| KK-452 | JFK |
| JR-201 | IAD |

**输出:**

| tail\_number | airline |
| ----- | ----- |
| XB-123 | foundry air |
| MT-222 | new airline |
| XB-123 | foundry airline |
| MT-222 | new air |
| KK-452 | new air |
| XB-123 | foundry airline |

***

### 示例 2: 基本情况

**描述**: 简单复杂连接条件。
**参数值:**

* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[tail\_number, airline, factor],<br>)
* **连接条件**: <br>and(<br> conditions: \[<br>lessThan(<br> left: `factor`,<br> right: `factor`,<br>), <br>equals(<br> left: `tail_number`,<br> right: `tail_number`,<br>)],<br>)
* **左侧数据集**: ri.foundry.main.dataset.left
* **右侧数据集**: ri.foundry.main.dataset.right

**输入:**
ri.foundry.main.dataset.left

| tail\_number | airline | miles | factor |
| ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 124 | 2 |
| MT-222 | new airline | 1123 | 5 |
| XB-123 | foundry airline | 335 | 5 |
| MT-222 | new air | 565 | 4 |
| KK-452 | new air | 222 | 1 |
| PA-452 | new air | 212 | 2 |
| XB-123 | foundry airline | 1134 | 2 |

ri.foundry.main.dataset.right

| tail\_number | home\_airport | factor |
| ----- | ----- | ----- |
| XB-123 | LHR | 2 |
| MT-222 | CPH | 1 |
| KK-452 | JFK | 10 |
| JR-201 | IAD | 4 |

**输出:**

| tail\_number | airline | factor |
| ----- | ----- | ----- |
| KK-452 | new air | 1 |

***

### 示例 3: 基本情况

**参数值:**

* **左侧选择列的条件**: <br>columnNameIsIn(<br> columnNames: \[tail\_number, airline, factor],<br>)
* **连接条件**: <br>and(<br> conditions: \[<br>equals(<br> left: `tail_number`,<br> right: `tail_number`,<br>), <br>equals(<br> left: `factor`,<br> right: `factor`,<br>)],<br>)
* **左侧数据集**: ri.foundry.main.dataset.left
* **右侧数据集**: ri.foundry.main.dataset.right

**输入:**
ri.foundry.main.dataset.left

| tail\_number | airline | miles | factor |
| ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 124 | 2 |
| MT-222 | new airline | 1123 | 5 |
| XB-123 | foundry airline | 335 | 5 |
| MT-222 | new air | 565 | 4 |
| KK-452 | new air | 222 | 1 |
| PA-452 | new air | 212 | 2 |
| XB-123 | foundry airline | 1134 | 2 |

ri.foundry.main.dataset.right

| tail\_number | home\_airport | factor |
| ----- | ----- | ----- |
| XB-123 | LHR | 2 |
| MT-222 | CPH | 1 |
| KK-452 | JFK | 10 |
| JR-201 | IAD | 4 |

**输出:**

| tail\_number | airline | factor |
| ----- | ----- | ----- |
| XB-123 | foundry air | 2 |
| XB-123 | foundry airline | 2 |

***

### 示例 4: 基本情况

**参数值:**

* **左侧选择列的条件**: <br>allColumns(<br><br>)
* **连接条件**: <br>equals(<br> left: `tail_number`,<br> right: `tail_number`,<br>)
* **左侧数据集**: ri.foundry.main.dataset.left
* **右侧数据集**: ri.foundry.main.dataset.right

**输入:**
ri.foundry.main.dataset.left

| tail\_number | airline | miles | factor |
| ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 124 | 2 |
| MT-222 | new airline | 1123 | 5 |
| XB-123 | foundry airline | 335 | 5 |
| MT-222 | new air | 565 | 4 |
| KK-452 | new air | 222 | 1 |
| PA-452 | new air | 212 | 2 |
| XB-123 | foundry airline | 1134 | 2 |

ri.foundry.main.dataset.right

| tail\_number | home\_airport |
| ----- | ----- |
| XB-123 | LHR |
| MT-222 | CPH |
| KK-452 | JFK |
| JR-201 | IAD |

**输出:**

| tail\_number | airline | miles | factor |
| ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 124 | 2 |
| MT-222 | new airline | 1123 | 5 |
| XB-123 | foundry airline | 335 | 5 |
| MT-222 | new air | 565 | 4 |
| KK-452 | new air | 222 | 1 |
| XB-123 | foundry airline | 1134 | 2 |

***
