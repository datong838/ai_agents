---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/action-types/action-reverts/",
  "title": "撤销或取消操作",
  "page_id": "action-reverts",
  "category_id": "ontology",
  "section_id": "action-types",
  "previous": "/zh/foundry/action-types/permissions/",
  "next": "/zh/foundry/action-types/action-metrics/",
  "scraped_at": "2026-07-14T04:28:49.746946+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 撤销或取消操作

在 [Ontology Manager](/zh/foundry/ontology-manager/overview/) 中，操作撤销允许在操作应用后立即撤销（即取消）操作。您可以通过在任何成功操作应用后的成功消息中选择 **撤销** 来撤销操作。

新的操作默认是可以撤销的。

:::callout{theme="neutral"}
操作撤销仅适用于 Object Storage V2；这意味着只有在 [OSv2](/zh/foundry/object-backend/object-storage-v2-breaking-changes/) 中修改或创建对象类型的操作才能被撤销。如果您的对象类型目前未存储在 Object Storage V2 中，您可以按照此 [指南](/zh/foundry/object-backend/osv1-osv2-migration/#migrate-from-object-storage-v1-phonograph-to-object-storage-v2) 进行迁移。
:::

## 配置可撤销的操作

目前，操作只能由应用操作的用户撤销。

在操作的 **表单** 选项卡中，打开 **在操作提交后允许撤销** 按钮。一旦该切换正确配置并保存到 Ontology 中，您的操作就可以被撤销。

![操作撤销在表单部分的屏幕截图](../../../images/foundry/action-types/action-reverts-form-button.png)

对于2024年5月之后创建且仅修改OSv2对象类型的操作，**表单** 选项卡中的 **在操作提交后允许撤销** 切换将默认启用。
如果一个操作在2024年5月之前存在并修改了OSv2中的对象类型，则操作撤销不会默认开启，但可以手动启用。

如果一个操作仅修改了OSv1对象类型，您将无法撤销该操作。

## 撤销操作

:::callout{theme="warn" title="撤销操作"}
下面的提示是您撤销操作的唯一机会。这在执行删除操作时尤其重要。
:::

一旦成功撤销，用户将看到类似于原始操作成功的提示，如下所示。

应用的编辑：

![提示通知：编辑成功撤销。](../../../images/foundry/action-types/action-reverts-revert-action.png)

已撤销的编辑：

![提示通知：编辑成功应用。](../../../images/foundry/action-types/action-reverts-edits-reverted.png)

## 注意事项

在某些情况下，操作撤销可能失败：

* 一旦对对象进行了任何后续编辑，某个对象上的操作就无法被撤销，即使该编辑是针对不同的属性。换句话说，只有当操作是对象的最新编辑时，才能撤销该操作。
* 如果在操作提交后操作撤销被关闭，即使之后再次开启，也无法撤销该操作。

操作撤销仅撤销对象实例的编辑，但不会撤销副作用，如通知或webhooks，也不会像应用操作那样调用它们。

### 在没有撤销操作提示的情况下撤销删除操作

如果执行了删除操作并且您希望撤销删除，但撤销操作提示不再可用，唯一的补救选项是：

* 迁移到新的对象类型并使用函数复制所需的编辑；或
* 删除对象类型上的所有编辑。
