---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/sharepoint-online/",
  "title": "Sharepoint Online",
  "page_id": "sharepoint-online",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/sftp/",
  "next": "/zh/foundry/available-connectors/shipstation/",
  "scraped_at": "2026-07-13T05:37:45.147074+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Sharepoint Online

连接到 SharePoint Online，以从指定的 SharePoint 库中导入文件到 Foundry。

## 支持的功能

| 功能  | 状态 |
|--- |--- |
| 探索 | 🟢 一般可用 |
| 批量导入 | 🟢 一般可用 |
| 增量 | 🟢 一般可用 |
| 导出任务 | 🟡 停用 |
| [文件导出](/zh/foundry/data-connection/export-overview/#file-exports) | 🟢 一般可用 |

## 数据模型

连接器可以将任何类型的文件传输到 Foundry 数据集。文件格式会被保留，传输过程中或之后不会应用任何模式。对输出数据集应用任何必要的模式，或[编写下游变换](/zh/foundry/pipeline-builder/transforms-overview/)以访问数据。

## 性能和限制

可传输文件的大小没有限制。然而，网络问题可能导致大规模传输失败。特别是，运行超过两天的直接云同步将被中断。为避免网络问题，我们建议使用较小的文件大小，并限制每次执行同步时摄取的文件数量。同步可以[定期安排](/zh/foundry/data-connection/set-up-sync/#configure-sync)运行。

:::callout{theme="warning"}
不支持连接到本地 SharePoint 服务器。
:::

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序，并在屏幕右上角选择 **+ 新建来源**。
2. 从可用的连接器类型中选择 **SharePoint Online**。
3. 选择通过互联网使用[**直接连接**](/zh/foundry/data-connection/set-up-direct-connection/)或通过[**中介代理连接**](/zh/foundry/data-connection/set-up-agent/)。
4. 根据以下部分的信息，按照其他配置提示继续设置连接器。

了解更多关于在 Foundry 中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

## 认证

:::callout{theme="warning"}
SharePoint Online 来源的认证需要在 Microsoft Entra ID（以前称为 Azure Active Directory）中创建一个应用程序。如果您不是 Entra ID 管理员，请联系您的 IT 部门请求访问。
:::

按照以下初始步骤访问 Azure 应用程序凭据：

1. 按照[Microsoft 文档 ↗](https://docs.microsoft.com/graph/auth-register-app-v2)中的说明在 Azure 中创建一个应用程序注册。
   * 在步骤 5，选择 **仅此组织目录中的帐户**，并跳过 **重定向 URL（非必填）**。
2. 注册完成后记录客户端 ID 和租户 ID。

然后，从以下两种可用的认证方法中选择：

* [客户端凭据：](#client-credentials) 当需要对每个 SharePoint 站点的广泛访问时推荐使用。
* [用户名/密码：](#usernamepassword) 当需要限制访问一个或几个 SharePoint 站点时推荐使用。

### 客户端凭据

在您的 Microsoft Entra 管理中心，完成以下步骤：

1. 在左侧边栏中进入 **API 权限**。
2. 选择 **添加权限**。
3. 选择 **Microsoft Graph**。
4. 选择 **应用程序权限**。
   * 如果您希望您的应用程序读取 *所有* SharePoint 站点，添加 `Sites.Read.All`。
     * 如果您计划配置导出任务，请使用 `Sites.ReadWrite.All`。
   * 如果您希望您的应用程序读取**选定的 SharePoint 站点**，添加 `Sites.Selected`。
5. 如果您是 Entra 管理员，选择 **授予 \[租户] 的管理员同意**。
6. 如果您在上面添加了 `Sites.Selected`，[将您的应用程序添加到特定站点 ↗](https://devblogs.microsoft.com/microsoft365dev/controlling-app-access-on-specific-sharepoint-site-collections/)。

   * `"roles"` 数组参数的可用选项为 `"write"` 和/或 `"read"`。选项 `"read"` 足以从 SharePoint 站点摄取文件。
   * 要轻松发送具有适当认证的 POST，请使用 [Graph Explorer ↗](https://developer.microsoft.com/graph/graph-explorer)。
   * 通过发送 GET 请求到 `https://graph.microsoft.com/v1.0/sites/[tenantName]:/sites/[siteName]` 可以接收有关站点的元数据（例如：<https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/mySite>）。此请求将返回一个 ID，该 ID 是几个值的组合：站点集合主机名、站点集合唯一 ID 和站点唯一 ID，其中中间值是运行权限 POST 所需的 siteId。
7. [生成客户端机密。↗](https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal#option-2-create-a-new-application-secret)。

在数据连接中设置以下源配置：

| 选项  | 必填?  | 描述 |
|--- |--- |---  |
| `Azure 客户端 ID` | 是 | 应用程序注册的 ID；也称为应用程序 ID。 |
| `Azure 租户 ID` | 是 | Microsoft Entra ID 实例的唯一标识符。|
| `客户端机密` | 是 | 应用程序注册中生成的机密。 |

### 用户名/密码

用户名/密码流程涉及创建一个可以登录到 Microsoft 365 的用户帐户。Graph API 不支持用户名/密码认证方法的双因素认证。因此，**我们强烈建议创建至少 32 个字符长度的随机生成密码**。

在您的 Entra 管理中心，完成以下步骤：

1. 在左侧边栏中进入 **API 权限**。
2. 选择 **添加权限**。
3. 选择 **Microsoft Graph**。
4. 选择 **委派权限**。
5. 添加 `Sites.Read.All` 权限；
   * 如果您计划配置导出任务，请使用 `Sites.ReadWrite.All`。
6. 如果您是 Azure 管理员，选择 **授予 \[租户] 的管理员同意**。
7. 在左侧边栏中进入 **认证**。
8. 将 **允许公共客户端流** 更改为 `是`。
9. 在 Microsoft Entra ID 中创建一个用户，并设置*至少 32 个字符长度的随机生成密码*。
10. 将该用户添加到您希望其读取或写入的任何 SharePoint 站点。

在数据连接中设置以下源配置：

| 选项  | 必填?  | 描述 |
|--- |--- |---  |
| `Azure 客户端 ID` | 是 | 应用程序注册的 ID；也称为应用程序 ID。 |
| `用户名` | 是 | 用户的电子邮件地址。|
| `密码` | 是 | 生成的密码。|

### 基于 XML 的 SharePoint 加载项权限管理

如果您正在使用 [SharePoint 加载项进行授权和认证 ↗](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/authorization-and-authentication-of-sharepoint-add-ins)，且您的 SharePoint 加载项使用 XML 进行权限管理，您必须确保在范围 URI 中设置了正确的范围，以避免连接到 SharePoint 时的访问问题。

请按照以下步骤验证和配置正确的范围：

1. 找到包含 SharePoint 加载项权限设置的 `AppManifest.xml` 文件。
2. 在 `AppManifest.xml` 文件中，识别 XML 文件中的范围 URI，应该类似于以下内容：

`<AppPermissionRequests AllowAppOnlyPolicy="true"> <AppPermissionRequest Scope="http://sharepoint/content/sitecollection/web" Right="FullControl" /> </AppPermissionRequests>`。

3. 验证范围值（在此示例中为 `http://sharepoint/content/sitecollection/web`）是否与您正在连接的 SharePoint 站点匹配；如果范围值不匹配，请相应调整范围值。

### 网络

SharePoint Online 连接器需要在端口 443 上访问以下域：

* `login.microsoftonline.com`
* `graph.microsoft.com`
* 您的 SharePoint URL；例如，`contoso.sharepoint.com`

如果您使用的是 GovCloud Sharepoint 实例，请改用以下域名在端口 443 上：

* `login.microsoftonline.us`
* `graph.microsoft.us`
* 您的 SharePoint URL；例如，`contoso.sharepoint.us`

## 配置选项

以下是 SharePoint Online 连接器的配置选项：

| 选项  | 必填?  | 描述 |
|--- |--- |---  |
| `SharePoint 库 URL` | 是 |  单个 SharePoint 站点可能有多个文档库；您的 URL 必须指向特定的库。必须采用格式 `https://[tenant].sharepoint.com/sites/[site]/[library]`。 |
| `凭证设置` | 是 |  使用上面显示的[认证](#authentication)指南进行配置。 |
| `代理设置` | 否 | 启用以在连接 SharePoint Online 时使用代理。|

## 从 Sharepoint Online 同步数据

SharePoint Online 连接器使用[基于文件的同步接口](/zh/foundry/data-connection/file-based-syncs/)。

## 导出数据到 SharePoint Online

要导出到 SharePoint 站点，首先为您的 SharePoint Online 连接器[启用导出](/zh/foundry/data-connection/export-overview/#enable-exports-for-source)。然后，[创建一个新的导出](/zh/foundry/data-connection/export-overview/#creating-a-new-export)。

### 导出配置选项

| 选项  | 必填? | 默认值 | 描述 |
|--- |--- |--- |--- |
| `目录路径` | 是 | / | SharePoint 库中应导出文件的文件夹路径。导出文件的完整路径计算为 `<SharePoint Library URL>/Directory Path>/<Exported File Path>` |
