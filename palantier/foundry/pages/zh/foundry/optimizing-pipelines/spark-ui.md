---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/optimizing-pipelines/spark-ui/",
  "title": "Spark UI [测试版]",
  "page_id": "spark-ui",
  "category_id": "data-integration",
  "section_id": "optimizing-pipelines",
  "previous": "/zh/foundry/optimizing-pipelines/understand-spark-details/",
  "next": "/zh/foundry/optimizing-pipelines/understand-compute/",
  "scraped_at": "2026-07-13T05:44:27.945550+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Spark UI \[测试版]

:::callout{theme="warning" title="测试版"}
在 Foundry 中查看 Spark UI 是一项测试版功能，可能不适用于所有注册。请联系 Palantir 客服支持以安装 Spark UI。目前，仅支持查看具有容器化基础设施的变换任务。
:::

Spark 具有自己的[Web UI ↗](https://spark.apache.org/docs/latest/web-ui.html)，它与 Foundry 的 [Spark 详情](/zh/foundry/optimizing-pipelines/understand-spark-details/) 页面互为补充，提供附加信息，包括：

* 执行器生命周期信息，例如执行器启动和关闭。
* 更大样本的任务和执行器指标，包括峰值内存使用情况。
* 执行期间使用的所有 Spark 配置。

## 查看 Spark UI

要查看变换任务的 Spark UI，请将任务重新运行为[调试任务](/zh/foundry/transforms-common/transforms-versions/#debug-jobs)。您将看到一个 **Spark UI** 按钮；选择此按钮将打开 Spark 的 Web UI。

<img alt="将任务重新运行为调试任务" src="../../foundry-docs/optimizing-pipelines/media/spark-ui-debug-job.png">

<img alt="Spark UI 按钮" src="../../foundry-docs/optimizing-pipelines/media/spark-ui.png">

:::callout{theme="neutral"}
Spark 事件会在延迟 1-2 分钟后出现在 Spark UI 中。
:::

## Foundry 中的 Spark UI 使用

Spark 的 Web UI 细节丰富，但没有以适合 Foundry 的方式呈现信息。以下是关于如何在 Foundry 任务中导航 Spark 的 Web UI 的建议。

### SQL 执行

Spark 可以将 SQL 查询分解为主查询和一个或多个子查询。在某些情况下，子查询比主查询更有趣。这在 Foundry 中的许多数据集写入中都是真实的。

在 Spark UI 中查看 *"写入数据集 ..."* 的 SQL 执行时，您可以在 **Sub Execution IDs** 下找到与写入相关联的查询图。

<img alt="写入数据集查询" src="../../foundry-docs/optimizing-pipelines/media/spark-ui-sql-execution.png">

<img alt="主查询 0 缺乏信息" src="../../foundry-docs/optimizing-pipelines/media/spark-ui-sql-execution-query.png">

<img alt="子查询 1 包含查询图" src="../../foundry-docs/optimizing-pipelines/media/spark-ui-sql-execution-subquery.png" height="500">

### 上下文预热

Spark UI 中的 **Jobs** 标签显示变换任务会触发一个初始 `count` 任务。`count` 任务的目的是提前请求执行器分配，同时运行时执行额外的设置（包括安装依赖项）。这增加了在变换准备运行时执行器可用的可能性。

<img alt="提前请求执行器的计数任务" src="../../foundry-docs/optimizing-pipelines/media/spark-ui-context-warmer.png" height="500">
