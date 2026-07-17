---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/salesforce/",
  "title": "Salesforce",
  "page_id": "salesforce",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/sage-business-cloud-accounting/",
  "next": "/zh/foundry/available-connectors/salesforce-marketing-cloud/",
  "scraped_at": "2026-07-13T05:37:27.668091+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Salesforce

Foundry的**Salesforce**连接器允许您在Salesforce和Foundry数据集之间同步数据。

:::callout{theme="warning"}
本文档指的是最新版本的Salesforce连接器。如果您正在编辑现有的Salesforce连接器，它可能是一个旧版本。请查看下面关于[迁移](#migration)的部分以获取更多信息。
:::

## 支持的功能

| 功能        | 状态                  |
|-------------|------------------------|
| 探索       | 🟢 一般可用            |
| 批量导入   | 🟢 一般可用            |

## 数据模型

该连接器将所有可用的[标准 ↗](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_list.htm)和自定义Salesforce对象建模为Foundry数据集。模式是动态检索的。探索视图允许您浏览数据模型并预览Salesforce对象导入到Foundry后的显示方式。

### 数据类型映射

连接器将Salesforce API类型映射到以下[Foundry字段类型](/zh/foundry/data-integration/datasets/#supported-field-types)：

| Salesforce                   | Foundry |
|------------------------------|---------|
| Auto Number                  | STRING  |
| Lookup Relationship          | STRING  |
| Master-Detail Relationship   | STRING  |
| External Lookup Relationship | STRING  |
| Checkbox                     | BOOLEAN |
| Currency                     | DECIMAL |
| Date                         | DATE    |
| Date/Time                    | LONG    |
| Email                        | STRING  |
| Geolocation                  | STRING  |
| Number                       | DOUBLE  |
| Percent                      | DOUBLE  |
| Phone                        | STRING  |
| Picklist                     | STRING  |
| Picklist (Multi-Select)      | STRING  |
| Text                         | STRING  |
| Text Area                    | STRING  |
| Text Area (Long)             | STRING  |
| Text Area (Rich)             | STRING  |
| Text (Encrypted)             | STRING  |
| Time                         | INTEGER |
| URL                          | STRING  |

## 性能和限制

该连接器利用了[Salesforce SOAP API ↗](https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_quickstart_intro.htm)，其受限于[Salesforce SOAP API调用限制 ↗](https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/salesforce_app_limits_platform_apicalls.htm)。

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序，选择屏幕右上角的\*\*+ 新建源\*\*。
2. 从可用的连接器类型中选择**Salesforce**。
3. 选择使用[**直接连接**](/zh/foundry/data-connection/set-up-direct-connection/)通过互联网连接，或选择[**通过中介代理连接**](/zh/foundry/data-connection/set-up-agent/)。
4. 按照其他配置提示继续设置连接器，使用下面各节中的信息。

了解更多关于在Foundry中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

## 认证

选择一种凭证方法来验证您的Salesforce连接：JWT词元或用户名-密码。

### JWT词元

您可以使用OAuth 2.0 [JSON Web词元 (JWT) 持有者流 ↗](https://help.salesforce.com/articleView?id=remoteaccess_oauth_jwt_flow.htm)来授权Foundry访问数据，而无需在每次请求时进行交互式登录。

要启用JWT认证，您必须生成一个证书，在创建连接的应用程序时上传该证书，然后执行一次性授权集成用户。

#### 第1部分：生成证书

首先，创建一个Salesforce用户并验证其是否具有API和任何您希望修改的Salesforce对象的访问权限。确保您能够以集成用户身份登录，因为在后续步骤中您需要以该用户身份进行授权。

现在，创建一个JWT证书。Salesforce [JWT持有者流 ↗](https://help.salesforce.com/articleView?id=remoteaccess_oauth_jwt_flow.htm\&type=5)需要一个X.509证书和关联的私钥。要生成私钥，请在命令行使用**openssl**并运行以下命令：

1. 生成x.509公钥和私钥对：

   ```bash
   % openssl genrsa 1024 | openssl pkcs8 -topk8 -inform PEM -out key.pem -nocrypt
   % openssl req -new -x509 -key key.pem -out cert.pem -days 3650
   ```

2. 将证书导出到PFX存储，转换为Base64，并复制到剪贴板：

   ```bash
   % openssl pkcs12 -export -in cert.pem -inkey key.pem | openssl base64 | pbcopy
   ```

:::callout{theme="warning"}
请确保将证书值保存在安全的位置。您需要在[配置](#part-3-authorize-user)中访问该值。
:::

#### 第2部分：创建连接的应用程序

在Salesforce Lightning Experience设置页面，滚动浏览左侧边栏以选择**应用程序 > 应用程序管理器**条目，位于**平台工具**部分。在应用程序管理器页面，通过选择**新建连接应用程序**来创建一个新的连接应用程序。

在应用程序创建页面的**基本信息**部分，填写以下字段：

1. 连接应用程序名称
2. API名称
3. 电子邮件

然后，按照以下步骤设置\*\*API（启用OAuth设置）\*\*部分：

1. 勾选**启用OAuth设置**。
2. 在**回调URL**中填写`https://localhost:12345`。这将在后续使用。
3. 勾选**使用数字签名**并上传上面生成的`cert.pem` **X.509证书文件**。
4. 从可用的**OAuth范围**中选择**api**、**offline\_access**和**refresh\_token**。
5. 勾选**要求Web服务器流的秘密**。

忽略其他部分，通过选择**保存**然后在下一页上选择**确认**来完成连接应用程序的创建。在尝试使用连接的应用程序之前，请等待十分钟。

一旦连接的应用程序创建完成，请在**API（启用OAuth设置）**部分下保存**消费者密钥**（例如，3MVG9FG3dv...）到一个安全的地方。

#### 第3部分：授权用户

使用以下选项之一授权集成用户：

* \*\*执行一次性授权：\*\*通过在浏览器中执行登录流来为集成用户授权连接应用程序：
  1. 导航到以下Salesforce URL：`https://<salesforce-url>/services/oauth2/authorize?client_id=`**`<CONSUMER_KEY>`**`&redirect_uri=`**`<CALLBACK_URL>`**`&scope=api%20offline_access%20refresh_token&response_type=code&response_mode=query&nonce=bebmwgu22zh`
     * 用您的连接应用程序消费者密钥替换`<CONSUMER_KEY>`，并用您在API配置步骤中输入的URL替换`<CALLBACK_URL>`。
     * 用您的Salesforce实例URL替换`<salesforce-url>`（`<site>.my.salesforce.com`）。
  2. 以集成用户身份完成登录流，必要时选择**使用自定义域**。在下一页上选择**允许**，以允许连接应用程序代表您执行指定范围的操作。确保显示的是集成用户的用户名，而不是您的个人帐户用户名。
  3. 然后，您将被重定向回`https://localhost:12345`（回调URL）。由于回调URL不是真实的，浏览器将显示预期的“未找到”错误。
* **通过遵循[Salesforce指导 ↗](https://help.salesforce.com/articleView?id=connected_app_manage_oauth.htm\&type=5)预授权用户**来更改**允许的用户**策略为**管理员批准的用户已预授权**。预授权完成后，返回连接应用程序配置页面为连接应用程序授予访问权限。可以将访问权限授予个人集成用户配置文件，或包含集成用户的权限集。

继续使用以下JWT认证配置选项在Foundry中设置Salesforce连接器：

| 名称  | 必需 | 描述 |
|--- |--- |---|
| `这是一个Salesforce沙盒帐户` | 是 | 确定是否应连接到Salesforce沙盒帐户。为`登录URL`设置默认值：标准帐户为`login.salesforce.com`，沙盒帐户为`test.salesforce.com`。|
| `用户名` | 是 | 输入集成用户的用户名。|
| `Base64 PFX证书` | 是 | 从[生成证书](#part-1-generate-a-certificate)获得的值。|
| `证书是密码保护的` | 否 | 如果证书存储是密码保护的，请打开切换。|
| `证书密码` | 否 | 证书存储的密码。 |
| `指定证书主题` | 否  | 关闭以使用存储中的第一个证书。如果证书存储中包含多个证书，请打开切换以指定要使用的证书。 |
| `证书主题` | 否  | 希望的证书主题。用于在存储中定位证书。如果未找到精确匹配，则在存储中搜索包含提供值的证书。 |
| `消费者密钥` | 是 | 输入[连接的应用程序](#part-2-create-a-connected-app)设置中可用的消费者密钥。|

### 用户名-密码

要使用[用户名-密码 ↗](https://help.salesforce.com/articleView?id=remoteaccess_oauth_username_password_flow.htm)认证方法连接到Salesforce，您必须在Salesforce中创建一个服务用户帐户和连接的应用程序。然后，将两者的凭证添加到Salesforce连接器中。

按照以下步骤启用用户名-密码认证流。

1. 创建一个Salesforce用户并验证其是否具有API和任何您希望修改的Salesforce对象的访问权限。请记录用户的用户名和密码以备将来参考。

2. 创建连接的应用程序：

   1. 在Salesforce Lightning Experience设置页面，滚动浏览左侧边栏以选择**应用程序 > 应用程序管理器**条目，位于**平台工具**部分。在应用程序管理器页面，通过选择**新建连接应用程序**来创建一个新的连接应用程序。

   2. 在应用程序创建页面的**基本信息**部分，填写以下字段：
      1. 连接应用程序名称
      2. API名称
      3. 电子邮件

   3. 然后，按照以下步骤设置\*\*API（启用OAuth设置）\*\*部分：
      1. 勾选**启用OAuth设置**。
      2. 在**回调URL**中填写`https://localhost:12345`。此字段是配置所需的，但回调URL将不被使用。
      3. 从可用的**选定OAuth范围**中选择**完全访问（full）**，以允许访问对活动用户可访问的所有数据。

   4. 忽略其他部分，通过选择**保存**然后在下一页上选择**确认**来完成连接应用程序的创建。在尝试使用连接的应用程序之前，请等待两到十分钟。

一旦连接的应用程序创建完成，请从应用程序管理器页面导航到它。选择**管理**，然后选择**编辑策略**。在**OAuth政策 > 允许的用户**下选择**所有用户可以自我授权**。

用户名-密码认证方法支持以下配置选项：

| 名称  | 必需 | 描述 |
|--- |--- |---|
| `这是一个Salesforce沙盒帐户` | 是 | 确定是否应连接到Salesforce沙盒帐户。为`登录URL`设置默认值：标准帐户为`login.salesforce.com`，沙盒帐户为`test.salesforce.com`。|
| `用户名` | 是 | 连接应用程序模拟的帐户的用户名。|
| `密码` | 是 | 连接应用程序模拟的帐户的密码。|

:::callout{theme="neutral"}
如果您在尝试从Foundry连接时遇到授权问题，并在用户的**Salesforce登录历史**中看到`出错：需要API安全词元`，您必须将用户的安全词元添加到密码末尾。

安全词元是一个自动生成的密钥，必须添加到密码中以便从不受信任的网络登录到Salesforce。Salesforce不允许用户在应用程序中查看安全词元；相反，您必须以*集成用户*身份登录到Salesforce，并导航到右上角的**我的设置**。然后，导航到**个人 > 重置我的安全词元**。
:::

### 网络

如果直接连接正在运行您的Salesforce连接器，您必须添加一个[网络出口策略](/zh/foundry/administration/configure-egress/)以白名单连接。

选择添加现有策略，或创建一个新策略。

要为Salesforce白名单直接连接，请添加以下策略：

* 登录URL：需要`DNS`，端口`443`（HTTPS），以及以下之一：
  * `login.salesforce.com`（生产）
    **或**
  * `test.salesforce.com`（沙盒）

* 实例URL：需要`DNS`用于`<site>.my.salesforce.com`，端口`443`（HTTPS）。

### 证书和私钥

SSL连接验证服务器证书。通常，SSL验证通过证书链进行；默认情况下，代理和直接连接运行时信任大多数行业标准证书链。如果您正在连接的服务器有一个自签名证书，或者在验证期间有TLS拦截，连接器必须信任该证书。了解更多关于[在数据连接中使用证书](/zh/foundry/data-connection/agent-configuration-reference/#certificates)的信息。

## 配置选项

Salesforce连接器支持以下配置选项：

| 名称                        | 必需                | 默认值                                                                | 描述                                                                                                                   |
|-----------------------------|-------------------------|------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `API版本`               | 是                     | 50                                                                     | Salesforce API版本。                                                                                 |
| `连接的应用程序凭证` | 是                     | `JWT持有者词元`                                                     | 包含连接到Salesforce所需的凭证。查看上面的[认证](#authentication)部分以获取更多信息。 |
| `登录URL`                 | 否 | `login.salesforce.com`（生产），或`test.salesforce.com`（沙盒） | 用于连接以检索OAuth词元的URL。 |
| `超时`                   | 否                      | 60                                                                     | HTTP客户端连接在等待响应时超时的持续时间。时间以秒为单位。  |
| `代理设置`             | 否                      | 否                                                                     | 连接到Salesforce时使用的代理配置。                                                                 |

## 从Salesforce同步数据

使用[探索视图](/zh/foundry/data-connection/source-exploration/)同步表。编辑同步时提供其他配置选项。

### 增量

在使用Salesforce连接器进行增量同步时，如果增量列值*大于或等于*先前观察到的最大值，则会同步新数据。虽然此行为对于同步数据的精确性和正确性是必需的，但会导致输出数据集中出现重复行。增量管道应始终包含一个去重步骤。

### 筛选

您可以向同步配置添加行筛选以排除不符合特定标准的数据。
使用条件树定义您的筛选：

* 逻辑运算符：
  * `ALL`：要求嵌套在下面的所有节点为true。
  * `ANY`：要求至少一个嵌套节点为true。
* 条件：
  * 从可用列列表中选择。
  * 根据列类型选择适当的运算符。
  * 设置一个值以与所选列进行比较。

确保**保存**您的配置以将其应用于同步。

## 迁移

如果您已经有一个Salesforce连接器，您可能正在运行旧版本。要识别您的连接器版本，请迁移到**连接设置 > 连接详细信息**。如果源配置显示一个带有`type: salesforce`字段的**自定义YAML**部分，您正在使用旧版Salesforce连接器。您必须迁移到最新版本以获得Palantir的支持（超出错误修复的范围）。

### 迁移连接器

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序，选择屏幕右上角的\*\*+ 新建源\*\*。
   1. 从可用的连接器类型中选择**Salesforce**。
   2. 选择使用[**直接连接**](/zh/foundry/data-connection/set-up-direct-connection/)通过互联网连接，或选择[**通过中介代理连接**](/zh/foundry/data-connection/set-up-agent/)。
   3. 按照其他配置提示继续设置连接器，使用下面各节中的信息。
2. 配置认证以匹配旧源。在旧源配置中，找到自定义YAML中的`auth-method`或`authentication-method`块。
   * 如果`type: oauth2-jwt`，使用[JWT认证](#jwt-token)配置新源：
     * 自定义YAML中的`claim-sub`变为新连接器配置中的`用户名`。
     * `x509-cert`导出为PFX，然后Base64编码并成为`证书`。了解更多关于证书的信息，请参见上面的[JWT认证](#jwt-token)部分。
   * 如果PFX是密码保护的，打开`证书是密码保护的`并输入`证书密码`。
     * 自定义YAML中的`claim-iss`变为新连接器配置中的`消费者密钥`。
   * 如果`type: oauth2-username-password`，使用[用户名-密码认证](#username-password)配置新源：
     * 自定义YAML中的`username`变为新连接器配置中的`用户名`。
     * 自定义YAML中的`password`变为新连接器配置中的`密码`。
     * 旧源上的`client-id`和`client-secret`属性在新连接器中*不*需要。
3. 配置其他属性：
   * 自定义YAML中的`auth-url`变为新连接器配置中的`登录URL`。
   * 如果自定义YAML中的`auth-url`值为`test.salesforce.com`，则在新连接器配置中打开`是Salesforce沙盒帐户`。

### 迁移同步

配置新的Salesforce连接器后，为旧连接器之前同步的对象创建同步。使用[探索视图](/zh/foundry/data-connection/source-exploration/)一次性批量同步多个对象并创建新的数据集。

:::callout{theme="neutral"}
如果使用相同的API版本，旧版和新版Salesforce连接器将使用相同的模式；如果输入已重新映射，所有下游应用程序应继续正常运行。
:::

您必须迁移下游管道以使用新的同步数据集。一旦确认没有其他消费者需要旧版数据集，您可以删除数据集、相关同步和连接。使用[数据沿袭](/zh/foundry/data-lineage/overview/)查找旧版数据集在您的环境中的使用位置。
