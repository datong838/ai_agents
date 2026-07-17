---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/lessThanV1/",
  "title": "小于",
  "page_id": "lessThanV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/lengthV1/",
  "next": "/zh/foundry/pb-functions-expression/lessThanOrEqualsV1/",
  "scraped_at": "2026-07-13T05:56:18.535894+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 小于

> 支持于: 批处理, 流处理

如果左侧小于右侧，则返回 true。

**表达式类别**: 布尔值

## 声明的参数

* **左侧** - 左侧表达式。<br>*表达式\<ComparableType>*
* **右侧** - 右侧表达式。<br>*表达式\<ComparableType>*

**输出类型:** *布尔值*

## 示例

### 示例 1: 基本情况

**参数值:**

* **左侧**: `left`
* **右侧**: `right`

| 左侧 | 右侧 | **输出** |
| ----- | ----- | ----- |
| 1.0 | 10 | true |
| 10.0 | 1 | false |

***

### 示例 2: 基本情况

**参数值:**

* **左侧**: `left`
* **右侧**: `right`

| 左侧 | 右侧 | **输出** |
| ----- | ----- | ----- |
| a | b | true |
| b | a | false |

***

### 示例 3: 空值情况

**参数值:**

* **左侧**: `a`
* **右侧**: `b`

| a | b | **输出** |
| ----- | ----- | ----- |
| *null* | *null* | true |
| 1 | *null* | false |
| *null* | 1 | false |

***
