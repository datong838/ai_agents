---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-health/create-watch-check-group/",
  "title": "创建和监视检查组",
  "page_id": "create-watch-check-group",
  "category_id": "data-integration",
  "section_id": "data-health",
  "previous": "/zh/foundry/data-health/check-groups-overview/",
  "next": "/zh/foundry/data-health/view-check-group/",
  "scraped_at": "2026-07-13T06:04:20.882433+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建和监视检查组

您可以通过点击数据健康应用中的**创建组**按钮来创建检查组：

<img src="./media/create-group.png" alt="创建组" width="300" >

这将打开一个包含以下选项的新窗口：

![检查组](/resources/foundry/data-health/check-groups.png)

| 组组件           | 描述                                                             | 是否必需 |
| ----------------- | ---------------------------------------------------------------- | -------- |
| **组名称**        | 在数据健康应用和通知中显示的检查组名称                           | 是       |
| **描述**          | 添加注释以提供额外的背景信息                                    | 否       |
| **计划**          | 仅关于检查的电子邮件通知频率                                    | 是       |
| **健康检查**      | 属于此组的各个检查                                               | 是       |

订阅检查组的用户将订阅摘要。这将根据配置的计划向用户发送汇总的摘要式通知。

您可以通过点击右上角的**监视**按钮订阅检查组。您必须拥有查看检查组的权限才能订阅它。检查组的所有者可以通过**操作**下拉菜单中的**管理权限**授予查看权限。

<img src="./media/checkgroup-manage-permissions.png" alt="订阅检查组" width="300" >

一旦您创建并订阅了一个组，了解更多关于[查看检查组](/zh/foundry/data-health/view-check-group/)的信息。
