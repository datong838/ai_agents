---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/recipes/edit-a-recipe/",
  "title": "编辑配方",
  "page_id": "edit-a-recipe",
  "category_id": "data-integration",
  "section_id": "recipes",
  "previous": "/zh/foundry/recipes/configure-notifications/",
  "next": "/zh/foundry/transforms-python/overview/",
  "scraped_at": "2026-07-13T06:06:18.626080+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 编辑配方

:::callout{theme="danger"}
配方应用程序处于稳定状态，不再更新。我们建议探索其他应用程序和功能来监控Foundry中的条件：

* [自动化:](/zh/foundry/automate/overview/) 创建自动化操作，这些操作运行在您的数据之上，并跟踪个体搜索和Object，当满足特定条件时触发通知或其他操作。
* [Foundry规则:](/zh/foundry/foundry-rules/overview/) 创建基于逻辑的规则，应用于数据集、Object和时间序列，当满足特定条件时触发警报。
* [大规模监控:](/zh/foundry/maintaining-pipelines/monitoring-views-intro/) 使用检查组或监控视图查看Foundry资源的指标更新，包括数据集、代理、计划、Object和链接类型。
* [工作坊:](/zh/foundry/workshop/overview/) 搭建警报收件箱或其他通知工作流，以配置在满足特定条件时将触发的操作。

如果您对为您的监控应用案例实施适当的工作流有疑问，请联系Palantir支持。
:::

根据您的权限级别，您可以对配方执行不同的操作。可以通过配方管理页面编辑配方。了解更多关于[配方权限模型](/zh/foundry/recipes/core-concepts/#privacy-permissions-and-sharing)的信息。

首先，点击您想要修改的配方，然后选择设置齿轮以打开菜单。

![配方设置菜单](../../../images/foundry/recipes/edit_recipe_part1.png)

选择**编辑**，然后选择**配置**以修改配方。

![编辑配方配置](../../../images/foundry/recipes/edit_recipe_part2.png)

## 向配方添加接收者

要向现有配方添加接收者，请从**编辑**菜单中选择**接收者**。

注意，默认情况下，接收者的最大数量设置为25，以保持整体性能。

![编辑配方接收者](../../../images/foundry/recipes/add_recipients_to_existing.png)

## 静音或暂停配方

如果您希望停止接收来自特定配方的通知，您可以静音该配方。静音的配方不会被删除，但会停止发送通知。静音配方将会使您的通知静音，但配方的其他接收者仍会收到通知。

配方的所有者可以选择**暂停全部**，这将停止向所有接收者发送通知。这在接收者长时间不在电脑前不希望接收通知，或在监控传感器上有计划的维护事件时可能有用。

要静音或暂停配方，请选择配方面板上的设置齿轮以打开菜单。选择**状态**，然后根据您的偏好选择**静音**或**暂停**。

![静音或暂停配方](../../../images/foundry/recipes/mute_pause_recipe.png)

## 更改配方的到期日期

配方的到期日期可以随时从配方管理页面进行延长。

![配方即将到期](../../../images/foundry/recipes/change_expiration_part1.png)

点击您希望修改的配方，然后点击设置齿轮。从菜单中选择**状态**。

要延长活动配方，点击**延长**。

![延长活动配方](../../../images/foundry/recipes/change_expiration_part2.png)

要恢复已过期的配方，点击**恢复**。

![恢复已过期配方](../../../images/foundry/recipes/resume_expired_recipe.png)

此外，可以通过首先在配方管理页面选择配方卡片，然后从屏幕右侧的信息面板中选择**恢复**来延长配方。作者应收到一封电子邮件，提醒他们延长配方，其中包含指向此视图的链接。

![从管理页面恢复配方](../../../images/foundry/recipes/extend_recipe_part1.png)

![到期通知](../../../images/foundry/recipes/extend_recipe_part2.png)

了解更多关于[配方到期](/zh/foundry/recipes/core-concepts/#expiration)的信息。

## 删除配方

在配方管理页面，首先点击您想要修改的配方。然后，选择设置齿轮以打开菜单。选择**删除**。

:::callout{theme="warning"}
您只能删除您拥有的配方。已删除的配方将不再为该配方的其他接收者运行。要停止配方通知您而不删除它，请[静音配方](#mute-or-pause-a-recipe)。
:::

![删除配方](../../../images/foundry/recipes/delete_recipe.png)
