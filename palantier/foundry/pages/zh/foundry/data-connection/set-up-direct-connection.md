---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/set-up-direct-connection/",
  "title": "设置直接连接",
  "page_id": "set-up-direct-connection",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/faq/",
  "next": "/zh/foundry/data-connection/set-up-agent/",
  "scraped_at": "2026-07-13T05:30:35.509830+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 设置直接连接

:::callout{theme="warning"}
直接连接依赖于Foundry的容器基础设施，该基础设施仅在Foundry托管的SaaS平台中可用。因此，基于云的直接连接在您的环境中可能不可用。
:::

如果您尝试连接到通过互联网访问的数据源，例如REST API、SFTP服务器或Azure存储帐户，您可以配置直接连接以避免需要[设置代理](/zh/foundry/data-connection/set-up-agent/)。使用直接连接有很多优点：

* 无需配置和管理代理及其主机
* 避免通过您的网络路由互联网到Foundry
* 提供卓越的正常运行时间和性能，因为基于云的同步不依赖于代理软件包或其主机

如果您有兴趣配置基于云的直接连接，请按照以下步骤操作：

1. [为您的注册配置网络出口策略](#configure-a-network-policy)。
2. [提供凭据](#provision-credentials)以连接到您的数据源。
3. [在数据连接中创建来源](#create-the-source-in-data-connection)。

## 配置网络策略

目前，Palantir托管的SaaS平台与外部域之间的网络出口受允许列表限制。要启用对您希望连接的域的出口，请与您的Palantir代表联系，并提供以下详细信息：

* 您的目标数据源的描述
* 有关如何连接到数据源的网络详细信息
  * 如果您通过HTTP(S)连接，您的数据源的DNS主机名
  * 如果您需要使用非HTTP协议，应允许的[CIDR ↗](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)地址和端口

Palantir将审核您的请求并适当地设置出口。

我们正在积极努力实现自助服务出口创建，消除与您的Palantir代表联系的需要。

:::callout{theme="warning"}
您必须在您的[注册](/zh/foundry/administration/enrollments-and-organizations/)中拥有*信息安全官*角色才能配置网络出口。如果您没有权限配置出口，请联系您的Palantir代表以获取帮助。

*信息安全官*角色可以在[控制面板](/zh/foundry/administration/control-panel/)的注册权限部分找到。管理员需要拥有*注册管理员*角色才能查看此部分。
:::

要配置网络策略，请使用[工作区侧边栏](/zh/foundry/getting-started/orientation-and-nav/#the-sidebar)中的**其他工作区**链接导航到控制面板。在控制面板中，选择侧边栏中的**网络出口**。如果您看不到此选项，请联系您的Palantir代表以完成以下步骤。

![create network policy](../../../images/foundry/data-connection/create-network-policy.png)

通过选择**添加网络策略**添加网络策略。添加描述和连接详细信息，类似于您联系Palantir时提供的详细信息：

* 如果您通过HTTP(S)连接，添加您的数据源的DNS主机名
* 如果您需要使用非HTTP协议，添加CIDR地址和端口

保持默认的**非必填**策略类型选择，然后选择**添加网络策略**。

## 提供凭据

在大多数情况下，Foundry将需要授权凭据（如用户名和密码）来访问来源。最佳实践是专门为Foundry使用一个服务帐户。

根据您的组织为建立服务帐户而制定的任何内部指南和流程，为来源提供一个服务帐户。在继续下一步之前记录凭据。

## 在数据连接中创建来源

完成上述步骤后，您可以继续在数据连接中创建来源：

* 登录后，使用[侧边栏](/zh/foundry/getting-started/orientation-and-nav/)导航到**数据连接**。
* 选择**来源**选项卡。
* 在右上角选择**新来源**。
* 选择与您的数据源对应的[来源类型](/zh/foundry/data-integration/source-type-overview/)。
* 选择**直接连接**，然后在右下角选择**继续**。

![Create direct connection](../../../images/foundry/data-connection/create-direct-connection.png)

### 将来源保存到项目中

接下来，为您的来源命名并选择一个[项目](/zh/foundry/projects/overview/)来放置它。我们通常建议为每个来源创建一个新项目，因为这为来源生成的数据集提供了最清晰的权限方式。有关更多信息，请参阅[来源权限最佳实践](/zh/foundry/data-connection/permissions/#source-best-practices)。关于如何在Foundry中端到端构建数据管道的完整指南，请参阅[推荐的项目结构文档](/zh/foundry/building-pipelines/recommended-project-structure/)。

选择右下角的**创建来源并继续**。

### 选择您的网络策略

在下一页，选择您[先前配置的](#configure-a-network-policy)网络策略，点击**使用现有策略**并搜索策略名称。

![Use existing policy for direct connection](../../../images/foundry/data-connection/use-existing-policy.png)
![select network policy](../../../images/foundry/data-connection/select-network-policy.png)

### 配置来源并添加驱动程序

添加有关如何连接到来源的详细信息。这些详细信息将取决于您使用的[来源类型](/zh/foundry/data-integration/source-type-overview/)，通常包括连接URL、云提供商区域等基本凭据。

[JDBC来源](/zh/foundry/available-connectors/custom-jdbc-sources/)可能需要添加和选择连接到来源所需的**驱动程序**。虽然Foundry自带许多驱动程序，但您可能需要上传和选择一个驱动程序才能继续。

### 添加凭据

添加您先前[提供的](#provision-credentials)凭据，以允许直接连接到您的数据。

### 保存并继续

选择右下角的**保存**以完成设置直接连接。一旦您的来源完全设置好，您可以继续[设置同步](/zh/foundry/data-connection/set-up-sync/)以将数据带入Foundry。
