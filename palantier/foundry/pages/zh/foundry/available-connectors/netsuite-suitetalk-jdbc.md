---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/netsuite-suitetalk-jdbc/",
  "title": "Oracle NetSuite SuiteTalk",
  "page_id": "netsuite-suitetalk-jdbc",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/netsuite-suiteql-jdbc/",
  "next": "/zh/foundry/available-connectors/oracle-sales/",
  "scraped_at": "2026-07-13T05:36:50.369234+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Oracle NetSuite SuiteTalk

使用 SuiteTalk 框架将 Foundry 连接到 Oracle NetSuite，并开始将数据从您的 NetSuite ERP 同步到 Foundry。

## 支持的功能

| 功能 | 状态 |
| --- |--- |
| 探索 | 🟢 一般可用 |
| 批量同步 | 🟢 一般可用 |
| 增量 | 🟢 一般可用 |

## 设置

1. 打开 [数据连接](/zh/foundry/data-connection/overview/) 应用程序，并在屏幕右上角选择 **+ 新建来源**。
2. 从可用的连接器类型中选择 **NetSuite SuiteTalk**。
3. 选择使用 [直接连接](/zh/foundry/data-connection/set-up-direct-connection/) 或通过 [代理运行时连接](/zh/foundry/data-connection/set-up-agent/)。
4. 按照下文章节中的信息继续设置您的连接器。

了解更多关于在 Foundry 中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

### 认证

