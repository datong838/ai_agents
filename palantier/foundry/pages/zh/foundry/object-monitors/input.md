---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/object-monitors/input/",
  "title": "输入",
  "page_id": "input",
  "category_id": "ontology",
  "section_id": "object-monitors",
  "previous": "/zh/foundry/object-monitors/monitor/",
  "next": "/zh/foundry/object-monitors/condition/",
  "scraped_at": "2026-07-14T04:35:03.017851+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 输入

:::callout{theme="warning"}
Object Monitors 已被 [Automate](/zh/foundry/automate/overview/) 取代。Automate 是一个完全向后兼容的产品，提供了平台中所有业务自动化的单一入口。
:::

监控输入是使用[对象集](/zh/foundry/analytics/datasets-object-sets/#object-sets)定义的。然后，监控[条件](/zh/foundry/object-monitors/condition/)可以引用输入的属性。输入可以用于计算指标，如聚合，或者监控何时在该输入中添加或移除Object。

输入对象集是通过在[Object Explorer](/zh/foundry/object-explorer/save-explorations/)中搭建一个**已保存的探索**创建的。您可以在[Object Explorer 中直接添加已保存的探索作为监控输入](/zh/foundry/object-monitors/create_new_object_monitor/#create-from-object-explorer)，或者在[Object Monitors 应用程序中配置新监控时](/zh/foundry/object-monitors/create_new_object_monitor/#create-from-object-monitors-application)添加。

在Object Monitors应用程序中查看Object监控时，监控输入显示在概览部分。点击一个监控以打开概览面板。

![在 Object Monitors 应用程序中查看输入](../../../images/foundry/object-monitors/input_shown_in_management_app.png)

在Object Explorer中查看特定已保存的探索时，使用此探索作为输入的Object监控会显示在屏幕右上角的**监控**弹出框中。

![在 Object Explorer 中使用已保存探索的监控列表](../../../images/foundry/object-monitors/list_of_monitors_for_exploration.png)
