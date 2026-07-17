---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/create-batch-pipeline-pb/",
  "title": "使用 Pipeline Builder 创建数据集批处理管道",
  "page_id": "create-batch-pipeline-pb",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/considerations-pb-cr/",
  "next": "/zh/foundry/building-pipelines/create-batch-pipeline-pb-media-set/",
  "scraped_at": "2026-07-13T05:46:13.950336+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用 Pipeline Builder 创建数据集批处理管道

在本教程中，我们将使用 Pipeline Builder 创建一个简单的管道，输出包含航班警报信息的单个数据集。然后，我们可以使用 Contour 或 Code Workbook 等工具分析此输出数据集，以回答哪些航班路径存在最大中断风险等问题。

以下使用的数据集可以在数据集导入步骤中按名称搜索，并可以在您的 Foundry 文件系统中的 Foundry 参考项目中找到：
`Foundry Training and Resources/Foundry Reference Project/Tutorial Reference Examples/Track: Data Engineering/Datasource Project: Flight Alerts/datasets`。

在本教程结束时，您将拥有一个如下所示的管道：

![完整Pipeline builder的截图](../../../images/foundry/building-pipelines/complete-pipeline.png)

该管道将生成一个新的数据集输出`Flight Alerts Data`，可以用于进一步探索。

## 第1部分：初始设置

首先，我们需要创建一个新的管道。

1. 登录 Foundry 后，从左侧导航栏下的 **应用程序** 中访问 **Pipeline Builder**。如果没有显示，请点击 **查看全部** 并在 **搭建与监控管道** 部分中找到 **Pipeline Builder**。

   ![导航栏上Pipeline builder链接的截图](../../../images/foundry/building-pipelines/application-pipeline-builder.png)

2. 接下来，在 Pipeline Builder 登陆页面的右上角，点击 **新建管道** 来创建一个新管道。选择 **批处理管道**。

   ![Pipeline选择的截图](../../../images/foundry/building-pipelines/new-pipeline-choice-standard-faster.png)

:::callout{theme="neutral"}
并非所有 Foundry 环境都支持创建流式管道。如果您的应用案例需要，请联系您的 Palantir 代表以获取更多信息。
:::

3. 选择一个位置来保存您的管道。请注意，管道不能保存在个人文件夹中。
   ![选择管道位置弹出框的截图](../../../images/foundry/building-pipelines/choose-pipeline-location.png)
4. 点击 **创建管道**。

## 第2部分：添加数据集

现在我们可以将数据集添加到我们的管道工作流中。对于本教程，我们将使用概念性或开源数据的示例数据集，所有数据集都应该作为 Foundry 参考项目的一部分在您的 Foundry 文件系统中可用。

在 Pipeline Builder 页面上，从 Foundry 点击 **添加数据集**。

![选择管道位置弹出框的截图](../../../images/foundry/building-pipelines/add-dataset-location.png)

或者，您可以从计算机拖放一个文件以用作您的数据集。

在我们的演练示例中，我们将添加 `passengers_preprocessed`、`flight_alerts_raw` 和 `status_mapping_raw` 数据集。要添加数据集的选择，请选择数据集并点击行内的 **+** 图标，或点击 **添加到选择**。

![从位置添加数据集的弹出框截图](../../../images/foundry/building-pipelines/add-dataset-location2.png)

选定所需的所有数据集后，点击 **添加数据集**。

![选择管道位置弹出框的截图](../../../images/foundry/building-pipelines/datasets-selected.png)

## 第3部分：清理数据

添加原始数据集后，我们可以执行一些基本的清理变换以继续定义我们的管道。我们将对三个原始数据集进行变换。

### 数据集1

首先，让我们清理 `passengers_preprocessed` 数据集。我们将从设置一个转换变换开始，将 `dob` 列名更改为 `dob_date`，同时将值转换为 MM/dd/yy 格式。

#### 转换变换

1. 点击图中的 `passengers_preprocessed` 节点。

2. 点击 **变换**。

   ![Passengers\_preprocessed数据集的截图](../../../images/foundry/building-pipelines/pax-preprocessed.png)

3. 从下拉菜单中搜索并选择 **转换** 变换以打开转换配置面板。

   ![Passengers\_preprocessed数据集变换视图的截图](../../../images/foundry/building-pipelines/pax-preprocessed-cast.png)

4. 从 **表达式** 字段中选择 `dob`，在 **类型** 中选择 `Date`。

5. 输入 `MM/dd/yy` 作为 **格式** 类型。请确保使用大写 `MM` 以确保转换变换成功。将输出列名更改为 `dob_date`。

   您的转换面板应如下所示：

   ![转换面板的截图](../../../images/foundry/building-pipelines/cast-board.png)

6. 点击 **应用** 将变换添加到您的管道中。

#### 标题大小写变换

现在我们将格式化 `flyer_status` 列的值，使其以大写字母开头。

