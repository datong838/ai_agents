---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/time-series-permissions/",
  "title": "时间序列权限",
  "page_id": "time-series-permissions",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/create-sensor-ot/",
  "next": "/zh/foundry/time-series/advanced-setup/",
  "scraped_at": "2026-07-13T06:10:22.877048+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 时间序列权限

在平台中使用时间序列需要以下权限和访问。

## 时间序列属性权限

要在给定的Object上查看[时间序列属性](/zh/foundry/time-series/time-series-properties/)，您必须能够访问该Object及时间序列属性的支持数据源。

![时间序列属性权限概述图。](../../../images/foundry/time-series/time-series-permissions-overview.png)

### Object权限

用户必须能够访问特定的Object（通常是支持数据源行）和属性（通常是提供该属性的支持数据源）。这一要求不仅限于时间序列属性；所有Object属性都遵循这一方案。有关更多信息，请查看我们的[管理Object安全性](/zh/foundry/object-permissioning/managing-object-security/)文档。

### 时间序列属性支持数据源权限

时间序列\_属性\_引用时间序列\_数据\_，位于时间序列\_同步\_中。这些时间序列同步必须在[时间序列属性](/zh/foundry/time-series/time-series-properties/)本身中列为支持数据源。要查看时间序列属性，您必须满足其所有支持数据源的访问要求。了解更多信息请参阅[以下部分](#granular-time-series-property-permissions)。

#### 时间序列同步权限

[时间序列同步](/zh/foundry/time-series/time-series-syncs/)将继承其输入数据集的所有权限标记。要查看时间序列同步，需要对输入数据集的权限标记拥有相应的权限。

## 细粒度时间序列属性权限

:::callout{theme="neutral"}
Palantir管理员可以通过内部配置启用此功能；这可能需要几天时间传播到您的注册。
:::

在Palantir中，Object及其属性的细粒度访问通过受限视图（权限行）和不同的数据源（通过MDO的权限列）组合配置。时间序列属性与其他属性不同，因为它们还引用时间序列同步。由于时间序列同步无法由受限视图支持，因此它们无法拥有细粒度权限。

作为时间序列同步细粒度权限的替代方案，我们建议在时间序列同步的输入数据集上设置非常严格的权限标记，仅允许选择的一组个人直接查看它。然后，在[时间序列目录应用](/zh/foundry/time-series/time-series-syncs/#time-series-catalog-app)中停止继承这些权限标记。如果某个权限标记不再被继承，那么在通过时间序列属性访问时间序列时，将不再需要该权限标记的权限。一旦切断了所有支持时间序列同步的权限标记，时间序列属性权限就与所有其他标准属性权限相同；如果您能够访问Object和属性，您就可以查看属性值。有关更多信息，请查看我们的[管理Object安全性](/zh/foundry/object-permissioning/managing-object-security/)文档。

![细粒度时间序列属性权限图。](../../../images/foundry/time-series/time-series-granular-permissions.png)

### 时间序列同步权限标记

时间序列同步继承其输入数据集的所有权限标记。要查看时间序列同步，您必须满足这些权限标记的所有查看要求。如果您选择停止继承时间序列同步上的权限标记，那么在通过时间序列属性加载时间序列时，将不再需要这些时间序列同步权限标记的权限（即，通过Object查看时间序列时）。

此配置仅在通过Object的时间序列属性加载时间序列时绕过时间序列同步的权限标记要求。您仍然需要满足这些权限标记以直接访问时间序列同步。

![管理时间序列的权限标记。](/resources/foundry/time-series/time-series-advanced-setup-manage-markings.png)

查看[权限标记](/zh/foundry/security/markings/)文档以获取更多关于使用权限标记的信息。

:::callout{theme="warning"}
这是一个高级配置。切断时间序列同步的权限标记时请谨慎。通过时间序列属性访问时间序列数据将完全取决于属性和Object权限。
:::

### 受限视图Object类型数据源

要查看时间序列属性，您必须能够访问Object及时间序列属性的支持数据源。一旦切断了支持时间序列同步的权限标记，您可以通过Object类型的细粒度权限为时间序列设置权限。

可以使用受限视图作为Object的支持数据源来控制对Object的细粒度访问。受限视图将决定用户可以访问哪些Object。了解更多关于[管理Object安全性](/zh/foundry/object-permissioning/managing-object-security/)的信息。
