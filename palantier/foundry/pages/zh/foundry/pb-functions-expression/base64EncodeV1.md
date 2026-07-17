---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/base64EncodeV1/",
  "title": "Base64 编码",
  "page_id": "base64EncodeV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/base64DecodeV1/",
  "next": "/zh/foundry/pb-functions-expression/bitShiftLeftV1/",
  "scraped_at": "2026-07-13T05:53:07.095790+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Base64 编码

> 支持于: 批处理, 流处理

对给定表达式进行 Base64 编码。

**表达式类别**: 二进制, 转换

## 声明的参数

* **表达式** - 要编码的字符串或二进制表达式。<br>*表达式<二进制 | 字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `city`

| city | **输出** |
| ----- | ----- |
| TG9uZG9u | TG9uZG9u |
| Q29wZW5oYWdlbg== | Q29wZW5oYWdlbg== |
| TmV3IFlvcms= | TmV3IFlvcms= |

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: `city`

| city | **输出** |
| ----- | ----- |
| London | TG9uZG9u |
| Copenhagen | Q29wZW5oYWdlbg== |
| New York | TmV3IFlvcms= |

***

### 示例 3: 空值情况

**参数值:**

* **表达式**: `city`

| city | **输出** |
| ----- | ----- |
| *null* | *null* |

***

### 示例 4: 空值情况

**参数值:**

* **表达式**: `city`

| city | **输出** |
| ----- | ----- |
| *null* | *null* |

***
