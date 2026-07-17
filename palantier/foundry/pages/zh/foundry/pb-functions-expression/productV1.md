---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/productV1/",
  "title": "产品",
  "page_id": "productV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/normalizeGeometryV2/",
  "next": "/zh/foundry/pb-functions-expression/rankV1/",
  "scraped_at": "2026-07-13T05:56:55.255658+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 产品

> 支持于: 批处理

计算所有输入列的乘积。

**表达式类别**: 数值型

## 声明的参数

* **表达式** - *无描述*<br>*表达式<数值型>*

**输出类型:** *双精度*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `factor`

**给定输入表:**

| factor |
| ----- |
| 2 |
| 4 |
| 3 |

**输出:** 24.0

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: `factor`

**给定输入表:**

| factor |
| ----- |
| 2 |
| *null* |
| 3 |

**输出:** 6.0

***
