---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/dataexpectations-configure-health-check/",
  "title": "配置数据健康检查",
  "page_id": "dataexpectations-configure-health-check",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/dataexpectations-overview/",
  "next": "/zh/foundry/pipeline-builder/dataexpectations-unit-tests/",
  "scraped_at": "2026-07-13T05:51:36.567317+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 配置数据健康检查

你可以通过访问图中的数据预览面板或打开数据集预览应用，在Pipeline Builder中配置数据集健康检查。

* 通过双击图中的数据集节点打开预览面板。
* 右键点击数据集节点并选择**打开**以打开数据集预览应用。

在预览的**关于**选项卡中，你会发现**健康检查**部分。此部分显示为数据集配置的任何活动健康检查。选择**查看详情**以了解更多关于活动健康检查的信息或配置新的检查。这将打开数据集预览应用中的**健康**选项卡。

![显示健康检查部分的数据预览窗格截图](../../../images/foundry/pipeline-builder/health-checks@2x.png)

要添加新的健康检查，首先搜索可用的检查。使用搜索栏按名称查找检查，或使用各个选项卡根据状态、时间、大小、内容或模式来搜索检查。有关可用检查、描述和示例选项的列表，请查看[检查参考](/zh/foundry/data-health/check-groups-overview/)。

健康检查类型包括：

* **任务级状态检查：** 验证与输出数据集对应的任务是否成功完成。
* **搭建级检查：** 验证搭建是否在预期时间内成功完成。
* **新鲜度检查：** 验证数据是否保持最新。

如果你想添加一个**搭建状态**检查，例如，可以在搜索栏或**状态**选项卡中搜索**搭建状态**。选择检查以打开配置侧面板。使用此面板配置健康检查规则、组、备注和问题提示。

![健康检查搭建状态弹出窗口截图](../../../images/foundry/pipeline-builder/health-build-status@2x.png)

* **规则：** 描述你正在配置的检查规则。
  * 选择**编辑严重性**以将检查标记为**中等**或**严重**。

    ![搭建状态严重性下拉菜单截图](../../../images/foundry/pipeline-builder/health-severity@2x.png)

  * 决定是否在连续失败达到一定次数后将检查提升为关键。选择**添加时间**以设置连续失败的时间参数。

* **组：** 显示此健康检查将属于的检查组。选择**添加检查组**以搜索可用的组。
  * 了解更多关于[检查组](/zh/foundry/data-health/check-groups-overview/#checks-vs-check-groups)的信息。

* **备注：** 通过在配置中包含备注为你的新健康检查添加上下文。

* **问题：** 勾选框以在检查失败时提示创建问题。

选择配置面板右下角的**保存**以将你的新健康检查保存到数据集中。

了解更多关于推荐的[健康检查](/zh/foundry/data-integration/health-checks/)和[数据健康](/zh/foundry/data-health/overview/)的信息。
