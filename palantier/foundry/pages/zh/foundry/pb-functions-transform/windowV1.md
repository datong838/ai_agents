---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/windowV1/",
  "title": "窗口",
  "page_id": "windowV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/wideUnionByNameV1/",
  "next": "/zh/foundry/code-repositories/overview/",
  "scraped_at": "2026-07-13T05:59:39.068998+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 窗口

> 支持于: 批处理

对按一组列分组的输入数据集执行指定的聚合操作。

**变换类别**: 聚合, 热门

## 声明的参数

* **数据集** - 执行聚合的数据集。<br>*表格*
* **表达式** - 要在窗口中计算的表达式列表。<br>*列表<表达式<任意类型>>*
* **窗口** - 要操作的窗口。<br>*窗口*
