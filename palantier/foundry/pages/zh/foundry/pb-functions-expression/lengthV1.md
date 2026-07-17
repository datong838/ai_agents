---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/lengthV1/",
  "title": "长度",
  "page_id": "lengthV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/leftPadV1/",
  "next": "/zh/foundry/pb-functions-expression/lessThanV1/",
  "scraped_at": "2026-07-13T05:56:21.358224+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 长度

> 支持于：批处理，流处理

返回字符串列或数组列中每个值的长度。

**表达式类别**：数组，数值

## 声明的参数

* **表达式** - 要计算长度的表达式。<br>*表达式<数组<任何类型> | 二进制 | 映射<任何类型, 任何类型> | 字符串>*

**输出类型：** *整数*

## 示例

### 示例 1：基本情况

**参数值：**

* **表达式**: `string`

| 字符串 | **输出** |
| ----- | ----- |
| hello | 5 |
| bye | 3 |

***
