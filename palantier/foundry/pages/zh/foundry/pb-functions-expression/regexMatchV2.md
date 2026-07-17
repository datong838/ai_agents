---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/regexMatchV2/",
  "title": "正则表达式匹配",
  "page_id": "regexMatchV2",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/regexIndexV1/",
  "next": "/zh/foundry/pb-functions-expression/regexReplaceV1/",
  "scraped_at": "2026-07-13T05:57:05.847932+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 正则表达式匹配

> 支持于: 批处理, 流处理

将表达式与正则表达式进行匹配。正则表达式必须匹配整个字符串。

**表达式类别**: 正则, 字符串

## 声明的参数

* **Expression** - 要与正则表达式匹配的表达式。<br>*Expression<字符串>*
* **Regex** - 要匹配的正则表达式。<br>*Expression<字符串>*

**输出类型:** *布尔值*

## 示例

### 示例 1: 基本情况

**描述**: 正则表达式必须匹配整个字符串
**参数值:**

* **Expression**: (
* **Regex**: abc

**输出:** false

***

### 示例 2: 基本情况

**描述**: 正则表达式必须匹配整个字符串
**参数值:**

* **Expression**: abcdefg
* **Regex**: abc

**输出:** false

***

### 示例 3: 基本情况

**描述**: 可以匹配正则表达式模式
**参数值:**

* **Expression**: abcdefg
* **Regex**: abc?d.+

**输出:** true

***

### 示例 4: 基本情况

**描述**: 正则表达式模式有时不匹配输入字符串
**参数值:**

* **Expression**: abdefg
* **Regex**: ab?d.\*

**输出:** true

***

### 示例 5: 空情况

**描述**: 空模式不匹配
**参数值:**

* **Expression**: foo
* **Regex**: *null*

**输出:** false

***

### 示例 6: 空情况

**描述**: 空列不匹配
**参数值:**

* **Expression**: *null*
* **Regex**: ab?d.\*

**输出:** false

***

### 示例 7: 空情况

**参数值:**

* **Expression**: `foo`
* **Regex**: `pattern`

| foo | pattern | **输出** |
| ----- | ----- | ----- |
| foo | ( | false |
| foo | *null* | false |
| *null* | foo | false |
| *null* | *null* | false |

***
