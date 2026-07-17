---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/interfaces/create-interface/",
  "title": "创建界面",
  "page_id": "create-interface",
  "category_id": "ontology",
  "section_id": "interfaces",
  "previous": "/zh/foundry/interfaces/interface-overview/",
  "next": "/zh/foundry/interfaces/implement-interface/",
  "scraped_at": "2026-07-14T04:31:08.054496+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建界面

按照以下步骤在[Ontology Manager](/zh/foundry/ontology-manager/overview/)中创建一个新界面。

1. 首先，通过检查左侧面板顶部的**Ontologies**下拉菜单，确认您正在使用所选的Ontology。

2. 在同一左侧面板的**Resources**部分下选择**Interfaces**。在**Interfaces**页面，从屏幕右上角选择**New interface**。

或者，您可以从Ontology Manager导航栏右上角选择**New**下拉菜单，并选择**Interface**。

3. 输入界面的显示名称和API名称。您还可以非必填地提供界面的描述并选择合适的图标。

<img src="../../foundry-docs/interfaces/media/create-interface-metadata.png" alt="Interface metadata creation" width="800" />

4. 选择界面的共享属性。

<img src="../../foundry-docs/interfaces/media/create-interface-choose-properties.png" alt="Interface property selection" width="800" />

任何实现该界面的Object类型必须具有这些共享属性，或提供从本地属性到界面共享属性的映射。如果界面所需的共享属性不存在，您必须[创建它](/zh/foundry/object-link-types/create-shared-property/)。

5. 选择右上角的**Save**以更改您的Ontology。

## 创建界面链接类型（非必填）

如果您希望此界面链接到另一个界面或Object类型，您可以非必填地向界面添加任何[界面链接类型](/zh/foundry/interfaces/interface-link-types-overview/)。

<img src="../../foundry-docs/interfaces/media/create-link-type-constraint.png" alt="Add a link type constraint" width="800" />

1. 在左侧面板中选择**Link type constraints**。
2. 然后，在右上角选择**Create new link type constraint**。

<img src="../../foundry-docs/interfaces/media/create-link-type-constraint-modal.png" alt="Create a link type constraint" width="800" />

如果您的建模应用案例需要界面链接类型，任何实现该界面的Object类型必须添加一个新链接类型或满足界面链接类型约束的现有链接类型。
