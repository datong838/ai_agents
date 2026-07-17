---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/management-checkpoints/",
  "title": "检查点",
  "page_id": "management-checkpoints",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/management-color-groups/",
  "next": "/zh/foundry/pipeline-builder/management-job-groups/",
  "scraped_at": "2026-07-13T05:50:32.293030+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 检查点

在搭建管道时，您通常会在多个输出之间使用共享变换节点。这一逻辑通常会为每个输出重新计算一次。通过 Pipeline Builder 中的检查点，您可以将变换节点标记为“检查点”，以在下次搭建时保存中间结果。该检查点节点上游的逻辑将仅为其所有共享输出计算一次，从而节省计算资源并减少搭建时间。

:::callout{theme="warning"}
检查点仅在批处理管道中可用。输出必须在同一个任务组中，检查点节点才能提高管道效率。了解更多关于 [Pipeline Builder 中的任务组](/zh/foundry/pipeline-builder/management-job-groups/)。
:::

## 添加检查点节点

以下是一个生成两个输出的示例管道：`Attachment` 和 `Request`。变换节点 `Checkpoint` 在两个输出之间共享。在这种情况下，逻辑节点 `Clean` 和 `Checkpoint` 将被计算两次，每个输出计算一次。

![Pipeline Builder 图中一个检查点节点](../../../images/foundry/pipeline-builder/checkpoint.png)

然而，我们希望仅为两个输出计算一次 `Clean` 和 `Checkpoint`。为此，右键单击 `Checkpoint` 并选择**标记为检查点**。

![在节点菜单底部选择标记为检查点。](../../../images/foundry/pipeline-builder/mark-as-checkpoint.png)

此时，`Checkpoint` 节点的顶部角落将出现一个浅蓝色徽章。

![检查点节点现在在图中标记为检查点。](../../../images/foundry/pipeline-builder/checkpoint-badge.png)

现在，将两个输出添加到同一个任务组以验证检查点行为。右键单击其中一个输出（`Request`）以**指派任务组**。选择**新建组**以打开**搭建设置**面板。

![使用节点菜单将输出节点指派到任务组。](../../../images/foundry/pipeline-builder/assign-checkpoint-group.png)

由于数据集默认情况下位于不同的任务组中，检查点将为每个输出重新计算，从而抵消任何好处。为了解决这个问题，通过选择输出 `Attachment`，然后在面板底部选择**添加到组...** 将另一个输出添加到同一个任务组。

![在搭建设置面板中将另一个输出节点添加到同一个任务组。](../../../images/foundry/pipeline-builder/add-output-to-checkpoint-group.png)

了解更多关于在 Pipeline Builder 中配置节点的信息，包括 [颜色组](/zh/foundry/pipeline-builder/management-color-groups/) 和 [任务组](/zh/foundry/pipeline-builder/management-job-groups/)。

## 检查点存储成本

检查点将变换的整个结果推送到存储，例如 Hadoop 分布式文件系统（HDFS）。例如，如果您对一个合并操作进行检查点，则合并的整个结果将输出到存储。这可能导致存储大量数据，即使数据集输出很小。
