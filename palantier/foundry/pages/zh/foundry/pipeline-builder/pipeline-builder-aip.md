---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/pipeline-builder/pipeline-builder-aip/",
  "title": "Pipeline Builder中的AIP功能",
  "page_id": "pipeline-builder-aip",
  "category_id": "data-integration",
  "section_id": "pipeline-builder",
  "previous": "/zh/foundry/pipeline-builder/navigation/",
  "next": "/zh/foundry/pipeline-builder/functions-index/",
  "scraped_at": "2026-07-13T05:56:19.644905+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Pipeline Builder中的AIP功能

Pipeline Builder提供了一系列AIP辅助功能，旨在帮助您更好地理解、搭建和管理您的pipeline。这些功能允许您通过单一提示生成新的数据变换逻辑，解释pipeline开发中的步骤，建议名称和描述，创建和编辑正则表达式，以及转换时间戳。

## Pipeline Builder助手功能

### 生成

使用**生成**功能，根据用户提示创建新的数据变换逻辑。AIP可以访问Pipeline Builder中可用的全部数据变换套件，并推荐最适合您特定需求的变换。这为建议变换提供了透明的推理和理由，使用元数据生成逻辑，而不暴露底层数据。最终，AIP变换会像常规数据变换一样保存到您的pipeline逻辑中，使其能够无缝集成到现有的工作流中。

![Pipeline Builder图上的AIP生成功能。](../../../images/foundry/pipeline-builder/aip-generate-complete.png)

要使用生成功能，请在Pipeline Builder图的顶部中心选择带有两颗星的紫色图标**AIP**。按照弹出窗口中的说明，选择图上的节点作为输入。在MacOS上按住`cmd`或在Windows上按住`ctrl`并选择一个节点以添加或移除它。

![AIP生成功能起始状态。](../../../images/foundry/pipeline-builder/aip-generate-starting-state.png)

接下来，输入AIP要评估的提示，然后选择**生成**以开始运行。

![AIP生成功能与用户输入提示。](../../../images/foundry/pipeline-builder/aip-generate-prompt.png)

这将返回一个或多个用紫色高亮显示的变换节点，以及生成的变换的描述。

![AIP生成功能返回的合并变换。](../../../images/foundry/pipeline-builder/aip-generate-union.png)

要继续变换，请选择**返回生成**。选择下一组节点并输入下一个提示以继续搭建您的pipeline。

![AIP生成功能返回的多个合并。](../../../images/foundry/pipeline-builder/aip-generate-join.png)

要查看您最近的提示，请选择输入框。您可以通过选择历史条目来重试任何提示，这将自动选择原始输入。

![AIP生成功能显示最近的提示。](../../../images/foundry/pipeline-builder/aip-generate-history.png)

### 解释

使用**解释**功能，通过开发过程的每一步动态获取pipeline的描述。保持您的协作者同步当前状态，为新的审批者提供有价值的背景信息，或在新团队成员之间进行知识传递，几乎无需维护。

![Pipeline Builder图上的AIP解释功能。](../../../images/foundry/pipeline-builder/aip-explain-button.png)

要使用解释，请在Pipeline Builder图的顶部中心选择标有**AIP**的紫色灯泡。按照弹出窗口中的说明，选择图上的表作为输入。按住并选择一个节点以添加或移除它。您的选择必须包含至少一个变换节点，并且是一个具有单一输出的连接节点集。

![按照说明选择图中的节点。](../../../images/foundry/pipeline-builder/aip-explain-select-node.png)

按住并选择一个节点以添加或移除它。您的选择必须包含至少一个变换节点，并且是一个具有单一输出的连接节点集。

最后，选择**解释xx节点**以生成变换解释。

![解释功能将为所选节点生成解释。](../../../images/foundry/pipeline-builder/aip-explain-generate.png)

![阅读输出以了解更多关于所选节点的信息。](../../../images/foundry/pipeline-builder/aip-explain-node.png)

