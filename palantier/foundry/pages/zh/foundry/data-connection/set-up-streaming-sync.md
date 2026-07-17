---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/set-up-streaming-sync/",
  "title": "设置流式同步",
  "page_id": "set-up-streaming-sync",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/set-up-sync/",
  "next": "/zh/foundry/data-connection/file-based-syncs/",
  "scraped_at": "2026-07-13T05:32:47.689346+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 设置流式同步

**同步** 是从源读取特定数据并将其摄入Foundry的任务。例如，如果您有一个包含多个表的关系数据库源，您可以配置同步以将特定表摄入Foundry。

流式同步类似于非流式（即批处理或增量）[同步](/zh/foundry/data-connection/set-up-sync/)，但存在一些差异。主要区别在于批处理或增量同步会定期运行，而流式同步会持续运行，以尽可能低的延迟将数据拉入Foundry。

下面，我们将讨论创建同步所需的步骤：

1. [定义要同步的数据](#part-1-define-data)。
2. [在Foundry中定义一个位置](#part-2-define-the-sync-location)以发送数据。
3. [配置](#part-3-configure-the-streaming-sync)流式同步。
4. [运行](#part-4-run-the-sync)流式同步。

在本教程中，我们将使用一个[Kafka](/zh/foundry/available-connectors/kafka/)源来设置同步。

## 第1部分：定义数据

首先，决定您想同步到Foundry的数据。在Data Connection中选择您的[流式源](/zh/foundry/data-integration/streaming-guide/)，然后选择右上角的可用操作：

* **浏览和创建同步：** 如果您的源类型支持[源浏览](/zh/foundry/data-connection/source-exploration/)，此选项将出现，允许您在创建同步时浏览数据源。
* **创建同步：** 如果您的源类型不支持源浏览，则会出现此选项。

<img alt="浏览Kafka源" src="../../foundry-docs/data-connection/media/stream-explore-create-sync@2x.png">

### 浏览和创建同步

如果您的源类型支持源浏览，您将进入Data Connection中的**浏览源**页面，该页面显示可同步的数据。浏览视图界面取决于您使用的源类型。例如，Kafka源浏览允许您查看Kafka代理上的[主题 ↗](https://kafka.apache.org/intro#intro_concepts_and_terms)并预览这些主题中包含的数据。

在Kafka浏览视图中，您可以在页面左侧的列表中查看现有主题。

<img alt="浏览Kafka源" src="../../foundry-docs/data-connection/media/stream-kafka-explore-source@2x.png">

选择一个主题将让您预览该主题的数据样本。

<img alt="预览Kafka主题" src="../../foundry-docs/data-connection/media/stream-kafka-preview-topic@2x.png">

## 第2部分：定义同步位置

接下来，您需要决定将同步的数据集保存到Foundry中的位置。数据集的位置将决定谁有权限访问生成的数据集，这基于[项目级别](/zh/foundry/projects/overview/)权限。

我们建议将同步的数据集保存到其源所在的项目旁边，使它们具有相同的权限；匹配的数据集和源权限在创建数据管道时非常有用。[了解更多关于数据管道推荐的项目结构。](/zh/foundry/building-pipelines/recommended-project-structure/)

选择同步位置后，点击右上角的**创建流式同步**。

## 第3部分：配置流式同步

现在，您将进入Data Connection中的**同步创建**页面，您可以在此为您的同步定义源特定和核心流式配置。

* **源特定：** 位于配置页面顶部，这些选项取决于您的源类型，并配置传递给您正在连接的特定源的参数。
* **核心流式：** 位于源特定配置下方，这些选项对所有流式同步通用。核心配置包括吞吐量、模式和同步目标。

<img alt="配置Kafka同步" src="../../foundry-docs/data-connection/media/stream-kafka-configure-sync@2x.png">

接下来，选择您流的[吞吐量](/zh/foundry/data-integration/streams/#partitions)。吞吐量决定将创建的分区数量。选择较多的分区数量可以实现更高的吞吐量。选择**正常**吞吐量将允许该流达到5 MB/s。

然后指定输入数据的模式，默认情况下从源推断，但如有必要可以覆盖。

<img alt="设置流模式" src="../../foundry-docs/data-connection/media/stream-kafka-set-schema@2x.png">

配置同步后，选择右上角的**创建同步**。

现在您的同步已创建，您将进入**概览**选项卡。

## 第4部分：运行同步

现在，您可以运行同步。选择**概览**选项卡以查看新同步的摘要，包括输出数据集、位置和可用操作。

点击**开始**以开始将外部流的数据同步到Foundry。

<img alt="Kafka同步概览" src="../../foundry-docs/data-connection/media/stream-kafka-sync-overview@2x.png">

要查看流数据，请导航到您在创建同步时配置的流以查看流预览页面。您应该可以看到记录从Kafka主题流入流中。

<img alt="查看流输出" src="../../foundry-docs/data-connection/media/stream-sync-output@2x.png">

## 后续步骤

现在您已成功运行同步，学习如何[调试失败的流](/zh/foundry/optimizing-pipelines/debug-stream/)，通过基于推送的摄取[将数据推入流](/zh/foundry/data-connection/push-based-ingestion/)，或将您的流[集成到Ontology](/zh/foundry/object-indexing/funnel-streaming-pipelines/)。
