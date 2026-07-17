---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/createArrayV1/",
  "title": "创建数组",
  "page_id": "createArrayV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/createEmptyArrayV1/",
  "next": "/zh/foundry/pb-functions-expression/createGeoEllipseGeometryV1/",
  "scraped_at": "2026-07-13T05:54:13.300433+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建数组

> 支持于: 批处理, 流处理

根据提供的列创建一个数组。

**表达式类别**: 数组

## 声明的参数

* **表达式** - 用于创建数组的表达式列表。<br>*List\<Expression\<T>>*

**类型变量界限:** *T 接受 AnyType*

**输出类型:** *Array\<T>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: \[1, 2, 3]

**输出:** \[ 1, 2, 3 ]

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: \[\[ 1 ], \[ 2 ]]

**输出:** \[ \[ 1 ], \[ 2 ] ]

***

### 示例 3: 空值情况

**参数值:**

* **表达式**: \[1, *null*, 3]

**输出:** \[ 1, *null*, 3 ]

***