您还可以通过选择一个节点并从出现在右侧的菜单中选择紫色**解释**按钮来解释单个节点。

![在图上解释单个节点。](../../../images/foundry/pipeline-builder/aip-explain-single-node.png)

此外，您可以选择解释节点内的任何一组变换。

![在搜索变换时解释一组变换。](../../../images/foundry/pipeline-builder/aip-explain-transfrom-set.png)

了解更多关于[Pipeline Builder中的变换](/zh/foundry/pipeline-builder/transforms-overview/)。

### 建议名称和描述

您还可以在Pipeline Builder中使用AIP快速记录您的工作，通过为任何变换节点生成建议的名称和描述。

选择默认变换名称旁边的紫色AIP星形图标以生成建议的名称。

![生成建议的变换节点名称。](../../../images/foundry/pipeline-builder/aip-transform-assist.png)

在此示例中，建议的名称`Open claims by landlord...`比`Transform path`提供了更多信息：

![建议的名称提供了更多关于变换的信息。](../../../images/foundry/pipeline-builder/aip-transform-suggested-name.png)

选择紫色的**生成**按钮以生成建议的描述。

![生成建议的变换节点描述。](../../../images/foundry/pipeline-builder/aip-transform-description.png)

在此示例中，描述提供了有关通过房东ID分组索赔数据的变换的更多细节：

![建议的描述提供了更多关于变换的信息。](../../../images/foundry/pipeline-builder/aip-transform-suggested-description.png)

生成的建议是变换路径的简短摘要。一旦您保存了生成的名称或描述，信息就会自动保存在pipeline中，并对协作者可见。

要一次建议最多10个节点，请打开屏幕底部的**建议**选项卡。

![Pipeline Builder图中有多个红色和绿色的节点。节点预览中出现了紫色的建议选项卡。](../../../images/foundry/pipeline-builder/aip-bulk-suggest.png)

选择pipeline上的一个或多个节点以生成名称和描述（如果尚不存在）。

![由于图中没有选择节点，节点预览中的紫色建议选项卡为空。](../../../images/foundry/pipeline-builder/aip-bulk-select.png)

在每个建议上选择**应用**以将更改保存到节点。

![图中选择了多个红色节点，建议选项卡列出了四个建议。](../../../images/foundry/pipeline-builder/aip-bulk-apply.png)

### 变换助手

变换助手功能可以帮助您充分利用Pipeline Builder中提供的多种变换选项。利用AIP的强大功能，正则表达式助手可以基于您的输入生成正则表达式，并更新现有表达式。此外，使用时间戳格式化器，您可以快速将面板值从`字符串`转换为`时间戳`。

#### 正则表达式助手

正则表达式助手通过为您提供准确有效的正则表达式模式来简化创建数据pipeline的过程，以提取、替换和查找数据中的字符串。要使用正则表达式助手，首先创建一个新变换面板，使用正则表达式参数：regex提取、regex提取所有、regex替换、regex查找或regex匹配。在下面的示例中，我们在表达式列`email_string`上使用regex提取变换。

选择**Pattern**字段旁边的紫色AIP星形图标，然后描述您要创建的正则表达式。在此示例中，我们想搜索电子邮件域名。

![使用正则表达式助手帮助创建精确的正则表达式](../../../images/foundry/pipeline-builder/aip-regex-helper.png)

选择紫色的**生成**按钮以查看结果。

![轻松创建和应用正则表达式到您的数据。](../../../images/foundry/pipeline-builder/aip-regex-helper-results.png)

##### 更新现有表达式

您还可以使用正则表达式助手更新现有的正则表达式。

选择**Pattern**字段旁边的紫色AIP星形图标。然后，输入您要修改的正则表达式，后跟修改。在下面的示例中，正则表达式`@([\da-z\.-]+\.([a-z\.]{2,63})`应该修改为包含大写。

![使用正则表达式助手修改现有的正则表达式。](../../../images/foundry/pipeline-builder/aip-modify-regex.png)

