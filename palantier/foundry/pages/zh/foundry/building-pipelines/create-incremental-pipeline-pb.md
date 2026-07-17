---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/create-incremental-pipeline-pb/",
  "title": "使用Pipeline Builder创建增量管道",
  "page_id": "create-incremental-pipeline-pb",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/create-batch-pipeline-cr-media-sets/",
  "next": "/zh/foundry/building-pipelines/create-stream-pipeline-pb/",
  "scraped_at": "2026-07-13T05:40:36.811576+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用Pipeline Builder创建增量管道

在本教程中，我们将使用Pipeline Builder创建一个简单的增量管道，其输出为单个数据集。

以下使用的数据集是为了说明增量计算的适用性而假设的示例。

## 第1部分：问题陈述

假设我们有一个每周追加新数据的`flights`输入数据集。我们想筛选出仅从`JFK`机场起飞的航班，然后将这些航班追加到输出`filtered_flights`中。

假设`flights`数据集有2000万行，但每周只增加100万行。通过增量计算，管道只需考虑`flights`中最新的未处理事务，而不是像快照计算那样考虑所有行。

:::callout{theme="success"}
如果管道定期运行，增量处理可以显著减少每次运行的数据规模，从而节省时间和资源。
:::

现在，让我们逐步了解如何设置增量管道。

## 第2部分：验证增量要求

:::callout{theme="warning"}
只有在本节中的所有考虑事项都满足的情况下，管道才会以增量计算运行。例如，您的输入必须通过不修改现有文件的`APPEND`或`UPDATE`事务进行更新。否则，将输入标记为增量将无效。
:::

首先，检查所有增量约束是否满足：

* 输入`flights`通过`APPEND`事务或不修改现有文件的`UPDATE`事务进行更新。
* 从`flights`计算`filtered_flights`的逻辑不需要在后续搭建中更改任何先前写入的`filtered_flights`数据。
  * 如果您希望更改管道逻辑（例如，还包括从`LGA`机场起飞的航班），可以更新管道。如果您想将该逻辑应用于先前处理的航班，您可能需要[重放](#replay-on-deploy)您的管道。
* 如果管道包含窗口函数、聚合或透视表，请确保这些仅对当前事务进行操作。

有关完整的考虑事项列表，请参考Pipeline Builder中增量计算的重要[限制](/zh/foundry/pipeline-builder/datasets-computation-modes-for-batch/#incremental-computation-restrictions)。

## 第3部分：创建您的管道

现在，我们可以初始化一个新的管道（有关逐步演练，请参考[在Pipeline Builder中创建批量管道](/zh/foundry/building-pipelines/create-batch-pipeline-pb/)）。假设我们已将`flights`导入为输入数据集。

首先，使用数据集下方的按钮将您的输入数据集标记为**增量**。您会看到右上角出现一个蓝色徽章，以指示更改。

![增量输入示例](../../../images/foundry/building-pipelines/incremental-input.png)

接下来，添加一个变换以筛选出从`JFK`机场起飞的`flights`。注意在数据集输入右侧标有**增量输入**工具提示的图标。下游变换将有此图标以指示它们正在被增量处理。

![增量变换路径示例](../../../images/foundry/building-pipelines/incremental-transform-path.png)

在图表上，下游节点将标有与输入相同的蓝色徽章。

![增量变换在图表上的示例](../../../images/foundry/building-pipelines/incremental-transform-graph.png)

最后，添加输出数据集`filtered_flights`。

![增量输出示例](../../../images/foundry/building-pipelines/incremental-output.png)

## 第4部分：部署输出数据集

您现在可以[部署您的管道](/zh/foundry/pipeline-builder/outputs-deliver-pipeline/#deploy)。

![增量部署示例](../../../images/foundry/building-pipelines/incremental-deploy.png)

### 部署时重放

有时，可能需要重新处理先前的输入事务（例如，如果逻辑更改且输出数据的先前版本现在已过时）。在这些情况下，您可以选择**部署时重放**以通过管道逻辑运行整个输入。重放后，随着新的追加事务被添加到输入中，您的管道应继续进行增量计算。

:::callout{theme="warning"}
部署时重放将在输出数据集上产生一个`SNAPSHOT`事务。
:::

![部署时重放的增量示例](../../../images/foundry/building-pipelines/incremental-replay-on-deploy.png)
