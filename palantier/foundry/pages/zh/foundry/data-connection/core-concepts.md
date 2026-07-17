---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/core-concepts/",
  "title": "核心概念",
  "page_id": "core-concepts",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/overview/",
  "next": "/zh/foundry/data-connection/architecture/",
  "scraped_at": "2026-07-13T05:30:17.172154+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 核心概念

本页描述了贯穿数据连接的核心概念。

## 源

一个**源**代表单个连接，包括指定目标系统所需的任何配置和成功认证所需的[凭证](#credentials)。根据Palantir平台与目标系统之间的网络，源必须配置特定的[运行时](#runtimes)。运行时还定义了与源一起使用的任何[功能](#capabilities)的运行位置。

源是基于特定**连接器**（也称为**源类型**）设置的。在Palantir平台中，[提供了广泛的连接器](/zh/foundry/data-integration/source-type-overview/)，旨在支持组织中最常见的数据系统。根据选择的连接器和运行时，可能会提供不同的[功能](#capabilities)。

对于没有专用连接器的系统，可以使用通用连接器或[REST API源](/zh/foundry/available-connectors/rest-apis/#rest-api-source)，与代码连接选项如[外部变换](/zh/foundry/data-integration/external-transforms-source-based/)、[外部函数](/zh/foundry/data-integration/external-functions/)和[计算模块](/zh/foundry/compute-modules/overview/)一起使用。

### 凭证

*凭证*是访问特定系统所需的秘密值；即凭证用于认证。凭证可以是密码、词元、API密钥或其他秘密值。在Palantir平台中，所有凭证都经过加密并安全存储。根据运行时，秘密可能会本地存储在数据连接代理上，或直接存储在平台中。

某些源能够在不存储任何秘密的情况下进行认证，例如使用[OpenID连接](/zh/foundry/data-connection/oidc/)、[出站应用程序](/zh/foundry/administration/configure-outbound-applications/)或[云身份](/zh/foundry/administration/configure-cloud-identities/)时。

## 运行时

源必须配置**运行时**。运行时定义网络配置以及[功能](#capabilities)的执行位置。

Palantir允许您使用三种不同的运行时连接到您的系统。通常情况下，如果您要连接的系统可以接受从您的Foundry实例托管的网络的入站连接，您应使用[直接连接](#direct-connection)运行时。如果这不可行，并且您使用的源类型支持[代理代理](#agent-proxy-runtime)，这是首选的基于代理的选项。如果其他运行时都不可用，您应使用[代理工作者](#agent-worker-runtime)。

:::callout{theme="neutral"}
并非所有源类型都支持所有运行时。
:::

| 运行时选项 | 网络 | 功能执行 |
| -------------- | ---------- | -------------------- |
| [直接连接](#direct-connection) \[推荐] | 目标系统必须允许来自Palantir的直接入站流量；对于标准Foundry实例，这通常意味着允许来自控制面板或数据连接应用程序中可查看的标准出口IP地址的入站流量。 | 功能在Foundry中执行。 |
| [代理代理](#agent-proxy-runtime) | 安装在您的基础设施上的代理用于反向代理无法通过直接连接访问的系统的流量。 | 功能在Foundry中执行。 |
| [代理工作者](#agent-worker-runtime) | 安装在您的基础设施上的代理用于运行与目标系统交互的任务，并单独从Foundry推送或拉取数据。 | 功能在客户提供的Linux主机上执行。 |

### 直接连接

直接连接使用户能够连接到可通过互联网访问的数据源，而无需设置代理。如果数据源可通过互联网访问，这是首选的源连接方法；它避免了设置和维护代理的操作开销，并提供高正常运行时间和性能。[了解如何设置直接连接。](/zh/foundry/data-connection/set-up-direct-connection/)

:::callout{theme="neutral"}
当使用在本地托管的Foundry实例进行直接连接时，目标系统必须能够从运行您的Foundry实例的网络访问。如果不是这种情况，您必须使用基于代理的运行时选项之一。
:::

## 代理

**代理**是Palantir提供的一种软件，运行在您的网络中的主机上。代理连接到您的源系统，并且还可以与Foundry通信。要使用**代理代理**和**代理工作者**运行时，需要一个代理。使用同一个代理作为代理代理或代理工作者是由使用代理的特定[源](#sources)决定的。

通过[本教程](/zh/foundry/data-connection/set-up-agent/)了解更多关于如何设置代理的信息。

### 代理代理运行时

代理代理运行时用于连接到无法通过互联网访问的数据源。代理充当反向网络代理，将起源于Foundry的网络流量转发到代理部署的网络中，并将流量回传到Foundry。这允许Foundry中的功能几乎与使用直接连接时完全相同，但不需要您允许来自Foundry的IP地址的入站网络流量。

为了实现高可用性，可以配置多个代理，具有不重叠的维护窗口，以确保始终有一个活动代理来代理连接到通过代理代理可访问的目标系统。[了解如何设置代理代理运行时。](/zh/foundry/data-connection/agent-proxy-runtime/)

### 代理工作者运行时

代理工作者运行时用于连接到无法通过互联网访问的数据源。只有在所需的连接器不支持*代理代理*运行时时，才应使用代理工作者。代理工作者运行时与一个或多个代理相关联，这些代理以加密格式在本地存储源配置和凭证，并在代理本身上运行源功能。[了解如何设置具有代理工作者运行时的源。](/zh/foundry/data-connection/agent-worker-runtime/)

## 功能

源可能支持多种*功能*，每个功能代表一些可以在源连接上运行的功能。支持的功能范围广泛，包括将数据引入Foundry、从Foundry推送数据、虚拟化存储在Foundry外部的数据以及向其他系统发出交互请求。

以下表中包含了可用功能的摘要。有关特定连接器支持的功能的更多信息，请参阅该连接器的文档页面。

| 功能 | 描述 |
| ---------- | ----------- |
| [**批量同步**](#batch-syncs) | 从外部源同步数据到[数据集](/zh/foundry/data-integration/datasets/)。 |
| [**流同步**](#streaming-syncs) | 从外部消息队列同步数据到[流](/zh/foundry/data-integration/streams/)。 |
| [**变更数据捕获(CDC)同步**](#change-data-capture-syncs) | 从数据库同步数据到具有[CDC元数据](/zh/foundry/data-integration/change-data-capture/#change-data-capture-in-streams)的[流](/zh/foundry/data-integration/streams/)。 |
| [**媒体同步**](#media-syncs) | 从外部源同步数据到[媒体集](/zh/foundry/data-integration/media-sets/)。 |
| [**HyperAuto**](#hyperauto) | [自动同步整个系统](/zh/foundry/hyperauto/overview/)。 |
| [**文件导出**](#file-exports) | 将数据作为文件从[数据集](/zh/foundry/data-integration/datasets/)推送到外部系统。 |
| [**表导出**](#table-exports) | 将带有架构的数据从[数据集](/zh/foundry/data-integration/datasets/)推送到外部数据库。 |
| [**流导出**](#streaming-exports) | 将数据从[流](/zh/foundry/data-integration/streams/)推送到外部消息队列。 |
| [**Webhooks**](#webhooks) | 交互式地向外部系统发出结构化请求。 |
| [**虚拟表**](#virtual-tables) | 注册来自外部数据仓库的数据以用作[虚拟表](/zh/foundry/data-integration/virtual-tables/)。 |
| [**虚拟媒体**](#virtual-media) | 将来自外部系统的非结构化媒体注册为[媒体集](/zh/foundry/data-integration/media-sets/)。 |
| [**探索**](#exploration) | 在使用其他功能之前交互式地探索外部系统的数据和架构。 |
| [**在代码中使用**](#use-in-code) | 在代码中使用源以扩展或自定义未涵盖的任何功能。 |

正在开发其他功能，并且功能覆盖范围会在特定连接器的文档中定期更新。

特定连接器支持的功能也显示在数据连接应用程序的新源页面上。可以按连接器名称和功能进行搜索。下面的示例显示了搜索支持“虚拟”选项的源的结果。

![显示连接器卡片上的可用功能的新源页面截图，带有“虚拟”搜索。](../../../images/foundry/data-connection/data-connection-new-source-page.png)

### 批量同步

**批量同步**从外部系统读取数据并将其写入Foundry的[数据集](/zh/foundry/data-integration/datasets/)。批量同步定义应该读取哪些数据以及在Foundry中输出到哪个数据集。批量同步可以配置为增量同步数据，并允许同步带有或不带有相应架构的数据。[了解如何设置同步。](/zh/foundry/data-connection/set-up-sync/)

通常，批量同步有两种主要类型：

* \*\*文件批量同步：\*\*允许将不带架构的文件直接同步到Foundry数据集。这些文件随后可以在下游变换中访问；例如，使用[基于文件的变换](/zh/foundry/transforms-python/unstructured-files/)。支持文件批量同步的最常见系统是文件系统和Blob存储，例如[S3](/zh/foundry/available-connectors/amazon-s3/)、[ABFS](/zh/foundry/available-connectors/azure-blob-filesystem/)、[Google云存储](/zh/foundry/available-connectors/google-cloud-storage/)、[SMB](/zh/foundry/available-connectors/smb/)和[Sharepoint online](/zh/foundry/available-connectors/sharepoint-online/)。[了解更多关于文件批量同步的信息。](/zh/foundry/data-connection/file-based-syncs/)
* \*\*表批量同步：\*\*允许将带有架构的数据同步到Foundry数据集。这种情况下，部分同步定义还包括如何在外部系统架构和支持的Foundry架构选项之间进行类型转换。支持表批量同步的最常见系统是数据库和SaaS提供商，如[Microsoft SQL Server](/zh/foundry/available-connectors/microsoft-sql-server/)、[Postgres](/zh/foundry/available-connectors/postgresql/)、[SAP](/zh/foundry/sap/overview/)、[Salesforce](/zh/foundry/available-connectors/salesforce/)和[Netsuite](/zh/foundry/available-connectors/netsuite-overview/)。

### 流同步

**流同步**提供从提供低延迟数据馈送的系统流式传输数据的能力。数据被传送到[流数据集](/zh/foundry/data-integration/streams/)。支持流同步的一些系统示例包括[Kafka](/zh/foundry/available-connectors/kafka/)、[Amazon Kinesis](/zh/foundry/available-connectors/amazon-kinesis/)和[Google Pub/Sub](/zh/foundry/available-connectors/pubsub/)。

[了解更多关于流同步的信息。](/zh/foundry/data-connection/set-up-streaming-sync/)

### 变更数据捕获同步

**变更数据捕获(CDC)同步**类似于流同步，具有自动传播到数据传送流数据集的附加变更日志元数据。这种类型的同步通常用于支持某种形式低延迟复制的数据库。[了解更多关于变更数据捕获同步的信息。](/zh/foundry/data-integration/change-data-capture/#create-a-change-data-capture-sync)

### 媒体同步

**媒体同步**允许将媒体数据导入到[媒体集](/zh/foundry/data-integration/media-sets/)。媒体集提供比标准数据集更好的工具，用于在Foundry中摄取、变换和消费媒体数据。处理PDF、图像、视频和其他媒体时，我们建议使用媒体集而非数据集。[了解更多关于媒体同步的信息。](/zh/foundry/data-connection/media-set-sync/)

### HyperAuto

**HyperAuto**是一种专门的功能，可以动态发现您的SAP系统的架构，并自动化同步、管道和在Foundry中创建相应的Ontology。HyperAuto目前仅支持SAP。[了解更多关于HyperAuto的信息。](/zh/foundry/hyperauto/overview/)

### 文件导出

**文件导出**是文件批量同步的反向操作。在进行文件导出时，数据直接从Foundry数据集的底层文件中提取，并按原样写入目标系统的文件系统位置。[了解更多关于文件导出的信息。](/zh/foundry/data-connection/export-overview/#file-exports)

### 表导出

**表导出**是表批量同步的反向操作。在执行表导出时，数据以带有架构的Foundry数据集的行形式导出，然后写入目标系统中的表。[了解更多关于表导出的信息。](/zh/foundry/data-connection/export-overview/#table-exports)

### 流导出

**流导出**是流同步的反向操作。在进行流导出时，数据从Foundry流中导出，并记录到目标系统中指定的流队列或主题。[了解更多关于流导出的信息。](/zh/foundry/data-connection/export-overview/#streaming-exports)

### Webhooks

**Webhooks**表示对Foundry外部源系统的请求。Webhook请求可以在数据连接中灵活定义，以实现广泛的与外部系统的连接。[了解更多关于webhooks的信息。](/zh/foundry/data-connection/webhooks-overview/)

### 虚拟表

**虚拟表**表示将外部系统中的表格数据注册到Foundry中的虚拟表资源的能力。

除了注册单个虚拟表外，此功能还允许动态发现和自动注册外部系统中找到的所有表。

[了解更多关于虚拟表的信息。](/zh/foundry/data-integration/virtual-tables/)

### 虚拟媒体

**虚拟媒体**的工作方式类似于[媒体同步](#media-syncs)，允许来自外部系统的媒体在[媒体集](/zh/foundry/data-integration/media-sets/)中使用，但不将数据复制到Foundry中。相反，外部系统中包含的媒体文件可以作为特定媒体集中的虚拟媒体项注册。

[了解更多关于虚拟媒体的信息。](/zh/foundry/data-integration/media-sets/#virtual-storage)

### 探索

交互式**探索**功能允许您在执行同步、导出或与该系统交互的其他功能之前查看外部系统中包含的数据。

探索最常用于检查连接是否按预期工作，以及是否使用正确的权限和凭证进行连接。

### 在代码中使用

在代码中使用连接的能力旨在允许开发人员扩展和自定义从Foundry到其他系统的连接。Palantir的一般原则是，平台中使用专用连接器和点选配置选项的任何功能也应能通过编写自定义代码实现。在任何时候，开发人员都应该能够切换到基于代码的连接，以便更细致地控制执行外部连接的工作流的功能或性能。

任何连接器都可以在代码中使用；在大多数情况下，我们建议在代码中连接时使用[REST API源](/zh/foundry/available-connectors/rest-apis/#rest-api-source)或[通用连接器](/zh/foundry/available-connectors/generic/)。

| 在代码中使用选项 | 描述 |
| ------------------ | ----------- |
| 外部变换 | [外部变换](/zh/foundry/data-integration/external-transforms-source-based/)允许用Python编写的变换与外部系统通信。</br></br> 外部变换是[文件批量同步](#batch-syncs)、[文件导出](#file-exports)、[表批量同步](#batch-syncs)、[表导出](#table-exports)和[媒体同步](#media-syncs)的基于代码的替代方案。外部变换还可以用于将数据注册到[虚拟媒体集](#virtual-media)和[虚拟表](#virtual-tables)中。 |
| 外部函数 (webhooks) | [外部函数](/zh/foundry/data-integration/external-functions/)用TypeScript编写，支持导入源以调用在该源上定义的现有webhooks。这允许将现有的webhook调用包装在自定义的typescript逻辑和出错处理中。 |
| 外部函数 (直接) | [外部函数](/zh/foundry/data-integration/external-functions/)现在允许使用TypeScript的`fetch`和Python的`requests`直接调用外部系统。外部函数是[webhooks](#webhooks)的基于代码的替代方案。</br></br>直接外部调用的外部函数尚未普遍可用。 |
| 计算模块 | [计算模块](/zh/foundry/compute-modules/overview/)允许使用任意语言进行长时间运行的计算和编写连接。</br></br> 计算模块可以作为[流同步](#streaming-syncs)、[流导出](#streaming-exports)、[变更数据捕获同步](#change-data-capture-syncs)和[webhooks](#webhooks)的基于代码的替代方案。</br></br> 在计算模块中使用源尚未普遍可用。 |
| 外部模型 | [外部模型](/zh/foundry/integrate-models/external-model-connection/)目前不支持导入源。相反，您必须直接使用网络出口策略。 |
| 代码工作区 | [代码工作区](/zh/foundry/code-workspaces/overview/)目前不支持导入源。相反，您必须直接使用网络出口策略。 |
| 代码工作簿 | [代码工作簿](/zh/foundry/code-workbook/overview/)目前不支持外部连接。 |

:::callout{theme="neutral"}
并非所有源配置都允许使用**在代码中使用**功能。不支持代理工作者连接，并且某些凭证类型如云身份、出站应用程序和OIDC目前可能无法从代码中使用。
:::

## 其他概念

数据连接还包括各种特定于特定工作流的其他概念。有些概念曾经使用过，现在已过时，但在此保留以供参考。

### 同步

历史上，术语**同步**通常用于指代将数据引入Foundry。同步现在被分为上面列出的更具体的功能。每个功能都有更多详细信息，例如**批量同步**、**流同步**、**变更数据捕获同步**、**媒体同步**等。

### 任务 \[已过时]

用于实现连接器的插件框架允许自定义扩展称为**任务**。任务表示通过提供YAML配置并在Java中作为数据连接插件的一部分实现的功能单元。Palantir已停止开发新任务，所有官方支持的功能已迁移不再使用任务。

根据[产品生命周期](/zh/foundry/platform-overview/development-life-cycle/#sunset-and-deprecation)，任务目前被视为`已过时`。任务最终将完全弃用，我们强烈建议在任何可能需要任务的地方使用[基于代码的连接选项](#use-in-code)。
