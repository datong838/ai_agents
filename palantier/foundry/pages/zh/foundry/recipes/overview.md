---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/recipes/overview/",
  "title": "Recipes",
  "page_id": "overview",
  "category_id": "data-integration",
  "section_id": "recipes",
  "previous": "/zh/foundry/preparation/faq/",
  "next": "/zh/foundry/recipes/core-concepts/",
  "scraped_at": "2026-07-13T06:06:12.962110+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Recipes

:::callout{theme="warning"}
Recipes应用程序处于稳定状态，不再更新。我们建议探索其他应用程序和功能来监控Foundry中的条件：

* [自动化:](/zh/foundry/automate/overview/) 创建在数据之上运行的自动化，跟踪个别搜索和对象，在满足特定条件时触发通知或其他操作。
* [Foundry规则:](/zh/foundry/foundry-rules/overview/) 创建基于逻辑的规则应用于数据集、对象和时间序列，在满足特定条件时触发警报。
* [大规模监控:](/zh/foundry/maintaining-pipelines/monitoring-views-intro/) 使用检查组或监控视图查看Foundry资源的指标更新，包括数据集、代理、计划、对象和链接类型。
* [Workshop:](/zh/foundry/workshop/overview/) 构建一个警报收件箱或其他通知工作流程，以配置在满足特定条件时触发的操作。

如果您对为您的监控应用案例实施适当的工作流程有疑问，请联系Palantir客服支持。
:::

Recipes使用户能够监控感兴趣的条件，通过Foundry或电子邮件自动发送通知给其他用户，并提供与感兴趣条件相关的额外上下文的预览。Recipes涵盖Foundry内的各种应用程序，包括[数据集预览](/zh/foundry/dataset-preview/overview/)和[报告](/zh/foundry/reports/overview/)。

## 应用案例示例

Recipes可以被用于在监控和应对各种情况，包括以下示例：

* 当任何产品的库存低于100时通知用户。
* 每周二上午9点发送报告或报告链接。
* 如果传感器在Quiver中达到某个阈值，向指定的一组人发送电子邮件。

## 考虑事项

Recipes旨在在数据健康时使用，以协助用户监控感兴趣的条件或项目。Recipes并非设计用于检查数据是否符合预期（就数量、质量等而言）。对于这些情况，我们建议使用[数据健康](/zh/foundry/data-health/overview/)。

Recipes绝不应被用作安全的关键警报系统。尽管Recipes在性能方面是有效的，但它并不是设计为低延迟、高依赖性的系统。Recipes应被视为一种跟踪感兴趣条件的方法，而不是用作关键警报系统。

Recipes不应作为用户通过预览和导出的唯一数据来源。它旨在当发生感兴趣的事情时作为提醒或链接回Foundry，在那里您可以看到数据的全貌。
