---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/smb/",
  "title": "服务器消息块 (SMB)",
  "page_id": "smb",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/smartsheet/",
  "next": "/zh/foundry/available-connectors/snapchat-ads/",
  "scraped_at": "2026-07-13T05:37:45.758529+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 服务器消息块 (SMB)

连接到服务器消息块 (SMB) 共享，以在文件夹和Foundry数据集中同步数据。常见的SMB服务器示例包括Windows文件服务器和Samba文件服务器。

## 支持的功能

| 功能  | 状态 |
|--- |--- |
| 探索 | 🟢 普遍可用 |
| 批量导入 | 🟢 普遍可用 |
| 增量 | 🟢 普遍可用 |
| [文件导出](/zh/foundry/data-connection/export-overview/#file-exports) | 🟢 普遍可用 |

SMB连接器支持SMB协议版本2和3。

## 数据模型

连接器可以将任何类型的文件传输到Foundry数据集中。文件格式会被保留，传输过程中或之后不会应用任何模式。将任何必要的模式应用到输出数据集，或[编写下游变换](/zh/foundry/pipeline-builder/transforms-overview/)以访问数据。

## 性能和限制

可传输文件的大小没有限制。然而，网络问题可能导致大规模传输的失败。特别是，运行超过两天的直接云同步将被中断。为避免网络问题，我们建议使用较小的文件大小，并限制每次同步执行中摄取的文件数量。可以[安排](/zh/foundry/data-connection/set-up-sync/#configure-sync)频繁运行同步。

## 设置

1. 打开[数据连接](/zh/foundry/data-connection/overview/)应用程序，并在屏幕右上角选择 **+ 新建源**。
2. 从 **协议源** 部分选择 **SMB**。
3. 选择使用[**直接连接**](/zh/foundry/data-connection/set-up-direct-connection/)通过互联网连接，或[**通过中介代理**](/zh/foundry/data-connection/set-up-agent/)进行连接。
4. 按照下面各节中的信息，继续设置连接器的附加配置提示。

了解更多关于在Foundry中[设置连接器](/zh/foundry/data-connection/set-up-source/)的信息。

### 配置选项

SMB连接器提供以下配置选项：

| 选项  | 必需?  | 描述 |
|--- |--- |---  |
| `Hostname` | 是 | 指向服务器的域名或服务器的IP地址。 |
| `Port` | 否 | SMB服务器运行的端口。 |
| `Share` | 是 | 您要连接的SMB共享名称。 |
| `Username` | 是 | SMB登录用户名。 |
| `Password` | 是 | SMB登录密码。 |
| `Domain` | 否 | SMB登录账户的活动目录域。如果登录账户不是AD用户，请留空。 |

### 网络

SMB连接器必须能够在`Port`（默认445）上访问`Hostname`。如果您使用直接连接，必须使用[TCP策略](/zh/foundry/administration/configure-egress/#tcp-policies)。

## 从SMB同步数据

SMB连接器使用[基于文件的同步接口](/zh/foundry/data-connection/file-based-syncs/)。

## 导出数据到SMB

要以SMB共享导出，首先为您的SMB连接器[启用导出](/zh/foundry/data-connection/export-overview/#enable-exports-for-source)。然后，[创建一个新的导出](/zh/foundry/data-connection/export-overview/#creating-a-new-export)。

### 导出配置选项

| 选项  | 必需? | 默认值 | 描述 |
|--- |--- |--- |--- |
| `Directory path` | 是 | / | SMB共享中应导出文件的文件夹路径。导出文件的完整路径计算为 `<Share>/<Directory Path>/<Exported File Path>` |
