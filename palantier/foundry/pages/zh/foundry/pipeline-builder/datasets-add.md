---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/datasets-add/",
  "title": "添加数据集",
  "page_id": "datasets-add",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/datasets-overview/",
  "next": "/zh/foundry/pipeline-builder/datasets-generated/",
  "scraped_at": "2026-07-13T05:45:53.898406+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 添加数据集

要开始搭建管道，可以通过以下四种方法之一将数据添加到图中：

* [数据连接应用程序](#add-data-to-pipeline-builder-from-data-connection)
* [从Foundry中选择数据集或媒体集](#add-data-from-foundry-to-pipeline-builder)
* [手动上传数据](#upload-data-from-your-computer-to-pipeline-builder)
* [在管道文件中手动输入数据](#manually-enter-data-in-pipeline-builder)

## 从数据连接中向Pipeline Builder添加数据

要从数据源访问数据，请在Foundry导航侧边栏中进入**数据连接**应用程序。找到您想要集成的数据源，然后点击**开始管道化**。选择新管道的位置，然后点击**保存**。这将创建一个新管道，并且所有连接到您的数据源的同步将被导入到您的Pipeline Builder图中。

:::callout{theme="neutral"}
您不能将新的管道保存到您的个人文件夹中。请设置[推荐的项目结构](/zh/foundry/building-pipelines/recommended-project-structure/)，以便在开发过程开始时就组织好数据安全和治理。
:::

![示例数据连接的截图](../../../images/foundry/pipeline-builder/datasets-data-cnx@2x.png)

## 从Foundry向Pipeline Builder添加数据

要导入已存在于您Foundry文件系统中的数据集或媒体集，请进入Pipeline Builder应用程序并在图形空间的中心选择**添加Foundry数据**。搜索并选择可用的数据集，然后选择**添加数据**。

![添加数据按钮的截图](../../../images/foundry/pipeline-builder/welcome-to-pipeline-builder-updated.png)

您可以通过添加每个数据集或媒体集并选择**添加到选择**来添加多个数据集或媒体集；一旦全部选中后，选择**添加数据**。

![添加数据集按钮的截图](../../../images/foundry/pipeline-builder/data-add-datasets-prompt@2x.png)

## 从您的计算机上传数据到Pipeline Builder

您还可以从计算机上传数据集或媒体集文件。选择**从您的计算机上传**以选择您要添加的文件，或将文件拖放到您的图中。

![手动上传数据部分的截图](../../../images/foundry/pipeline-builder/data-manually-upload-data@2x.png)

## 在Pipeline Builder中手动输入数据

也可以通过定义数据表并手动填充数据来创建输入数据集。

![手动输入数据图标](../../../images/foundry/pipeline-builder/manually-enter-data@2x.png)

通过选择列名和类型来定义新表的模式，然后手动向表中添加值。手动输入的表可以在任何时候进行修改。

![在表中手动输入数据](../../../images/foundry/pipeline-builder/manually-entered-data-table@2x.png)

下表列出了手动输入表中可用的列类型：

| 列类型 | 格式 |
|---|---|
| 字符串 | 所有字符 |
| 时间戳 | `mm/dd/yyyy hh:mm:ss`；可以使用其他时间戳格式 |
| 日期 | `mm/dd/yyyy` |
| 布尔值 | 0 → false，不是0 → true |
| 二进制 | 所有字符，将显示为`base64` |
| 整数，长整型 | 正负数，无小数点 |
| 双精度 | 正负数，包括小数点 |

## 下一步

将数据集或媒体集添加到Pipeline Builder后，您可以更改其[计算模式](/zh/foundry/pipeline-builder/datasets-computation-modes-for-batch/)，选择[变换数据](/zh/foundry/pipeline-builder/transforms-overview/)或[添加输出](/zh/foundry/pipeline-builder/outputs-add-dataset-output/)。

![导入数据集的截图](../../../images/foundry/pipeline-builder/demo-pipeline@2x.png)
