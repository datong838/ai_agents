---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/code-repositories/artifact-repositories-overview/",
  "title": "Artifact 存储库",
  "page_id": "artifact-repositories-overview",
  "category_id": "data-integration",
  "section_id": "code-repositories",
  "previous": "/zh/foundry/code-repositories/marketplace-dataset-transformation/",
  "next": "/zh/foundry/code-repositories/artifact-repositories-nav/",
  "scraped_at": "2026-07-13T06:00:14.411456+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Artifact 存储库

Artifact 存储库使用户能够发布和管理 Artifact，包括 [Conda ↗](https://docs.conda.io/en/latest/)、[Docker ↗](https://www.docker.com/) 和 [Maven ↗](https://maven.apache.org/what-is-maven.html)。

Artifact 存储库被用于在上传所有非以[库](/zh/foundry/transforms-python/use-python-libraries/)形式创作或通过外部 URL 访问的 Conda、Docker 或 Maven Artifact。例如，您可能在本地机器上编写了一个 Conda 包，您希望在代码存储库中访问它。通过将 Conda 包发布到 Artifact 存储库，您将可以从[代码存储库](/zh/foundry/code-repositories/overview/)中的 **Library** 搜索面板访问它。

Artifact 存储库的关键功能包括：

* [**发布 Artifact:**](/zh/foundry/code-repositories/publish-artifact/) 生成词元并将 Artifact 推送到 Artifact 存储库。
* [**搜索 Artifact:**](/zh/foundry/code-repositories/artifact-repositories-nav/#search) 从 Artifact 存储库界面查找 Artifact。
* [**召回 Conda Artifact:**](/zh/foundry/code-repositories/recall-artifact/) 召回 Conda Artifact，以防止下游消费者使用特定版本编译代码。

了解更多关于 Artifact 存储库[界面](/zh/foundry/code-repositories/artifact-repositories-nav/)的信息以及如何[创建一个 Artifact 存储库](/zh/foundry/code-repositories/create-artifact-repository/)。
