---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/dataexpectations-unit-tests/",
  "title": "在 Pipeline Builder 中进行单元测试",
  "page_id": "dataexpectations-unit-tests",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/dataexpectations-configure-health-check/",
  "next": "/zh/foundry/pipeline-builder/marketplace-pipeline-builder/",
  "scraped_at": "2026-07-13T05:53:58.669328+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在 Pipeline Builder 中进行单元测试

通过单元测试提高 Pipeline Builder 中管道的可靠性。这些测试是调试、检测中断更改的宝贵工具，最终确保更高质量的管道。

## 什么是单元测试？

![单元测试说明图。](../../../images/foundry/pipeline-builder/unit-test-architecture.png)

类似于代码中的单元测试，Pipeline Builder 中的单元测试是一种检查管道逻辑在使用预定义输入进行测试时产生预期输出的方法。单元测试由以下组成：

* 测试输入
* 变换节点
* 预期输出

测试输入和预期输出通过手动输入表格创建，但您可以复制和粘贴以加快创建速度。您可以在主要的 Pipeline Builder 工作区中选择要测试的变换节点。有关创建单元测试的更多信息，请参阅下文。

## 创建单元测试

1. 在主要工作区的右侧面板，选择**单元测试**图标。 <br><br>
   ![单元测试侧边栏。](../../../images/foundry/pipeline-builder/unit-test-side-bar.png) <br><br>
2. 在屏幕中央选择**创建新测试**或在右上角选择**新测试**。这将在您的工作区顶部打开一个对话框，提示您选择相关节点。 <br><br>
   ![单元测试初始选择屏幕。](../../../images/foundry/pipeline-builder/unit-test-initial-selection.png) <br><br>
3. 选择所有相关节点后，选择**开始**。 <br><br>
   ![包含在单元测试中的已选节点。](../../../images/foundry/pipeline-builder/unit-test-selected-boards.png) <br><br>
   这将带您进入单元测试配置窗口。

   * 黄色节点对应于先前选择的变换节点。
   * 绿色节点对应于测试输入。
   * 蓝色节点对应于测试输出。

   对于每个单元测试，您必须填写输入和输出数据。 <br><br>
   ![单元测试中的初始编辑屏幕。](../../../images/foundry/pipeline-builder/unit-test-initial-edit-screen.png) <br><br>
4. 双击节点填写输入数据或预期输出数据。这将带您进入以下页面： <br><br>
   ![单元测试中的添加输入或输出数据页面。](../../../images/foundry/pipeline-builder/unit-test-data.png) <br><br>
   在左侧选择：

   * **复用模式：** 将输出模式设置为匹配连接表的模式。
   * **从数据集：** 使用现有数据集中的模式。
   * **添加列：** 手动输入数据模式。

   一旦模式设置完成，在中间表中填写行，然后选择**应用**，然后**返回图表**。 <br><br>
   ![单元测试中的手动数据填写页面。](../../../images/foundry/pipeline-builder/unit-test-manual-data-fill.png) <br><br>
5. 对所有输入和输出数据集重复此步骤。

完成后，您将能够在右侧面板中看到手动输入的数据，详细显示每个表中的行数和列数。

![填充输入和输出的单元测试。](../../../images/foundry/pipeline-builder/unit-test-with-data-filled.png)

## 运行单元测试

对于每个单元测试，您可以选择在右上角**运行测试**。

![单元测试的运行测试按钮。](../../../images/foundry/pipeline-builder/unit-test-run-test.png)

一旦测试运行，您可以在下面看到测试结果。要查看确切的表格结果，请选择**查看测试结果**。

![分别为失败和通过的测试结果。](../../../images/foundry/pipeline-builder/unit-test-pass-fail.png)

这将在屏幕底部打开预期输出和接收输出的视图。

![在屏幕底部显示的预期和接收输出。](../../../images/foundry/pipeline-builder/unit-test-full-screen.png)

完成编辑和查看单元测试后，您可以在右上角选择**关闭单元测试**。

## 删除单元测试

要删除单元测试，选择它并使用右上角的三个点打开选项菜单。选择**删除测试用例**。

![如何删除单元测试。](../../../images/foundry/pipeline-builder/unit-test-delete-test.png)

## 编辑现有单元测试

选择**单元测试**图标以查看管道中的单元测试列表。选择铅笔图标以编辑选定的单元测试。

![管道中的单元测试列表。](../../../images/foundry/pipeline-builder/unit-test-edit-unit-test.png)

要更改单元测试中选定的测试变换，请使用**重新选择**按钮。这将带您返回选择页面。

![单元测试的重新选择过程。](../../../images/foundry/pipeline-builder/unit-test-selection.png)

:::callout{theme="neutral"}
如果您在已经包含为单元测试中的测试变换的节点之间添加节点，添加的节点将自动显示在现有单元测试中。
:::

要更改任何测试输入或预期输出，您可以直接在图表视图中双击节点，或在右侧面板中选择铅笔图标。

![单元测试中的输入和输出编辑页面。](../../../images/foundry/pipeline-builder/unit-test-edit-input-output.png)

完成编辑单元测试后，选择右上角的**关闭单元测试**以返回主图。

## 建议中的单元测试

对单元测试的任何更改也将在左侧面板的**单元测试**选项卡下的建议页面中显示。

![建议页面上的单元测试。](../../../images/foundry/pipeline-builder/unit-test-changes.png)

在建议页面上，您将看到**单元测试成功**部分。Pipeline Builder 将在合并建议之前检查单元测试是否通过。

![建议页面上的单元测试。](../../../images/foundry/pipeline-builder/unit-test-proposal-page.png)
