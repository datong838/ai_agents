# 环境准备 — BGE-M3 Embedding

> **角色**：文本 **向量化**（analyze 检索 + ingest 入库）  
> **阶段**：**POC 必须**（先于 Chroma 写入）  
> **配置**：`server.json#embedding`  
> **技术方案**：[服务端 §8.3](../技术方案-SalesAgent服务端.md)

---

## 1. 选型说明

| 项 | 值 |
|----|-----|
| 模型 | **BAAI/bge-m3**（BGE-M3） |
| 设备 | **CPU**（`embedding.device: cpu`） |
| 库 | `FlagEmbedding` 或 `sentence-transformers`（二选一，项目内统一） |
| 切块 | `chunk_size: 500`，`overlap: 50` |
| 批量 | `batch_size: 8`（2GB 机器默认） |

---

## 2. 安装

### 2.1 依赖

```powershell
# 方式 A：分两步（推荐，避免 --index-url 覆盖 PyPI）
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install "FlagEmbedding>=1.2.0"

# 方式 B：一条命令（须用 extra-index-url，不能用 index-url）
pip install FlagEmbedding torch --extra-index-url https://download.pytorch.org/whl/cpu

# 方式 C：sentence-transformers（torch 走 PyPI，体积可能更大）
pip install sentence-transformers
```

> `--index-url` 会**只**查 PyTorch 源，找不到 PyPI 上的 `FlagEmbedding`；CPU 版 torch 用上面 A/B，勿写成 `--index-url` 装两个包。

**Linux 生产（venv 内，与 systemd `WorkingDirectory` 一致）**

```bash
cd /www/wwwroot/salesagent
python3.11 -m venv venv          # 首次；已有 venv 则跳过
source venv/bin/activate
pip install -U pip
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install "FlagEmbedding>=1.2.0"
```

`requirements.txt` 示例：

```text
FlagEmbedding>=1.2.0
torch
```

### 2.2 模型下载

首次运行 `BGEM3FlagModel("BAAI/bge-m3", ...)` 会**自动**从 HuggingFace 拉取权重（约 **2GB+**）。

