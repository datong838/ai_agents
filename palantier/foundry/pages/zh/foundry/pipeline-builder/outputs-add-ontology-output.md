---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/outputs-add-ontology-output/",
  "title": "添加Ontology输出",
  "page_id": "outputs-add-ontology-output",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/outputs-add-dataset-output/",
  "next": "/zh/foundry/pipeline-builder/outputs-add-geotemporal-series-output/",
  "scraped_at": "2026-07-13T05:50:02.263474+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 添加Ontology输出

您可以选择添加Ontology输出，以引导您的管道集成到定义全局Ontology新元素的干净、结构化的数据中。添加输出指导可以帮助节省计算检查时间，并帮助告知您的工作流程的端到端创建。

Pipeline Builder目前支持从批量和流数据集创建Ontology对象和链接。然而，在Pipeline Builder中，无法启用编辑或配置由流数据集支持的对象的多对多链接。

## 添加对象类型输出

有两种方式可以添加对象类型输出。您可以通过管道输出面板创建一个空白对象，或在连接到变换节点的图形上创建一个已填充的对象。

### 使用管道输出面板

打开位于Pipeline Builder右侧的**管道输出**面板，然后选择**对象类型 > 添加**以创建一个空白对象模板，您可以在其中编辑对象名称、图标和属性。

<img src="../../foundry-docs/pipeline-builder/media/outputs-add-pipeline-output.png" alt="从图形添加对象。" width="600">

请注意，为方便起见，**复数名称**和**对象类型ID**将自动从**名称**中填充。

:::callout{theme="warning"}
您可以在Pipeline Builder中定义新对象，但无法修改或删除现有对象，除非它们是在Pipeline Builder中创建的。首次部署后，无法修改对象类型ID。
:::

<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-object.png" alt="通过管道输出面板配置对象类型。" width="800">

您现在可以通过选择**手动输入数据**或将现有数据集或变换的输出拖到此节点的输入来填充您的对象。

<img src="../../foundry-docs/pipeline-builder/media/outputs-configured-ontology-output.png" alt="通过管道输出面板配置对象类型。" width="800">

### 使用图形

选择您想从中创建对象的变换节点，然后选择**添加输出 > 新对象类型**。

<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-object-on-graph-1@2x.png" alt="从图形添加对象。" width="600">

<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-object-on-graph-2@2x.png" alt="从图形添加对象，第二个屏幕。" width="600">

:::callout{theme="warning"}
如果您的注册包含多个Ontology，您需要在对象创建时选择对象所属的Ontology。否则，将显示错误信息`必须指定一个Ontology才能发布Ontology类型输出`。要设置Ontology，请在底部面板或对象上选择**设置Ontology**，如下所示。
:::

<img src="../../foundry-docs/pipeline-builder/media/outputs-set-ontology.png" alt="如果您的管道中需要，在哪里设置Ontology的截图。" width="800">

## 启用对象类型上的编辑

如果对象是在Pipeline Builder中创建并由批量数据集支持的，您可以在Pipeline Builder或Ontology Manager中启用对象类型上的编辑。

