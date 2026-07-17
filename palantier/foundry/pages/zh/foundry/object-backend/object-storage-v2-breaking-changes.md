---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/object-backend/object-storage-v2-breaking-changes/",
  "title": "Object Storage V1与Object Storage V2之间的重大变更",
  "page_id": "object-storage-v2-breaking-changes",
  "category_id": "ontology",
  "section_id": "object-backend",
  "previous": "/zh/foundry/object-backend/overview/",
  "next": "/zh/foundry/object-backend/osv1-osv2-migration/",
  "scraped_at": "2026-07-14T05:07:12.457714+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Object Storage V1与Object Storage V2之间的重大变更

从Object Storage V1（Phonograph）到Object Storage V2的过渡是一个重大的架构转变，需要进行许多重大变更。传统的Object Storage V1（Phonograph）具有广泛的API表面，直接暴露了大量底层数据库功能。相反，全新的Object Storage V2架构通过Object Data Funnel服务将对象同步到专用的对象数据库中，以获得规模、性能、灵活性和安全性的改进。此架构转变导致了两种主要类型的重大变更：

* 专用的对象数据库被设计用于特定的应用案例，可能无法提供与Object Storage V1相同的功能。这可能需要在OSv2中以不同于OSv1的方式建模工作流。
* 分离在Object Storage V1中整合的[关注维度](/zh/foundry/object-backend/overview/#object-storage-v2-architecture)需要对一些直接与OSv1 API交互的现有查询进行重构。

这些重大变更可能会阻止某些基于OSv1的对象类型在不进行重构或补救的情况下迁移到OSv2。有关这些问题如何向用户展示以及如何从OSv1迁移到OSv2的更多信息，请参阅[迁移到OSv2](/zh/foundry/object-backend/osv1-osv2-migration/)文档。

## 永久性重大变更

本节提供了Object Storage V1（Phonograph）与Object Storage V2之间的重大变更列表。在尝试将任何对象类型迁移到OSv2之前，应解决这些重大变更。这些OSv1和OSv2之间的变更旨在提高进入Ontology的数据质量，确保行为更具确定性，并提高平台的可读性。

* OSv2仅支持通过操作进行用户编辑。必须重构所有现有的OSv1编辑API上的直接查询以使用操作，然后才能迁移到OSv2。
* OSv2将"数据输出数据集"重命名为"物化"。在OSv1中，数据输出数据集是必需的；在OSv2中，物化是非必填的。有关物化数据集的更多详细信息，请参阅[物化](/zh/foundry/object-edits/materializations/)。
* 无法从OSv1迁移对象类型到OSv2并保留用户的OSv1编辑历史。
  * 之前的OSv1编辑将保留，但OSv1的编辑历史在OSv2中不可用。
  * 需要在Ontology Manager中为OSv2中的对象类型启用[**跟踪用户编辑历史**](/zh/foundry/object-edits/user-edit-history/)，并需要更新对象视图以添加[编辑历史微件](/zh/foundry/object-views/widgets-properties-links/#edits-history)以显示用户编辑历史。
  * 用户还可以配置[操作日志](/zh/foundry/action-types/action-log/)对象类型，以捕获操作如何影响对象；另请参阅[操作日志时间线微件](/zh/foundry/action-types/action-log/#action-log-timeline)以显示目标对象的操作历史。
* OSv2对数据源的对象主键实施唯一性约束。如果数据源中存在重复的主键，则将数据源索引到Ontology中将失败并抛出错误。
* OSv2阻止某些数据类型用作主键，以鼓励Ontology建模的最佳实践。以下类型**不能**用作主键：
  * Geohash
  * Geoshapes
  * 数组
  * 时间序列属性
  * 实数类型（十进制、双精度、浮点）
* OSv2在每次同步时强制数据源模式和对象类型模式之间的数据类型一致性。不兼容的数据类型将导致搭建失败。
* OSv2不允许嵌套数组。
* OSv2不允许将NaN或±无穷大作为属性值。
* 对于具有更改日志数据源的对象类型，OSv2不考虑[传统更改日志数据集](/zh/foundry/building-pipelines/maintaining-incremental-performance/#changelog-datasets)使用的“最新时间戳优先”语义。
  * OSv2默认增量索引所有管道；Funnel在后台自动执行所有相关的更改日志计算，使"更改日志python装饰器"过时。
* OSv2对Geohash属性有更严格的验证。
  * OSv2中不允许空字符串；在OSv1中，空字符串被默默地转换为null。
  * `Lat, Long`应该是逗号分隔的字符串，没有括号，例如`-29.123, 150.982`。
* OSv2不允许具有数组数据类型的属性包含null值。
  * OSv1当前跳过索引数组属性的null值，并返回数组包含null值；因此，查询`null`将不会匹配具有null值的对象，这可能导致对象加载和搜索之间出现不需要的差异。
* 对象集服务（OSS）API不支持查询字符串；OSv1支持查询字符串。
* OSS基数指标**不**支持包含来自Object Storage V1和Object Storage V2的对象的对象集，例如多后端对象集。
* OSv2对象类型只能通过[监控视图](/zh/foundry/maintaining-pipelines/monitoring-views-intro/)进行监控，取代了[Object Storage V1（Phonograph）同步状态健康检查](/zh/foundry/data-health/checks-reference/#sync-status)。

## 临时性重大变更

本节列出了Object Storage V1（Phonograph）与Object Storage V2之间的当前功能差距。这些功能正在开发中，随着重大变更的解决，列表将会更新。

* OSv2目前不支持连接路径在上游和下游目标之间经过物化的计划。

* OSv2目前有一个极端情况，在搜索响应中返回的数据比用户允许看到的数据要少：
  * 当满足以下所有条件时，会出现此问题：
    * 一个对象类型被索引到OSv2，并使用限制视图数据源。
    * 对限制视图数据源的一个数组列应用了[权限标记](/zh/foundry/security/markings/)。
    * 数组列在某些行中包含空数组。
  * 根据权限标记的定义，用户应该被允许看到包含空数组的行，但OSv2在搜索响应中不返回相应的行。
  * 一个临时解决方案是向每个数组添加一个元素，使权限标记使用的数组列不再包含空数组。例如，您可以添加一个每个用户都有访问权限的权限标记。

* OSv2目前不支持在限制视图数据源的细粒度权限策略中使用`Not`条件。

* OSv2目前不支持自定义分析器。

* OSv2目前不支持对增量更新的后备数据集进行投影。

* OSv2目前不支持索引由多个事务支持的增量[视图](/zh/foundry/data-integration/views/)数据集的对象类型。

* Foundry规则原型目前不支持OSv2的完整功能集。例如，由多个数据源支持的对象类型和具有多个物化的对象类型不受支持。有关更多详细信息，您可以参阅[Foundry规则文档](/zh/foundry/foundry-rules/rule-logic/#inputs)。
