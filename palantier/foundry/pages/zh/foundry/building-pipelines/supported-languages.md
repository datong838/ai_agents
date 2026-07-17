---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/supported-languages/",
  "title": "支持的语言",
  "page_id": "supported-languages",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/pipeline-types/",
  "next": "/zh/foundry/building-pipelines/considerations-pb-cr/",
  "scraped_at": "2026-07-13T05:39:46.641352+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 支持的语言

在开始进行数据变换之前，考虑每种语言的优点和限制是很重要的。下表总结了支持语言之间的主要区别：

|描述|[SQL](#sql)|[Python](#python)|[Java](#java)|
|---|---|---|---|
|*非专有语言：* 在线文档可用|✓|✓|✓|
|*支持文件访问：* 读取和写入Foundry数据集中文件——这意味着你的数据变换可以操作非结构化数据| |✓|✓|
|*变换级别逻辑版本控制 (TLLV)：* 更多信息请参见[TLLV部分](/zh/foundry/transforms-python/transforms-pipelines/#transform-logic-level-versioning)|✓|✓| |
|*增量计算：* 更多信息请参见[增量计算部分](/zh/foundry/building-pipelines/incremental-overview/)| |✓|✓|
|*支持删除继承的权限标记*|✓|✓|✓|
|*每个文件允许多个输出数据集*| |✓|✓|
|*支持数据集预览*|✓|✓|✓|
|*自定义变换配置* |✓|✓|✓|

## SQL

SQL是一种有大量在线文档可用的语言。以下是使用SQL进行数据变换的一些主要优点：

* SQL是性能最优的语言（包括大多数Spark优化）。
* 变换SQL为你提供一个SQL草稿本，允许你运行示例SQL查询以检查你的SQL语法。

[了解更多关于SQL变换的信息。](/zh/foundry/transforms-sql/overview/)

## Python

Python是一种有大量在线文档可用的语言。你可能希望使用Python进行数据变换，以利用Python的特定功能和库。Python API比其他语言如SQL更底层。以下是使用Python的一些主要优点：

* [`transforms` Python库](/zh/foundry/transforms-python/transforms-python-api/) 是一个API，提供文件读取和写入等功能。基于文件的数据变换在数据变换管道的早期阶段非常有用，当你需要解析和清理数据时。
* 对使用外部库如pandas、NumPy和其他机器学习库有一流的支持。
* 你可以访问完整的Spark Python (PySpark) API，其中包括其他语言不支持的Spark附加功能。

[了解更多关于Python变换的信息。](/zh/foundry/transforms-python/overview/)

## Java

Java是一种有大量在线文档可用的语言。你可能希望使用Java进行数据变换，以利用Java的特定功能。Java API比其他语言如SQL更底层。以下是使用Java的一些主要优点：

* `transforms` Java库是一个API，提供文件读取和写入等功能。基于文件的数据变换在数据变换管道的早期阶段非常有用，当你需要解析和清理数据时。

[了解更多关于Java变换的信息。](/zh/foundry/transforms-java/overview/)
