---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/palantir-extension-for-visual-studio-code/overview/",
  "title": "Palantir扩展用于Visual Studio Code",
  "page_id": "overview",
  "category_id": "data-integration",
  "section_id": "palantir-extension-for-visual-studio-code",
  "previous": "/zh/foundry/vs-code/troubleshooting/",
  "next": "/zh/foundry/palantir-extension-for-visual-studio-code/extension-features/",
  "scraped_at": "2026-07-13T06:01:45.558035+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Palantir扩展用于Visual Studio Code

:::callout{theme="neutral"}
VS Code工作区和Palantir扩展用于Visual Studio Code与微软无关联或未经其认可。
:::

:::callout{theme="warning" title="Beta"}
Palantir扩展用于Visual Studio Code处于测试阶段，并在使用[VS Code工作区](/zh/foundry/vs-code/overview/)时默认启用。
:::

Palantir扩展用于Visual Studio Code旨在将您在[Code Repositories](/zh/foundry/code-repositories/overview/)中看到的许多功能与VS Code集成。目前它专注于提供Python变换功能。

## 访问扩展

### 从VS Code工作区

在VS Code工作区中默认提供Palantir扩展。查看[VS Code工作区文档](/zh/foundry/vs-code/overview/)以了解更多信息。

### 本地

:::callout{theme="warning"}
即使扩展在您的注册中可用，您可能没有所需的权限在本地使用该扩展。需要平台管理员启用本地扩展使用。
:::

### 1. 下载Palantir扩展

导航到Code Repositories中的任何现有库，并在屏幕右上角选择**Work locally**以下载扩展文件。如果您从未安装过该扩展，则此步骤是必需的。

:::callout{theme="warning"}
Palantir扩展用于Visual Studio Code尚未在Visual Studio Code Marketplace中提供。您目前只能从Palantir平台下载该扩展。
:::

### 2. 安装扩展

通过执行以下步骤之一安装扩展：

* 将VSIX文件拖放到VS Code的**扩展**侧边栏中，或
* 使用命令`Extensions: Install from VSIX...`

### 3. 打开Palantir代码库

安装Palantir扩展后，您应该会在VS Code侧边栏看到Palantir logo。从侧边栏，您可以执行以下操作之一：

* 打开您已克隆的Palantir库，或
* 选择**Clone a repository**以克隆新的Palantir库。为此，打开Palantir库并复制git远程URL链接。

[查看Palantir扩展用于Visual Studio Code的其他功能。](/zh/foundry/palantir-extension-for-visual-studio-code/extension-features/)。
