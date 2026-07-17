---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/create-batch-pipeline-cr-media-sets/",
  "title": "使用代码库创建媒体集批处理管道",
  "page_id": "create-batch-pipeline-cr-media-sets",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/create-batch-pipeline-cr/",
  "next": "/zh/foundry/building-pipelines/create-incremental-pipeline-pb/",
  "scraped_at": "2026-07-13T05:40:57.722443+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用代码库创建媒体集批处理管道

本指南将通过一个简单的变换示例，引导您使用**代码库**应用程序。您将学习如何编写和编辑带有媒体集的Python代码。

## 1. 创建一个库

起始通过创建一个新库。在Foundry中导航到一个[项目](/zh/foundry/getting-started/projects-and-resources/)，选择右上角的\*\*+ 新建\*\*，然后选择**代码库**。

在本指南中，我们将编写一个Python变换。为您的库命名，并在**语言模板**下拉菜单中选择**Python**。然后，选择**初始化库**。

![新Python变换库](../../../images/foundry/building-pipelines/new-code-repository-python.png)

## 2. 导入您的数据

如果您已经导入了一个原始媒体集以供使用，可以继续进行下一步。否则，请参阅媒体集指南了解[如何将媒体导入Foundry](/zh/foundry/data-integration/media-sets/)。

## 3. 导入`transforms-media`库

要使用媒体集变换，您必须导入`transforms-media`库。

从左侧边栏导航到**库**选项，然后搜索并选择`transforms-media`库。然后，选择**添加并安装库**。

![Transforms-media库](../../../images/foundry/building-pipelines/install-transforms-media.png)

安装完成后，状态应显示为**库已安装**。

![Transforms-media库已安装](../../../images/foundry/building-pipelines/transforms-media-library-installed.png)

## 4. 编辑代码

### 创建一个新文件

创建Python变换库应自动生成一个`examples.py`文件，您可以将其用作基础。您可以通过选择省略号图标，选择**重命名**，并相应地为文件命名来重命名文件。
![自动生成的Python文件](../../../images/foundry/building-pipelines/example-python-file.png)

如果您想创建一个新文件，请选择省略号图标并在**数据集**目录下选择**新文件**。确保您正在创建一个Python文件以用于此工作流程。

### 将正确的库导入您的文件

在处理媒体集时，您必须使用`@transform`装饰器。媒体集输入和输出必须使用`transforms.mediasets.MediaSetInput`和`transforms.mediasets.MediaSetOutput`规范传递：

```python
from transforms.api import transform
from transforms.mediasets import MediaSetInput, MediaSetOutput

@transform(
    images=MediaSetInput('/examples/images'),  # 输入路径，指定要转换的图像集合
    ...
)
```

### 确保输出文件存在

如果您正在创建一个媒体集输出文件，请确保在变换装饰器中引用它之前创建它。

您可以通过导航到您的项目文件夹（您首次创建Python变换代码库的位置），然后从下拉菜单中选择**新建 > 媒体集**来创建此文件。

![创建空媒体集输出](../../../images/foundry/building-pipelines/project-add-media-set-dialog.png)

### 使用`get_media_item()`、`get_media_item_by_path()`或`list_media_items_by_path_with_media_reference()`

要变换媒体集中的每个媒体项，您必须在您的变换中使用`get_media_item()`或`get_media_item_by_path()`引用这些媒体项。

