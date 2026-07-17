---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/unstructured-overview/",
  "title": "概览",
  "page_id": "unstructured-overview",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/building-production-pipeline/",
  "next": "/zh/foundry/building-pipelines/infer-schema/",
  "scraped_at": "2026-07-13T05:42:31.403263+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概览

如在[datasets](/zh/foundry/data-integration/datasets/)的概览中讨论的那样，Foundry中的非结构化数据被存储为数据集中一系列文件，就像表格数据一样。

以下是一些在结构化和非结构化数据的管道中相同的功能：

* 管道可以增量化，以优化计算性能。
* 您可以针对您的管道编写单元测试。
* 计算输出数据集是通过[搭建](/zh/foundry/data-integration/builds/)和[计划](/zh/foundry/building-pipelines/scheduling-overview/)完成的。
* Foundry的[管道安全性](/zh/foundry/building-pipelines/security-overview/)功能提供了强大的端到端安全保证。

与表格数据的管道的不同之处包括：

* 文档中的大多数指导和示例代码集中在处理数据帧，而数据帧不是用于非结构化数据的输入类型。
* 您必须使用底层文件系统API来读取和写入非结构化数据集中的文件。
* 因为非结构化数据集没有模式，一些专注于验证表格数据集行和列的功能不可用。
* 可以使用Spark并行处理非结构化文件，但API比数据帧处理的API更低级且更复杂。

要开始使用非结构化数据的管道，请参考Python和Java变换的相关文档部分：

* [Python变换：读取和写入非结构化文件](/zh/foundry/transforms-python/unstructured-files/)
* [Java变换：读取和写入非结构化文件](/zh/foundry/transforms-java/unstructured-files/)

一旦非结构化数据被清理和规范化，您可以使用[代码工作簿](/zh/foundry/code-workbook/overview/)来分析非结构化数据集并在Python和R中训练机器学习模型。[了解更多关于代码工作簿中非结构化数据访问的信息](/zh/foundry/code-workbook/transforms-unstructured/)。
