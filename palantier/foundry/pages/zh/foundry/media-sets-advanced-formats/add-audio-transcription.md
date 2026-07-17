---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/media-sets-advanced-formats/add-audio-transcription/",
  "title": "转录音频媒体集",
  "page_id": "add-audio-transcription",
  "category_id": "data-integration",
  "section_id": "media-sets-advanced-formats",
  "previous": "/zh/foundry/media-sets-advanced-formats/add-dicom-media-set/",
  "next": "/zh/foundry/microsoft-excel/transforms-excel-parser/",
  "scraped_at": "2026-07-13T06:22:42.212454+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 转录音频媒体集

本指南将介绍如何在Foundry中使用[媒体集](/zh/foundry/data-integration/media-sets/)进行音频转录。

## 第1部分：在Foundry中将音频文件导入为媒体集

首先，您应将音频文件导入为[媒体集](/zh/foundry/data-integration/media-sets/)。有两种方法可以实现：

* [直接上传](/zh/foundry/data-integration/media-sets/#direct-upload)
* [数据连接](/zh/foundry/data-connection/media-set-sync/)

导入后，您将能够查看音频媒体集。

![音频媒体集](../../../images/foundry/media-sets-advanced-formats/audio-media-set.png)

## 第2部分：通过Pipeline Builder转录音频媒体集

1. 在Pipeline Builder中创建一个新的管道。详细步骤可以在Pipeline Builder文档的[初始设置部分](/zh/foundry/building-pipelines/create-batch-pipeline-pb-media-set/#part-1-initial-setup)中找到。

2. 将您的音频媒体集添加到管道中。

   ![将音频媒体集添加到Pipeline Builder。](/resources/foundry/media-sets-advanced-formats/add-audio-media-set.png)

   您导入的音频媒体集应如下所示：

   ![已导入的音频媒体集。](../../../images/foundry/media-sets-advanced-formats/audio-media-set-in-pipeline-builder.png)

3. 使用**变换**将媒体集转换为表格行。

   ![将音频媒体集转换为表格行。](/resources/foundry/media-sets-advanced-formats/audio-media-set-to-table-rows.png)

   这将为您的媒体集中的项目生成媒体引用。媒体引用使您能够在Foundry中使用媒体项目，而无需复制该媒体项目本身。[了解更多关于媒体引用的信息](/zh/foundry/data-integration/media-sets/#media-references)。

4. 接下来，选择**将音频转录为文本**变换。

   ![将音频转录为文本变换。](../../../images/foundry/media-sets-advanced-formats/transcribe-audio-into-text-preview.png)

5. 指定**将音频转录为文本**变换的输入，并选择**应用**。

   ![变换的示例输入。](../../../images/foundry/media-sets-advanced-formats/transcribe-audio-into-text-inputs.png)
   使用步骤3中生成的`mediaReference`，并选择所需的语言。如果未提供语言，将从音频的前30秒推断。

6. 您可以在表格中预览转录输出。

   ![预览音频转录输出。](../../../images/foundry/media-sets-advanced-formats/audio-transcription-output-preview.png)

7. 如果需要，您可以继续使用可用的字符串变换来变换您的音频转录字符串输出。

## 第3部分：保存管道输出

选择所需的管道输出。您可以输出为**数据集**或选择通过选择**对象类型**输出来对输出进行本体化。创建对象类型将允许您在[**Workshop**](/zh/foundry/workshop/overview/)中使用您的管道输出。

[了解更多关于如何保存您的管道输出](/zh/foundry/building-pipelines/create-batch-pipeline-pb-media-set/#part-4-add-an-output)。
