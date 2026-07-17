---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/create-stream-pipeline-pb/",
  "title": "使用Pipeline Builder创建流式管道",
  "page_id": "create-stream-pipeline-pb",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/create-incremental-pipeline-pb/",
  "next": "/zh/foundry/building-pipelines/incremental-overview/",
  "scraped_at": "2026-07-13T05:42:31.981940+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用Pipeline Builder创建流式管道

在本教程中，我们将使用Foundry Streaming和Pipeline Builder创建一个简单的管道，其输出为一个包含传感器温度信息的数据集。您将学习如何在Foundry中创建一个流，将记录推送到该流中，并在Pipeline Builder中变换它们。

## 第1部分：初始设置

首先，我们需要创建一个新的流。

1. 登录Foundry后，导航到Foundry中的一个[项目](/zh/foundry/projects/overview/)，在右上角选择\*\*+ New\*\*，然后选择**Stream**。

![流创建下拉菜单的截图](../../../images/foundry/building-pipelines/stream-create-dropdown.png)

2. 接下来，您需要定义您的流。在本指南中，我们将创建一个简单的单分区流，并手动将记录推送到其中。

在**定义**页面上，选择**Normal**作为吞吐量，并定义一个基本的模式为：**sensor\_id:** `字符串`, **temperature:** `Double`。

![流定义页面的截图](../../../images/foundry/building-pipelines/stream-define.png)

3. 选择**创建流**。这将带您进入**连接**页面，您可以在此指定如何连接到流数据。

## 第2部分：将记录推送到流中

我们现在准备连接我们的流。在此时，我们可以使用一个[数据源](/zh/foundry/data-integration/source-type-overview/)来设置一个流数据摄取任务。在本教程中，我们将手动使用**Curl**将记录推送到流中。

1. 首先，在**通过API连接**部分下选择\*\*Curl (Bash)\*\*来为您的流设置身份验证。我们将使用个人词元来提交记录。

![流连接页面的截图](../../../images/foundry/building-pipelines/stream-connect.png)

2. 选择**使用个人词元测试**，并按照屏幕提示生成一个短时效个人词元。

   :::callout{theme="neutral"}
   个人词元不应用于生产管道。生产管道应使用[OAuth词元工作流](/zh/foundry/platform-security-third-party/writing-oauth2-clients/#oauth2-api-reference)。
   :::

![流连接认证页面的截图](../../../images/foundry/building-pipelines/stream-push-auth.png)

3. 将生成的词元粘贴到文本框中，然后点击**下一步**。
4. 复制**Curl**命令。在您的计算机上打开一个可以执行Bash的终端，并粘贴该命令。在终端中运行该命令。

![使用curl推送流的截图](../../../images/foundry/building-pipelines/stream-push-curl.png)

几秒钟内，您将在页面上的流只读器中看到一个记录出现：

![流查看记录选项卡的截图](../../../images/foundry/building-pipelines/stream-view-records.png)

我们现在已经实时摄取了流数据。现在让我们变换这些数据。

## 第3部分：变换流

1. 选择**开始管道化**按钮以开始在Pipeline Builder中编写一个基本的流式变换。

![流查看记录选项卡的截图](../../../images/foundry/building-pipelines/stream-start-pipelining.png)

2. 在**创建新管道**模式窗口中，选择**流式管道**类型，然后点击**创建管道**。

![创建builder流式管道的截图](../../../images/foundry/building-pipelines/create-new-stream-pipeline.png)

这将为输入流创建一个管道，并在图上显示。

选择输入流节点将显示数据的预览。请注意，预览在流的冷存储视图上运行；流中的记录在出现之前会有延迟。

![builder图中输入流的截图](../../../images/foundry/building-pipelines/stream-input-pb.png)

3. 点击图上的输入流节点，并选择**变换**操作（输入节点旁边的蓝色**T**图标）。

   这将打开一个列表，其中显示了当前支持的所有基于流中列的输入类型的变换。对于本教程，我们将所有`sensor_ids`转换为大写，去除其上的空白，并筛选出温度超过三度的记录。

![builder流变换下拉菜单的截图](../../../images/foundry/building-pipelines/stream-transform-dropdown.png)

4. 选择**大写**变换，选择`sensor_id`列，然后点击**应用**。

![builder流大写变换的截图](../../../images/foundry/building-pipelines/stream-uppercase-transform-pb.png)

5. 然后，搜索**修剪空白**变换并选择它。再次选择`sensor_id`列，然后点击**应用**。

![builder修剪空白变换的截图](../../../images/foundry/building-pipelines/stream-trim-whitespace-transform-pb.png)

6. 对于最后的变换，首先搜索**筛选**变换并选择**保留行**。然后，选择`temperature`列，将筛选设置为**大于**`3`，并选择**应用**。

![builder筛选变换的截图](../../../images/foundry/building-pipelines/stream-filter-transform-pb.png)

7. 点击屏幕右上角的**应用所有更改**。然后，选择**返回图形**以返回到您的管道。

![builder图中有变换的截图](../../../images/foundry/building-pipelines/stream-transform-graph.png)

8. 选择我们刚创建的**变换路径**节点，然后点击**新数据集**。

![builder图中创建新输出的截图](../../../images/foundry/building-pipelines/stream-transform-new-dataset-pb.png)

9. 在应用程序的右上角，首先点击**保存**以应用管道的所有新更改。然后，点击**部署**和**部署管道**。

:::callout{theme="warning"}
如果您保存更改但未部署，您的管道逻辑将**不会**更新为最新更改。您必须部署管道以捕获变换逻辑的更改。
:::

![builder图部署下拉菜单的截图](../../../images/foundry/building-pipelines/stream-builder-graph.png)

10. 选择您刚创建的输出流节点，然后点击图底部**数据预览**部分上方的流名称。

![builder图中已部署输出的截图](../../../images/foundry/building-pipelines/stream-deployed-builder-graph.png)

这将带您进入变换输出流的流预览页面。

:::callout{theme="neutral"}
流集群启动大约需要一分钟，因此您可能不会立即看到记录。然而，一旦运行，集群将实时处理所有新记录。
:::

![输出流的截图](../../../images/foundry/building-pipelines/stream-view-output.png)

## 接下来的步骤

现在您已经知道如何创建一个简单的流式管道，学习更多关于管理流的方法，探索如何[调试失败的流](/zh/foundry/optimizing-pipelines/debug-stream/)。对于更高级的变换功能，请了解更多关于[Pipeline Builder](/zh/foundry/pipeline-builder/overview/)的信息。
