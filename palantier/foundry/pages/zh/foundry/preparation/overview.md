---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/preparation/overview/",
  "title": "准备",
  "page_id": "overview",
  "category_id": "data-integration",
  "section_id": "preparation",
  "previous": "/zh/foundry/linter/impact-tracking/",
  "next": "/zh/foundry/preparation/getting-started/",
  "scraped_at": "2026-07-13T06:05:33.944759+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 准备

:::callout{theme="warning"}
准备已被[Pipeline Builder](/zh/foundry/pipeline-builder/overview/)取代，因此不再是清理和准备数据的推荐方法。Pipeline Builder使清理和准备管道数据变得容易，同时还提供[Marketplace](/zh/foundry/marketplace/overview/)支持。
:::

准备是一个用于清理和准备数据的交互式工具。清理指的是修复数据质量问题，准备指的是操作数据以使其可用于特定的分析任务。

下方显示的数据集来自The Meteoritical Society，通过[NASA数据门户 ↗](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh)获取。

![准备清理工作流程的示例](../../../images/foundry/preparation/tutorial_namecol_fullscreen.png)

## 术语

在使用准备工具之前，了解以下术语是有益的：

* **准备：** 一个清理/准备会话

* **清理：** 修复数据集中数据质量问题

* **准备：** 使数据集适应特定用途

* **更改：** 一个单独的清理/准备步骤

* **更改日志：** 在准备过程中进行的所有更改
