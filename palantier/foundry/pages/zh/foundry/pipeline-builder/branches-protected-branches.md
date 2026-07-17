---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/branches-protected-branches/",
  "title": "分支保护",
  "page_id": "branches-protected-branches",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/branches-approve-a-change/",
  "next": "/zh/foundry/pipeline-builder/branches-fallback-branches/",
  "scraped_at": "2026-07-13T05:50:53.812096+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 分支保护

当有多个作者对同一Pipeline Builder实例进行贡献，或当该管道支持关键数据资产时，可以*保护*您的分支，以实现更高水平的治理和防范无意的更改。一个*受保护的分支*只能通过拉取请求进行修改，并且必须满足一组预定义的要求。

## 如何保护分支

导航到左上角的**设置**下拉菜单。选择**管理分支**。

![设置下拉菜单的截图。](../../../images/foundry/pipeline-builder/branches-settings.png)

选择**分支保护**选项卡。在此选项卡中，启用**需要提案...**以保护主分支和在下面文本框中指定的任何其他分支。完成后选择**保存**。

![配置多个受保护分支的位置的截图。](../../../images/foundry/pipeline-builder/branches-multiple-protected.png)

所有受保护的分支要求用户在单独的分支上更改，然后这些更改才能合并到受保护的分支中。目前，Pipeline Builder中的所有受保护分支共享相同的审批规则。
