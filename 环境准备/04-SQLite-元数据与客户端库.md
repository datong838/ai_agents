# 环境准备 — SQLite（元数据 DB + 客户端本地库）

> **角色**：**结构化持久化**（非向量）  
> **阶段**：**POC 必须**  
> **技术方案**：服务端 [§12](../技术方案-SalesAgent服务端.md) · 客户端 [§10](../技术方案-谛听客户端.md)

---

## 1. 双端分工

| 端 | 文件路径 | 访问层 | 主要表 |
|----|----------|--------|--------|
| **SalesAgent** | `{data_root}/salesagent.db` | Python `sqlite3` / SQLAlchemy | `demand_events`、`analyze_daily_quota`、`analyze_errors`、`niushop_sync_log`… |
| **谛听客户端** | `{data_root}/client.db` | **仅 Electron 主进程** `better-sqlite3` | `demand_events_cache`、`contacts`、`listener_stats`… |

**禁止**：Redis 做配额；Renderer 直连 SQLite。

---

## 2. 服务端 SQLite

### 2.1 路径

| 环境 | `data_root` | DB 文件 |
|------|-------------|---------|
| Windows 开发 | `C:/work/salesagent/data` | `salesagent.db` |
| Linux 生产 | `/www/wwwroot/salesagent/data` | `salesagent.db` |

`server.json#data_root` 或环境变量 `SALESAGENT_DATA_ROOT` 覆盖。

### 2.2 安装

Python 标准库 `sqlite3`，**无需额外安装**。

**环境准备验收**（编码前）：

```powershell
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

通过标准：有版本号输出、无 ImportError（本机 DESKTOP-TH91SO5：**3.50.4** ✅）。

```bash
pip install aiosqlite  # 若 FastAPI 异步封装需要（可选，Phase 1）
```

### 2.3 初始化

应用启动时执行 DDL（见技术方案 §12.1），或使用迁移脚本 `schema.sql`：

```bash
mkdir -p C:/work/salesagent/data
sqlite3 C:/work/salesagent/data/salesagent.db ".read schema.sql"
```

**WAL 模式**（推荐，与客户端一致）：

```sql
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
```

### 2.4 配额表（原子性）

`analyze_daily_quota` 使用 `BEGIN IMMEDIATE` 递增（服务端 §6、客户端 §14.1 双侧护栏）。

### 2.5 License POC

POC 用 `{data_root}/config/license_keys.json`，**不**写 `license_keys` 表；v1.0 再迁 SQLite。

---

## 3. 客户端 SQLite

### 3.1 路径

`ditingclient/config/client.json`：

```json
"local_db": {
  "sqlite_path": "{data_root}/client.db",
  "journal_mode": "WAL",
  "synchronous": "NORMAL",
  "cache_size_mb": 64
}
```

默认：`C:/work/diting/data/client.db`

### 3.2 安装（Node / Electron）

```bash
cd ditingclient
npm install better-sqlite3
```

- **原生模块**：需与 Electron 版本匹配；使用 `@electron/rebuild` 或 `electron-builder install-app-deps`。
- **仅主进程** `require('better-sqlite3')`；Renderer 经 IPC。

### 3.3 初始化

主进程启动时：

```typescript
import Database from 'better-sqlite3'
const db = new Database(sqlitePath)
db.pragma('journal_mode = WAL')
db.exec(fs.readFileSync('schema.sql', 'utf-8'))
```

### 3.4 与 WS 联动

`demand_events_cache`：WS 收到 `demand_event` 后写入，供雷达列表与离线阅读（POC **不**调服务端 `GET /api/demands`）。

---

## 4. 验收

### 服务端

```bash
sqlite3 C:/work/salesagent/data/salesagent.db ".tables"
# 应见 demand_events analyze_daily_quota 等
```

启动 SalesAgent 后 `POST /api/analyze` 成功，`demand_events` 有行。

### 客户端

Electron 启动后 `client.db` 生成；`demand_events_cache` 在 WS 推送后有数据。

```powershell
cd ditingclient
npm run verify:phase2   # 需 SalesAgent 8765 已启动
```

**本机备案（2026-06-17）**：`C:/work/diting/data/client.db` 已建表；`verify_phase2` 通过。

---

## 5. 备份

```bash
# WAL 模式下建议 checkpoint 后备份
sqlite3 salesagent.db "PRAGMA wal_checkpoint(TRUNCATE);"
cp salesagent.db salesagent.db.bak
```

---

## 6. 常见问题

| 问题 | 处理 |
|------|------|
| `better-sqlite3` 编译失败 | 安装 VS Build Tools；或用预编译 electron 对应版本 |
| database is locked | 单进程写；配额用 `BEGIN IMMEDIATE`；勿多进程写同一库 |
| 路径不存在 | 启动前 `mkdir -p data_root` |

---

## 7. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-06-16 | 初稿 |
| v1.1 | 2026-06-17 | §2.2 环境准备验收命令；本机 SQLite **3.50.4** 备案 |
| v1.2 | 2026-06-17 | §4 客户端验收：`verify_phase2` 备案 |
