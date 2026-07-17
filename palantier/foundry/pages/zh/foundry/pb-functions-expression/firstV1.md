---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/firstV1/",
  "title": "First",
  "page_id": "firstV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/geometryFilterV1/",
  "next": "/zh/foundry/pb-functions-expression/firstNonNullV1/",
  "scraped_at": "2026-07-13T05:54:45.493788+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# First

> 支持于: 批处理

组中的第一个项目。注意，如果在聚合或无序窗口中使用，所选择的行将是非确定性的。

**表达式类别**: 聚合

## 声明的参数

* **表达式** - 要聚合的表达式。<br>*Expression\<T>*
* **忽略空值** - 如果为true，空值将被忽略。<br>*Literal\<Boolean>*

**类型变量界限:** *T 接受 AnyType*

**输出类型:** *T*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `values`
* **忽略空值**: false

**给定输入表:**

| values |
| ----- |
| 2 |
| 4 |
| 3 |

**输出:** 2

***