注意，对`get_media_item()`、`get_media_item_by_path()`的调用返回一个类似Python文件的流Object。 [`io.open()` ↗](https://docs.python.org/3/library/io.html#io.open)接受的所有选项也都支持。项目被读取为流，这意味着不支持随机访问。

您可以按以下方式引用单个媒体项：

```python
from transforms.api import transform
from transforms.mediasets import MediaSetInput, MediaSetOutput

@transform(
    images=MediaSetInput('/examples/images'),
    output_images=MediaSetOutput('/examples/output_images')
)
def translate_images(images, output_images):
    image1 = images.get_media_item_by_path("image1")  # 使用路径获取媒体项
    image2 = images.get_media_item("ri.mio.main.media-item.123")  # 使用RID获取媒体项
```

然而，您可能希望通过将媒体项放入数据框中来列出媒体集中的所有媒体项。您必须使用`list_media_items_by_path_with_media_reference()`列出媒体项：

```python
from transforms.api import transform, Output
from transforms.mediasets import MediaSetInput

@transform(
    images=MediaSetInput('/examples/images'),
    listing_output=Output('/examples/listed_images')
)
def translate_images(ctx, images, listing_output):
    # 列出媒体项及其引用路径
    media_items_listing = images.list_media_items_by_path_with_media_reference(ctx)

    # 您可以对列出的输出执行任何 PySpark 函数
```

此代码定义了一个数据转换函数 `translate_images`，用于处理媒体文件。使用 `transform` 装饰器来指定输入和输出路径。
列表将具有以下模式：

```
+--------------------------+-----------+-------------------+
|        mediaItemRid      |    path   |  mediaReference  |
+--------------------------+-----------+-------------------+
| ri.mio.main.media-item.1 | item1.jpg |  {{reference1}}   |  // 这里的mediaItemRid是媒体项的唯一标识符
| ri.mio.main.media-item.2 | item2.jpg |  {{reference2}}   |  // path列表示图片文件的名称
| ri.mio.main.media-item.3 | item3.jpg |  {{reference3}}   |  // mediaReference是媒体引用的占位符
+--------------------------+-----------+-------------------+
```

### 示例：将 PDF 媒体集转换为新的 PNG 媒体集

在此示例中，我们将遍历 PDF 媒体集中的所有媒体项，并将它们保存为 PNG 图像。

输入示例：

![输入PDFs](../../../images/foundry/building-pipelines/pdf_input.png)

注意，`list_media_items_by_path_with_media_reference()` 返回一个数据框，这允许你对输出执行 PySpark 函数。在此示例中，我们收集 `mediaItemRid` 列的值以作为数组进行遍历：

```python
from transforms.api import transform
from transforms.mediasets import MediaSetInput, MediaSetOutput

# 使用装饰器定义transform函数，指定输入和输出的媒体集路径
@transform(
    pdfs=MediaSetInput('INPUT_MEDIA_SET_PATH'),  # 输入媒体集路径
    output_pngs=MediaSetOutput('OUTPUT_MEDIA_SET_PATH')  # 输出媒体集路径
)
def upload_images(ctx, pdfs, output_images):
    # 获取所有媒体项的列表，包含媒体引用
    media_items_listing = pdfs.list_media_items_by_path_with_media_reference(ctx)

    # 提取媒体项的RID（资源标识符）列表
    rid_list = media_items_listing.rdd.map(lambda x: x.mediaItemRid).collect()

    # 遍历RID列表，将每个PDF转换为PNG并存储到输出媒体集中
    for rid in rid_list:
        output_png = pdfs.transform_document_to_png(rid, 0)  # 将PDF第一页转换为PNG
        output_images.put_media_item(output_png, "PNG_"+rid)  # 存储转换后的PNG文件
```

在这个代码中，我们通过装饰器定义了一个transform函数`upload_images`，它接收PDF文件并将其转换为PNG格式。函数首先获取所有媒体项的RID列表，然后遍历该列表，将每个PDF的第一页转换为PNG文件，并将转换后的文件存储到指定的输出媒体集中。
这将生成一个包含PNG文件的输出媒体集（如元数据属性中所述）：

![输出PNG](../../../images/foundry/building-pipelines/png_output.png)

在我们的[文档](/zh/foundry/data-integration/media-sets/#/#reference-built-in-transformations)中查看可用的开箱即用变换列表。

## 4. 测试你的更改

:::callout{theme="neutral"}
在Foundry中，媒体集可以像代码库一样分支。分支对于测试多步骤数据管道的设计非常有用。例如，你可以在不破坏依赖于你分支的用户的下游依赖关系的情况下，单独测试数据管道的部分更改。
:::

编写完数据变换代码后，你应该测试所做的更改。测试可确保你的代码在合并更改之前按预期工作。

## 5. 提交你的更改

现在，你可以在代码库中提交更改以标记你所完成的工作。在你进行提交之前，你的工作默认会自动保存。提交专门标记你在达到停止点时的一组更改。

:::callout{theme="success"}
选择 **提交** 按钮以提交你的更改并对代码运行自动检查。选择 **搭建** 按钮也会提交你的更改，运行自动代码检查，并开始搭建输出数据集。要快速测试你的更改而不搭建数据集以确保代码通过代码检查，请选择 **提交**。否则，你可以跳到[搭建你的数据集](#build-your-dataset-on-your-branch)。
:::

## 6. 合并并搭建你的更改

一旦你对新的媒体集输出满意，与任何合作者一起合并、搭建并查看更改。
