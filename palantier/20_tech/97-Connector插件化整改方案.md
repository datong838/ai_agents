# 97 · Connector 插件化整改（对齐 20 §3.1）

> **版本**：v1.0 · 2026-07-19  
> **状态**：✅ 已落地 · 自测通过  
> **强制对齐**：[20 §3.1](20-AOS整体技术方案.md) · [T05 §3](T05-L1数据集成详细技术方案.md) · 对标 [83](83-LLM-Provider插件化整改方案.md)  
> **Rules**：军规优先 · 先方案后编码 · 最小更改 · 不把 Airbyte monorepo 当产品

---

## 1. 问题

| 现状 | §3.1 / T05 要求 |
| --- | --- |
| 仓库无 `plugins/connectors/` | 每种连接器 = 插件包 + manifest |
| `/v1/sources` 内存字典，任意 type 字符串 | Host 只认已安装插件 |
| DataPage 硬编码 `file` / `jdbc` 两卡 | 扫描注册表 · 可安装扩展 |
| MySQL 运行时写死在 `mysql_connector.py` | **本刀保留运行时**；插件声明能力与健康面，不拆内核 |

**本刀不做：** 真 Sync 调度重写 · Vault 轮换 · 200+ 连接器 · Widget 插件 · 把解析器 extract 全改边车（解析器仅补 manifest 落点，另刀深改）。

---

## 2. 目标

1. `aos-platform/plugins/connectors/<id>/manifest.json` 首批落地（T05 §3.3）  
2. `connector_registry`：磁盘扫描 · install/uninstall · KV 持久化  
3. API：`GET/POST …/connector-plugins`  
4. `POST /v1/sources`：type 必须为已安装插件（兼容旧别名 `file`/`jdbc`）  
5. DataPage 向导：连接器卡来自注册表；未安装可一键安装  

---

## 3. 首批插件（T05 §3.3）

| id | 状态 | 说明 |
| --- | --- | --- |
| `file-local` | 必做 · 默认已装 | 本地/上传文件 |
| `file-object-store` | 必做 · 默认已装 | S3 兼容对象仓 |
| `jdbc-mysql` | 必做 · 默认已装 | 对接既有 `/v1/connectors/mysql/*` |
| `jdbc-postgres` | 鼓励 | 可装；运行时本刀 stub health |
| `jdbc-sqlserver` | 鼓励 | 同上 |
| `rest-generic` | 鼓励 | HTTP 源占位 |

兼容别名：`file`→`file-local` · `jdbc`→`jdbc-mysql`。

---

## 4. 契约

```text
GET  /v1/connector-plugins
POST /v1/connector-plugins/{id}/install
POST /v1/connector-plugins/{id}/uninstall

POST /v1/sources  { id, type }  # type = 插件 id 或别名；未安装 → 400 PLUGIN_NOT_INSTALLED
```

manifest 最低字段：`id · version · kind · nameZh · capabilities · configSchema · healthPath?`

---

## 5. 文件

| 路径 | 变更 |
| --- | --- |
| `plugins/connectors/*/manifest.json` | 新建 |
| `aos_api/connector_registry.py` | 新建 |
| `wave_ext.py` | 插件 API · sources 校验 |
| `DataPage.tsx` | 注册表驱动选型 |
| 本文 + `00` 索引 | 登记 |

---

## 6. 自测

1. GET connector-plugins ≥6 · 必做三者 `installed=true` ✅  
2. uninstall jdbc-postgres 后再 install 成功 ✅  
3. sources type=`jdbc-mysql` 200；未安装插件 type → 400 ✅  
4. 别名 `file` / `jdbc` 仍可建源 ✅  

pytest：`test_connector_plugins_97` + `test_syncs_and_datasets` → **5 passed**

---

## 7. 风险

| 风险 | 处理 |
| --- | --- |
| 破坏已有 file/jdbc 源 | 别名归一 + 必做默认已装 |
| 误以为 postgres 已可 ingest | manifest `runtime:"stub"` · UI 诚实提示 |
