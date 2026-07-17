---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/derived-series-permissions/",
  "title": "派生序列权限",
  "page_id": "derived-series-permissions",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/manage-derived-series/",
  "next": "/zh/foundry/time-series/derived-series-common-questions/",
  "scraped_at": "2026-07-13T06:11:20.155563+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 派生序列权限

派生序列权限与标准[时间序列权限](/zh/foundry/time-series/time-series-permissions/)非常相似。

## 派生时间序列管理资源

派生序列管理资源的行为与任何其他Palantir资源一样。有关更多信息，请查看我们的[项目和资源](/zh/foundry/projects/overview/)文档。

## 派生时间序列属性值

要查看包含派生序列的时间序列属性，您必须有权访问派生序列逻辑引用的所有时间序列属性。有关详细信息，请查看[时间序列属性权限](/zh/foundry/time-series/time-series-permissions/#time-series-property-permissions)文档。

要手动将派生序列添加到Ontology，您必须有权限编辑绑定对象类型的后备数据源以及该绑定对象类型上的Ontology编辑权限。查看如何[将派生序列保存到Ontology](/zh/foundry/time-series/setup-derived-series/#step-2-ontology-saving)以获取更多信息。

## 派生序列更新

要更新派生序列，用户需要绑定对象类型的Object类型编辑权限。
