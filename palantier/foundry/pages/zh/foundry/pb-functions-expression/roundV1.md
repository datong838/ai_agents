---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/roundV1/",
  "title": "数字取整",
  "page_id": "roundV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/rightPadV1/",
  "next": "/zh/foundry/pb-functions-expression/rowCountV1/",
  "scraped_at": "2026-07-13T05:57:19.236348+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数字取整

> 支持于: 批处理, 流处理

将数字取整到“scale”个小数位。

**表达式类别**: 数值

## 声明的参数

* **列** - 要进行取整的列。<br>*表达式\<Decimal | Double | Float>*
* **非必填** **Scale** - 要取整的小数位数，默认为0。<br>*字面量\<Integer>*

**输出类型:** *Decimal | Double | Float*

## 示例

### 示例 1: 基本情况

**参数值:**

* **列**: 10.123
* **Scale**: 2

**输出:** 10.12

***

### 示例 2: 基本情况

**参数值:**

* **列**: 10.123
* **Scale**: *null*

**输出:** 10.0

***

### 示例 3: 基本情况

**参数值:**

* **列**: `number`
* **Scale**: 2

| number | **输出** |
| ----- | ----- |
| *null* | *null* |

***

### 示例 4: 基本情况

**参数值:**

* **列**: `number`
* **Scale**: 0

| number | **输出** |
| ----- | ----- |
| 32352366881234567890123456789012345678 | 32352366881234567890123456789012345678 |

***

### 示例 5: 基本情况

**参数值:**

* **列**: `number`
* **Scale**: -38

| number | **输出** |
| ----- | ----- |
| 10000000000000000000000000000000000078 | 0 |

***

### 示例 6: 基本情况

**参数值:**

* **列**: `number`
* **Scale**: -1

| number | **输出** |
| ----- | ----- |
| 10000000000000000000000000000000000078 | 10000000000000000000000000000000000080 |

***
