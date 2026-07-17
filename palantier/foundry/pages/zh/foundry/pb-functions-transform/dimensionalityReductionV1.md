---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/dimensionalityReductionV1/",
  "title": "降维",
  "page_id": "dimensionalityReductionV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/dateDistributionV1/",
  "next": "/zh/foundry/pb-functions-transform/dropV1/",
  "scraped_at": "2026-07-13T05:58:13.344467+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 降维

> 支持于: Batch

通过应用主成分分析，将n维数组降维为k维数组。

**变换类别**: 其他

## 声明的参数

* **列** - 将应用降维的数组所在列。<br>*Column\<Embedded vector | Embedded vector>*
* **数据集** - 要应用降维的数据集。<br>*Table*
* *非必填* **输出维度** - 降维后输出数组的维度。<br>*Literal\<Integer>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **列**: `array`
* **数据集**: ri.foundry.main.dataset.a
* **输出维度**: 2

**输入:**

| array |
| ----- |
| \[ 1.0, 2.0, 3.0 ] |
| \[ 4.0, 5.0, 6.0 ] |
| \[ 7.0, 8.0, 9.0 ] |
| \[ 10.0, 11.0, 12.0 ] |

**输出:**

| array | array\_pca |
| ----- | ----- |
| \[ 1.0, 2.0, 3.0 ] | \[ -3.46, 1.36 ] |
| \[ 4.0, 5.0, 6.0 ] | \[ -8.66, 1.36 ] |
| \[ 7.0, 8.0, 9.0 ] | \[ -13.85, 1.36 ] |
| \[ 10.0, 11.0, 12.0 ] | \[ -19.05, 1.36 ] |

***

### 示例 2: 基本情况

**参数值:**

* **列**: `array`
* **数据集**: ri.foundry.main.dataset.a
* **输出维度**: 3

**输入:**

| array |
| ----- |
| \[ 1.0, 2.0, 3.0, 4.0, 5.0 ] |
| \[ 6.0, 7.0, 8.0, 9.0, 10.0 ] |
| \[ 11.0, 12.0, 13.0, 14.0, 15.0 ] |
| \[ 16.0, 17.0, 18.0, 19.0, 20.0 ] |

**输出:**

| array | array\_pca |
| ----- | ----- |
| \[ 1.0, 2.0, 3.0, 4.0, 5.0 ] | \[ -6.71, -2.24, -1.73 ] |
| \[ 6.0, 7.0, 8.0, 9.0, 10.0 ] | \[ -17.89, -2.24, -1.73 ] |
| \[ 11.0, 12.0, 13.0, 14.0, 15.0 ] | \[ -29.07, -2.24, -1.73 ] |
| \[ 16.0, 17.0, 18.0, 19.0, 20.0 ] | \[ -40.25, -2.24, -1.73 ] |

***

### 示例 3: 空值情况

**参数值:**

* **列**: `array`
* **数据集**: ri.foundry.main.dataset.a
* **输出维度**: 2

**输入:**

| array |
| ----- |
| \[ 1.0, *null* ] |
| \[ *null*, *null* ] |
| \[ *null*, 1.0 ] |

**输出:**

| array | array\_pca |
| ----- | ----- |
| \[ 1.0, *null* ] | \[ -0.7, 0.7 ] |
| \[ *null*, *null* ] | \[ 0.0, 0.0 ] |
| \[ *null*, 1.0 ] | \[ 0.7, 0.7 ] |

***

### 示例 4: 空值情况

**参数值:**

* **列**: `array`
* **数据集**: ri.foundry.main.dataset.a
* **输出维度**: 2

**输入:**

| array |
| ----- |
| \[ 1.0, *null* ] |
| *null* |
| \[ *null*, 1.0 ] |

**输出:**

| array | array\_pca |
| ----- | ----- |
| \[ 1.0, *null* ] | \[ -0.7, 0.7 ] |
| \[ *null*, 1.0 ] | \[ 0.7, 0.7 ] |

***
