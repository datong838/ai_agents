---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/filesystem/",
  "title": "代理级文件系统",
  "page_id": "filesystem",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/adp/",
  "next": "/zh/foundry/available-connectors/airtable/",
  "scraped_at": "2026-07-13T05:34:38.665845+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 代理级文件系统

存储在[代理](/zh/foundry/data-connection/core-concepts/#agents)磁盘上的文件可以使用文件系统源类型同步到Foundry中。

这种源类型可以通过在代理主机上挂载NFS或NAS并适当地配置根目录，将数据从[网络文件系统↗](https://en.wikipedia.org/wiki/Network_File_System) (NFS) 或[网络附加存储↗](https://en.wikipedia.org/wiki/Network-attached_storage) (NAS) 同步到Foundry中。

## 支持的功能

| 功能  | 状态 |
|--- |--- |
| 探索 | 🟢 一般可用 |
| 批量导入 | 🟢 一般可用 |
| 增量 | 🟢 一般可用 |
| [文件以导出](/zh/foundry/data-connection/export-overview/#file-exports) | 🟢 一般可用 |

## 配置

| 参数  | 必需? | 默认值 | 描述 |
|--- |--- |--- |--- |
| `rootDirectory` | Y | | 包含数据的根目录。 |
| `fileMustNotChangeDuration` | N | `PT2.0S` | 文件在被考虑上传之前必须保持不变的时间量（以[ISO-8601 ↗](https://docs.oracle.com/javase/8/docs/api/java/time/Duration.html#parse-java.lang.CharSequence)）。<br>注意：如果可能，使用更高效的`lastModifiedBefore`处理器。 |

**示例：**

```yaml
myDirectorySource:
    type:           directory  # 数据源类型为目录
    rootDirectory:  /foo/bar   # 根目录路径
```

:::callout{theme="neutral"}
数据连接排除所有符号链接，无论这些链接是指向文件还是文件夹。
:::
