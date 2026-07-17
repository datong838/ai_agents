---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/action-types/action-metrics/",
  "title": "操作指标 [测试版]",
  "page_id": "action-metrics",
  "category_id": "ontology",
  "section_id": "action-types",
  "previous": "/zh/foundry/action-types/action-reverts/",
  "next": "/zh/foundry/action-types/action-log/",
  "scraped_at": "2026-07-14T04:28:46.202216+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 操作指标 \[测试版]

:::callout{theme="warning" title="测试版"}
操作指标功能处于测试版阶段；操作类型失败的分类仍在积极开发中。
:::

[Ontology Manager](/zh/foundry/ontology-manager/overview/) 中的操作指标显示操作类型在操作类型概览页面上的使用情况。

![概览部分的操作指标截图。](/resources/foundry/action-types/action-metrics.png)

操作指标不需要显示操作日志。与操作日志不同，操作指标跟踪失败。

操作指标具有各种不同类别的失败情况，这些类别包括：

* **无效参数失败：** 操作提交时包含在操作上下文中无效的参数。
* **规模限制失败：** 操作影响的Object类型超过了允许的限制（默认情况下，通常为10,000）。
* **认证失败：** 用户未通过操作的安全提交标准。
* **副作用失败：** 操作由于webhook或配置错误的副作用而失败。
* **函数失败：** 操作失败是因为底层函数失败。这种失败模式仅适用于由函数支持的操作。
* **未分类失败：** 操作失败不属于上述任何类别。
