---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/levenshteinDistanceV1/",
  "title": "Levenshtein距离",
  "page_id": "levenshteinDistanceV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/lessThanOrEqualsV1/",
  "next": "/zh/foundry/pb-functions-expression/linearRegressionGradientV1/",
  "scraped_at": "2026-07-13T05:56:18.752555+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Levenshtein距离

> 支持于: 批处理, 流处理

计算两个字符串之间的Levenshtein距离。

**表达式类别**: 字符串

## 声明的参数

* **忽略大小写** - 是否希望在比较左右字符串时忽略大小写？<br>*Literal\<Boolean>*
* **左边** - 要比较的左边字符串。<br>*Expression<字符串>*
* **右边** - 要比较的右边字符串。<br>*Expression<字符串>*

**输出类型:** *Integer*

## 示例

### 示例 1: 基本情况

**参数值:**

* **忽略大小写**: false
* **左边**: `left`
* **右边**: `right`

| left | right | **输出** |
| ----- | ----- | ----- |
| hello | hello | 0 |
| hallo | hello | 1 |
| hello | hEllO | 2 |
| hello | hello, world! | 8 |
| hello | farewell | 6 |

***

### 示例 2: 基本情况

**描述**: 通过将忽略大小写设置为true，大小写不同的字母被视为相等。
**参数值:**

* **忽略大小写**: true
* **左边**: `left`
* **右边**: `right`

| left | right | **输出** |
| ----- | ----- | ----- |
| hello | hello | 0 |
| hELlo | hello | 0 |
| hello | hEllO | 0 |

***

### 示例 3: 空值情况

**参数值:**

* **忽略大小写**: false
* **左边**: `left`
* **右边**: `right`

| left | right | **输出** |
| ----- | ----- | ----- |
| hello | *null* | *null* |
| *null* | hello | *null* |
| *null* | *null* | *null* |

***
