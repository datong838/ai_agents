---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/isValidH3IndexV1/",
  "title": "是否为有效的H3索引",
  "page_id": "isValidH3IndexV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/isValidGeohashV1/",
  "next": "/zh/foundry/pb-functions-expression/isValidMgrsV1/",
  "scraped_at": "2026-07-13T05:56:00.282091+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 是否为有效的H3索引

> 支持于: 批处理, 流处理

如果输入是一个有效的H3索引字符串，则返回true。

**表达式类别**: 地理空间

## 声明的参数

* **表达式** - *无描述*<br>*表达式<字符串>*

**输出类型:** *布尔*

## 示例

### 示例 1: 基本案例

**参数值:**

* **表达式**: `h3`

| h3 | **输出** |
| ----- | ----- |
| 862a1072fffffff | true |
| not an h3 value | false |

***