1. 在变换搜索字段中搜索并选择 **标题大小写** 变换以打开标题大小写配置面板。

2. 在 **表达式** 字段中，从下拉菜单中选择 `flyer_status` 列。

   您的标题大小写面板应如下所示：

   ![标题大小写面板的截图](../../../images/foundry/building-pipelines/titlecase-board.png)

3. 点击 **应用** 将变换添加到您的管道中。

4. 在变换配置窗口的左上角，将变换重命名为 `Passengers_Clean`。

   ![变换的截图](../../../images/foundry/building-pipelines/passengers-clean.png)

5. 点击右上角的 **返回到图表** 以返回到您的管道图表。

   ![变换的截图](../../../images/foundry/building-pipelines/dataset-1-transformed.png)

### 数据集2

现在，让我们清理 `flight_alerts_raw` 数据集。首先，我们将设置另一个转换变换以将 `flight-date` 列的值转换为 `MM/dd/yy` 格式。

#### 转换变换

1. 点击图中的 `flight_alerts_raw` 数据集节点。

2. 点击 **变换**。

   ![变换的截图](../../../images/foundry/building-pipelines/flight-alerts-transform.png)

3. 从下拉菜单中搜索并选择 **转换** 变换以打开转换配置面板。您可以阅读选择框右侧列出的函数定义以了解更多关于函数的信息。
   ![函数定义的截图](../../../images/foundry/building-pipelines/castdefinition.png)

4. 在 **表达式** 字段中，从下拉菜单中选择 `flight_date` 列。

5. 从 **类型** 字段下拉菜单中选择 `Date`。

6. 输入 `MM/dd/yy` 作为 **格式** 类型。请确保使用大写 `MM` 以确保转换变换成功。

   您的转换面板应如下所示：

   ![第二个转换板的截图](../../../images/foundry/building-pipelines/dataset-2-cast.png)

7. 点击 **应用** 将变换添加到您的管道中。

#### 清理字符串变换

现在，我们将添加一个 **清理字符串** 变换，该变换将删除 `category` 列值中的空格。例如，该变换将把 `delay···` 字符串值转换为 `delay`。

1. 从下拉菜单中搜索并选择清理字符串变换以打开清理字符串配置面板。

2. 在 **表达式** 字段中，从下拉菜单中选择 `category` 列。

3. 勾选所有三个 **清理操作** 选项：

   * 将空字符串转换为 null
   * 将多个空白字符的序列减少为一个空白字符
   * 修剪字符串开头和结尾的空白

   您的清理字符串面板应如下所示：

   ![清理字符串面板的截图](../../../images/foundry/building-pipelines/clean-string.png)

4. 点击 **应用** 将变换添加到您的管道中。

5. 在变换配置窗口的左上角，将变换重命名为 `Flight Alerts - Clean`。

6. 点击右上角的 **返回到图表** 以返回到您的管道图表。

   ![带有Flight Alerts - Clean节点的图表截图](../../../images/foundry/building-pipelines/flight-alerts-clean-graph.png)

### 数据集3

最后，让我们清理 `status_mapping_raw` 数据集。

#### 清理字符串变换

我们将仅对该数据集应用一个 **清理字符串** 变换。

1. 点击图中的 `status_mapping_raw` 数据集节点。

2. 点击 **变换**。

   ![第三个数据集变换的截图](../../../images/foundry/building-pipelines/status-mapping-raw-transform.png)

3. 在 **搜索变换和列...** 字段中，从下拉菜单中选择 `mapped_value` 列。

   ![映射值列选择的截图](../../../images/foundry/building-pipelines/mapped-value-transform.png)

4. 在同一字段中搜索并选择清理字符串变换。

5. 勾选所有三个 **清理操作** 选项：

   * 将空字符串转换为 null
   * 将多个空白字符的序列减少为一个空白字符
   * 修剪字符串开头和结尾的空白

   您的清理字符串面板应如下所示：

   ![第二个清理字符串面板的截图](../../../images/foundry/building-pipelines/clean-string-mapped-value.png)

6. 点击 **应用** 将变换添加到您的管道中。

7. 在变换配置窗口的左上角，将变换重命名为 `Status Mapping - Clean`。

8. 点击右上角的 **返回到图表** 以返回到您的管道图表。

   您可以看到刚刚添加的变换与应用它们的数据集之间的连接。

   ![第二个清理字符串面板的截图](../../../images/foundry/building-pipelines/transforms-done.png)

## 第4部分：合并数据集

现在，让我们使用 **合并** 来合并一些已清理的数据集。合并允许您合并至少有一个匹配列的数据集。我们将在管道工作流中添加两个合并。

### 合并1

我们的第一个合并将合并两个已清理的数据集。

1. 点击 `Flight Alerts - Clean` 变换节点。这将是合并的左侧。

2. 选择 **合并**。

   ![配置合并选项的截图](../../../images/foundry/building-pipelines/join-time.png)

