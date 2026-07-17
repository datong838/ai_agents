---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/moduloV1/",
  "title": "Modulo",
  "page_id": "moduloV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/modeV1/",
  "next": "/zh/foundry/pb-functions-expression/multiplyV2/",
  "scraped_at": "2026-07-13T05:56:31.053928+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Modulo

> 支持于: 批处理, 流处理

返回表达式的模。

**表达式类别**: 数值

## 声明的参数

* **分母** - *无描述*<br>*Expression\<DefiniteNumeric>*
* **分子** - *无描述*<br>*Expression\<DefiniteNumeric>*

**输出类型:** *DefiniteNumeric*

## 示例

### 示例 1: 基本情况

**参数值:**

* **分母**: 4
* **分子**: 10.123

**输出:** 2.123

***

### 示例 2: 基本情况

**参数值:**

* **分母**: 2
* **分子**: *null*

**输出:** *null*

***
