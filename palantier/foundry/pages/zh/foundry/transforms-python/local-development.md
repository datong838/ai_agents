---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/local-development/",
  "title": "设置 Python 本地开发",
  "page_id": "local-development",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/share-python-libraries/",
  "next": "/zh/foundry/transforms-python/velox-overview/",
  "scraped_at": "2026-07-13T06:07:50.298009+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 设置 Python 本地开发

可以进行 Transforms Python 仓库的本地开发，从而实现高速迭代开发。

## 为 Python 变换库设置本地开发环境

### 克隆仓库

1. 在仓库的菜单栏中，选择 **本地工作** 以打开对话框并复制给定的仓库 URL。

![仓库顶部菜单栏，右侧有“本地工作”选项。](../../../images/foundry/transforms-python/clone-repo.png)

![“本地工作”对话框。](../../../images/foundry/transforms-python/clone-repository-dialog.png)

2. 使用命令行，在本地机器上运行 `git clone <URI>` 于您选择的目录中。然后使用 `cd` 命令导航到仓库。

### 限制

* 授予用于克隆的词元是短期的并且仅可读，除了推送回到您的仓库。
* 您仍然需要将更改推送到 Foundry 以发布任务规格或工件，或者如果您希望运行检查或搭建。

### 预览

数据集预览在本地开发中是支持的。请参阅[本地预览](/zh/foundry/transforms-common/local-preview/)获取更多细节。

## 设置开发环境

### 先决条件

* 确保 Java 17 已安装，并且环境变量 `JAVA_HOME` 指向正确的 Java 安装。Java 17 可以从 [Oracle 网站 ↗](https://www.oracle.com/java/technologies/downloads/#java17) 下载。

:::callout{theme="neutral"}
根据您的操作系统设置 `JAVA_HOME` 环境变量：

* Windows: 在 PowerShell 中运行 `SETX JAVA_HOME -m "<java-home-dir>"`。这会修改系统环境变量，您需要重启 shell 以使更改生效。或者，您可以运行 ` [System.Environment]::SetEnvironmentVariable("JAVA_HOME", "<java-home-dir>")` 在运行进程中设置 `JAVA_HOME`。
* Linux 或 macOS: 运行 `export JAVA_HOME=<java-home-dir>`。
:::

* 确保您的仓库已升级到最新的模板版本，按照[此处](/zh/foundry/code-repositories/repository-upgrades/#manual-branch-upgrade)概述的步骤进行。

* 确保环境变量 `CI`、`JEMMA` 和 `CA` 没有设置。

* 如果在 Apple silicon Mac 上运行，确保安装了 [Rosetta 2 ↗](https://developer.apple.com/documentation/apple-silicon/about-the-rosetta-translation-environment)。您可以通过在终端中运行 `/usr/sbin/softwareupdate --install-rosetta --agree-to-license` 来安装 Rosetta 2。

## Visual Studio Code

* 确保您已安装 [Visual Studio Code ↗](https://code.visualstudio.com/)。
* 从 Visual Studio Code 网站或应用程序中的 **扩展** 选项卡安装 [Python 扩展 ↗](https://marketplace.visualstudio.com/items?itemName=ms-python.python)。
* 如果在您的注册中启用，安装适用于 Visual Studio Code 的 [Palantir 扩展](/zh/foundry/palantir-extension-for-visual-studio-code/overview/) \[Beta]。

### 要求

:::callout{theme="warning" title="Beta"}
适用于 Visual Studio Code 的 Palantir 扩展处于 beta 状态，在您的注册中可能不可用。
:::

要使用适用于 Visual Studio Code 的 Palantir 扩展，您必须在您的注册中拥有对 [代码仓库](/zh/foundry/code-repositories/overview/) 的访问权限。

:::callout{theme="neutral"}
如果您看到意外的语言服务器出错，例如导入出错，可能是 Python 解释器的自动设置失败。要解决此问题，您可以通过导航到 [命令面板 ↗](https://code.visualstudio.com/docs/getstarted/userinterface#_commandpalette)，然后输入 `Python: Select interpreter` 并选择匹配路径的 Python 解释器：`./maestro/bin/python` 来手动设置解释器。如果 Palantir 扩展成功运行命令 **Palantir: Install Python environment**，那么 `.maestro` 文件夹应该存在。
:::

## PyCharm

* 要设置 Python 开发环境，运行命令 `./gradlew condaDevelop`。

* 确保您本地安装了 [JetBrains PyCharm ↗](https://www.jetbrains.com/pycharm/)。

* 按照 [此处 ↗](https://www.jetbrains.com/help/pycharm/open-projects.html) 概述的步骤导入项目。

* 从状态栏的 [Python 解释器选择器 ↗](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#widget) 中选择 **添加新解释器**。

  ![添加 python 解释器截图](../../../images/foundry/transforms-python/pycharm-add-python-interpreter.png)

* 在 **添加 Python 解释器** 对话框的左侧窗格中，选择 **Virtualenv 环境**。

  ![配置 python 解释器截图](../../../images/foundry/transforms-python/pycharm-configure-python-interpreter.png)

* 选择 **现有环境**，并将 **解释器** 字段设置为来自您的 Conda 环境的 Python 解释器。可以通过运行 `./gradlew condaEnvList` 列出 Conda 环境路径。
  * 对于 Unix，Python 解释器路径是 <code>\<your-conda-environment-dir>/bin/python</code>。<br/>
  * 对于 Windows，Python 解释器路径是 <code>\<your-conda-environment-dir>\python.exe</code>。

:::callout{theme="neutral"}
根据是否启用测试插件，安装的环境列表将包括 `./transforms-python/build/conda/run-env` 或 `./transforms-python/build/conda/test-env` 或两者。如果计划运行测试，应选择测试环境。
:::

* 选择 **确定**。

### （高级设置）基于 Gradle 的环境

如果适用于 Visual Studio Code 的 Palantir 扩展在您的注册中不可用，可以使用 Gradle 来设置 Python 环境。在新的终端窗口中，使用 `cd` 命令导航到仓库目录，然后运行 `./gradlew vsCode`。这将创建一个 Python 环境，并通过将其放置在 `.vscode/setting.json` 文件中来配置 Visual Studio Code 使用该环境的 Python 解释器。
