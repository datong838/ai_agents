# 217m · REST/File 可选 ingest

> **版本**：v1.1 · 2026-07-20 · **已编码**（M1-W13a）  
> **对齐**：[201m](201m-REST-Connector可选HTTP方案.md) · [202m](202m-File-Connector可选探针方案.md) · [213m](213m-jdbc-postgres可选ingest方案.md)  
> **点名**：用户「按你建议继续干完」→ W13

## 已决

| 插件 | 未配 | MOCK / 已配 |
| --- | --- | --- |
| rest-generic | ingest 501 | `AOS_REST_CONNECTOR_MOCK=1` 或 URL → written≥1 |
| file-local | ingest 501 | `AOS_FILE_LOCAL_MOCK=1` 或 ROOT → written≥1 |

## 落地

| 路径 | 说明 |
| --- | --- |
| `connector_runtime._rest_ingest` / `_file_local_ingest` | MOCK · upsert |
| `plugins/.../manifest.json` | runtime live · ingest |
| `tests/test_w13_217_219m.py` | stub · MOCK |

## 自检

- [x] rest/file 无配置 501  
- [x] MOCK ingest 200  

---

*v1.1 · 217m*
