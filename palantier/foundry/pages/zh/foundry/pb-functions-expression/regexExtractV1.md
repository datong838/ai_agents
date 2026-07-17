---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/regexExtractV1/",
  "title": "正则表达式提取",
  "page_id": "regexExtractV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/reduceArrayElementsV1/",
  "next": "/zh/foundry/pb-functions-expression/regexFindV1/",
  "scraped_at": "2026-07-13T05:56:59.064700+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 正则表达式提取

> 支持于: 批处理, 流处理

从正则表达式中提取指定的组。当未找到匹配时返回空字符串。

**表达式类别**: 正则表达式, 字符串

## 声明的参数

* **表达式** - 要从中提取的表达式。<br>*表达式<字符串>*
* **组** - 要从正则表达式匹配中提取的组。<br>*字面量<整数>*
* **模式** - 要匹配的正则表达式模式。<br>*表达式<字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本案例

**描述**: 从第一个匹配中提取前两个首字母。
**参数值:**

* **表达式**: MT-112, XB-967
* **组**: 1
* **模式**: (\w\w)(-)

**输出:** MT

***

### 示例 2: 基本案例

**参数值:**

* **表达式**: MT-112, XB-967
* **组**: 0
* **模式**: NOT\_FOUND

**输出:** *空字符串*

***

### 示例 3: 空案例

**描述**: 空输入给出空输出。
**参数值:**

* **表达式**: *null*
* **组**: 1
* **模式**: (\w\w)(-)

**输出:** *null*

***