选择紫色的**生成**按钮以查看结果。

![轻松修改和应用更新的正则表达式到您的数据。](../../../images/foundry/pipeline-builder/aip-modify-regex-results.png)

#### 时间戳格式化器

时间戳格式化器提供了一种节省时间的解决方案，可以在转换面板中快速将字符串转换为时间戳。要使用时间戳格式化器，首先创建一个新的转换面板，配置为从字符串转换为时间戳。在下面的示例中，我们有不同格式的时间戳：

![Pipeline Builder中的一个转换为时间戳面板的示例。](../../../images/foundry/pipeline-builder/aip-timestamp-formatter.png)

然后，选择紫色的**生成**按钮，输入您想在转换中使用的解析格式的示例。在我们的示例中，我们将粘贴所有五个时间戳：

![将出现一个框以输入您想使用的解析格式。](../../../images/foundry/pipeline-builder/aip-generate-timestamp.png)

然后，AIP将生成一组与这些时间戳匹配的格式并将其输入到转换面板中。选择**应用**。

![一旦生成格式，它们将自动添加到面板中。](../../../images/foundry/pipeline-builder/aip-apply-timestamp-format.png)

然后，字符串列被解析为时间戳列。

![您的数据集现在有一个解析后的时间戳列以及原始字符串列。](../../../images/foundry/pipeline-builder/aip-cast-string-to-timestamp.png)

了解更多关于[Pipeline Builder中的变换](/zh/foundry/pipeline-builder/transforms-overview/)。

#### 生成提案描述

您还可以在Pipeline Builder中使用AIP快速描述您的更改，通过在提出提案时生成提案描述。

![更改后，创建提案。](../../../images/foundry/pipeline-builder/aip-proposal-graph.png)

要做到这一点，首先在右上角选择**提案**。这将带您进入提案创建视图。

![新提案。](../../../images/foundry/pipeline-builder/aip-proposal-new.png)

现在选择紫色的**生成**按钮。AIP将为您的分支上的pipeline更改撰写提案描述。

![生成的提案描述。](../../../images/foundry/pipeline-builder/aip-proposal-description.png)

在此示例中，有多个更改，包括对某些pipeline设置的更改。AIP为您描述了所有这些。

您还可以输入额外的上下文，注意特定更改，甚至在选择**生成**之前在文本框中开始撰写粗略的提案描述。AIP将利用这些来增强其提案描述。生成的描述将被添加在您的文本下方，并有明确的分隔。

![另一个生成的提案描述，之前有用户提示。](../../../images/foundry/pipeline-builder/aip-proposal-generated.png)

要再次生成或更改您提供的描述，请确保在选择**生成**之前，只有相关文本位于文本框中。为获得最佳效果，所有其他文本，包括任何先前生成的描述，都应删除。

## 用于自定义工作流的AIP功能

要使用以下功能，用户必须由平台管理员[授予AIP功能用于自定义工作流的权限](/zh/foundry/administration/enable-aip-features/#aip-and-capabilities-for-custom-workflows)。

### 文本转嵌入

您可以使用[`文本转嵌入`](/zh/foundry/pb-functions-expression/textToEmbeddingsV2/)表达式，通过提供要转换为嵌入向量的字符串，将文本嵌入为向量，使用`Text embedding ada-002`嵌入模型。这些向量旨在捕捉单词或短语的语义含义，从而实现高级文本分析和操作。

嵌入文本计算成本高昂，可能导致预览和搭建速度变慢。

![文本转嵌入](../../../images/foundry/pipeline-builder/text-to-embedding.png)

### 使用LLM节点

[使用LLM节点](/zh/foundry/pipeline-builder/pipeline-builder-llm/)功能提供了一种便捷的方法，可以在大规模数据上执行大型语言模型（LLM），从而使您能够无缝地将LLM处理逻辑集成到各种数据变换之间，无需编写代码即可简化LLM的集成。

***

注意：AIP功能的可用性可能会发生变化，并可能因客户而异。
