---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/management-create-custom-functions/",
  "title": "创建自定义函数",
  "page_id": "management-create-custom-functions",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/management-build-settings/",
  "next": "/zh/foundry/pipeline-builder/management-show-hide-nodes/",
  "scraped_at": "2026-07-13T05:51:00.767751+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建自定义函数

自定义函数使您能够将一系列变换保存为单个变换，以便在您的管道中重复使用。此功能对于在管道中重复逻辑但在单一位置进行管理非常有用。

一个自定义函数包括一个**名称**（必填）、**描述**（非必填）、**函数参数**（非必填）和**函数定义**（必填）。

创建自定义函数需要两个步骤：

1. 将您的逻辑定义为一系列变换面板。
2. 将变换面板转换为新的自定义函数。

下面，我们将为每个步骤提供一个示例。

## 定义一系列变换面板

假设您有一个`users`表，并且您想创建一个主键以唯一标识每个用户。您知道每个用户的`first_name`、`last_name`和`first_login_date`是一个唯一的组合。您希望向数据集中添加一个`String`类型的`primary_key`列，它是这三列的哈希值，然后删除`first_name`、`last_name`和`first_login_date`。最后，如果有重复项，您希望每个用户只保留一行，并保留`age`值最低的行。

![用户输入表的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-1@2x.png)

首先，将`first_name`、`last_name`和`first_login_date`合并到一列中。您可以使用`Concatenate strings`变换将这三列合并在一起。

![连接字符串变换的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-2@2x.png)

在`Separator`字段中输入`-`。然后，在**Expressions**下拉菜单中选择每一列。对于前两列，选择`first_name`和`last_name`。然而，`first_login_date`列不是我们第三个字段可供选择的选项。这是因为它是`Date`类型，而`Concatenate strings`函数只接受`String`类型。

![连接字符串变换不包含日期列的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-3@2x.png)

为了解决这个问题，从**Expressions**选项卡中插入一个`Cast`表达式。参数将是`first_login_date`作为`Expression`，以及`String`作为要转换的`Type`。这样可以避免您需要全局更改`first_login_date`，因为这会影响所有下游变换面板。

![连接字符串变换包含转换表达式的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-4@2x.png)

一旦您选择`Apply`，输出表应如下所示：

![连接字符串变换后的输出表截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-5@2x.png)

现在，您必须对`primary_key`中的数据进行去标识化。实现这一点的一种方法是通过应用`Hash sha256`变换为`primary_key`中的每个值创建一个哈希。在同一个面板中，选择`Reuse value`选项，将`Concatenate strings`替换为`Hash sha256`。

![复用值与哈希sha256变换的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-6@2x.png)

此选项保留现有值并将其作为新变换的第一个输入。

![哈希sha256变换的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-7@2x.png)

选择`Apply`后，验证您的输出是否与预期一致：一个包含关于每行的唯一数据的`primary_key: String`列。

![中间输出表预览的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-8@2x.png)

现在，您会注意到`primary_key`中的第一行和最后一行是相同的。您希望保留`age`为25的行，并删除`first_name`、`last_name`和`first_login_date`。为此，添加一个`Aggregate`变换。在第一个字段`Group by columns`中输入`primary_key`，在第二个字段`Aggregations`中输入`age`，并使用`Min`表达式：

![聚合变换的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-9@2x.png)

最后，输出表应如下图所示。您可以验证`primary_key = b3c01...`只有一行，并且`age`是25。

![最终输出表预览的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-10@2x.png)

## 将一系列变换面板转换为自定义函数

现在，假设您希望在管道中的三个不同位置重复使用此逻辑。我们可以通过使用`Shift + Down Arrow`选择这两个面板，然后选择顶部栏中的\*\*+\*\*按钮，将我们的逻辑转换为自定义函数。

![将多个变换面板转换为自定义函数的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-11@2x.png)

这将带您进入自定义函数创建页面。您会注意到列输入`first_name`、`last_name`、`first_login_date`和`age`被划掉；这是因为您正在创建的函数将在您的管道中对任何四个正确类型的输入都是通用的，无论列名是什么。

![自定义函数创建页面的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-12@2x.png)

要定义这些输入，选择**Add argument**四次。通过点击黄色框来配置参数名称。

![自定义函数参数初始配置的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-13@2x.png)

然后，通过点击每个参数右侧的齿轮图标配置参数类型。这里，您希望前两个参数为`Expression<String>`类型，以表示`String`类型的列，第三个参数为`Expression<Date>`类型，最后一个参数为`Expression<Integer>`类型。

![自定义函数参数完整配置的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-14@2x.png)

现在，您可以像之前一样将新的参数添加到这两个面板中。然而，它们现在会在`Parameters`部分而不是`Columns`部分中可用。

![具有参数的自定义函数的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-15@2x.png)

一旦您完成配置，为函数命名为`Primary key generator`，给它一个非必填描述，并选择**Apply all changes**。

![自定义函数参数最终配置的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-16@2x.png)

新的函数现在可以在任何变换路径中使用。下次您需要使用此模式创建主键时，可以在变换下拉菜单中搜索`Primary key generator`。

![在搜索栏中可用的自定义函数的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-17@2x.png)

您可以使用原始列`first_name`、`last_name`、`first_login_date`和`age`填充您的自定义函数。

![变换路径中自定义函数配置的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-18@2x.png)

通过将相关的列名称填入您的自定义函数中，您将产生与在路径中使用相同变换创建函数相同的结果。然而，通过创建自定义函数，您可以保存函数逻辑以在管道中重复使用，而不是使用单独的变换面板重新创建逻辑。

![最终输出表预览的截图](../../../images/foundry/pipeline-builder/transforms-custom-functions-10@2x.png)
