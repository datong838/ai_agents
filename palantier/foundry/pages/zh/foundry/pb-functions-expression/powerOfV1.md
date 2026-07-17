---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/powerOfV1/",
  "title": "幂函数",
  "page_id": "powerOfV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/positiveModuloV1/",
  "next": "/zh/foundry/pb-functions-expression/normalizeGeometryV2/",
  "scraped_at": "2026-07-13T05:56:53.412579+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 幂函数

> 支持：批处理，流处理

计算表达式的幂值。如果任何一个值为null，则返回null。

**表达式类别**：数值

## 声明的参数

* **指数** - 幂函数的指数。<br>*Expression\<Numeric>*
* **表达式** - 幂函数的底数。<br>*Expression\<Numeric>*

**输出类型：** *Double*

## 示例

### 示例 1: 基本情况

**参数值：**

* **指数**: 3
* **表达式**: 10

**输出：** 1000.0

***

### 示例 2: 基本情况

**参数值：**

* **指数**: 3.0
* **表达式**: 10

**输出：** 1000.0

***

### 示例 3: 空值情况

**描述**: 当参数之一为null时，输出将为null。
**参数值：**

* **指数**: *null*
* **表达式**: 10

**输出：** *null*

***

### 示例 4: 空值情况

**描述**: 当参数之一为null时，输出将为null。
**参数值：**

* **指数**: 3
* **表达式**: *null*

**输出：** *null*

***
