---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/management-input-sampling/",
  "title": "添加输入采样策略",
  "page_id": "management-input-sampling",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/management-overview/",
  "next": "/zh/foundry/pipeline-builder/management-parameter-overview/",
  "scraped_at": "2026-07-13T05:49:30.539009+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 添加输入采样策略

如果您的输入数据集较大，可以通过为这些输入添加采样策略来加快预览时间。

1. 右键单击您想要采样的输入节点，然后在下拉菜单中选择**采样策略**。

<img src="../../foundry-docs/pipeline-builder/media/management-sampling-entry-point.png" alt="带有采样策略选项的下拉菜单。" width="400">

2. 在采样策略对话框中，选择所需的输入数据集。

<img src="../../foundry-docs/pipeline-builder/media/management-sampling-dialog.png" alt="采样策略对话框。" width="800">

3. 选择**百分比**策略，并输入1到100之间的数字以对输入进行下采样。

<img src="../../foundry-docs/pipeline-builder/media/management-sampling-percentage.png" alt="采样策略对话框配置为使用20%的策略。" width="800">

4. 关闭对话框。现在应该在输入节点的右上方出现一个蓝色标记，表示已应用采样策略。

<img src="../../foundry-docs/pipeline-builder/media/management-sampling-badge.png" alt="显示采样策略指示器的输入节点。" width="400">

输入节点下游的任何节点的预览面板也将指示已应用采样。

<img src="../../foundry-docs/pipeline-builder/media/management-sampling-downstream.png" alt="采样策略应用于下游输入。" width="800">
