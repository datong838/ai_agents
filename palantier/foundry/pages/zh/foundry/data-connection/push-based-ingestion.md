---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/push-based-ingestion/",
  "title": "将数据推入流",
  "page_id": "push-based-ingestion",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/syncs-troubleshooting/",
  "next": "/zh/foundry/data-connection/export-overview/",
  "scraped_at": "2026-07-13T05:33:00.141850+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 将数据推入流

在 Foundry 中，大多数数据摄取专注于从源系统提取数据并将其同步到数据集或流中。

通过流，Foundry 支持**基于推送的摄取**以支持基于事件的工作流。

在 Foundry 中，基于推送的记录摄取遵循与典型 REST 服务相同的原则。通过一系列 REST 端点，我们公开了一个基于推送的 API，可以消费记录并将其写入流和数据集。推送到流中需要以下高级信息：

* 流的数据集资源标识符。
* 分支名称。
* 用于验证请求的词元。

:::callout{theme="neutral"}
如果您已经为您的数据配置了一个 Foundry 源，您可能希望连接该源。了解如何[设置流同步](/zh/foundry/data-connection/set-up-streaming-sync/)以使用现有源，或了解如何[设置 Kafka 源](/zh/foundry/available-connectors/kafka/)。
:::

下面，我们将讨论将数据推入流所需的步骤：

