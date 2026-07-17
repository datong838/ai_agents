---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/zoho-inventory/",
  "title": "Zoho Inventory",
  "page_id": "zoho-inventory",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/zoho-crm/",
  "next": "/zh/foundry/available-connectors/zoho-projects/",
  "scraped_at": "2026-07-13T05:38:21.036754+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Zoho Inventory

Zoho Inventory 连接器是一个[Palantir 提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。此驱动程序的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/KZJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名  | 必须 |
|--- |--- |
| inventory.zoho.\<Region> | 始终。区域连接属性映射到 TLD（默认 `Region=US` --> .com） |
| \<AccountsServer> - 默认: accounts.zoho.\<Region> | 始终。通过 OAuth 流程自动检索；在手动提供 OAuthAccessToken 时设置在 AccountsServer 连接属性中 |

### 区域映射

使用以下区域映射来完成域名 URL：

| 区域  | 终端 |
|--- |--- |
| 美国 | .com |
| 欧洲 | .eu |
| 印度 | .in |
| 澳大利亚 | .com.au |
