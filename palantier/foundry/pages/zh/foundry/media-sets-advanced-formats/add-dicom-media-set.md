---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/media-sets-advanced-formats/add-dicom-media-set/",
  "title": "添加DICOM媒体集",
  "page_id": "add-dicom-media-set",
  "category_id": "data-integration",
  "section_id": "media-sets-advanced-formats",
  "previous": "/zh/foundry/geotemporal-series/faq/",
  "next": "/zh/foundry/media-sets-advanced-formats/add-audio-transcription/",
  "scraped_at": "2026-07-13T06:30:02.208198+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 添加DICOM媒体集

本指南将介绍如何将DICOM (`.dcm`) 文件导入到Foundry中作为[媒体集](/zh/foundry/data-integration/media-sets/)。

![显示在Foundry中使用DICOM文件所需步骤的图表。](../../../images/foundry/media-sets-advanced-formats/dicom-diagram.png)

## 第1部分：导入DICOM文件

首先，您需要创建一个新的媒体集，并将DICOM文件添加到媒体集中。

1. 导航到要创建媒体集的文件夹中。选择 **新建 > 媒体集**。 <br><br>
   ![添加新媒体集。](../../../images/foundry/media-sets-advanced-formats/add-new-media-set.png) <br><br>
2. 输入您的媒体集名称。选择 **DICOM** 作为媒体类型，选择 **批处理** 作为延迟。选择 **创建媒体集** 以创建DICOM媒体集。 <br><br>
   ![创建一个DICOM媒体集。](../../../images/foundry/media-sets-advanced-formats/create-dicom-media-set.png) <br><br>
3. 接下来，向媒体集中添加一个或多个 `.dcm` 文件。 <br><br>
   ![向媒体集中添加文件。](../../../images/foundry/media-sets-advanced-formats/dicom-media-set.png) <br><br>
   **DICOM** 媒体集类型包括如 `Patient ID` 和 `Study ID` 的元数据。

您可以选择一个DICOM文件，并通过左右或上下拖动来更改对比度和曝光。

![上下左右拖动以更改对比度和曝光。](../../../images/foundry/media-sets-advanced-formats/change-exposure.gif)

## 第2部分：创建Object类型

接下来，您需要创建一个新的流水线，将媒体集变换为可以在Foundry中使用的Object类型。

[了解有关为媒体集创建流水线的更多信息](/zh/foundry/building-pipelines/create-batch-pipeline-pb-media-set/)。

1. 通过从 **所有操作** 下拉菜单中选择 **创建新流水线** 来创建流水线。 <br><br>
   ![创建新流水线选项被高亮显示。](../../../images/foundry/media-sets-advanced-formats/create-pipeline.png) <br><br>
2. 媒体集将自动添加到流水线中。选择 **变换** 以将媒体集转换为表。 <br><br>
   ![变换选项被高亮显示。](../../../images/foundry/media-sets-advanced-formats/transform-dicom-media-set.png) <br><br>
3. 选择 **将媒体集转换为表行**，然后选择 **应用**。 <br><br>
   ![媒体集变换为表。](../../../images/foundry/media-sets-advanced-formats/convert-dicom-to-table-rows.png) <br><br>
   在生成的表中，每一行代表媒体集中的一个DICOM文件。 <br><br>
   ![表格中有四行对应媒体集中的四个DICOM文件。](../../../images/foundry/media-sets-advanced-formats/dicom-media-set-table.png) <br><br>
4. 通过从右侧面板的 **流水线输出** 菜单中选择 **添加流水线输出** 来创建一个Object类型。 <br><br>
   ![添加流水线输出选项被高亮显示。](../../../images/foundry/media-sets-advanced-formats/add-pipeline-output.png) <br><br>
   选择 **Object类型** 选项。 <br><br> <img alt="添加Object类型流水线输出。" src="../../foundry-docs/media-sets-advanced-formats/media/add-pipeline-output-object-type.png" width=400> <br><br>
5. 输入Object类型的名称，例如 `DICOM媒体集`。您可以通过选择属性右侧的三点，然后选择 **设为主键** 来将 `Media Item Rid` 属性设置为主键。 <br><br> <img alt="DICOM媒体集文件映射。" src="../../foundry-docs/media-sets-advanced-formats/media/create-dicom-object-type.png" width=400> <br><br>
   完成后，您可以[保存并部署流水线](/zh/foundry/pipeline-builder/outputs-deliver-pipeline/)。

流水线部署后，您可以在Object Explorer或Ontology Manager中查看Object类型。

## （非必填）第3部分：创建Workshop模块

您可以通过选择 **创建Workshop模块** 来打开Workshop。

![创建Workshop模块。](../../../images/foundry/media-sets-advanced-formats/create-workshop-module.png)

Workshop将自动生成有用的微件，如Object表和预览。

![带有DICOM文件Object表的Workshop模块。](../../../images/foundry/media-sets-advanced-formats/dicom-workshop-module.png)

[了解有关在Workshop中创建微件的更多信息](/zh/foundry/workshop/concepts-widgets/)。
