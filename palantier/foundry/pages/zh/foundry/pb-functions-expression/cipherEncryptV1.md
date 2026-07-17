---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/cipherEncryptV1/",
  "title": "加密算法",
  "page_id": "cipherEncryptV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/cipherDecryptV1/",
  "next": "/zh/foundry/pb-functions-expression/cipherHashV1/",
  "scraped_at": "2026-07-13T05:53:15.365211+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 加密算法

> 支持于: 批处理, 流处理

使用加密算法对表达式进行加密。

**表达式类别**: 其他

## 声明的参数

* **Cipher license rid** - 使用的加密许可。<br>*ResourceIdentifier*
* **Expression** - 以应用加密算法的表达式。<br>*Expression<字符串>*

**输出类型:** *加密文本*

## 示例

### 示例 1: 基本案例

**参数值:**

* **Cipher license rid**: ri.bellaso.main.cipher-license.1-encrypt
* **Expression**: `string`

| string | **输出** |
| ----- | ----- |
| bar | CIPHER::ri.bellaso.main.cipher-channel.1::OCRBIW3iHDltOGa6MEHwb7f/Dw==::CIPHER |

***

### 示例 2: 空值案例

**参数值:**

* **Cipher license rid**: ri.bellaso.main.cipher-license.1-encrypt
* **Expression**: `string`

| string | **输出** |
| ----- | ----- |
| *null* | *null* |

***
