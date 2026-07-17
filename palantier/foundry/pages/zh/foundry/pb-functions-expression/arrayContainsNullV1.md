---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arrayContainsNullV1/",
  "title": "数组包含null",
  "page_id": "arrayContainsNullV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arrayContainsV1/",
  "next": "/zh/foundry/pb-functions-expression/arrayDifferenceV1/",
  "scraped_at": "2026-07-13T05:52:30.713034+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组包含null

> 支持于：批处理，流处理

如果`array`包含null，返回true。

**表达式类别**：数组，布尔值

## 声明的参数

* **表达式** - 一个可能包含null值的数组。<br>*Expression\<Array\<ComparableType>>*

**输出类型：** *布尔值*

## 示例

### 示例 1：基本情况

**参数值：**

* **表达式**: `part_ids`

| part\_ids | **输出** |
| ----- | ----- |
| \[ AWE-112, BRR-123, *null* ] | true |
| \[ AWE-222, ABC-543 ] | false |

***

### 示例 2：Null情况

**参数值：**

* **表达式**: `part_ids`

| part\_ids | **输出** |
| ----- | ----- |
| *null* | false |
| \[ AWE-222, ABC-543 ] | false |

***

### 示例 3：边缘情况

**参数值：**

* **表达式**: `part_ids`

| part\_ids | **输出** |
| ----- | ----- |
| \[  ] | false |

***
