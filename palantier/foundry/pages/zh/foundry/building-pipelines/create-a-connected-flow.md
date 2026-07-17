---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/building-pipelines/create-a-connected-flow/",
  "title": "创建连接流",
  "page_id": "create-a-connected-flow",
  "category_id": "data-integration",
  "section_id": "building-pipelines",
  "previous": "/zh/foundry/building-pipelines/logic-flows-overview/",
  "next": "/zh/foundry/building-pipelines/compass-file-lister/",
  "scraped_at": "2026-07-13T05:42:27.255621+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 创建连接流

在 Logic Flows 应用中，您可以：

* **创建新的** 连接流（右上角）
* 查看现有的连接流，按自动化分组

要打开应用，请访问 `/workspace/logic-flows`。

![Logic Flows 主页](../../../images/foundry/building-pipelines/lf-app-homepage.png)

要在 [Compass Files Lister](/zh/foundry/building-pipelines/compass-file-lister/) 中创建连接流，请按照以下步骤操作：

1. 创建新的连接流时，会出现一个对话框，允许您设置名称、项目和所需参数及配置。这些会在输入时验证，也可以通过单击 **Validate** 手动验证。 <br>对于 Compass Files lister 自动化，您需要设置输入文件夹和输出存储库。

   ![连接流创建UI（已填充）](../../../images/foundry/building-pipelines/lf-connection-ui-filled.png)

:::callout{theme="neutral"}
逻辑流是*项目范围*的，这意味着您必须指定将创建连接流资源的项目。连接流应与用于连接流的任何参数保存在同一项目中。
:::

2. 保存连接流后，它将出现在连接流列表中。

   ![连接流列表](../../../images/foundry/building-pipelines/lf-connected-flow-list.png)

3. 要触发任务，请单击与特定连接流同行的 **Build**。一条消息会指引您到 Builds 应用视图，您可以在其中监控任务的状态。

   ![Builds 应用显示 Logic flows 任务](../../../images/foundry/building-pipelines/lf-flow-run-builds.png)

4. 要检查任务的结果，请验证目标存储库视图中的拉取请求。

   ![输出存储库上的拉取请求](../../../images/foundry/building-pipelines/lf-compass-file-lister-pr.png)

5. 返回到 Logic Flows 应用，您可以看到您的连接流、其参数和配置，并从那里创建一个计划。

   ![连接流视图](../../../images/foundry/building-pipelines/lf-connected-flow-view.png)