> **常见误解**：`{data_root}/models/bge-m3/` 只是**可选**的落盘目录，**不会**因为建了空文件夹就自动有文件；也**不是**默认下载位置。  
> 默认缓存：`%USERPROFILE%\.cache\huggingface\hub\`（Linux：`~/.cache/huggingface/hub/`）。

**国内加速**（自动/手动下载均建议）：

```powershell
# Windows PowerShell
$env:HF_ENDPOINT="https://hf-mirror.com"
```

```bash
# Linux bash
export HF_ENDPOINT=https://hf-mirror.com
```

#### 2.2.1 自动下载（推荐）

国内 **hf-mirror** 上，`verify_bge.py` 直接拉全量仓库可能因 `imgs/.DS_Store` 返回 **403** 失败（FlagEmbedding 无法跳过该文件）。  
**推荐**：先用 `download_bge_m3.py` 跳过无关文件，再验收。

**Windows 开发机**

```powershell
cd C:\work\projects\wchat\salesagent
$env:HF_ENDPOINT="https://hf-mirror.com"
python scripts\download_bge_m3.py
$env:BGE_MODEL_PATH="C:/work/salesagent/data/models/bge-m3"
python scripts\verify_bge.py
```

**Linux 线上**

```bash
cd /www/wwwroot/salesagent
export HF_ENDPOINT=https://hf-mirror.com
source venv/bin/activate
export BGE_MODEL_PATH=/www/wwwroot/salesagent/data/models/bge-m3
python scripts/download_bge_m3.py
python scripts/verify_bge.py
```

- 首次约 **2GB+**（PyTorch 权重 `pytorch_model.bin` 或 `model.safetensors`，已排除 `onnx/` 目录）。
- **期望输出**：`BGE-M3 OK: dim=1024`。

仍想走 HuggingFace 默认缓存（不落到 `data/models`）时，可直连官方源或海外机执行 `python scripts/verify_bge.py`；国内镜像建议用上表两步法。

**前置条件（Linux 线上，首次部署）**

```bash
cd /www/wwwroot/salesagent
python3.11 -m venv venv                    # 尚无 venv 时
source venv/bin/activate
pip install -U pip
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install "FlagEmbedding>=1.2.0"
# 代码需已发布到本目录（含 scripts/download_bge_m3.py、scripts/verify_bge.py）
```

**步骤 1 — 下载（跳过 onnx/imgs/.DS_Store）**

```bash
cd /www/wwwroot/salesagent
export HF_ENDPOINT=https://hf-mirror.com
export BGE_MODEL_PATH=/www/wwwroot/salesagent/data/models/bge-m3
source venv/bin/activate
python scripts/download_bge_m3.py
```

**步骤 2 — 验收**

```bash
python scripts/verify_bge.py
```

未 `activate` 时：

```bash
cd /www/wwwroot/salesagent
export HF_ENDPOINT=https://hf-mirror.com
export BGE_MODEL_PATH=/www/wwwroot/salesagent/data/models/bge-m3
./venv/bin/python scripts/download_bge_m3.py
./venv/bin/python scripts/verify_bge.py
```

- 首次约 **2GB+** 下载，视带宽需 **数分钟～十几分钟**。
- **期望输出**：`BGE-M3 OK: dim=1024`。

海外服务器可省略 `HF_ENDPOINT`，直连 HuggingFace。

**步骤 3 — 核对落盘（可选）**

```bash
ls -lh /www/wwwroot/salesagent/data/models/bge-m3/pytorch_model.bin
# 或 model.safetensors（视镜像/版本而定）
```

**步骤 4 — 仅 import 探活（不下载权重，可选）**

依赖装好后、下载前可先测：

```bash
cd /www/wwwroot/salesagent
source venv/bin/activate
python -c "from FlagEmbedding import BGEM3FlagModel; print('import ok')"
```

期望：`import ok`。

---

**Windows 开发机（对照，见上文「Windows 开发机」代码块）**

下载完成后可在资源管理器打开 `C:\work\salesagent\data\models\bge-m3\` 核对 `pytorch_model.bin`（约 2.2GB）或 `model.safetensors`。

#### 2.2.2 手动下载到 `data_root`（离线 / 线上可控路径）

若希望权重落在项目 `data_root`（便于备份、与 Linux 路径对称），需**显式执行**下载命令：

**Windows（PowerShell）**

```powershell
$env:HF_ENDPOINT="https://hf-mirror.com"
pip install -U "huggingface_hub[cli]"
python scripts\download_bge_m3.py
# 或 CLI（须排除无关文件）：
huggingface-cli download BAAI/bge-m3 --local-dir C:/work/salesagent/data/models/bge-m3 --exclude "onnx/*" "imgs/*" "**/.DS_Store" "*.jpg"
```

**Linux 生产**

```bash
export HF_ENDPOINT=https://hf-mirror.com
source /www/wwwroot/salesagent/venv/bin/activate
export BGE_MODEL_PATH=/www/wwwroot/salesagent/data/models/bge-m3
python scripts/download_bge_m3.py
```

下载成功后，目录内应有 `config.json`、`tokenizer.json`、`model.safetensors`（或 `pytorch_model.bin`）等文件，**不再是空文件夹**。

浏览器手动下：打开 [hf-mirror.com/BAAI/bge-m3](https://hf-mirror.com/BAAI/bge-m3) → Files → 逐个下载到上述目录（不推荐，文件多且易漏）。

#### 2.2.3 使用本地路径加载

手动落盘后，把模型 id 换成本地目录（正斜杠路径更稳）：

```python
model = BGEM3FlagModel(
    "C:/work/salesagent/data/models/bge-m3",
    use_fp16=False,
    device="cpu",
)
```

验收脚本同理可改路径，或设置环境变量后执行（见 `verify_bge.py` 内 `BGE_MODEL_PATH`）。

路径约定：

```text
{data_root}/models/bge-m3/     # 开发：C:/work/salesagent/data/models/bge-m3/
                               # 生产：/www/wwwroot/salesagent/data/models/bge-m3/
