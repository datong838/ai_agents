---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-health/watching-checks/",
  "title": "监测检查",
  "page_id": "watching-checks",
  "category_id": "data-integration",
  "section_id": "data-health",
  "previous": "/zh/foundry/data-health/check-evaluation/",
  "next": "/zh/foundry/data-health/notifications/",
  "scraped_at": "2026-07-13T06:04:12.073115+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 监测检查

:::callout{theme="success" title="提示"}
与其监测单个检查，创建并监测一个[检查组](/zh/foundry/data-health/create-watch-check-group/)可能更有帮助。
:::

您可以**监测**检查以在它们失败时收到警报。您可以通过展开检查并点击**监测**按钮来监测单个检查：

![监测单个检查](/resources/foundry/data-health/watching-individual-checks.png)

根据检查的[**规则部分**](/zh/foundry/data-health/checks-reference/)中的配置：

* **无通知**将永远不会通知您失败情况，无论严重程度如何。
* **所有失败**将通知您任何失败（包括`中等`和`严重`）。
* **仅严重**将*仅*通知您任何`严重`失败。

:::callout{theme="neutral"}
我们建议为中等和严重检查设置不同的阈值。理想情况下，严重警报应具有更宽松的界限（例如，如果搭建持续5分钟则中等失败，如果持续10分钟则严重失败）。
:::

## 监测数据集上的所有检查

您还可以通过使用**监测所有**按钮对数据集上的所有检查进行上述任何操作：

![监测所有检查](/resources/foundry/data-health/watching-all-checks.png)

## 暂停和删除检查

您还可以通过展开检查并点击**更多**按钮来暂停或删除检查。

* **暂停**检查将暂时使其对所有监测/订阅用户的警报静音。
* **删除**检查将永久删除其配置和计划，如果您想监测它，则需要重新创建。
