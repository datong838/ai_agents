---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/transforms-pattern-mining/",
  "title": "频繁模式挖掘",
  "page_id": "transforms-pattern-mining",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/pipeline-builder-llm/",
  "next": "/zh/foundry/pipeline-builder/outputs-overview/",
  "scraped_at": "2026-07-13T05:46:41.373371+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 频繁模式挖掘

Pipeline Builder 通过在变换中使用频繁模式增长（FP-Growth）算法的强大功能简化了频繁模式挖掘的过程。该算法使您能够轻松构建和管理挖掘工作流，并在大型数据集中发现有价值和频繁的模式。

频繁模式挖掘是一种数据挖掘技术，用于识别大型数据集中重复出现的模式或关联。频繁模式挖掘的主要目标是发现一起出现的项目或事件之间的关系，这些关系比偶然出现的频率更高。这些模式通常被称为频繁项集，可以帮助揭示数据中的隐藏关联和依赖关系，从而促进更好的决策和预测。

频繁模式挖掘可以在多个领域中应用，包括市场篮分析、推荐系统、生物信息学、网络流量分析、客户属性分析、可解释AI（XAI）等。通过识别频繁模式，组织可以获得宝贵的见解，提升他们的策略，并提高整体效率。

## 频繁模式挖掘示例：市场篮分析

频繁模式挖掘在零售中的一个常见应用称为“市场篮分析”。使用 Pipeline Builder 频繁模式增长变换，您可以识别在同一交易中频繁出现的产品组合。

例如，超市可能拥有其客户过去购买（交易）的数据集。每笔交易包含一组一起购买的产品。以下是该类交易的简化示例数据集：

| transaction\_id | products\_purchased |
| ----- | ----- |
| 1 | \[面包, 黄油, 牛奶] |
| 2 | \[面包, 黄油] |
| 3 | \[面包, 尿布, 啤酒] |
| 4 | \[牛奶, 尿布, 啤酒, 黄油] |
| 5 | \[面包, 黄油, 尿布] |

频繁模式增长变换将 `Items column` 和 `Minimum support` 值作为输入。在此示例中，`products_purchased` 列是项目列。由于输出中只会包含频繁模式，因此将 `Minimum support` 设置为0.6；变换将仅返回至少在60%交易中出现的模式。以下截图显示如何为此示例配置变换：

![使用 Pipeline Builder 变换表配置频繁模式增长变换。](../../../images/foundry/pipeline-builder/transforms-pattern-mining-configuration.png)

变换的输出数据集如下：

| pattern | pattern\_occurence | total\_count |
| ----- | ----- | ----- |
| \[面包] | 4 | 5 |
| \[黄油] | 4 | 5 |
| \[面包, 黄油] | 3 | 5 |
| \[尿布] | 3 | 5 |

在这种情况下，频繁模式挖掘揭示了`面包`和`黄油`经常一起出现在交易中（它们是一个频繁项集，在五笔交易中出现了三次）。这些信息可以用于推动各种业务策略，例如产品摆放（将面包和黄油放在一起以增加销售）或促销活动（购买面包时黄油打折，反之亦然）。

以上是一个简化的示例，展示了真实应用案例中发现的大型且更复杂的数据集；使用像 FP-Growth 这样的高效算法对于有效的频繁模式挖掘至关重要。