```

---

## 3. 加载示例

### 方案 A：FlagEmbedding（推荐，与 BGE 官方一致）

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=False, device="cpu")

def embed_texts(texts: list[str]) -> list[list[float]]:
    out = model.encode(texts, batch_size=8, max_length=512)
    return out["dense_vecs"].tolist()  # 或按 API 版本取 dense embedding
```

### 方案 B：sentence-transformers

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3", device="cpu")

def embed_texts(texts: list[str]) -> list[list[float]]:
    return model.encode(texts, batch_size=8, normalize_embeddings=True).tolist()
```

**维度**：dense 向量一般为 **1024**；写入 Chroma 前确认与 collection 一致。

---

## 4. 与 Chroma 串联

```python
texts = ["商品【防晒霜】适合敏感肌..."]
embeddings = embed_texts(texts)
collection.upsert(
    ids=["chk_001"],
    documents=texts,
    embeddings=embeddings,
    metadatas=[{"source": "user_excel", "category": "beauty"}],
)
```

Analyze 时：对用户消息做 `embed_query` → `collection.query(query_embeddings=..., n_results=5)`。

---

## 5. 资源占用

| 环境 | 说明 |
|------|------|
| Windows 开发（30GB） | 可 `batch_size=16` 调试 |
| Linux 2GB 生产 | **batch_size=8**；与 Chroma、Uvicorn 共存时注意内存 |

---

## 6. 验收

> **工作目录**：开发 `cd` 到 monorepo 内 `salesagent/`；线上 `cd /www/wwwroot/salesagent`（`WorkingDirectory` 与线上一致）。  
> **Python**：线上用 **3.11/3.12 venv**（`venv/bin/python`）；本机若为 3.14，import 探活须预加载（见 6.1）。

### 6.1 快速探活（仅 import，不加载模型权重）

依赖已 `pip install` 后，先确认包能 import（约 10 秒）。

**Windows（PowerShell）**

```powershell
cd C:\work\projects\wchat\salesagent
python -c "import sklearn,pandas,pyarrow; from FlagEmbedding import BGEM3FlagModel; print('import ok')"
```

**Linux 生产（bash）**

```bash
cd /www/wwwroot/salesagent
source venv/bin/activate
python -c "import sklearn,pandas,pyarrow; from FlagEmbedding import BGEM3FlagModel; print('import ok')"
```

期望输出：`import ok`。

> **Python 3.14（仅开发机）**：若省略 `sklearn,pandas,pyarrow` 预加载，可能**无输出、无报错**直接回到提示符（pyarrow 导入顺序崩溃）。线上 3.11/3.12 一般可直接 `from FlagEmbedding import BGEM3FlagModel`。

### 6.2 完整验收（加载模型 + encode）

首次会下载 `BAAI/bge-m3`（约 **2GB+**），国内建议设 HuggingFace 镜像。

**方式 A — 独立脚本（推荐）**

Windows：

```powershell
cd C:\work\projects\wchat\salesagent
$env:HF_ENDPOINT="https://hf-mirror.com"
python scripts\verify_bge.py
```

Linux 生产：

```bash
cd /www/wwwroot/salesagent
export HF_ENDPOINT=https://hf-mirror.com   # 国内 CVM 建议；海外可省略
source venv/bin/activate
python scripts/verify_bge.py
```

未激活 venv 时也可：

```bash
cd /www/wwwroot/salesagent
export HF_ENDPOINT=https://hf-mirror.com
./venv/bin/python scripts/verify_bge.py
```

期望输出：`BGE-M3 OK: dim=1024`。

**方式 B — 单行（无脚本时）**

Windows：

```powershell
cd C:\work\projects\wchat\salesagent
$env:HF_ENDPOINT="https://hf-mirror.com"
python -c "import sklearn,pandas,pyarrow; from FlagEmbedding import BGEM3FlagModel; m=BGEM3FlagModel('BAAI/bge-m3', use_fp16=False, device='cpu'); v=m.encode(['测试'], batch_size=1); print('ok', len(v['dense_vecs'][0]))"
```

Linux：

```bash
cd /www/wwwroot/salesagent
export HF_ENDPOINT=https://hf-mirror.com
./venv/bin/python -c "from FlagEmbedding import BGEM3FlagModel; m=BGEM3FlagModel('BAAI/bge-m3', use_fp16=False, device='cpu'); v=m.encode(['测试'], batch_size=1); print('ok', len(v['dense_vecs'][0]))"
```

期望输出：`ok 1024`。

### 6.3 模型路径核对

| 方式 | 路径 | 何时出现文件 |
|------|------|----------------|
| **默认（自动下载）** | `%USERPROFILE%\.cache\huggingface\hub\` | 跑完 §6.2 验收后 |
| **手动落盘（可选）** | `C:/work/salesagent/data/models/bge-m3/` | 执行 §2.2.2 `huggingface-cli download` 后 |

使用本地落盘路径验收：

```powershell
$env:HF_ENDPOINT="https://hf-mirror.com"
$env:BGE_MODEL_PATH="C:/work/salesagent/data/models/bge-m3"
python scripts\verify_bge.py
```

线上验收通过后，可继续 [02-ChromaDB](02-ChromaDB.md)（顺序 4）。

---

## 7. 常见问题

| 问题 | 处理 |
|------|------|
| 下载超时 | 设 `HF_ENDPOINT` 镜像；或按 §2.2.2 `huggingface-cli download` 落到 `models/bge-m3` |
| `models/bge-m3` 文件夹是空的 | 正常：空目录不会自动下载；跑 `download_bge_m3.py` 或 §2.2.1 |
| hf-mirror **403** `.DS_Store` | 勿直接 `verify_bge.py` 拉全仓；用 `scripts/download_bge_m3.py`（跳过 `imgs/`、`onnx/`） |
| Windows symlink 警告 | 可忽略；或开「开发人员模式」；或设 `HF_HUB_DISABLE_SYMLINKS_WARNING=1` |
| `No matching distribution found for FlagEmbedding` | 勿用 `--index-url` 同时装两包；先装 CPU 版 `torch`，再 `pip install FlagEmbedding` |
| torch CPU 版 | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| 编码慢 | POC 可接受；仅夜间大批量 ingest |
| `import` 无输出、直接回到提示符 | Python 3.14 + pyarrow 导入顺序问题；用 `scripts/verify_bge.py` 或预加载 `sklearn,pandas,pyarrow` |

---

## 8. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-06-16 | 初稿 |
| v1.1 | 2026-06-17 | §2.1 修正 pip：`--index-url` → 分步或 `--extra-index-url` |
| v1.2 | 2026-06-17 | §6 增 `verify_bge.py`；Python 3.14 import 顺序说明 |
| v1.3 | 2026-06-17 | §6 拆分为探活/完整验收；补 Linux 线上命令 |
| v1.4 | 2026-06-17 | §2.1 补 Linux venv 安装步骤 |
| v1.5 | 2026-06-17 | §2.2 拆自动/手动下载；澄清 `models/bge-m3` 非默认缓存 |
| v1.6 | 2026-06-17 | §2.2.1 补 Linux 线上自动下载与验收全流程 |
| v1.7 | 2026-06-17 | 增 `download_bge_m3.py`；修复 hf-mirror 403 `.DS_Store` |
| v1.8 | 2026-06-17 | `download_bge_m3.py` 同时认可 `pytorch_model.bin` 权重 |
