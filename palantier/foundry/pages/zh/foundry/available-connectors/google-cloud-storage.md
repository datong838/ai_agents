---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/google-cloud-storage/",
  "title": "Google Cloud Storage",
  "page_id": "google-cloud-storage",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/google-campaign-manager/",
  "next": "/zh/foundry/available-connectors/google-contacts/",
  "scraped_at": "2026-07-13T05:35:56.931627+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Google Cloud Storage

将Foundry连接到Google Cloud Storage，以在Foundry数据集和存储桶之间同步文件。

## 支持的功能

| 功能  | 状态 |
|--- |--- |
| 探索 | 🟢 普遍可用 |
| 批量导入 | 🟢 普遍可用 |
| 增量 | 🟢 普遍可用 |
| [虚拟表](/zh/foundry/data-integration/virtual-tables/) | 🟢 普遍可用 |
| 导出任务 | 🟡 停用 |
| [文件导出](/zh/foundry/data-connection/export-overview/#file-exports) | 🟢 普遍可用 |

## 数据模型

连接器可以将任何类型的文件传输到Foundry数据集。文件格式会被保留，传输过程中或之后不会应用任何模式。对输出数据集应用任何必要的模式，或[编写下游变换](/zh/foundry/pipeline-builder/transforms-overview/)以访问数据。

## 性能和限制

传输文件的大小没有限制。但是，网络问题可能导致大规模传输失败。特别是，运行超过两天的直接云同步将被中断。为了避免网络问题，我们建议使用较小的文件大小，并限制每次执行同步时摄取的文件数量。可以[安排](/zh/foundry/data-connection/set-up-sync/#configure-sync)频繁运行同步。

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用，并在屏幕右上角选择\*\*+ 新来源\*\*。
2. 从可用的连接器类型中选择**Google Cloud Storage**。
3. 选择通过互联网使用[**直接连接**](/zh/foundry/data-connection/set-up-direct-connection/)或通过[**中介代理**](/zh/foundry/data-connection/set-up-agent/)连接。
4. 按照以下部分的信息继续设置您的连接器。

了解更多关于在Foundry中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

:::callout{theme="warning"}
您必须拥有[Google Cloud IAM服务账户 ↗](https://cloud.google.com/iam/docs/overview#service_account0)才能进行Google Cloud Storage身份验证和设置。
:::

### 身份验证

访问的存储桶需要以下角色：

* `Storage Object Viewer`: 读取数据
* `Storage Object Creator`: 导出数据到Google Cloud Storage
* `Storage Object Admin`: 将文件导入Foundry后从Google Cloud Storage中删除文件。

了解更多关于所需角色的信息，请参阅[Google Cloud文档关于访问控制 ↗](https://cloud.google.com/storage/docs/access-control/iam-roles)。

从以下可用的身份验证方法中选择一个：

* **GCP实例账户：** 请参阅[Google Cloud文档 ↗](https://cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances#using)以获取有关如何设置基于实例的身份验证的信息。
  * 请注意，GCP实例身份验证仅适用于通过运行在GCP中适当配置的实例上的代理操作的连接器。

* **服务账户密钥文件：** 请参阅[Google Cloud文档 ↗](https://cloud.google.com/docs/authentication/provide-credentials-adc#local-key)以获取有关如何设置服务账户密钥文件身份验证的信息。

* **工作负载身份联合（OIDC）：** 按照显示的源系统配置说明设置OIDC。有关工作负载身份联合的详细信息，请参阅[Google Cloud文档 ↗](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-providers)和[我们的文档](/zh/foundry/data-connection/oidc/)以了解OIDC如何与Foundry一起工作。

### 网络

Google Cloud Storage连接器需要通过443端口访问以下域的网络权限：

* `storage.googleapis.com`
* `oauth2.googleapis.com`
* `accounts.google.com`

## 配置选项

Google Cloud Storage连接器提供以下配置选项：

| 选项  | 必需？  | 描述 |
|--- |--- |---  |
| `Project Id` | 是 | 包含Cloud Storage存储桶的项目ID。 |
| `Bucket name` | 是 | 要读取/写入数据的存储桶名称。|
| `Credentials settings` | 是 | 使用上面显示的[身份验证](#authentication)指导进行配置。 |
| `Proxy settings` | 否 | 启用以在连接Google Cloud Storage时使用代理。|

## 从Google Cloud Storage同步数据

Google Cloud Storage连接器使用基于文件的同步接口。请参阅关于[配置基于文件的同步](/zh/foundry/data-connection/file-based-syncs/)的文档。

## 虚拟表

本节提供了关于使用来自Google Cloud Storage源的[虚拟表](/zh/foundry/data-integration/virtual-tables/)的额外细节。本节不适用于同步到Foundry数据集。

| 虚拟表功能 | 状态 |
| --- | --- |
| 源格式 | 🟢 普遍可用: [Avro ↗](https://avro.apache.org/), [Delta ↗](https://docs.delta.io/latest/), [Iceberg ↗](https://iceberg.apache.org/), [Parquet ↗](https://parquet.apache.org/) |
| 手动注册 | 🟢 普遍可用 |
| 自动注册 | 🔴 不可用 |
| 下推计算 | 🔴 不可用 |
| 增量管道支持 | 🟢 Delta表普遍可用: `APPEND` 仅 ([详情](#delta))<br /> 🟢 Iceberg表普遍可用: `APPEND` 仅 ([详情](#iceberg))<br /> 🔴 Parquet表不可用 |

使用[虚拟表](/zh/foundry/data-integration/virtual-tables/)时，请记住以下源配置要求：

* 您必须将源设置为[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)。虚拟表不支持使用[中介代理](/zh/foundry/data-connection/set-up-agent/)。
* 确保建立了双向连接和白名单，如本[文档的网络部分](#networking)所述。
* 如果在代码仓库中使用虚拟表，请参阅[虚拟表文档](/zh/foundry/data-integration/virtual-tables/#virtual-tables-in-code-repositories)以了解所需的额外源配置的详细信息。
* 在设置源凭据时，您必须使用`JSON Credentials`、`PKC8 Auth`或`Workload Identity Federation (OIDC)`之一。使用虚拟表时不支持其他凭据选项。

### Delta

要启用由虚拟表支持的管道的增量支持，请确保在源Delta表上启用了[变更数据馈送 ↗](https://docs.databricks.com/delta/delta-change-data-feed.html#enable-change-data-feed)。在[Python变换](/zh/foundry/transforms-python/incremental-reference/#incrementaltransforminput)中支持`current`和`added`读取模式。在Python变换中会提供`_change_type`、`_commit_version`和`_commit_timestamp`列。

### Iceberg

需要Iceberg目录来加载由Apache Iceberg表支持的虚拟表。要了解更多关于Iceberg目录的信息，请参阅[Apache Iceberg文档 ↗](https://iceberg.apache.org/concepts/catalog/)。在源上注册的所有Iceberg表必须使用相同的Iceberg目录。

表将使用GCS中的Iceberg元数据文件创建。注册表时必须提供一个指示这些元数据文件位置的`warehousePath`。

增量支持依赖于Iceberg的[增量读取 ↗](https://iceberg.apache.org/docs/1.5.1/spark-queries/#incremental-read)，目前仅限于追加。在[Python变换](/zh/foundry/transforms-python/incremental-reference/#incrementaltransforminput)中支持`current`和`added`读取模式。

### Parquet

使用Parquet的虚拟表依赖于模式推断。最多将使用100个文件来确定模式。

## 导出数据到Google Cloud Storage

连接器可以将文件从Foundry数据集复制到Google Cloud Storage存储桶的任何位置。

要开始导出数据，您必须配置一个导出任务。导航到包含您要导出的Google Cloud Storage连接器的项目文件夹。右键选择连接器名称，然后选择`创建数据连接任务`。

在数据连接视图的左侧面板中：

1. 验证`源`名称与您要使用的连接器匹配。
2. 添加名为`inputDataset`的`输入`。**输入数据集**是正在导出的Foundry数据集。
3. 添加名为`outputDataset`的`输出`。**输出数据集**用于运行、安排和监控任务。
4. 最后，在文本字段中添加一个YAML块以定义任务配置。

:::callout{theme="neutral"}
左侧面板中显示的连接器和输入数据集的标签不反映YAML中定义的名称。
:::

在创建导出任务YAML时使用以下选项：

| 选项  | 必需？ | 描述 |
|---  |---  | --- |
| `directoryPath` | 是 | 将文件写入的Cloud Storage中的目录。|
| `excludePaths` | 否 | 正则表达式列表；名称匹配这些表达式的文件将不会被导出。 |
| `uploadConfirmation` | 否 | 当值为`exportedFiles`时，输出数据集将包含已导出文件的列表。  |
| `retriesPerFile` | 否 | 如果遇到网络出错，请增加此数字以允许在整个任务出错前重试上传到Cloud Storage。 |
| `createTransactionFolders` | 否 | 启用时，数据将写入指定`directoryPath`内的子文件夹。每个子文件夹基于Foundry中提交事务的时间并为每个导出事务提供唯一名称。|
| `threads` | 否 | 设置用于并行上传文件的线程数量。增加数量以使用更多资源。确保在代理上运行的导出有足够的资源来处理增加的并行化。|
| `incrementalType` | 否 | 对于增量搭建的数据集，设置为`incremental`以仅导出自上次导出以来发生的事务。|

示例任务配置：

```yaml
type: export-google-cloud-storage  # 类型：导出到 Google Cloud Storage
directoryPath: directory/to/export/to  # 导出文件的目录路径
excludePaths:  # 排除的路径
  -  ^_.*  # 排除以“_”开头的路径
  - ^spark/.*  # 排除以“spark/_”开头的路径
uploadConfirmation: exportedFiles  # 上传确认文件的名称
incrementalType: incremental  # 增量类型：增量导出
retriesPerFile: 0  # 每个文件的重试次数
createTransactionFolders: true  # 是否创建事务文件夹
threads: 0  # 使用的线程数，0表示自动选择
```

这段代码是一个配置文件，用于将数据导出到 Google Cloud Storage。它指定了导出目录、排除的路径、上传确认、增量导出类型、重试次数、事务文件夹创建和线程数等参数。
配置导出任务后，选择右上角的 **保存**。
