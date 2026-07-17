---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-connection/architecture/",
  "title": "代理架构",
  "page_id": "architecture",
  "category_id": "data-integration",
  "section_id": "data-connection",
  "previous": "/zh/foundry/data-connection/core-concepts/",
  "next": "/zh/foundry/data-connection/initial-setup-overview/",
  "scraped_at": "2026-07-13T05:30:16.749960+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 代理架构

:::callout{theme="warning"}
仅在配置[源运行时](/zh/foundry/data-connection/core-concepts/#runtimes)以连接到本地系统时才需要数据连接代理。当数据源可以通过互联网访问时，优先使用[直接连接](/zh/foundry/data-connection/core-concepts/#direct-connections)。
:::

数据连接代理是一个在客户网络中运行在客户控制的主机上的 Foundry 控制应用程序。

* **数据连接应用程序**使授权用户能够配置、探索和运行同步以同步到 Foundry。
* [**代理工作器**](/zh/foundry/data-connection/agent-worker-runtime/)是一个实际执行数据同步的服务，包括执行操作、运行同步、将数据上传到 Foundry 和缓存元数据。
* [**代理代理**](/zh/foundry/data-connection/agent-proxy-runtime/)是一个为 Foundry 中的服务提供网络连接以连接到代理网络中的源系统的服务。
* **协调器**负责配置和执行告知代理如何同步数据的任务。它位于 Foundry 云隔离区。

代理仅通过 HTTPS 从客户网络到 Foundry 平台的单向出站连接与协调器通信。在*代理代理*模式下，这些出站连接用于为 Foundry 内的服务提供双向网络连接。

![架构图](/resources/foundry/data-connection/data-connection-architecture.png)
