---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/positiveModuloV1/",
  "title": "正数模",
  "page_id": "positiveModuloV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/pivotExpressionV1/",
  "next": "/zh/foundry/pb-functions-expression/powerOfV1/",
  "scraped_at": "2026-07-13T05:56:55.587275+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 正数模

> 支持于: 批处理

返回表达式的正模。

**表达式类别**: 数值

## 声明的参数

* **分母** - *无描述*<br>*Expression\<T2>*
* **分子** - *无描述*<br>*Expression\<T1>*

**类型变量界限：** *T1 接受 Byte | Integer | Long | Short\*\*T2 接受 Byte | Integer | Long | Short*

**输出类型：** *T1*

## 示例

### 示例 1: 基本情况

**参数值：**

* **分母**: 3
* **分子**: 10

**输出：** 1

***

### 示例 2: 空值情况

**参数值：**

* **分母**: *null*
* **分子**: 10

**输出：** *null*

***

### 示例 3: 空值情况

**参数值：**

* **分母**: 3
* **分子**: *null*

**输出：** *null*

***
