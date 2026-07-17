---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/schedules-scheduler-aip/",
  "title": "调度器中的 AIP 功能",
  "page_id": "schedules-scheduler-aip",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/schedules-create-schedule/",
  "next": "/zh/foundry/pipeline-builder/dataexpectations-overview/",
  "scraped_at": "2026-07-13T05:51:17.908068+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 调度器中的 AIP 功能

在创建具有特定时间触发器的数据集搭建调度时，使用 AIP 生成调度配置。在 **新建调度** 视图侧边栏中输入一个调度触发提示，以生成复杂触发器的正确 cron 格式。

<img src="../../foundry-docs/pipeline-builder/media/schedules-aip-schedule-2.png" alt="由 AIP 提供支持的调度列表配置菜单图像。" width=450>

## 使用 AIP 功能

要在调度器中使用 AIP 辅助，在 Pipeline Builder 中打开您的图形，然后按照以下步骤操作：

1. 右键单击数据集节点，选择 **管理调度...**，然后选择 **创建新调度** 以进入数据沿袭应用。

2. 在 **新建调度** 视图中，找到 **何时搭建** 并选择 **在特定时间**。

3. 最后，选择由 AIP 双星图标表示的 **建议**，然后在提示中输入您偏好的调度描述，再按下紫色箭头图标。

要接受建议，选择 **保存**。要拒绝，选择 **建议**，然后输入新提示，或手动配置您的 cron 任务。

***

注意：AIP 功能的可用性可能会有所更改，并且可能因客户而异。
