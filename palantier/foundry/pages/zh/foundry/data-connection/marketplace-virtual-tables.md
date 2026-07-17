---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/marketplace-virtual-tables/",
  "title": "将虚拟表添加到Marketplace产品",
  "page_id": "marketplace-virtual-tables",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/marketplace-data-connection/",
  "next": "/zh/foundry/hyperauto/overview/",
  "scraped_at": "2026-07-13T05:32:24.867795+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将虚拟表添加到Marketplace产品 \[Beta]

使用[Foundry DevOps](/zh/foundry/devops/overview/)将您的[虚拟表](/zh/foundry/data-integration/virtual-tables/)包含在[Marketplace产品](/zh/foundry/devops/core-concepts/#product)中，以供其他用户安装和重用。[了解如何创建您的第一个产品。](/zh/foundry/foundry-devops/create-products/)

## 支持的功能

所有虚拟表都可以打包和同步。

目前，不支持单独打包源，也不支持打包启用虚拟表自动注册的源。

安装人员必须确保目标源在相同位置包含与原始源具有相同模式的表，以保证兼容性和功能性。

## 将虚拟表添加到产品中

要将虚拟表添加到产品中，首先[创建一个产品](/zh/foundry/foundry-devops/create-products/)，然后选择如下的**虚拟表**内容类型。

![将虚拟表添加到您的产品](/resources/foundry/data-connection/marketplace-add-virtual-table.png)

然后您可以选择要包含在产品中的虚拟表。

![为您的产品选择虚拟表](../../../images/foundry/data-connection/marketplace-virtual-table-selection.png)
