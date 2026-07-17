---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pb-functions-transform/renameColumnsV1/",
  "title": "重命名列",
  "page_id": "renameColumnsV1",
  "category_id": "data-integration",
  "section_id": "pb-functions-transform",
  "previous": "/zh/foundry/pb-functions-transform/windowedProjectV1/",
  "next": "/zh/foundry/pb-functions-transform/repartitionV1/",
  "scraped_at": "2026-07-13T05:58:52.369453+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 重命名列

> 支持于: 批处理, 流处理

重命名一组列。

**变换类别**: 数据准备, 流行

## 声明的参数

* **输入数据集** - 包含要重命名列的源数据集。<br>*Table*
* **重命名** - 从现有列名重命名为新名称。<br>*List\<Tuple\<Column\<AnyType>, Literal<字符串>>>*

## 示例

### 示例 1: 基本案例

**参数值:**

* **输入数据集**: ri.foundry.main.dataset.a
* **重命名**: \[(`recently_serviced`, does\_not\_require\_service)]

**输入:**

| recently\_serviced | tail\_number | airline\_code |
| ----- | ----- | ----- |
| true | KK-150 | KK |
| false | XB-120 | XB |
| true | MT-190 | MT |

**输出:**

| does\_not\_require\_service | tail\_number | airline\_code |
| ----- | ----- | ----- |
| true | KK-150 | KK |
| false | XB-120 | XB |
| true | MT-190 | MT |

***
