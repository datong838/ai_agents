---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/environment-overview/",
  "title": "概览",
  "page_id": "environment-overview",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/create-historical-dataset/",
  "next": "/zh/foundry/transforms-python/environment-creation-overview/",
  "scraped_at": "2026-07-13T06:06:51.601213+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概览

用于变换的**Python环境**是在检查期间使用Hawk包管理器根据[`conda_recipe/meta.yaml`](/zh/foundry/transforms-python/project-structure/#metayaml)文件中指定的包列表解决的。使用包选项卡，您可以[发现可用包并自动将其添加到您的`meta.yml`以便于环境解析](/zh/foundry/transforms-python/use-python-libraries/)。这个解析后的环境会在内部发布到Artifacts中，准备在搭建过程中使用。

当变换被搭建时，它会获取环境文件并安装环境文件中指定的所需包。如果由于某种原因失败，变换将在搭建过程中使用Hawk再次解析环境。

### 有用的资源

请参阅[环境创建简介](/zh/foundry/transforms-python/environment-creation-overview/)，了解使用Conda、Mamba和Hawk创建环境的介绍。有关常见环境问题的一般故障排除，请参阅[环境故障排除指南](/zh/foundry/transforms-python/environment-troubleshooting/)。
