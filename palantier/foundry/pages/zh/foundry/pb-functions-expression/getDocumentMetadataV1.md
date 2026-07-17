---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-expression/getDocumentMetadataV1/",
  "title": "提取文档元数据",
  "page_id": "getDocumentMetadataV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-expression",
  "previous": "/zh/foundry/pb-functions-expression/datePartV1/",
  "next": "/zh/foundry/pb-functions-expression/getImageryMetadataV1/",
  "scraped_at": "2026-07-13T05:54:34.875927+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 提取文档元数据

> 支持于: 批处理

从文档的媒体引用中提取元数据字段。

**表达式类别**: 媒体

## 声明的参数

* **要包含的文档元数据信息** - 额外要包含的元数据列。<br>*Set\<Enum\<Bytes, Document Author, Document Title, Page Count>>*
* **媒体引用** - 包含媒体集合中PDF文件媒体引用的列。<br>*Expression\<Media reference>*

**输出类型:** *Struct*

## 示例

### 示例 1: 基本案例

**参数值:**

* **要包含的文档元数据信息**: \[`Document Author`, `Page Count`, `Document Title`]
* **媒体引用**: `Media Reference`

| 媒体引用 | **输出** |
| ----- | ----- |
| {"mimeType":"application/pdf","reference":{"type":"mediaSetItem","mediaSetItem":{"mediaSetRid":"ri.mio.test.media-set.1","mediaItemRid":"ri.mio.test.media-item.1"}}} | {<br> **author**: Jane Doe,<br> **page\_count**: 23,<br> **title**: Document Title,<br>} |

***

### 示例 2: 基本案例

**参数值:**

* **要包含的文档元数据信息**: \[`Document Title`]
* **媒体引用**: `Media Reference`

| 媒体引用 | **输出** |
| ----- | ----- |
| {"mimeType":"application/pdf","reference":{"type":"mediaSetItem","mediaSetItem":{"mediaSetRid":"ri.mio.test.media-set.1","mediaItemRid":"ri.mio.test.media-item.1"}}} | {<br> **title**: Who Framed Roger Rabbit - Final Script,<br>} |

***

### 示例 3: 基本案例

**参数值:**

* **要包含的文档元数据信息**: \[`Document Author`, `Page Count`]
* **媒体引用**: `Media Reference`

| 媒体引用 | **输出** |
| ----- | ----- |
| {"mimeType":"application/pdf","reference":{"type":"mediaSetItem","mediaSetItem":{"mediaSetRid":"ri.mio.test.media-set.1","mediaItemRid":"ri.mio.test.media-item.1"}}} | {<br> **author**: John Smith,<br> **page\_count**: 78,<br>} |

***

### 示例 4: 空案例

**参数值:**

* **要包含的文档元数据信息**: \[]
* **媒体引用**: `Media Reference`

| 媒体引用 | **输出** |
| ----- | ----- |
| {"mimeType":"application/pdf","reference":{"type":"mediaSetItem","mediaSetItem":{"mediaSetRid":"ri.mio.test.media-set.1","mediaItemRid":"ri.mio.test.media-item.1"}}} | *null* |

***
