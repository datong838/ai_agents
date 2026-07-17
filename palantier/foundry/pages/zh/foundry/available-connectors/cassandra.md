---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/cassandra/",
  "title": "Cassandra",
  "page_id": "cassandra",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/bullhorn-crm/",
  "next": "/zh/foundry/available-connectors/certinia/",
  "scraped_at": "2026-07-13T05:35:18.074110+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Cassandra

Cassandra 连接器是一个[由Palantir提供的驱动](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。此驱动的官方文档可以在[此处 ↗](https://cdn.cdata.com/help/RCJ/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够到达目标IP地址，并且目标系统必须被配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名  | 必需 |
|--- |--- |
| \<Server>:\<Port>  | 仅当 `UseSSH=FALSE`（默认），服务器和端口连接属性（默认：localhost:9042） |
| \<LDAPServer>:\<LDAPPort> | 仅当 `AuthScheme=LDAP`（默认 `Port=389)` |
| \<SSHServer>:\<SSHPort> | 仅当 `UseSSH=TRUE`（默认 `Port=22)` |
| \<KerberosKDC>:88 | 仅当 `AuthScheme=Kerberos` |
| \<KerberosServiceKDC>:88 | 仅当 `AuthScheme=Kerberos` 且 Kerberos 拓扑使用多个领域 |
