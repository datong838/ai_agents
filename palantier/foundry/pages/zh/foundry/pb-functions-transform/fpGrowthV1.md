---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/fpGrowthV1/",
  "title": "频繁模式增长",
  "page_id": "fpGrowthV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/flattenStructV1/",
  "next": "/zh/foundry/pb-functions-transform/geoDistanceInnerJoinV1/",
  "scraped_at": "2026-07-13T05:58:28.963171+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 频繁模式增长

> 支持于: 批处理

频繁模式（fp）增长在您的数据集中查找频繁模式。

**变换类别**: 聚合, 其他

## 声明的参数

* **输入数据集** - 包含项目列和事务列的源数据集。<br>*表格*
* **项目列** - 包含模式项目的数组列。<br>*列<数组<字符串>>*
* **最小支持度** - 模式需要出现的最小频率。<br>*字面值<双精度>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **输入数据集**: ri.foundry.main.dataset.a
* **项目列**: `customer_attributes`
* **最小支持度**: 0.6

**输入:**

| customer\_attributes |
| ----- |
| \[ age\_group: 20-30, country: Germany, gender: Female ] |
| \[ age\_group: 20-30, country: Germany, gender: Male ] |

**输出:**

| pattern | pattern\_occurrence | total\_count |
| ----- | ----- | ----- |
| \[ country: Germany, age\_group: 20-30 ] | 2 | 2 |
| \[ age\_group: 20-30 ] | 2 | 2 |
| \[ country: Germany ] | 2 | 2 |

***

### 示例 2: 空情况

**参数值:**

* **输入数据集**: ri.foundry.main.dataset.a
* **项目列**: `customer_attributes`
* **最小支持度**: 0.0

**输入:**

| customer\_attributes |
| ----- |
| *null* |

**输出:**

| pattern | pattern\_occurrence | total\_count |
| ----- | ----- | ----- |

***

### 示例 3: 空情况

**参数值:**

* **输入数据集**: ri.foundry.main.dataset.a
* **项目列**: `customer_attributes`
* **最小支持度**: 0.0

**输入:**

| customer\_attributes |
| ----- |
| \[ age\_group: 20-30, country: Germany, gender: Female ] |
| \[ *null* ] |

**输出:**

| pattern | pattern\_occurrence | total\_count |
| ----- | ----- | ----- |
| \[ country: Germany ] | 1 | 2 |
| \[ country: Germany, age\_group: 20-30 ] | 1 | 2 |
| \[ *null* ] | 1 | 2 |
| \[ age\_group: 20-30 ] | 1 | 2 |
| \[ gender: Female ] | 1 | 2 |
| \[ gender: Female, country: Germany ] | 1 | 2 |
| \[ gender: Female, country: Germany, age\_group: 20-30 ] | 1 | 2 |
| \[ gender: Female, age\_group: 20-30 ] | 1 | 2 |

***

### 示例 4: 边缘情况

**参数值:**

* **输入数据集**: ri.foundry.main.dataset.a
* **项目列**: `customer_attributes`
* **最小支持度**: 0.0

**输入:**

| customer\_attributes |
| ----- |
| \[ age\_group: 20-30, country: Germany, gender: Female ] |
| \[ age\_group: 20-30, country: Germany, gender: Male ] |

**输出:**

| pattern | pattern\_occurrence | total\_count |
| ----- | ----- | ----- |
| \[ gender: Male ] | 1 | 2 |
| \[ gender: Male, country: Germany ] | 1 | 2 |
| \[ gender: Male, country: Germany, age\_group: 20-30 ] | 1 | 2 |
| \[ gender: Male, age\_group: 20-30 ] | 1 | 2 |
| \[ age\_group: 20-30 ] | 2 | 2 |
| \[ country: Germany ] | 2 | 2 |
| \[ country: Germany, age\_group: 20-30 ] | 2 | 2 |
| \[ gender: Female ] | 1 | 2 |
| \[ gender: Female, country: Germany ] | 1 | 2 |
| \[ gender: Female, country: Germany, age\_group: 20-30 ] | 1 | 2 |
| \[ gender: Female, age\_group: 20-30 ] | 1 | 2 |

***