NetSuite SuiteTalk 来源使用 [基于词元的认证 (TBA) ↗](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_4247329078.html#To-set-up-TBA-in-your-NetSuite-account%3A)。

:::callout{theme="neutral"}
必须在您的账户中启用基于词元的认证功能。要启用 TBA，请参阅 [NetSuite 文档 ↗](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_4253254429.html#procedure_4253064345)。
:::

#### 在 NetSuite 中配置用户角色和权限

NetSuite 中的访问控制是通过为用户指派角色来配置的；每个角色都是权限的集合，定义了用户可以执行的任务和可以访问的数据。我们建议为将连接到 Foundry 的用户进行以下配置：

1. 创建具有适当权限的专用角色。
   1. 从 NetSuite 的工具栏中选择 **Setup** > **Users/Roles** > **Manage Roles** > **New**，并为角色提供一个明确的名称。我们建议使用 `foundry-role`。
      * 您可以选择勾选 **仅限 Web 服务** 配置框。
   2. 通过导航到角色页面底部并选择 **Permissions** > **Setup**，为角色添加系统范围的权限。您需要添加的最低权限是：
      * **使用访问词元登录**，
      * **SOAP Web 服务**，
      * **其他自定义字段**，
      * **自定义主体字段**，
      * **自定义项目字段**，
      * 记得 **保存** 权限。
   3. 通过导航到角色页面底部并选择 **Permissions** > **Lists**，为您希望从 Foundry 查询的表添加表权限。选择您想要的表，选择 **添加** 然后 **保存**。

2. 为用户指派新角色。
   1. 从 NetSuite 的工具栏中选择 **Setup** > **Users/Roles** > **Manage Users**。选择您想要用于连接到 Foundry 的用户，然后选择 **Edit**。
   2. 导航到 **Access** 标签，确保 **Give Access** 复选框被勾选。
   3. 在 **Roles** 标签中，从下拉列表中选择新创建的角色 (`foundry-role`)，选择 **Add** 然后 **Save**。

要验证您添加了正确的权限，请以您指派新角色的用户身份登录，并检查您是否可以查看预期的所有数据。

#### 在 NetSuite 中配置集成和访问词元

集成记录用于在 NetSuite 中管理与外部系统的连接。我们建议以下配置以连接到 Foundry：

1. 使用 TBA 创建一个新的集成记录（参见[更多详情 ↗](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_4249032125.html#procedure_4253065190)）。
   1. 从 NetSuite 的工具栏中选择 **Setup** > **Integration** > **Manage Integrations** > **New**，并为集成提供一个明确的名称。我们建议 `foundry-integration`。
   2. 确保 **State** 为 **Enabled**，并且仅勾选 **Token-based Authentication**。其他所有框应取消勾选。
   3. 在您 **保存** 后，记下 **`CLIENT ID`** 和 **`CLIENT SECRET`**。您将需要它们来配置 Foundry。

:::callout{theme="neutral"}
`CLIENT ID` 和 `CLIENT SECRET` 仅在您首次保存集成记录时显示。要获取新的值，您必须重置 `CLIENT ID` 和 `CLIENT SECRET`，这将使以前的值失效。
:::

2. 创建并指派一个 TBA 词元。
   1. 从 NetSuite 的工具栏中选择 **Setup** > **User/Roles** > **Access Tokens** > **New**。
      * 如果您不能为其他用户管理词元，请导航到 NetSuite 首页左下角的 **Settings** 面板并选择 **Manage Access Tokens**。
   2. 选择新创建的 **application** (`foundry-integration` 在我们的示例中)，指派了新创建角色的用户 (`foundry-role`)，以及新创建的角色。
      * 如果您不能为其他用户管理词元，您的用户将默认被选中。确保您的用户已被指派了新创建的角色 (`foundry-role`)。
   3. 在您 **保存** 后，记下 **`TOKEN ID`** 和 **`TOKEN SECRET`**。您将需要它们来配置 Foundry。

:::callout{theme="neutral"}
`TOKEN ID` 和 `TOKEN SECRET` 仅在您首次保存词元时显示。您需要创建一个新词元以获取新的 `TOKEN ID` 和 `TOKEN SECRET`。
:::

[了解更多关于在 NetSuite 中管理词元的信息。↗](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4254975694.html)

### 网络

NetSuite SuiteTalk 连接器需要网络访问您要连接的 NetSuite 实例。

#### 选项 1: 直接连接

如果您是通过 [直接连接](/zh/foundry/data-connection/core-concepts/#direct-connections) 进行连接的，您需要在来源中添加以下 [出口策略](/zh/foundry/administration/configure-egress/)：

* `<ACCOUNT_ID>.suitetalk.api.netsuite.com` 端口 443；您可以在连接到 NetSuite 时在 URL 中找到您的账户 ID。
* `webservices.netsuite.com` 端口 443。

如果这些出口策略不存在，您可以[请求它们](/zh/foundry/data-connection/set-up-direct-connection/#configure-a-network-policy)；否则您可以[添加它们](/zh/foundry/data-connection/set-up-direct-connection/#choose-your-network-policy)。

#### 选项 2: 代理连接

如果您使用代理运行时连接，您必须确保代理主机的防火墙对连接到您的 NetSuite Connect 实例所需的主机名、IP 地址和端口开放。

### 连接详情

| 选项 | 必需? | 描述 |
| --- | --- | --- |
| `Account ID` | 是 | NetSuite 账户 ID，位于您的 NetSuite 实例 URL 的前缀中 |
| `Client ID` | 是 | 创建 [`foundry-integration`](#configure-integration-and-access-tokens-in-netsuite) 时复制的 `CLIENT ID` |
| `Client secret` | 是 | 创建 [`foundry-integration`](#configure-integration-and-access-tokens-in-netsuite) 时复制的 `CLIENT SECRET` |
| `Access token` | 是 | 创建 [TBA 词元](#configure-integration-and-access-tokens-in-netsuite) 时复制的 `TOKEN ID` |
| `Access token secret` | 是 | 创建 [TBA 词元](#configure-integration-and-access-tokens-in-netsuite) 时复制的 `CLIENT ID` |

## 创建同步

NetSuite SuiteTalk 来源可以被[探索](/zh/foundry/data-connection/source-exploration/)以发现表并创建新的同步。
您还可以从来源的概览页面[手动创建新的同步](/zh/foundry/data-connection/set-up-sync/)。
