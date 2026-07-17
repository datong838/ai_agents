---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/object-views/use-object-views-in-platform/",
  "title": "在平台中使用Object View",
  "page_id": "use-object-views-in-platform",
  "category_id": "ontology",
  "section_id": "object-views",
  "previous": "/zh/foundry/object-views/overview/",
  "next": "/zh/foundry/object-views/config-overview/",
  "scraped_at": "2026-07-14T04:35:59.920186+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在平台中使用Object View

您可以从Foundry中的多个点访问Object View，特别是在Workshop和Object Explorer中。具有适当权限的用户可以在Control Panel中配置Object View，以自定义设计、可见性等。

## 配置Object View

编辑某个对象类型的Object View所需的权限取决于该对象类型是否使用[Ontology角色](/zh/foundry/ontology-manager/ontology-roles-migration/)：

* 如果对象类型未使用Ontology角色，用户必须在[Control Panel](/zh/foundry/administration/enrollments-and-organizations-permissions/)中拥有`Object View Admin`应用权限，并在对象类型的输入数据源上拥有`Editor`角色。
* 如果对象类型使用Ontology角色，用户仅需在该对象类型上拥有`Ontology Editor`角色。

配置选项包括更改视图中的选项卡和微件，以及自定义设计和条件可见性。默认情况下，object view的配置基于Ontology中的对象类型定义。

管理员还可以使用Control Panel配置在Object View中使用的配置文件。配置文件允许用户查看与其角色相关的对象信息。

[了解更多关于配置Object View的信息。](/zh/foundry/object-views/config-overview/)

## 使用Object View

一旦您创建了Ontology，就可以在Foundry的不同应用程序中访问Object View。Object View是Workshop和Object Explorer的核心组件。

### Workshop

使用Workshop在您的模块中显示详细的object view微件或配置object view选项卡。

![Workshop中的Object View微件](/resources/foundry/object-views/object-view-widget-workshop.png)

了解更多关于在Workshop中使用[Object View微件](/zh/foundry/workshop/widgets-object-view/)和[配置Object View选项卡的信息。](/zh/foundry/object-views/config-tabs/)

### Object Explorer

使用Object Explorer，您可以访问Object View以查找您在Ontology中定义的对象的详细信息。搜索对象并选择它以打开object view。

![在Object Explorer中查找对象](/resources/foundry/object-views/object-explorer-object.png)

![选择对象以打开Object View](/resources/foundry/object-views/object-view-from-object-explorer.png)

[了解更多关于Object Explorer的信息。](/zh/foundry/object-explorer/overview/)
