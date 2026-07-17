---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/microsoft-sql-server/",
  "title": "Microsoft SQL Server",
  "page_id": "microsoft-sql-server",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/microsoft-project/",
  "next": "/zh/foundry/available-connectors/microsoft-teams/",
  "scraped_at": "2026-07-13T05:36:34.769997+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Microsoft SQL Server

连接Foundry到Microsoft SQL Server，以便在SQL Server数据库和Foundry之间读取和同步数据。

## 支持的功能

| 功能 | 状态 |
| --- |--- |
| 探索 | 🟢 普遍可用 |
| 批量同步 | 🟢 普遍可用 |
| 增量 | 🟢 普遍可用 |
| 更改数据捕获同步 | 🟢 普遍可用 |

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序，并在屏幕右上角选择\*\*+ 新建源\*\*。
2. 从可用的连接器类型中选择**MS SQL Server**。
3. 选择通过互联网使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)或通过[代理运行时](/zh/foundry/data-connection/set-up-agent/)连接。
4. 按照下面各部分中的信息继续设置连接器的其他配置提示。

了解更多关于在Foundry中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

## 认证

您可以通过以下方式与SQL Server进行认证：

1. **用户名和密码**：提供用户名和密码。我们建议使用服务凭证而不是个人用户凭证。
2. **Active Directory Msi**\*：此选项将使用`authentication=ActiveDirectoryMSI` JDBC设置。可以非必填提供一个`msiClientId`。
3. **Active Directory Password**\*：此选项将使用`authentication=ActiveDirectoryPassword` JDBC设置。必须提供Active Directory用户的用户名和密码以使用此设置。
4. **Active Directory Service Principal**\*：此选项将使用`authentication=ActiveDirectoryServicePrincipal` JDBC设置。必须指定一个主体ID（有时称为应用程序或客户端ID），以及该主体ID的密钥。

