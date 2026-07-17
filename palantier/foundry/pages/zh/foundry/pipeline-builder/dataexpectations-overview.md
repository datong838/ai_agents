---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/dataexpectations-overview/",
  "title": "数据期望",
  "page_id": "dataexpectations-overview",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/schedules-scheduler-aip/",
  "next": "/zh/foundry/pipeline-builder/dataexpectations-configure-health-check/",
  "scraped_at": "2026-07-13T05:51:36.304768+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数据期望

数据期望是可以应用于数据集输出的要求。这些要求（称为“期望”）可用于创建检查，以提高数据管道的稳定性。

可以在每个管道输出上设置数据期望，以定义对结果输出的期望。Pipeline Builder目前支持两种数据期望：主键和行数。

![数据期望窗格截图](../../../images/foundry/pipeline-builder/output-expectations@2x.png)

如果任何期望出错，搭建将失败。任务期望窗格将显示哪些数据期望通过或失败。

## 主键数据期望

主键期望提供一个或多个列名并验证：

* 每列没有空值。
* 列的组合是唯一的。

### 主键数据期望示例

在选定的特定列中，我们检查下面的每个条目是否唯一。

如果选择了两列，我们检查两列的组合是否唯一。

在我们的示例中，我们将使用`id`和`time`作为数据集中存在的两列。

示例数据集：

| id | time |
|----|------|
| 1  | 8pm  |
| 1  | 9pm  |
| 2  | 8pm  |
| 3  | 8pm  |

上述示例将通过检查。这是因为即使`1`和`8pm`分别重复，`id`和`time`的组合仍然是唯一的。

相反，以下示例将出错：

| id | time |
|----|------|
| 1  | 8pm  |
| 2  | 9pm  |
| 1  | 8pm  |

该表将出错，因为`1`和`8pm`的组合重复。

## 行数数据期望

行数期望提供最小和/或最大行数。

如果提供了最小行数，期望将验证至少有指定数量的行。

如果提供了最大行数，期望将验证最多有此数量的行。
