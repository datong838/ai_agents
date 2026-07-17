---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/sap/oauth2-writeback/",
  "title": "用户归属的 SAP 数据输出与 OAuth 2.0",
  "page_id": "oauth2-writeback",
  "category_id": "data-integration",
  "section_id": "sap",
  "previous": "/zh/foundry/sap/ingest-hana-views/",
  "next": "/zh/foundry/sap/faq/",
  "scraped_at": "2026-07-13T05:39:58.121065+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 用户归属的 SAP 数据输出与 OAuth 2.0

本页面包含[在 SAP 中设置 OAuth 2.0 服务器](#setting-up-the-oauth-20-server-in-sap)和[在 Foundry 中设置 OAuth 2.0 客户端](#setting-up-the-oauth-20-client-in-foundry)的说明。

## 在 SAP 中设置 OAuth 2.0 服务器

### 先决条件

* Palantir Foundry Connector 2.0 for SAP Applications ("Connector") 的 SP21 或更高版本
* SAP 中的 Foundry 技术用户应为 `SYSTEM` 用户
* `/PALANTIR/OAUTH_CLIENT` 应指派给 Foundry 技术用户和任何希望从 Foundry 数据输出到 SAP 的终端用户
* `/PALANTIR/CONTENT_FUNCTION_ALL` 应指派给终端用户
* 需激活 `/sap/public/bc` 节点下的所有服务（用于 OAuth 2.0 配置）
  * `/sap/bc/sec/oauth2*`
  * `/default_host/sap/bc/webdynpro/sap/oauth2_authority`
* SAP 网关已激活
* SAP NetWeaver 7.4 SP09 或更高版本（支持 OAuth 2.0 和 OData）

### 参考

* [注释 1688545 - AS ABAP 中的 OAuth 2.0 服务器故障排除 ↗](https://me.sap.com/notes/1688545)（需要 SAP 登录）
* [帮助: AS ABAP 的 OAuth 2.0 服务器 ↗](https://help.sap.com/viewer/3c4e8fc004cb4401a4fdd737f02ac2b9/7.5.9/en-US/4bd73e2050e84ce99b2d781687e0c62d.html)

### OAuth 2.0 配置

1. 运行 `SOAUTH2` 事务。
2. 选择 **创建...**。
3. 输入 Foundry 技术用户的用户名作为 **OAuth 2.0 客户端 ID**。
4. 选择 **下一步 >**。
5. 输入 Foundry 技术用户的用户名作为 **用户 ID**。
6. 确保勾选了 **客户端用户 ID 和密码** 和 **SSL 客户端证书**。
7. 选择 **下一步 >**。
8. 将 **重定向 URI** 设置为 `https://<FOUNDRY_DOMAIN>/workspace/oauth2-clients/callback`。
9. 选择 **下一步 >**。
10. 添加一个 **范围分配**，**OAuth 2.0 范围 ID** 为 `/PALANTIR/SRV_0001`，描述如 `使用 SAP 函数进行 Palantir Foundry 数据输出`。
11. 选择 **下一步 >** 然后 **完成**。

### OData 配置

1. 在 SAP 的 **维护服务** 页面中，按照服务层次结构找到 **opu > odata > palantir**。
2. 右键点击 **palantir** 并选择 **激活服务**。
3. 在提示时选择 **是**。
4. 在 **创建/更改服务** 选项卡中，选择 **交互选项** 下的 **GUI 配置**。
5. 添加名称为 `~CHECK_CSRF_TOKEN`，值为 `0`（零）的参数。
6. 按照此处说明禁用 CSRF\_TOKEN 验证：https://help.sap.com/doc/saphelp\_hba/1.0/de-DE/e6/cae27d5e8d4996add4067280c8714e/content.htm
7. 运行 `/IWFND/MAINT_SERVICE` 事务。
8. 在 **系统别名** 下选择 **添加系统别名**。
9. 添加具有以下值的系统别名：
   * **服务文档标识符**：`/PALANTIR/SRV_0001`
   * **用户角色**：空
   * **主机名**：空
   * **SAP 系统别名**：`LOCAL`
   * **元数据默认**：未勾选
   * **默认系统**：已勾选
   * **技术服务名称**：`/PALANTIR/SRV`
   * **外部服务名称**：`ODATA_SRV`
   * **版本**：`1`
   * **用户名**：空

## 在 Foundry 中设置 OAuth 2.0 客户端

此过程遵循[配置外部应用程序](/zh/foundry/administration/configure-outbound-applications/)中概述的一般方法，但已专门针对 SAP 系统进行调整。

### 源连接设置

:::callout{theme="warning" title="警告"}
确保 SAP 源 URL 使用 HTTPS，否则在使用 OAuth 流时，webhook 将出错。
:::

1. 创建一个新的 **REST API** 源。

![创建 REST API 源](../../../images/foundry/sap/create-rest-source.png)

2. 使用用于 SAP 源的基础域 URL 和端口配置源。
3. 选择 **基本** 认证并添加用于连接 SAP 的用户名和密码。

![配置 REST API 源](../../../images/foundry/sap/configure-rest-source.png)

4. 保存源。

### OAuth 2.0 授权流程 webhook 设置

1. 在新 **REST API** 源的概览页面上，选择 **创建 webhook**。

2. 为 webhook 命名（例如“***SAP OAuth2 授权代码流 webhook***”）。

3. 前进到 **请求配置** 步骤。

4. 在 **调用** 下，选择 **POST** 作为请求类型，并输入 `sap/bc/sec/oauth2/token` 作为路径。

5. 在 **查询参数** 下，如果使用的客户端不是默认客户端，可能需要设置 `sap-client`。

![Webhook 调用](../../../images/foundry/sap/webhook-calls.png)

6. 向下滚动到 **输入参数** 并添加以下三个参数（均为字符串类型）：

* `redirect_uri`
* `client_id`
* `authorization_code`

![Webhook 输入参数](../../../images/foundry/sap/webhook-input-parameters.png)

7. 向上滚动回 **调用** 并选择 **正文** 选项卡。
8. 选择 **表单 URL 编码** 并添加以下四个条目：

* `grant_type` → `authorization_code`
* `redirect_uri` → 映射到 `redirect_uri` 输入参数（请参见下文了解如何进行此操作）
* `client_id` → 映射到 `client_id` 输入参数
* `code` → 映射到 `authorization_code` 输入参数

9. 要映射输入参数，请在字段中键入 **@**，然后选择 **输入参数**。找到相关参数，选择它，然后选择下面的 **添加**。

![输入参数映射](../../../images/foundry/sap/webhook-mappings.png)

10. 完成的 **正文** 配置应如下所示：

![Webhook 正文](../../../images/foundry/sap/webhook-body.png)

11. 前进到 **响应** 步骤。
12. 创建以下五个 **输出参数**。所有参数都应为字符串类型，并应从响应中按键提取。

* `access_token`
* `token_type`
* `expires_in`
* `refresh_token`
* `scope`

这是创建 `access_token` 的示例。所有输出参数应遵循此模式。

![Webhook 输出参数](../../../images/foundry/sap/webhook-output.png)

13. 通过选择 **创建 webhook 并继续** 保存 webhook。

### OAuth 2.0 刷新流 webhook 设置

1. 从 **REST API** 源创建一个新的 webhook。
2. 为 webhook 命名一个不同的名称（例如“***SAP OAuth2 刷新流 webhook***”）。
3. 请求方法应再次设置为 **POST**，并使用相同的路径 (`sap/bc/sec/oauth2/token`)。
4. 与前一个 webhook 一样，如有需要，设置 `sap-client` 为 **查询参数**。
5. 在 **头** 选项卡中，添加以下头：

* `Content-Type` → `application/x-www-form-urlencoded`

![刷新 webhook 头](../../../images/foundry/sap/refresh-webhook-header.png)

6. 设置这两个 **输入参数**（均为字符串）：

* `client_id`
* `refresh_token`

7. 然后在 **正文** 选项卡下，添加以下三个条目：

* `grant_type` → `refresh_token`
* `client_id` → 映射到 `client_id` 输入参数
* `refresh_token` → 映射到 `refresh_token` 输入参数

![刷新 webhook 正文](../../../images/foundry/sap/refresh-webhook-body.png)

8. 创建与授权代码流 webhook 完全相同的五个 **输出参数**。所有参数都应为字符串类型，并应从响应中按键提取。

* `access_token`
* `token_type`
* `expires_in`
* `refresh_token`
* `scope`

9. 通过选择 **创建 webhook 并继续** 保存 webhook。

### 外部应用程序设置

1. 导航到 **Foundry 控制面板** 并选择 **外部应用程序**。
2. 为应用程序命名，然后按照[本地 OAuth 服务器的配置选项](/zh/foundry/administration/configure-outbound-applications/#configuration-options-for-on-premise-oauth-servers)中概述的步骤进行操作。
3. 之前创建的两个 webhook 应分别用作 **令牌 webhook** 和 **刷新令牌 webhook**。
4. **授权页面 URL** 应为以下形式：

```
https://<SAP_DOMAIN>/sap/bc/sec/oauth2/authorize
```

这个URL用于SAP系统中OAuth2授权过程的端点。
5\. 在 **OAuth 2.0 设置**下，将 **Client ID** 设置为 SAP OAuth 2.0 服务器配置中的客户端 ID。在 **Scopes** 下，添加 `/PALANTIR/SRV_0001`。
6\. 保存出站应用程序。
7\. 现在可以在创建 SAP webhook 时使用此出站应用程序。
