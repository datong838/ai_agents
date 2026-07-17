---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-health/marketplace-data-health/",
  "title": "将健康检查添加到Marketplace产品",
  "page_id": "marketplace-data-health",
  "category_id": "data-integration",
  "section_id": "data-health",
  "previous": "/zh/foundry/data-health/view-check-group/",
  "next": "/zh/foundry/dataset-preview/overview/",
  "scraped_at": "2026-07-13T06:04:32.432882+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将健康检查添加到Marketplace产品 \[Beta]

使用[Foundry DevOps](/zh/foundry/devops/overview/)将您的数据健康检查包含在[Marketplace产品](/zh/foundry/devops/core-concepts/#product)中，供其他用户安装和重用。[了解如何创建您的第一个产品。](/zh/foundry/foundry-devops/create-products/)

## 支持的功能

将健康检查添加到Marketplace产品时支持以下功能：

* 数据集上的健康检查。
* 健康检查配置验证支持所有情况，除了：
  * 数据集验证（例如，涉及次要数据集验证的健康检查）。
  * 路径配置验证（例如，具有源路径验证的健康检查）。
  * 具有创建[Foundry问题](/zh/foundry/getting-started/issues/)配置的健康检查。
* 健康检查组（包括具有[监控视图](/zh/foundry/maintaining-pipelines/monitoring-views-intro/)的组）会自动作为输入添加，这样，打包在组中的所有健康检查将在[安装](/zh/foundry/marketplace/install-product/)期间添加到提供的输入组中。
* 如果打包了包含数据期望的[数据集变换](/zh/foundry/code-repositories/marketplace-dataset-transformation/)，则[数据期望](/zh/foundry/pipeline-builder/dataexpectations-overview/)健康检查会自动添加。这些类型的检查无法由打包者手动添加或删除，因为它们是变换逻辑的一部分。

## 将数据健康检查添加到产品

要将数据健康检查添加到产品中，首先[创建一个产品](/zh/foundry/foundry-devops/create-products/)，然后将[数据集变换](/zh/foundry/code-repositories/marketplace-dataset-transformation/)或[Pipeline Builder管道](/zh/foundry/pipeline-builder/marketplace-pipeline-builder/)添加到您的产品中。然后，您可以将与数据集变换或管道的输出数据集相关联的任何检查进行打包，如下所示。

![添加健康检查](/resources/foundry/data-health/marketplace-add-health-check.png)