3. 点击 `Status Mapping - Clean` 节点将其添加为合并的右侧。

4. 点击 **开始** 以打开合并配置面板。

   ![配置合并选项的截图](../../../images/foundry/building-pipelines/start-join.png)

5. 验证 **合并类型** 设置为 `左合并`。

6. 设置 **匹配条件** 列为 `status` 等于 `value`。

7. 点击 **显示高级** 查看其他配置选项。

8. 设置右侧 `Status Mapping - Clean` 数据集的 **前缀** 为 `status`。

   您的合并配置面板应如下所示：

   ![输入表的截图](../../../images/foundry/building-pipelines/input-tables.png)

9. 点击 **应用** 将合并添加到您的管道中。

10. 在配置窗口底部的 **预览** 窗格中查看合并输出表的预览。

    ![Pipeline预览窗格的截图](../../../images/foundry/building-pipelines/pipeline-preview-pane.png)

11. 在合并配置窗口的左上角，将合并重命名为 `Join Status`。

12. 点击右上角的 **返回到图表** 以返回到您的管道图表。

    ![Pipeline预览窗格的截图](../../../images/foundry/building-pipelines/back-to-graph-join-status.png)

13. 为了使图表更易读，点击 **设计** 图标自动排列数据集或手动拖动两个连接的数据集到彼此旁边。

    ![Pipeline重新组织的截图](../../../images/foundry/building-pipelines/reorganized-graph.png)

### 合并2

对于我们的第二个合并，我们将合并第一个合并输出表与另一个原始数据集。

1. 通过点击 **添加数据集** 将 `priority_mapping_raw` 数据集添加到图表中。

2. 点击我们刚刚添加到图表中的 `Join Status` 节点。这将是合并的左侧。

3. 选择 **合并**。

4. 点击 `priority_mapping_raw` 数据集节点将其添加为合并的右侧。

5. 点击 **开始** 打开配置面板。

   ![Pipeline预览窗格的截图](../../../images/foundry/building-pipelines/select-another-table-to-join.png)

6. 验证 **合并类型** 设置为 `左合并`。

7. 设置 **匹配条件** 列为 `priority` 等于 `value`。

8. 点击 **显示高级** 查看其他配置选项。

9. 设置右侧 `priority_mapping_raw` 数据集的 **前缀** 为 `priority`。

   您的合并配置面板应如下所示：

   ![Pipeline预览窗格的截图](../../../images/foundry/building-pipelines/input-tables2.png)

10. 点击 **应用** 将合并添加到您的管道中。

11. 在配置窗口底部的 **预览** 窗格中查看合并输出表的预览。

    ![Pipeline预览窗格的截图](../../../images/foundry/building-pipelines/preview-pane2.png)

12. 在合并配置窗口的左上角，将合并重命名为 `Join (2)`。

13. 点击右上角的 **返回到图表** 以返回到您的管道图表。

您现在可以看到刚刚添加的合并与应用它们的数据集之间的连接。

![Pipeline预览窗格的截图](../../../images/foundry/building-pipelines/join-stage-in-workspace.png)

## 第5部分：添加输出

现在我们已经完成了数据的变换和结构化，让我们添加一个输出。对于本教程，我们将添加一个数据集输出。

1. 在 Pipeline Builder 图表右侧的 **管道输出** 侧栏中，将输出命名为 `Flight Alerts data`。然后点击 **添加数据集输出**。
2. 点击合并节点右侧的白色圆圈，将 `Join (2)` 连接到 `Flight Alerts data` 数据集。
3. 点击 **使用输入模式** 以使用现有模式。
4. 从这里，选择要保留的数据列。在我们的例子中，我们将保留所有数据。

   ![填充模式的数据集输出窗格截图](../../../images/foundry/building-pipelines/add-an-output.png)

## 第6部分：搭建管道

要搭建您的管道，请确保点击 **保存**，然后点击 **部署 > 部署管道**。

![填充模式的数据集输出窗格截图](../../../images/foundry/building-pipelines/deploy-this-pipeline.png)

您应该会看到一个小提示，指示部署成功。在提示框中点击 **查看** 以打开 **搭建进度** 页面。

![搭建进度页面的截图](../../../images/foundry/building-pipelines/build-progress.png)

从此页面，您可以监控搭建的进度，直到数据集输出准备就绪。

![搭建成功状态页面的截图](../../../images/foundry/building-pipelines/build-succeed.png)

您现在可以通过点击 **操作 > 打开** 访问您的数据集。

![数据集输出的截图](../../../images/foundry/building-pipelines/flight-alerts-data.png)

通过最后一步，我们已经生成了我们的管道输出。此输出是一个数据集，可以在 Foundry 的其他应用程序中进一步探索，例如 [Contour](/zh/foundry/contour/analysis-create-path/#starting-an-analysis-from-datasets-in-foundry) 或 [Code Workbook](/zh/foundry/code-workbook/workbooks-overview/)。
