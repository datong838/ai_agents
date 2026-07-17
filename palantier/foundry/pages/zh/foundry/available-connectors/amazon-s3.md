---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/amazon-s3/",
  "title": "Amazon S3",
  "page_id": "amazon-s3",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/amazon-marketplace/",
  "next": "/zh/foundry/available-connectors/apache-couchdb/",
  "scraped_at": "2026-07-13T05:34:50.505010+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Amazon S3

将Foundry连接到AWS S3，以读取和同步S3与Foundry之间的数据。

## 支持的功能

| 功能  | 状态 |
|--- |--- |
| 探索 | 🟢 通用可用 |
| 批量导入 | 🟢 通用可用 |
| 增量 | 🟢 支持的文件格式通用可用 |
| 媒体集 | 🟢 通用可用 |
| [虚拟表](/zh/foundry/data-integration/virtual-tables/) | 🟢 通用可用 |
| [文件导出](/zh/foundry/data-connection/export-overview/#file-exports) | 🟢 通用可用 |

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序，并在屏幕右上角选择\*\*+ 新来源\*\*。
2. 从可用的连接器类型中选择**S3**。
3. 选择使用通过互联网的[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)或通过[中介代理](/zh/foundry/data-connection/set-up-agent/)连接。
4. 按照下面各节中的信息，遵循附加的配置提示以继续设置您的连接器。

了解更多有关在Foundry中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

## 连接详情

| 选项 | 必须吗？ | 描述 |
| --- | --- | --- |
| `URL` | 是 | S3桶的URL。数据连接支持s3a协议。应包含结尾斜杠。有关更多详细信息，请参阅AWS的[官方文档 ↗](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-bucket-intro.html#accessing-a-bucket-using-S3-format)。<br />例如：`s3://bucket-name/` |
| `Endpoint` | 是 | 用于访问S3的端点。<br />例如：`s3.amazonaws.com` 或 `s3.us-east-1.amazonaws.com` |
| `Region` | 否 | 配置AWS服务时使用的AWS区域。当使用STS角色时，这是必需的。警告：同时提供区域和包含区域的S3端点可能会导致失败。<br />例如：`us-east-1` 或 `eu-central-1` |
| `Network connectivity` | 是 - 仅适用于直接连接 | **步骤1: Foundry出口策略**<br />为桶附加一个Foundry [出口策略](/zh/foundry/administration/configure-egress/#network-egress-policies)，以允许Foundry出口到S3。数据连接应用程序根据提供的连接详细信息建议适当的出口策略。<br />例如：`bucket-name.s3.us-east-1.amazonaws.com (Port 443)` <br /><br /> **步骤2: AWS桶策略**<br />此外，您需要将相关的Foundry IP和/或桶详细信息列入白名单，以便从S3访问。您的Foundry IP详细信息可以在[控制面板应用程序](/zh/foundry/administration/control-panel/)的`网络出口`下找到。有关如何在S3中配置桶策略的更多详细信息，请参阅[官方AWS文档 ↗](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html#example-bucket-policies-IP)。<br /><br />*注意：设置与您的Foundry注册在同一区域托管的S3桶的访问需要额外的配置。阅读更多关于这些要求的信息，请参阅[网络出口文档](/zh/foundry/administration/configure-egress/#amazon-s3-bucket-policies)。*|
| `Client certificates & private key` | 否 | 客户端证书和私钥可能是必需的，也可能不是，用于保护连接。|
| `Server certificates` | 否 | 服务器证书可能是必需的，也可能不是，用于保护连接。|
| `Credentials` | 是 | **选项1: 访问密钥和密钥**<br/>提供用于连接S3的访问密钥ID和密钥。<br/> 可以通过在您的AWS账户中为Foundry创建一个新的IAM用户来生成凭证，并授予该IAM用户对S3桶的访问权限。<br/><br/> **选项2: OpenID Connect (OIDC)**<br/> 按照显示的源系统配置说明设置OIDC。有关OpenID Connect的详细信息，请参阅官方[AWS文档 ↗](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)和[我们的文档](/zh/foundry/data-connection/oidc/)以了解OIDC如何与Foundry一起工作。<br/><br/> 有关创建AWS IAM用户的更多详细信息，请参阅官方[AWS文档 ↗](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html)。查看[我们的S3文档权限](#required-permissions-for-s3)以了解Foundry期望用户具备的AWS权限。|
| `STS role` | 否 | S3连接器可以选择性地假定[安全令牌服务(STS)角色 ↗](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html)以连接到S3。有关更多详细信息，请参阅[STS角色配置](#sts-role-configuration)。|
| `Connection timeout` | 否 | 在最初建立连接时等待的时间（以毫秒为单位），在放弃和超时之前。<br /> 默认：`50000` |
| `Socket timeout` | 否 | 在已建立的开放连接上传输数据时等待的时间（以毫秒为单位），在连接超时并关闭之前。<br /> 默认：`50000` |
| `Max connections` | 否 | 允许的最大开放HTTP连接数。<br /> 默认：`50` |
| `Max error retries` | 否 | 失败的可重试请求（例如：来自服务的5xx错误响应）的最大重试次数。<br /> 默认：`3`|
| `Client KMS key` | 否 | 使用AWS SDK执行客户端数据加密的KMS密钥名称或别名。在PCloud中使用此选项需要代理更改。|
| `Client KMS region` | 否 | 用于KMS客户端的AWS区域。仅在提供AWS KMS密钥时相关。|
| `Match subfolder exactly` | 否 | 可选地将子文件夹下指定的路径与S3中的确切子文件夹匹配。如果设置为false，则`s3://bucket-name/foo/bar/`和`s3://bucket-name/foo/bar_baz/`都将与子文件夹设置`foo/bar/`匹配。|
| `Proxy configurations` | 是 - 仅适用于基于代理的连接 | 配置S3的代理设置。<br />*注意：如果(a)您的Foundry注册托管在AWS中，(b)您连接到的S3桶托管在与您的Foundry注册不同的AWS区域，并且(c)您通过数据连接代理进行连接，则这是必需的。有关更多详细信息，请参阅[S3代理配置](#s3-proxy-configuration-agent-based-connections)。* |
| `Enable path style access` | 否 | 使用路径样式访问URL（例如，`https://s3.region-code.amazonaws.com/bucket-name/key-name`）而不是虚拟托管样式访问URL（例如，`https://bucket-name.s3.region-code.amazonaws.com/key-name`）。有关更多详细信息，请参阅[官方AWS文档 ↗](https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html)。|
| `Catalog` | 否 | 配置此S3桶中存储的表的目录。有关更多详细信息，请参阅[虚拟表](#virtual-tables)。|

## S3的必需读取和同步权限

以下AWS权限是S3桶交互式探索所必需的：

```json
{
    "Action": ["s3:ListBucket"], // 操作：列出S3存储桶中的对象
    "Resource": ["arn:aws:s3:::path/to/bucket"], // 资源：指定存储桶的ARN（Amazon资源名称）
    "Effect": "Allow", // 效果：允许执行指定的操作
}
```

以下AWS权限是从S3进行批量同步、虚拟表和媒体同步所需的：

```json
{
    "Action": ["s3:GetObject"],  // 指定的动作是从S3中获取对象
    "Resource": ["arn:aws:s3:::path/to/bucket/*"],  // 指定的资源是S3桶中的路径
    "Effect": "Allow",  // 允许上述动作的效果
}
```

请参阅 [关于 Amazon S3 中策略和权限的官方 AWS 文档 ↗](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html)，了解有关如何在 S3 中配置桶策略的更多详细信息。

## S3 代理配置（基于代理的连接）

使用数据连接代理连接到 S3 时，可以通过两种方式定义代理设置：

* 源配置：直接在源配置中定义每个代理设置，如下表所述。
* 代理的系统属性：作为后备，您可以在代理的系统属性中配置代理设置。为此，请在代理的高级配置设置中包含适当的 JVM 参数（例如，`-Dhttps.proxyHost=example.proxy.com`）。

| 参数  | 必填？ | 默认值 | 描述 |
|--- |--- |--- |--- |
| `host` | Y | | HTTP 代理主机（无方案）。 |
| `port` | Y | | HTTP 代理的端口。 |
| `protocol` | N | `HTTPS` | 使用的协议。可以是 `HTTPS` 或 `HTTP`。 |
| `nonProxyHosts` | N | | 不应使用代理的主机名列表（或通配符域名）。例如：`*.s3-external-1.amazonaws.com|*.example.com`。 |
| `credentials` | N |  | 如果您的代理需要基本 HTTP 身份验证（由 [HTTP 407 响应 ↗](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.34) 触发），请包含此块。 |
| `credentials.username` | N | | HTTP 代理的明文用户名。 |
| `credentials.password` | N | | HTTP 代理的加密密码。 |

## STS 角色配置

STS 角色配置允许您使用 [AWS Security Token Service ↗](https://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html) 在从 S3 读取时假设一个角色。

| 参数  | 必填？ | 默认值 | 描述 |
|--- |--- |--- |--- |
| `roleArn` | Y | | STS 角色 ARN 名称。 |
| `roleSessionName` | Y | | 假设此角色时使用的会话名称。 |
| `roleSessionDuration` | N | 3600 秒 | 会话持续时间。 |
| `externalId` | N | | 假设角色时使用的外部 ID。 |

## 云身份配置

云身份认证允许 Foundry 访问您 AWS 实例中的资源。云身份在控制面板的[注册](/zh/foundry/administration/enrollments-and-organizations/)级别进行配置和管理。了解如何[配置云身份](/zh/foundry/administration/configure-cloud-identities/)。

![具有云身份的 S3 源](../../../images/foundry/available-connectors/s3-source-with-cloud-identity.png)

使用云身份认证时，角色 ARN 将显示在凭证部分。选择 `Cloud identity` 凭证选项后，还必须配置以下内容：

1. 在目标 Amazon AWS 账户中配置一个身份和访问管理 (IAM) 角色。
2. 授予 IAM 角色访问您希望连接的 S3 桶的权限。您通常可以使用 [桶策略 ↗](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html) 来实现这一点。
3. 在 S3 源配置详细信息中，在 [Security Token Service (STS) 角色 ↗](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) 配置下添加 IAM 角色。在访问 S3 时，Foundry 中的云身份 IAM 角色将尝试假设 [AWS 账户 IAM 角色 ↗](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)。
4. [配置相应的信任策略 ↗](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-managingrole_edit-trust-policy)，以允许云身份 IAM 角色假设目标 AWS 账户 IAM 角色。

## 虚拟表

本节提供有关使用来自 S3 源的[虚拟表](/zh/foundry/data-integration/virtual-tables/)的更多详细信息。在同步到 Foundry 数据集时，本节不适用。

| 虚拟表功能 | 状态 |
| --- | --- |
| 源格式 | 🟢 普遍可用：[Avro ↗](https://avro.apache.org/)、[Delta ↗](https://docs.delta.io/latest/)、[Iceberg ↗](https://iceberg.apache.org/)、[Parquet ↗](https://parquet.apache.org/) |
| 手动注册 | 🟢 普遍可用 |
| 自动注册 | 🔴 不可用 |
| 下推计算 | 🔴 不可用 |
| 增量管道支持 | 🟢 Delta 表普遍可用：仅限 `APPEND`（[详情](#delta)）<br /> 🟢 Iceberg 表普遍可用：仅限 `APPEND`（[详情](#iceberg)）<br /> 🔴 Parquet 表不可用 |

注册[虚拟表](/zh/foundry/data-integration/virtual-tables/)时，请记住以下源配置要求：

* 您必须将源设置为[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)。虚拟表不支持使用[中介代理](/zh/foundry/data-connection/set-up-agent/)。
* 确保已根据[连接详细信息](#connection-details)中的**网络连接**部分建立双向连接和白名单。
* 如果在代码库中使用虚拟表，请参阅[虚拟表文档](/zh/foundry/data-integration/virtual-tables/#virtual-tables-in-code-repositories)以获取所需的其他源配置详细信息。
* 如果您的桶包含 `.`，您必须启用路径样式访问并设置适当的出口策略。

请参阅上述[连接详细信息](#connection-details)部分以获取更多详细信息。

### Delta

要启用由虚拟表支持的管道的增量支持，请确保在源 Delta 表上启用了[更改数据馈送 ↗](https://docs.databricks.com/en/delta/delta-change-data-feed.html#enable-change-data-feed)。在[Python 变换](/zh/foundry/transforms-python/incremental-reference/#incrementaltransforminput)中支持 `current` 和 `added` 读取模式。`_change_type`、`_commit_version` 和 `_commit_timestamp` 列将在 Python 变换中可用。

### Iceberg

需要 Iceberg 目录来加载由 Apache Iceberg 表支持的虚拟表。要了解有关 Iceberg 目录的更多信息，请参阅 [Apache Iceberg 文档 ↗](https://iceberg.apache.org/concepts/catalog/)。在源上注册的所有 Iceberg 表都必须使用相同的 Iceberg 目录。

默认情况下，表将使用 S3 中的 Iceberg 元数据文件创建。在注册表时，必须提供指示这些元数据文件位置的 `warehousePath`。

[AWS Glue ↗](https://aws.amazon.com/glue/) 可以用作存储在 S3 中的表的 Iceberg 目录。要了解有关此集成的更多信息，请参阅 [AWS Glue 文档 ↗](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-iceberg.html)。在源上配置的凭证必须有权访问您的 AWS Glue 数据目录。AWS Glue 可以在源上的[连接详细信息](#connection-details)选项卡中进行配置。在此源上注册的所有 Iceberg 表将自动使用 AWS Glue 作为目录。表应使用 `database_name.table_name` 命名模式注册。

[Unity Catalog ↗](https://www.databricks.com/product/unity-catalog) 可以在 Databricks 中使用 Delta Universal Format (UniForm) 时用作 Iceberg 目录。要了解有关此集成的更多信息，请参阅 [Databricks 文档 ↗](https://docs.databricks.com/en/delta/uniform.html)。与 AWS Glue 一样，可以在源上的[连接详细信息](#connection-details)选项卡中配置目录。您需要提供端点和[个人访问词元](https://docs.databricks.com/en/dev-tools/auth/pat.html)以连接到 Unity Catalog。表应使用 `catalog_name.schema_name.table_name` 命名模式注册。

![虚拟表 S3 目录](../../../images/foundry/available-connectors/virtual_tables_s3_catalog.png)

增量支持依赖于 Iceberg [增量读取 ↗](https://iceberg.apache.org/docs/1.5.1/spark-queries/#incremental-read)，目前仅支持追加。支持在[Python 变换](/zh/foundry/transforms-python/incremental-reference/#incrementaltransforminput)中的 `current` 和 `added` 读取模式。

### Parquet

使用 Parquet 的虚拟表依赖于模式推断。最多将使用 100 个文件来确定模式。

## 以 S3 格式导出数据

要导出到 S3，首先为您的 S3 连接器[启用导出](/zh/foundry/data-connection/export-overview/#enable-exports-for-source)。然后，[创建一个新的导出](/zh/foundry/data-connection/export-overview/#creating-a-new-export)。

## S3 所需的导出权限

导出数据到 S3 需要以下 AWS 权限：

```json
{
    "Action": ["s3:PutObject"], // 指定允许执行的操作，这里是将对象上传到 S3 存储桶中
    "Resource": ["arn:aws:s3:::path/to/bucket/*"], // 指定可以操作的资源，这里是特定存储桶路径下的所有对象
    "Effect": "Allow", // 指定策略的效果，这里是允许执行指定的操作
}
```

请参阅 [AWS 官方文档关于 Amazon S3 中的策略和权限 ↗](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html)，以获取有关如何配置 S3 中存储桶策略的更多详细信息。

### 以配置导出选项

| 选项  | 必填？ | 默认值 | 描述 |
|--- |--- |--- |--- |
| `Path Prefix` | 否 | N/A | 应用于导出文件的路径前缀。导出文件的完整路径计算为 `s3://<bucket-name>/<path-in-source-config>/<path-prefix>/<exported-file>` |
| `Canned ACL` | 否 | N/A | 设置附加到上传文件的 AWS 访问控制列表 (ACL)，使用其中一个预设的 ACL。有关每个 ACL 的描述，请参阅 [AWS 文档 ↗](https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl)。 |
