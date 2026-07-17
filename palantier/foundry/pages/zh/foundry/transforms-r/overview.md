---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-r/overview/",
  "title": "概述",
  "page_id": "overview",
  "category_id": "data-integration",
  "section_id": "transforms-r",
  "previous": "/zh/foundry/transforms-sql/spark-reference/",
  "next": "/zh/foundry/transforms-r/getting-started/",
  "scraped_at": "2026-07-13T06:08:56.638619+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

:::callout{theme="warning" title="实验性"}
R变换处于[实验性](/zh/foundry/platform-overview/development-life-cycle/)状态，可能无法在您的Foundry实例上使用。请联系您的Palantir代表以获取更多信息。
:::

在Foundry中使用R变换，您可以使用[代码工作区RStudio®工作台](/zh/foundry/code-workspaces/rstudio/)编写和发布R语言的数据变换，并访问R库。

R变换使用与Foundry中其他变换语言不同的执行模式，并提供不同的API。具体来说，R变换在单个节点上执行，并且不使用Spark进行数据读取和写入。

R变换支持使用[Palantir R SDK ↗](https://github.com/palantir/palantir-r-sdk)读取和写入结构化（表格）和非结构化数据集，并从CRAN、Posit™包管理器和Bioconductor导入R库。

[开始在Foundry中编写R变换。](/zh/foundry/transforms-r/getting-started/)

***

*RStudio®是Posit™的商标。*

所有提及的第三方商标（包括标识和图标）仍然是其各自所有者的财产。不暗示任何附属关系或认可。
