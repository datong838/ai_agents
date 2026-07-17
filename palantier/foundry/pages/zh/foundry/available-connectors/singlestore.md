---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/singlestore/",
  "title": "SingleStore",
  "page_id": "singlestore",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/shopify/",
  "next": "/zh/foundry/available-connectors/slack/",
  "scraped_at": "2026-07-13T05:37:41.459791+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# SingleStore

SingleStore连接器是一个[Palantir提供的驱动](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。该驱动的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/JMJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域 | 必需 |
|--- |--- |
| \<Server>:\<Port> | 仅当`UseSSH=FALSE,`服务器支持列出多个地址时（即，`Server='192.168.1.100,192.168.1.101'）` |
| 无 | 始终。端口支持列出多个地址（即，`Port='3306,` 3307'）；默认`Port=3306` |
| \<SSHServer>:\<SSHPort> | 仅当`UseSSH=TRUE,` 默认`SSHPort=22` |
