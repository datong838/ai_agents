---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/hdfs/",
  "title": "HDFS",
  "page_id": "hdfs",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/greenplum/",
  "next": "/zh/foundry/available-connectors/highrise/",
  "scraped_at": "2026-07-13T05:35:57.036002+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# HDFS

连接 Foundry 到 Hadoop 分布式文件系统 (HDFS)，以从 HDFS 读取和同步数据到 Foundry 数据集。

## 支持的功能

| 功能  | 状态 |
|--- |--- |
| 探索 | 🟢 普遍可用 |
| 批量导入 | 🟢 普遍可用 |

## 数据模型

连接器可以将任何类型的文件传输到 Foundry 数据集。文件格式将被保留，传输过程中或之后不会应用任何架构。对输出数据集应用任何必要的架构，或[编写下游变换](/zh/foundry/pipeline-builder/transforms-overview/)以访问数据。

## 性能与限制

可传输文件的大小没有限制。然而，网络问题可能导致大规模传输的失败。特别是，运行超过两天的直接云同步将被中断。为避免网络问题，我们建议使用较小的文件大小，并限制每次同步执行中摄取的文件数量。可以[安排](/zh/foundry/data-connection/set-up-sync/#configure-sync)频繁运行同步。

:::callout{theme="warning"}
通常，基于代理的运行时需要连接到 HDFS 源，除非集群可以通过互联网访问。
:::

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序，并在屏幕右上角选择 **+ 新建源**。
2. 从可用的连接器类型中选择 **HDFS**。
3. 选择使用[**直接连接**](/zh/foundry/data-connection/set-up-direct-connection/)通过互联网连接或[**通过中介代理**](/zh/foundry/data-connection/set-up-agent/)连接。
4. 按照下面各节中的信息继续设置连接器的附加配置提示。

了解更多关于在 Foundry 中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

### 网络

如果可用，我们建议使用 [HDFS 方案 ↗](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/ViewFsOverloadScheme.html)，因为其具有更快的 RPC 性能。或者，[WebHDFS ↗](https://hadoop.apache.org/docs/r1.0.4/webhdfs.html) 是一个支持 HDFS 完整文件系统接口的 HTTP REST API。一些示例包括：

* hdfs://myhost.example.com:1234/path/to/root/directory
* webhdfs://example.com/path
* swebhdfs://example.com/path

:::callout{theme="warning"}
所需的网络端口将因选择的方案而异。对于 HDFS 方案，这些端口通常是 NameNode 服务器上的 8020/9000 和 DataNode 上的 1019、50010 和 50020。对于 WebHDFS 方案，所需端口通常是 9820。
:::

### 证书和私钥

SSL 连接验证服务器证书。通常，SSL 验证通过证书链发生；默认情况下，代理和直接连接运行时都信任大多数行业标准证书链。如果您正在连接的服务器有自签名证书，或者在验证期间有 TLS 拦截，则连接器必须信任证书。了解更多关于在数据连接中[使用证书](/zh/foundry/data-connection/agent-configuration-reference/#certificates)的信息。

## 配置选项

以下配置选项可用于 HDFS 连接器：

| 选项  | 必需?  | 描述 |
|--- |--- |---  |
| `URL` |  是  |  到根数据目录的 HDFS URL  |
| `额外属性` | 否 |  添加传递给 [Hadoop 配置 ↗](https://hadoop.apache.org/docs/r2.7.1/api/org/apache/hadoop/conf/Configuration.html) 的属性映射。每个条目是对应单个属性的名称和值对，避免需要通过 `configurationResources` 在磁盘上指定配置。|

### 高级选项

以下高级选项可用于 HDFS 连接器：

| 选项  | 必需?  | 描述 |
|--- |--- |---  |
| `用户` | 否 |  HDFS 用户（默认为代理运行时当前登录的用户）。<br>`user` 参数会覆盖数据连接的全局 Kerberos 设置。如果您正在使用 Kerberos，请留空 `user` 参数。|
| `文件更改超时` | 否 | 在被视为上传之前文件必须保持不变的时间量（以 [ISO-8601 ↗](https://docs.oracle.com/javase/8/docs/api/java/time/Duration.html#parse-java.lang.CharSequence) 表示）。<br>如果可能，使用更高效的 `lastModifiedBefore` 处理器。|

## 从 HDFS 同步数据

访问 `探索` 选项卡以交互式地探索配置的 HDFS 实例中的数据。选择 `新建同步` 以定期将数据从 HDFS 拉到 Foundry 中的指定数据集。
