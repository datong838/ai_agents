---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/timestampToEpochMillisV1/",
  "title": "将时间戳转换为纪元毫秒",
  "page_id": "timestampToEpochMillisV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/timestampSubtractV1/",
  "next": "/zh/foundry/pb-functions-expression/timestampToEpochSecondsV1/",
  "scraped_at": "2026-07-13T05:57:44.408981+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将时间戳转换为纪元毫秒

> 支持于: 批处理, 流处理

将UTC时间戳转换为纪元毫秒。

**表达式类别**: 转换, 日期时间

## 声明的参数

* **时间戳** - *无描述*<br>*表达式<时间戳>*

**输出类型:** *长整型*

## 示例

### 示例 1: 基本情况

**参数值:**

* **时间戳**: 2022-10-01T09:00:00Z

**输出:** 1664614800000

***

### 示例 2: 空值情况

**参数值:**

* **时间戳**: *空值*

**输出:** *空值*

***
