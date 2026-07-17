---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/ftps/",
  "title": "FTP/FTPS",
  "page_id": "ftps",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/freshdesk/",
  "next": "/zh/foundry/available-connectors/github/",
  "scraped_at": "2026-07-13T05:35:40.053657+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# FTP/FTPS

连接Foundry到FTP和FTPS服务器，以在文件夹和Foundry数据集中同步数据。

## 支持的功能

| 功能  | 状态 |
|--- |--- |
| 探索 | 🟢 普遍可用 |
| 批量导入 | 🟢 普遍可用 |
| 增量 | 🟢 普遍可用 |

## 数据模型

连接器可以将任何类型的文件传输到Foundry数据集中。文件格式会被保留，传输期间或之后不会应用任何模式。请对输出数据集应用任何必要的模式，或编写一个[下游变换](/zh/foundry/pipeline-builder/transforms-overview/)以访问数据。

## 性能和限制

可传输文件的大小没有限制。然而，网络问题可能导致大规模传输的失败。特别是，运行超过两天的直接云同步将会被中断。为避免网络问题，我们建议使用较小的文件大小，并限制每次同步执行时要导入的文件数量。同步可以[定期安排](/zh/foundry/data-connection/set-up-sync/#configure-sync)运行。

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序，并在屏幕右上角选择\*\*+ 新建来源\*\*。
2. 从可用的连接器类型中选择**FTP/FTPS**。
3. 选择使用[**直接连接**](/zh/foundry/data-connection/set-up-direct-connection/)通过互联网连接，或者通过[**中介代理**](/zh/foundry/data-connection/set-up-agent/)进行连接。
4. 根据以下各节中的信息，按照附加配置提示继续设置连接器。

:::callout{theme="warning"}
要配置直接连接，Foundry必须能够通过互联网访问FTP服务器。若要访问本地FTP服务器，请选择通过代理进行连接。
:::

了解更多关于在Foundry中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

### 认证

FTP/FTPS认证通过用户名和密码完成。如果FTP用户没有连接配置的根目录权限，FTP/FTPS连接可能会失败。有关根目录的更多详细信息，请参阅[配置选项](#configuration-options)。

| 选项    | 必需？ | 描述   |
|---        |---        |---            |
| `Username` | 是 | FTP登录用户名。 |
| `Password` | 是 | FTP登录密码。此字段可为空值用于匿名登录。请联系您的服务器管理员以获取更多信息。|

### 网络

如果直接连接正在运行FTP/FTPS连接器，您必须添加一个[网络出口策略](/zh/foundry/administration/configure-egress/)以将连接列入白名单。

如果通过域名连接，出口策略应为FTP服务器域在控制端口（通常为端口21）和数据端口上创建。我们建议创建两个网络策略：一个针对控制端口的单端口策略，和一个针对数据端口的端口范围策略。数据端口由FTP服务器的管理员确定。如果尽管正确配置了出口策略，错误仍然发生，[提交一个问题](/zh/foundry/getting-started/issues/)并引用应用的策略列表。

:::callout{theme="warning"}
如果服务器的域解析为多个域和/或服务器，则所有相关域及其相关IP都需要被列入白名单。要验证服务器是否解析为多个域和/或服务器，请从终端运行命令`dig <domain>`，查看您尝试连接的服务器的答案部分。
:::

:::callout{theme="neutral"}
如果代理正在运行您的连接器，请确保代理的服务器可以与FTP/FTPS服务器建立网络连接，并且防火墙配置正确。我们建议在需要时使用[netcat ↗](https://en.wikipedia.org/wiki/Netcat)或类似工具验证网络连接。
:::

### 证书和私钥

根据以下指导配置额外的客户端或服务器证书和私钥，以正确设置您的连接器。

#### SSL和主机名验证

SSL连接验证服务器证书。通常，SSL验证通过证书链进行；默认情况下，代理和直接连接运行时信任大多数行业标准的证书链。如果您连接的服务器有一个自签名证书，或者防火墙在连接上执行TLS拦截，连接器必须信任该证书。了解更多关于[在数据连接中使用证书](/zh/foundry/data-connection/agent-configuration-reference/#certificates)的信息。

:::callout{theme="warning"}
为了SSL验证正常工作，服务器必须提供完整的证书链。可以通过运行命令`openssl s_client -connect {hostname}:{port} -showcerts -starttls ftp`来获取FTP服务器的证书链。使用OpenSSL命令行工具或任何其他可用工具验证证书链。
:::

:::callout{theme="neutral"}
如果使用FTPS，请确保FTPS服务器的证书已被添加到代理的信任库中。
:::

:::callout{theme="neutral"}
Foundry尝试对所有出口路径进行验证。然而，无法检查FTP，导致连接挂起和/或超时错误。如果尽管正确配置了出口策略，错误仍然发生，请报告一个问题并提供您想要禁用主机名验证的策略列表。
:::

#### 隐式/显式SSL

FTP服务器可以配置为支持显式或隐式SSL。运行在端口990上的服务器通常使用隐式SSL。

请与您的服务器管理员确认服务器的设置。默认情况下，连接器假定显式SSL；您可能需要为您的环境更改此设置。

### 连接要求

FTP需要`CONTROL`和`DATA`连接类型。`DATA`连接必须配置为`ACTIVE`或`PASSIVE`模式。

* **CONTROL:** 客户端到服务器
* **DATA:** 从范围中选择的数据（例如，1024–1123）
  * **PASSIVE:** 客户端到服务器
  * **ACTIVE:** 服务器到客户端
    * 仅适用于代理连接

默认FTP/FTPS连接器端口：

* FTP: 21
* FTPS显式: 21
* FTPS隐式: 990

### 主动和被动模式

我们建议使用**被动模式**的网络连接。在被动模式下，所有连接均由客户端发起。当使用被动模式时，请确保控制端口（通常为21）和数据传输的端口范围（例如1024–1123）被列入白名单。请联系您的FTP/FTPS服务器管理员以获取连接详细信息。

**主动模式**是一种较旧的文件传输建立方法。在主动模式下，客户端连接到服务器，而服务器连接到客户端。服务器和客户端相互依赖，并需要**双向**网络连接。这种网络方法在大多数安全环境中通常难以实现，并且在使用直接连接时不可能实现。

## 配置选项

| 选项  | 必需？  |  默认值   | 描述 |
|--- |--- |---  |---  |
| `URL` | 是  |   |  FTP/FTPS服务器的URL。URL可以可选地包含服务器上目录的路径，该目录将用作连接的根目录（例如，`ftp://server.name/folder/name`）。 |
| `配置客户端证书和私钥` | 否 |   | 有关更多信息，请参阅[证书和私钥](#certificates-and-private-keys)。 |
| `配置服务器证书` | 否 |   | 有关更多信息，请参阅[证书和私钥](#certificates-and-private-keys)。 |
| `连接超时` | 否 | 30秒 | 增加超时毫秒数。 |
| `重新登录时间` | 否 | 15分钟 | 修改间隔分钟数。 |
| `文件更改超时` | 否 | 2秒  | 设置文件在被视为上传前必须保持不变的时间量。超时以毫秒为单位。|
| `HTTP代理URL` | 否 |   | 代理服务器的URL，以`http://`或`https://`开头。对HTTP代理的支持高度依赖于所使用的FTP服务器，并且不能在`ACTIVE`模式下使用。这是因为HTTP代理不支持客户端请求在一个外部可访问的端口上侦听。`ACTIVE`模式传输涉及FTP服务器连接回客户端，这在HTTP代理中是不可能的。|
| `SSL方法` | 否 | 显式 | 是否为FTPS连接使用[显式或隐式SSL](#implicitexplicit-ssl)。 |
| `模式` | 否 | `PASSIVE`  | `PASSIVE`或`ACTIVE` |
| `时区` | 否 | 连接器的时区  | FTP服务器的时区。FTP记录没有时区的时间戳。要查看准确的修改时间戳，如果FTP服务器的时区与默认不同，请指定FTP服务器的时区。 |
| `时间戳格式字符串` | 否 | `MM-dd-yy hh:mma` | 用于解析FTP服务器时间戳的格式字符串。时间戳用于确定自上次同步以来修改的文件。请参阅[Java文档 ↗](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)以了解支持的格式。 |
| `控制编码` | 否 | US-ASCII | FTP控制消息的编码。当文件名的编码与数据连接服务器的默认文件系统编码不同时，控制编码可能是必要的。<br />**示例：** 在Windows FTP服务器上，`windows-31j`通常用于日语，`x-windows-949`通常用于韩语。<br /> 请参阅[Java文档 ↗](https://docs.oracle.com/javase/8/docs/technotes/guides/intl/encoding.doc.html)以获取更多信息。 |
| `保持活跃` | 否 | `false`| 选择是否发送FTP NOOP命令以保持在下载大文件时的控制连接活跃。并非所有FTP服务器都支持。|

## 从FTP同步数据

FTP连接器使用[基于文件的同步](/zh/foundry/data-connection/file-based-syncs/)界面。

## 故障排除

### 代理连接

* 您在设置代理连接时遇到问题吗？安装一个FTP/S客户端，并尝试使用与来源相同的配置连接到服务器。如果此连接失败，则问题不是连接器错误。在提交问题之前，请调查网络连接、认证和FTP服务器配置。

* 您使用的是出口代理负载均衡器吗？FTP是一种有状态协议，因此如果使用负载均衡器，当顺序请求不从同一IP发起时，会导致同步（非确定性地）失败。

### SSL和FTPS

* 您的服务器使用自签名证书吗？您是否已将其添加到来源信任库中？请参阅上面的[SSL和主机名验证](#ssl-and-hostname-validation)部分。

* 您的FTP服务器是否只支持旧版TLS版本（例如，TLS 1.1）？如果是这样，连接器运行时可能不会接受服务器提供的任何加密套件。提交一个问题与Palantir代表探讨替代方案。
