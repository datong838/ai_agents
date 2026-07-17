# 环境准备 — ChromaDB 向量库

> **角色**：服务端 **向量存储与检索**（beauty 类目 collection）  
> **阶段**：**POC 必须**（依赖 [BGE-M3](03-BGE-M3-Embedding.md) 生成向量）  
> **配置**：`server.json#chroma`、`paths.category_chroma`  
> **技术方案**：[服务端 §8](../技术方案-SalesAgent服务端.md)

---

## 1. 选型说明


| 项      | 值                                                            |
| ------ | ------------------------------------------------------------ |
| 产品     | **ChromaDB** 持久化模式                                           |
| 部署形态   | **嵌入式**，无独立 Docker 服务；数据在磁盘目录                                |
| 路径     | `{data_root}/{category}/chroma/` 例：`.../data/beauty/chroma/` |
| POC 集合 | 单 collection `beauty`（商品 + 资料切片）                             |
| 内存限制   | `chroma_memory_limit_bytes = 1GB`（§8.4）                      |


---

## 2. 安装

### 2.1 Python 依赖

```powershell
cd C:\work\projects\wchat\salesagent

# 国内若 pip 卡在 grpcio/chromadb 下载，用清华源（约 1～3 分钟）
pip install "chromadb>=0.4.0" -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=120
```

> 默认 `pypi.org` 在国内常卡在 **grpcio**（几 MB 下几十分钟）。`Ctrl+C` 中断后换 `-i` 镜像重跑即可。


| **环境**       | `cd salesagent` **实际路径**            |
| ------------ | ----------------------------------- |
| **你本机开发**    | `C:\work\projects\wchat\salesagent` |
| **Linux 线上** | `/www/wwwroot/salesagent`           |

写入 `requirements.txt`：

```text
chromadb>=0.4.0
```

### 2.2 版本建议

- `pip install "chromadb>=0.4.0"` 在 2026 年会解析到 **1.x**（如 **1.5.9**），属正常，**POC 全新部署可用**。
- 文档早期写的 **0.4.x / 0.5.x** 指当时主流线；Chroma 已在 2025 年发布 **1.0+**，`PersistentClient` / `upsert` / `query` API 与本文 §3、§6 一致。
- **锁定版本**：环境准备通过后写入 `chromadb==1.5.9`（或你本机 `pip show chromadb` 的版本），开发机与 Linux 线上一致。
- **注意（1.x）**：`Settings(chroma_memory_limit_bytes=...)` 在 1.x 可能被忽略；若需严格控内存，见 Chroma 1.x 文档或 POC 阶段先靠 `upsert_batch_size` 分批（§5）。

---

## 3. 初始化代码（与线上一致）

```python
# com/yanpanji/agents/vector/chroma_store.py
import os
import chromadb
from chromadb.config import Settings

def get_chroma_client(category: str, data_root: str):
    persist_dir = os.path.join(data_root, category, "chroma")
    os.makedirs(persist_dir, exist_ok=True)

    settings = Settings(
        anonymized_telemetry=False,
        chroma_memory_limit_bytes=1024 * 1024 * 1024,
        allow_reset=os.getenv("ENV") == "development",
    )
    return chromadb.PersistentClient(path=persist_dir, settings=settings)

def get_collection(client, name: str = "beauty"):
    return client.get_or_create_collection(name=name)
```

> **注意**：`chroma_memory_limit_bytes` 需与你安装的 Chroma 版本支持情况一致；若启动报错，查该版本 `Settings` 文档并调整。

---

## 4. 目录与权限

### Windows 开发

```text
C:/work/salesagent/data/
└── beauty/
    └── chroma/          # Chroma 自动生成 sqlite 等文件
```

环境变量：`SALESAGENT_DATA_ROOT=C:/work/salesagent/data`

### Linux 生产

```text
/www/wwwroot/salesagent/data/beauty/chroma/
```

属主与 `salesagent` systemd 用户一致（如 `www`），可写。

---

## 5. Upsert 与内存（必读）

**禁止**一次性全量 upsert。必须使用 `server.json#chroma.upsert_batch_size: 50` 分片：

```python
for i in range(0, len(chunks), 50):
    batch = chunks[i : i + 50]
    collection.upsert(ids=..., embeddings=..., documents=..., metadatas=...)
```

夜间 ingest / Niushop 同步均复用此逻辑（服务端 §8.4.2、§10.2）。

---

## 6. 验收

### 6.1 写入测试向量

**方式 A — 独立脚本（推荐）**

```powershell
cd C:\work\projects\wchat\salesagent
python scripts\verify_chroma.py
```

Linux 生产：

```bash
cd /www/wwwroot/salesagent
source venv/bin/activate
python scripts/verify_chroma.py
```

期望输出：`Chroma OK: path=.../beauty/chroma, count=1`（重复执行 count 可能 ≥1）。

**方式 B — 单行（无脚本时）**

```python
import os
from chromadb.config import Settings
import chromadb

data_root = os.environ.get("SALESAGENT_DATA_ROOT", "C:/work/salesagent/data")
client = chromadb.PersistentClient(
    path=f"{data_root}/beauty/chroma",
    settings=Settings(anonymized_telemetry=False),
)
col = client.get_or_create_collection("beauty")
col.upsert(
    ids=["test_001"],
    documents=["敏感肌防晒推荐测试"],
    metadatas=[{"source": "test", "category": "beauty"}],
    embeddings=[[0.1] * 1024],  # 正式环境用 BGE-M3 维度，此处仅测连通
)
print(col.count())
```

正式 POC：embedding 维度须与 [BGE-M3](03-BGE-M3-Embedding.md) 一致（通常 **1024**）。

### 6.2 API 验收（Phase 1 后）

> **环境准备阶段（现在）**：服务端 HTTP 尚未实现，**无法执行**本节。顺序 4 以 §6.1 `verify_chroma.py` 通过即可。  
> **Phase 1 S4** 实现 `chroma_store` + `GET /api/ingest/status` 后再验收。

`GET /api/ingest/status?category=beauty` → `chunk_count >= 1`。

```powershell
# Phase 1 服务启动后（默认端口 8765）
Invoke-RestMethod "http://127.0.0.1:8765/api/ingest/status?category=beauty"
```

### 6.3 Analyze 检索（Phase 1 后）

`POST /api/analyze` 后台日志可见 top-K 命中片段。

---

## 7. 备份与迁移

```bash
# 整目录 rsync 即可（与 PRD §4.11）
rsync -avz /www/wwwroot/salesagent/data/beauty/chroma/ new-cvm:/www/wwwroot/salesagent/data/beauty/chroma/
```

---

## 8. 常见问题


| 问题            | 处理                                      |
| ------------- | --------------------------------------- |
| OOM           | 减小 batch；开 Swap（§8.4.3）；白天勿 bulk upsert |
| 维度不匹配         | upsert 的 embedding 维数须与 BGE-M3 一致       |
| Windows 路径    | 用正斜杠或 `path.join`，勿混大小写（§开发计划 1.4）      |
| collection 为空 | 先跑 BGE embed 再 upsert；或 HTTP 联调导入商品文本   |


---

## 9. 修订记录


| 版本   | 日期         | 说明  |
| ---- | ---------- | --- |
| v1.0 | 2026-06-16 | 初稿 |
| v1.1 | 2026-06-17 | §2.1 清华源；§2.2 更新为 1.x 可用说明 |
| v1.2 | 2026-06-17 | §6.1 增 `scripts/verify_chroma.py` |
| v1.3 | 2026-06-17 | §6.2/6.3 标明 Phase 1 后验收 |


