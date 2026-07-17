---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/available-connectors/generic/",
  "title": "通用连接器",
  "page_id": "generic",
  "category_id": "data-integration",
  "section_id": "available-connectors",
  "previous": "/zh/foundry/available-connectors/github/",
  "next": "/zh/foundry/available-connectors/gmail/",
  "scraped_at": "2026-07-13T05:35:43.984703+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 通用连接器

通用连接器可以被用于在表示连接到任意外部系统。作为一个连接器，它不直接支持其他连接器中可用的标准[功能](/zh/foundry/data-connection/core-concepts/#capabilities)。然而，当仅被用作[**在代码中使用**](/zh/foundry/data-connection/core-concepts/#use-in-code)的连接器时，它可以被用于在代码中创建这些标准功能的替代方案，包括批量同步、文件和表格以某种格式导出、流式同步、流式导出、媒体同步、webhooks等。

通过配置通用连接器与适当的运行时、凭证和以某种格式导出控制，开发人员可以使用它编写连接到任意外部系统的代码。当源所有者一起配置网络/运行时、凭证和以某种格式导出控制时，他们可以确保凭证仅与指定的外部系统一起使用，并且在建立连接的不同代码环境中强制执行权限标记。

## 支持的功能

| 功能  | 状态 |
|--- |--- |
| 在代码中使用 | 🟢 普遍可用 |

## 设置

通用连接器应从代码库环境侧边栏中的**新建连接**选项创建，而不是通过数据连接应用程序。然而，任何配置的通用连接器将在数据连接中与其他连接器一起出现。

查看[我们的外部变换教程](/zh/foundry/data-integration/external-transforms-source-based/#option-1-create-source-in-the-external-systems-sidebar)，以获取有关如何直接从代码库设置通用连接器的更多信息。

## 网络

由于通用连接器必须在代码中使用，唯一可用的运行时选项是[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)用于可接受来自Palantir入站流量的系统，以及[代理代理](/zh/foundry/data-connection/agent-proxy-runtime/)用于位于无法接受来自Palantir入站流量的私有网络中的系统。

:::callout{theme="neutral"}
仅在数据连接中配置通用连接器时可以选择代理代理运行时选项；在代码库中直接设置通用连接器时无法选择此选项。
:::

## 配置选项

从概念上讲，您可以将通用连接器视为一组**网络配置**、**凭证**和**可导出的权限标记**的集合，旨在一起使用。

* **网络配置**指定使用此通用连接器从代码中应可访问哪个系统。
* **凭证**指定必须可用的秘密值以成功连接。
* **可导出的权限标记**指定哪些数据可以安全地离开Palantir平台到指定的网络目的地。

为了提供上述功能，通用连接器提供以下配置选项：

| 选项  | 是否必需?  | 描述 |
|--- |--- |---  |
|`网络` |  是  | 如果选择了[直接连接](/zh/foundry/data-connection/set-up-direct-connection/)运行时，则通用连接器支持选择一组[出口策略](/zh/foundry/administration/configure-egress/#network-egress-policies)，规定哪些目的地址或IP应可访问。 </br></br>如果选择了[代理代理](/zh/foundry/data-connection/agent-proxy-runtime/)运行时，代码中使用的客户端必须能够通过代理代理路由流量。 |
|`凭证` | 否 | 一组键值对可用于存储凭证。目前，仅可存储秘密值。不支持未加密的值。 |
|`可导出的控制权限标记` | 否 | 如果通用连接器将与Foundry数据输入一起使用，必须启用允许以某种格式导出的设置，并且必须指定一组可导出的权限标记。有关数据连接的以某种格式导出控制的更多信息，请参阅[我们的文档](/zh/foundry/data-integration/external-transforms-source-based/#use-foundry-inputs-in-external-transforms)。|

## 在代码中使用通用连接器

本节提供有关如何从Foundry中的各种代码环境中使用通用连接器的附加信息。

| 代码环境 | 描述 |
| ---------------- | ----------- |
| [Python外部变换](#python-external-transforms) | 使用通用连接器从[Python变换](/zh/foundry/transforms-python/overview/)库连接到外部系统。 |
| [计算模块](#compute-modules) | 使用通用连接器从长时间运行的计算模块中连接。用于流式同步和导出工作流以及定制的数据输出工作流。 |
| [TypeScript函数](#typescript-functions) | 在测试中。联系Palantir支持团队以启用此功能。 |
| [Python函数](#python-functions) | 处于测试状态。联系Palantir支持团队以启用此功能。|

### Python外部变换

通用连接器可以被导入到代码库中。使用此通用连接器，您可以编写代码来访问外部系统并在源上访问凭证。

[了解有关基于源的外部变换的更多信息。](/zh/foundry/data-integration/external-transforms-source-based/)

### 计算模块

通用连接器可以被导入到[计算模块](/zh/foundry/compute-modules/overview/)中。使用此通用连接器，您可以编写与外部系统交互的计算模块。

### TypeScript函数

通用连接器可以被导入到[TypeScript函数代码库](/zh/foundry/functions/getting-started/)中。使用此通用连接器，您可以使用`fetch`直接调用外部系统。

### Python函数

通用连接器可以被导入到[Python函数代码库](/zh/foundry/functions/python-getting-started/)中。使用此通用连接器，您可以使用Python的`requests`库直接调用外部系统。

## 通用连接器的转换

如果源上仅附有一个用于端口443的DNS地址的出口策略，通用连接器可以转换为[REST API源](/zh/foundry/available-connectors/rest-apis/)。

执行此转换将使开发人员能够访问用于代码中的[内置HTTP客户端](/zh/foundry/data-integration/external-transforms-source-based/#use-the-built-in-http-client)，允许开发人员立即编写与外部系统交互的代码。

![提示将通用连接器转换为REST API源的提示框。](../../../images/foundry/available-connectors/generic-connector-conversion-into-rest-api.png)
