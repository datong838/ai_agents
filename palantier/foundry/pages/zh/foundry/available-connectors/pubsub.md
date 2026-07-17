---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/pubsub/",
  "title": "Google Pub/Sub",
  "page_id": "pubsub",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/google-drive/",
  "next": "/zh/foundry/available-connectors/google-search/",
  "scraped_at": "2026-07-13T05:35:49.813431+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Google Pub/Sub

将 Foundry 连接到 Google Pub/Sub，以实时读取主题中的数据到 Foundry 流。

## 支持的功能

|功能 |状态 |
|--- |--- |
| 探索 | 🟢 一般可用 |
| 流同步 | 🟢 一般可用 |
| [流导出](/zh/foundry/data-connection/export-overview/#streaming-exports) | 🟢 一般可用 |

## 数据模型

连接器不会解析消息内容，任何类型的数据都可以同步到 Foundry。所有内容都会上传到 `data` 列中，未解析。使用下游流变换（例如，在 [Pipeline Builder](/zh/foundry/pipeline-builder/transforms-overview/) 中的 `parse_json`）来解析数据。`id` 列将显示从 Pub/Sub 接收到的消息 ID。

| id (字符串) | data (字符串) |
|---    |--- |
| 5986331692832221    | {"firstName": "John", "lastName": "Doe"} |
| 5986326266478130    | test-payload |

设置同步时，Foundry 中数据集的模式**必须匹配**上述模式。

## 性能和限制

连接器使用单个消费者线程从 Pub/Sub 同步消息。当从 Foundry 导出数据到 Pub/Sub 时，每个 Foundry 数据流分区使用一个线程。

:::callout{theme="neutral"}
流同步基于 Foundry 中的输出数据集创建一个订阅。凭据必须具有创建订阅的权限。如果配置了多个导入从同一个主题读取，它们每个都会创建自己的订阅并读取主题上的所有消息。
:::

流同步旨在成为一致的、长时间运行的任务。任何对流同步的中断都可能导致停机，具体取决于预期结果。

在 Foundry 中设置流同步之前，请考虑以下事项：

* 代理连接的任务将在维护窗口期间（通常每周一次）重新启动以进行升级。预计这些重启期间的停机时间少于五分钟。
* 直接连接的任务至少每48小时重新启动一次。假设资源可用，任务可以立即重新启动，预计停机时间少于十分钟。

## 设置

1. 打开 [Data Connection](/zh/foundry/data-connection/overview/) 应用程序并选择屏幕右上角的 **+ New Source**。
2. 从可用的连接器类型中选择 **Pub/Sub**。
3. 选择通过互联网使用[**直接连接**](/zh/foundry/data-connection/set-up-direct-connection/)或[**通过中介代理**](/zh/foundry/data-connection/set-up-agent/)连接。
4. 按照以下部分中的信息继续设置连接器的其他配置提示。

了解更多关于在 Foundry 中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

### 认证

选择两种可用的认证方法之一：

* **GCP 实例帐户：** 请参阅 [Google Cloud 文档 ↗](https://cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances#using) 了解如何设置基于实例的认证。
  * 请注意，GCP 实例认证仅适用于在 GCP 中适当配置的实例上运行的代理连接。

* **服务帐户密钥文件：** 请参阅 [Google Cloud 文档 ↗](https://cloud.google.com/bigquery/docs/authentication/service-account-file) 了解如何设置服务帐户密钥文件认证。密钥文件可以作为 **JSON** 或 **PKCS8** 凭据提供。

配置的凭据必须具有以下访问权限：

* 对于同步：
  * `roles/pubsub.viewer`
  * `roles/pubsub.subscriber`
  * `projects.subscriptions.create`
* 对于导出：
  * `roles/pubsub.publisher`

## 连接详情

Pub/Sub 连接器提供以下配置选项：

| 选项  | 必需?  | 描述 |
|--- |--- |---  |
| `Project ID` | 是 |   GCP 中项目的 ID。 |
| `Credentials settings` | 是 |  按照上述[认证](#authentication)指南进行配置。 |
| `Proxy settings` | 否 | 启用以允许代理连接到 Pub/Sub。|
| `GRPC Settings` | 否\* |  用于配置 GRPC 通道的高级设置。 |

## 从 Pub/Sub 同步数据

在 [设置流同步](/zh/foundry/data-connection/set-up-streaming-sync/) 教程中了解如何设置与 Pub/Sub 的同步。

设置同步时，数据集的模式**必须匹配**上述[数据模型部分](#data-model)中描述的模式。

## 导出数据到 Pub/Sub

连接器支持通过 Data Connection 将流导出到 Pub/Sub。

要导出到 Pub/Sub，首先[启用导出](/zh/foundry/data-connection/export-overview/#enable-exports-for-source)用于 Pub/Sub 连接器。然后，[创建新导出](/zh/foundry/data-connection/export-overview/#creating-a-new-export)。

### 导出配置选项

| 选项  | 必需? | 默认 | 描述 |
|--- |--- |--- |--- |
| `Topic` | 是 | N/A  | 您要导出的 Pub/Sub 主题。 |
| `Value Column` | 否 | N/A | 如果此处未指定值，Foundry 流记录的整个内容将作为字符串写入 Pub/Sub。如果指定，则只有 `Value Column` 的内容将导出到 Pub/Sub。 |
