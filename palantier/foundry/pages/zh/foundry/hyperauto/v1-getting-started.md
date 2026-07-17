---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/hyperauto/v1-getting-started/",
  "title": "开始使用 HyperAuto V1",
  "page_id": "v1-getting-started",
  "category_id": "data-integration",
  "section_id": "hyperauto",
  "previous": "/zh/foundry/hyperauto/v1-overview/",
  "next": "/zh/foundry/hyperauto/v1-source-exploration/",
  "scraped_at": "2026-07-13T05:33:38.302522+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 开始使用 HyperAuto V1

:::callout{theme="neutral"}
本文档适用于 HyperAuto V1。如果您使用的是 HyperAuto V2，请参阅[HyperAuto V2 入门文档](/zh/foundry/hyperauto/getting-started/)。
:::

以下步骤指导创建一个 SDDI 实例：

1. 从[侧边栏](/zh/foundry/getting-started/orientation-and-nav/#the-sidebar)或在 `[foundryinstance URL]/workspace/sddi-app` 打开 SDDI Cockpit，并选择 **创建新实例**。

   <img src="../../foundry-docs/hyperauto/media/v1-sddi-initial-set-up.png" alt="初始设置创建新实例" width="400" />

2. 按照屏幕上的说明选择适当的源类型。

3. 输入您首选的存储库名称，并选择所需的存储库位置以及管道输出文件夹位置。对于管道输出文件夹，HyperAuto 提供了建议的位置。

   <img src="../../foundry-docs/hyperauto/media/v1-sddi-initial-set-up-new-repo-for-non-sap-sources.png" alt="为非SAP源初始设置新存储库" width="500" />

4. 配置您希望应用 HyperAuto 的数据连接源。此源应具有与您在步骤 1 中选择的相同源类型。分别确定原始数据和元数据的文件夹位置。这些文件夹将随后存放从源同步的原始数据和元数据集。

   <img src="../../foundry-docs/hyperauto/media/v1-sddi-initial-set-up-source-configuration-for-non-sap-sources.png" alt="为非SAP源初始设置源配置" width="500" />

5. 在“同步数据”步骤中同步数据库元数据表。这将从您的源系统同步相关的元数据表，并将其添加到指定的自动管道生成器存储库中，以在后台生成管道。

   <img src="../../foundry-docs/hyperauto/media/v1-sddi-metadata-ingestion.png" alt="元数据摄取" width="500" />

您的 SDDI 实例现在应该可以正常运行，并准备从您的源中清理表格。要了解有关配置和执行 SDDI 流的更多信息，请导航到[Cockpit](/zh/foundry/hyperauto/v1-cockpit/)。
