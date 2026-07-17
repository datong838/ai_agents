---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/action-types/permissions/",
  "title": "权限",
  "page_id": "permissions",
  "category_id": "ontology",
  "section_id": "action-types",
  "previous": "/zh/foundry/action-types/inline-edits/",
  "next": "/zh/foundry/action-types/action-reverts/",
  "scraped_at": "2026-07-14T04:28:45.318999+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 权限

权限以以下方式应用于操作类型：

* 谁可以查看给定的操作类型？
* 谁可以编辑给定的操作类型？
* 谁可以应用具有给定参数集的操作类型？

:::callout{theme="warning" title="警告"}
操作类型的授权模型正在从[旧版权限](/zh/foundry/ontologies/ontology-permissions/#datasource-derived-permissions-legacy)更改为[Ontology角色](/zh/foundry/ontologies/ontology-permissions/#ontology-roles)。[迁移到Ontology角色的文档](/zh/foundry/ontology-manager/ontology-roles-migration/)提供了有关如何进行迁移的分步指南。
:::

## 应用操作

应用操作类型的能力取决于它所编辑的object类型和链接类型的配置。在所有情况下，提交操作的用户必须能够查看被编辑的object类型和链接类型及其数据源，并通过[提交标准](/zh/foundry/action-types/submission-criteria/)。如果object类型仅允许通过操作进行编辑，用户可以对他们可以查看的所有object进行编辑。对于允许超出操作编辑的object类型和链接类型，如果object类型或链接类型由数据集支持，用户还需要对数据输出数据集进行编辑权限。如果object类型或链接类型由[受限视图](/zh/foundry/security/restricted-views/)支持，用户需要通过编辑策略。

:::callout{theme="neutral"}
侧边栏中的**检查访问**面板可用于检查某人对Workshop模块的访问权限，包括对依赖的操作类型及其提交标准的访问。有关更多信息，请参阅[检查访问面板文档](/zh/foundry/security/checking-permissions/)。
:::

### 提交标准

操作提交标准允许对谁可以运行操作进行细粒度控制。简单的提交标准可以要求特定的用户ID或组ID，并可以与参数信息结合使用。有关更多信息，请参阅[提交标准文档](/zh/foundry/action-types/submission-criteria/)。

### Object编辑权限

Object编辑可以被锁定，使得仅允许通过操作进行编辑，或重新开放，使得允许通过操作、Foundry Forms、直接Object Explorer编辑和API调用进行编辑。为了在许多工作流程中实施一致的安全范式，默认情况下，新的object类型仅允许通过操作进行编辑。不推荐新使用其他形式的编辑。

对于仅允许通过操作进行编辑的object类型，提交操作的用户只需要对正在编辑的object具有`读取`权限。这意味着用户可以创建他们无法查看的object。

相反，当由数据集支持的object类型可以通过操作、Foundry Forms、直接Object Explorer编辑和API调用进行编辑时，提交操作的用户必须对所有正在编辑的object的数据输出数据集具有`编辑`权限。具有`编辑`权限的用户将能够查看数据输出数据集中的所有数据。

因此，设置一个object类型通过操作、Foundry Forms、直接Object Explorer编辑和API调用进行编辑是不鼓励的，因为仅为了object编辑而授予`编辑`权限可能会向用户暴露比完成Ontology编辑工作流程所需更多的数据。

无论使用哪种数据输出设置，操作类型的配置都不会显示受影响的底层object类型的权限设置；配置操作类型的人必须确保这些权限是正确的。

将object类型的编辑权限更新为"仅允许通过操作进行编辑"不会删除历史的非操作编辑，但将阻止进一步通过Foundry Forms、直接Object Explorer编辑和API调用的编辑。

![推荐仅允许通过操作进行编辑。](/resources/foundry/action-types/recommended_writeback_setting.png)

[了解更多关于数据输出权限的信息。](/zh/foundry/object-permissioning/configuring-rv-access-controls/)

## 副作用权限

任何可以设置操作的用户都可以配置副作用。

* Webhook副作用默认未启用。需要额外的权限才能在数据连接应用中配置Webhook插件，然后才能在操作设置页面中使用。如果有任何关于在您的Foundry实例上使用Webhook的问题，请联系您的Palantir代表。

提交标准必须正常通过；如果操作提交标准失败，则副作用不会被触发。

接收者必须能够访问通知中包含的任何object数据。

* 如果用户无权访问通知内容中包含的所有数据，则通知将不会发送给他们。
* 如果有多个接收者，并且有些接收者缺少正确的权限数据，则只有拥有足够权限的用户会收到通知。
* 如果通知由于任何原因发送失败，编辑可能仍会成功。

执行操作的用户必须能够查看将收到通知的用户和/或组。
