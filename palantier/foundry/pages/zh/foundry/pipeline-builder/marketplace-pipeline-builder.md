---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/marketplace-pipeline-builder/",
  "title": "向Marketplace产品添加pipeline",
  "page_id": "marketplace-pipeline-builder",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/dataexpectations-unit-tests/",
  "next": "/zh/foundry/pb-functions-expression/absV1/",
  "scraped_at": "2026-07-13T05:52:00.446744+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 向Marketplace产品添加pipeline \[Beta]

使用[Foundry DevOps](/zh/foundry/devops/overview/)将您的Pipeline Builder pipelines包含在[Marketplace产品](/zh/foundry/devops/core-concepts/#product)中，以供其他用户安装和重用。[了解如何创建您的第一个产品。](/zh/foundry/foundry-devops/create-products/)

## 支持的功能

Marketplace产品支持所有Pipeline Builder功能，但以下情况除外：

* 具有时间序列目标的流式pipeline
* 以下类型的参数：结构类型**常量**、不由常量组成的复杂**表达式**、**选项**和**结构定位器**。

### 使用Marketplace linter检查Marketplace兼容性

在Pipeline Builder中，您可以使用Marketplace linter检查pipeline是否与Marketplace兼容。要启用此功能，请导航到**设置**，并在您的pipeline中选择**启用Marketplace验证**。此设置默认未启用。

![启用Marketplace验证设置。](../../../images/foundry/pipeline-builder/marketplace-settings-enable-validation.png)

启用后，pipeline底部的**Pipeline警告**部分将显示任何阻止您的pipeline在Marketplace中打包的出错。

![Pipeline警告示例。](../../../images/foundry/pipeline-builder/marketplace-pipeline-warnings.png)

如果没有Marketplace不兼容性，则错误/警告抽屉中不会出现**Marketplace打包警告**。请注意，其他类型的pipeline出错或警告可能仍然会出现。

## 将Pipeline Builder pipelines添加到产品

要将Pipeline Builder pipeline添加到产品中，首先[创建一个产品](/zh/foundry/foundry-devops/create-products/)，然后选择如下所示的**Pipeline**内容类型。

![添加pipeline](/resources/foundry/pipeline-builder/marketplace-add-pipeline.png)

## Pipeline参数

您可以使用[pipeline参数](/zh/foundry/pipeline-builder/management-parameter-overview/)以便安装者在安装时自定义他们的pipeline。例如，您可以使用`boolean`参数根据安装者的输入选择pipeline的一个分支而不是另一个。参见[支持的功能](#supported-features)以获取支持的参数类型列表。当您使用参数打包pipeline时，该参数将作为[pipeline的依赖项](/zh/foundry/foundry-devops/create-products/#content)和安装者的[输入](/zh/foundry/foundry-devops/create-products/#inputs)显示，如下所示。

![参数](../../../images/foundry/pipeline-builder/marketplace-parameter.png)

## 打包设置

要配置安装者所需或非必填的数据集和列，请导航到**Pipeline输出面板 > 设置**以访问**打包设置**。

![打包设置](../../../images/foundry/pipeline-builder/marketplace-packaging-settings.png)

默认情况下，所有列和输入数据集对于Marketplace安装都是必需的。如果有任何不需要的列或输入数据集，您可以将它们标记为非必填。非必填的输入数据集将默认为空，非必填的列值将在pipeline逻辑中使用时默认为null。

![打包设置对话框](../../../images/foundry/pipeline-builder/marketplace-packaging-settings-dialog.png)
