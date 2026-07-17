---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/extractMapValuesV1/",
  "title": "提取映射值",
  "page_id": "extractMapValuesV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/extractMapKeysV1/",
  "next": "/zh/foundry/pb-functions-expression/pdfTextExtractionV1/",
  "scraped_at": "2026-07-13T05:54:38.920909+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 提取映射值

> 支持于: 批处理, 流处理

将映射值返回为数组。请注意，数组元素的顺序是不确定的。

**表达式类别**: 映射

## 声明的参数

* **映射** - 映射表达式。<br>*表达式<映射<任意类型, V>>*

**类型变量界限:** *V 接受任意类型*

**输出类型:** *数组\<V>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| {<br> MT-111 -> 2,<br> XB-134 -> 1,<br>} | \[ 1, 2 ] |

***

### 示例 2: 空值情况

**参数值:**

* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| {<br> MT-111 -> 2,<br> XB-134 -> *null*,<br>} | \[ *null*, 2 ] |
| *null* | *null* |

***
