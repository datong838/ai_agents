---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/cleanStringV1/",
  "title": "清理字符串",
  "page_id": "cleanStringV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/cipherHashV1/",
  "next": "/zh/foundry/pb-functions-expression/collectArrayV1/",
  "scraped_at": "2026-07-13T05:53:18.262818+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 清理字符串

> 支持于: 批处理, 流处理

对表达式应用一组清理操作。

**表达式类别**: 数据准备, 字符串

## 声明的参数

* **清理操作** - 将要应用的一组操作。<br>*Set\<Enum\<Normalize whitespace, Nullify empty, Trim>>*
* **表达式** - 要清理的字符串。<br>*Expression<字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **清理操作**: {`normalize`}
* **表达式**: hello     world

**输出:** hello world

***

### 示例 2: 基本情况

**参数值:**

* **清理操作**: {`nullify_empty`}
* **表达式**: *空字符串*

**输出:** *null*

***

### 示例 3: 基本情况

**参数值:**

* **清理操作**: {`trim`}
* **表达式**:   hello world

**输出:** hello world

***

### 示例 4: 空值情况

**参数值:**

* **清理操作**: {`trim`}
* **表达式**: *null*

**输出:** *null*

***
