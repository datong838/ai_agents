---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/time-series-syncs/",
  "title": "时间序列同步",
  "page_id": "time-series-syncs",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/time-series-properties/",
  "next": "/zh/foundry/time-series/create-sensor-ot/",
  "scraped_at": "2026-07-13T06:11:08.695658+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 时间序列同步

时间序列同步保存与任何数量的时间序列（由`seriesIds`作为键）相关的时间-值对，从而在每个序列和相关的时间-值对上实现高效的索引。时间序列同步由[数据集](/zh/foundry/data-integration/datasets/)或[流](/zh/foundry/data-integration/streams/)支持，并且是时间序列属性的支持数据源。

当 Foundry 在给定对象时间序列属性上解析时间序列属性时，将在该属性的数据源中搜索属性值中包含的`seriesId`，并返回其关联的时间序列数据。

时间序列同步需要以下列：

1. **seriesId:** 序列的标识符（`字符串`）。
2. **timestamp:** 关联值发生的时间（`timestamp`或`long`）。
   * 对于 long 类型的时间列，必须指定单位。可用单位包括秒、毫秒、微秒或纳秒。
3. **value:** 在给定时间戳上的序列值（`double`、`integer`、`float`或`字符串`）。
4. **摄取时间:** （非必填）：流数据点被摄取的时间（`timestamp`）。

:::callout{theme="warning"}
如果时间序列属性由多个时间序列同步支持，则属性值中的`seriesIds`必须完全包含在单个时间序列同步中。
:::

:::callout{theme="warning"}
创建时间序列同步时构建的[投影](/zh/foundry/time-series/faqs/#what-is-the-time-series-projection)所需的变换配置文件的大小会随着输入数据集的大小而变化。对于大于10 TB的数据集，我们建议将您的数据集拆分为多个数据集，按序列标识符分区，然后从这些较小的数据集中创建同步。
:::

### 创建时间序列同步

我们建议使用 Pipeline Builder 来创建时间序列同步。查看我们的[文档](/zh/foundry/pipeline-builder/overview/)部分，以获取有关添加数据、创建变换和设置同步目标的指导。或者，您可以[手动设置它们](/zh/foundry/time-series/advanced-setup/#2-set-up-a-time-series-sync)。

1. 如果您正在使用设置助手，请选择**Go to Builder**。

![系列设置助手中的提示。](../../../images/foundry/time-series/time-series-setup-sync-go-to-builder.png)

或者，导航到 Pipeline Builder 应用程序并创建一个新管道。

2. 导入您的[时间序列数据](/zh/foundry/time-series/time-series-concepts-glossary/#time-series)并应用必要的变换以适应时间序列同步的形状。

3. 一旦您的数据被变换为正确的形状，创建一个[时间序列同步目标](/zh/foundry/pipeline-builder/outputs-overview/#time-series-syncs)。

![在 Pipeline Builder 中设置时间序列同步目标](../../../images/foundry/time-series/time-series-setup-builder-sync-target.png)

4. 接下来，配置列映射。

![在 Pipeline Builder 中的时间序列同步目标配置](../../../images/foundry/time-series/time-series-setup-builder-sync-target-configuration.png)

5. 部署管道以创建和搭建时间序列同步。这将创建支持数据集和时间序列同步。

:::callout{theme="warning"}
Pipeline Builder 目前不支持将`long`类型的列映射到时间序列同步的时间戳列。
:::

6. 返回到 Ontology Manager 应用程序，并将此时间序列同步作为数据源添加到时间序列属性中。

对您希望添加的任何其他时间序列属性重复这些步骤。如果您的同步包含所有的系列 ID，那么您可以为新的时间序列属性选择相同的同步，而不是创建新的。

确保在 Ontology Manager 中选择**保存**以保存您的更改。如果您创建了一个新的对象类型，并且这是您第一次保存更改，您需要等待初始索引完成后才能分析 TSPs。通过导航到 Ontology Manager 中对象类型的**数据源**选项卡来检查索引状态。

查看如何[使用时间序列](/zh/foundry/time-series/time-series-usage/)以了解如何分析您新配置的时间序列数据。

## 时间序列目录应用程序

时间序列目录应用程序用于高级时间序列同步配置。可以通过打开时间序列同步资源或手动导航到`https://<domain>/workspace/time-series-catalog-app`来访问该应用程序。

高级时间序列配置包括以下功能：

1. 停止从输入数据集或流继承[权限标记](/zh/foundry/security/markings/)。查看我们的[时间序列权限](/zh/foundry/time-series/time-series-permissions/)文档以获取更多详细信息。
2. 设置[Spark](/zh/foundry/code-repositories/spark-profiles/)或Flink计算配置文件。
   * 我们建议使用默认计算配置文件。如果没有添加配置文件，将使用默认计算配置文件。
3. 设置一个计划，以便在输入数据集更新时自动搭建时间序列同步。查看我们的[事件触发器](/zh/foundry/building-pipelines/triggers-reference/)和[计划](/zh/foundry/data-integration/schedules/)文档以获取更多信息。
4. 覆盖当前时间序列同步中存在的指定时间序列同步中的`seriesIds`。这是为传统时间序列设置保留的高级功能。

下面的示例显示了由数据集支持的时间序列同步：

![时间序列目录应用](/resources/foundry/time-series/time-series-setup-time-series-catalog-app.png)

:::callout{theme="warning"}
如果时间序列同步是在 Pipeline Builder 中创建的，Pipeline Builder 可以配置的所有字段将覆盖时间序列目录应用程序中的任何配置。例如，如果在时间序列目录应用程序中更改了列映射，但是时间序列同步是在 Pipeline Builder 中创建的，那么下次运行创建管道时更改将被覆盖。
:::
