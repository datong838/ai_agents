---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/dataset-preview/dataset-preview-faq/",
  "title": "数据集预览常见问题",
  "page_id": "dataset-preview-faq",
  "category_id": "data-integration",
  "section_id": "dataset-preview",
  "previous": "/zh/foundry/dataset-preview/sql-console/",
  "next": "/zh/foundry/linter/overview/",
  "scraped_at": "2026-07-13T06:04:34.421279+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 数据集预览常见问题

以下是关于数据集预览的一些常见问题。

有关一般信息，请参阅[数据集预览概述](/zh/foundry/dataset-preview/overview/)。

* [CSV因引号字符不匹配而解析失败](#csv-fails-to-parse-due-to-unmatched-quote-character)
* [数据集解析失败，因为一些底层CSV有更多列](#dataset-fails-to-parse-because-some-underlying-csvs-have-more-columns)
* [为什么我下载的数据集在Microsoft Excel中打开时看起来很奇怪？](#why-does-my-downloaded-dataset-look-weird-when-i-open-it-in-microsoft-excel)

***

## CSV因引号字符不匹配而解析失败

当上传一个包含嵌套双引号和嵌入的换行符（`\n`）字符的CSV时，模式推断将失败，并且您无法使用模式编辑器创建一个有效的模式。

要进行故障排除，请执行以下步骤：

1. 将CSV上传到数据集中并选择**编辑模式**。
2. 设置**列**和**引号**属性。
3. 忽略模式验证出错，并选择**保存而不验证**，该选项在**保存并验证**选项旁的下拉菜单中可用。这将创建一个具有正确列定义的模式。
4. 在**详情**选项卡中，以编辑模式打开模式。
5. 将`dataFrameReaderClass`更改为`com.palantir.foundry.spark.input.DataSourceDataFrameReader`。
6. 在 `"customMetadata"` Object中添加以下内容：

```json
  "customMetadata": {
    "format": "csv",  // 文件格式为 CSV
    "options": {
      "header": true,  // CSV 文件中包含表头
      "multiLine": true  // 允许 CSV 文件中的字段占用多行
    }
  }
```

[返回顶部](#dataset-preview-faq)

***

## 数据集解析失败因为某些底层CSV具有更多列

当一个数据集由多个CSV组成时（例如，通过数据连接 `APPEND` 事务），如果其中一些CSV包含更多列，模式推断将失败。一种选择是忽略不规则行（例如缺少某些列的行）。要做到这一点，请选择**编辑模式**，展开**解析选项**部分，并勾选**忽略不规则行**。

然而，如果您希望保留不规则行并为数据集指定一个标准化的模式，则适用此部分。如果您数据中符合下文**假设**部分中列出的条件，那么故障排除步骤将生成一个用户定义的标准模式的数据集，其中不规则行将自动填充缺少列为`null`。

**解析失败的症状：**

您可能会遇到这样的错误信息：“无法加载预览：解析输入CSV数据时出错。请确保所有数据格式正确。”

在选择**编辑模式**然后**保存并验证**后，您也可能会遇到以下错误信息：“您的数据集在x行上验证失败。”

**假设**：

1. 您可以定义所需的模式，例如数据集应具备的所有列名和类型。

2. 您的模式强制严格的列顺序。例如，如果您希望数据集包含和显示列\_{a, b, c}\_，则底层CSV可以具有如下列结构：

* *{a}*
* *{a, b}*

但不能具有如下列结构：

* *{b, a}*

3. 如果底层CSV具有第\_(n+1)\_ 列，则其必须具有所有前面的\_n\_列。例如，如果您希望数据集包含和显示列\_{a, b, c, d}\_，则底层CSV可以具有如下列结构：

* *{a}*
* *{a, b}*
* *{a, b, c}*

但不能具有如下列结构：

* *{b, c, d}*
* *{a, c, d}*
* *{a, b, d}*

以下是一个故障排除步骤适用且有用的案例示例：

通过`APPEND`事务定期将CSV添加到数据集中。某天，添加了一个新列，并成为CSV中的新最后一列。在数据集中，所有先前追加的CSV的行应该具有新列，字段值自动填充为`null`，而不是被视为不规则。

故障排除步骤不会复制`mergeSchema`选项的功能，该选项适用于原始Parquet数据集（这些数据集使用`com.palantir.foundry.spark.input.ParquetDataFrameReader`作为`dataFrameReaderClass`进行解析）。需要用户编写变换以在原始CSV数据集上复制此类功能。

要进行故障排除，请执行以下步骤：

1. 在**详情**选项卡中，打开**模式**选项卡，并选择**编辑**
2. 修改`fieldSchemaList`以确保其包含数据集应具备的所有列。例如，如果数据集应具有列\_{a, b, c}\_，且全部为整数类型，则`fieldSchemaList`可能如下所示：

```json
  "fieldSchemaList": [
    {
      "type": "INTEGER",  // 字段类型为整数
      "name": "a",  // 字段名称为a
      "nullable": null,  // 是否可为空，当前为null未指定
      "userDefinedTypeClass": null,  // 用户定义的类型类，当前为null未指定
      "customMetadata": {},  // 自定义元数据，当前为空对象
      "arraySubtype": null,  // 数组子类型，当前为null未指定
      "precision": null,  // 精度，当前为null未指定
      "scale": null,  // 标度，当前为null未指定
      "mapKeyType": null,  // 映射键类型，当前为null未指定
      "mapValueType": null,  // 映射值类型，当前为null未指定
      "subSchemas": null  // 子模式，当前为null未指定
    },
    {
      "type": "INTEGER",  // 字段类型为整数
      "name": "b",  // 字段名称为b
      "nullable": null,  // 是否可为空，当前为null未指定
      "userDefinedTypeClass": null,  // 用户定义的类型类，当前为null未指定
      "customMetadata": {},  // 自定义元数据，当前为空对象
      "arraySubtype": null,  // 数组子类型，当前为null未指定
      "precision": null,  // 精度，当前为null未指定
      "scale": null,  // 标度，当前为null未指定
      "mapKeyType": null,  // 映射键类型，当前为null未指定
      "mapValueType": null,  // 映射值类型，当前为null未指定
      "subSchemas": null  // 子模式，当前为null未指定
    },
    {
      "type": "INTEGER",  // 字段类型为整数
      "name": "c",  // 字段名称为c
      "nullable": null,  // 是否可为空，当前为null未指定
      "userDefinedTypeClass": null,  // 用户定义的类型类，当前为null未指定
      "customMetadata": {},  // 自定义元数据，当前为空对象
      "arraySubtype": null,  // 数组子类型，当前为null未指定
      "precision": null,  // 精度，当前为null未指定
      "scale": null,  // 标度，当前为null未指定
      "mapKeyType": null,  // 映射键类型，当前为null未指定
      "mapValueType": null,  // 映射值类型，当前为null未指定
      "subSchemas": null  // 子模式，当前为null未指定
    }
  ],
```

3. 更改 `"dataFrameReaderClass"` 及其嵌套的 `customMetadata` Object，使您的模式 JSON 的结尾看起来如下所示：

```json
"dataFrameReaderClass": "com.palantir.foundry.spark.input.DataSourceDataFrameReader",
  "customMetadata": {
    "format": "csv",  // 指定数据格式为 CSV
    "options": {
      "multiLine": true,  // 支持多行数据
      "header": true,  // 第一行作为表头
      "mode": "PERMISSIVE"  // 解析模式为宽容模式，允许有错误的输入并尝试解析
    }
  }
}
```

4. 选择 **保存**。

[返回顶部](#dataset-preview-faq)

***

## 为什么我下载的数据集在 Microsoft Excel 中打开时看起来很奇怪？

当从平台导出数据集时，有些文件在打开时可能会显得压缩。在某些地区观察到了这个问题，原因是 Excel 使用的默认分隔符。要解决此问题，您需要更改导出设置中的分隔符模式：

1. 在 Excel 中打开文件。
2. 选择功能区中的 **数据** 选项卡。
3. 在 **数据工具** 组中选择 **分列** 选项。
4. 在 **文本分列向导** 窗口中，选择 **分隔符号** 选项，然后点击 **下一步**。
5. 在 **分隔符** 部分，选择您想使用的分隔符（如逗号、分号、制表符）。
6. 选择 **下一步** 然后 **完成** 以完成该过程。

[返回顶部](#dataset-preview-faq)
