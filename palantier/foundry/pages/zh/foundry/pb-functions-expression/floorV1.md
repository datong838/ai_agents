---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/floorV1/",
  "title": "Floor",
  "page_id": "floorV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/firstNonNullV1/",
  "next": "/zh/foundry/pb-functions-expression/dateToStringV2/",
  "scraped_at": "2026-07-13T05:54:49.201339+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Floor

> 支持于: 批处理, 流处理

返回给定小数值的向下取整值。

**表达式类别**: 数值

## 声明的参数

* **表达式** - 要向下取整的值。<br>*表达式\<Decimal | Double | Float>*

**输出类型:** *Decimal | Long*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: 10.123

**输出:** 10

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: `number`

| number | **输出** |
| ----- | ----- |
| *null* | *null* |

***