:::callout{theme="warning"}
流支持的对象类型目前不支持编辑。有关详细信息，请参见[流对象类型的限制](/zh/foundry/object-indexing/funnel-streaming-pipelines/#current-product-limitations-of-streaming-object-types)。
:::

要启用编辑，请在右侧面板中悬停在对象类型上并选择**编辑**。切换**允许编辑此类型的对象**。保存并部署您的管道以使此功能生效。

<img src="../../foundry-docs/pipeline-builder/media/outputs-allow-edits.png" alt="启用编辑对话框，选择了Person对象类型。" width="800">

## 添加链接类型输出

一旦添加了对象类型输出，您可以定义链接类型输出。与对象输出类似，这些可以在面板中或图形上创建。

### 使用管道输出面板

在**管道输出**面板中，选择**链接类型 > 添加**。这将打开一个表单，您可以在其中定义链接类型的左侧和右侧。

:::callout{theme="warning"}
在Pipeline Builder中定义的链接只能使用在同一管道中创建的对象。在Ontology Manager应用程序中，您可以在Pipeline Builder中创建的对象和Ontology Manager中创建的对象之间创建链接。 <br>
首次部署后，链接类型ID或源和目标对象类型将不再能够修改。
:::

<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-link@2x.png" alt="通过管道输出面板配置链接类型" width="400">

#### 图例

**链接类型ID：** 这是一个自动生成的ID，唯一代表此链接。

**选择一个对象类型输出：** 从下拉菜单中选择一个对象类型。如果您的管道中没有任何对象输出，您将需要首先配置一个对象输出类型。

**基数：** 选择链接类型每一侧的基数。支持两种类型的基数：一对多和多对多。目前不支持一对一链接类型。在下面的例子中，假设有两种对象类型通过基数相关联：`Aircraft`对象类型和`Flight`对象类型。

* 一对多基数：这表示一个`Aircraft`可以链接到多个`Flights`。
* 多对多基数：这表示一个`Aircraft`可以链接到多个`Flights`，一个`Flight`可以链接到多个`Aircraft`。
  * 请注意，当您选择多对多基数时，您将看到一个提示，要求**单击并拖动数据集或变换的输出以用作合并表**。此表应包含第一个对象类型（在本例中为`Aircraft`）和第二个对象类型（在本例中为`Flight`）的主键之间的所有链接组合。
  * 下面是一个多对多基数的例子，其中一个`Class`对象可以链接到多个`Student`对象，一个`Student`对象可以链接到多个`Class`对象：

<img src="../../foundry-docs/pipeline-builder/media/outputs-many-to-many-link.png" alt="Pipeline Builder中多对多链接的示例。" width="800">

**主键/列：** 选择哪个属性用于创建链接的左侧。

* 在一对多基数链接类型中，主键将由对象类型确定。
* 在多对多基数链接类型中，选择合并表中映射到每个链接对象类型的主键的列。

**外键/列：** 选择哪个属性用于创建链接的右侧。

* 在一对多基数链接类型中，一个对象类型的外键属性必须引用另一个对象类型的主键属性。
* 在多对多基数链接类型中，选择合并表中映射到每个链接对象类型的主键的列。

**名称：** 填写链接类型每一侧的显示名称。链接类型的一侧代表到该对象类型的链接。`Aircraft`对象类型的显示名称描述了从`Flight`到`Aircraft`的链接。在本例中，您可以选择显示名称"指派飞机"，因为一个`Flight`有一个指派的`Aircraft`。

**复数显示名称：** 对于具有多基数的链接类型的侧面，您还将被提示填写复数显示名称，以便用户应用程序在显示链接对象时可以显示正确的名称。在我们的例子中，`Flight`对象类型的复数显示名称将描述从`Aircraft`到`Flight`的链接。我们可能会选择复数显示名称为"计划航班"，因为一个`Aircraft`有多个计划的`Flights`。

### 使用图形

选择您想从中创建链接的两个对象输出，然后右键单击并选择**新链接类型**。这将创建一个包含所有对象信息的链接。

<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-link-from-objects@2x.png" alt="从两个对象添加链接。" width="400">
<br>
<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-link-from-objects-panel@2x.png" alt="从两个对象填充的链接。" width="400">

或者，选择图形上的单个对象，以创建一个填充了一侧的新链接类型。

<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-link-from-object@2x.png" alt="从单个对象添加链接。" width="600">
<br>
<img src="../../foundry-docs/pipeline-builder/media/outputs-configure-link-from-object-panel@2x.png" alt="从一个对象填充一半的链接。" width="400">

## 解决Ontology验证错误

用户可能会进行管道更改，导致Ontology中出现验证错误。一些错误示例包括：

* 在Pipeline Builder和Ontology Manager中对同一对象类型或链接类型进行冲突的更改。
* 更改由管道外的链接类型引用的对象类型的主键。
* 对对象类型的模式进行破坏性更改，以致需要[模式迁移](/zh/foundry/object-edits/schema-migrations/)。

任何错误都将显示在右侧面板的**部署此管道**部分。在**错误**标签中，将有一条消息描述在部署之前需要进行的解决方案类型。

您必须解决这些错误才能部署您的管道。

<img src="../../foundry-docs/pipeline-builder/media/outputs-ontology-merge-confict.png" alt="在部署之前必须解决的Ontology验证失败的示例，并将用户带到Ontology Manager。" width="800">

当**解决**按钮显示一个箭头时，选择它将带您到Ontology Manager以解决验证错误。否则，您将能够直接在Pipeline Builder中解决错误。

### 在Ontology Manager中解决合并冲突

<img src="../../foundry-docs/pipeline-builder/media/outputs-ontology-manager.png" alt="解决按钮引导到的Ontology Manager页面。" width="800">

按照Ontology Manager中的提示应用合并冲突解决方案。如果您的更改影响潜在的编辑，您可以决定是放弃编辑还是使您的编辑与对象的最新版本兼容。否则，解决合并冲突不需要额外的说明，您可以选择**应用**。

<img src="../../foundry-docs/pipeline-builder/media/outputs-ontology-no-conflicts.png" alt="不需要对对象进行额外操作的弹出窗口截图。" width="600">

一旦更改被应用，Ontology将更新为最新更改，您可以选择**返回管道**。

<img src="../../foundry-docs/pipeline-builder/media/outputs-ontology-go-back-to-pipeline.png" alt="从一个对象填充一半的链接。" width="800">

在解决冲突后，您可能偶尔会遇到错误`Ontology类型输出与Ontology不同步`，当返回到您的管道时。这是因为管道尚未获取通过上述冲突解决工作流对Ontology输出所做的更改。

<img src="../../foundry-docs/pipeline-builder/media/outputs-ontology-outputs-out-of-date.png" alt="由于冲突解决后管道陈旧而导致Ontology类型输出不同步的示例。" width="800">

选择**解决**应能解决此问题，并允许您部署管道。

### 在Pipeline Builder中解决冲突

一些Ontology验证错误不需要切换到Ontology Manager。在下面的例子中，需要进行模式迁移，当Pipeline Builder中的对象类型模式与Ontology主分支上的最新模式不同时发生。选择**解决**以直接在Pipeline Builder中选择迁移策略。

<img src="../../foundry-docs/pipeline-builder/media/outputs-schema-migration-required.png" alt="在部署之前必须解决的模式迁移失败的示例。" width="800">

对于受影响的属性，您可以选择**从属性中删除编辑**或迁移您的编辑以使其与属性的最新版本兼容。

<img src="../../foundry-docs/pipeline-builder/media/outputs-schema-migrations.png" alt="从一个对象填充一半的链接。" width="800">

一旦选择了最佳方法，选择**应用迁移**。

## 将对象类型输出带回Pipeline Builder

您可以通过以下步骤将由数据集输出支持的对象类型带回Pipeline Builder：

在右侧面板中，选择**管道输出**旁边的齿轮图标。

<img src="../../foundry-docs/pipeline-builder/media/outputs-replace-with-objects.png" alt="选择符号以链接到Ontology Manager中的对象类型。" width="800">

选择**用对象替换**。这将打开**用Ontology类型输出替换数据集**对话框。

<img src="../../foundry-docs/pipeline-builder/media/outputs-replace-dataset-with-ontology.png" alt="选择符号以链接到Ontology Manager中的对象类型。" width="800">

选择您要转换回管道中相应对象的数据集输出，并选择**导入所选输出**。

<img src="../../foundry-docs/pipeline-builder/media/outputs-replace-dataset-with-ontology2.png" alt="选择符号以链接到Ontology Manager中的对象类型。" width="800">

保存您的更改并部署您的管道。

## \[已弃用] 在Pipeline Builder中放弃Ontology类型输出

在Pipeline Builder中放弃Ontology类型输出将把这些Ontology类型的管理转移到Ontology Manager。这意味着对这些Ontology类型的所有未来修改将只能在Ontology Manager中进行。要放弃Ontology类型，请选择您要放弃的对象类型。任何引用所选对象类型的链接类型将自动转移到Ontology Manager。

:::callout{theme="warning"}
只有在成功部署了`main`分支的最新保存版本后，才能用数据集输出替换Ontology类型输出。
:::

<img src="../../foundry-docs/pipeline-builder/media/outputs-disown-object.png" alt="选择了Student对象类型的放弃所选对象和链接类型。" width="800">

选择**放弃所选对象和链接类型**。

在此管道中，*对象类型*输出节点将转换为*数据集*输出节点，支持Ontology Manager中的对象类型。从最右侧面板中，通过选择输出旁边的图标导航到Ontology Manager中的对象类型。

<img src="../../foundry-docs/pipeline-builder/media/outputs-enable-edits-oma-link.png" alt="选择符号以链接到Ontology Manager中的对象类型。" width="800">

在放弃所选对象后，部署您的管道。
