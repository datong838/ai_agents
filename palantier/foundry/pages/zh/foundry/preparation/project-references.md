---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/preparation/project-references/",
  "title": "项目引用",
  "page_id": "project-references",
  "category_id": "data-integration",
  "section_id": "preparation",
  "previous": "/zh/foundry/preparation/preparation-tutorial/",
  "next": "/zh/foundry/preparation/basic-examples/",
  "scraped_at": "2026-07-13T06:05:53.680702+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 项目引用

在 Foundry 中，[项目](/zh/foundry/projects/overview/) 定义了相关工作的概念边界和应用及管理访问的安全边界。跨项目边界使用数据时必须格外小心。

## 项目引用

项目引用为拥有更高权限的用户（通常是数据集或管道的所有者）提供了一种机制，以允许在其他项目的管道中发现和使用数据。项目引用通过明确确认何时将数据集导入项目，为在项目之间持久移动数据增加了一层审查。

要向项目添加资源引用，请前往项目根级别的[项目详细信息面板](/zh/foundry/projects/use-project-details-panel/)。点击\*\*+添加引用\*\*按钮，以添加对数据集的引用。在下图中，数据集 `flights` 和 `training_data` 被添加为项目中的引用。这意味着您可以在准备中的保存数据集中使用 `flights` 和 `training_data` 作为输入。

![添加项目引用](../../../images/foundry/preparation/add-reference-project.png)

:::callout{theme="neutral"}
要引用资源，您必须拥有资源上的 `compass:import-resource-from` （通常扩展自 `只读角色`），以及目标项目上的 `compass:import-resource-to`（通常扩展自 `编辑者` 角色）。这些角色可以通过控制面板中的[自定义角色](/zh/foundry/administration/enrollments-and-organizations-permissions/#custom-roles)进行自定义。
:::

## 项目范围的准备

:::callout{theme="neutral"}
从 Contour 9.161.0 开始，所有新的准备都启用了项目范围。
:::

要在项目范围的准备中保存输出数据集，输入和输出数据集必须在项目范围内。

准备的输入数据集必须在项目范围内。这意味着输入数据集必须与工作簿在同一个项目中，或在项目中添加为引用。

输出数据集必须与准备在同一个项目中。

在准备界面的右上角查看准备的项目范围设置。任何超出范围的输入或输出数据集将列在项目范围对话框中。您可以选择直接从对话框中添加引用。

![在准备中查看项目范围设置](../../../images/foundry/preparation/preparation-psj-settings.png)

当输入数据集超出范围时，您将无法保存输出数据集。

![准备超出范围错误](../../../images/foundry/preparation/preparation-oos-warning.png)

:::callout{theme="neutral"}
如果您不保存已清理的数据集，则无需添加引用即可在输入数据集上使用准备。
:::

## 启用准备的项目范围

如果您在项目范围默认启用之前创建了准备，可以在准备的右上角启用项目范围。在启用项目范围之前，您必须通过添加对输入的引用来解决任何超出范围的输入，并通过将输出移至准备的项目来解决任何超出范围的输出。
