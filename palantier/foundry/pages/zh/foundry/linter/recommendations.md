---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/linter/recommendations/",
  "title": "建议",
  "page_id": "recommendations",
  "category_id": "data-integration",
  "section_id": "linter",
  "previous": "/zh/foundry/linter/modes/",
  "next": "/zh/foundry/linter/rules/",
  "scraped_at": "2026-07-13T06:05:00.195351+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 建议

在Linter中，一个建议代表了一项可以采取的操作，以将一个或多个资源从检测到的、可能次优的状态迁移到更理想的状态。一旦Linter在给定范围内运行一轮规则，就会生成建议。

Linter建议包含一个Foundry资源，您查看建议的能力继承自您查看其基础资源的权限。一个建议可以属于一个或多个项目，并且对于某些模式，可能包含遵循其建议操作的影响估计。

一旦用户对建议进行操作，必须再次进行Linter扫描以确认规则标准，并将建议从视图中移除。

## 筛选到建议

使用左侧边栏缩小显示建议的范围，以更好地搜索特定资源、规则、影响级别或项目。

![应用筛选搜索建议时可用的筛选列表。](../../../images/foundry/linter/filter.png)

## 建议上下文

使用右侧边栏提取建议上下文，了解其出现的原因、当前状态的潜在影响，以及将资源移动到更理想状态所需的操作。

## 建议状态

建议可以处于三种状态之一，并可以根据用户互动进行更改：

* **默认：** 在Linter扫描后未进行操作的建议处于默认状态。除非被搁置或在另一次扫描后从视图中移除，否则将保持此状态。
* **搁置：** 如果您在某个时间无法采取行动，可以选择搁置建议。查看[下面的部分](#snooze-a-recommendation)了解更多信息。
* **搁置过期：** 先前搁置的建议将在搁置时间框架结束后进入搁置过期状态。

### 搁置建议

如果您无法立即对一个或多个建议采取行动，可以选择搁置它们，以避免反复看到它们。使用操作栏为选定的建议设置搁置，输入搁置原因，并提供搁置过期的时间。在那个时间之后，建议将不再处于搁置状态。

![操作栏显示了用于设置建议搁置的可用时间菜单。](../../../images/foundry/linter/snooze.png)

搁置的建议以橙色圆点和搁置警报符号表示。您可以从操作栏选择取消搁置建议。

![搁置的建议，以橙色圆点和搁置警报符号表示。](../../../images/foundry/linter/snoozed-recommendation.png)