有关这些认证模式的更多信息，请参阅[官方文档 ↗](https://learn.microsoft.com/sql/connect/jdbc/connecting-using-azure-active-directory-authentication)。对于所有认证选项，请确保所提供的用户和角色在目标数据库上具有必要的权限，以及读取或写入目标表的权限。

\* 请注意，Azure Active Directory现已更名为[Microsoft Entra ID ↗](https://www.microsoft.com/security/business/identity-access/microsoft-entra-id)；然而，微软发布的SQL Server驱动程序上的JDBC选项仍保留原始名称，指的是Active Directory。

## 网络

Microsoft SQL Server连接器需要访问您希望连接的SQL Server实例的网络。SQL Server连接通常使用主机名连接到端口1433。

为了启用从Foundry直接连接到SQL Server，在[数据连接应用程序](/zh/foundry/data-connection/overview/)中设置源时，必须添加适当的[出口策略](/zh/foundry/administration/configure-egress/)。

对于托管在像Azure SQL或AWS RDS这样的云服务上的SQL Server实例，您必须为从云提供商的控制台检索到的主机名添加出口策略。

:::callout{theme="warning"}
如果使用Azure重定向模式，则必须为所有解析的IP地址添加出口策略。解析的IP可能会偶尔更改，您必须更新出口策略以允许新的IP。如果您的SQL Server实例托管在Azure上，例如，您可以在[Azure SQL文档 ↗](https://learn.microsoft.com/azure/azure-sql/managed-instance/connectivity-architecture-overview?view=azuresql\&tabs=current#public-endpoint)中找到有关Azure SQL实例公共IP地址的更多信息。
:::

* 要查找您的Azure SQL实例的主机名，请导航到Azure门户中的**设置 > 属性**页面，并查找**服务器名称**字段。Azure SQL的一个基于主机名的出口策略示例：`<your-database-name>.database.windows.net (port 1433)`
* 要查找解析的IP，您可以从命令行运行`nslookup <your-database-name>.database.windows.net`。最终结果将是此主机名在Azure中解析到的IP地址。以下是一个基于IPv4的Azure SQL出口策略示例：`x.x.x.x (port 1433)`。Azure SQL在多个主机之间进行负载平衡，因此您可能需要多次运行`nslookup`命令，并添加所有解析的IP地址。

:::callout{theme="neutral"}
如果您从托管在Azure中的Foundry实例连接到Azure SQL实例，您将需要使用**代理**连接策略选项。对于源自Azure内部的流量，连接策略默认为**重定向**。使用重定向选项进行Azure-Azure连接将需要为所有Azure SQL IP地址在11000到11999范围内的所有端口配置出口策略。这是可能的，但不推荐，因为它过于宽松。有关Azure SQL连接策略的详细信息，请参阅官方[Azure SQL文档 ↗](https://learn.microsoft.com/azure/azure-sql/database/connectivity-architecture?view=azuresql#connection-policy)。
:::

如果您使用代理运行时连接，您必须确保代理主机开放防火墙，以连接到您的MS SQL Server数据库所需的主机名、IP地址和端口。

## 连接详情

| 选项 | 必需？ | 描述 |
| --- | --- | --- |
| `Host type` | 是 | 指定Foundry如何与您的SQL Server数据库连接。<br /><br /> **选项1：主机名** <br />提供一个主机名。这是所有SQL Server连接的推荐选项，并且在连接到[Azure SQL ↗](https://azure.microsoft.com/products/azure-sql)实例时应始终使用。<br /><br /> **选项2：IPv4** <br />提供一个IPv4地址。如果您通常在公司网络内或通过互联网使用IPv4地址连接，可以使用此选项。<br /><br /> **选项3：IPv6** <br />提供一个IPv6地址。如果您通常使用IPv6地址连接，请使用此选项。 |
| `Port` | 是 | 指定连接时使用的端口。大多数SQL Server实例的默认端口是`1433`。有关端口的更多信息，请参阅您正在连接的SQL Server版本的官方文档。 |
| `Database name` | 是 | 您在MS SQL Server实例中连接的数据库名称。 |
| `Authentication` | 是 | 按照上面的[认证](#authentication)指导进行配置。 |
| `Require encryption` | 是 | 默认为启用。有关更多详细信息，请参阅Microsoft关于SQL Server JDBC驱动程序上的`encrypt`设置的文档：<br /><br /> [连接属性参考 ↗](https://learn.microsoft.com/sql/connect/jdbc/setting-the-connection-properties?view=sql-server-ver16)<br /> [加密支持示例 ↗](https://learn.microsoft.com/sql/connect/jdbc/understanding-ssl-support?view=sql-server-ver16) |
| `Trust server certificate` | 是 | 默认为禁用。有关更多详细信息，请参阅Microsoft关于SQL Server JDBC驱动程序上的`trustServerCertificate`设置的文档：<br /><br /> [连接属性参考 ↗](https://learn.microsoft.com/sql/connect/jdbc/setting-the-connection-properties?view=sql-server-ver16) |
| `Network Connectivity` | 是 | 您必须提供一个与您的MS SQL Server实例联网的运行时。对于公司防火墙后的实例，您通常需要使用代理运行时。对于云托管的实例，请参考[网络](#networking)部分以获取更多详细信息。 |

## 更改数据捕获

Microsoft SQL Server源支持[更改数据捕获](/zh/foundry/data-integration/change-data-capture/)同步。

要启用Microsoft SQL Server的更改数据捕获，您必须运行如下命令以在数据库上启用CDC。

```sql
USE <database> -- 使用目标数据库
GO
EXEC sys.sp_cdc_enable_db -- 启用数据库的更改数据捕获（Change Data Capture）
GO
```

然后，在每个应该记录更改日志的表上运行另一个命令：

```sql
EXEC sys.sp_cdc_enable_table
    @source_schema = N'<schema>'  -- 源表的架构名称
  , @source_name = N'<table_name>'  -- 源表的名称
  , @role_name = NULL  -- 用于访问更改数据捕获（CDC）数据的角色名称，NULL表示使用默认角色
  , @capture_instance = NULL  -- 捕获实例的名称，NULL表示使用默认实例名
  , @supports_net_changes = 0  -- 指定是否支持净更改，0表示不支持
  , @filegroup_name = N'PRIMARY';  -- 存储CDC对象的文件组名称
GO
```

上述代码用于启用SQL Server中的更改数据捕获（Change Data Capture, CDC）功能。CDC用于跟踪表中的更改，便于数据同步和审核。
一旦为您希望同步到Foundry的表启用了更改数据捕获，您可以导航到**概览**页面并选择\*\*+ 创建CDC同步\*\*以开始创建新的更改数据捕获同步。

:::callout{theme="neutral"}
探索运行时必须正常工作才能创建更改数据捕获同步。如果运行时仍在初始化，您可能需要等待几秒钟并刷新页面以继续创建更改数据捕获同步。
:::

有关这些命令和在Microsoft SQL Server中使用更改数据捕获（CDC）的更多信息，请参阅所使用版本的SQL Server的[官方文档 ↗](https://learn.microsoft.com/azure/azure-sql/database/change-data-capture-overview)。
