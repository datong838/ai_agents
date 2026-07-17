---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/dynamic-scheduling/scheduling-getting-started/",
  "title": "起始",
  "page_id": "scheduling-getting-started",
  "category_id": "ontology",
  "section_id": "dynamic-scheduling",
  "previous": "/zh/foundry/dynamic-scheduling/scheduling-overview/",
  "next": "/zh/foundry/dynamic-scheduling/scheduling-concepts/",
  "scraped_at": "2026-07-14T05:04:51.017997+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 起始

以下指南提供了实施动态调度工作流初始版本的步骤。请查看每个部分中引用的文档以获取更多信息。

## 1. 创建核心Ontology对象

您必须创建以下核心对象类型以搭建动态调度工作流：

* 创建一个`Task`或`Schedule`对象类型。这代表了分配给资源（如人员或对象）的时段。例如，`修理温度传感器`。
  * 对象类型必须具有属性，以持有外键以创建与资源对象类型的关系。
  * 此对象类型可以有一个“固定持续时间”布尔属性，以强制或不强制`Task`或`Schedule`的静态持续时间。
  * 您必须启用对此对象的编辑，因为开始/结束/持续时间和与资源的关系将在此过程中进行编辑。
* 创建一个或多个`Resource`对象类型，代表分配给`Task`或`Schedule`的资源。例如，需要在任务上工作的人员（`Mechanic`）和需要工作的元素（`Vehicle`）。
* 创建`Task`或`Schedule`对象类型与不同`Resource`对象类型之间的链接。

查看[动态调度Ontology原语文档](/zh/foundry/dynamic-scheduling/scheduling-ontology-primitives/)，以获取关于每个对象类型架构的更多信息。

## 2. （非必填）定义验证规则

验证规则是一种强制约束的方式，并决定是否接受对计划的编辑。

* 创建两个数据集：一个用于支持`Validation Rule`对象类型，一个用于支持`Validation Rule`与`Task`/`Schedule`之间的多对多关系。
  * 您可以通过在Pipeline Builder中[手动输入](/zh/foundry/pipeline-builder/datasets-add/#manually-enter-data-in-pipeline-builder)数据集来创建此数据集。
* 创建一个`Validation Rule`对象类型。这将存储执行验证的函数的RID和版本。
* 创建`Validation Rule`与`Task`/`Schedule`对象类型之间的多对多关系。
  * 使用特殊类型类设置链接：`schedules:schedulable-rule-link`。
* 创建一个代码库来编写验证规则的函数。给定一个`Task`/`Schedule`对象类型，函数应根据某些任意逻辑验证其是否“有效”。这些函数的RID和版本将手动存储在`Validation Rule`对象类型实例中。
  * 打开Ontology Manager找到函数的RID（例如`ri.function-registry.main.function.48e0044f-554a-4b0c-8879-18e0866dffb3`）和版本（例如`1.0.0`）。

查看[动态调度验证规则文档](/zh/foundry/dynamic-scheduling/scheduling-validation-rules/)，以获取关于验证规则的更多信息。

## 3. 在Ontology Manager中启用功能

您必须在Ontology Manager中为`Task`或`Schedule`对象类型启用**动态调度**功能。这样做将帮助您配置和自动生成动态调度工作流的操作和其他相关元素。

查看[动态调度功能向导文档](/zh/foundry/dynamic-scheduling/scheduling-ontology-primitives/#ontology-manager-wizard)，以获取关于启用此功能的更多信息。

## 4. 在Workshop中使用动态调度

在此阶段，您可以开始使用并记录在上述步骤中创建的不同元素上的决策。

1. 创建一个Workshop模块。
2. 添加调度甘特图微件。
3. 配置微件。
4. 排程、属性和验证更改。

查看[调度甘特图微件文档](/zh/foundry/dynamic-scheduling/scheduling-gantt-chart-widget/)以获取更多信息。
