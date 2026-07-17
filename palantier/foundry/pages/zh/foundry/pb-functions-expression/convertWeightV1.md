---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/convertWeightV1/",
  "title": "在重量单位之间转换",
  "page_id": "convertWeightV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/convertTimeV1/",
  "next": "/zh/foundry/pb-functions-expression/jsonStringV2/",
  "scraped_at": "2026-07-13T05:53:41.990440+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在重量单位之间转换

> 支持于: 批处理, 流处理

**表达式类别**: 数值

## 声明的参数

* **当前单位的数量** - *无描述*<br>*Expression\<DefiniteNumeric>*
* **当前单位** - 转换前的单位。<br>*Enum\<Centigram, Decagram, Decigram, Grain, Gram, Hectogram, Kilogram, Long hundredweight, Megagram, Metric ton, and more ...>*
* **目标单位** - 转换后的期望单位。<br>*Enum\<Centigram, Decagram, Decigram, Grain, Gram, Hectogram, Kilogram, Long hundredweight, Megagram, Metric ton, and more ...>*

**输出类型:** *Double*

## 示例

### 示例 1: 基本情况

**参数值:**

* **当前单位的数量**: `kilograms`
* **当前单位**: `kilogram`
* **目标单位**: `gram`

| kilograms | **输出** |
| ----- | ----- |
| 5 | 5000.0 |

***

### 示例 2: 基本情况

**参数值:**

* **当前单位的数量**: `kilograms`
* **当前单位**: `kilogram`
* **目标单位**: `gram`

| kilograms | **输出** |
| ----- | ----- |
| *null* | *null* |

***
