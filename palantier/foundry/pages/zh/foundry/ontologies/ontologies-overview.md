---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/ontologies/ontologies-overview/",
  "title": "概述",
  "page_id": "ontologies-overview",
  "category_id": "ontology",
  "section_id": "ontologies",
  "previous": "/zh/foundry/ontology/applications/",
  "next": "/zh/foundry/ontologies/ontologies-proposals/",
  "scraped_at": "2026-07-14T04:23:37.614907+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

Ontology 是一种存储本体资源或实体的工件，包括以下内容：

* [Object 类型](/zh/foundry/object-link-types/object-types-overview/)
* [链接类型](/zh/foundry/object-link-types/link-types-overview/)
* [操作类型](/zh/foundry/action-types/overview/)
* [接口](/zh/foundry/interfaces/interface-overview/)

我们称这些资源为 **Ontology 资源**。一个 Ontology 可以是私有的并指派给单个[组织](/zh/foundry/security/orgs-and-spaces/)，也可以在多个组织之间共享。共享的 Ontology 允许不同组织的用户以安全的方式共享数据和工作流。在 Ontology 中对实体进行分组可确保只有指定组织的用户可以访问本体实体。

有权访问多个 Ontology 的用户可以通过使用位于 [Ontology 管理器](/zh/foundry/ontology-manager/overview/)左上角的选择下拉菜单在它们之间切换。当一个 Ontology 被迁移到[角色](/zh/foundry/ontology-manager/ontology-roles-migration/)后，该本体的成员将对所有本体实体具有 `Discoverer` 访问权限。

## 与空间的关系

一个 Ontology 与一个[空间](/zh/foundry/security/orgs-and-spaces/#spaces)是 1:1 映射的。当创建一个新空间时，一个具有相同名称的对应 Ontology 将同时创建，且具有与该空间相同的组织[权限标记](/zh/foundry/security/markings/)。一个私有空间将映射到一个私有 Ontology，而一个共享空间将映射到一个共享 Ontology。

在空间上被授予 `Owner` 角色的用户和群组也在对应的 Ontology 上拥有 `Ontology Owner` 角色。
