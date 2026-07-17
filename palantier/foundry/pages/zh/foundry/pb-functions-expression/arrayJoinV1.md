---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/arrayJoinV1/",
  "title": "合并数组",
  "page_id": "arrayJoinV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/isValidUuidV1/",
  "next": "/zh/foundry/pb-functions-expression/lagV1/",
  "scraped_at": "2026-07-13T05:56:09.451993+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 合并数组

> 支持于: 批处理, 流处理

使用指定的分隔符合并数组。

**表达式类别**: 数组

## 声明的参数

* **要合并的数组** - *无描述*<br>*表达式<数组<字符串>>*
* **分隔符** - *无描述*<br>*表达式<字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **要合并的数组**: \[ hello, world ]
* **分隔符**: -

**输出:** hello-world

***

### 示例 2: 基本情况

**参数值:**

* **要合并的数组**: \[ hello, world ]
* **分隔符**: <br>

**输出:** hello<br>world

***

### 示例 3: 空值情况

**参数值:**

* **要合并的数组**: `array`
* **分隔符**: `separator`

| array | separator | **输出** |
| ----- | ----- | ----- |
| \[ hello, world ] | *null* | helloworld |
| *null* | - | *null* |
| *null* | *null* | *null* |

***
