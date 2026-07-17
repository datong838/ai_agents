---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/branches-overview/",
  "title": "概览",
  "page_id": "branches-overview",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/export-pipeline/",
  "next": "/zh/foundry/pipeline-builder/branches-create-a-branch/",
  "scraped_at": "2026-07-13T05:50:57.865216+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概览

版本控制与分支在Foundry中广泛使用，是Pipeline Builder的重要组成部分。版本控制对于维护健康的流水线工作流、支持安全协作以及确保主生产分支的保护至关重要。

Pipeline Builder将流水线工作流的每个独特版本称为流水线\_分支\_（类似于Git中的分支），其中一个分支用作**主分支**。

![分支截图](../../../images/foundry/pipeline-builder/pb-branch-selector.png)

**分支**是流水线的副本，用户可以在其上进行迭代而无需保存回主流水线。Pipeline Builder中的分支类似于Git代码库中的代码分支；用户在自己的分支中进行编辑和测试更改，而不会对流水线产生负面影响。每个流水线工作流从一个**主分支**开始，用户可以在需要协作时从主分支创建其他分支。当用户对其分支中的更改感到满意时，他们可以提议将分支合并到**主分支**中。

了解更多关于[Foundry中的分支工作流](/zh/foundry/data-integration/branching/)。

## 管理分支

要管理分支，导航到顶部工具栏并选择指示您当前分支的下拉菜单。从下拉菜单中选择**管理分支**。

### 活动分支

在**活动分支**选项卡中，查看所有当前活动的分支，或选择存档一个活动分支。存档的分支将不会在流水线图中的分支下拉菜单中显示，并且除非恢复，否则无法编辑或使用。要恢复存档的分支，请在**活动分支**选项卡中选择**查看存档分支**。找到要恢复的分支，然后选择右侧的**恢复分支**图标。

### 分支保护

在此选项卡中，启用\*\*需要提案...\*\*以通过防止用户对指定分支进行直接更改来保护一个或多个分支。此选项要求用户对单独的分支进行更改，然后才能将其合并到任何受保护的分支中。

![配置多个受保护分支的截图。](../../../images/foundry/pipeline-builder/branches-multiple-protected.png)

选择\*\*至少需要一个批准...\*\*以添加另一层保护，要求对拟议更改进行其他用户批准后才能合并到主分支。有效的批准者是对流水线具有`编辑`权限且未对提议更改做出贡献的用户。了解更多关于多个受保护分支的信息，请参阅[分支保护文档](/zh/foundry/pipeline-builder/branches-protected-branches/)。

### 提案模板

在此选项卡中添加或查看提案模板。在可用的文本框中用Markdown撰写新提案，或在**预览**选项卡中预览您的文本。如果添加了模板，它将包含在流水线中所有新提案的正文中。
