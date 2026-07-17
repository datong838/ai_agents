---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/complexInnerJoinV1/",
  "title": "内连接",
  "page_id": "complexInnerJoinV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/heartbeatDetectionV2/",
  "next": "/zh/foundry/pb-functions-transform/joinV2/",
  "scraped_at": "2026-07-13T05:58:35.748068+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 内连接

> 支持于: 批处理

合并两个数据集，仅保留满足每个表中提供条件的行。

**变换类别**: 合并

## 声明的参数

* **选择左侧列的条件** - 将测试左侧输入模式中的所有列以查看它们是否满足此条件。如果满足，列将被选择到输出中。<br>*ColumnPredicate*
* **选择右侧列的条件** - 将测试右侧输入模式中的所有列以查看它们是否满足此条件。如果满足，列将被选择到输出中。<br>*ColumnPredicate*
* **合并条件** - 用于合并的条件。<br>*Expression\<Boolean>*
* **左侧数据集** - 用于合并的左侧数据集。<br>*Table*
* **右侧数据集** - 用于合并的右侧数据集。<br>*Table*
* *非必填* **右侧列的前缀** - 添加到右侧所有列的前缀。<br>*Literal<字符串>*

## 示例

### 示例 1: 基本案例

**参数值:**

* **选择左侧列的条件**: <br>columnNameIsIn(<br> columnNames: \[tail\_number, airline],<br>)
* **选择右侧列的条件**: <br>columnNameIsIn(<br> columnNames: \[home\_airport],<br>)
* **合并条件**: <br>equals(<br> left: `tail_number`,<br> right: `tail_number`,<br>)
* **左侧数据集**: ri.foundry.main.dataset.left
* **右侧数据集**: ri.foundry.main.dataset.right
* **右侧列的前缀**: *null*

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

| tail\_number | airline | home\_airport |
| ----- | ----- | ----- |
| XB-123 | foundry air | LHR |
| MT-222 | new airline | CPH |
| XB-123 | foundry airline | LHR |
| MT-222 | new air | CPH |
| KK-452 | new air | JFK |
| XB-123 | foundry airline | LHR |

***

### 示例 2: 基本案例

**描述**: 简单复杂合并条件。
**参数值:**

* **选择左侧列的条件**: <br>columnNameIsIn(<br> columnNames: \[tail\_number, airline, factor],<br>)
* **选择右侧列的条件**: <br>columnNameIsIn(<br> columnNames: \[tail\_number, home\_airport, factor],<br>)
* **合并条件**: <br>lessThan(<br> left: `factor`,<br> right: `factor`,<br>)
* **左侧数据集**: ri.foundry.main.dataset.left
* **右侧数据集**: ri.foundry.main.dataset.right
* **右侧列的前缀**: right\_

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

| tail\_number | airline | factor | right\_tail\_number | right\_home\_airport | right\_factor |
| ----- | ----- | ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 2 | KK-452 | JFK | 10 |
| XB-123 | foundry air | 2 | JR-201 | IAD | 4 |
| MT-222 | new airline | 5 | KK-452 | JFK | 10 |
| XB-123 | foundry airline | 5 | KK-452 | JFK | 10 |
| MT-222 | new air | 4 | KK-452 | JFK | 10 |
| KK-452 | new air | 1 | XB-123 | LHR | 2 |
| KK-452 | new air | 1 | KK-452 | JFK | 10 |
| KK-452 | new air | 1 | JR-201 | IAD | 4 |
| PA-452 | new air | 2 | KK-452 | JFK | 10 |
| PA-452 | new air | 2 | JR-201 | IAD | 4 |
| XB-123 | foundry airline | 2 | KK-452 | JFK | 10 |
| XB-123 | foundry airline | 2 | JR-201 | IAD | 4 |

***

### 示例 3: 基本案例

**参数值:**

* **选择左侧列的条件**: <br>columnNameIsIn(<br> columnNames: \[tail\_number, airline, factor],<br>)
* **选择右侧列的条件**: <br>columnNameIsIn(<br> columnNames: \[home\_airport],<br>)
* **合并条件**: <br>and(<br> conditions: \[<br>equals(<br> left: `tail_number`,<br> right: `tail_number`,<br>), <br>equals(<br> left: `factor`,<br> right: `factor`,<br>)],<br>)
* **左侧数据集**: ri.foundry.main.dataset.left
* **右侧数据集**: ri.foundry.main.dataset.right
* **右侧列的前缀**: *null*

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

| tail\_number | airline | factor | home\_airport |
| ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 2 | LHR |
| XB-123 | foundry airline | 2 | LHR |

***

### 示例 4: 基本案例

**参数值:**

* **选择左侧列的条件**: <br>allColumns(<br><br>)
* **选择右侧列的条件**: <br>columnNameIsIn(<br> columnNames: \[home\_airport],<br>)
* **合并条件**: <br>equals(<br> left: `tail_number`,<br> right: `tail_number`,<br>)
* **左侧数据集**: ri.foundry.main.dataset.left
* **右侧数据集**: ri.foundry.main.dataset.right
* **右侧列的前缀**: *null*

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

| tail\_number | airline | miles | factor | home\_airport |
| ----- | ----- | ----- | ----- | ----- |
| XB-123 | foundry air | 124 | 2 | LHR |
| MT-222 | new airline | 1123 | 5 | CPH |
| XB-123 | foundry airline | 335 | 5 | LHR |
| MT-222 | new air | 565 | 4 | CPH |
| KK-452 | new air | 222 | 1 | JFK |
| XB-123 | foundry airline | 1134 | 2 | LHR |

***
