---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/formatStringV1/",
  "title": "格式化字符串",
  "page_id": "formatStringV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/formatNumberV1/",
  "next": "/zh/foundry/pb-functions-expression/timestampToStringV2/",
  "scraped_at": "2026-07-13T05:54:51.596411+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 格式化字符串

> 支持于: 批处理, 流处理

以printf样式格式化字符串。

**表达式类别**: 字符串

## 声明的参数

* **格式参数** - 要插入到格式字符串中的参数列表。<br>*List\<Expression\<Boolean | Byte | Date | Decimal | Double | Float | Integer | Long | Short | 字符串 | Timestamp>>*
* **格式字符串** - 要格式化的字符串。<br>*Literal<字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本案例

**参数值:**

* **格式参数**: \[`argument1`, `argument2`]
* **格式字符串**: Hello %s, my name is %s

| argument1 | argument2 | **输出** |
| ----- | ----- | ----- |
| Alice | Bob | Hello Alice, my name is Bob |
| Jane | John | Hello Jane, my name is John |

***

### 示例 2: 基本案例

**描述**: 格式化一个整数。
**参数值:**

* **格式参数**: \[4]
* **格式字符串**: number = %d

**输出:** number = 4

***

### 示例 3: 基本案例

**描述**: 格式化一个带符号和4位小数的双精度数。
**参数值:**

* **格式参数**: \[2.718281828459045]
* **格式字符串**: e = %+.4f

**输出:** e = +2.7183

***

### 示例 4: 空值案例

**参数值:**

* **格式参数**: \[`argument1`, `argument2`]
* **格式字符串**: Hello %s, my name is %s

| argument1 | argument2 | **输出** |
| ----- | ----- | ----- |
| *null* | Bob | Hello null, my name is Bob |
| Alice | *null* | Hello Alice, my name is null |
| *null* | *null* | Hello null, my name is null |

***
