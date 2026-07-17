---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-integration/media-sets/",
  "title": "媒体集（非结构化数据）",
  "page_id": "media-sets",
  "category_id": "data-integration",
  "section_id": null,
  "previous": "/zh/foundry/data-integration/streams/",
  "next": "/zh/foundry/data-integration/branching/",
  "scraped_at": "2026-07-13T05:30:08.009339+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 媒体集（非结构化数据）

一个**媒体集**是具有共同模式的媒体文件的集合，例如相同格式的文件。媒体集旨在处理大规模的非结构化数据，并支持处理音频、图像、视频和文档等媒体项。媒体集支持灵活的存储、计算优化和模式特定的变换，以增强媒体工作流和管道。

![媒体集支持导入音频、图像、视频和文档。](../../../images/foundry/data-integration/mediasetsGA.png)

媒体集工作流示例包括：

* 通过管道构建器从PDF中提取文本以支持内容分析
* 在地图应用中使用栅格切片（TIFF，NITF）进行地理空间分析
* 使用管道构建器处理医学影像文件（DICOM格式）

要开始搭建管道，请按照以下步骤操作：

* [导入媒体到Foundry](#import-media)
* [通过代码仓库或管道构建器变换媒体](#transform-media-in-foundry)
* [将媒体本体化](#ontologize-media-using-media-references)

## 支持的媒体集文件类型

以下文件类型支持作为媒体集：

* 音频
  * WAV (`.wav`)
  * MP3 (`.mp3`)
  * NIST SPHERE (`.sph`)
  * FLAC (`.flac`)
* 文档
  * PDF (`.pdf`)\*
* 图像
  * PNG (`.png`)
  * JPEG (`.jpg`, `.jpeg`)
  * JP2K (`.jp2`)
  * BMP (`.bmp`)
  * TIFF (`.tiff`, `.tif`)
  * NITF (`.nitf`)
  * DICOM (`.dcm`)
* 视频
  * MP4 (`.mp4`)
  * MOV (`.mov`)
  * TS (`.ts`)

:::callout{theme="warning" title="PDF支持"}
需要专有功能查看或受密码、数字签名或加密保护的PDF文件不支持。
:::

## 导入媒体

可以通过[直接上传](/zh/foundry/projects/manually-upload-data/)、在数据连接中与外部源系统的连接、API发布和变换（包括[外部变换](/zh/foundry/data-integration/external-transforms/)）配置媒体集以进行导入。

### 直接上传

要通过直接上传将媒体文件导入媒体集，请将文件拖放到您的新媒体集中。文件必须符合创建媒体集时指定的预期文件类型才能上传到媒体集。

1. 首先，通过在项目中选择**新建**并从搜索栏中选择`媒体集`来创建一个新的媒体集，如下所示。

![从项目创建媒体集](../../../images/foundry/data-integration/project-add-media-set-dialog.png)

2. 接下来，为新的媒体集选择所需的媒体文件类型，然后选择**创建媒体集**。

![选择媒体文件类型](../../../images/foundry/data-integration/add-media-set-welcome-page.png)

3. 创建媒体集后，可以通过将媒体拖放到空的媒体集上或选择**从计算机中选择**提示上传媒体。

![从空媒体集上传](../../../images/foundry/data-integration/empty-media-set-action.png)

### 数据连接

可以使用数据连接与外部源的同步导入媒体集。在[媒体集同步文档](/zh/foundry/data-connection/media-set-sync/)中可以找到详细的操作步骤。

要创建新的媒体集[同步](/zh/foundry/data-connection/set-up-sync/)，请导航到所需[源](/zh/foundry/data-connection/set-up-source/)的**概览**选项卡。

创建同步后，在媒体集视图中触发搭建以使媒体出现在您的媒体集中。

您也可以通过**选择源**选项将现有源连接到新的媒体集中。

![将现有源添加到媒体集](../../../images/foundry/data-integration/add-media-set-welcome-page-add-source.png)

#### 虚拟存储

对于支持的源类型，媒体集可以选择配置为直接从外部源系统读取，因此无需将数据复制到Foundry的后台存储中（“虚拟媒体集”）。

目前，虚拟媒体集仅支持某些源类型。如果您对其他源类型的虚拟存储感兴趣，请联系Palantir支持。

![存储策略](/resources/foundry/data-integration/media-set-storage-policy.png)

### 外部变换

对于具有REST API的源，可以通过[外部变换](/zh/foundry/data-integration/external-transforms/)将媒体导入媒体集。

### 管道构建器

媒体集也可以直接导入到管道构建器中。[了解在管道构建器中可用的上传方法。](/zh/foundry/pipeline-builder/datasets-add/)

## 保留策略

您可以为媒体集配置基于时间的保留策略，例如14天，以便不需要永久存在的数据。媒体项仅在保留窗口内可访问，之后将被永久删除。这是一个有助于最小化存储成本的选项。

一旦媒体项的保留窗口到期，它将永远无法再次访问，并将被删除。例如：

* 当保留窗口从30天减少到7天时，所有超过新窗口（7天）天数的媒体项将立即无法访问。
* 当保留窗口从7天扩展到30天时，之前过期的媒体项（7天零1秒）将不会再次可访问。即使保留期更改为“永久”，也是如此。

## 在Foundry中变换媒体

### 管道构建器

在[管道构建器](/zh/foundry/pipeline-builder/overview/)中提供了常见的媒体集变换。[了解如何在管道构建器中搭建带有媒体集的批处理管道。](/zh/foundry/building-pipelines/create-batch-pipeline-pb-media-set/)

以下是一个在PDF上使用的文本提取（OCR选项）面板的示例：

![在管道构建器上的文本提取](../../../images/foundry/data-integration/pipeline_builder_pdf_ocr_board.png)

如果您对当前不可用的变换感兴趣，请联系您的Palantir代表。

### 代码仓库

媒体集也支持通过[导入`transforms-media`库](/zh/foundry/transforms-python/use-python-libraries/)在Python变换中使用的专门变换，如PDF文本提取、光学字符识别（OCR）、图像切片和元数据解析。

可以在[使用Python变换的媒体集文档](/zh/foundry/transforms-python/media-sets/)中找到常见变换。

以下是您如何在代码仓库中开始使用媒体集的示例：

```python
from transforms.api import transform
from transforms.mediasets import MediaSetInput, MediaSetOutput

# 使用装饰器 @transform 来定义一个数据转换函数
@transform(
    images=MediaSetInput('/examples/images'),  # 输入媒体集路径
    output_images=MediaSetOutput('/examples/output_images')  # 输出媒体集路径
)
def translate_images(images, output_images):
    ...
```

此代码中，使用了 `transforms` 库中的功能来处理媒体数据集。`translate_images` 函数被装饰器 `@transform` 修饰，表示这是一个数据转换函数。`MediaSetInput` 和 `MediaSetOutput` 分别定义了输入和输出的媒体集路径。

### 访问模式

高级用户和开发人员可以利用媒体集的*访问模式*，这些模式是预先配置的变换，可以按需在媒体集中的媒体项上执行。访问模式具有存储和优化调整的持久性策略，提供在每次请求时重新计算、首次请求后无限期保留输出或缓存一段时间的选项。

Foundry平台利用访问模式以最佳方式处理或呈现媒体集项。例如：

* Workshop中的PDF缩略图和预览
* Preview应用中的缓冲音频波形
* Map中的瓦片化卫星影像

默认可用的访问模式集是根据配置的媒体集模式确定的。额外的变换通过API调用注册为媒体集的访问模式。

## 媒体引用

媒体集中的项可以使用*媒体引用*进行引用。媒体引用使您可以在Foundry中使用媒体项，而无需复制媒体项本身。

使用*媒体引用*在数据集中引用媒体集项。这对于将媒体项与元数据或其他信息以表格格式关联很有用。例如，您可以将原始PDF与其文件名、页数和提取的文本关联为附加列。

您还可以将媒体引用用作[模型适配器](/zh/foundry/integrate-models/model-adapter-overview/)的批量推理管道的输入。

要为您的媒体集生成媒体引用列表，请在Pipeline Builder中使用`Get media references`函数。您还可以通过导入`transforms-media`库并调用`list_media_items_by_path_with_media_reference`方法，在Python变换中生成媒体引用：

```python
from pyspark.sql import functions as F
from transforms.api import transform, Input, Output
from transforms.mediasets import MediaSetInput

@transform(
    metadata_out=Output("{YOUR_OUTPUT_METADATA_DATASET}"),  # 指定输出数据集
    mediaset_in=MediaSetInput("{YOUR_MEDIA_SET_RID}")       # 指定输入媒体集资源ID
)
def compute(ctx, mediaset_in, metadata_out):
    # 获取媒体项目的路径及其引用
    media_references = mediaset_in.list_media_items_by_path_with_media_reference(ctx)

    # 定义列的类型，'mediaReference' 是引用类型，这样可以在数据集中启用内联缩略图
    column_typeclasses = {'mediaReference': [{'kind': 'reference', 'name': 'media_reference'}]}

    # 将数据写入输出数据集，同时指定列类型
    metadata_out.write_dataframe(media_references, column_typeclasses=column_typeclasses)
```

## 使用媒体引用对媒体进行Ontology化

使用媒体引用[对象属性](/zh/foundry/object-link-types/properties-overview/)在构建于Ontology的应用中高效显示您的媒体。优化包括在Workshop或Object Explorer中更快和互动的预览，以及在Map中用于地理空间图像的平铺。

## 使用媒体引用属性的自定义逻辑

在[对象函数](/zh/foundry/functions/api-media/)中使用具有媒体引用对象属性的对象。

您可以直接读取原始媒体项。此外，您还可以对媒体项执行常见的特定类型操作，例如：

* 对文档进行OCR
* 从文档中提取文本
* 音频转录
* 读取媒体项元数据

## 从媒体集中删除媒体项

您可以通过选择要删除的媒体项，并选择**删除**操作，从媒体集中删除媒体项。为了防止意外删除，此操作将要求您在弹出窗口中再次选择**确认删除**以确认您删除媒体项的意图。

![删除媒体项](../../../images/foundry/data-integration/delete-media-item.png)

一旦您成功删除了该项目，媒体集将刷新并显示成功消息。您现在可以查看没有被删除媒体项的媒体集。

![成功删除](../../../images/foundry/data-integration/delete-media-item-success.png)

## 媒体集计算使用

媒体集为平台带来了许多先进的开箱即用变换。除了通过变换和管道触发外，还可以通过前端与媒体项交互（例如，预览媒体项）触发媒体变换。此外，下载或流式传输媒体项的全部内容也是有成本的。

使用情况以Foundry计算秒为单位进行跟踪。下表描述了每个可用的变换，以及按每GB处理量的计算秒的使用率。

如果您与Palantir签订了企业合同，请在进行使用计算之前联系您的Palantir代表。

### 变换

*使用率以每GB的计算秒为单位衡量*

#### 全部

| 变换                 | 使用率          |
|----------------------|-----------------|
| 下载 / 流式传输      | 2               |

#### 图像

| 变换                      | 使用率          |
|---------------------------|-----------------|
| 旋转                      | 40              |
| 调整大小                  | 40              |
| 生成PDF                   | 40              |
| 调整对比度                | 75              |
| 裁剪 / 切片               | 75              |
| 灰度                      | 75              |
| 地理平铺                  | 75              |
| 渲染DICOM图像层           | 75              |
| 提取文本（OCR）           | 275             |
| 加密 / 解密               | 75              |

#### 音频

| 变换                | 使用率          |
|---------------------|-----------------|
| 转码                | 75              |
| 波形生成            | 75              |
| 转录                | 275             |

#### 视频

| 变换                          | 使用率          |
|-------------------------------|-----------------|
| 获取场景帧的时间戳            | 40              |
| 提取音频                      | 75              |
| 在时间戳提取帧                | 75              |
| 提取所有场景帧                | 275             |
| 使用HLS流式传输               | 275             |
| 转码                          | 275             |

#### 文档

| 变换                                  | 使用率          |
|---------------------------------------|-----------------|
| 将页面渲染为图像                      | 40              |
| 在边界框内将页面渲染为图像            | 40              |
| 获取PDF页面尺寸                       | 40              |
| 切分PDF范围                          | 75              |
| 提取表单字段                          | 75              |
| 提取目录                             | 75              |
| 提取页面上的文本（原始）              | 75              |
| 提取所有文本（原始）                  | 75              |
| 提取文本（OCR）                       | 275             |

## 媒体集限制

* 事务性媒体集每个事务的项目限制为10,000个。
* 非事务性媒体集没有项目限制。
* 媒体集中项目的路径不能超过256个字符。尝试将路径长度超过256个字符的项目添加到媒体集中将导致`MediaSet:MediaItemPathInvalid`错误。
