---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/hyperauto/getting-started/",
  "title": "HyperAuto V2 入门指南",
  "page_id": "getting-started",
  "category_id": "data-integration",
  "section_id": "hyperauto",
  "previous": "/zh/foundry/hyperauto/supported-sources/",
  "next": "/zh/foundry/hyperauto/proposals/",
  "scraped_at": "2026-07-13T05:33:38.667658+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# HyperAuto V2 入门指南

:::callout{theme="neutral"}
本指南适用于 HyperAuto V2。要开始使用 HyperAuto V1，请参阅 [HyperAuto V1 文档](/zh/foundry/hyperauto/v1-getting-started/)。
:::

:::callout{theme="neutral"}
如果您没有直接连接到系统并且正在处理静态数据，可以创建一个[基于文件夹的管道](/zh/foundry/hyperauto/folder-based-sap/)。
:::

按照以下步骤创建您的第一个 HyperAuto 管道：

1. 导航到您希望从中同步数据的[支持源](/zh/foundry/hyperauto/supported-sources/)。您可以在 Foundry 实例的[数据连接](/zh/foundry/data-connection/overview/)应用中找到所有源的列表。

    <img src="../../foundry-docs/hyperauto/media/data-connection-sap-sources.png" alt="源列表" width="750">

2. 在源的特定概览选项卡中，选择**创建 HyperAuto 管道**以打开 HyperAuto 管道向导。

    <img src="../../foundry-docs/hyperauto/media/source-overview-pipelines-card.png" alt="源概览页面上的创建 HyperAuto 管道按钮" width="750">

3. 定义新的 HyperAuto 管道资源的名称和位置以及任何相应的生成资源。请注意，HyperAuto 管道必须与输入数据集位于同一项目中。

    <img src="../../foundry-docs/hyperauto/media/hyperauto-v2-wizard-1-name-and-location.png" alt="名称和位置选项卡" width="750">

4. 如果适用，请选择源子系统（例如，SAP 源的"上下文"），以及摄取方法（批处理或流式处理，详细信息请参见[架构](/zh/foundry/hyperauto/architecture/)）。

    <img src="../../foundry-docs/hyperauto/media/hyperauto-v2-wizard-2-source-config.png" alt="向导中的源配置屏幕" width="750">

5. 在**输入配置**步骤中，选择您希望处理数据的源表。您可以按类别（"模块"）或按工作流单独选择表。您还可以选择没有数据连接同步的表作为输入。如果选定的输入已有同步，HyperAuto 将默认使用最近的一个。要重新配置选定的输入，将鼠标悬停在**配置输入**表按钮上。在此菜单中，您可以选择替代的现有同步或创建新的同步。

    <img src="../../foundry-docs/hyperauto/media/hyperauto-v2-wizard-3-add-add-to-cart.png" alt="输入配置" width="750">

6. 决定所需的管道配置，包括语言和变换选项。详细信息请参见[配置选项](/zh/foundry/hyperauto/configuration-options/)。

    <img src="../../foundry-docs/hyperauto/media/hyperauto-v2-wizard-4-pipeline-config.png" alt="管道配置" width="750">

7. 选择**创建 HyperAuto 管道**。您的新 HyperAuto 管道将被创建并开始处理数据。您将被重定向到管道的概览页面，在那里您可以监控生成进度。

    <img src="../../foundry-docs/hyperauto/media/hyperauto-v2-overview-creating-resources.png" alt="生成中" width="750">

8. 一旦生成成功，您可以使用概览页面管理和监控管道及其相关资源，包括输入同步和数据集，以及输出数据集和Object。

   * 选择**查看生成器管道**以打开只读生成器管道，并更详细地查看变换逻辑。

    <img src="../../foundry-docs/hyperauto/media/hyperauto-v2-builder-pipeline.png" alt="HyperAuto 生成的生成器管道" width="750">

   * **配置**选项卡显示 HyperAuto 管道的输入和管道配置。在此选项卡中选择**编辑**以创建新的[提案](/zh/foundry/hyperauto/proposals/)并更新配置。

       <img src="../../foundry-docs/hyperauto/media/hyperauto-v2-overview-pipeline-config.png" alt="HyperAuto 管道" width="750">
