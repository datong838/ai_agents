---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/databricks/",
  "title": "Databricks",
  "page_id": "databricks",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/couchbase/",
  "next": "/zh/foundry/available-connectors/docusign/",
  "scraped_at": "2026-07-13T05:35:24.766794+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Databricks

连接Foundry到Databricks，以读取和同步Databricks与Foundry之间的数据。

## 支持的功能

| 功能 | 状态 |
| --- |--- |
| 探索 | 🟢 普遍可用 |
| 批量导入 | 🟢 普遍可用 |
| 增量 | 🟢 普遍可用 |

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序，并在屏幕右上角选择\*\*+ 新建来源\*\*。
2. 从可用的连接器类型中选择**Databricks**。
3. 选择通过互联网使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)或通过[中介代理](/zh/foundry/data-connection/set-up-agent/)进行连接。
4. 按照附加配置提示，使用以下部分中的信息继续设置您的连接器。

了解有关在Foundry中[设置连接器](/zh/foundry/data-connection/set-up-source/)的更多信息。

### 配置选项

Databricks连接器提供以下配置选项：

| 选项  | 是否必需?  | 描述 |
|--- |--- |---  |
| `Hostname` | 是 | Databricks计算资源的服务器主机名值。 |
| `HTTP Path` | 是 | Databricks计算资源的HTTP路径值。 |

请参考[官方Databricks文档 ↗](https://docs.databricks.com/integrations/compute-details.html)以获取有关如何获取这些值的信息。

### 认证

您可以通过以下方式认证到Databricks：

1. **个人访问词元:** 使用个人访问词元以Databricks用户身份进行认证。更多信息请参见[官方Databricks文档 ↗](https://docs.databricks.com/dev-tools/auth/pat.html)。
2. **OAuth 机器对机器 (M2M):** 使用客户端ID和密钥以Databricks服务主体进行认证。更多信息请参见[官方Databricks文档 ↗](https://docs.databricks.com/dev-tools/auth/oauth-m2m.html)。
3. **基本:** 使用用户名和密码以Databricks用户身份进行认证。基本认证是遗留认证方式，不推荐在生产中使用。更多信息请参见[官方Databricks文档 ↗](https://docs.databricks.com/dev-tools/auth/basic.html)。

### 网络

Databricks连接器需要对[配置选项](#configuration-optons)中提供的`Hostname`在端口443上的网络访问。如果您使用通过互联网的直接连接，请确保存在一个[出口策略](/zh/foundry/administration/configure-egress/)。对于代理运行时，运行代理的服务器必须能够访问该域。