1. [设置](#part-1-initial-setup)一个新的流。
2. [推送记录](#part-2-push-records-into-the-stream)到流中。
3. [共享](#part-3-share-the-stream)流。
4. [测试](#part-4-test-the-stream)流。

## 第1部分. 初始设置

首先，开始流创建工作流程。

1. 登录 Foundry。
2. 导航到一个[项目](/zh/foundry/projects/overview/)。
3. 选择右上角的 **+ 新建**。
4. 向下滚动并选择 **流**。

<img alt="创建流" src="../../foundry-docs/data-connection/media/stream-create@2x.png">

接下来，我们必须定义流的模式、吞吐量和键。

* **模式**定义了流数据的结构和类型。
* **吞吐量**代表数据处理速率，并将影响流中使用的分区数量。了解更多信息请参阅我们的[吞吐量](/zh/foundry/building-pipelines/streaming-performance-considerations/#throughput)和[分区](/zh/foundry/data-integration/streams/#partitions)文档。
* **键**用于在使用多个分区时保证唯一 ID 的排序。了解更多信息请参阅我们的[流键](/zh/foundry/building-pipelines/streaming-keys/)文档。

在本教程中，我们将创建一个简单的单分区流。

* 将模式设置为 `sensor_id: String`、`temperature: Double` 和 `created_at: Timestamp`。
* 将吞吐量设置为 `Normal`。

然后，配置您的流。

* 通过选择 `从 JSON 样本生成...` 按钮并粘贴现有的 JSON blob，自动生成模式。
* 如果您正在从关系数据库流式传输实时更新，请设置[变更数据捕获](/zh/foundry/data-integration/change-data-capture/)。
* 考虑流的并行性需求，以确定是否需要更高的吞吐量设置。请查看我们的[分区](/zh/foundry/data-integration/streams/#partitions)文档以获取更多信息。
* 考虑在使用多个分区时设置键以保证排序。

<img alt="定义流" src="../../foundry-docs/data-connection/media/stream-define@2x.png">

:::callout{theme="neutral"}
在选择 **创建流** 之前，必须解决所有验证错误。将鼠标悬停在页面底部的工具提示上以获取更多关于错误的详细信息。
:::

选择右下角的 **创建流** 按钮以导航到 **连接** 页面。在这里，您可以指定如何连接到流数据。

## 第2部分. 将记录推入流中

我们现在准备连接我们的流。

1. 对于基于推送的摄取，选择 **通过 API 连接** 部分下的选项之一。

   任何可以发出 HTTP 请求的语言或技术都可以用来推送记录。我们提供 cURL、Python、JavaScript via Node 和 Java 的示例。如果您想通过 Foundry 同步而不是将数据推入 Foundry，请查看如何[设置流同步](/zh/foundry/data-connection/set-up-streaming-sync/)。

   在本示例中，我们将选择 **cURL**。

    <img alt="流连接" src="../../foundry-docs/data-connection/media/stream-connect@2x.png">

   然后您将进入 **推送** 数据工作流程页面。

2. 接下来，选择一种身份验证机制。我们支持两种请求身份验证方式：

   * **使用第三方应用程序推送（推荐）：** 此方法使用 OAuth2 工作流程创建一个安全的词元，该词元可以用于将记录推入您的流。
   * **使用个人词元推送：** 此方法仅使用用户生成的词元进行测试。

    <img alt="流推送选项" src="../../foundry-docs/data-connection/media/stream-push-auth@2x.png">

3. 对于本教程，选择 **使用第三方应用程序推送** 方法。按照屏幕上的步骤设置第三方应用程序并创建您的[客户端密钥](/zh/foundry/platform-security-third-party/register-3pa/)。

    <img alt="流推送第三方身份验证" src="../../foundry-docs/data-connection/media/stream-push-auth-third-party@2x.png">

4. 现在，选择 **前往第三方应用程序** 以在您的 Foundry 平台设置中打开第三方应用程序管理页面。

5. 选择屏幕右上角的 **注册新应用程序**。

    <img alt="第三方新应用" src="../../foundry-docs/data-connection/media/stream-third-party-register@2x.png">

6. 选择一个名称，将客户端类型设置为 **服务器应用程序**。

    <img alt="第三方创建应用" src="../../foundry-docs/data-connection/media/stream-third-party-register-new@2x.png">

7. 选择 **创建**，您将看到您的客户端 ID 和密钥。

   :::callout{theme="warning"}
   一旦离开此页面，客户端密钥将不可访问。请务必将其存储在安全位置。
   :::

8. 现在，您可以将客户端 ID 和密钥添加到 **推送** 工作流程页面。

    <img alt="添加客户端密钥" src="../../foundry-docs/data-connection/media/stream-client-secret@2x.png">

9. 向下滚动到工作流程的 **配置应用程序** 部分，然后选择 **管理应用程序** 以在 Foundry 平台设置中打开 **第三方应用程序** 管理页面。

    <img alt="配置第三方应用" src="../../foundry-docs/data-connection/media/stream-configure-third-party-app@2x.png">

10. 接下来，启用 **客户端凭证授予** 设置。

    <img alt="配置授予" src="../../foundry-docs/data-connection/media/stream-third-party-app-server@2x.png">

11. 最后，点击右上角的 **保存**。

## 第3部分: 共享流

现在，我们需要与我们创建的应用程序共享流。

1. 首先，返回到 **推送** 工作流程页面。在工作流程中的 **使用您的新应用程序** 部分下，找到您生成的客户端 ID。

    <img alt="客户端 ID" src="../../foundry-docs/data-connection/media/stream-client-id@2x.png">

2. 接下来，选择右上角的 **共享** 以打开流 **详细信息** 侧边栏的 **角色** 选项卡。

    <img alt="共享第三方应用" src="../../foundry-docs/data-connection/media/stream-share-third-party-app@2x.png">

3. 复制并粘贴客户端 ID 到 **角色** 搜索字段中以找到您创建的应用程序。选择 **+** 搜索并选择 `Editor` 角色。

4. 选择侧边栏底部的 **保存** 以共享流。

5. 返回到推送工作流程并选择 **下一步**。

## 第4部分: 测试流

现在将为您提供可以用于将测试记录推入流中的代码示例。根据您在前面步骤中选择的语言，代码示例会有所不同。在本示例中，我们使用 cURL。

:::callout{theme="neutral"}
在运行 cURL 命令之前，请确保安装 jQuery 以进行命令行 JSON 解析。
:::

1. 首先，从第一个框中复制命令。这将访问 Foundry 的 OAuth2 端点，为您提供一个可以用于推送记录的访问词元。

  <img alt="用 cURL 推送记录" src="../../foundry-docs/data-connection/media/stream-curl-push@2x.png">

2. 在您的 Mac、Windows 或 Linux 机器上的 bash 终端中执行命令。

   一旦命令执行完毕，您将拥有一个名为 `$ACCESS_TOKEN` 的可用变量。您将在下一个命令中使用此变量来推送记录。

   第二个命令将使用 cURL 向 Foundry 端点发出包含我们想要插入到流中的记录的 post 请求。该命令预先填充了一个要推送到流中的虚拟记录，但您可以在 HTTP 请求中提供任何符合流模式的数据。

3. 将第二个命令复制并粘贴到您的终端并执行。

   如果命令成功，您将在流中看到记录出现。

    <img alt="查看记录" src="../../foundry-docs/data-connection/media/stream-view-records@2x.png">

要更改推入流中的数据，请修改 post 请求的数据参数。

```json
[
  {
    "value": {
      "sensor_id": "sensor4", // 传感器的唯一标识符
      "temperature": 4.132   // 传感器测量的温度值
    }
  }
]
```

您还可以通过展开 **测试 JSON** 卡片，从用户界面向流中发送测试记录。

<img alt="Test with JSON" src="../../foundry-docs/data-connection/media/stream-test-with-json.png">

## 下一步

现在您已经成功将数据推送到流中，可以开始变换您的数据了。选择 **开始构建管道** 以导航到管道搭建器应用程序，在那里您将搭建您的流式管道。了解如何[变换您的数据](/zh/foundry/building-pipelines/create-stream-pipeline-pb/)，以及了解有关管道搭建器中[可用的不同变换](/zh/foundry/pipeline-builder/overview/)的更多信息。
