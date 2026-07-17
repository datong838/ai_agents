---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/unicodeNormalizeV1/",
  "title": "Unicode 规范化",
  "page_id": "unicodeNormalizeV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/uncompactH3SetV1/",
  "next": "/zh/foundry/pb-functions-expression/uniformRandomV1/",
  "scraped_at": "2026-07-13T05:57:55.718510+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Unicode 规范化

> 支持于: 批处理, 流处理

根据 Unicode 标准附件 #15 执行 Unicode 规范化。

**表达式类别**: 数据准备, 字符串

## 声明的参数

* **表达式** - *无描述*<br>*Expression<字符串>*
* **规范化形式** - *无描述*<br>*Enum\<NFC, NFD, NFKC, NFKD>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `string`
* **规范化形式**: `nfc`

| 字符串 | **输出** |
| ----- | ----- |
| １２３ | １２３ |
| イナゴ | イナゴ |

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: `string`
* **规范化形式**: `nfd`

| 字符串 | **输出** |
| ----- | ----- |
| １２３ | １２３ |
| イナゴ | イナゴ |

***

### 示例 3: 基本情况

**参数值:**

* **表达式**: `string`
* **规范化形式**: `nfkc`

| 字符串 | **输出** |
| ----- | ----- |
| １２３ | 123 |
| イナゴ | イナゴ |

***

### 示例 4: 基本情况

**参数值:**

* **表达式**: `string`
* **规范化形式**: `nfkd`

| 字符串 | **输出** |
| ----- | ----- |
| １２３ | 123 |
| イナゴ | イナゴ |

***
