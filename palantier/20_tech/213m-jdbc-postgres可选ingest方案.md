# 213m · jdbc-postgres 可选 ingest

> **版本**：v1.1 · 2026-07-20 · **已编码**（M1-W11c）  
> **对齐**：[205m](205m-jdbc-postgres可选探针方案.md) · [100](100-连接器插件运行时方案.md)  
> **点名**：用户「按你建议继续干完」→ W11

## 已决

未配 → 501；`AOS_PG_CONNECTOR_MOCK=1` → mock ingest 写 1 条样本；真 DSN 时按 probe sample upsert（同 mysql 形）。manifest `runtime: live`。

## 落地

| 路径 | 说明 |
| --- | --- |
| `pg_connector.ingest` | mock / live |
| `connector_runtime._pg_ingest` | 注册 ingest |
| `plugins/connectors/jdbc-postgres/manifest.json` | runtime live |
| `tests/test_w11_211_212_213m.py` | stub 501 · MOCK written≥1 |

## 自检

- [x] 无配置 ingest 501  
- [x] MOCK ingest 200 · written≥1  

---

*v1.1 · 213m*
