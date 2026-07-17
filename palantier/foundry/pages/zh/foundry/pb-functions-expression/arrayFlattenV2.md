---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arrayFlattenV2/",
  "title": "数组扁平化",
  "page_id": "arrayFlattenV2",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/isArrayUniqueV1/",
  "next": "/zh/foundry/pb-functions-expression/arrayIntersectV1/",
  "scraped_at": "2026-07-13T05:52:47.796245+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数组扁平化

> 支持于: 批处理, 流处理

通过合并第一层嵌套内的元素，从输入的嵌套数组创建单个数组。

**表达式类别**: 数组

## 声明的参数

* **表达式** - 要扁平化的嵌套数组。<br>*Expression\<Array\<Array\<T>>>*

**类型变量范围:** *T 接受 AnyType*

**输出类型:** *Array\<T>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `array`

| array | **输出** |
| ----- | ----- |
| \[ \[ 1, 2, 3 ], \[ 4, 5, 6 ] ] | \[ 1, 2, 3, 4, 5, 6 ] |

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: `array`

| array | **输出** |
| ----- | ----- |
| \[ \[ \[ 1 ], \[ 2 ] ], \[ \[ 3 ], \[ 4 ] ] ] | \[ \[ 1 ], \[ 2 ], \[ 3 ], \[ 4 ] ] |

***

### 示例 3: 空值情况

**参数值:**

* **表达式**: `array`

| array | **输出** |
| ----- | ----- |
| *null* | *null* |
| \[ *null*, \[ 1, 2 ] ] | \[ 1, 2 ] |

***
