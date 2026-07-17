---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/dateToStringV2/",
  "title": "将日期格式化为字符串",
  "page_id": "dateToStringV2",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/floorV1/",
  "next": "/zh/foundry/pb-functions-expression/formatNumberV1/",
  "scraped_at": "2026-07-13T05:54:48.412898+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将日期格式化为字符串

> 支持于: 批处理, 流处理

根据Java DateTimeFormatter格式化返回日期为字符串。默认格式为ISO8601。

**表达式类别**: 转换, 字符串

## 声明的参数

* **Date** - 要格式化为字符串的日期。<br>*表达式\<Date>*
* *非必填* **Format** - 要使用的格式。默认格式为ISO8601。<br>*字面量<字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基础情况

**参数值:**

* **Date**: 2022-12-20
* **Format**: yy-MM-dd

**输出:** 22-12-20

***

### 示例 2: 基础情况

**参数值:**

* **Date**: 2022-12-20
* **Format**: *null*

**输出:** 2022-12-20

***

### 示例 3: 基础情况

**参数值:**

* **Date**: 2023-10-01
* **Format**: yyyy\_Q

**输出:** 2023\_4

***

### 示例 4: 基础情况

**参数值:**

* **Date**: 2023-10-01
* **Format**: yyyy\_q

**输出:** 2023\_4

***

### 示例 5: 空值情况

**参数值:**

* **Date**: *null*
* **Format**: yyyy-MM-dd

**输出:** *null*

***

### 示例 6: 边缘情况

**参数值:**

* **Date**: 2022-12-20
* **Format**: E

**输出:** Tue

***

### 示例 7: 边缘情况

**参数值:**

* **Date**: 2022-12-20
* **Format**: EEEE

**输出:** Tuesday

***

### 示例 8: 边缘情况

**参数值:**

* **Date**: 2023-10-01
* **Format**: DDD

**输出:** 274

***

### 示例 9: 边缘情况

**参数值:**

* **Date**: 2023-10-01
* **Format**: yyyy GG

**输出:** 2023 AD

***

### 示例 10: 边缘情况

**参数值:**

* **Date**: 2022-12-20
* **Format**: MMM, MMMM

**输出:** Dec, December

***

### 示例 11: 边缘情况

**参数值:**

* **Date**: 2023-10-01
* **Format**: YYYY

**输出:** 2023

***

### 示例 12: 边缘情况

**参数值:**

* **Date**: 2022-12-20
* **Format**: W

**输出:** 4

***

### 示例 13: 边缘情况

**参数值:**

* **Date**: 2022-12-20
* **Format**: F

**输出:** 6

***

### 示例 14: 边缘情况

**参数值:**

* **Date**: 2023-10-01
* **Format**: uuuu

**输出:** 2023

***
