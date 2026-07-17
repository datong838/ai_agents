---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-health/notifications/",
  "title": "通知和问题",
  "page_id": "notifications",
  "category_id": "data-integration",
  "section_id": "data-health",
  "previous": "/zh/foundry/data-health/watching-checks/",
  "next": "/zh/foundry/data-health/checks-reference/",
  "scraped_at": "2026-07-13T06:04:23.654997+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 通知和问题

Data Health 与 Foundry 通知和电子邮件集成，以在检查失败时分别提供平台内通知和电子邮件。

## Foundry 通知

Data Health 将始终向失败检查的[监测者](/zh/foundry/data-health/watching-checks/)发送平台内通知：

![通知](/resources/foundry/data-health/notifications.png)

## 电子邮件通知

作为检查的监测者，您还可以启用失败检查的电子邮件通知。您可以通过导航到右上角的**个人资料图标**，点击**设置**，然后导航到**通知**选项卡来更改您的电子邮件和通知偏好设置：

![通知设置](/resources/foundry/data-health/notification-settings.png)

要接收检查更新，请确保勾选**搭建**部分下的所有内容。

## 与问题集成

您还可以配置 Data Health，以便在检查失败时自动报告问题，从而更轻松地进行调试和讨论：

![问题](/resources/foundry/data-health/issues.png)

要启用问题报告，只需在创建/编辑检查时勾选**当此检查失败时自动创建问题**框：

![启用问题](/resources/foundry/data-health/enabling-issues.png)

您还可以通过在下面的框中输入特定用户的姓名，自动将创建的问题指派给该用户。

:::callout{theme="neutral"}
Data Health 会在检查失败时提交问题，但一旦检查解决，它也可以自动关闭问题。
:::
