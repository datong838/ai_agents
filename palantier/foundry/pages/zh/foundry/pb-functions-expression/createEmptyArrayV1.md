---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/createEmptyArrayV1/",
  "title": "创建一个空数组",
  "page_id": "createEmptyArrayV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/createGeoPointFromCoordinateSystemV1/",
  "next": "/zh/foundry/pb-functions-expression/createArrayV1/",
  "scraped_at": "2026-07-13T05:54:04.456434+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建一个空数组

> 支持于: 批处理, 流处理

返回给定类型的空数组。

**表达式类别**: 数组

## 声明的参数

* **类型** - 要创建的数组的元素类型。<br>*Type\<T>*

**类型变量范围:** *T 接受 AnyType*

**输出类型:** *Array\<T>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **类型**: Array<字符串>

**输出:** \[  ]

***

### 示例 2: 基本情况

**参数值:**

* **类型**: Map<字符串, 字符串>

**输出:** \[  ]

***

### 示例 3: 基本情况

**参数值:**

* **类型**: 字符串

**输出:** \[  ]

***

### 示例 4: 基本情况

**参数值:**

* **类型**: Struct\<string:字符串, array:Array<字符串>>

**输出:** \[  ]

***
