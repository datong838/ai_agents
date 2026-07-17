---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/epochMillisToDateV1/",
  "title": "Epoch 毫秒到日期",
  "page_id": "epochMillisToDateV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/endsWithV1/",
  "next": "/zh/foundry/pb-functions-expression/epochMillisToTimestampV1/",
  "scraped_at": "2026-07-13T05:54:24.632022+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Epoch 毫秒到日期

> 支持于: 批处理, 流处理

将 epoch 毫秒转换为日期，UTC。

**表达式类别**: 转换, 日期时间

## 声明的参数

* **表达式** - Epoch 毫秒表达式。<br>*表达式\<Double | Long>*

**输出类型:** *日期*

## 示例

### 示例 1: 基本情况

**描述**: 你可以将以毫秒为单位的 epoch 时间戳转换为日期类型
**参数值:**

* **表达式**: 1673964111000

**输出:** 2023-01-17

***

### 示例 2: 空值情况

**描述**: 空列保持为空
**参数值:**

* **表达式**: `input`

| input | **输出** |
| ----- | ----- |
| *null* | *null* |

***
