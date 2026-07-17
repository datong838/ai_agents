---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/kmeansV1/",
  "title": "K-means 聚类",
  "page_id": "kmeansV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/joinV2/",
  "next": "/zh/foundry/pb-functions-transform/keepDuplicatesV1/",
  "scraped_at": "2026-07-13T05:58:39.368965+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# K-means 聚类

> 支持于: 批处理

K-means 聚类是一种无监督机器学习算法。它将数据集向量分组到 k 个簇中。通过计算指定范围内从最小 k 到最大 k 的最佳轮廓系数来确定 k 值。k 值的数量定义了在此范围内应尝试多少个 k 值，包括边界。

**变换类别**: 其他

## 声明的参数

* **输入数据集** - 包含向量列的源数据集。<br>*Table*
* **最大 k** - 最大簇数。<br>*Literal\<Integer>*
* **最小 k** - 最小簇数。<br>*Literal\<Integer>*
* **k 值的数量** - 要测试的 k 值数量，从最小 k 到最大 k 的值。注意，我们将训练数量为 k 的聚类模型，因此如果 k 值的数量设置为较高的值，管道执行可能会比较慢。最佳模型基于轮廓系数选择。<br>*Literal\<Integer>*
* **向量列** - 包含将用于聚类的浮点向量的列。<br>*Column\<Array\<Float>>*

## 示例

### 示例 1: 基本案例

**参数值:**

* **输入数据集**: ri.foundry.main.dataset.a
* **最大 k**: 12
* **最小 k**: 3
* **k 值的数量**: 4
* **向量列**: `feature_column`

**输入:**

| feature\_column |
| ----- |
| \[ 0.05, 3.1, 2.3 ] |
| \[ 1.0, 3.1, 2.3 ] |
| \[ 1.0, 3.5, 2.3 ] |
| \[ 19.0, 12.3, -1.4 ] |

**输出:**

| feature\_column | cluster\_id |
| ----- | ----- |
| \[ 1.0, 3.1, 2.3 ] | 0 |
| \[ 1.0, 3.5, 2.3 ] | 0 |
| \[ 19.0, 12.3, -1.4 ] | 1 |
| \[ 0.05, 3.1, 2.3 ] | 2 |

***

### 示例 2: 空案例

**参数值:**

* **输入数据集**: ri.foundry.main.dataset.a
* **最大 k**: 12
* **最小 k**: 3
* **k 值的数量**: 4
* **向量列**: `feature_column`

**输入:**

| feature\_column |
| ----- |
| \[ 0.05, 3.1, 2.3 ] |
| *null* |
| \[ 1.0, 3.1, 2.3 ] |
| \[ 1.0, 3.5, 2.3 ] |
| \[ 19.0, 12.3, -1.4 ] |

**输出:**

| feature\_column | cluster\_id |
| ----- | ----- |
| \[ 1.0, 3.1, 2.3 ] | 0 |
| \[ 1.0, 3.5, 2.3 ] | 0 |
| \[ 19.0, 12.3, -1.4 ] | 1 |
| \[ 0.05, 3.1, 2.3 ] | 2 |

***

### 示例 3: 边缘案例

**参数值:**

* **输入数据集**: ri.foundry.main.dataset.a
* **最大 k**: 3
* **最小 k**: 3
* **k 值的数量**: 1
* **向量列**: `feature_column`

**输入:**

| feature\_column |
| ----- |
| \[ 0.05, 3.1, 2.3 ] |
| \[ 1.0, 3.5, 2.3 ] |
| \[ 19.0, 12.3, -1.4 ] |

**输出:**

| feature\_column | cluster\_id |
| ----- | ----- |
| \[ 19.0, 12.3, -1.4 ] | 0 |
| \[ 0.05, 3.1, 2.3 ] | 1 |
| \[ 1.0, 3.5, 2.3 ] | 2 |

***
