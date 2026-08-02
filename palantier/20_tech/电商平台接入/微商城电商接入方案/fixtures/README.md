# fixtures · 数字孪生数据目录

> **安全边界（2026-08-02）：** 本目录不得落入未脱敏的线上业务明细。默认只允许合成数据或经审批、脱敏、限量的数据；真实 PII、订单明细和支付信息不得进入 Git。现有导出脚本已隔离，禁止直接运行。

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
