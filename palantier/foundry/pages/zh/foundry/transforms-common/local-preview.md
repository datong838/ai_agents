---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-common/local-preview/",
  "title": "在本地开发中预览变换",
  "page_id": "local-preview",
  "category_id": "data-integration",
  "section_id": "transforms-common",
  "previous": "/zh/foundry/transforms-r/getting-started/",
  "next": "/zh/foundry/transforms-common/transforms-versions/",
  "scraped_at": "2026-07-13T06:09:51.623827+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在本地开发中预览变换

在使用VS Code进行本地开发中预览变换有两种主要方法：

* [使用适用于Visual Studio Code的Palantir扩展（Beta版）预览变换](#visual-studio-code-extension-preview-python-only)
* [使用基于Gradle的本地预览](#gradle-based-local-preview-for-java-and-python)

## 使用适用于Visual Studio Code的Palantir扩展（Beta版）进行预览（仅限Python）

适用于Visual Studio Code的Palantir扩展支持本地预览功能。有关安装说明，请参阅[扩展文档](/zh/foundry/palantir-extension-for-visual-studio-code/overview/)。一旦扩展安装完成并且环境已准备好进行预览，您的变换应自动在**预览**选项卡中被发现，如下所示。

![在Visual Studio Code扩展中Python变换库的预览功能。](../../../images/foundry/transforms-common/vscode-transforms-preview.png)

## 基于Gradle的Java和Python本地预览

本节详细介绍了在本地开发中预览Python和Java变换所需的步骤。有关更多背景信息，请查看我们的[Python本地开发](/zh/foundry/transforms-python/local-development/)和[Java本地开发](/zh/foundry/transforms-java/local-development/)文档。您还可以了解更多关于[如何预览变换](/zh/foundry/code-repositories/preview-transforms/)。

### 先决条件和限制

本地预览支持要求本地分支必须跟踪远程分支，因此本地分支至少需要被推送一次，除了现有的本地开发先决条件外。请注意以下附加限制：

* 预览URI只能由运行预览的用户访问，并且仅在临时基础上可用。

### 运行数据集预览

在运行预览之前，必须为本地开发设置环境，并确保您的库已[升级到最新的模板版本](/zh/foundry/code-repositories/repository-upgrades/#manual-branch-upgrade)。

1. 运行`./gradlew displayTransformsList`，这将返回所有可用变换的列表。
   ![使用datasetPreview任务列出所有可用变换](../../../images/foundry/transforms-common/display-transforms-list.png)

2. 运行`./gradlew datasetPreview --transformId=<transformId>`，将`<transformId>`替换为其中一个变换ID（上图中的蓝色文本），这将返回一个链接到Foundry，在那里可以访问已经计算的预览。
   ![使用datasetPreview任务运行预览并获取Foundry链接](../../../images/foundry/transforms-common/dataset-preview-result-in-terminal-as-uri.png)
   ![在Foundry中预计算的数据集预览](../../../images/foundry/transforms-common/dataset-preview-result-in-foundry.png)

3. （非必填）在上述命令中添加`--printMode=table`标志，以在终端中直接打印所有预览数据集的前10行，而不是提供预览链接。
   ![使用datasetPreview任务运行预览并打印到终端](../../../images/foundry/transforms-common/dataset-preview-result-in-terminal-as-table.png)

4. （非必填）要在预览中包含输入文件，请添加`--inputFiles=<datasetAlias>:<path>`，其中`<datasetAlias>`是所选变换函数的输入数据集之一，`<path>`是输入数据集内的文件路径。
   ![使用输入文件参数包含数据集的文件](../../../images/foundry/transforms-common/dataset-preview-file-input-arguments.png)

5. （非必填）要在预览中包含输出文件，请添加`--outputFiles=<datasetAlias>:<path>`，其中`<datasetAlias>`是所选变换函数的输出数据集之一，`<path>`是输出数据集内的文件路径。
   ![使用输出文件参数包含数据集的文件](../../../images/foundry/transforms-common/dataset-preview-file-output-arguments.png)
