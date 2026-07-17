---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/action-types/marketplace-action-types/",
  "title": "将操作类型添加到Marketplace产品",
  "page_id": "marketplace-action-types",
  "category_id": "ontology",
  "section_id": "action-types",
  "previous": "/zh/foundry/action-types/action-log/",
  "next": "/zh/foundry/functions/overview/",
  "scraped_at": "2026-07-14T04:29:28.177795+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将操作类型添加到Marketplace产品 \[Beta]

使用[Foundry DevOps](/zh/foundry/devops/overview/)将您的操作类型包含在[Marketplace产品](/zh/foundry/devops/core-concepts/#product)中，以供其他用户安装和重用。[了解如何创建您的第一个产品。](/zh/foundry/foundry-devops/create-products/)

## 支持的功能

大多数操作类型功能都支持，除了一些引用[具有不支持功能的Object类型](/zh/foundry/object-link-types/marketplace-ontology-types/#supported-features)的操作。在为打包准备操作类型时，确保您的操作类型[**安全性和提交标准**](/zh/foundry/action-types/getting-started/#add-submission-criteria)不引用用户；将任何用户引用更新为引用群组。

## 将操作类型添加到产品

要将操作类型添加到产品，首先[创建一个产品](/zh/foundry/foundry-devops/create-products/)，然后选择如下所示的**操作类型**内容类型。

![添加操作类型](../../../images/foundry/action-types/marketplace-add-action-type.png)

然后系统会提示您选择一个操作类型。

![添加操作类型](../../../images/foundry/action-types/marketplace-add-action-type-dialog.png)

虽然您可以直接选择操作类型，但我们建议首先添加像[Workshop应用程序](/zh/foundry/workshop/marketplace-workshop/)这样的内容，然后通过如下所示的[依赖面板](/zh/foundry/foundry-devops/create-products/#content)选择相关的操作。

![通过面板添加操作类型](../../../images/foundry/action-types/marketplace-add-action-type-panel.png)
