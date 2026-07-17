---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/preparation/preparation-tutorial/",
  "title": "创建一个简单的准备",
  "page_id": "preparation-tutorial",
  "category_id": "data-integration",
  "section_id": "preparation",
  "previous": "/zh/foundry/preparation/getting-started/",
  "next": "/zh/foundry/preparation/project-references/",
  "scraped_at": "2026-07-13T06:05:51.001090+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建一个简单的准备

:::callout{theme="warning"}
准备已被[Pipeline Builder](/zh/foundry/pipeline-builder/overview/)替代，因此不再是清理和准备数据的推荐方法。Pipeline Builder使您能够轻松地清理和准备数据以用于管道，同时还提供[Marketplace](/zh/foundry/marketplace/overview/)支持。
:::

以下教程将指导您如何使用准备以将原始数据的电子表格变换为已清理和准备好的数据集，以便进行分析。

本教程使用来自陨石学会的数据，通过[NASA 数据门户 ↗](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh)。您可以在自己的准备实例中使用此示例数据集进行操作：

[下载 meteorite\_landings\_raw](../../foundry-docs/preparation/media/meteorite_landings_raw.csv)

此数据集包含在地球上发现的陨石的原始数据。

数据集包括每个陨石的名称、质量、分类及其他识别信息，以及其被发现的年份和发现位置的坐标。

我们建议在[上传到 Foundry](/zh/foundry/projects/manually-upload-data/)之前打开 CSV 文件以查看数据。

## 1. 创建一个准备

我们将起始通过创建一个新的准备。

1. 首先，将 `meteorite_landings_raw.csv` 文件上传到 Foundry。

2. 然后，导航到 `meteorite_landings_raw` 数据集，右键单击并选择**在准备中清理**。

这将创建一个新的[准备](/zh/foundry/preparation/overview/#preparation)。您应该以有意义的名称保存您的准备，以便在您的文件中更容易找到。

3. 最后，点击**保存**并选择准备的名称和保存位置。

:::callout{theme="neutral"}
您创建但未明确保存的准备默认存储在**文件 > .auto-save**中。
:::

## 2. 清理数据

现在，检查数据集并识别并修复您发现的任何数据质量问题。

### 修剪空白

1. 首先，点击表格中的**名称**列：

<img src="../../foundry-docs/preparation/media/tutorial_table_namecol.png" style="max-height: 256.0px;" />

下方的面板将显示有关列中数据的一些信息：统计数据、图表等：

<img src="../../foundry-docs/preparation/media/tutorial_namecol.png" style="max-height: 512.5px;" />

您可以从统计面板中看到一些值已被标记为**需要修剪**，这意味着在值的开头或结尾有多余的空白。

2. 将鼠标悬停在粉色灯泡上，然后点击**修剪空白**按钮以解决此问题。

<img src="../../foundry-docs/preparation/media/tutorial_namecol_trim.png" style="max-height: 289.5px;" />

在列统计刷新后，您现在应该会看到**需要修剪**的计数已变为零，并且列已成功清理。您还将在屏幕右侧的**数据集更改**列表中看到添加的**修剪空白**更改：

<img src="../../foundry-docs/preparation/media/tutorial_changes_trimname.png" style="max-height: 183.0px;" />

### 将 `year` 列变换为日期

现在，让我们移至 **year** 列。您可以在表格中看到该列的数据类型为**时间戳**。然而，我们只希望它是一个**日期**。

1. 首先，点击**更改类型**按钮并从下拉列表中选择**日期（整天）**。

2. 点击**更改类型**按钮。

<img src="../../foundry-docs/preparation/media/actions_changetypetodate.png" style="max-height: 126.5px;" />

### 将地理位置值设置为 `null`

最后，让我们看看 **GeoLocation** 列。您将在直方图中看到大量行的值为\*\*(0.000000,0.000000)\*\*，这不是一个有效的地理位置。

<img src="../../foundry-docs/preparation/media/tutorial_geolocationcol_values.png" style="max-height: 145.5px;" />

让我们通过将这些值设置为 `null` 来修复这些值。

1. 首先，在直方图中选择 **(0.000000, 0.000000)** 值。
2. 接下来，点击**更改数据（针对所选行）**下的**新值**操作。
3. 最后，在文本框中输入 `/NULL`，然后点击**应用**以将这些值设置为 `null`。

<img src="../../foundry-docs/preparation/media/actions_newvalue_null.png" style="max-height: 187.0px;" />

## 3. 保存数据集的已清理版本

现在我们已经清理了数据质量问题，我们可以保存一个新的、已清理版本的数据集。

1. 首先，点击屏幕顶部的**另存为数据集**按钮。
2. 然后，为新的已清理数据集选择一个名称和位置。将出现一个弹出窗口，指示新数据集正在搭建中。

<img src="../../foundry-docs/preparation/media/tutorial_building.png" style="max-height: 95.5px;" />

将有一个指示**输出：**的新数据集的链接。随着您对准备进行更改，可以使用**更新**按钮更新输出数据集。

:::callout
要在不必保存新数据集的情况下在 Contour 中试用您的清理结果，请点击屏幕顶部的**分析**按钮。
:::
