---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/netsuite-suiteanalytics/",
  "title": "Oracle NetSuite SuiteAnalytics",
  "page_id": "netsuite-suiteanalytics",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/netsuite-overview/",
  "next": "/zh/foundry/available-connectors/netsuite-suiteql-jdbc/",
  "scraped_at": "2026-07-13T05:37:10.180848+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Oracle NetSuite SuiteAnalytics

通过SuiteAnalytics Connect将Foundry连接到Oracle NetSuite，以将数据从您的NetSuite ERP同步到Foundry。

:::callout{theme="note"}
需要在您的NetSuite实例上启用SuiteAnalytics。请参阅[NetSuite文档 ↗](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_3996274388.html#To-enable-the-Connect-Service-feature%3A)以启用它。
:::

## 支持的功能

| 功能 | 状态 |
| --- |--- |
| 探索 | 🟢 一般可用 |
| 批量同步 | 🟢 一般可用 |
| 增量 | 🟢 一般可用 |

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序并在屏幕右上角选择\*\*+ 新来源\*\*。
2. 从可用的连接器类型中选择**JDBC**。
3. 选择使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)通过互联网连接，或者通过[代理运行时连接](/zh/foundry/data-connection/set-up-agent/)。
4. 按照下列部分中的信息继续进行连接器的附加配置提示。

了解更多关于在Foundry中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

## 认证

您可以使用**用户名/密码**组合进行SuiteAnalytics认证。我们建议使用服务用户凭据而不是个人用户凭据。

### 在NetSuite中配置用户角色和权限

在NetSuite中，为控制访问，每个用户被指派一个或多个角色，每个角色是定义用户可以执行哪些任务和可以访问哪些数据的权限集合。我们建议为将连接到Foundry的用户进行以下配置：

