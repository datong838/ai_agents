---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/addOrUpdateStructFieldV1/",
  "title": "添加或更新结构体字段",
  "page_id": "addOrUpdateStructFieldV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/addV2/",
  "next": "/zh/foundry/pb-functions-expression/dateAddV2/",
  "scraped_at": "2026-07-13T05:51:59.946191+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 添加或更新结构体字段

> 支持于: 批处理, 流处理

更新结构体的字段或添加一个新字段。

**表达式类别**: 结构体

## 声明的参数

* **Expression** - 更新结构体字段的表达式。<br>*Expression\<AnyType>*
* **Locator** - 定位具有多个条目的内部元素，例如 \['author', 'email']。<br>*StructLocator*
* **Struct** - 要更新的结构体。<br>*Expression\<Struct>*

**输出类型:** *Struct*

## 例子

### 例子 1: 基本案例

**参数值:**

* **Expression**: `value`
* **Locator**: flight
* **Struct**: `struct`

| struct | value | **输出** |
| ----- | ----- | ----- |
| {<br> **airline**: {<br> **id**: NA,<br>},<br>} | foo | {<br> **airline**: {<br> **id**: NA,<br>},<br> **flight**: foo,<br>} |

***

### 例子 2: 基本案例

**参数值:**

* **Expression**: `value`
* **Locator**: flight
* **Struct**: `struct`

| struct | value | **输出** |
| ----- | ----- | ----- |
| {<br> **airline**: {<br> **id**: FE,<br>},<br>} | {<br> **id**: 1,<br>} | {<br> **airline**: {<br> **id**: FE,<br>},<br> **flight**: {<br> **id**: 1,<br>},<br>} |

***

### 例子 3: 基本案例

**参数值:**

* **Expression**: `value`
* **Locator**: airline.id
* **Struct**: `struct`

| struct | value | **输出** |
| ----- | ----- | ----- |
| {<br> **airline**: {<br> **id**: NA,<br>},<br>} | 1 | {<br> **airline**: {<br> **id**: 1,<br>},<br>} |
| {<br> **airline**: {<br> **id**: FE,<br>},<br>} | 2 | {<br> **airline**: {<br> **id**: 2,<br>},<br>} |

***

### 例子 4: 空值案例

**参数值:**

* **Expression**: `value`
* **Locator**: airline.id
* **Struct**: `struct`

| struct | value | **输出** |
| ----- | ----- | ----- |
| *null* | *null* | *null* |
| *null* | 1 | *null* |
| {<br> **airline**: {<br> **id**: FE,<br>},<br>} | *null* | {<br> **airline**: {<br> **id**: *null*,<br>},<br>} |

***
