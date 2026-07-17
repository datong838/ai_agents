---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/branches-approve-a-change/",
  "title": "批准更改",
  "page_id": "branches-approve-a-change",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/branches-propose-a-change/",
  "next": "/zh/foundry/pipeline-builder/branches-protected-branches/",
  "scraped_at": "2026-07-13T05:52:12.250414+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 批准更改

具有工作流项目`编辑`访问权限的Pipeline Builder用户可以批准对**Main**管道分支的更改提案。要批准提案，首先打开Builder的**提案**视图，并从`开放`提案列表中选择它。在这里，您可以查看详细信息，包括合并行为（例如，从`test/branch`到`Main`），更改描述以及提案中发现的任何出错。

![批准更改分支](../../../images/foundry/pipeline-builder/branch-approve-a-change@2x.png)

## 查看更改

切换到**更改**选项卡以比较提议的更改和**Main**分支的工作流。在左侧面板中，您可以在不同类型的更改之间筛选。在下面的示例中，提议的更改包括对`变换`的四次编辑和对`输出`的三次编辑。

每个提议的编辑都被标记为提案类型：`ADD`、`MOD`或`DEL`。

* `ADD`：该编辑是工作流中的新增加。
* `MOD`：该编辑是对现有工作流节点的修改。
* `DEL`：该编辑从工作流中移除一个节点。

点击单个编辑以查看**Main**分支和提案分支之间的差异。在下面的示例中，提议的`合并人员数据`修改将`CITY`列添加到现有合并中。

![分支更改输出的截图](../../../images/foundry/pipeline-builder/branch-change-target@2x.png)

切换回**概览**选项卡以继续审核提案。

## 解决出错

在某些情况下，提案会显示必须在合并前解决的模式或编辑出错。

![分支更改输出的截图](../../../images/foundry/pipeline-builder/branches-fail-to-compute@2x.png)

要解决阻止成功搭建和合并的模式出错，请选择**修复模式**。

这将带您回到模式出错所在的图表。

![分支合并出错的截图](../../../images/foundry/pipeline-builder/branches-join-error@2x.png)

双击图中有出错的步骤并解决有问题的条件。

![分支出错解决的截图](../../../images/foundry/pipeline-builder/branches-resolve-error@2x.png)

点击**提议**以自动保存并提议解决的分支。

## 解决合并冲突

在某些情况下，提案会显示必须在合并前解决的合并冲突。合并冲突是自您从它创建分支以来对基础分支所做的更改。必须解决合并冲突以确保正确的更改合并到管道的基础分支中。要解决这些冲突，您需要重新基准化您的分支。在Pipeline Builder中重新基准化允许您将本地分支中的未发布更改与远程分支上的最新发布更改合并。

要通过重新基准化开始解决冲突，请在提案中选择**解决**。

![解决合并冲突提案窗格](../../../images/foundry/pipeline-builder/branch-proposal-conflict.png)

这将带您到**重新基准化分支**视图中的图表。在这里，您可以从顶部栏或左侧边栏查看并解决冲突列表，并调查个别冲突和更改。

在重新基准化分支中，您可以在图表上查看冲突和更改。通过悬停在受影响节点右上角的符号上，找到更多详细信息，包括解释和可能的解决方案。在下面的示例中，您可以通过双击符号来解决合并冲突。

![重新基准化分支以解决合并冲突](../../../images/foundry/pipeline-builder/branch-rebase.png)

一旦解决了所有冲突，您可以通过点击图表右上角的**提交**来提交更改到您的分支和提案。
