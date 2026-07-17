---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/logNV1/",
  "title": "以指定底数计算对数",
  "page_id": "logNV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/logV1/",
  "next": "/zh/foundry/pb-functions-expression/logicalTypeCastV1/",
  "scraped_at": "2026-07-13T05:56:21.515304+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 以指定底数计算对数

> 支持于: 批处理, 流处理

计算以给定底数的对数。

**表达式类别**: 数值型

## 声明的参数

* **底数** - *无描述*<br>*Literal\<Double>*
* **表达式** - *无描述*<br>*Expression\<Numeric>*

**输出类型:** *Double*

## 示例

### 示例 1: 基础情况

**参数值:**

* **底数**: 2.0
* **表达式**: 8

**输出:** 3.0

***

### 示例 2: 空值情况

**参数值:**

* **底数**: 2.0
* **表达式**: *null*

**输出:** *null*

***
