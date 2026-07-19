# 208m · jdbc-sqlserver 可选探针

> **版本**：v1.1 · 2026-07-20 · **已编码**（M1-W10a）  
> **对齐**：[205m](205m-jdbc-postgres可选探针方案.md)  
> **点名**：用户「继续」→ W10

## 已决

未配 → 501；`AOS_MSSQL_CONNECTOR_MOCK=1` 或 HOST/DSN → health/probe 绿。

## 落地

| 路径 | 说明 |
| --- | --- |
| `aos_api/mssql_connector.py` | mock / live（pymssql） |
| `connector_runtime._HANDLERS["jdbc-sqlserver"]` | health · probe |
| `tests/test_w10_208_209m.py` | stub 501 · MOCK 200 |

## 自检

- [x] 无配置 501  
- [x] MOCK 200  

---

*v1.1 · 208m*
