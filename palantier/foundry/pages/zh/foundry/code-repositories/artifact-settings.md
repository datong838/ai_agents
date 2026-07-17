---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/code-repositories/artifact-settings/",
  "title": "工件设置",
  "page_id": "artifact-settings",
  "category_id": "data-integration",
  "section_id": "code-repositories",
  "previous": "/zh/foundry/code-repositories/spark-profiles/",
  "next": "/zh/foundry/code-repositories/ontology-imports/",
  "scraped_at": "2026-07-13T06:01:34.900748+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 工件设置

:::callout{theme="neutral"}
如果您希望导入和使用Python库，请参阅有关[共享Python库](/zh/foundry/transforms-python/share-python-libraries/)的部分。
:::

工件选项卡包含可以在您的代码库中引用的库列表，我们称之为支持库。这是您Foundry环境中所有共享代码库的列表，以及外部或公共库。您可以使用工件选项卡来发现和添加支持库。

:::callout{theme="neutral"}
查看工件设置需要`artifacts:view-repository`权限，管理工件设置需要`artifacts:manage-repository`权限。
:::

![artifact-settings-tab](../../../images/foundry/code-repositories/repository-artifact-settings-tab.png)

### 向您的代码库添加新工件

要添加新工件，请点击“添加”并选择两种类型的库之一：

1. **本地库** - 这些是您的Foundry环境中配置为[共享库](/zh/foundry/code-repositories/libraries/)的其他代码库。
2. **外部库** - 存储在您的Foundry环境之外的工件库。这些可能是外部Foundry库或在您的环境中可用的公共工件库。

![artifact-settings-add-repository](../../../images/foundry/code-repositories/repository-artifact-settings-add-repo.png)

如果添加的工件库包含对其他库的引用，它们也会被添加。所有已添加库的依赖项需要相同的访问权限。

:::callout{theme="neutral"}
当从不同项目添加本地库时，将向该库添加项目引用。这需要在您自己的代码库上具有`compass:view-project-imports`和`compass:import-resource-to`权限，并在引用的共享库上具有`compass:import-resource-from`权限。
:::

:::callout{theme="warning" title="警告"}
虽然可以重新排序和删除支持库，但这可能会破坏使用这些库中的包的变换的搭建。只有在考虑可能的影响后再采取此操作。
:::
