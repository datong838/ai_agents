---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/linter/impact-tracking/",
  "title": "影响跟踪",
  "page_id": "impact-tracking",
  "category_id": "data-integration",
  "section_id": "linter",
  "previous": "/zh/foundry/linter/sweep-schedules/",
  "next": "/zh/foundry/preparation/overview/",
  "scraped_at": "2026-07-13T06:05:54.442812+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 影响跟踪

Linter影响跟踪界面允许您跟踪已执行的建议和节省估算的进展。您可以通过在Linter主页上选择**影响跟踪**来进入影响跟踪页面。您可以使用筛选器查看选定时间范围、规则和项目的指标。

![Linter影响跟踪截图，显示已执行的建议。](../../../images/foundry/linter/linter-impact-tracking-screenshot.png)

在影响跟踪中显示三个指标：

* **建议计数：** 显示已解决的建议数量。当用户首次从建议表中选择一个建议时，它会转为`调查中`状态，并拍摄当前建议的快照。用户未选择的建议将处于`开放`状态，并在下一次扫描中消失。这些建议不被跟踪，也不会出现在影响跟踪中。
* **预估影响：** 显示Linter在执行建议之前预测的计算小时减少量。此估算值被标准化为三十天，并与建议表中的每月预估节省数字相同。
* **验证影响：** 显示建议执行前后预估每月使用量的差异。Linter通过获取修复前一周的使用量，减去修复后一周的使用量，并将差异标准化为30天的使用量来构建验证估算。请注意，修复前后的一周不保证能代表建议影响的资源使用情况。

验证通常需要七天，因此操作的验证影响不会立即在影响跟踪页面上显示。所有节省估算均基于API提供的可见性和访问权限计算。这意味着由于规则间的共享资源，Linter估算中可能会出现资源的重复计算，例如，一个[计划可能未使用](/zh/foundry/linter/rules/#schedule-potentially-unused)规则可以覆盖一个数据集，而该数据集也可能被一个[增量追加数据集分区不良](/zh/foundry/linter/rules/#incremental-append-dataset-poorly-partitioned)规则提及。用户在汇总建议数字时应考虑这一点。

## 影响指标之间的差异

预估影响和验证影响是使用[资源管理](/zh/foundry/resource-management/overview/)进行的估算。这两个指标之间的估算方法差异在于，如果用户在Linter建议后迅速采取行动，预估节省将高于验证节省。

例如，假设在第一天创建了一个`计划可能未使用`的建议：

1. 您在警报创建后一天，即第二天暂停了计划。
2. 验证影响估算将修复后七天的使用量（正常使用）减去修复前七天的使用量（六天的正常使用和一天的高使用）。
3. 差异被标准化为三十天。
4. 预估影响将明显高于验证影响，因为预估影响是基于如果问题持续运行一个月再修复一个月的节省。
