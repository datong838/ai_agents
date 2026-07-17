---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/create-batch-pipeline-pb-media-set/",
  "title": "使用Pipeline Builder创建媒体集批处理管道",
  "page_id": "create-batch-pipeline-pb-media-set",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/create-batch-pipeline-pb/",
  "next": "/zh/foundry/building-pipelines/create-batch-pipeline-cr/",
  "scraped_at": "2026-07-13T05:42:07.922326+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用Pipeline Builder创建媒体集批处理管道

在本教程中，我们将使用Pipeline Builder创建一个简单的管道，通过媒体集从PDF中提取文本。

在这个示例中，我们使用Palantir发布的公开可用文档的PDF。

在本教程结束时，您将拥有如下所示的管道：

![完整的Pipeline builder截图](../../../images/foundry/building-pipelines/pb-media-sets-overview.png)

该管道将生成一个新的Object输出，其中包含提取的PDF文本，可用于进一步的探索。

## 第1部分：初始设置

首先，我们需要创建一个新的管道。

1. 登录到Foundry后，从左侧导航栏访问**Pipeline Builder**。如果Pipeline Builder不在应用列表中，选择**查看全部**，在**构建和监控管道**部分下找到**Pipeline Builder**。

   ![导航栏上的Pipeline builder链接截图](../../../images/foundry/building-pipelines/application-pipeline-builder.png)

2. 接下来，在Pipeline Builder主页的右上角，通过选择**新建管道**来创建新管道。然后选择**批处理管道**。

   ![管道选择截图](../../../images/foundry/building-pipelines/new-pipeline-choice-standard-faster.png)

   :::callout{theme="neutral"}
   创建流式管道的功能并不是在所有Foundry环境中都可用。如果您的应用案例需要它，请联系您的Palantir代表以获取更多信息。
   :::

3. 选择一个位置保存您的管道。请注意，管道不能保存在个人文件夹中。

   ![选择管道位置弹出窗口截图](../../../images/foundry/building-pipelines/choose-pipeline-location.png)

4. 选择**创建管道**。

## 第2部分：添加媒体集

现在我们可以将数据集添加到我们的管道工作流中。在本教程中，我们将使用来自Palantir的公开可用文档的PDF。

1. 从Pipeline Builder页面，在主页上选择**添加Foundry数据**。

   ![选择管道位置弹出窗口截图](../../../images/foundry/building-pipelines/welcome-to-pipeline-builder-updated.png)

   您还可以选择顶部面板上的**添加数据**操作。

   ![选择管道位置弹出窗口截图](../../../images/foundry/building-pipelines/pb-add-data-option.png)

   或者，您可以拖放计算机上的文件以用作您的媒体集。

2. 如果您选择了**添加数据**或**添加Foundry数据**，您将可以选择您想要的媒体集。

   ![从位置添加媒体集弹出窗口截图](../../../images/foundry/building-pipelines/add-media-set-pipeline-builder.png)

3. 选择所有媒体集后，选择**添加数据**。

4. 导入媒体集后，您将能够看到带有缩略图预览的媒体集。

   ![导入的媒体集截图](../../../images/foundry/building-pipelines/pb-imported-preview-media-set.png)

## 第3部分：媒体集变换

添加原始媒体集后，我们可以进行一些基本的变换。在此工作流中，我们将从这些PDF文件中提取文本。

### 从PDF中提取文本

首先，我们将变换`年度信件媒体集`媒体集。选择媒体集中媒体项的[媒体引用](/zh/foundry/data-integration/media-sets/)。

#### 获取媒体引用

1. 在您的图中选择`年度信件媒体集`节点。

2. 选择**变换**。

   ![年度信件媒体集节点截图](../../../images/foundry/building-pipelines/pb-transform-mediaset.png)

3. 搜索并选择**将媒体集转换为表行**变换以打开面板。

   ![媒体集转换为表面板截图](/resources/foundry/building-pipelines/pb-convert-media-set-to-table-rows.png)

4. 选择是否`包含时间戳`和`按路径去重`。

   ![媒体引用面板截图](/resources/foundry/building-pipelines/pb-get-media-references-options.png)

