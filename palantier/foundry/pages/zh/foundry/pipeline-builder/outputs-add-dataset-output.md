---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/outputs-add-dataset-output/",
  "title": "添加数据集输出",
  "page_id": "outputs-add-dataset-output",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/outputs-overview/",
  "next": "/zh/foundry/pipeline-builder/outputs-add-ontology-output/",
  "scraped_at": "2026-07-13T05:48:03.569946+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 添加数据集输出

您可以选择在Pipeline Builder中添加数据集输出，以引导您的管道集成生成干净、变换后的数据。了解更多关于[不同输出类型](/zh/foundry/pipeline-builder/outputs-overview/)。

## 创建数据集输出

首先，点击图右侧输出面板中的数据集类型旁边的**添加**。

<img src="../../foundry-docs/pipeline-builder/media/outputs-output-types.png" alt="输出类型" width="800">

现在您已创建了一个新的输出数据集。在第一次搭建您的管道后，您的数据集输出将与您的管道在同一个文件夹中创建。例如，Demo Pipeline的`Vendor`数据集输出将具有以下文件路径：`/Palantir/Pipeline Builder/Demo Pipeline/Vendor`。

通过点击名称字段重命名您的输出数据集。选择**添加列**以手动向输出模式添加列，或连接一个变换节点以使用其输出模式，选择**使用更新后的模式**。

<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-dataset@2x.png" alt="配置数据集输出初始状态" width="800">

一旦您添加了一个输出模式，使用**搜索列...**字段快速查找数据集中的列。要仅查看输出模式中的出错，切换**仅显示出错**按钮。

<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-dataset-errors@2x.png" alt="配置带有出错的数据集输出" width="800">

添加输出数据集后，点击**返回所有输出**以查看管道中所有输出的列表。快速了解每个输出的状态，包括输出模式是否与输入变换节点模式匹配。以下三个输出代表输出模式可能的不同状态：

* **数据集 1** 有5/5的必需列，意味着输入变换节点中的每一列都会在输出数据集中搭建。
* **数据集 2** 有3/3的必需列，并丢弃了2列，意味着输入变换节点有5列，但仅3列会在输出数据集中搭建。当输入变换节点中有不必要的列时，这是可取的。
* **数据集 3** 有5/7的必需列，这是一个出错状态。在将2个缺少的列映射到输入变换节点中的列之前，您将无法部署管道。

随时点击**编辑**更新输出模式。

<img src="../../foundry-docs/pipeline-builder/media/outputs-datasets-list@2x.png" alt="数据集输出列表" width="800">

了解更多关于数据集模式的信息在[数据集成](/zh/foundry/data-integration/datasets/#schemas)。

## 配置输出设置

除了模式配置，每个单独的输出都有各种默认设置可供定制。

<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-dataset-settings@2x.png" alt="输出配置设置 1" width="800">
<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-dataset-settings-2@2x.png" alt="输出配置设置 2" width="800">

### 配置期望

在您的输出数据集上添加期望以确保管道稳定性。如果在管道搭建期间任何检查失败，搭建将失败。

![输出配置期望](../../../images/foundry/pipeline-builder/outputs-configure-expectations@2x.png)

### 配置写入模式

定义如何在未来部署中将数据添加到数据集输出中。

![输出配置写入模式](../../../images/foundry/pipeline-builder/outputs-configure-write-mode@2x.png)

**默认:** 推荐用于大多数批处理管道，包括[快照和增量](/zh/foundry/pipeline-builder/datasets-computation-modes-for-batch/)。如果至少一个输入被标记为增量，并且所有标记为增量的输入自上次搭建以来仅有`APPEND`或附加的`UPDATE`交易，则默认写入模式将输出结果为`APPEND`交易。否则，默认写入模式将输出结果为`SNAPSHOT`交易。了解更多关于[交易类型](/zh/foundry/data-integration/datasets/#transaction-types)。

**始终追加行:** 以`APPEND`交易输出结果。

**仅追加新行:** 以`APPEND`交易输出结果，其中仅新增的行（定义为新见的主键）被添加到输出中。如果当前交易中存在重复行，则会随机丢弃一行。主键在先前输出中存在的行将被丢弃。

**变更日志:** *仅用于Object Storage v1。* 输出一系列包含所有记录更改完整历史记录的`APPEND`交易。了解更多关于[变更日志数据集](/zh/foundry/building-pipelines/maintaining-incremental-performance/#changelog-datasets)。

**快照差异:** 以`SNAPSHOT`交易输出结果，其中仅保留新见的主键行。如果当前交易中存在重复行，将被保留。所有其他行将被丢弃。

**快照替换:** 以`SNAPSHOT`交易输出结果，其中新数据与先前输出合并。先前输出中的现有主键将被新行替代。如果当前交易中存在重复行，除一行外所有行将被随机丢弃，因此输出最终仅每个主键有一行。

**快照替换并移除:** *这相当于快照替换，随后进行后筛选阶段以选择性地移除旧数据中的行。* 以`SNAPSHOT`交易输出结果，其中新数据与先前输出合并，随后进行后筛选阶段以根据提供的布尔值`post_filtering_column`移除先前交易中的行。如果`post_filtering_column = TRUE`，则先前输出中的现有主键将被新行替代。然而，如果当前交易中存在`post_filtering_column = FALSE`的行，则旧数据中的对应行将被筛选掉（尽管这不会覆盖存储的`post_filtering_column = TRUE`的新行）。如果当前交易中存在`post_filtering_column = TRUE`的重复行，除一行外所有行将被随机丢弃，因此输出最终仅每个主键有一行。

### 数据集写入格式

数据集的输出文件格式可以在初始部署后更改，并将在下一次管道部署时生效。了解更多关于[文件格式](/zh/foundry/data-integration/datasets/#file-formats)。

<img src="../../foundry-docs/pipeline-builder/media/outputs-write-format@2x.png" alt="配置写入格式" width="600">

### 覆盖数据集

一次性操作，将现有数据集的所有权授予Pipeline Builder中的新输出。请注意，此操作可能需要在Pipeline Builder之外进行额外操作。

<img src="../../foundry-docs/pipeline-builder/media/outputs-overwrite-dataset@2x.png" alt="覆盖输出数据集" width="600">

## 搭建数据集输出

将您的数据集输出添加到管道后，请确保保存更改。如果您已完成数据变换并定义了管道工作流，您就可以部署管道并搭建数据集输出。在部署管道后，使用最终的数据集输出作为[Ontology Manager](/zh/foundry/ontology-manager/overview/)中Ontology搭建的基础。

了解如何[部署您的管道](/zh/foundry/pipeline-builder/outputs-deliver-pipeline/)。
