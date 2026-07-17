---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/amazon-dynamodb/",
  "title": "Amazon DynamoDB",
  "page_id": "amazon-dynamodb",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/alloydb/",
  "next": "/zh/foundry/available-connectors/amazon-kinesis/",
  "scraped_at": "2026-07-13T05:34:40.211352+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Amazon DynamoDB

Amazon DynamoDB连接器是一个[由Palantir提供的驱动程序](/zh/foundry/data-integration/foundry-provided-drivers/)连接器。此驱动程序的官方文档可以在[这里 ↗](https://cdn.cdata.com/help/DDH/jdbc/pg_connectionj.htm)找到。

## 网络

如果使用[代理连接](/zh/foundry/data-connection/core-concepts/#agents)，则必须允许代理连接到您选择的系统。这意味着代理必须能够访问目标IP地址，并且目标系统必须配置为允许来自代理的连接。

如果使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)，请确保将以下出口策略添加到连接器中：

| 域名 | 必需 |
|--- |--- |
| dynamodb.\<AWSRegion>.\<domain> | 始终。AWSRegion 映射 |
| sts.\<Region>.amazonaws.\<TLD> | 仅当 `AuthScheme=AwsIAMRoles,AwsMFA,TemporaryCredentials` |
| cognito-idp.\<AWSCognitoRegion>.amazonaws.\<TLD> | 仅当 `AuthScheme=AwsCognitoBasic,AwsCognitoSrp` |
| cognito-identity.\<AWSCognitoRegion>.amazonaws.\<TLD> | 仅当 `AuthScheme=AwsCognitoBasic,AwsCognitoSrp` |
| \<SSOLoginURL> | 仅当 `AuthScheme=Okta,ADFS,PingFederate,` 使用SSOLoginURL属性 |
| \<Resource> | 仅当 `AuthScheme=AzureAD,` 在SSOProperties中设置Resource |
| \<SSOExchangeURL> | 仅当 `AuthScheme=Okta` |
