---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/set-up-source/",
  "title": "设置数据源",
  "page_id": "set-up-source",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/oidc/",
  "next": "/zh/foundry/data-connection/source-exploration/",
  "scraped_at": "2026-07-13T05:30:37.342860+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 设置数据源

数据源是您连接到 Foundry 的任何外部数据。例如，数据源可以是 Postgres 数据库、S3 存储桶、Linux 服务器上的文件系统、SAP 实例或互联网上的 REST API。

从总体上看，以下是将数据源连接到 Foundry 所需的步骤。请注意，步骤 1 到步骤 3 可能需要您更改或验证现有架构中的配置：

1. [确保数据源和 Foundry 之间有有效的网络连接](#configure-network-access)。
2. [为 Foundry 提供有效的凭证](#provision-credentials)以进行数据源身份验证。
3. 如果数据源将通过代理访问，则确保代理具有访问数据源的[适当驱动程序](#add-drivers-if-needed)。
4. 最后，[在数据连接中创建数据源](#create-the-source-in-data-connection)。

一旦建立了这个数据源连接，您可以配置[同步](/zh/foundry/data-connection/set-up-sync/)以将特定的数据集导入 Foundry。同步可以完全通过数据连接 UI 配置，因此数据源设置是可能需要在您组织的环境中更新配置的最后任务，然后您才能在 Foundry 中访问您的数据。

## 配置网络访问

要将 Foundry 连接到数据源，首先验证网络连接。使用代理的数据源需要两个有效的网络连接：（1）从代理主机到数据源，（2）从代理主机到 Foundry。直接连接只需要一个有效的网络连接：从 Foundry 到数据源。

您需要确保在已设置在您网络中的代理和数据源之间有连接。代理充当从您网络到 Foundry 的单一验证入口，并将处理读取和发送数据到 Foundry VPC 的过程；对于每个新的数据源，您只需要确保代理和新数据源之间有有效连接。

:::callout{theme="neutral"}
您无需建立从数据源到 Foundry 的直接网络出口，因为流量只从代理流向 Foundry，并从代理流向数据源。[了解更多关于数据连接的架构。](/zh/foundry/data-connection/architecture/)
:::

建立此连接所需的步骤将根据您组织的网络设置而有所不同。无论您的具体设置如何，目标是使代理能够连接到数据源。这可能涉及到在代理主机上的出口设置配置、数据源上的入口设置、网络上的防火墙规则、代理上的代理设置、将数据源系统[证书](/zh/foundry/data-connection/agent-configuration-reference/#certificates)添加到代理信任库等。

如果您需要配置代理设置以使代理能够到达数据源，您可以通过[数据连接界面](/zh/foundry/data-connection/agent-configuration-reference/#proxy-configuration)进行设置。

## 提供凭证

在大多数情况下，Foundry 需要授权凭证（如用户名和密码）来访问数据源。最佳实践是使用专门为 Foundry 设立的服务账户。请注意，即使您有多个代理，也只需要一组凭证——凭证与 Foundry 中的特定数据源资源相关联，并将由您指派给该数据源的任何代理使用。

根据您组织为建立服务账户制定的任何内部指南和流程，为数据源提供服务账户。在继续下一步之前记下凭证。

## 添加驱动程序（如有需要）

[JDBC 数据源](/zh/foundry/available-connectors/custom-jdbc-sources/)可能需要添加连接到您的数据源所需的**驱动程序**。对于基于代理的数据源，您需要在代理设置页面中为您打算用于数据源连接的代理添加驱动程序。

[了解更多关于添加驱动程序的信息。](/zh/foundry/available-connectors/custom-jdbc-sources/#jdbc-drivers)

## 在数据连接中创建数据源

完成上述步骤后，您可以继续在数据连接中创建数据源：

* 登录后，使用[侧边栏](/zh/foundry/getting-started/orientation-and-nav/)导航到**数据连接**。
* 选择**数据源**选项卡。
* 在右上角选择**新建数据源**。
* 选择与您的数据源对应的[数据源类型](/zh/foundry/data-integration/source-type-overview/)。
* 选择**通过代理**，然后在右下角选择**继续**。

![create agent source](/resources/foundry/data-connection/create-agent-source.png)

### 将数据源保存到项目中

接下来，命名您的数据源并选择一个[项目](/zh/foundry/projects/overview/)放置在其中。我们通常建议为每个数据源创建一个新项目，因为这为从该数据源派生的数据集提供了最自然的权限方式。

您可以阅读更多关于[数据源权限最佳实践](/zh/foundry/data-connection/permissions/#source-best-practices)的信息，或查阅[如何在 Foundry 中端到端构建数据管道的完整指南](/zh/foundry/building-pipelines/recommended-project-structure/)。

选择右下角的**创建数据源并继续**。

### 配置数据源

添加有关如何连接到您的数据源的详细信息。这些将取决于您正在使用的[数据源类型](/zh/foundry/data-integration/source-type-overview/)，通常包括基本凭证，如连接 URL、云提供商区域等。

### 添加凭证

添加您之前[提供](#provision-credentials)的凭证以允许数据源连接到您的数据。

### 保存并继续

选择右下角的**保存**以完成数据源的设置。一旦您的数据源完全设置，您可以继续[设置同步](/zh/foundry/data-connection/set-up-sync/)以将数据导入 Foundry。

### 故障排除

如果数据源不能正常工作，请检查以下内容：

1. 确保代理正常运行（如果使用代理）。
2. 登录到代理的主机并确认可以独立于 Foundry 建立到数据源的连接。
3. 检查代理主机上的日志文件，按建议检查[同步失败](/zh/foundry/data-connection/syncs-troubleshooting/#intermittent-sync-failures-or-hangs)。
