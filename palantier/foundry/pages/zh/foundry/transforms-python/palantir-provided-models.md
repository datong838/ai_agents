---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/palantir-provided-models/",
  "title": "在变换中使用Palantir提供的语言模型",
  "page_id": "palantir-provided-models",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/lightweight-examples/",
  "next": "/zh/foundry/transforms-python/container-overview/",
  "scraped_at": "2026-07-13T06:07:51.971416+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 在变换中使用Palantir提供的语言模型

:::callout{title="先决条件" theme="neutral"}
要使用Palantir提供的语言模型，必须先在您的注册中启用[AIP](/zh/foundry/administration/enable-aip-features/)。
:::

Palantir提供了一[套语言和嵌入模型](/zh/foundry/platform-overview/aip-capabilities/#supported-llms)，可以被用于在Python变换中。这些模型可以通过`palantir_models`库使用。此库提供了一组`FoundryInputParams`，可以与[`transforms.api.transform`](/zh/foundry/transforms-python/transforms-python-api/#transform)装饰器一起使用。

### 仓库设置

要为您的变换添加语言模型支持，请打开代码仓库左侧的库搜索面板。搜索`palantir_models`并在**库**选项卡中选择**添加并安装库**。重复此过程以添加`language-model-service-api`库。

然后，您的代码仓库将解决所有依赖关系并再次运行检查。检查可能需要一些时间才能完成，之后您将能够在变换中开始使用该库。

### 变换设置

:::callout{title="先决条件" theme="neutral"}
`palantir_model`类只能与[`transforms.api.transform`](/zh/foundry/transforms-python/transforms-python-api/#transform)装饰器一起使用。
:::

在此示例中，我们将使用`palantir_models.transforms.OpenAiGptChatLanguageModelInput`。首先，将`OpenAiGptChatLanguageModelInput`导入到您的Python文件中。现在可以使用此类来创建我们的变换。然后，按照提示指定并导入您希望用作输入的模型和数据集。

```python
from transforms.api import transform, Input, Output
from palantir_models.transforms import OpenAiGptChatLanguageModelInput
from palantir_models.models import OpenAiGptChatLanguageModel

@transform(
    source_df=Input("/path/to/input/dataset")  # 输入数据集路径
    model=OpenAiGptChatLanguageModelInput("ri.language-model-service..language-model.gpt-4_azure"),  # GPT-4 语言模型输入
    output=Output("/path/to/output/dataset"),  # 输出数据集路径
)
def compute_generic(ctx, source_df, model: OpenAiGptChatLanguageModel, output):
    ...
```

当您开始键入资源标识符时，将自动出现一个下拉菜单，以指示可供使用的模型。您可以从下拉菜单中选择所需的选项。

### 使用语言模型生成补全

在此示例中，我们将使用语言模型来确定输入数据集中每个评论的情感。`OpenAiGptChatLanguageModelInput`在运行时向变换提供一个`OpenAiGptChatLanguageModel`，然后可以用来为评论生成补全。

```python
from transforms.api import transform, Input, Output
from palantir_models.transforms import OpenAiGptChatLanguageModelInput
from palantir_models.models import OpenAiGptChatLanguageModel
from language_model_service_api.languagemodelservice_api_completion_v3 import GptChatCompletionRequest
from language_model_service_api.languagemodelservice_api import ChatMessage, ChatMessageRole


@transform(
    reviews=Input("/path/to/reviews/dataset"),
    model=OpenAiGptChatLanguageModelInput("ri.language-model-service..language-model.gpt-4_azure"),
    output=Output("/output/path"),
)
def compute_sentiment(ctx, reviews, model: OpenAiGptChatLanguageModel, output):
    def get_completions(review_content: str) -> str:
        # 系统提示，用于指导语言模型完成任务
        system_prompt = "Take the following review determine the sentiment of the review"
        # 创建聊天完成请求，其中包含系统提示和用户输入的评论内容
        request = GptChatCompletionRequest(
            [ChatMessage(ChatMessageRole.SYSTEM, system_prompt), ChatMessage(ChatMessageRole.USER, review_content)]
        )
        # 使用模型生成情感分析结果
        resp = model.create_chat_completion(request)
        # 返回生成的情感分析结果
        return resp.choices[0].message.content

    # 将输入的评论数据集转换为 Pandas DataFrame
    reviews_df = reviews.pandas()
    # 对评论内容进行情感分析，并将结果添加到新的列 'sentiment' 中
    reviews_df['sentiment'] = reviews_df['review_content'].apply(get_completions)
    # 将 Pandas DataFrame 转换为 Spark DataFrame
    out_df = ctx.spark_session.createDataFrame(reviews_df)
    # 将结果写入输出路径
    return output.write_dataframe(out_df)
```

该代码段用于对评论数据集进行情感分析。它使用 OpenAI 的 GPT-4 模型来分析每条评论的情感，并将结果添加到原数据集的一个新列中，然后将结果存储到指定的输出路径中。

### 嵌入

除了生成语言模型之外，Palantir还提供了一个嵌入模型。以下示例展示了如何使用`palantir_models.transforms.GenericEmbeddingModelInput`在同一个`reviews`数据集上计算嵌入。`GenericEmbeddingModelInput`在运行时为变换提供一个`GenericEmbeddingModel`，可以用来为每个评论计算嵌入。由于Ontology向量属性要求，因此嵌入被显式转换为浮点数。

```python
from transforms.api import transform, Input, Output
from language_model_service_api.languagemodelservice_api_embeddings_v3 import GenericEmbeddingsRequest
from palantir_models.models import GenericEmbeddingModel
from palantir_models.transforms import GenericEmbeddingModelInput
from pyspark.sql.types import ArrayType, FloatType

@transform(
    reviews=Input("/path/to/reviews/dataset"),  # 输入数据集路径
    embedding_model=GenericEmbeddingModelInput("ri.language-model-service..language-model.text-embedding-ada-002_azure"),  # 嵌入模型输入
    output=Output("/path/to/embedding/output")  # 输出数据集路径
)
def compute_embeddings(ctx, reviews, embedding_model: GenericEmbeddingModel, output):
    # 内部函数用于创建嵌入
    def internal_create_embeddings(val: str):
        # 使用嵌入模型生成嵌入向量
        return embedding_model.create_embeddings(GenericEmbeddingsRequest(inputs=[val])).embeddings[0]

    # 将输入数据集转换为Pandas DataFrame
    reviews_df = reviews.pandas()
    # 应用internal_create_embeddings函数生成嵌入并添加到DataFrame
    reviews_df['embedding'] = reviews_df['review_content'].apply(internal_create_embeddings)
    # 将Pandas DataFrame转换为Spark DataFrame
    spark_df = ctx.spark_session.createDataFrame(reviews_df)
    # 将生成的嵌入列类型转换为ArrayType(FloatType)
    out_df = spark_df.withColumn('embedding', spark_df['embedding'].cast(ArrayType(FloatType())))
    # 将最终的DataFrame写入输出路径
    return output.write_dataframe(out_df)
```

该代码片段主要功能是从输入数据集中提取文本内容，通过一个通用嵌入模型生成文本的向量嵌入，并将结果作为新的列添加到数据集中，最终将处理后的数据写入指定的输出路径。
