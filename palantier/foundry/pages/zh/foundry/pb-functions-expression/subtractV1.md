---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/subtractV1/",
  "title": "数字相减",
  "page_id": "subtractV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/subtractManyV1/",
  "next": "/zh/foundry/pb-functions-expression/timestampDiffV1/",
  "scraped_at": "2026-07-13T05:57:28.535059+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数字相减

> 支持于: 批处理, 流处理

将一个数字从另一个数字中减去。

**表达式类别**: 数值

## 声明的参数

* **Left** - 左侧数字。<br>*Expression\<Numeric>*
* **Right** - 右侧数字。<br>*Expression\<Numeric>*

**输出类型:** *数值*

## 示例

### 示例 1: 基本情况

**参数值:**

* **Left**: `col_a`
* **Right**: `col_b`

| col\_a | col\_b | **输出** |
| ----- | ----- | ----- |
| 32 | 4 | 28 |
| -5 | -3 | -2 |

***
