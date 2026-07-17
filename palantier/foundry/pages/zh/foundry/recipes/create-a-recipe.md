---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/recipes/create-a-recipe/",
  "title": "创建配方",
  "page_id": "create-a-recipe",
  "category_id": "data-integration",
  "section_id": "recipes",
  "previous": "/zh/foundry/recipes/core-concepts/",
  "next": "/zh/foundry/recipes/view-recipes/",
  "scraped_at": "2026-07-13T06:06:22.777615+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建配方

:::callout{theme="danger"}
Recipes 应用程序处于稳定状态，不再进行更新。我们建议探索其他应用程序和功能来监控 Foundry 中的条件：

* [自动化:](/zh/foundry/automate/overview/) 创建在您的数据之上运行的自动化，跟踪个别搜索和对象，当满足某些条件时触发通知或其他操作。
* [Foundry 规则:](/zh/foundry/foundry-rules/overview/) 创建基于逻辑的规则，应用于数据集、对象和时间序列，当满足某些条件时触发警报。
* [大规模监控:](/zh/foundry/maintaining-pipelines/monitoring-views-intro/) 使用检查组或监控视图查看 Foundry 资源的指标更新，包括数据集、代理、计划、对象和链接类型。
* [Workshop:](/zh/foundry/workshop/overview/) 搭建一个警报收件箱或其他通知工作流，以配置当满足某些条件时将触发的操作。

如果您对实施监控应用案例的适当工作流有疑问，请联系 Palantir 客服支持。
:::

在 Foundry 中创建配方有多种方式。使用本指南学习如何从 Recipes 应用程序、数据集预览和 Quiver 中创建配方。

## 来自 Recipes 应用程序

从导航侧边栏打开 Recipes 应用程序。

![Foundry 导航侧边栏中的 Recipes](../../../images/foundry/recipes/see_all_recipes.png)

点击界面右上角的 **New Recipe**。

![Recipes 界面中的新配方按钮](../../../images/foundry/recipes/home-page-new-recipe.png)

然后，您将被引导选择通过配方监控的资源。

## 来自数据集预览

要从数据集预览应用程序创建新配方，请在 **操作** 菜单中选择 **Create a recipe**。

配方允许您通过定义以下内容发送数据集的预览：

* 感兴趣的列
* 随预览发送的消息
* 收件人
* 发送预览的条件
* 消息类型（电子邮件或通知）

:::callout{theme="neutral"}
预览最多可以发送五列。
:::

![在数据集预览中选择列](../../../images/foundry/recipes/data_selectcols.png)

## 来自报告

报告可以自动化以在计划的时间作为附加的 PDF 或电子邮件中的图像发送给指定的收件人。

从报告的 **操作** 菜单中，选择 **Email on a schedule**。

![在操作菜单中按计划发送电子邮件](../../../images/foundry/recipes/email.png)

然后，撰写一条消息以随预览一起发送。

![撰写预览消息](../../../images/foundry/recipes/report_email.png)

最后，安排电子邮件的发送。选择报告将发送的日期。请注意，时区将默认为配方创建者的本地系统时区。

![安排报告发送时间](../../../images/foundry/recipes/reports_schedule.png)
