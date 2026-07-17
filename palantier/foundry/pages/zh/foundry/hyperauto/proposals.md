---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/hyperauto/proposals/",
  "title": "提案",
  "page_id": "proposals",
  "category_id": "data-integration",
  "section_id": "hyperauto",
  "previous": "/zh/foundry/hyperauto/getting-started/",
  "next": "/zh/foundry/hyperauto/configuration-options/",
  "scraped_at": "2026-07-13T05:33:20.272073+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 提案

要对HyperAuto管道进行编辑，用户需要创建一个提案。在HyperAuto管道上一次只能存在一个提案，并代表该管道所拥有的资源和变换逻辑的分阶段再生成。

用户必须决定是批准并应用提案还是丢弃它。

## 创建提案

要创建提案，请打开现有HyperAuto管道的**配置**标签并选择**编辑**。

![配置标签](../../../images/foundry/hyperauto/hyperauto-v2-overview-input-config.png)

在编辑模式下，可以在一次编辑中更新输入配置（添加或移除作为输入的源表）和管道配置。

![编辑模式](../../../images/foundry/hyperauto/hyperauto-v2-overview-input-config-edit-mode.png)

一旦对更改感到满意，选择**创建提案**以获得一个准备好供您评估和批准的提案，并已链接。

![待处理提案](../../../images/foundry/hyperauto/hyperauto-v2-overview-pending-proposal.png)

## 查看提案

从概览页面选择**查看提案**，以在Pipeline Builder中打开提案。这是您可以合并或关闭提案的页面。采取的操作将反映在相应的HyperAuto管道页面上。

![构建器提案](../../../images/foundry/hyperauto/hyperauto-v2-builder-proposal.png)

要查看提案生成的管道逻辑更改，请选择**更改**标签。

![更改](../../../images/foundry/hyperauto/hyperauto-v2-builder-proposal-changes.png)

在审查更改后，选择**合并提案**将更改提交到管道的主分支。确保在合并提案后选择**部署分支"Main"**。这将确保管道被部署，更改体现在输出数据集和Ontology中。
