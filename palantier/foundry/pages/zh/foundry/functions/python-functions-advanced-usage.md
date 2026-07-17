---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/functions/python-functions-advanced-usage/",
  "title": "高级用法",
  "page_id": "python-functions-advanced-usage",
  "category_id": "ontology",
  "section_id": "functions",
  "previous": "/zh/foundry/functions/python-functions-workshop/",
  "next": "/zh/foundry/functions/functions-on-models/",
  "scraped_at": "2026-07-14T04:29:29.225286+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 高级用法

## 发布查询函数

要注册一个可从其他 TypeScript 或 Python 函数调用的 Python 函数，必须为您的 Python 函数提供一个 API 名称。为此，请在 `@function` 装饰器中提供 `api_name` 字段：

```python
from functions.api import function  # 从functions.api导入function

@function(api_name="myPythonFunction")  # 使用装饰器定义API名称为myPythonFunction
def my_python_function() -> str:
    return "Hello World!"  # 返回字符串 "Hello World!"
```

## 调用查询函数

在发布您的 TypeScript 或 Python 查询函数后，导航到您希望使用该函数的代码库，并使用[**资源导入**侧边栏](/zh/foundry/functions/resource-imports-sidebar/)导入它。

然后，您的函数将可以从使用该函数的代码库中调用。例如，要从 Python 函数中调用它：

```python
from functions.api import function
from ontology_sdk import FoundryClient

@function
def call_query_function() -> str:
    # 调用 FoundryClient 来执行查询，并返回结果
    return FoundryClient().ontology.queries.my_python_function()
```

从TypeScript函数调用它：

```typescript
import { Queries } from "@foundry/ontology-api"

export class MyFunctions {
    @Function()
    public callQueryFunction(): Promise<string> {
        // 调用查询函数，返回一个Promise对象，该对象解析为字符串
        return Queries.myPythonFunction();
    }
}
```

从Python函数调用TypeScript查询函数看起来完全相同；使用[API名称](/zh/foundry/functions/query-functions/#example-api-named-query)发布TypeScript查询函数，然后如上所示从Python中使用它。
