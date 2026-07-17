---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/container-overview/",
  "title": "概述",
  "page_id": "container-overview",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/palantir-provided-models/",
  "next": "/zh/foundry/transforms-python/transforms-sidecar/",
  "scraped_at": "2026-07-13T06:07:52.386966+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

:::callout{theme="warning" title="先决条件"}
以下文档假定您具有容器化基础设施和容器镜像等概念的工作知识。如果您不熟悉这些主题，我们建议您查看 [Docker 概述文档 ↗](https://docs.docker.com/get-started/)。
:::

Foundry 以两种方式与推送到平台的容器进行交互：

1. 使用 [transforms sidecar 装饰器](/zh/foundry/transforms-python/transforms-sidecar/)。
2. 构建和使用[容器支持的模型资产](/zh/foundry/integrate-models/upload-image-container-model/)。

在这两种应用案例中，第一步都是将镜像推送到 Foundry 内托管的 Docker 注册表，同时遵循以下列出的镜像要求。

## 镜像要求

1. 镜像具有数字 `userID`。

* Dockerfile 中定义的 `userID` 必须是数字且不能为 '0'。Foundry 不允许在容器中以 root 用户身份运行命令；在某些系统中，'0' 被解释为零，非数字 ID 可以设置为以 root 身份运行。

2. 镜像为 `linux/amd64` 平台构建。

* Foundry 仅支持为此平台构建的容器执行。Docker 的默认平台是 `linux`，因此请在 [Docker 构建命令 ↗](https://docs.docker.com/engine/reference/commandline/build/) 中添加 `--platform linux/amd64` 以专门设置平台。

3. 镜像以 `digest` 或任何非 `latest` 的标签推送。

* 执行的 Docker push 命令应指定镜像的 digest 或使用非 `latest` 的标签。Foundry 不会执行标记为 `latest` 的镜像，因为没有机制确保任何给定的镜像实际上是最新的。

4. 最大镜像层大小小于约 10 GB。

* 强烈建议每个层小于约 10 GB。如果您的应用案例需要更大的层大小，请联系您的 Palantir 代表。

5. 暴露的端口在 1024 到 65535 之间。

* 端口 0 到 1023 是众所周知的端口，因此保留给 root。Foundry 不允许在容器中以 root 用户身份运行命令；因此，指定在此范围内的任何端口在镜像在 Foundry 中启动时将不可用。

6. \[非必填] 镜像启用了遥测。

* 要启用来自容器的遥测日志记录：
  * 镜像必须在 `/bin/sh` 中有一个 shell 可执行文件。
  * 镜像必须支持 shell 命令 `set` 和 `tee`。
