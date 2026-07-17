---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/sage-300/",
  "title": "Sage 300",
  "page_id": "sage-300",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/sage-200/",
  "next": "/zh/foundry/available-connectors/sage-50-uk/",
  "scraped_at": "2026-07-13T05:37:23.898316+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Sage 300

Sage 300 连接器是一个[由Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动程序的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/GTJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须被配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名  | 必需 |
|--- |--- |
| \<URL> | 总是。URL连接属性，格式为{protocol}://{host-application-path}/v{version}/{tet}/ (例如，`http://localhost/Sage300WebApi/v1.0/-/`) |
