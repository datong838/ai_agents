---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/transforms-python/read-files-repository/",
  "title": "读取存储库中的文件",
  "page_id": "read-files-repository",
  "category_id": "data-integration",
  "section_id": "transforms-python",
  "previous": "/zh/foundry/transforms-python/data-expectations-reference/",
  "next": "/zh/foundry/transforms-python/output-column-metadata/",
  "scraped_at": "2026-07-13T06:07:59.595594+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 读取存储库中的文件

您可以将存储库中的其他文件读入变换上下文。这可能有助于设置参数，以供您的变换代码引用。

首先，在您的 Python 存储库中编辑 `setup.py`:

```python
setup(
    name=os.environ['PKG_NAME'],
    # 从环境变量中获取包的名称
    package_data={
        '': ['*.yaml', '*.csv']
        # 包含在包中的非Python文件类型，通常用于配置或数据文件
    }
)
```

这告诉Python将yaml和csv文件打包到包中。 然后将配置文件（例如`config.yaml`，也可以是csv或txt）放在Python变换（例如`read_yml.py`，见下文）旁边：

```yaml
- name: tbl1
  primaryKey:
  - col1
  - col2
  # 定义主键，由col1和col2组成

  update:
  - column: col3
    with: 'XXX'
    # 更新操作，将col3列的值替换为'XXX'
```

您可以使用以下代码在您的变换 `read_yml.py` 中读取它：

```python
from transforms.api import transform_df, Input, Output
from pkg_resources import resource_stream
import yaml
import json

@transform_df(
    Output("/Demo/read_yml")
)
def my_compute_function(ctx):
    # 从当前包中读取名为 "config.yaml" 的资源文件
    stream = resource_stream(__name__, "config.yaml")
    # 使用 yaml.safe_load 解析 YAML 文件流
    docs = yaml.safe_load(stream)
    # 将解析的 YAML 内容转换为 JSON 格式，并创建一个 DataFrame 返回
    return ctx.spark_session.createDataFrame([{'result': json.dumps(docs)}])
```

因此，您的项目结构将是：

* some\_folder
  * `config.yaml`
  * `read_yml.py`

这将在您的数据集中输出一行，其中一列“result”的内容为：

```json
[
    {
        "primaryKey": ["col1", "col2"], // 主键由col1和col2两列组成
        "update": [
            {
                "column": "col3", // 需要更新的列是col3
                "with": "XXX" // 更新的内容是XXX
            }
        ],
        "name": "tbl1" // 表的名称是tbl1
    }
]
```
