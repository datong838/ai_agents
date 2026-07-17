---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/mappingJoinV1/",
  "title": "映射合并",
  "page_id": "mappingJoinV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/manuallyEnteredTableV1/",
  "next": "/zh/foundry/pb-functions-transform/narrowUnionByNameV1/",
  "scraped_at": "2026-07-13T05:58:45.232451+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 映射合并

> 支持于: 批处理

用映射数据集中值替换源数据集中目标列的值。

**变换类别**: 合并

## 声明的参数

* **输入数据集** - 包含要映射的列的源数据集。<br>*表格*
* **用于映射值的键列** - 用于映射值的键列。<br>*列\<T1>*
* **映射数据集** - 包含用于映射的值的数据集。<br>*表格*
* **目标列** - 左侧将被替换值的列列表。<br>*列表<列\<T1>>*
* **用于映射的值** - 用于映射的值。<br>*列\<T2>*
* *非必填* **假设唯一映射** - 如果为true，将对映射表的键列应用一个去重操作。如果为false，并且映射表包含重复的键，结果数据集将基于每个映射包含重复的行。默认情况下，将应用此操作。注意：将其设置为false可能会提高性能。<br>*字面量<布尔>*
* *非必填* **默认值** - 如果为空，当在映射表中找不到映射时，目标列的值将保持不变。默认情况下，这是空的。<br>*表达式\<T2>*

**类型变量界限：** *T1 接受任意类型\*\*T2 接受任意类型*

## 示例

### 示例 1: 基本案例

**参数值:**

* **输入数据集**: ri.foundry.main.dataset.input
* **用于映射值的键列**: `flight_code`
* **映射数据集**: ri.foundry.main.dataset.mapping
* **目标列**: \[`flight_no`, `next_flight`]
* **用于映射的值**: `flight_number`
* **假设唯一映射**: *null*
* **默认值**: unknown

**输入:**
ri.foundry.main.dataset.input

| flight\_no | next\_flight | departure\_time |
| ----- | ----- | ----- |
| 533 | 112 | 2022-01-20T10:45:00Z |
| 934 | 533 | 2022-01-20T11:20:00Z |
| 222 | 934 | 2022-01-20T11:20:00Z |

ri.foundry.main.dataset.mapping

| flight\_code | flight\_number | airline |
| ----- | ----- | ----- |
| 112 | XB-123 | foundry airlines |
| 533 | MT-444 | foundry airlines |
| 934 | KK-123 | new air |

**输出:**

| flight\_no | next\_flight | departure\_time |
| ----- | ----- | ----- |
| MT-444 | XB-123 | 2022-01-20T10:45:00Z |
| KK-123 | MT-444 | 2022-01-20T11:20:00Z |
| unknown | KK-123 | 2022-01-20T11:20:00Z |

***
