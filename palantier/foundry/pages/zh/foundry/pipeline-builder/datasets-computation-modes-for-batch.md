---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/datasets-computation-modes-for-batch/",
  "title": "批量输入数据集的计算模式",
  "page_id": "datasets-computation-modes-for-batch",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/datasets-generated/",
  "next": "/zh/foundry/pipeline-builder/transforms-overview/",
  "scraped_at": "2026-07-13T05:45:42.999618+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 批量输入数据集的计算模式

您可以选择以快照或增量方式读取输入数据集，具体取决于您的应用案例。

## 快照计算

快照计算对整个输入执行变换，而不仅仅是新添加的数据。输出数据集在每次搭建时由最新的管道输出完全替换。

![快照计算示例](../../../images/foundry/pipeline-builder/datasets-snapshot-computation.png)

最佳使用场景：

* 输入数据集不通过`APPEND`事务更新。
  * 当输入使用`SNAPSHOT`事务写入时，无法增量读取输入。
* 输出数据集无法通过`APPEND`事务更新。
  * 示例：每次运行时整个输出数据集都需要更改，要求快照输出。
* 输入数据集较小。
  * 在这种情况下，快照计算与增量计算一样高效。

## 增量计算

增量计算仅对自上次搭建以来追加到选定输入的新数据执行变换。这可以减少计算资源的使用，但有重要的[限制](#incremental-computation-restrictions)。

:::callout{theme="warning"}
只有在选定输入数据集通过不修改现有文件的`APPEND`或`UPDATE`事务更改时，管道才会以增量计算运行。将快照输入标记为增量将无效。
:::

![增量计算示例](../../../images/foundry/pipeline-builder/datasets-incremental-computation.png)

最佳使用场景：

* 输入数据集通过`APPEND`事务或附加的`UPDATE`事务更改。
  * 这表明随着新数据的添加，先前的输出保持不变。增量计算减少了每次搭建时处理的数据量。
* 您不需要引用先前的输出。
  * Pipeline Builder当前不允许[读取模式：previous](/zh/foundry/transforms-python/incremental-reference/#incrementaltransforminput)。然而，一些输出写入模式支持此读取模式的常见应用案例。[了解有关Pipeline Builder中输出写入模式的更多信息。](/zh/foundry/pipeline-builder/outputs-add-dataset-output/#configure-write-mode)
* 输入数据集很大且经常添加新数据。
  * 增量搭建可以节省计算资源和时间，并带来性能优势。

### 增量计算限制

:::callout{theme="warning"}
本节概述了可能适用于您的工作流程的限制。在设置增量计算之前，请仔细检查以确保正确实施。
:::

* **合并**：对于涉及增量数据集的合并，增量数据集必须在合并的左侧，快照数据集在右侧。目前不支持两个增量数据集之间的合并。
  * **合并中的快照输入**：如果快照输入接收到新事务，任何涉及增量数据集的下游合并将继续以增量方式运行。Pipeline Builder不支持在合并右侧使用快照输入的更改来强制重放管道。
* **合并**：合并的所有输入必须使用相同的计算模式（要么全部快照，要么全部增量）。
* **变换**：可能更改先前输出的变换仅限于当前事务。窗口函数、聚合和透视仅适用于当前事务数据，而不是先前的输出。
* **重放**：如果您的管道逻辑已更改，并且您希望将新逻辑应用于先前处理的输入事务，您可以选择在部署时重放。仅支持对整个输入的重放。

有关更多信息，请参见[Pipeline Builder中的增量计算示例](/zh/foundry/building-pipelines/create-incremental-pipeline-pb/)。
