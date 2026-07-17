---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/splitStringV2/",
  "title": "拆分字符串",
  "page_id": "splitStringV2",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arraySliceV1/",
  "next": "/zh/foundry/pb-functions-expression/sqrtV1/",
  "scraped_at": "2026-07-13T05:57:18.061293+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 拆分字符串

> 支持于: 批处理, 流处理

根据指定的正则表达式模式拆分字符串。

**表达式类别**: 字符串

## 声明的参数

* **Expression** - 根据指定模式拆分的输入字符串。<br>*Expression<字符串>*
* **Pattern** - 拆分所用的正则表达式模式。<br>*Regex*
* *非必填* **Limit** - 将字符串最多拆分为该数量的元素。必须大于0。<br>*Literal\<Integer>*

**输出类型:** *Array<字符串>*

## 示例

### 示例 1: 基本情况

**参数值:**

* **Expression**: `string`
* **Pattern**:
* **Limit**: 2

| string | **输出** |
| ----- | ----- |
| hello | \[ hello ] |
| hello world | \[ hello, world ] |
| hello there world | \[ hello, there world ] |

***

### 示例 2: 基本情况

**参数值:**

* **Expression**: oneAtwoBthreeC
* **Pattern**: \[ABC]
* **Limit**: 10

**输出:** \[ one, two, three, *empty string* ]

***

### 示例 3: 基本情况

**参数值:**

* **Expression**: oneAtwoBthreeC
* **Pattern**: \[ABC]
* **Limit**: 2

**输出:** \[ one, twoBthreeC ]

***

### 示例 4: 空情况

**参数值:**

* **Expression**: *null*
* **Pattern**: pattern
* **Limit**: *null*

**输出:** *null*

***

### 示例 5: 边缘情况

**参数值:**

* **Expression**: *empty string*
* **Pattern**: foo
* **Limit**: *null*

**输出:** \[ *empty string* ]

***

### 示例 6: 边缘情况

**参数值:**

* **Expression**: abc
* **Pattern**: *empty string*
* **Limit**: *null*

**输出:** \[ a, b, c ]

***

### 示例 7: 边缘情况

**参数值:**

* **Expression**: *empty string*
* **Pattern**: *empty string*
* **Limit**: *null*

**输出:** \[ *empty string* ]

***
