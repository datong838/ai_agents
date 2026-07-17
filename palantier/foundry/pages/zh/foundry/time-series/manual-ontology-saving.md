---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/manual-ontology-saving/",
  "title": "手动保存派生序列至Ontology",
  "page_id": "manual-ontology-saving",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/setup-derived-series/",
  "next": "/zh/foundry/time-series/manage-derived-series/",
  "scraped_at": "2026-07-13T06:12:22.865529+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 手动保存派生序列至Ontology

:::callout{theme="neutral"}
如果您在创建对话框中选择了[自动保存派生序列](/zh/foundry/time-series/setup-derived-series/#step-2-ontology-saving)至Ontology的选项，则此设置部分不是必需的。
:::

[派生序列设置文档](/zh/foundry/time-series/setup-derived-series/)描述了用于管理派生序列的**逻辑资源**的准备过程。**Codex模板**是逻辑资源的模板化格式转换，允许逻辑在任何根Object上得到解决，只要它有正确的输入。

通过以下步骤，我们可以通过在绑定Object类型的时间序列属性上添加对模板化逻辑的引用，手动将派生序列添加到Ontology中。一旦添加到Ontology，派生序列将像原始时间序列一样运行，并且可以在Palantir应用中使用。

![显示派生序列资产架构的图表。](../../../images/foundry/time-series/derived-series-asset-structure-graphic.svg)

## 1. 访问Codex模板ID

Codex模板是用于存储模板化派生序列逻辑的隐藏Palantir资源。在继续之前，您需要找到派生序列的Codex模板RID。

首先，找到您的派生序列资源。您可以通过名称搜索它，或定位您在[**保存派生序列**对话框](/zh/foundry/time-series/setup-derived-series/#步骤2选择资源位置)中指定的文件夹。打开**概览**标签查看[派生序列管理页面](/zh/foundry/time-series/manage-derived-series/)。

从**派生序列详情**部分复制**模板RID**。

![在派生序列管理页面上显示的Codex模板RID。](../../../images/foundry/time-series/derived-series-codex-template-rid.png)

## 2. 将派生序列绑定到Ontology中的Object类型

时间序列绑定Object类型显示在[派生序列管理页面](/zh/foundry/time-series/manage-derived-series/)右侧的**详情**部分。

![“Delta压力”派生序列资源的“机器传感器”绑定Object类型。](../../../images/foundry/time-series/derived-series-bound-object-type.png)

:::callout{theme="warning"}
在派生序列设置期间指定的绑定Object类型是派生序列模板可以解决的\_唯一\_ Object类型。
:::

派生序列使用类似于\_原始\_时间序列的[时间序列属性](/zh/foundry/time-series/time-series-properties/) (TSPs)。然而，作为时间序列属性值，资源标识符（RID）而不是系列ID被使用。
查看以下选项，并选择是否将派生序列绑定到根或传感器Object类型。

### 选项1：绑定到根Object类型

要将派生序列绑定到根Object类型，请在根Object类型的支持数据源中创建一个新的字符串类型列（或使用现有列），并用Codex模板RID填充。在下例中，`Delta压力`派生序列模板RID已添加到十台机器中。

![包含Codex模板RID列的示例数据集。](../../../images/foundry/time-series/derived-series-root-dataset.png)

导航到Ontology Manager，并将包含新的Codex模板RID的列映射到时间序列属性（如果尚未映射）。查看如何[设置时间序列属性](/zh/foundry/time-series/time-series-properties/)以获取更多信息。

### 选项2：绑定到传感器Object类型

您必须为每个根Object创建一个传感器Object以应用此派生序列。

在绑定Object类型支持数据源的TSP支持的列中输入Codex模板RID。在我们的示例中，行1到10指的是原始系列ID，而行11到15通过Codex模板RID指的是派生序列。在下例中，五个传感器Object包含`Delta压力`派生序列模板RID被添加。

![派生序列传感器Object支持数据集的示例。](../../../images/foundry/time-series/derived-series-sensor-dataset.png)

如果您希望引用特定版本的逻辑，您的TSP值应如下所示：

```
{"templateRid":"ri.codex-emu.main.template.8da5f759-4b...","templateVersion":"0.0.x"}
```

## 派生序列属性数据源

目前，派生序列的数据源不需要在包含的时间序列属性数据源中列出。

:::callout{theme="warning"}
即使一个时间序列属性仅引用派生序列，该时间序列属性仍然必须列出一个数据源。作为一种解决方法，可以使用任何所需类型的时间序列同步。查看如何[创建时间序列同步](/zh/foundry/time-series/time-series-syncs/)以获取更多详细信息。
:::
