---
{
  "source_url": "https://www.palantir.com/docs/zh/foundry/functions/debug/",
  "title": "调试函数",
  "page_id": "debug",
  "category_id": "ontology",
  "section_id": "functions",
  "previous": "/zh/foundry/functions/undefined-values/",
  "next": "/zh/foundry/functions/add-dependencies/",
  "scraped_at": "2026-07-14T04:28:58.972013+00:00"
}
---

:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 调试函数

当您编写函数时，可能需要检查执行状态以解决代码正确性或性能问题。以下是您可以用来执行此操作的功能。

## 控制台日志记录

函数支持在执行期间发出控制台日志以进行调试。为此，只需使用 `console.log` 命令来发出日志。例如：

```typescript
    @Function()
    public testConsoleLogging(n: Integer): Integer {
        for (let i = 0; i < n; i++) {
            console.log(`Iteration ${i}`); // 打印当前迭代次数
        }
        return n; // 返回输入参数 n
    }
```

当您在**编写**中使用**函数助手**运行此函数时，控制台日志将被捕获并显示在下方，伴随时间戳：

![console-logging-live-preview](../../../images/foundry/functions/console-logging-live-preview.png)

以这种方式使用控制台日志可以帮助调试正确性问题。您还可以添加控制台日志以识别代码中的性能瓶颈。请参阅[优化性能](/zh/foundry/functions/optimize-performance/)指南，以获取有关如何提高链接遍历逻辑性能的更多信息。
