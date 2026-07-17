---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/extractFileMetadataAsRowsV1/",
  "title": "从数据集中提取文件元数据为行",
  "page_id": "extractFileMetadataAsRowsV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/emptyTableV1/",
  "next": "/zh/foundry/pb-functions-transform/getManyStructFieldsV1/",
  "scraped_at": "2026-07-13T05:58:18.419577+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从数据集中提取文件元数据为行

> 支持于: 批处理

从文件数据集中读取文件元数据为行。

**变换类别**: 文件

## 声明的参数

* **数据集** - 文件数据集。<br>*文件*
* **要包含的数据集信息** - 要包含的附加元数据列。<br>*集合<枚举<文件修改时间戳、文件大小（字节）、包含输入数据集分支、输入数据集 RID>>*
