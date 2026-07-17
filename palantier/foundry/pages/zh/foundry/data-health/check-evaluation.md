---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-health/check-evaluation/",
  "title": "检查计划",
  "page_id": "check-evaluation",
  "category_id": "data-integration",
  "section_id": "data-health",
  "previous": "/zh/foundry/data-health/check-types/",
  "next": "/zh/foundry/data-health/watching-checks/",
  "scraped_at": "2026-07-13T06:04:11.236206+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 检查计划

基于时间的检查可以配置为自动评估或手动计划评估。

## 自动

当配置为自动运行时，检查会在以下两种情况下运行：

1. 当数据集更新时。
2. 当数据集超过您配置的阈值时。

数据集更新事务会触发检查，评估i)基于配置的检查的数据集和ii)当前时间与先前提交的事务之间的经过时间。它还会通过将时间阈值最小值添加到当前时间来重置下一个检查的阈值。

例如，假设您将[自上次更新检查的时间](/zh/foundry/data-health/checks-reference/#time-since-last-updated)阈值设置为少于1小时（“当自上次更新的时间少于或等于1小时时，此检查通过”）。

![一小时检查](/resources/foundry/data-health/one-hour-check.png)

### 检查通过

假设您的数据集在58分钟内更新。此时，检查将运行，产生“通过”结果，因为自上次事务以来不到60分钟。更新事务还导致下一个检查的阈值重置 - 它现在将自动在60分钟后再次运行，以评估数据集是否已更新。

只要数据集在不到60分钟内继续更新，检查将在数据集更新时继续通过，并且永远不会达到您配置的阈值。

### 检查失败

这次，假设您的数据集在62分钟内更新。在自上次更新以来的60分钟时，会运行一个检查（由一小时阈值设置），并且失败，因为自上次事务以来已经超过60分钟。当数据集在62分钟时更新，检查将再次运行，将自上次更新以来的时间值更新为当前时间，并且检查将通过。任何[监测者](/zh/foundry/data-health/watching-checks/)都会收到通知。

## 手动计划

手动计划会在定期间隔内运行检查，而不管数据集何时构建。它可以设置为按分钟、每小时、每天、每周或自定义计划运行。

![手动检查](/resources/foundry/data-health/Manual-checks.png)
