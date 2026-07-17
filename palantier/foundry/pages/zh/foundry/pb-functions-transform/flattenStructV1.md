---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/flattenStructV1/",
  "title": "扁平化结构",
  "page_id": "flattenStructV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/firstUnionByNameV1/",
  "next": "/zh/foundry/pb-functions-transform/fpGrowthV1/",
  "scraped_at": "2026-07-13T05:58:26.332931+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 扁平化结构

> 支持于: 批处理, 流处理

将结构中的所有字段转换为输出数据集中列。

**变换类别**: 结构

## 声明的参数

* **数据集** - 包含结构列的数据集。<br>*表格*
* **表达式** - 评估为将被扁平化的结构列的表达式。<br>*表达式<结构>*
* **最大深度** - 指定嵌套结构将被扁平化的深度级别。<br>*字面值<整数>*
* *非必填* **列前缀** - 为在扁平化过程中创建的所有列添加前缀。<br>*字面值<字符串>*
* *非必填* **分隔符** - 分隔来自嵌套结构的字段名称。<br>*字面值<字符串>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **数据集**: ri.foundry.main.dataset.a
* **表达式**: `raw`
* **最大深度**: 2
* **列前缀**: new\_
* **分隔符**: *null*

**输入:**

| raw |
| ----- |
| {<br> **airline**: {<br> **id**: NA,<br> **name**: new air,<br>},<br> **tail\_no**: NA-123,<br>} |
| {<br> **airline**: {<br> **id**: FA,<br> **name**: foundry airways,<br>},<br> **tail\_no**: FA-123,<br>} |

**输出:**

| new\_airline\_name | new\_airline\_id | new\_tail\_no | raw |
| ----- | ----- | ----- | ----- |
| new air | NA | NA-123 | {<br> **airline**: {<br> **id**: NA,<br> **name**: new air,<br>},<br> **tail\_no**: NA-123,<br>} |
| foundry airways | FA | FA-123 | {<br> **airline**: {<br> **id**: FA,<br> **name**: foundry airways,<br>},<br> **tail\_no**: FA-123,<br>} |

***

### 示例 2: 基本情况

**参数值:**

* **数据集**: ri.foundry.main.dataset.a
* **表达式**: `raw`
* **最大深度**: 2
* **列前缀**: new\_
* **分隔符**: #SEPARATOR#

**输入:**

| raw |
| ----- |
| {<br> **airline**: {<br> **id**: NA,<br> **name**: new air,<br>},<br> **tail\_no**: NA-123,<br>} |
| {<br> **airline**: {<br> **id**: FA,<br> **name**: foundry airways,<br>},<br> **tail\_no**: FA-123,<br>} |

**输出:**

| new\_airline#SEPARATOR#name | new\_airline#SEPARATOR#id | new\_tail\_no | raw |
| ----- | ----- | ----- | ----- |
| new air | NA | NA-123 | {<br> **airline**: {<br> **id**: NA,<br> **name**: new air,<br>},<br> **tail\_no**: NA-123,<br>} |
| foundry airways | FA | FA-123 | {<br> **airline**: {<br> **id**: FA,<br> **name**: foundry airways,<br>},<br> **tail\_no**: FA-123,<br>} |

***

### 示例 3: 空值情况

**参数值:**

* **数据集**: ri.foundry.main.dataset.a
* **表达式**: `raw`
* **最大深度**: 2
* **列前缀**: new\_
* **分隔符**: *null*

**输入:**

| raw |
| ----- |
| *null* |
| {<br> **airline**: *null*,<br> **tail\_no**: NA-123,<br>} |
| {<br> **airline**: {<br> **id**: FA,<br> **name**: *null*,<br>},<br> **tail\_no**: FA-123,<br>} |

**输出:**

| new\_airline\_name | new\_airline\_id | new\_tail\_no | raw |
| ----- | ----- | ----- | ----- |
| *null* | *null* | *null* | *null* |
| *null* | *null* | NA-123 | {<br> **airline**: *null*,<br> **tail\_no**: NA-123,<br>} |
| *null* | FA | FA-123 | {<br> **airline**: {<br> **id**: FA,<br> **name**: *null*,<br>},<br> **tail\_no**: FA-123,<br>} |

***
