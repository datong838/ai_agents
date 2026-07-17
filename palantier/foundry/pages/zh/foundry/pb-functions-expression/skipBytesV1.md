---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/skipBytesV1/",
  "title": "跳过字节",
  "page_id": "skipBytesV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/sineV1/",
  "next": "/zh/foundry/pb-functions-expression/arraySliceV1/",
  "scraped_at": "2026-07-13T05:57:15.561219+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 跳过字节

> 支持于: 批处理, 流式处理

在二进制列中跳过给定数量的字节。

**表达式类别**: 二进制

## 声明的参数

* **字节** - *无描述*<br>*表达式\<Binary>*
* **要跳过的字节数** - *无描述*<br>*表达式\<Integer>*

**输出类型:** *Binary*

## 示例

### 示例 1: 基本案例

**参数值:**

* **字节**: aGk=
* **要跳过的字节数**: 1

**输出:** aQ==

***

### 示例 2: 空值案例

**参数值:**

* **字节**: *null*
* **要跳过的字节数**: 1

**输出:** *null*

***

### 示例 3: 空值案例

**参数值:**

* **字节**: aGk=
* **要跳过的字节数**: *null*

**输出:** *null*

***

### 示例 4: 边缘案例

**参数值:**

* **字节**: aGk=
* **要跳过的字节数**: 100

**输出:** *null*

***
