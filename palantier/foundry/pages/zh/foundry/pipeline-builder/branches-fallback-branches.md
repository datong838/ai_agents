---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/branches-fallback-branches/",
  "title": "回退分支",
  "page_id": "branches-fallback-branches",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/branches-protected-branches/",
  "next": "/zh/foundry/pipeline-builder/schedules-overview/",
  "scraped_at": "2026-07-13T05:51:47.221750+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 回退分支

Pipeline Builder允许您在任何分支上搭建数据集并查看逻辑对数据的影响。如果您的管道的输入数据集尚未在当前分支上搭建，Pipeline Builder会尝试从回退分支列表中定位已搭建的版本。默认分支将自动设置为回退分支，除非另有配置。您可以为每个分支设置不同的回退分支，并在需要时设置多个回退分支。

## 在Pipeline Builder中配置回退分支

要配置回退分支，请按照以下步骤操作：

1. 选择 **设置 > 管理分支**。

<img src="../../foundry-docs/pipeline-builder/media/branches-fallback-settings.png" alt="可用分支的截图。" width="350">

2. 选择 **回退分支** 选项卡，并使用右侧的双箭头图标展开您的分支。要更改回退分支配置，请在 **按顺序检查以下分支** 字段下搜索，可以直接在文本框中键入分支名称或在下面的 **拖动以重新排序** 部分中拖动以重新排序回退分支顺序。

![回退分支子选项卡的截图。](../../../images/foundry/pipeline-builder/branches-fallback-branches-collapsed.png)

![回退分支配置更改的截图。](../../../images/foundry/pipeline-builder/branches-fallback-branches-expanded.png)

3. 完成分支回退配置后，选择 **保存**。

如果您的分支未在 **回退分支** 选项卡下列出，请在弹出窗口的右下角使用 **添加新配置**。要删除分支的回退配置，请选择分支右侧的回收站图标。
