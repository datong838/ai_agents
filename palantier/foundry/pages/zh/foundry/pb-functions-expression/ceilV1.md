---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/ceilV1/",
  "title": "Ceil",
  "page_id": "ceilV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/castV2/",
  "next": "/zh/foundry/pb-functions-expression/changeTimestampTimeZoneV1/",
  "scraped_at": "2026-07-13T05:53:09.463320+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Ceil

> 支持于: 批处理, 流处理

返回给定分数值的上限值。

**表达式类别**: 数值

## 声明的参数

* **表达式** - 分数输入值。<br>*Expression\<Decimal | Double | Float>*

**输出类型:** *Decimal | Long*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: 10.123

**输出:** 11

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: `number`

| number | **输出** |
| ----- | ----- |
| *null* | *null* |

***
