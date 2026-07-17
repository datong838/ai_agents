---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/pivotV1/",
  "title": "透视表",
  "page_id": "pivotV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/complexOuterJoinV1/",
  "next": "/zh/foundry/pb-functions-transform/projectV1/",
  "scraped_at": "2026-07-13T05:58:50.823920+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 透视表

> 支持于: 批处理

对按一组列分组的输入数据集执行指定的聚合操作。必须提供用于透视的唯一值，以便提前知道输出模式。这提高了运行时的稳定性。

**变换类别**: 聚合, 热门

## 声明的参数

* **聚合** - 在数据集上执行的聚合列表。<br>*List\<Expression\<AnyType>>*
* **数据集** - 要进行聚合的数据集。<br>*Table*
* **按列分组** - 聚合时按列分组数据集的列列表。<br>*List\<Column\<AnyType>>*
* **透视列** - 用于透视的列。<br>*Column\<T>*
* **透视值** - 用于透视的唯一值列表和输出的别名。别名值用于根据前缀/后缀参数构造输出列名。<br>*List\<Tuple\<Literal\<T>, Literal<字符串>>>*
* **前缀或后缀别名**（非必填） - 如果是前缀，输出列名将为 'alias'*'aggregate'，如果是后缀，则为 'aggregate'*`alias`。<br>*Enum\<Prefix, Suffix>*

**类型变量界限：** *T 接受 Boolean | Byte | Integer | Long | Short | 字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **聚合**: \[<br>alias(<br> alias: miles,<br> expression: <br>mean(<br> expression: `miles`,<br>),<br>)]
* **数据集**: ri.foundry.main.dataset.a
* **按列分组**: \[`airline`]
* **透视列**: `airport`
* **透视值**: \[(JFK, new\_york), (LHR, london)]
* **前缀或后缀别名**: *null*

**输入:**

| airline | airport | miles |
| ----- | ----- | ----- |
| foundry airways | JFK | 1002345 |
| foundry airways | LHR | 2221324 |
| new air | SFO | 21356673 |
| new air | JFK | 12323456 |
| foundry airways | LHR | 12542352 |
| new air | JFK | 12232355 |

**输出:**

| airline | new\_york\_miles | london\_miles |
| ----- | ----- | ----- |
| foundry airways | 1002345.0 | 7381838.0 |
| new air | 1.22779055E7 | *null* |

***

### 示例 2: 基本情况

**参数值:**

* **聚合**: \[<br>alias(<br> alias: miles,<br> expression: <br>mean(<br> expression: `miles`,<br>),<br>)]
* **数据集**: ri.foundry.main.dataset.a
* **按列分组**: \[`airline`]
* **透视列**: `airport`
* **透视值**: \[(JFK, new\_york), (LHR, london)]
* **前缀或后缀别名**: `SUFFIX`

**输入:**

| airline | airport | miles |
| ----- | ----- | ----- |
| foundry airways | JFK | 1002345 |
| foundry airways | LHR | 2221324 |
| new air | SFO | 21356673 |
| new air | JFK | 12323456 |
| foundry airways | LHR | 12542352 |
| new air | JFK | 12232355 |

**输出:**

| airline | miles\_new\_york | miles\_london |
| ----- | ----- | ----- |
| foundry airways | 1002345.0 | 7381838.0 |
| new air | 1.22779055E7 | *null* |

***
