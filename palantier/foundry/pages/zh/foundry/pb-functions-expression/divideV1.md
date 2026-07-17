---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/divideV1/",
  "title": "数字除法",
  "page_id": "divideV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/distinctCountV1/",
  "next": "/zh/foundry/pb-functions-expression/geometryToGeobufExpressionV1/",
  "scraped_at": "2026-07-13T05:54:23.344668+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数字除法

> 支持于: 批处理, 流处理

将一个数字除以另一个数字。

**表达式类别**: 数值

## 声明的参数

* **左** - 分子。<br>*表达式<数值>*
* **右** - 分母。<br>*表达式<数值>*

**输出类型:** *小数 | 双精度*

## 示例

### 示例 1: 基本情况

**参数值:**

* **左**: `col_a`
* **右**: `col_b`

| col\_a | col\_b | **输出** |
| ----- | ----- | ----- |
| 4 | 2 | 2.0 |
| 11 | 2 | 5.5 |

***
