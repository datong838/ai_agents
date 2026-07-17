---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/dateSubV2/",
  "title": "从日期中减去值",
  "page_id": "dateSubV2",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/timestampDiffV1/",
  "next": "/zh/foundry/pb-functions-expression/sumV1/",
  "scraped_at": "2026-07-13T05:57:39.901908+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从日期中减去值

> 支持于: 批处理, 流处理

返回'开始'之前'value'天/周/月/季度/年的日期。

**表达式类别**: 日期时间

## 声明的参数

* **日期** - 要减去值的日期。<br>*表达式\<Date>*
* **单位** - 'value'参数的日期单位。<br>*枚举<天, 月, 季度, 周, 年>*
* **值** - 要减去的天数/周数/季度数/年数。<br>*表达式<整数>*

**输出类型:** *日期*

## 示例

### 示例 1: 基本情况

**参数值:**

* **日期**: 2022-04-05
* **单位**: `DAYS`
* **值**: 2

**输出:** 2022-04-03

***

### 示例 2: 基本情况

**参数值:**

* **日期**: 2022-04-05
* **单位**: `MONTHS`
* **值**: 2

**输出:** 2022-02-05

***

### 示例 3: 基本情况

**参数值:**

* **日期**: 2022-04-05
* **单位**: `QUARTERS`
* **值**: 2

**输出:** 2021-10-05

***

### 示例 4: 基本情况

**参数值:**

* **日期**: 2022-04-05
* **单位**: `YEARS`
* **值**: 2

**输出:** 2020-04-05

***

### 示例 5: 空值情况

**参数值:**

* **日期**: `date`
* **单位**: `YEARS`
* **值**: `value`

| 日期 | 值 | **输出** |
| ----- | ----- | ----- |
| 2022-04-05 | *null* | *null* |
| *null* | 2 | *null* |
| *null* | *null* | *null* |

***
