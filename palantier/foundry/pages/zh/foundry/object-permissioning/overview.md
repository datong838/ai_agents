---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/object-permissioning/overview/",
  "title": "概述",
  "page_id": "overview",
  "category_id": "ontology",
  "section_id": "object-permissioning",
  "previous": "/zh/foundry/object-backend/aggregation-considerations/",
  "next": "/zh/foundry/object-permissioning/managing-object-security/",
  "scraped_at": "2026-07-14T05:08:13.093224+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 概述

Foundry Ontology允许对所有Ontology实体进行细粒度、强大且灵活的安全控制。这些实体包括Ontology元数据，如[Object类型](/zh/foundry/object-link-types/object-types-overview/)、[链接类型](/zh/foundry/object-link-types/link-types-overview/)和[操作类型](/zh/foundry/action-types/overview/)，以及如Objects和链接（元数据的实例化）这样的Ontology数据。

我们可以将Ontology的授权结构概念化为元数据和数据这两个层次。本节文档的剩余部分解释了构成Ontology数据的授权和权限系统的不同机制。

## Ontology元数据

Ontology元数据指的是关于Ontology实体的类型级信息，如Object类型、链接类型和操作类型。例如，Object类型的元数据可能包括显示名称、属性名称、属性数据类型和描述。元数据不指Object类型属性或主键的实际数据或值；这些被视为Ontology数据。

[了解更多关于Ontology元数据权限的信息。](/zh/foundry/ontologies/ontology-permissions/)

## Ontology数据

Ontology数据是Ontology实体特定实例的实际主键和属性值。例如，Airplane Object类型可以有一个Object实例，其中`Plane ID`属性的值为`my_plane_id1`，`Maximum Occupancy`属性的值为`240`。

[了解更多关于Ontology数据权限的信息。](/zh/foundry/object-permissioning/managing-object-security/)
