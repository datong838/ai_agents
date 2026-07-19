# fixtures · 数字孪生数据目录

线上真实数据落地处（**非测试假数据**）。

```text
fixtures/
  excel/     ← mall-order.xlsx（订单全字段）· mall-goods.xlsx · mall-catalog.xlsx
  word/      ← 业务 Word（协议/说明等）
  ppt/       ← 业务 PPT
  pdf/
    product-intro/
    customer-service/
```

重导 Excel：`python export_fixtures_excel.py`（SSH 隧道需开着）。说明见 [02](../02-Excel与Word-PDF夹具清单.md)。
