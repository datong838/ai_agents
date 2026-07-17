---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/marketplace-schedules/",
  "title": "向市场产品添加计划 [测试版]",
  "page_id": "marketplace-schedules",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/schedule-troubleshooting/",
  "next": "/zh/foundry/building-pipelines/logic-flows-overview/",
  "scraped_at": "2026-07-13T05:41:43.538087+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 向市场产品添加计划 \[测试版]

使用[Foundry DevOps](/zh/foundry/devops/overview/)将您的计划包含在[市场产品](/zh/foundry/devops/core-concepts/#product)中，以供其他用户安装和重用。[了解如何创建您的第一个产品。](/zh/foundry/foundry-devops/create-products/)

## 支持的功能

我们支持将符合以下条件的计划包含在市场产品中：

* 计划不是用户范围的。
* 计划没有[回退分支](/zh/foundry/code-repositories/branch-settings/#fallback-branches)。
* 所有[触发器](/zh/foundry/building-pipelines/triggers-reference/)应为同一分支定义。
* [触发器](/zh/foundry/building-pipelines/triggers-reference/)或[目标](/zh/foundry/building-pipelines/create-schedule/#target-datasets)数据集不是[受限视图](/zh/foundry/security/restricted-views/)。

我们强烈建议所有打包的数据集（不包括静态数据集）都有一个相应的计划以目标为数据集。如果数据集未包含计划，则该数据集及其下游的任何内容将变得陈旧。

## 向产品添加计划

要向产品添加计划，首先[创建一个产品](/zh/foundry/foundry-devops/create-products/)，然后选择如下所示的 **Schedule** 内容类型。

![add schedule](/resources/foundry/building-pipelines/marketplace-add-schedule.png)

如果您尚未添加任何[管道](/zh/foundry/pipeline-builder/marketplace-pipeline-builder/)或[数据集变换](/zh/foundry/code-repositories/marketplace-dataset-transformation/)，您将没有任何计划可供选择。鉴于此，我们通常建议先添加这些资源类型。一旦添加了管道或数据集变换，查看 **Datasets** 内容类型以审查哪些数据集不会被搭建，以及您可以添加到产品中的计划以解决此问题。

![add highlighted schedule](../../../images/foundry/building-pipelines/marketplace-add-highlighted-schedules.png)

选择任何相关的计划以包含在您的产品中。如果您没有看到任何计划，您应该[使用您的源数据集创建一个计划](/zh/foundry/building-pipelines/create-schedule/)，然后[创建产品的新版本](/zh/foundry/foundry-devops/manage-products/)。

![add schedule dialog](../../../images/foundry/building-pipelines/marketplace-schedule-dialog.png)
