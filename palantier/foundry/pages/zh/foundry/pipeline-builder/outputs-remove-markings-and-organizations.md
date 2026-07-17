---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/outputs-remove-markings-and-organizations/",
  "title": "从输出中移除权限标记",
  "page_id": "outputs-remove-markings-and-organizations",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/outputs-deliver-pipeline/",
  "next": "/zh/foundry/pipeline-builder/breaking-changes/",
  "scraped_at": "2026-07-13T05:49:53.460048+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 从输出中移除权限标记

平台资源的访问要求由[权限标记](/zh/foundry/security/markings/)控制。权限标记以全有或全无的方式限制访问：要访问资源，用户必须是应用于该资源的所有权限标记的成员。此外，权限标记通过文件层次结构和直接依赖关系继承。

如果您具有特定权限标记的`移除权限标记`权限，现在可以从Pipeline Builder中的输出中移除继承的权限标记。这相当于代码库中的[`停止传播`](/zh/foundry/building-pipelines/remove-inherited-markings/)参数。

:::callout{theme="neutral"}
移除输出上的权限标记相当于停止从输入传播权限标记。
:::

## 先决条件

在使用Pipeline Builder移除权限标记之前，您必须完成以下步骤。

### 启用分支保护

1. 在Pipeline Builder中，选择**设置**，然后选择**管理分支**。

![Pipeline Builder中的设置和管理分支选项。](../../../images/foundry/pipeline-builder/markings-settings.png)

2. 选择**分支保护**选项卡。

![Pipeline Builder中的管理分支保护弹出菜单。](../../../images/foundry/pipeline-builder/markings-manage-branch.png)

### 需要代码审批

1. 在**分支保护**选项卡中，勾选**要求提议以更新受保护分支**和**合并前需要审批**的框。
2. 指定所需的审批策略。下面显示了一个示例审批策略。

![Pipeline Builder中的示例审批策略。](../../../images/foundry/pipeline-builder/markings-example-code-approval.png)

### 在管道设置中启用对安全权限标记的更改

1. 导航到**安全审批**选项卡，并勾选**允许更改此管道中的安全权限标记**旁边的框。您必须在管道上拥有`Owner`角色才能完成此步骤。

![Pipeline Builder中的安全审批选项卡。](../../../images/foundry/pipeline-builder/markings-security-approvals.png)

一旦您**允许更改此管道中的安全权限标记**，就不能禁用分支保护或移除代码审批要求。必须禁用**允许更改此管道中的安全权限标记**以禁用这些功能。

一旦在受保护的分支中移除权限标记，您不能从**安全审批**选项卡中禁用**允许更改此管道中的安全权限标记**。必须先撤销权限标记的移除才能禁用此设置。

## 移除权限标记

1. [创建一个分支](/zh/foundry/pipeline-builder/branches-create-a-branch/)从受保护的分支上。

2. 导航到屏幕右侧的**管道输出**，将鼠标悬停在要移除的权限标记的输出上。然后，选择**编辑**。

![Pipeline Builder中的管道输出选项卡。](../../../images/foundry/pipeline-builder/markings-pipeline-output.png)

3. 在输出数据集下选择**配置权限标记**下拉菜单。

![Pipeline Builder输出上的配置权限标记下拉菜单。](../../../images/foundry/pipeline-builder/markings-configure-markings-option.png)

4. 在弹出菜单中的**继承的权限标记**部分，选择要移除的权限标记旁边的红色移除图标。

![Pipeline Builder中移除输出上的权限标记的弹出对话框。](../../../images/foundry/pipeline-builder/markings-inherited-markings.png)

移除的权限标记现在将显示在对话框中的**已移除权限标记**部分。

![弹出对话框中已移除的权限标记部分中的移除权限标记。](../../../images/foundry/pipeline-builder/markings-removed.png)

5. 选择**应用**。您现在应该会在输出面板的左上角看到一个带有负号的盾牌图标，表示您正在移除多少个权限标记。

![Pipeline Builder输出上的移除权限标记图标。](../../../images/foundry/pipeline-builder/markings-removed-pop-up.png)

:::callout{theme="neutral"}
您应用于输出上的权限标记的更改不会生效，直到分支成功合并并部署到受保护的分支上。如果您尝试在您的分支上搭建数据集，它仍将显示原始权限标记。
:::

### 提出您的更改

1. 要使您对管道输出上的权限标记的更改生效，请[创建提议](/zh/foundry/pipeline-builder/branches-propose-a-change/)以将更改合并到受保护的分支中。提议将包括一个用于批准权限标记移除的部分，类似于[管道代码审批](/zh/foundry/pipeline-builder/branches-approve-a-change/)。

您必须具有`移除权限标记`权限才能批准更改。移除权限标记的提议的审批者不需要是管道所有者，只需对提议具有`查看`访问权限。

![从管道输出中移除权限标记的提议。](../../../images/foundry/pipeline-builder/markings-approval-page-pull-request.png)

每个移除的权限标记都需要单独检查，这意味着您可能在一个提议中有多个检查。当您批准权限标记移除时，您的批准将适用于您有权审核的每个权限标记。

一旦授予所有必需的批准，提议将被允许合并。部署该版本将允许权限标记移除生效。

### 撤销从管道输出中移除权限标记

1. 要撤销权限标记的移除，导航到屏幕右侧的**管道输出**，将鼠标悬停在您移除的权限标记的输出上。

2. 选择**编辑**。

![Pipeline Builder中的管道输出选项卡。](../../../images/foundry/pipeline-builder/markings-pipeline-output.png)

3. 在输出数据集下选择**配置权限标记**下拉菜单。

![Pipeline Builder输出上的配置权限标记下拉菜单。](../../../images/foundry/pipeline-builder/markings-configure-markings-option.png)

4. 在弹出对话框中的**未传播的权限标记**部分选择撤销图标。

![权限标记移除弹出对话框，选择撤销停止传播的权限标记选项。](../../../images/foundry/pipeline-builder/markings-undo-remove-marking.png)

5. 选择**应用**，然后从屏幕右上角保存您的管道。

![屏幕右上角的管道保存按钮。](../../../images/foundry/pipeline-builder/markings-save-pipeline.png)

6. [提出您的更改](/zh/foundry/pipeline-builder/branches-propose-a-change/)以开始[审批检查](/zh/foundry/pipeline-builder/branches-approve-a-change/)。

7. 一旦获得批准，[部署](/zh/foundry/pipeline-builder/outputs-deliver-pipeline/)您的管道。

:::callout{theme="neutral"}
撤销权限标记的移除不需要提升的权限，与移除权限标记所需的权限不同。
:::

### 权限标记和任务组

在任务组中，所有输入的权限标记将被同一任务组内的所有输出继承。要查看示例并了解有关任务组的更多信息，请查看我们的[文档](/zh/foundry/pipeline-builder/management-job-groups/)。

### 权限标记和多个受保护的分支

如果在任何分支上有权限标记的移除，您必须在保护或取消保护分支之前停止从管道中的所有分支移除权限标记。当多个分支受到保护时，权限标记的移除将针对所有受保护的分支。

当启用安全审批设置时，您将无法更改分支保护设置，包括保护或取消保护分支。
