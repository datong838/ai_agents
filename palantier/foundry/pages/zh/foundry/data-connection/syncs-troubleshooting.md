---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/syncs-troubleshooting/",
  "title": "故障排除参考",
  "page_id": "syncs-troubleshooting",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/optimize-jdbc-syncs/",
  "next": "/zh/foundry/data-connection/push-based-ingestion/",
  "scraped_at": "2026-07-13T05:31:46.677863+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 故障排除参考

本页描述了一些与同步相关的常见问题及调试步骤：

* [PKIX 和 SSL 异常](#pkix-and-ssl-exceptions)
* [出口代理问题](#egress-proxy-issues)
* [增量 JDBC 同步问题](#incremental-jdbc-syncs)
* [间歇性同步失败或挂起](#intermittent-sync-failures-or-hangs)
* [同步开始失败](#a-sync-started-failing)
* [同步了意外的数据](#unexpected-data-was-synced)

## PKIX 和 SSL 异常

当代理没有正确的证书时，会发生 PKIX 异常和其他 `SSLHandshakeException`，因此无法与源进行身份验证。为了确保您安装了正确的证书，请按照我们[数据连接和证书](/zh/foundry/data-connection/agent-configuration-reference/#certificates)文档中的指南进行操作。

如果您的同步因错误 `Response 421 received. Server closed connection` 而失败，这表明您可能正在使用不受支持的 SSL 协议/端口组合进行连接。例如，端口 991 上的隐式 FTPS 是一种过时且不受支持的标准。在这种情况下，首选方法是通过端口 21 的显式 SSL。

## 出口代理问题

### FTP 同步

如果您的同步是 FTP/S 同步，请确保您没有使用出口代理负载均衡器。FTP 是一种有状态协议，因此如果连续请求不是来自同一 IP，使用负载均衡器可能会导致同步失败。

请注意，由于负载均衡的性质，故障将是不确定的；即使在负载均衡代理存在的情况下，同步和预览有时也可能成功。

### S3 同步

如果您的同步或探索因错误 `com.amazonaws.services.s3.model.AmazonS3Exception:Forbidden (Service: Amazon S3; Status Code: 403; Error Code: 403 Forbidden; Request ID: null; S3 Extended Request ID: null)` 而失败，这意味着命令在通过出口代理时出错。如果您收到此错误，您应检查以下场景是否适用：

* 区域字段为空。当您连接的 S3 存储桶与代理位于不同的区域时，这是必需的。
* 由于未被列入白名单，STS 无法访问。
* 由于未被列入白名单，S3 URL 无法访问。
* STS 凭证无效或您无法承担 IAM 角色。
* 同步需要使用 VPC 而不是代理；为了解决 S3 端点，地址必须通过添加以下配置从代理中排除：
  * 在 S3 源 proxyConfiguration 块中添加：

    ```yaml
    host: <address of deployment gateway or egress NLB>
    port: 8888
    protocol: http
    nonProxyHosts: <bucket>.s3.<region>.amazonaws.com,s3.<region>.amazonaws.com,s3-<region>.amazonaws.com
    ```

    例如：将所有 VPC 存储桶列入白名单将涉及配置添加：

    ```yaml
    clientConfiguration:
         proxyConfiguration:
            host: <color>-egress-proxy.palantirfoundry.com
            port: 8888
            protocol: http
            nonProxyHosts: *.s3.<region>.amazonaws.com, s3.<region>.amazonaws.com, s3-<region>.amazonaws.com
    ```

## 增量 JDBC 同步问题

要查看在您的源系统上运行的确切查询，请参阅 `_data-ingestion.log`。

如果您的同步是增量同步，请确保您提供了一个单调递增的列（例如时间戳或 id）以及该列的初始值。

选择增量列后，您需要确保在同步配置页面的 `SQL` 查询中添加了 `?` 运算符（`?` 将替换为“增量”值，并且只能使用一个 `?`）。例如，`SELECT * FROM table WHERE id > ?`。

#### 缺失行和未更新的行

如果您认为同步的数据集中缺少某些行或先前同步的行未被正确更新，请检查以下内容：

* 如果新行被添加到现有数据集中，并且新行中存储在增量列中的值小于当前游标，则不会同步新行。
  * 例如，如果您使用 `ID` 作为单调递增的列，并且上次同步中同步的最后一个 `ID` 值是 10，然后添加了一个 `ID` 为 5 的行，则该 `ID` 为 5 的行将不会被同步。
* 如果由于上述原因而未同步某些行，您仍然可以通过以下任一方式同步这些行：
  * 执行快照同步而不是增量同步，或
  * 调整查询以定位缺失的行，并将其作为一次性运行。

#### 重复行

如果您认为现有行正在被重新同步，请检查以下内容：

* 如果源数据库中的现有行被更新，并且这些行的增量列发生更改，使其大于当前游标，则这些行将被重新同步，从而导致重复。例如，如果您用作增量列的列是一个时间戳，表示行被插入或最后更新的时间，并且您在数据集同步之间更新了一行，则该更新的行将被重新同步。
  * 如果由于上述原因存在重复行，您可以通过以下任一方式删除它们：
    * 执行快照同步而不是增量同步，或
    * 使用下游变换来删除重复行。
* 如果您选择的增量列的数据类型是时间戳，并且它使用亚毫秒精度，则重复行将被重新同步。这是因为当前增量 JDBC 同步仅将时间戳值序列化到毫秒精度，并且增量值始终向下舍入到最近的毫秒。因此，具有微秒和/或纳秒精度的行将始终被重新同步，因为与当前（向下舍入）增量值的比较始终为“正”。
* 如果由于上述原因存在重复行，您需要将增量列转换为 `LONG` 或 `STRING`（ISO-8601 格式）。

#### 增量同步时抛出 NullPointerException

如果在增量同步时抛出 NullPointerException，这可能表明 SQL 查询正在从数据库中检索行，这将导致增量列包含空值。

* 例如，考虑查询 `SELECT * FROM table WHERE col > ? OR timestamp > 1`，其中 `col` 是用于同步的增量列。使用 `OR` 表示查询不保证 `col` 仅包含非空值。如果同步的任何行的 `col` 值为空，则在数据连接尝试更新同步的增量状态时，当前状态将与同步的空值进行比较并抛出错误。
* 为了解决此类情况，可以选择不同的增量列，或者确保当前增量列不会同步空值。对于上述查询，我们可以通过重写 `SELECT * FROM table WHERE (col > ? OR timestamp > 1) AND col IS NOT NULL` 来避免错误。

:::callout{theme="neutral"}
如果您希望更改用于同步的增量列，我们建议您创建一个新的同步。
:::

## 间歇性同步失败或挂起

#### 检查您的代理是否资源不足

在代理主机上的 `<bootvisor-directory>/var/data/processes` 目录中，运行 `ls -lrt` 以找到最近创建的 `bootstrapper~<uuid>` 目录。

* `cd` 进入该目录并导航到 `/var/log/`。
* 查看 `magritte-agent-output.log` 的内容。

如果您看到错误 `OutOfMemory Exception`，这意味着代理无法处理指派给它的工作负载。

* 为了解决此问题，您可能需要增加 "代理堆大小" 参数，可以在代理概览页面上完成。但是，在执行此操作之前，我们建议您阅读代理故障排除参考指南中的[调整堆大小](/zh/foundry/data-connection/agents-troubleshooting/#agent-status-shows-unhealthy)的说明。
* 如果您无法增加代理的堆大小，您可能需要减少 "最大并发同步" 参数。这也可以在代理概览页面上完成。

#### 同步挂起

以下是一些常见的同步挂起原因及其相关解决方法：

**所有同步：在获取阶段挂起**

如果您的同步在获取阶段挂起，请检查源是否可用并正常运行：

* 要检查源是否可用，请尝试连接并与源交互（不使用您的代理或其他 Foundry 产品）。如果您能够成功连接并且查询按预期运行，请联系您的 Palantir 代表以获得进一步帮助。
* 如果您发现无法连接到源或发送到源的查询响应缓慢，则可能是源正在经历比正常情况下更高的流量或已经关闭。为减轻繁忙源的影响，我们建议您采取以下措施：
  * 将您的同步分解为较小的同步。
  * 使用增量同步（如果适用）。
  * 在您知道源不会繁忙的时间安排同步。

**JDBC 同步：在获取阶段挂起**

如果您的同步完成获取阶段的时间比预期长，这可能是因为代理正在进行大量网络和数据库调用。为了调整同步期间进行的网络和数据库调用次数，您可以更改 `Fetch Size` 参数：

* `Fetch Size` 参数位于源配置的“高级选项”部分内，定义了每次数据库往返期间获取的行数。因此：
  * 减少 `Fetch Size` 参数将导致每次对数据库的调用返回较少的行，并且需要更多的调用。但是，这意味着代理将使用更少的内存，因为在代理的堆中同时存储的行更少。
  * 增加 `Fetch Size` 参数将导致每次对数据库的调用返回更多的行，并且需要更少的调用。但是，这意味着代理将使用更多的内存，因为在代理的堆中同时存储的行更多。
  * 我们建议从 `Fetch Size`: 500 开始，并根据需要进行调整。

**JDBC 同步：在上传阶段挂起**

如果您的同步在上传文件时花费的时间过长或在上传阶段失败，则可能是由于网络链接过载。在这种情况下，我们建议调整 `Max file size` 参数：

* `Max file size` 参数位于源配置的“高级选项”部分内，定义了上传到 Foundry 的输出文件的最大大小（以字节或行为单位）。因此：
  * 减少 `Max file size` 参数可能会增加网络压力，因为较小的文件会更频繁地上传；如果文件上传失败，重新上传的成本较低。
  * 增加 `Max file size` 参数将需要更少的总带宽，但这种上传更容易失败。
  * 我们建议 `Max file size`: 120mb。

**FTP / SFTP / 目录 / 同步：在获取阶段挂起**

文件同步在获取阶段挂起的最常见原因是代理正在爬行一个大型文件系统。

* 为了避免长时间的爬行，请确保您已在源配置页面中指定了要爬行的子文件夹。
  * 注意：任何正则表达式筛选器都将在相对于源根目录的文件路径上运行。
* 如果未指定子文件夹，同步将爬行源根目录。

:::callout{theme="neutral"}
爬行文件系统的同步将对文件系统进行两次完整爬行（除非另有配置）。这是为了确保同步不会上传正在被写入或以任何方式被修改的文件。
:::

#### 如果您的同步因 `REQUEST_ENTITY_TOO_LARGE` 错误而失败

下载、处理和上传大文件容易出错且缓慢。如果单个文件超过为代理的上传目标配置的最大大小，则会发生 `REQUEST_ENTITY_TOO_LARGE` 服务异常。对于 `data-proxy` 上传策略，默认设置为 100GB。

不建议覆盖此限制；如果可能，请找到一种以较小文件集合的方式访问此数据的方法。但是，如果您希望将此限制作为临时解决方案覆盖，请按照以下步骤操作：

1. 在数据连接中，导航到您的代理并选择 **高级** 配置选项卡。
2. 选择“代理”选项卡。
3. 在 destinations 块下，包含以下内容以将限制增加到 150Gb：

   ```yaml
   uploadStrategy:
       type: data-proxy
       maximumUploadedFileSizeBytes: 161061273600
   ```

## 同步开始失败

#### 如果您的同步因 `BadPaddingException` 错误而失败

`BadPaddingException` 异常是由于存储在代理中的源凭证加密密钥与预期不符。这通常发生在代理管理器手动升级时，但旧的 `/var/data` 目录未复制到新安装位置。

解决此问题的最简单方法是重新输入受影响代理所用源的凭证。

## 同步了意外的数据

#### 如果您的 JBDC 同步中的时间戳列在 Foundry 中显示为 Long 列

当从 JDBC 源同步行时，如果它们包含时间戳列，这些时间戳列将在 Foundry 中转换为 long 列。此行为是出于向后兼容性原因。

要修正这些列的数据类型，我们建议使用 [Python 变换](/zh/foundry/transforms-python/overview/) 环境来执行此清理。以下是一个将列 `"mytimestamp"` 转换回时间戳形式的示例代码片段：

```python
df = df.withColumn("mytimestamp", (F.col("mytimestamp") / 1000).cast("timestamp"))
# 将 "mytimestamp" 列的值除以1000，以转换毫秒为秒，然后将结果转换为时间戳格式
```
