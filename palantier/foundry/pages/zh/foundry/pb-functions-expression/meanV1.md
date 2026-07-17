---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/meanV1/",
  "title": "平均值",
  "page_id": "meanV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/maxV1/",
  "next": "/zh/foundry/pb-functions-expression/minV1/",
  "scraped_at": "2026-07-13T05:56:30.604731+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 平均值

> 支持于: 批处理, 流处理

计算列中值的平均值。

**表达式类别**: 数值

## 声明的参数

* **表达式** - 计算平均值的列。<br>*表达式<数值>*

**输出类型:** *十进制 | 双精度*

## 示例

### 示例1: 基本案例

**参数值:**

* **表达式**: `values`

**给定的输入表:**

| values |
| ----- |
| 2 |
| 4 |
| 3 |

**输出:** 3.0

***

### 示例2: 空值案例

**参数值:**

* **表达式**: `values`

**给定的输入表:**

| values |
| ----- |
| 2 |
| *null* |
| 3 |

**输出:** 2.5

***
