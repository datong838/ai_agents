---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-integration/streaming-guide/",
  "title": "流式资源指南",
  "page_id": "streaming-guide",
  "category_id": "data-integration",
  "section_id": null,
  "previous": "/zh/foundry/sap/faq/",
  "next": "/zh/foundry/data-integration/flink-streaming/",
  "scraped_at": "2026-07-13T05:39:19.656923+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 流式资源指南

此页面列出了在实现端到端流式工作流时可能需要参考的资源。

数据连接支持将数据从多种流式平台同步到 Foundry 流式数据集，然后可以在[流式管道](/zh/foundry/building-pipelines/streaming-overview/)中使用这些数据集。流式同步使数据能够以低延迟和高吞吐量流入 Foundry，以支持实时决策过程。

有两种方式可以将数据从流中同步到 Foundry：

* 数据连接支持将记录从流式平台拉取到 Foundry。与批量同步一样，数据从流中读取并使用[代理架构](/zh/foundry/data-connection/architecture/)通过单向连接同步到 Foundry。
* 如果需要，Foundry 允许通过*流代理*将记录直接推送到 Foundry 流中。

Foundry 可以连接到许多流式数据源，包括：

* **[Apache Kafka](/zh/foundry/available-connectors/kafka/)**
* **ActiveMQ**
* **[Amazon Kinesis](/zh/foundry/available-connectors/amazon-kinesis/)**
* **Amazon SNS**
* **Amazon SQS**
* **[Google Pub/Sub](/zh/foundry/available-connectors/pubsub/)**
* **IBM MQ**
* **RabbitMQ**
* **MQTT (beta 支持)**
* **Solace**

此页面列出了在实现端到端流式工作流时可能需要参考的资源。

## 1. 核心概念

我们建议查看以下入门概念页面，以了解流是什么、如何存储以及如何处理。

* [流](/zh/foundry/data-integration/streams/)
* [Foundry 流式中的 Flink](/zh/foundry/data-integration/flink-streaming/)

## 2. 概述

这些页面将提供更广泛的视角，以便在确定流是否适合您的应用案例时考虑各种要点。

* [流式管道概述](/zh/foundry/building-pipelines/streaming-overview/)
* [比较：流式与批量](/zh/foundry/building-pipelines/stream-vs-batch/)
* [性能考量](/zh/foundry/building-pipelines/streaming-performance-considerations/)
* [流式计算使用](/zh/foundry/building-pipelines/streaming-compute-usage/)
* [流式配置文件](/zh/foundry/data-integration/streaming-profiles/)

## 3. 连接到数据源

您需要完成以下工作流之一，以将外部数据源连接到 Foundry 以进行流式传输。我们建议查看这两种选项，以了解您的应用案例可能的优势和限制。

* [设置流式同步](/zh/foundry/data-connection/set-up-streaming-sync/)
* [将数据推送到流中](/zh/foundry/data-connection/push-based-ingestion/)

## 4. 转换流式数据

您可以使用[Pipeline Builder](/zh/foundry/pipeline-builder/overview/)来变换您的实时数据。Pipeline Builder 变换的输出将仍然是流式数据集，您可以[在 Foundry 中实时使用](/zh/foundry/building-pipelines/stream-vs-batch/#front-end-tools)。

* [使用 Pipeline Builder 创建流式管道](/zh/foundry/building-pipelines/create-stream-pipeline-pb/)
* [将您的流与 Ontology 集成](/zh/foundry/object-indexing/funnel-streaming-pipelines/)

## 5. 监控流式管道 \[Beta]

设置关于管道健康状况的警报。

* [流监控](/zh/foundry/data-integration/stream-monitoring/)

## 6. 开发工具

在此，您可以找到改进流式管道开发的工具。

* [重置流](/zh/foundry/data-integration/reset-stream/)
