---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/createNullValueV1/",
  "title": "创建空值",
  "page_id": "createNullValueV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/mapFromArraysV1/",
  "next": "/zh/foundry/pb-functions-expression/createGeoRangeFanGeometryV1/",
  "scraped_at": "2026-07-13T05:54:10.383944+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建空值

> 支持于：批处理、流处理

返回给定类型的空值。

**表达式类别**：数据准备

## 声明的参数

* **类型** - 要创建的空值的类型。<br>*Type\<T>*

**类型变量界限：** *T 接受 AnyType*

**输出类型：** *T*

## 示例

### 示例 1：基本情况

**参数值：**

* **类型**: Array\<String>

**输出：** *null*

***

### 示例 2：基本情况

**参数值：**

* **类型**: Map\<String, String>

**输出：** *null*

***

### 示例 3：基本情况

**参数值：**

* **类型**: String

**输出：** *null*

***

### 示例 4：基本情况

**参数值：**

* **类型**: Struct\<string:String, array:Array\<String>>

**输出：** *null*

***
