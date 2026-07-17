---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/data-integration/reset-stream/",
  "title": "重置流",
  "page_id": "reset-stream",
  "category_id": "data-integration",
  "section_id": null,
  "previous": "/zh/foundry/data-integration/flink-streaming/",
  "next": "/zh/foundry/data-integration/stream-monitoring/",
  "scraped_at": "2026-07-13T05:39:53.144535+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 重置流

重置导入流会清除流中的现有记录，并提供更改流的模式、吞吐量和配置值的机会。这在流管道开发过程中非常有用，因为您可以清除和更新导入流而无需替换管道构建器管道中的现有流引用。

请注意，重置仅适用于导入流。导入流的下游消费管道必须在重置后重新播放。

* [基于推送的导入](/zh/foundry/data-connection/push-based-ingestion/)需要更新POST URL以引用新的流`viewRid`值。
* [基于Magritte的导入](/zh/foundry/data-connection/set-up-streaming-sync/)需要重新搭建代理。

:::callout{theme="danger"}
重置流可能对数据产生不可逆的影响。我们不建议重置生产导入流，因为现有记录将会丢失。
:::

要重置流，请按照以下说明操作：

1. 打开一个导入流。
2. 选择 **详情** 标签。
3. 在 **关于** 部分，选择 **重置流**。

<img alt="流连接详情。" src="../../foundry-docs/data-integration/media/reset-stream-open.png">

4. 您将被重定向到流重置页面。在此页面上，您可以非必填更新模式、吞吐量或配置值。如果您只想清除流中的数据，请保持这些部分不变。

<img alt="流连接重置视图。" src="../../foundry-docs/data-integration/media/reset-stream-page.png">

5. 选择 **重置流** 以启动流重置。
