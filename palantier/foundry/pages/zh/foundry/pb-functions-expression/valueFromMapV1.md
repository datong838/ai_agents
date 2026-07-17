---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/valueFromMapV1/",
  "title": "从映射中获取值",
  "page_id": "valueFromMapV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/useLlmV2/",
  "next": "/zh/foundry/pb-functions-expression/varianceV1/",
  "scraped_at": "2026-07-13T05:58:10.376182+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从映射中获取值

> 支持于: 批处理, 流处理

使用键从映射中获取值。

**表达式类别**: 映射

## 声明的参数

* **键** - 键表达式。<br>*Expression\<K>*
* **映射** - 映射表达式。<br>*Expression\<Map\<K, V>>*

**类型变量界限:** *K 接受 ComparableType\*\*V 接受 AnyType*

**输出类型:** *V*

## 示例

### 示例 1: 基本情况

**参数值:**

* **键**: \[ 1 ]
* **映射**: {<br> \[ 1 ] -> Foo,<br>}

**输出:** Foo

***

### 示例 2: 基本情况

**参数值:**

* **键**: Bar
* **映射**: {<br> Bar -> 2,<br> Foo -> 1,<br>}

**输出:** 2

***

### 示例 3: 基本情况

**参数值:**

* **键**: 1
* **映射**: {<br> 1 -> 10,<br> 2 -> 20,<br>}

**输出:** 10

***

### 示例 4: 基本情况

**参数值:**

* **键**: Foo
* **映射**: {<br> Bar -> World,<br> Foo -> Hello,<br>}

**输出:** Hello

***

### 示例 5: 基本情况

**参数值:**

* **键**: Foo
* **映射**: {<br> Bar -> World,<br>}

**输出:** *null*

***

### 示例 6: 基本情况

**参数值:**

* **键**: \[ \[ 1 ], \[ 1 ] ]
* **映射**: {<br> \[ \[ 1 ], \[ 1 ] ] -> Foo,<br>}

**输出:** Foo

***

### 示例 7: 空值情况

**参数值:**

* **键**: `key`
* **映射**: `map`

| map | key | **输出** |
| ----- | ----- | ----- |
| *null* | *null* | *null* |
| {<br> Foo -> Hello,<br>} | *null* | *null* |
| *null* | Foo | *null* |

***
