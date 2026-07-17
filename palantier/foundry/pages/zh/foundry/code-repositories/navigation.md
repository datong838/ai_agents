---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/code-repositories/navigation/",
  "title": "导航",
  "page_id": "navigation",
  "category_id": "data-integration",
  "section_id": "code-repositories",
  "previous": "/zh/foundry/code-repositories/overview/",
  "next": "/zh/foundry/code-repositories/configure-repositories-in-control-panel/",
  "scraped_at": "2026-07-13T06:09:25.044135+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 导航

在代码库界面的顶部，你可以选择五个不同的选项卡：

1. [代码选项卡](#code-tab)
2. [分支选项卡](#branches-tab)
3. [拉取请求选项卡](#pull-requests-tab)
4. [检查选项卡](#checks-tab)
5. [设置选项卡](#settings-tab)

## 代码选项卡

![代码视图](../../../images/foundry/code-repositories/code-view.png)

1. [应用内帮助](#in-app-help)
2. [分支选项](#branch-options)
3. [代码编辑器选项](#code-editor-options)
4. [文件编辑器](#file-editor)
5. [辅助面板](#helper-panels)
6. [状态栏](#status-bar)

### 应用内帮助

在**代码**选项卡中，你可以点击 <img src="../../foundry-docs/code-repositories/media/help.png" alt="help" height="25" width="25"> 按钮，启动逐步指南，引导你了解代码库中可用的核心功能。应用内帮助目前仅在**代码**视图中可用。

通过命令面板使用键盘快捷键，在Windows上使用F1键或在macOS上使用Fn+F1：

<img src="../../foundry-docs/code-repositories/media/command.png" alt="command">

### 分支选项

使用下拉分支菜单选择一个现有的沙盒分支进行工作。或者，点击 <img src="../../foundry-docs/code-repositories/media/new-branch.png" alt ="new-branch" height="35" width="35"> 图标创建一个新的沙盒分支，该分支包含现有分支代码的副本。要在你的库中编辑代码，你必须在沙盒分支中工作——受保护的分支无法直接编辑。

### 代码编辑器选项

在你的库中编写和编辑代码时，你可以执行以下操作：

* 点击 <img src="../../foundry-docs/code-repositories/media/preview.png" alt ="preview" width="106"> 按钮，在输入数据集的样本上运行变换。这是预览你在真实数据上代码更改的快速方法。
* 点击 <img src="../../foundry-docs/code-repositories/media/test.png" alt ="test" width="80"> 按钮，运行当前文件中定义的所有单元测试。有关如何向库中添加单元测试的信息，请参见[Python测试](/zh/foundry/transforms-python/unit-tests/)或[Java测试](/zh/foundry/transforms-java/unit-tests/)。
* 点击 <img src="../../foundry-docs/code-repositories/media/commit.png" alt ="commit" width="103"> 按钮，提交沙盒分支中的任何更改。一旦提交更改，自动检查将运行在你的代码上。
* 如果你选择了一个数据集源文件（定义变换的文件，例如参见[Python变换装饰器](/zh/foundry/transforms-python/transforms-pipelines/#decorator)），可以点击 <img src="../../foundry-docs/code-repositories/media/build-button.png" alt ="build" width="86"> 按钮，在你的代码上运行自动检查后构建输出数据集的新版本。点击此按钮将触发*当前文件的所有输出数据集*的构建；如果当前文件不生成任何数据集，则不会触发构建。
* 点击 <img src="../../foundry-docs/code-repositories/media/propose-changes.png" alt ="propose-changes" width=166> 按钮，创建包含更改的新*拉取请求*。这允许其他人在将代码合并到主代码之前审阅和评论你的代码。
* 点击 **...** 按钮访问几个附加操作：
  * **合并：** 将另一个分支合并到当前分支。
  * **重置：** 将所有文件的内容重置为匹配远程分支上的最新提交。这将清除分支上尚未提交的任何更改。
  * **升级：** 将分支升级到最新的语言版本。

### 文件编辑器

点击 <img src="../../foundry-docs/code-repositories/media/new-file-button.png" alt ="new-file-button" height="28" width="28"> 图标，创建新文件、文件夹或子项目。如果你想向代码库中添加另一个特定语言的子项目，请选择“新子项目”选项。

### 辅助面板

**Foundry Explorer 辅助**

**Foundry Explorer** 辅助是一个文件导航界面，让你快速浏览所有文件和文件夹。一旦选择了特定的数据集，可以点击“打开”查看完整数据集。

**问题辅助**

**问题**辅助会告诉你代码中检测到的任何问题。点击这里列出的特定问题可以打开有问题的代码。

**调试器辅助**

**调试器**允许你在变换运行时检查其行为（参见[调试变换](/zh/foundry/code-repositories/debug-transforms/)）。

**预览辅助**

**预览**辅助允许你在输入数据集的有限样本上运行代码，以快速预览代码而不提交更改（参见[预览变换](/zh/foundry/code-repositories/preview-transforms/)）。

**测试辅助**

当你的库包含单元测试时（参见[Python测试](/zh/foundry/transforms-python/unit-tests/)和[Java测试](/zh/foundry/transforms-java/unit-tests/)），**测试辅助**可以让你运行这些测试并显示其结果。

**文件更改辅助**

**文件更改**辅助可以用于查看当前文件的任何未提交更改，以及比较文件的以前版本。

**构建辅助**

**构建**辅助可以让你触发数据集构建并查看构建的进度。一旦选择了数据集源文件，可以点击构建按钮来构建输出数据集的新版本，并在代码上运行自动检查。然后可以在**构建**辅助中查看正在运行任务的进度。

:::callout{theme="neutral"}
点击代码库界面右上角的**构建**按钮相当于从**构建**辅助中触发构建。
:::

**文档辅助**

**文档**辅助包含可以用来编写代码的可用语言的参考资料。有关不在产品文档中提供的更详细的特定语言文档，请参见[支持的语言](/zh/foundry/building-pipelines/supported-languages/)。

**SQL草稿**

**SQL**辅助允许你快速测试SQL查询。编写SQL查询并点击 <img src="../../foundry-docs/code-repositories/media/sql-run-file.png" alt ="sql-run-file" width="60"> 预览查询结果。你也可以通过选择适当的`.sql`文件并点击 <img src="../../foundry-docs/code-repositories/media/sql-preview-file.png" alt ="sql-preview-file" width="110"> 测试你在库中编写的现有查询。

要查看标记为收藏的查询，请转到 <img src="../../foundry-docs/code-repositories/media/sql-tab2.png" alt ="sql-tab2" width="25"> 选项卡。要查看**SQL**辅助中运行的查询历史，请转到 <img src="../../foundry-docs/code-repositories/media/sql-tab3.png" alt ="sql-tab3" width="25"> 选项卡。

:::callout{theme="neutral"}
要在SQL草稿中访问输入数据集的特定分支，请在查询中添加分支名称：例如 `` SELECT * FROM `branch_A`.`/path/to/dataset` ``。如果未指定分支，将默认为`master`。
:::

### 状态栏

状态栏提供有关环境状态和检查结果的信息。你可以在状态栏中找到以下信息：

* **代码助手状态** - 代码助手对于检测代码中的问题和运行预览至关重要。你可以在没有代码助手的情况下编写代码，但需要它启动并运行才能完成工作。将鼠标悬停在代码助手状态上可以获取初始化进度的详细信息。如果代码助手初始化失败，请提升客服支持请求。
* **问题** - 当在代码中检测到问题时，状态栏左侧会出现指示。点击指示打开问题辅助。
* **检查状态** - 检查状态显示在状态栏的右侧。有关检查的更多详细信息，请参见[检查选项卡](#checks-tab)。
* **文件保存** - 在任何更改之后，文件保存状态显示自动保存进度。

## 分支选项卡

:::callout{theme="neutral"}
本节总结了如何在**分支**选项卡中创建新分支和创建新的拉取请求。这些功能也可以在[代码选项卡](#code-tab)中使用。
:::

在**分支**选项卡中，你可以看到代码库中存在的分支列表——这包括你自己的分支以及其他用户的分支。点击 <img src="../../foundry-docs/code-repositories/media/new-branch2.png" alt ="new-branch2" width="100"> 按钮，创建一个新的沙盒分支，该分支包含特定分支代码的副本。

![分支视图](../../../images/foundry/code-repositories/branch-view.png)

每个列出的分支都包含一个摘要，其中包括以下可用功能：

* “检查”列指示分支的自动代码检查是否通过。
* “拉取请求”列告诉你分支中是否存在任何现有的*拉取请求*，并允许你创建新的*拉取请求*。
  要创建一个包含分支更改的新*拉取请求*，请点击“提议更改”按钮。这将默认创建一个新的*拉取请求*，将你的更改合并到*master*分支中。如果你想将更改合并到*master*以外的分支，请从下拉菜单中选择不同的分支。
  如果你没有看到创建新*拉取请求*的按钮，则意味着分支中已存在一个*拉取请求*。点击“打开”/“关闭”/“合并”按钮打开完整的*拉取请求*。
* 点击分支名称旁边的“查看代码”以查看该分支上的代码。
* 要删除分支，请点击 <img src="../../foundry-docs/code-repositories/media/trash.png" alt ="trash" width="25"> 图标。**你不应该删除任何你未创建的分支。这可能导致他人工作丢失。**

### 标签

分支选项卡还允许你访问**标签**列表，标签类似于不可变的分支。标签可用于通过赋予版本号或名称标记代码的一个重要版本，以供将来参考。要创建新标签，请导航到分支选项卡的标签部分并点击“新建标签”按钮。标签可以从当前分支版本或任何任意提交中创建。

![创建标签对话框](../../../images/foundry/code-repositories/create-tag-dialog.png)

:::callout{theme="neutral"}
为了确保所有标签名称遵循特定的命名约定，你可以在库根目录下的`repoSettings.json`文件中添加一个`tagNameValidation`配置块，例如："tagNameValidation": { "regex": "^(0|\[1-9]\\\d\*)\\\\.(0|\[1-9]\\\d\*)\\\\.(0|\[1-9]\\\d\*)(-rc\\\d+)?$", "errorMessage": "标签名称必须具有格式x.x.x或x.x.x-rcx。" }
:::

有关推荐的git开发工作流程的更多信息，请参见[开发者最佳实践](/zh/foundry/building-pipelines/development-best-practices/)。

## 拉取请求选项卡

:::callout{theme="neutral"}
本节总结了如何在**拉取请求**选项卡中创建新的拉取请求。此功能也可以在[代码选项卡](#code-tab)中使用。
:::

在**拉取请求**选项卡中，你可以找到代码库中*拉取请求*的信息。*拉取请求*允许用户在合并更改之前查看分支更改的历史记录并逐行审查你的代码。每当你想将分支上的更改合并到主代码中时，你应该创建一个新的*拉取请求*。

点击 <img src="../../foundry-docs/code-repositories/media/new-pull-request.png" alt ="new-pull-request" width="100"> 按钮，创建一个新的*拉取请求*。默认情况下，创建的新*拉取请求*将你的更改合并到库的主分支中（通常是*master*分支）。选择你想基于哪个分支创建新的*拉取请求*。

### 筛选拉取请求

通过点击拉取请求列表顶部的“打开”/“关闭”按钮，可以在打开和关闭的*拉取请求*列表之间切换，并使用搜索栏根据标题或作者进一步筛选列表。

![拉取请求列表](../../../images/foundry/code-repositories/pull-requests-list.png)

### 审查拉取请求

点击其中一个*拉取请求*，逐行审查提议的代码更改并添加评论。根据库设置，每个*拉取请求*可能需要至少一个批准的审查才能合并。

在审查变换代码的更改时，你还可以检查[这些更改对你的数据集的影响](/zh/foundry/code-repositories/analyze-impact/)。

## 检查选项卡

在**检查**选项卡中，你可以查看每个分支正在运行和已完成检查的摘要。使用下拉分支菜单选择不同的分支。点击特定检查以查看更详细的信息。

![检查视图](../../../images/foundry/code-repositories/checks-view.png)

检查选项卡还将包括为你的库定义的任何单元测试的输出。你可以为[Python](/zh/foundry/transforms-python/unit-tests/)和[Java](/zh/foundry/transforms-java/unit-tests/)定义单元测试。

:::callout{theme="neutral"}
如果你的堆栈上启用了AIP，[错误增强微件](/zh/foundry/code-repositories/aip-features/#error-enhancer)将补充失败检查的详细视图，帮助你更好地理解和解决出现的问题。
:::

![动画截图显示在代码库中错误增强的实际操作](../../../images/foundry/code-repositories/error-enhancer-in-authoring.gif)

## 设置选项卡

在设置选项卡中，代码作者可以配置个人编辑器偏好，库管理员可以控制库的行为和策略。要了解有关设置选项卡的更多信息，请参阅[管理代码库](/zh/foundry/code-repositories/admin-overview/)。

:::callout{theme="neutral"}
**设置**选项卡中的大多数选项是针对管理员的，并且只对具有适当权限的用户可用（默认情况下，库所有者）。
:::
