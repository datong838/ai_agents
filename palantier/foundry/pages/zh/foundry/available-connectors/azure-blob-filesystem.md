---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/azure-blob-filesystem/",
  "title": "Azure Blob Filesystem (ABFS)",
  "page_id": "azure-blob-filesystem",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/azure-active-directory/",
  "next": "/zh/foundry/available-connectors/azure-cosmos-db/",
  "scraped_at": "2026-07-13T05:34:56.399750+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Azure Blob Filesystem (ABFS)

将 Foundry 连接到 Azure Data Lake Storage Gen2 (ADLS Gen2) 和其他合格的 Azure 产品，使用 [Azure Blob Filesystem (ABFS) ↗](https://hadoop.apache.org/docs/r3.3.1/hadoop-azure/abfs.html)。ABFS 连接器允许将文件读取到 Foundry 并从 Foundry 写入到 Azure。

:::callout{theme="warning"}
不支持连接到 Azure Data Lake Storage Gen1。
:::

## 支持的功能

| 功能  | 状态 |
|--- |--- |
| 探索 | 🟢 普遍可用 |
| 批量导入 | 🟢 普遍可用 |
| 增量 | 🟢 普遍可用 |
| 媒体集 | 🟢 普遍可用  |
| [虚拟表](/zh/foundry/data-integration/virtual-tables/) | 🟢 普遍可用 |
| 导出任务 | 🟡 弃用 |
| [文件导出](/zh/foundry/data-connection/export-overview/#file-exports) | 🟢 普遍可用 |

## 数据模型

连接器可以将任何类型的文件传输到 Foundry 数据集。文件格式会被保留，并且在传输期间或之后不应用任何模式。对输出数据集应用任何必要的模式，或编写一个[下游变换](/zh/foundry/pipeline-builder/transforms-overview/)来访问数据。

## 性能和限制

可传输文件的大小没有限制。然而，网络问题可能导致大规模传输的失败。特别是，运行超过两天的直接云同步将被中断。为了避免网络问题，我们建议使用较小的文件大小，并限制每次同步执行中摄取的文件数量。可以[安排](/zh/foundry/data-connection/set-up-sync/#configure-sync)频繁运行同步。

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序，并在屏幕右上角选择 **+ 新建源**。
2. 从可用的连接器类型中选择 **ABFS—Azure Data Lake Storage Gen2**。
3. 选择使用[**直接连接**](/zh/foundry/data-connection/set-up-direct-connection/)通过互联网连接，或通过[**中介代理**](/zh/foundry/data-connection/set-up-agent/)连接。
4. 按照下文部分中的信息，继续设置连接器的其他配置提示。

:::callout{theme="warning"}
我们建议使用 ABFS 连接器的直接连接，以简化设置和配置。
:::

了解更多关于在 Foundry 中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

## 认证

要导入数据，连接器必须 `列出` 文件系统内容并 `读取` Azure 中的文件内容。可以通过与提供的连接凭证关联的主体的授权模式实现此行为。

* 在基于角色的访问控制 (RBAC) 的情况下，这是一种粗粒度的访问控制形式，主体需要在数据所在的容器上具有 [`Storage Blob Data Reader` ↗](https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-reader) 角色。
* 对于访问控制列表 (ACL)，这是一种细粒度的访问控制形式，主体需要在摄取文件上具有 `Read` ACL，并在从容器根目录到文件位置的所有路径目录上具有 `Execute` ACL。

了解更多关于 [ADLS Gen2 中的访问控制 ↗](https://docs.microsoft.com/azure/storage/blobs/data-lake-storage-access-control-model)。

ABFS 连接器支持以下身份验证配置选项，从最推荐到最不推荐：

* [Azure 托管身份](#azure-managed-identity-recommended)（推荐用于代理连接）
* [客户端凭证](#client-credentials)（推荐用于直接连接）
* [共享访问签名](#shared-access-signature)
* [用户名和密码](#usernamepassword)
* [刷新词元](#refresh-token)
* [共享密钥](#shared-key)
* [工作负载身份联合](#workload-identity-federation-oidc)

### Azure 托管身份（推荐用于代理连接）

我们建议使用 [Azure 托管身份 ↗](https://docs.microsoft.com/azure/active-directory/managed-identities-azure-resources/overview)进行身份验证。这种身份验证机制不需要在 Foundry 中存储凭证。用于连接数据的托管身份必须在底层存储上具有适当的权限。

| 选项  | 是否必需  | 描述 |
|--- |--- |---  |
| `Tenant ID` | 否 | 可从 [Microsoft Entra ID ↗](https://learn.microsoft.com/entra/fundamentals/how-to-find-tenant) 获取租户 ID。  |
| `Client ID` | 否 | 如果在代理运行的虚拟机 (VM) 上附加了多个托管身份（由系统或用户指派），请提供用于连接存储的 ID。 |

:::callout{theme="warning"}
托管身份身份验证方法依赖于虚拟机 (VM) 上所有进程可用的本地 REST 端点。此方法仅在通过部署在同一 Azure 租户内的 VM 上的代理进行连接时有效。
:::

### 客户端凭证（推荐用于直接连接）

[客户端凭证 ↗](https://hadoop.apache.org/docs/r3.3.1/hadoop-azure/abfs.html#OAuth_2.0_Client_Credentials)依赖于 Entra ID 中的[应用注册 ↗](https://learn.microsoft.com/azure/app-service/configure-authentication-provider-aad#--option-1-create-a-new-app-registration-automatically)（服务主体）。此方法是所有直接连接的首选方法。使用以下字段配置客户端凭证身份验证：

| 选项  | 是否必需  | 描述 |
|--- |--- |---  |
| `Client endpoint` | 是 | 用于直接连接的身份验证端点。<br/><br/> 通常采用 `https://login.microsoftonline.com/<directory-id>/oauth2/token` 的形式，其中 `<directory-id>` 是订阅 ID。有关更多详细信息，请参见 Azure 的[官方文档 ↗](https://learn.microsoft.com/azure/databricks/storage/azure-storage#azureserviceprincipal)。 |
| `Client ID` | 是 | 应用注册的 ID；也称为应用程序 ID。 |
| `Client secret` | 是 | 应用注册中生成的机密。 |

### 共享访问签名

[共享访问签名 (SAS) ↗](https://hadoop.apache.org/docs/r3.3.1/hadoop-azure/abfs.html#Shared_Access_Signature_.28SAS.29_Token_Provider)身份验证使用提供短期和严格范围凭证的词元。当服务可以根据需要生成这些词元并将其分发给使用它们的客户以供非常有限的时间使用时，这些词元最有用。

| 选项  | 是否必需  | 描述 |
|--- |--- |---  |
| `Blob SAS token` | 是 | [共享访问签名词元](#shared-access-signature-token)。

连接器需要一个静态 SAS 词元，并将存储一个长期有效的词元来对存储账户进行身份验证。

:::callout{theme="warning"}
一旦 SAS 词元过期，您的同步将停止工作，直到它被手动更新。因此，我们强烈建议不要使用 SAS 词元，并鼓励您使用其他身份验证解决方案。
:::

#### 共享访问签名词元

按照 [Azure 指南 ↗](https://learn.microsoft.com/rest/api/storageservices/create-user-delegation-sas#specify-the-signed-resource-field)获取 SAS 词元。

示例词元：

`/container1/dir1?sp=r&st=2023-02-23T17:53:28Z&se=2023-02-24T01:53:28Z&spr=https&sv=2021-12-02&sr=d&sig=1gF9B%2FOnEmtYeDl6eB9tb0va1qpSBjZw3ZJuW2pMm1E%3D&sdd=1`

我们通常建议在存储容器级别生成 SAS 词元。在 Azure 门户的容器视图中找到存储容器（在**设置** > **共享访问词元**下）。如果需要在存储账户级别（在 Azure 门户的存储账户视图中，在**安全性** > **网络** > **共享访问签名**下）生成 SAS 词元，则最小权限集如下：

* `"允许的服务": "Blob"`
* `"允许的资源类型": "Container" + "Object"`
* `"允许的权限": "Read" + "List"`

:::callout{theme="warning"}
要使用 SAS 词元连接到 Azure Blob Storage，您必须[指定目录 ↗](https://learn.microsoft.com/rest/api/storageservices/create-user-delegation-sas#specify-the-signed-resource-field)资源，其中存储了 blob。
:::

生成 SAS 词元时，请务必设置以下参数：

**签名协议：** 我们建议设置 [`spr` ↗](https://learn.microsoft.com/rest/api/storageservices/create-user-delegation-sas#specify-the-http-protocol) 以要求连接的 `https`。

**签名资源：** [根据授予访问的资源类型更改值 ↗](https://learn.microsoft.com/rest/api/storageservices/create-user-delegation-sas#specify-the-signed-resource-field)。

:::callout{theme="warning"}
如果正在使用的签名资源是指定目录，请确保还指定了[目录深度 ↗](https://learn.microsoft.com/rest/api/storageservices/create-user-delegation-sas#specify-the-directory-depth)。我们建议设置一个较高的深度值，以允许连接从嵌套目录中提取数据（例如，`sdd=100`）。
:::

### 用户名/密码

[用户名/密码 ↗](https://hadoop.apache.org/docs/r3.3.1/hadoop-azure/abfs.html#OAuth_2.0:_Username_and_Password)身份验证方法遵循 OAuth 协议。凭证是使用您的租户的 Azure 页面生成的（例如，`https://login.microsoftonline.com/<tenant-id>/oauth2/token`）。用您要连接的租户 ID 替换 `<tenant-id>`。

设置以下配置：

| 选项  | 是否必需  | 描述 |
|--- |--- |---  |
| `Client endpoint` | 是 | OAuth 配置中的客户端端点。 |
| `Username` | 是 | 用户的电子邮件地址。|
| `Proxy password` | 是 | 密码词元。|

### 刷新词元

[刷新词元 ↗](https://hadoop.apache.org/docs/r3.3.1/hadoop-azure/abfs.html#OAuth_2.0:_Refresh_Token)授权方法遵循 OAuth 协议。了解如何使用 [Azure 文档 ↗](https://learn.microsoft.com/azure/energy-data-services/how-to-generate-refresh-token)生成刷新词元。

设置以下配置：

| 选项  | 是否必需  | 描述 |
|--- |--- |---  |
| `Client ID` | 是 | 客户端 ID；可在 Microsoft Entra ID 中找到。  |
| `Refresh Token` | 是 | 刷新词元。 |

### 共享密钥

每个 Azure 存储账户都有两个[共享密钥 ↗](https://hadoop.apache.org/docs/r3.3.1/hadoop-azure/abfs.html#Default:_Shared_Key)。但是，我们不建议在生产中使用共享密钥，因为它们是在存储账户级别进行范围限定，而不是在容器级别。默认情况下，共享密钥具有管理员权限，旋转它们是手动操作。

要获取共享密钥，请导航到 Azure 门户中所需的存储账户，并在**安全性+网络**部分下选择**访问密钥**。

| 选项  | 是否必需  | 描述 |
|--- |--- |---  |
| `Account key` | 是 | 账户访问密钥。|

### 工作负载身份联合 (OIDC)

Azure [工作负载身份联合 ↗](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-create-trust-user-assigned-managed-identity)授权方法遵循 OpenID Connect (OIDC) 协议。按照显示的源系统配置说明设置工作负载身份联合。查阅[我们的文档](/zh/foundry/data-connection/oidc/)，了解 OIDC 如何与 Foundry 一起工作。

| 选项  | 是否必需  | 描述 |
|--- |--- |---  |
| `Tenant ID` | 是 | 可从 [Microsoft Entra ID ↗](https://learn.microsoft.com/entra/fundamentals/how-to-find-tenant) 获取租户 ID。  |
| `Client ID` | 是 | 客户端 ID 可在 Microsoft Entra ID 中找到。  |

### 网络

在设置到 Azure 的[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)时，需要设置网络访问，以便 Foundry 能够与源通信。这是一个两步过程：

1. **设置 Foundry 到源的网络出口访问。** 您可以通过在数据连接应用程序中对源应用适当的[出口策略](/zh/foundry/administration/configure-egress/#network-egress-policies)来实现这一点。Azure 连接器需要对存储账户域的 `端口 443` 的网络访问。例如，如果您正在连接到 `abfss://file_system@account_name.dfs.core.windows.net`，则存储账户的域是 `account_name.dfs.core.windows.net`。数据连接应用程序会根据源中提供的连接详细信息建议适当的出口策略。
2. **将 Foundry 列入 Azure 存储容器的白名单。** 您可以通过按照 Azure 的[文档 ↗](https://learn.microsoft.com/azure/storage/common/storage-network-security?tabs=azure-portal)中描述的方式，将 Foundry IP 列入 Azure 存储账户的白名单。在[控制面板应用程序](/zh/foundry/administration/control-panel/)的**网络出口**下可以找到您的 Foundry IP 详细信息。

:::callout{theme="neutral"}
如果您正在设置对与 Foundry 注册位于同一 Azure 区域的 Azure 存储桶的访问，则需要通过 PrivateLink 设置与上述不同的网络配置。如果是这种情况，请联系您的 Palantir 管理员以获取帮助。
:::

## 配置选项

连接器具有以下附加配置选项：

| 选项  | 是否必需  | 描述 |
|--- |--- |---  |
| `Root directory` | 是 |  读取/写入数据的目录。 |
| `Catalog` | 否 | 为此 S3 存储桶中存储的表配置一个目录。有关更多详细信息，请参见[虚拟表](#virtual-tables)。 |

根目录必须按照以下格式指定：`abfss://file_system@account_name.dfs.core.windows.net/<directory>`。

示例：

* [`abfss://file_system@account_name.dfs.core.windows.net/` ↗](https://github.com/apache/hadoop/blob/branch-3.3.1/hadoop-common-project/hadoop-common/src/main/resources/core-default.xml#L2188) 访问该文件系统的所有内容。
* [`abfss://file_system@account_name.dfs.core.windows.net/path/to/directory` ↗](https://github.com/apache/hadoop/blob/branch-3.3.1/hadoop-common-project/hadoop-common/src/main/resources/core-default.xml#L2194) 访问特定目录。

:::callout{theme="neutral"}
如果您正在使用 SAS 词元进行身份验证并访问 blob 存储，必须在根目录配置中指定一个目录。所有内容必须位于指定目录的子文件夹中，以确保正确访问。
:::

## 从 Azure 数据湖/Blob 存储同步数据

ABFS 连接器使用[基于文件的同步界面](/zh/foundry/data-connection/file-based-syncs/)。

## 导出数据到 Azure 数据湖/Blob 存储

要导出到 ABFS，首先为您的 ABFS 连接器[启用导出](/zh/foundry/data-connection/export-overview/#enable-exports-for-source)。然后， [创建一个新的导出](/zh/foundry/data-connection/export-overview/#creating-a-new-export)。

:::callout{theme="warning"}
虽然上述导出工作流是首选，但现有导出最初可能配置为导出任务。我们通常不建议使用导出任务将数据写回外部源。然而，导出任务可能在某些 Foundry 注册上为某些源类型提供并支持。

以下导出任务文档适用于尚未过渡到我们推荐的导出工作流的导出任务用户。
:::

连接器可以将文件从 Foundry 数据集复制到 Azure 文件系统的任何位置。

要开始导出数据，必须配置导出任务。导航到包含要导出到的连接器的项目文件夹。右键选择连接器名称，然后选择 `创建数据连接任务`。

在数据连接视图的左侧面板中：

1. 验证 `Source` 名称与您要使用的连接器匹配。
2. 添加一个名为 `inputDataset` 的 `输入`。**输入数据集**是正在导出的 Foundry 数据集。
3. 添加一个名为 `outputDataset` 的 `输出`。**输出数据集**用于运行、安排和监控任务。
4. 最后，在文本字段中添加一个 YAML 块以定义任务配置。

:::callout{theme="neutral"}
左侧面板中出现的连接器和输入数据集的标签不反映 YAMl 中定义的名称。
:::

在创建导出任务 YAML 时使用以下选项：

| 选项  | 是否必需 | 描述 |
|---  |---  | --- |
| `directoryPath` | 是 | 文件将被写入的目录。路径必须以 `/` 结尾。  |
| `excludePaths` | 否 | 正则表达式列表；名称匹配这些表达式的文件将不会被导出。 |
| `rewritePaths` | 否 | 有关更多信息，请参见[以下部分](#rewritepaths)。 |
| `uploadConfirmation` | 否 | 当值为 `exportedFiles` 时，输出数据集将包含已导出文件的列表。  |
| `createTransactionFolders` | 否 | 启用时，数据将被写入指定 `directoryPath` 中的子文件夹。每个子文件夹将在 Foundry 中具有唯一名称的每个导出事务中基于提交时间创建。 |
| `incrementalType` | 否 | 对于增量搭建的数据集，设置为 `incremental` 以仅导出自上次导出以来发生的事务。|
| `flagFile` | 否 | 有关更多信息，请参见[以下部分](#flag-file)。 |
| `spanMultipleViews` | 否 | 如果 `true`，将一次导出多个 Foundry 事务。如果 `false`，单个搭建将一次只导出一个事务。如果启用了增量，则将首先导出最旧事务中的文件。 |

### `rewritePaths`

如果第一个键匹配文件名，键中的捕获组将被值替换。值本身可以有额外的部分来向文件名添加元数据。

如果值包含：

* `${dt:javaDateExpression}`：值中的这一部分将被文件导出时的时间戳替换。`javaDateExpression` 遵循 [DateTimeFormatter ↗](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html) 模式。
* `${transaction}`：值中的这一部分将被包含此文件的 Foundry 事务 ID 替换。
* `${dataset}`：值中的这一部分将被包含此文件的 Foundry 数据集 ID 替换。

示例：

考虑一个 Foundry 数据集中的文件名为 "spark/file\_name"，事务 ID 为 `transaction_id`，数据集 ID 为 `dataset_id`。如果您使用表达式 `fi.*ame` 作为键，并将 `file_${dt:DD-MM-YYYY}-${transaction}-${dataset}_end` 作为值，当文件写入到 Azure 时，它将被存储为 `spark/file_79-03-2023-transaction_id-dataset_id_end`。

### 标记文件

连接器可以在构建完成后将一个空的标记文件写入到 Azure 存储中。空文件表示内容已准备好供使用，并且不会再被修改。标记文件将写入到 `directoryPath`。然而，如果启用了 `createTransactionFolders`，将在每个写入内容的文件夹中创建一个标记文件。如果启用标记文件，并且标记文件被命名为 `confirmation.txt`，则在构建中导出的文件被写入后，所有标记文件将被一次性写入

:::callout{theme="neutral"}
标记文件在构建结束时写入，而不是在子文件夹导出时写入。
:::

如果 Azure 中的文件比标记文件更新，这通常表示前一次导出未成功或正在进行导出。

配置导出任务后，选择右上角的 **保存**。

## 虚拟表

本节提供有关使用来自 Azure Data Lake Storage Gen 2 (Azure Blob Storage) 源的[虚拟表](/zh/foundry/data-integration/virtual-tables/)的更多详细信息。在同步到 Foundry 数据集时，本节不适用。

| 虚拟表功能 | 状态 |
| --- | --- |
| 源格式 | 🟢 普遍可用：[Avro ↗](https://avro.apache.org/)、[Delta ↗](https://docs.delta.io/latest/)、[Iceberg ↗](https://iceberg.apache.org/)、[Parquet ↗](https://parquet.apache.org/) |
| 手动注册 | 🟢 普遍可用 |
| 自动注册 | 🔴 不可用 |
| 下推计算 | 🔴 不可用 |
| 增量流水线支持 | 🟢 Delta 表普遍可用：仅限 `APPEND`（[详细信息](#delta)）<br /> 🟢 Iceberg 表普遍可用：仅限 `APPEND`（[详细信息](#iceberg)）<br /> 🔴 Parquet 表不可用 |

使用[虚拟表](/zh/foundry/data-integration/virtual-tables/)时，请记住以下源配置要求：

* 您必须将源设置为[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)。虚拟表不支持使用[中介代理](/zh/foundry/data-connection/set-up-agent/)。
* 确保按照本文件的[网络部分](#networking)所述建立了双向连接和白名单。
* 如果在代码库中使用虚拟表，请参阅[虚拟表文档](/zh/foundry/data-integration/virtual-tables/#virtual-tables-in-code-repositories)，了解所需的额外源配置。
* 在设置源凭证时，您必须使用 `客户端凭证`、`用户名/密码` 或 `工作负载身份联合` 之一。使用虚拟表时不支持其他凭证选项。

### Delta

要启用由虚拟表支持的流水线的增量支持，请确保在源 Delta 表上启用 [变更数据提要 ↗](https://docs.databricks.com/delta/delta-change-data-feed.html#enable-change-data-feed)。[Python 变换](/zh/foundry/transforms-python/incremental-reference/#incrementaltransforminput)中的 `current` 和 `added` 读取模式均受支持。`_change_type`、`_commit_version` 和 `_commit_timestamp` 列将可用于 Python 变换。

### Iceberg

要加载由 Apache Iceberg 表支持的虚拟表，需要 Iceberg 目录。要了解有关 Iceberg 目录的更多信息，请参阅 [Apache Iceberg 文档 ↗](https://iceberg.apache.org/concepts/catalog/)。在源上注册的所有 Iceberg 表必须使用相同的 Iceberg 目录。

默认情况下，表将使用 S3 中的 Iceberg 元数据文件创建。注册表时，必须提供一个指示这些元数据文件位置的 `warehousePath`。

[Unity Catalog ↗](https://www.databricks.com/product/unity-catalog) 可以在 Databricks 中使用 Delta Universal Format (UniForm) 作为 Iceberg 目录。要了解有关此集成的更多信息，请参阅 [Databricks 文档 ↗](https://docs.databricks.com/en/delta/uniform.html)。目录可以在源的[连接详细信息](#connection-details)选项卡中进行配置。您需要提供端点和一个[个人访问词元](https://docs.databricks.com/en/dev-tools/auth/pat.html)以连接到 Unity Catalog。表应使用 `catalog_name.schema_name.table_name` 命名模式注册。

![虚拟表 ABFS 目录](../../../images/foundry/available-connectors/virtual_tables_abfs_catalog.png)

增量支持依赖于 Iceberg [增量读取 ↗](https://iceberg.apache.org/docs/1.5.1/spark-queries/#incremental-read)，目前仅支持追加。[Python 变换](/zh/foundry/transforms-python/incremental-reference/#incrementaltransforminput)中的 `current` 和 `added` 读取模式均受支持。

### Parquet

使用 Parquet 的虚拟表依赖于模式推断。最多会使用 100 个文件来确定模式。

## 故障排除

使用以下部分进行已知错误的故障排除。

### 资源不支持指定的 HTTP 动词 HEAD

确保您正在使用 DFS 位置，而非 blob 存储。

例如：

```yaml
# 正确:
abfsRootDirectory: 'abfss://<account_name>.dfs.core.windows.net/'
# 错误:
abfsRootDirectory: 'abfss://<account_name>.blob.core.windows.net/'
```

以上代码涉及 Azure Data Lake Storage (ADLS) 的路径配置。在使用 ADLS Gen2 时，正确的路径应该使用 `dfs.core.windows.net`，而不是 `blob.core.windows.net`。

### 此端点不支持BlobStorageEvents或SoftDelete。如果您想使用此端点，请禁用这些账户功能

```markdown
magritteabfs.source.org.apache.hadoop.fs.FileAlreadyExistsException: 操作失败：
"此端点不支持 BlobStorageEvents 或 SoftDelete。如果您希望使用此端点，请禁用这些账户功能。", 409, HEAD,
https://STORAGE_ACCOUNT_NAME.dfs.core.windows.net/CONTAINER_NAME/?
upn=false&action=getAccessControl&timeout=90
```

此错误信息表示在使用 Azure Data Lake Storage (ADLS) 时遇到了`FileAlreadyExistsException`异常。具体原因是所使用的端点不支持 BlobStorageEvents 或 SoftDelete 功能。要解决此问题，需要禁用这些账户功能。
由于Hadoop ABFS当前[不支持 ↗](https://issues.apache.org/jira/browse/HADOOP-16842)启用了`SoftDelete`的账户，因此抛出了此出错。唯一的解决方案是禁用存储账户的此功能。

### AADToken: HTTP连接失败于从AzureAD获取词元。HTTP响应：401 Unauthorized

`Client Credentials`身份验证机制存在[已知问题 ↗](https://knowledgebase.progress.com/articles/Article/oauth2-token-request-to-microsoft-azure-active-directory-service-failed-with-aadsts7000215)。如果使用数据连接界面设置，包含`+`或`/`的服务主体客户端机密将无法正常工作。通过创建不含`+`或`/`的新凭据来解决此问题。如果此问题持续，请联系您的Palantir代表。

### 确认托管身份流在数据连接代理之外正常工作

在排查问题时，我们建议将访问问题与网络问题分开。为此，首先独立测试对源数据的访问（在数据连接之外）。然后，验证[托管身份 ↗](https://docs.microsoft.com/azure/active-directory/managed-identities-azure-resources/how-to-use-vm-token#get-a-token-using-curl.)是否可以被用于成功建立从数据连接VM到存储账户的连接：

```bash
# 使用本地元数据端点获取一个新的令牌。
# 如果您没有安装 jq，可以手动将 API 调用结果中的 access_token 键的值导出到 TOKEN 环境变量。
export TOKEN=`curl 'http://IP_ADDRESS_OF_VM/metadata/identity/oauth2/token?api-version=2018-02-01
&resource=https%3A%2F%2Fstorage.azure.com%2F' -H Metadata:true | jq '.access_token' | sed 's/"//g'`

# 确保令牌已正确设置；这应该是一个 OAuth2 令牌。例如 `eyJ0e...`（不带引号）。
echo $TOKEN

# 列出容器根目录的内容。
curl -XGET -H "x-ms-version: 2018-11-09" -H "Authorization: Bearer $TOKEN"
"https://STORAGE_ACCOUNT_NAME.dfs.core.windows.net/CONTAINER_NAME?resource=filesystem&recursive=false"

# 显示容器内某个文件的内容。
curl -XGET -H "x-ms-version: 2018-11-09" -H "Authorization: Bearer $TOKEN"
"https://STORAGE_ACCOUNT_NAME.dfs.core.windows.net/CONTAINER_NAME/path/to/file.txt"
```

### AADToken: HTTP连接获取AzureAD词元失败。HTTP响应：400 错误请求

对于`Azure托管身份`，此消息可能意味着用于从虚拟机检索词元的元数据端点存在问题。虚拟机本身可能处于不良状态，或者托管身份尚未附加到虚拟机上。要调试此问题，请尝试使用上面[部分](#confirm-that-a-managed-identity-flow-works-outside-the-data-connection-agent)中的cURL命令从虚拟机检索词元。

### 接收到HTML 504网关超时页面，起始<!DOCTYPE html>

如果页面包含文本`如需支持，请通过电子邮件联系我们...`，错误可能来自网络问题。确保代理在Foundry与安装代理的虚拟机之间，以及代理虚拟机与源之间正确配置。如果代理在界面中显示正常，并且您能够使用终端从虚拟机访问Azure上的文件，请提交问题以寻求额外帮助。

:::callout{theme="neutral"}
ABFS插件不管理代理设置，依赖于代理设置。
:::

### 此请求未被授权使用此资源类型执行此操作., 403, HEAD

此错误通常发生在生成的SAS词元权限不足时。尝试创建同步时，整个源的预览将如预期显示；然而，使用精简筛选的预览会导致错误。请参考[共享访问签名](#shared-access-signature)部分了解如何生成SAS词元。

### 导出文件位置使用Magritte文件系统

使用`export-abfs-task`时，如果文件被导出到`root/opt/palantir/magritte-bootvisor/var/data/processes/bootstrapper/`而不是指定的`directoryPath`，请确保目录URL的末尾有一个斜杠`/`。

例如：

```yaml
# Correct: 正确的配置
abfsRootDirectory: 'abfss://STORAGE_ACCOUNT_NAME.dfs.core.windows.net/'
# Incorrect: 错误的配置
abfsRootDirectory: 'abfss://STORAGE_ACCOUNT_NAME.blob.core.windows.net'
```

在Azure Data Lake Storage中，`abfss`协议应当使用`dfs.core.windows.net`，而不是`blob.core.windows.net`。
