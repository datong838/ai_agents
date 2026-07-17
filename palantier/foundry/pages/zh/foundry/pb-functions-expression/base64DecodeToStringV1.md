---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/base64DecodeToStringV1/",
  "title": "Base 64 解码为字符串",
  "page_id": "base64DecodeToStringV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/arraysZipV1/",
  "next": "/zh/foundry/pb-functions-expression/base64DecodeV1/",
  "scraped_at": "2026-07-13T05:52:59.513750+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Base 64 解码为字符串

> 支持于: 批处理, 流处理

对给定表达式进行Base64解码。使用utf-8编码处理二进制数据。

**表达式类别**: 二进制, 转换, 字符串

## 声明的参数

* **表达式** - *无描述*<br>*Expression\<Binary | 字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本情况

**参数值:**

* **表达式**: `encoded`

| encoded | **输出** |
| ----- | ----- |
| Wm05dg== | foo |
| WW1GeQ== | bar |

***

### 示例 2: 基本情况

**参数值:**

* **表达式**: `encoded`

| encoded | **输出** |
| ----- | ----- |
| Zm9v | foo |
| YmFy | bar |

***

### 示例 3: 空值情况

**参数值:**

* **表达式**: `encoded`

| encoded | **输出** |
| ----- | ----- |
| *null* | *null* |

***

### 示例 4: 空值情况

**参数值:**

* **表达式**: `encoded`

| encoded | **输出** |
| ----- | ----- |
| *null* | *null* |

***
