---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/cipherDecryptV1/",
  "title": "密码解密",
  "page_id": "cipherDecryptV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/chunkStringV1/",
  "next": "/zh/foundry/pb-functions-expression/cipherEncryptV1/",
  "scraped_at": "2026-07-13T05:53:12.544010+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 密码解密

> 支持于: 批处理, 流处理

使用密码解密表达式。

**表达式类别**: 其他

## 声明参数

* **密码许可证 rid** - 要使用的密码许可证。<br>*ResourceIdentifier*
* **表达式** - 要应用密码解密的表达式。<br>*Expression<字符串>*

**输出类型:** *字符串*

## 示例

### 示例 1: 基本案例

**参数值:**

* **密码许可证 rid**: ri.bellaso.main.cipher-license.1-decrypt
* **表达式**: `string`

| string | **输出** |
| ----- | ----- |
| CIPHER::ri.bellaso.main.cipher-channel.1::OCRBIW3iHDltOGa6MEHwb7f/Dw==::CIPHER | bar |

***

### 示例 2: 空案例

**参数值:**

* **密码许可证 rid**: ri.bellaso.main.cipher-license.1-decrypt
* **表达式**: `string`

| string | **输出** |
| ----- | ----- |
| *null* | *null* |

***