1. 创建一个具有适当权限的专用角色。
   1. 从NetSuite的工具栏中选择**设置** > **用户/角色** > **管理角色** > **新建**，并为角色提供一个明确的名称。我们建议使用`foundry-role`。
   2. 通过导航到角色页面底部并选择**权限** > **设置**，为角色添加系统范围的权限。选择**SuiteAnalytics Connect**，选择**添加**然后**保存**。
      * *注意：NetSuite文档建议添加**SuiteAnalytics Connect: Read All**权限，但对于NetSuite2.com数据源是无关的（参见[详情 ↗](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_3998867068.html#bridgehead_1539708454)）。添加此权限不会有任何效果。*
   3. 通过导航到角色页面底部并选择**权限** > **列表**，为角色添加您希望能够从Foundry查询的表的权限。选择您想要的表，选择**添加**然后**保存**。
2. 将新角色指派给用户。
   1. 从NetSuite的工具栏中选择**设置** > **用户/角色** > **管理用户**。选择您希望用于连接到Foundry的用户，然后选择**编辑**。
   2. 导航到**访问**选项卡，并确保选中**给予访问**复选框。
   3. 在**角色**选项卡中，从下拉列表中选择新创建的角色（`foundry-role`），选择**添加**然后**保存**。
      * *注意：NetSuite文档建议使用**数据仓库集成器**角色代替自定义角色。然而，此角色需要使用基于词元认证的访问（参见[更多详情 ↗](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_3998867068.html#subsect_162885566786)），这在Foundry中不可用。*

为了验证您是否添加了正确的权限，请以您已分配新角色的用户身份登录，并检查您是否可以查看所有预期的数据。

## 网络连接

SuiteAnalytics连接器需要网络访问您希望连接到的NetSuite Connect实例。

### 选项1：直接连接

如果您是通过[直接连接](/zh/foundry/data-connection/core-concepts/#direct-connections)进行连接，则在设置来源时必须添加适当的[出口政策](/zh/foundry/administration/configure-egress/)。

需要允许的**服务主机**和**端口**可以在**NetSuite的配置主页**上找到，网址为`https://<YOUR_ACCOUNT_ID>.app.netsuite.com/app/external/odbc/suiteAnalyticsConnectDownload.nl`。
要在没有您的NetSuite账户ID的情况下访问此页面：

1. 登录到您的NetSuite账户主页。
2. 找到左下角的**设置**面板并选择**设置SuiteAnalytics Connect**。

**服务主机**通常的形式为\*\*\<ACCOUNT\_ID>.connect.api.netsuite.com\*\*，端口为**1708**。

如果不存在这样的出口政策，您可以[请求一个新的](/zh/foundry/data-connection/set-up-direct-connection/#configure-a-network-policy)；否则您可以[添加它](/zh/foundry/data-connection/set-up-direct-connection/#choose-your-network-policy)。

:::callout{theme="warning"}
由于这是使用非HTTPS协议，您需要添加：

* 一个按名称引用您服务主机的DNS政策，以及
* 一个明确引用IP范围的CIDR政策。您可以通过在终端中运行`nslookup you-service-host`来获取NetSuite实例的IP范围。NetSuite服务的IP地址可能会随时更改，且无事先通知。
:::

### 选项2：代理连接

如果您是使用代理运行时进行连接，您必须确保代理主机已打开连接到您的NetSuite Connect实例所需的主机名、IP地址和端口的防火墙。

## 连接详情

| 选项 | 必需？ | 描述 |
| --- | --- | --- |
| `URL` | 是 | 形式为`jdbc:ns://<SERVICE_HOST>:<SERVICE_PORT>`，其中`SERVICE_HOST`和`SERVICE_PORT`可以从[NetSuite的配置主页](#option-1-direct-connection)检索。通常的形式为\*\*`jdbc:ns://<ACCOUNT_ID>.connect.api.netsuite.com:1708`**|
| `Driver class` | 是 | 需要是**com.netsuite.jdbc.openaccess.OpenAccessDriver\*\* |
| `Drivers` | 是 | **(选项1)** 对于[直接连接](/zh/foundry/data-connection/core-concepts/#direct-connections)，上传您可以从[NetSuite的配置主页](#option-1-direct-connection)下载的最新JDBC驱动程序。<br /><br />**(选项2)** 对于[代理连接](/zh/foundry/data-connection/core-concepts/#agent-based-sources)，与**选项1**相同的JDBC驱动程序需要正确签署以便上传到代理。请联系您的Palantir代表以进行此操作。参见如何[将驱动程序添加到代理](/zh/foundry/available-connectors/custom-jdbc-sources/#jdbc-drivers)以获取更多详情。|
| `Credentials` | 是 | 用于连接到Foundry的用户的**用户名**和**密码**。|
| `JDBC properties` | 是 | 可用属性的完整列表在[此处 ↗](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4425626714.html#Connection-Properties)描述。以下属性是强制性的：<br /><br />  - **CustomProperties** : `(AccountID=<ACCOUNT_ID>;RoleID=<ROLE_ID>)` <br />\* **ROLE\_ID**是您分配给用户的角色（`foundry-role`）的内部ID。您可以在**设置** > **用户/角色** > **管理角色**页面上找到此值。如果未显示内部ID，请参见[如何启用它 ↗](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N3423996.html#Setting-the-Internal-ID-Preference)。\*  <br /><br />  - **NegotiateSSLClose** : `false` <br /><br />  - **ServerDataSource** : `NetSuite2.com`  <br /> *自2021年11月8日起，新Connect用户只能使用NetSuite2.com数据源访问Connect服务。有关更多详情，请参见[Oracle NetSuite的文档 ↗](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_N752122.html#Connect-Data-Source)。* <br /><br />  - **encrypted** : `1`|

其他连接参数与任何[JDBC来源](/zh/foundry/available-connectors/custom-jdbc-sources/#jdbc-properties)相同。

## 创建同步

NetSuite SuiteAnalytics来源可以通过[探索](/zh/foundry/data-connection/source-exploration/)来发现表并创建新同步。
您还可以从来源的概览页面[手动创建新同步](/zh/foundry/data-connection/set-up-sync/)。
