# 100 · Connector Host 运行时按插件分发

> **版本**：v1.0 · 2026-07-19  
> **状态**：✅ 已落地 · 自测通过  
> **上游**：[97](97-Connector插件化整改方案.md) · [20 §3.1](20-AOS整体技术方案.md) · T05  
> **Rules**：Host 只认 pluginId · 厂商实现挂 handler · 旧 `/mysql/*` 兼容别名 · stub 诚实 501

---

## 1. 问题

97 已有 `plugins/connectors` 目录，但运行时仍是 **`/v1/connectors/mysql/*` 厂商路径**，新增 postgres 仍要改 Host 路由表。

## 2. 目标

| 项 | 做法 |
| --- | --- |
| 统一面 | `GET/POST /v1/connectors/{plugin_id}/health\|probe\|ingest` |
| 分发 | `connector_runtime` 按已安装插件 id 调 handler |
| live | `jdbc-mysql` → 既有 `mysql_connector` |
| stub | postgres/sqlserver/rest → **501 CONNECTOR_STUB** |
| 兼容 | `/v1/connectors/mysql/*` 转发到 `jdbc-mysql` |

非目标：真做 postgres ingest · 拆 mysql 为独立进程 · 改 Sync 调度。

## 3. 自测

1. `/v1/connectors/jdbc-mysql/health` 与 `/mysql/health` 同形 ✅  
2. stub 插件 probe → 501 ✅  
3. 未安装插件 → 400 PLUGIN_NOT_INSTALLED ✅  
4. 旧 mysql 用例仍过 ✅  

pytest：`test_connector_runtime_100` + `test_mysql_connector` + `test_connector_plugins_97` → **11 passed**
