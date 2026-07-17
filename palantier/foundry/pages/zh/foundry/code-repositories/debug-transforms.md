---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/code-repositories/debug-transforms/",
  "title": "调试变换",
  "page_id": "debug-transforms",
  "category_id": "data-integration",
  "section_id": "code-repositories",
  "previous": "/zh/foundry/code-repositories/preview-transforms/",
  "next": "/zh/foundry/code-repositories/use-project-references/",
  "scraped_at": "2026-07-13T06:00:09.134093+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 调试变换

使用Code Repositories中的调试工具，在运行时检查数据变换的行为。设置断点以暂停变换的执行，以便检查变量、查看数据框并理解函数和库。

![调试器概览面板](../../../images/foundry/code-repositories/debugger-overview.png)

:::callout
调试器仅适用于[Python](/zh/foundry/transforms-python/debugging/)。
:::

## 设置断点

要使用调试器，您需要设置*断点*。断点向调试器指示它应该在代码执行的哪些点暂停，并允许您与变量和数据框进行交互。

您可以通过点击每行代码边缘上的淡红色点来设置断点。调试器在标记行运行之前暂停执行。如果需要，您可以在多个文件中设置多个断点。

:::callout{theme="neutral"}
在使用内部库断点时，控制台功能可能会受到限制。在这种情况下，断点呈灰色，调试器提供忽略断点或使用有限控制台功能的选项。
:::

![调试器断点](../../../images/foundry/code-repositories/debugger-breakpoint.png)

## 运行调试器

在代码中添加断点后，点击代码编辑器操作栏中的**预览和调试**。调试器面板打开并在遇到的第一个断点处暂停。调试器的左侧栏允许您导航代码、移除断点并结束/停止调试会话。

![调试器设计](../../../images/foundry/code-repositories/debugger-layout.png)

您可以启用导航内部库的功能。找到**内部库调试已禁用**部分，然后选择**启用内部库调试**。

![调试器内部库](../../../images/foundry/code-repositories/debugger-internal-libraries-enable.png)

当您在代码中导航时，编辑器会突出显示下一步要执行的代码行。使用以下按钮来推进调试器：

![调试器控制](../../../images/foundry/code-repositories/debugger-controls.png)

1. **恢复执行：** 继续执行直到完成或被下一个断点暂停。
2. **单步跳过：** 执行代码行而不进入内部函数。
3. **单步进入：** 如果该代码行中存在内部函数，则进入内部函数。
4. **单步退出：** 退出内部函数并推进调试器。
5. **停止执行：** 完全停止调试器。
6. **移除断点：** 从代码库中移除所有断点并运行预览而不暂停执行。
7. **设置：** 切换调试器开/关（不清除断点）。
8. **文档：** 打开文档以获取更多详细信息。

## 预览数据框

运行调试器时，您还可以在每个断点预览中间数据框。为此，请在变量视图中选择**预览**：

![调试器预览数据框](../../../images/foundry/code-repositories/debugger-preview-df.png)

选择**预览**将为所选数据框打开调试器预览面板：

![调试器预览数据框结果](../../../images/foundry/code-repositories/debugger-preview-df-result.png)

要返回调试器，请选择**返回调试器**：

![调试器返回](../../../images/foundry/code-repositories/debugger-return.png)

## 检查变量

调试器运行时，您可以在代码执行的确切位置检查变量和数据。

### 框架

框架表示调试器处于活动状态或存在断点的函数。每个框架指示函数的名称，后跟文件名和编写函数的行号。

选择一个框架以检查该框架内的变量，并在其上运行控制台命令。

### 变量

*变量*部分显示在变换执行时存储在本地和全局变量中的值。

:::callout{theme="neutral"}
数据框值基于预览样本，可能不代表完整数据集。使用它们来理解和调试您的代码，但不能作为变换输出的指示。
:::

![调试器变量](../../../images/foundry/code-repositories/debugger-variables.png)

### 控制台

控制台允许您在运行调试器时使用PySpark命令与数据交互。控制台中有两种常用模式：

* 在控制台选项卡底部的命令行中直接对数据框和变量运行命令，使用Enter或Return键启动命令。
* 在变换代码中调用`print`函数以将指示性信息发送到控制台。

:::callout{theme="neutral"}
注意，控制台运行在选定的框架上。尝试在不同框架的本地变量上执行命令将导致NameError。
:::

![调试器控制台](../../../images/foundry/code-repositories/debugger-console.png)

## 配置调试器

通过导航到调试器选项卡并点击设置齿轮来打开和关闭调试器功能。如果您希望在不停止断点的情况下运行预览，请关闭调试器。

:::callout{theme="neutral"}
虽然调试器配置适用于整个代码库，但代码库中可能存在不受其支持的语言。如果调试器不支持某种语言，则无论调试器设置如何，预览将继续正常运行。
:::

![调试器功能齿轮](../../../images/foundry/code-repositories/debugger-configuration-1.png)

您还可以在**设置**选项卡下的**首选项** > **调试器**中配置调试器。

![设置中的调试器配置](../../../images/foundry/code-repositories/debugger-configuration-2.png)
