---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/snowflake/",
  "title": "Snowflake",
  "page_id": "snowflake",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/snapchat-ads/",
  "next": "/zh/foundry/available-connectors/spark-sql/",
  "scraped_at": "2026-07-13T05:38:08.022563+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Snowflake

将Foundry连接到Snowflake以读取和同步Snowflake与Foundry之间的数据。

## 支持的功能

| 功能 | 状态 |
| --- |--- |
| 探索 | 🟢 一般可用 |
| 批量导入 | 🟢 一般可用 |
| 增量 | 🟢 一般可用 |
| [虚拟表](/zh/foundry/data-integration/virtual-tables/) | 🟢 一般可用 |
| 导出任务 | 🟡 即将停用 |

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序，并在屏幕右上角选择 **+ 新建来源**。
2. 从可用的连接器类型中选择 **Snowflake**。
3. 选择通过互联网使用[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)或[通过中介代理连接](/zh/foundry/data-connection/set-up-agent/)。
4. 根据以下部分中的信息，按照额外的配置提示继续设置您的连接器。

了解更多有关在Foundry中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

## 连接详情

| 选项 | 必须的? | 描述 |
| --- | --- | --- |
| `Account identifier` | 是 | 这是在“.snowflakecomputing.com”之前的标识符。有关更多详情，请参阅Snowflake的[官方文档 ↗](https://docs.snowflake.com/user-guide/admin-account-identifier)。 |
| `Roles` | 否 | 这是连接所用的默认角色，以防提供的凭据具有访问多个角色的权限。 |
| `Database` | 是 | 指定连接后要使用的默认数据库。 |
| `Schema` | 否 | 选项以指定连接后要使用的默认模式。如果未指定，将提供凭据范围内的所有模式。 |
| `Warehouse` | 否\* | 连接后要使用的虚拟仓库。在注册的[虚拟表](/zh/foundry/data-integration/virtual-tables/)情况下，这将用于任何源端计算。 |
| `Credentials` | 是 | **选项1：用户名和密码** <br /> 提供用户名和密码。我们建议使用服务凭据而不是单个用户凭据。 <br /><br /> **选项2：密钥对认证**<br />提供用户名和私钥。有关配置密钥对认证的详情，请参阅Snowflake的[官方文档 ↗](https://docs.snowflake.com/user-guide/key-pair-auth#configuring-key-pair-authentication)。 <br /><br /> **选项3：外部OAuth (OIDC)**<br />按照显示的源系统配置说明设置外部OAuth。有关外部OAuth的详情，请参阅Snowflake的[官方文档 ↗](https://docs.snowflake.com/en/user-guide/oauth-ext-custom)和[我们的文档](/zh/foundry/data-connection/oidc/)，了解OIDC如何与Foundry协作。<br /><br /> 对于所有凭据选项，请确保提供的用户和角色对目标数据库和模式具有使用权限，并对目标表具有选择权限。 <br /><br /> 在注册[虚拟表](/zh/foundry/data-integration/virtual-tables/)时，用户及其角色还应具有对仓库的使用权限。 |
| `Network Connectivity` | 是\*\* | 在Snowflake中运行 `SELECT SYSTEM$ALLOWLIST()` 并确保至少将 `SNOWFLAKE_DEPLOYMENT` 和 `STAGE` 的条目添加为Foundry中的出口策略。有关更多详情，请参阅下面的[网络](#networking)部分。 |

*\* 仓库详细信息对于同步[Foundry数据集](/zh/foundry/data-integration/datasets/)是非必填的，但对于注册[虚拟表](/zh/foundry/data-integration/virtual-tables/)是必须的。<br />*
*\*\* 网络出口策略对于直接连接是必须的，但对于基于代理的连接不是。*

## 网络

要在Snowflake和Foundry之间启用直接连接，必须在[数据连接应用程序](/zh/foundry/data-connection/overview/)中设置来源时添加适当的[出口策略](/zh/foundry/administration/configure-egress/)。

要识别要列入允许名单的Snowflake帐户的主机名和端口号，可以在Snowflake控制台中运行以下命令。确保至少将 `SNOWFLAKE_DEPLOYMENT` 和 `STAGE` 的条目添加为Foundry中的出口策略。

```sql
SELECT t.VALUE:type::VARCHAR as type,  -- 将JSON解析后的type字段转换为VARCHAR类型，并命名为type
       t.VALUE:host::VARCHAR as host,  -- 将JSON解析后的host字段转换为VARCHAR类型，并命名为host
       t.VALUE:port as port            -- 直接选择JSON解析后的port字段
FROM TABLE(FLATTEN(input => PARSE_JSON(SYSTEM$ALLOWLIST()))) AS t;
-- PARSE_JSON(SYSTEM$ALLOWLIST())解析系统白名单并将其展开为一个表格，t为临时表别名
```

请参阅Snowflake的[官方文档 ↗](https://docs.snowflake.com/sql-reference/functions/system_allowlist)以获取有关识别主机名和端口号以进行允许列表的更多信息。

:::callout{theme="neutral"}
在某些情况下（取决于您的Foundry和Snowflake环境），可能需要通过PrivateLink建立连接。通常情况下，Foundry和Snowflake由相同的CSP托管（例如，AWS-AWS或Azure-Azure）。如果您认为这适用于您的设置，请联系您的Palantir代表以获取更多指导。
:::

:::callout{theme="neutral"}
对于依赖于与您的Foundry实例位于同一区域的S3桶的出口策略，请确保您已完成我们[Amazon S3桶策略文档](/zh/foundry/administration/configure-egress/#amazon-s3-bucket-policies)中详细描述的受影响桶的额外配置步骤。
:::

## 虚拟表

本节提供了有关使用Snowflake源的[虚拟表](/zh/foundry/data-integration/virtual-tables/)的更多详细信息。当同步到Foundry数据集时，本节不适用。

| 虚拟表功能 | 状态 |
| --- | --- |
| 源格式 | 🟢 一般可用：表、视图和物化视图 |
| 手动注册 | 🟢 一般可用 |
| 自动注册 | 🟢 一般可用 |
| 下推计算 | 🟢 一般可用；通过[Snowflake Spark连接器 ↗](https://docs.snowflake.com/en/user-guide/spark-connector)可用 |
| 增量 | 🟢 一般可用：仅`APPEND` [\[1\]](#snowflake-incremental) |

使用[虚拟表](/zh/foundry/data-integration/virtual-tables/)时，请记住以下源配置要求：

* 必须将源设置为[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)。虚拟表不支持使用[中介代理](/zh/foundry/data-connection/set-up-agent/)。
* 确保如本文档[网络部分](#networking)中所述建立双向连接和允许列表。
* 如果在代码库中使用虚拟表，请参阅[虚拟表文档](/zh/foundry/data-integration/virtual-tables/#virtual-tables-in-code-repositories)以获取所需的额外源配置的详细信息。
* 必须在连接详情中指定仓库。
* 提供的凭证必须具有仓库的使用权限。

有关更多详细信息，请参阅上面的[连接详情](#connection-details)部分。

<span id="snowflake-incremental">\[1]</span> 为了启用由Snowflake虚拟表支持的管道的增量支持，确保为适当的保留期限启用了[变更跟踪 ↗](https://docs.snowflake.com/user-guide/streams-manage#enabling-change-tracking-on-views-and-underlying-tables)和[时间旅行 ↗](https://docs.snowflake.com/en/user-guide/data-time-travel#enabling-and-disabling-time-travel)。此功能依赖于[CHANGES ↗](https://docs.snowflake.com/en/sql-reference/constructs/changes)。在[Python变换](/zh/foundry/transforms-python/incremental-reference/#incrementaltransforminput)中支持`current`和`added`读取模式。这些将根据`METADATA$ACTION`列揭示变更提要的相关行。在Python变换中，将提供`METADATA$ACTION`、`METADATA$ISUPDATE`、`METADATA$ROW_ID`列。

## 数据模型

请注意，类型为[`array` ↗](https://docs.snowflake.com/en/sql-reference/data-types-semistructured#array)、[`object` ↗](https://docs.snowflake.com/sql-reference/data-types-semistructured#object)和[`variant` ↗](https://docs.snowflake.com/sql-reference/data-types-semistructured#variant)的列将被Foundry解析为类型`字符串`。这是由于源的可变类型。

例如，Snowflake数组`[ 1, 2, 3 ]`将被Foundry解释为字符串`"[1,2,3]"`。

请参阅Snowflake的[官方文档 ↗](https://docs.snowflake.com/user-guide/spark-connector-use#from-snowflake-to-spark-sql)以获取更多详细信息。
