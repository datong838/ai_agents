---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/h3BufferV1/",
  "title": "缓冲 H3 索引",
  "page_id": "h3BufferV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/bitShiftRightV1/",
  "next": "/zh/foundry/pb-functions-expression/inverseHaversineV1/",
  "scraped_at": "2026-07-13T05:53:04.475506+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 缓冲 H3 索引

> 支持于: 批处理, 流处理

从一组 H3 索引创建距离 k 的缓冲区。

**表达式类别**: 地理空间

## 声明的参数

* **H3 索引数组** - 用于创建距离 k 的缓冲区的数组。<br>*Expression\<Array\<H3 Index>>*
* **距离 k** - 距离 k 表示 k 个 H3 单元的缓冲区。k 的值必须 >=0。<br>*Expression\<Integer>*

**输出类型:** *Array\<H3 Index>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **H3 索引数组**: `h3Array`
* **距离 k**: 0

| h3Array | **输出** |
| ----- | ----- |
| \[ 8528340bfffffff ] | \[ 8528340bfffffff ] |
| \[  ] | \[  ] |

***

### 示例 2: 基本情况

**参数值:**

* **H3 索引数组**: `h3Array`
* **距离 k**: 2

| h3Array | **输出** |
| ----- | ----- |
| \[ 8528340bfffffff ] | \[ 85283403fffffff, 85283407fffffff, 8528340bfffffff, 8528340ffffffff, 85283413fffffff, 85283417fffff... |
| \[ 85283403fffffff, 85283407fffffff, 8528341bfffffff, 852834cffffffff ] | \[ 85283403fffffff, 85283407fffffff, 8528340bfffffff, 8528340ffffffff, 85283413fffffff, 85283417fffff... |
| \[ 85283403fffffff, 85283407fffffff ] | \[ 85283403fffffff, 85283407fffffff, 8528340bfffffff, 8528340ffffffff, 85283413fffffff, 85283417fffff... |
| \[ 85283403fffffff, 852834cffffffff ] | \[ 85283403fffffff, 85283407fffffff, 8528340bfffffff, 8528340ffffffff, 85283413fffffff, 85283417fffff... |
| \[ 852835cffffffff, 8529a937fffffff ] | \[ 85283427fffffff, 85283437fffffff, 85283453fffffff, 8528345bfffffff, 852834c3fffffff, 852834cbfffff... |

***

### 示例 3: 空值情况

**参数值:**

* **H3 索引数组**: `h3Array`
* **距离 k**: 1

| h3Array | **输出** |
| ----- | ----- |
| *null* | *null* |
| \[ Invalid H3 ] | *null* |

***
