---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/notV1/",
  "title": "Not",
  "page_id": "notV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/normalRandomV1/",
  "next": "/zh/foundry/pb-functions-expression/getNthChainFromPolygonV1/",
  "scraped_at": "2026-07-13T05:56:40.924467+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Not

> 支持于：批处理，流处理

返回布尔表达式的否定布尔值。

**表达式类别**：布尔

## 声明的参数

* **表达式** - *无描述*<br>*Expression\<Boolean>*

**输出类型：** *Boolean*

## 例子

### 例子 1: 基本情况

**参数值：**

* **表达式**: `boolean`

| boolean | **输出** |
| ----- | ----- |
| true | false |
| false | true |

***

### 例子 2: 空值情况

**参数值：**

* **表达式**: *null*

**输出：** *null*

***
