---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/zoho-projects/",
  "title": "Zoho Projects",
  "page_id": "zoho-projects",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/zoho-inventory/",
  "next": "/zh/foundry/available-connectors/zuora/",
  "scraped_at": "2026-07-13T05:38:25.183380+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Zoho Projects

Zoho Projects连接器是一个[Palantir提供的驱动](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/PZJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够访问目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域 | 必须 |
|--- |--- |
| projectsapi.zoho.\<Region> | 始终。区域连接属性映射到TLD（默认`Region=US` --> .com） |
| \<APIDomain> - 默认: zohoapis.\<Region> | 始终。通过OAuth流程自动检索；在手动提供OAuthAccessToken时设置在APIDomain连接属性中 |
| \<AccountsServer> - 默认: accounts.zoho.\<Region> | 始终。通过OAuth流程自动检索；在手动提供OAuthAccessToken时设置在AccountsServer连接属性中 |

### 区域映射

使用以下区域映射来完成域url：

| 区域 | 端点 |
|--- |--- |
| 美国 | .com |
| 欧洲 | .eu |
| 印度 | .in |
| 澳大利亚 | .com.au |
| 日本 | .jp |
| 中国 | .com.cn |
