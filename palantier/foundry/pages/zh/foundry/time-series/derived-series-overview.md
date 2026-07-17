---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/derived-series-overview/",
  "title": "派生序列",
  "page_id": "derived-series-overview",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/advanced-setup/",
  "next": "/zh/foundry/time-series/setup-derived-series/",
  "scraped_at": "2026-07-13T06:11:03.317528+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 派生序列

派生序列允许用户保存和复制通常应用于原始（非派生）时间序列的计算和变换。通过将此数据保存为Palantir资源，派生序列可以被共享并保存到Ontology中。一旦在Ontology中，派生序列的行为就像原始时间序列，但它们是即时计算的。这消除了在整个平台上管理或存储派生数据或重复这些计算的需要。

![派生序列概览](../../../images/foundry/time-series/derived-series-overview-graphic.svg)

以下指南解释了如何在[Quiver](/zh/foundry/quiver/overview/)中创建派生序列并将其保存到Ontology以在平台上使用。

## 要求

以下部分解释了创建派生序列时必须遵循的要求。

### 逻辑要求

1. 派生序列逻辑是基于根对象类型模板化的，因此必须在\_单一\_根对象上操作。如果逻辑需要其他对象类型上的时间序列输入，则必须将该对象类型设置为[\_传感器\_对象类型](/zh/foundry/time-series/create-sensor-ot/)。

例如，Quiver中的**对象时间序列属性卡片**允许选择当前对象类型的时间序列属性以及其传感器对象类型上的时间序列数据：

![Quiver中的"对象时间序列属性"卡片下拉菜单，显示了根对象和链接的传感器对象上的时间序列属性。](../../../images/foundry/time-series/derived-series-quiver-tsp-card.png)

2. 在关联传感器上创建派生序列时，应从Quiver中的根对象类型访问它们，而不是手动进行搜索。

3. 除了时间序列属性外，属性引用只有在直接引用于**时间序列公式**卡片中时才会被模板化。

![在"时间序列公式"卡片中的直接属性引用。](../../../images/foundry/time-series/derived-series-property-reference.png)

### 权限要求

要保存派生序列，需要在绑定对象类型上具有[对象类型编辑权限](/zh/foundry/ontologies/ontology-permissions/#create-new-resources-with-ontology-roles)。

要使用自动Ontology保存，配置必要的传感器对象类型和操作类型需要相同的权限。您还必须满足操作类型的[提交标准](/zh/foundry/action-types/submission-criteria/)。此外，您必须能够查看根对象类型和传感器对象类型的对象。具有受限视图数据源的对象类型是支持的；然而，如果用户可以查看一个根对象，他们也应该能够查看其所有链接的传感器对象（反之亦然）以用于给定的派生序列。

### 自动Ontology保存的传感器对象类型要求

1. 用于自动保存到Ontology的传感器对象类型的主键必须是`字符串`类型。
2. 传感器对象类型必须使用[Object Storage V2](/zh/foundry/object-backend/overview/#object-storage-v2-architecture.md)存储；这是为了让操作能够写入时间序列属性。
3. 传感器对象类型必须启用编辑。
4. 根对象类型和传感器对象类型之间必须有一个单一的[一对多基数链接](/zh/foundry/object-link-types/create-link-type/#configure-a-new-link-type)，根对象类型位于"一"侧。

### 自动Ontology保存的操作类型要求

[自动保存派生序列到Ontology](/zh/foundry/time-series/setup-derived-series/#step-2-ontology-saving)是通过传感器对象类型上的操作执行的。

如果以下任何要求未满足，您将无法选择用于自动Ontology写入的操作类型：

1. 每个操作类型必须只有一个规则。
2. 操作类型参数不得使用限制可提供值的约束。同样，操作类型参数不得使用导致值约束的覆盖。这些都是严格禁止的，即使约束是合理的。
3. 操作类型不应有未使用的参数。如果参数未使用，则无法配置为必需。
4. 未映射的传感器对象属性的参数必须配置为"非必需"。未映射的属性是指传感器对象类型上不用于根对象类型的任何外键。
5. 操作类型提交标准不得使用基于参数的条件。

您必须创建三个独立的操作类型：创建、修改和删除。以下列出了这些操作类型的规则。

##### `创建对象`操作类型

**规则：** 每个属性类型使用相同类型的参数并编辑对象类型的所有属性。如果您使用Ontology Manager配置操作类型，您必须从左侧的**表单**选项卡手动创建主键的字符串参数。

![一个"创建对象"操作类型的例子。](../../../images/foundry/time-series/derived-series-create-object-action.png)

##### `修改对象`操作类型

**规则：** 类似于`创建对象`操作类型，`修改对象`操作类型应使用与相关属性类型相同类型的参数，并应编辑除主键之外的所有属性。

![一个"修改对象"操作类型的例子。](../../../images/foundry/time-series/derived-series-modify-object-action.png)

##### `删除对象`操作类型

**规则：** 配置`删除对象`操作类型以删除传感器对象类型。不需要进一步的属性或参数配置。

![一个"删除对象"操作类型的例子。](../../../images/foundry/time-series/derived-series-delete-object-action.png)

在下一节中了解更多关于[创建派生序列](/zh/foundry/time-series/setup-derived-series/)的信息。
