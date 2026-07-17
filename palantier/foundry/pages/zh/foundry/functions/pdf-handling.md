---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/functions/pdf-handling/",
  "title": "PDF处理",
  "page_id": "pdf-handling",
  "category_id": "ontology",
  "section_id": "functions",
  "previous": "/zh/foundry/functions/chunking/",
  "next": "/zh/foundry/functions/edits-overview/",
  "scraped_at": "2026-07-14T04:30:05.286570+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# PDF处理

本页面提供了一个基本指南，以使用[Pipeline Builder](/zh/foundry/pipeline-builder/overview/)解析PDF以进行语义搜索，并推荐在[Workshop](/zh/foundry/workshop/overview/)应用中展示信息的方法。

语义搜索是处理PDF的强大工具，特别是当内容被分解成更小的单独嵌入的“块”时，帮助用户和工作流找到可能难以访问的重要信息。这在考虑到PDF中大量未被注意的非结构化知识时尤其有用。

要使用此功能，只需将您的PDF上传到Foundry，提取文本，分块相同的文本，搜索这些块，并通过侧边呈现相应的PDF来为用户提供交叉验证的真实来源。

## 设置语义搜索以在PDF中进行搜索

按照以下步骤导入PDF并建立语义搜索，以从PDF中呈现内容：

1. [将PDF导入为媒体集](/zh/foundry/data-integration/media-sets/#import-media)
2. [将媒体集添加到Pipeline Builder中](/zh/foundry/pipeline-builder/datasets-add/#add-datasets-from-foundry-to-pipeline-builder)
3. 使用 **获取媒体引用** 面板。

![获取媒体引用面板](../../../images/foundry/functions/get-media-references.png)

4. 使用 **文本提取** 面板。

![文本提取面板](/resources/foundry/functions/text-extraction.png)

5. 遵循[分块](/zh/foundry/functions/chunking/)策略。
6. 创建具有[媒体引用](/zh/foundry/data-integration/media-sets/#media-references)属性的块对象。
7. 在[语义搜索工作流](/zh/foundry/functions/using-palantir-provided-models-to-create-a-semantic-search-workflow/)中搜索块。
8. 在Workshop中使用[PDF查看器微件](/zh/foundry/workshop/widgets-pdf-viewer/)，注意配置选项。
