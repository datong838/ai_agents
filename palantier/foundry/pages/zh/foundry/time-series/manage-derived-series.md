---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/time-series/manage-derived-series/",
  "title": "管理派生序列",
  "page_id": "manage-derived-series",
  "category_id": "data-integration",
  "section_id": "time-series",
  "previous": "/zh/foundry/time-series/manual-ontology-saving/",
  "next": "/zh/foundry/time-series/derived-series-permissions/",
  "scraped_at": "2026-07-13T06:11:50.425115+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 管理派生序列

一旦您保存了来自Quiver的派生序列逻辑，您可以访问派生序列的管理页面。该页面表示生成的Palantir资源以及用于执行派生序列计算的codex模板。您可以从平台文件系统或派生序列创建后出现的通知中导航到此页面。

![创建成功通知。](/resources/foundry/time-series/derived-series-success-toast.png)

管理页面包括以下三个主要标签页。

## 概览

**概览**标签允许用户预览其逻辑、Ontology设置和一般的派生序列详细信息。

选择**标题**或**描述**文本，以编辑在Quiver分析和其他应用程序中使用的标题和描述。在右上角选择**重新发布**以查看更改并更新派生序列的显示信息。

![派生序列“概览”标签。](../../../images/foundry/time-series/derived-series-overview-tab.png)

## 逻辑

**逻辑**标签可用于查看和编辑派生序列逻辑。修改行内的时间序列卡片以编辑逻辑。在顶部工具栏中选择**保存**以持久化更改。

:::callout{theme="neutral"}
如果派生序列被保存到Ontology，保存的逻辑更改将立即生效，除非派生序列[固定到Ontology中的特定版本](/zh/foundry/time-series/setup-derived-series/#option-2-bind-to-a-sensor-object-type)。
:::

![派生序列“逻辑”标签。](../../../images/foundry/time-series/derived-series-logic-tab.png)

## Ontology

如果派生序列已[自动保存到Ontology](/zh/foundry/time-series/setup-derived-series/#step-2-ontology-saving)，则**Ontology**标签可用于查看和编辑传感器Object类型的Object范围和属性映射。

![派生序列“Ontology”标签。](../../../images/foundry/time-series/derived-series-ontology-tab.png)

对Object范围的更改必须保存并部署。在顶部工具栏中选择**保存**以查看和保存范围更改。保存后，选择工具栏中的**部署**以将更改部署到Ontology。

### Ontology状态指示器

Ontology状态指示器显示派生序列是否根据当前请求的逻辑版本和Ontology选项是最新的。

![派生序列Ontology状态指示器。](../../../images/foundry/time-series/derived-series-ontology-status-indicator.png)
