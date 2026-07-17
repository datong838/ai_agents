---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/jsonStringV2/",
  "title": "转换数据为JSON",
  "page_id": "jsonStringV2",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/convertWeightV1/",
  "next": "/zh/foundry/pb-functions-expression/ontologyGeopointToGeopointV1/",
  "scraped_at": "2026-07-13T05:53:44.191105+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 转换数据为JSON

> 支持于: 批处理, 流处理

将输入变换为json字符串。

**表达式类别**: 文件, 字符串

## 声明的参数

* **输入** - 要变换的输入。<br>*表达式<数组\<AnyType> | 映射\<AnyType, AnyType> | 结构体>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **输入**: `array`

| array | **输出** |
| ----- | ----- |
| \[ hello, world ] | \["hello","world"] |

***

### 示例 2: 基本情况

**参数值:**

* **输入**: `struct`

| struct | **输出** |
| ----- | ----- |
| {<br> **airline**: {<br> **id**: NA,<br>},<br>} | {"airline":{"id":"NA"}} |

***

### 示例 3: 基本情况

**参数值:**

* **输入**: `struct_0`

| struct\_0 | **输出** |
| ----- | ----- |
| {<br> **date**: 2021-01-01,<br> **dec32**: 1.12,<br> **dec33**: 0.120,<br> \*\*dec... | {"dec32":1.12,"dec33":0.120,"dec64":10.0000,"timestamp":"2021-01-01T01:01:01.000Z","date":"2021-01-01","struct\_1":{"airline":{"id":"NA"}}} |

***

### 示例 4: 基本情况

**参数值:**

* **输入**: `array`

| array | **输出** |
| ----- | ----- |
| \[ 1.00, 2.10, 36.00 ] | \[1.00,2.10,36.00] |

***

### 示例 5: 基本情况

**参数值:**

* **输入**: `map`

| map | **输出** |
| ----- | ----- |
| {<br> a -> 1,<br> b -> 2,<br>} | {"a":"1","b":"2"} |

***

### 示例 6: 基本情况

**参数值:**

* **输入**: `array`

| array | **输出** |
| ----- | ----- |
| \[ {<br> **airline**: {<br> **id**: NA,<br>},<br>}, *null* ] | \[{"airline":{"id":"NA"}},null] |

***

### 示例 7: 基本情况

**参数值:**

* **输入**: `map`

| map | **输出** |
| ----- | ----- |
| {<br> a -> {<br> **airline**: {<br> **id**: NA,<br>},<br>},<br>} | {"a":{"airline":{"id":"NA"}}} |

***

### 示例 8: 基本情况

**参数值:**

* **输入**: `struct_0`

| struct\_0 | **输出** |
| ----- | ----- |
| {<br> **array\_1**: \[ *null*, *null*, *null* ],<br> **struct\_1**: {<br> **double**: *null*,<br> **string**: *null*,<br>},<br>} | {"struct\_1":{"string":null,"double":null},"array\_1":\[null,null,null]} |
| {<br> **array\_1**: *null*,<br> **struct\_1**: *null*,<br>} | {"struct\_1":null,"array\_1":null} |

***
