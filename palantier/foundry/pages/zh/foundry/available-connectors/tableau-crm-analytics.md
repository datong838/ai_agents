---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/tableau-crm-analytics/",
  "title": "Tableau CRM 分析",
  "page_id": "tableau-crm-analytics",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/sybaseiq/",
  "next": "/zh/foundry/available-connectors/tally/",
  "scraped_at": "2026-07-13T05:37:56.156340+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Tableau CRM 分析

Tableau CRM 分析连接器是一个[Palantir 提供的驱动](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/FSJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，代理必须被允许连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域 | 必需 |
|--- |--- |
| \<InstanceURL> | 始终。由 Salesforce 在身份验证时返回；可以通过 InstanceURL 属性设置，当 `InitiateOAuth=OFF` 时 |
| login.salesforce.com | 仅当 `UseSandbox=FALSE` 且子域为空时 |
| test.salesforce.com  | 仅当 `UseSandbox=TRUE` 时 |
| \<Subdomain>.cloudforce.com | 仅当子域连接属性用于自定义品牌身份验证页面时 |
