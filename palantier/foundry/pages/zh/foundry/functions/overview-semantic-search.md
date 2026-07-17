---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/functions/overview-semantic-search/",
  "title": "概述",
  "page_id": "overview-semantic-search",
  "category_id": "ontology",
  "section_id": "functions",
  "previous": "/zh/foundry/functions/api-media/",
  "next": "/zh/foundry/functions/using-palantir-provided-models-to-create-a-semantic-search-workflow/",
  "scraped_at": "2026-07-14T04:29:56.333085+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

语义搜索是一种基于内在意义或上下文的文本搜索方式，而不仅仅依赖于关键词或其他传统的搜索方法。

语义搜索通过使用AI模型将文本变换为向量来实现，这些向量是数字数组，被称为“嵌入”。如果模型有效，那么在N维空间中彼此接近的向量，它们具有相似的基础或语义意义。例如，“面罩”的嵌入向量将比“呼吸器”更接近“面部覆盖物”的嵌入向量。

![嵌入可视化](/resources/foundry/functions/aip-embeddings-visualization.png)

如果嵌入的文本与[Ontology](/zh/foundry/ontology/overview/)中的特定Object相关联，那么您的搜索驱动的操作流程将变得更加有用。找到相关实体或与特定搜索查询相关的实体就如同在N维空间中找到最近的向量。

查看以下文档页面，了解与语义搜索相关的主题：

* [了解如何使用Palantir提供的模型创建语义搜索工作流](/zh/foundry/functions/using-palantir-provided-models-to-create-a-semantic-search-workflow/)
* [了解如何使用自定义模型创建语义搜索工作流](/zh/foundry/functions/using-custom-models-to-create-a-semantic-search-workflow/)
* [了解如何将分块融入您的语义搜索工作流](/zh/foundry/functions/chunking/)
* [了解如何在语义搜索工作流中使用PDF](/zh/foundry/functions/pdf-handling/)
* 如需更多学习资料，请参阅我们的[YouTube视频“搭建Palantir AIP: 语义搜索” ↗](https://youtu.be/7rRLOTXe60Q)和[博客“搭建Palantir AIP: 语义搜索” ↗](https://blog.palantir.com/building-with-palantir-aip-semantic-search-dc3adf40f6a6)。
