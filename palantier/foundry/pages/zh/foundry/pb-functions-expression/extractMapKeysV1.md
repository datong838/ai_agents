---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/extractMapKeysV1/",
  "title": "提取映射键",
  "page_id": "extractMapKeysV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/getImageryMetadataV1/",
  "next": "/zh/foundry/pb-functions-expression/extractMapValuesV1/",
  "scraped_at": "2026-07-13T05:55:01.959268+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 提取映射键

> 支持于: 批处理, 流处理

将映射键返回为数组。注意数组元素的顺序是不确定的。

**表达式类别**: 映射

## 声明的参数

* **映射** - 映射表达式。<br>*表达式\<Map\<K, AnyType>>*

**类型变量界限:** *K 接受 AnyType*

**输出类型:** *数组\<K>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| {<br> MT-111 -> 2,<br> XB-134 -> 1,<br>} | \[ XB-134, MT-111 ] |

***

### 示例 2: 空值情况

**参数值:**

* **映射**: `flight_number`

| flight\_number | **输出** |
| ----- | ----- |
| *null* | *null* |

***