5. 选择**应用**以将变换添加到您的管道中。

6. 您的输出应如下所示：

   ![Cast面板截图](/resources/foundry/building-pipelines/pb-media-reference-unhovered.png)

   示例媒体引用：

   ```
   {"mimeType":"application/pdf","reference":{"type":"mediaSetItem","mediaSetItem":{"mediaSetRid":"ri.mio.main.media-set.xxx","mediaItemRid":"ri.mio.main.media-item.xxx"}}}
   ```

   示例媒体项RID：

   ```
   ri.mio.main.media-item.xxx-xxx-xxx-xxx-xxxx
   ```

   [了解更多关于媒体引用的信息。](/zh/foundry/data-integration/media-sets/)

#### 提取文本

1. 使用媒体引用后，您现在可以选择一个新的面板，该面板利用媒体引用。搜索并选择**文本提取**变换。

   ![文本提取面板](/resources/foundry/building-pipelines/pb-text-extraction-board.png)

2. 选择提取方法（`原始文本`（PDF解析）或`OCR`），`媒体引用`列，`OCR输出格式`（如果选择了OCR），以及`语言/脚本`。

   ![文本提取选项](/resources/foundry/building-pipelines/pb-text-extraction-options.png)

3. 选择**应用**以将变换添加到您的管道中。

4. 当您将鼠标悬停在提取的文本上时，您的输出应如下所示：

   ![带悬停的文本提取输出](../../../images/foundry/building-pipelines/pb-text-extraction-output-hover.png)

   您现在可以在提取的文本列上运行可用的字符串变换。

5. 选择右上角的**返回图表**以返回到您的管道图表。

   ![变换截图](../../../images/foundry/building-pipelines/pb-transforms-mediaset-graph.png)

#### （非必填）语义搜索工作流

如果需要，您可以继续使用提取的文本进行[语义搜索工作流](/zh/foundry/functions/pdf-handling/)。

## 第4部分：添加输出

现在我们已完成从PDF中提取文本并可能运行额外的字符串变换，我们可以添加一个输出。在本教程中，我们将添加一个Object输出。

1. 在完成变换的`Transforms`节点中，选择**添加输出**。

   ![从媒体集变换添加输出](../../../images/foundry/building-pipelines/pb-media-sets-add-output.png)

2. 选择**新对象类型**。

   ![添加新对象类型](../../../images/foundry/building-pipelines/pb-mediasets-create-new-obj-type.png)

3. 命名您的对象类型并通过选择**请选择一个Ontology**来设置Ontology。

   ![重命名和设置Ontology输出](../../../images/foundry/building-pipelines/pb-rename-and-set-ontology.png)

4. 选择**编辑**并编辑任何列映射。确保为主键选择有效的列。

   ![编辑列映射](../../../images/foundry/building-pipelines/pb-media-set-ontology-col-mapping.png)

## 第5部分：搭建管道

1. 要搭建您的管道，请确保选择**保存**，然后选择**部署 > 部署管道**。

   ![方案填充的数据集输出窗格截图](../../../images/foundry/building-pipelines/deploy-this-pipeline.png)

2. 您应该在`部署管道`侧边栏选项下看到`初始化部署`。

   ![初始化部署](../../../images/foundry/building-pipelines/pb-initializing-deployment.png)

3. 选择**查看部署历史**以跟踪您的部署进度。您应该被引导到管道中的`历史`选项卡，在那里您可以查看部署的状态和历史：

   ![部署进行中](../../../images/foundry/building-pipelines/pb-deployment-history-deploying.png)

   ![部署完成](../../../images/foundry/building-pipelines/pb-deployment-history-deployed.png)

## （非必填）第6部分：Ontology之北

一旦部署完成并且您的对象已初始化，您应该能够直接在您的对象输出上进行操作。选择**创建Workshop模块**以生成一个带有管道输出的Workshop模块。

![创建Workshop模块](../../../images/foundry/building-pipelines/pb-create-workshop-module.png)

通过这最后一步，我们生成了管道输出并生成了一个Workshop模块。
