# 216m · jdbc-sqlserver 可选 ingest

> **版本**：v1.1 · 2026-07-20 · **已编码**（M1-W12c）  
> **对齐**：[208m](208m-jdbc-sqlserver可选探针方案.md) · [213m](213m-jdbc-postgres可选ingest方案.md)  
> **点名**：用户「按你建议继续干完」→ W12

## 已决

未配 → 501；`AOS_MSSQL_CONNECTOR_MOCK=1` → mock ingest 写 1 条；manifest `runtime: live`。

## 落地

| 路径 | 说明 |
| --- | --- |
| `mssql_connector.ingest` | mock / live |
| `connector_runtime._mssql_ingest` | 注册 |
| `plugins/connectors/jdbc-sqlserver/manifest.json` | runtime live |
| `tests/test_w12_216m.py` | stub · MOCK |

## 自检

- [x] 无配置 501  
- [x] MOCK written≥1  

---

*v1.1 · 216m*
