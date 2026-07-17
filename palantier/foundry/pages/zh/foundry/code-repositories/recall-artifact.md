---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/code-repositories/recall-artifact/",
  "title": "召回制品",
  "page_id": "recall-artifact",
  "category_id": "data-integration",
  "section_id": "code-repositories",
  "previous": "/zh/foundry/code-repositories/publish-artifact/",
  "next": "/zh/foundry/code-repositories/manage-permissions/",
  "scraped_at": "2026-07-13T06:01:02.181361+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 召回制品

可以召回 Conda 制品以阻止下游消费者使用被召回的版本编译代码。我们建议在开始召回流程之前，为被召回的制品提供补丁版本。

按照以下步骤召回制品：

1. 在您的制品库中[搜索](/zh/foundry/code-repositories/artifact-repositories-nav/) Conda 制品，并选择它以在摘要页面中查看版本历史部分。

2. 选择要召回的版本，然后点击 **召回**。

   ![选择版本并点击召回](../../../images/foundry/code-repositories/ar-recall-select.png)

3. 会出现一个**召回制品**的弹出窗口。在字段中输入召回制品的原因。

    <img src="../../foundry-docs/code-repositories/media/ar-recall-reason.png" alt ="输入召回原因" width="300">

4. 再次查看版本历史，以查看制品现在已被标记为 `Recalled`。

   ![版本被标记为已召回。](../../../images/foundry/code-repositories/ar-recall-overview.png)

## 取消召回

您可以取消召回制品。

要取消召回制品，选择被召回制品的版本并点击 **取消召回**。

![取消召回](../../../images/foundry/code-repositories/ar-unrecall.png)

## 删除

Conda 制品可以被召回，但无法删除制品库中的任何制品。如果您明确需要删除制品，您必须[删除制品库](/zh/foundry/code-repositories/delete-artifact-repository/)。
