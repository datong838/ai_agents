---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/management-file-tree/",
  "title": "Pipeline Builder 中的文件夹",
  "page_id": "management-file-tree",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/management-show-hide-nodes/",
  "next": "/zh/foundry/pipeline-builder/management-color-groups/",
  "scraped_at": "2026-07-13T05:50:19.064738+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Pipeline Builder 中的文件夹

为了高效管理大型管道，可以在 Pipeline Builder 中将节点组织到不同的文件夹和子文件夹中。仅显示文件夹或文件夹集中的节点，以便专注于管道子部分，从而改善导航和编辑体验。

## 文件夹设置

1. 要设置文件夹，请选择管道工作区左侧的 **Pipeline 文件树** 文件夹图标。

![Pipeline 文件树侧边栏。](../../../images/foundry/pipeline-builder/file-tree-side-bar.png)

2. 在侧边栏顶部，选择带加号的文件夹图标以添加新文件夹。您可以在提供的文本框中重命名文件夹。

![Pipeline Builder 中的新建文件夹按钮。](../../../images/foundry/pipeline-builder/file-tree-new-folder.png)

3. 要将节点移动到文件夹中，直接从管道文件树侧边栏中突出显示它们，或在图形上选择它们，这将自动在侧边栏中突出显示这些节点。选择并将突出显示的节点拖动到所需的文件夹中。

![选择两个节点并将其放入文件夹中。](../../../images/foundry/pipeline-builder/file-tree-move-items.png)

![从图形中选择节点，这将在侧面板中突出显示节点。](../../../images/foundry/pipeline-builder/file-tree-graph-selection.png)

4. 非必填，您可以通过将现有文件夹拖动到另一个文件夹中来创建子文件夹，或者选择父文件夹旁边的三个点并悬停在 **创建文件夹** 上。然后，您可以在提供的文本框中重命名新的子文件夹。

![使用“创建文件夹”和提供的文本框创建子文件夹。](../../../images/foundry/pipeline-builder/file-tree-sub-folder.png)

## 删除文件夹

1. 选择指定文件夹右侧的三个点。
2. 选择 **删除文件夹**。

:::callout{theme="danger"}
删除文件夹也会删除这些文件夹中的节点。
:::

![文件夹上的删除选项。](../../../images/foundry/pipeline-builder/file-tree-delete-folder.png)

## 显示和隐藏文件夹

一旦文件夹设置好后，可以通过选择指定文件夹上的眼睛图标轻松显示和隐藏节点部分。

![文件夹上的显示隐藏功能。](../../../images/foundry/pipeline-builder/file-tree-show-hide.png)

要在图形上将文件夹中的节点居中，请选择目标图标。

![将图形居中于文件夹中节点的目标图标。](../../../images/foundry/pipeline-builder/file-tree-target.png)
