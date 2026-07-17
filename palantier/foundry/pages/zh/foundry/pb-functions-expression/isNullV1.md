---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/isNullV1/",
  "title": "是否为空",
  "page_id": "isNullV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/isNotNullV1/",
  "next": "/zh/foundry/pb-functions-expression/isValidGeoJsonV1/",
  "scraped_at": "2026-07-13T05:55:51.406517+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 是否为空

> 支持于：批处理，流处理

如果输入为空，则返回true，可以选择性地将空字符串视为null。

**表达式类别**：布尔值

## 声明的参数

* **表达式** - *无描述*<br>*Expression\<AnyType>*
* *非必填* **将空字符串视为null** - *无描述*<br>*Literal\<Boolean>*

**输出类型：** *布尔值*

## 示例

### 示例 1：基本情况

**参数值：**

* **表达式**：*空字符串*
* **将空字符串视为null**：true

**输出：** true

***

### 示例 2：基本情况

**参数值：**

* **表达式**：hello
* **将空字符串视为null**：*null*

**输出：** false

***

### 示例 3：基本情况

**参数值：**

* **表达式**：1
* **将空字符串视为null**：*null*

**输出：** false

***

### 示例 4：基本情况

**参数值：**

* **表达式**：*null*
* **将空字符串视为null**：*null*

**输出：** true

***
