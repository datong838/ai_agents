---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-integration/health-checks/",
  "title": "健康检查",
  "page_id": "health-checks",
  "category_id": "data-integration",
  "section_id": null,
  "previous": "/zh/foundry/data-integration/schedules/",
  "next": "/zh/foundry/data-integration/virtual-tables/",
  "scraped_at": "2026-07-13T05:30:15.214583+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 健康检查

一旦数据同步到Foundry，并在管道中被变换，并使用[计划](/zh/foundry/data-integration/schedules/)定期运行后，可以使用**健康检查**来验证整个管道中的数据质量。这是确保管道中流动的数据保持可靠并维持预期结构所必需的。健康检查通常用于[管道维护](/zh/foundry/maintaining-pipelines/overview/)。

在Foundry中有几种类型的健康检查：

* *任务级检查* 验证与输出数据集对应的任务是否成功完成。
* *搭建级检查* 验证搭建是否成功完成，并在预期时间内完成。
* *新鲜度检查* 验证数据是否保持最新。

要了解更多信息，请参考以下资源：

* 探索[数据健康](/zh/foundry/data-health/overview/)应用程序，学习如何定义健康检查。
* 阅读[检查参考](/zh/foundry/data-health/checks-reference/)，了解可用检查的范围。
* 了解哪些[健康检查是推荐的](/zh/foundry/maintaining-pipelines/recommended-health-checks/)。
