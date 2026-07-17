# M2-2 — VLM 图片描述：本地化部署与使用（Runbook）

> **阶段**：MVP M2-2（知识网增强层）  
> **原方案模型**：Qwen2-VL-2B-Instruct-GPTQ-Int4（CPU Int4）— **已暂停，不再推进**（见 §零）  
> **原则**：**增量增强**，只给尚无 `vlm_description` 的媒体节点补描述；**不**清空重同步知识库。  
> **关联**：[知识库-结构化入库方案.md](知识库-结构化入库方案.md) §6、§8、§13.4；[06-Qwen2-VL-Int4.md](环境准备/06-Qwen2-VL-Int4.md)；[技术方案-SalesAgent服务端.md](技术方案-SalesAgent服务端.md) §9.3

---

## 零、方案状态与暂停说明（2026-06）

> **结论**：原定的 **Qwen2-VL-2B-Instruct-GPTQ-Int4 + CPU 本地推理** 方案**已验证不可行**，M2-2 **暂停按此路径上线**；`vlm_description` 仍全 NULL，待新方案定稿后切换。  
> 下文 §三–§七 中关于 2B Int4 的安装/配置/验收内容**保留作历史记录**，新方案确定后会增补或替换对应章节。

### 0.1 暂停原因（实测 + 能力评估）

| 维度 | 结论 |
| --- | --- |
| **性能** | Windows 本地 CPU + GPTQ Int4，单图推理 **约 15–40 分钟/张**（无 CUDA/Exllama 内核，`disable_exllama=True`）；开发验收与夜间批补均**基本不可用** |
| **工程** | Python 3.14 无法正确加载 GPTQ 权重；Windows 需 **Python 3.11 + transformers 4.45.2 + auto-gptq** 方能出现 `QuantLinear`，环境割裂 |
| **效果** | **2B Int4** 识图能力偏弱：实验可靠性低，难以区分「知识库不够」还是「模型看不懂图」 |
| **生产** | 2GB 独占 CVM 同样无 GPU，预期与本地 CPU 同类问题；原「50 张/夜」假设不成立 |

### 0.2 替代模型选型参考（「看懂题」前提）

先做实验 / 批补描述时，按识图能力与运维成本粗选（**新方案待产品确认**）：

| 模型 / 路径 | 做 VLM 批补 / 实验的可行性 | 说明 |
| --- | --- | --- |
| **2B Int4 CPU（原方案）** | ❌ **绝对不行** | 太慢 + 识图弱；已停用 |
| **7B Int4 本地** | ⚠️ **勉强可用，有噪声** | 印刷体、常规商品图可读；几何/坐标类精细读错约 **~5%**，可能污染描述质量 |
| **Qwen2.5-VL-7B / 72B 本地** | ✅ **实验级可用** | 72B 基本不看错题；2.5 系 7B 明显强于旧版 2B；需相应算力（GPU 或大内存），非 2GB CVM |
| **API 调用大模型（最推荐待评）** | ✅ **优先评估** | 如阿里云百炼 **`qwen-vl-max`**、**`qwen2.5-vl-72b-instruct`** 等：按量付费、免维护 GPU、识图最强；需单独评估**数据合规**（商品图是否允许出域）与成本 |

### 0.3 代码与配置现状

| 项 | 状态 |
| --- | --- |
| `ingest/vlm.py`、`knowledge/vlm_enrich.py`、`cli vlm_enrich` | 已按 2B Int4 骨架实现，**随本方案一并冻结** |
| `server.json` `vlm.enabled` / `vlm_enrich.enabled` | 建议保持 **`false`** 直至新方案落地 |
| `knowledge_media_nodes.vlm_description` | 仍为 NULL，不影响 M2-1 图检索与其它链路 |

### 0.4 后续文档约定

- **v2 已定稿**：见 **[M2-2-媒体图片描述-元宝技能方案.md](M2-2-媒体图片描述-元宝技能方案.md)**（谛听技能集 + 本机元宝桌面客户端，替代 2B CPU）。  
- 下文 §三–§七 保留作 **2B Int4 历史记录**，勿再按此部署。  
- 若将来再评估 **API 批补**（百炼 `qwen-vl-max` 等）：可另开 M2-2c，与元宝技能并行选型。

---

## 一、文档目的

说明从 **本机/线上算力准备 → 模型部署 → 配置 → 夜间批处理 → 验收** 的全流程，使 Niushop 知识网中 **303 个全局媒体节点**（beauty 类目当前规模）逐步获得 `vlm_description`，并回写 `knowledge_media_{hash}` 向量 chunk，供 Analyze / 技能集选图使用。

**与谛听客户端 PaddleOCR 的边界**：微信聊天截图 OCR 在客户端；**商品详情图 / 知识库上传图** 在 SalesAgent 用 Qwen-VL（本文范围）。

---

## 二、M2-2 在知识网中的位置

### 2.1 当前状态（M1.6 已交付）


| 项                                     | 状态                                   |
| ------------------------------------- | ------------------------------------ |
| `knowledge_media_nodes`               | ✅ 303 节点（URL 去重）                     |
| `knowledge_edges`                     | ✅ contains / appears_in / references |
| `knowledge_media_{hash}` Chroma chunk | ✅ 含 URL + 上下文摘录                      |
| `vlm_description`                     | ❌ **均为 NULL**（待 M2-2 填充）             |


### 2.2 M2-2 做什么（增量 UPDATE）

```text
SELECT media_node WHERE vlm_description IS NULL
    → 下载图片（CDN URL → 临时文件）
    → Qwen-VL 生成中文场景描述
    → UPDATE knowledge_media_nodes.vlm_description
    → 重建 knowledge_media_{hash} 文本（模板 §6.3）
    → BGE embed 单条 upsert Chroma（不碰 contains/appears_in 边）
    → 写 vlm_enrich_log（按 url_hash 幂等）
```

**不会**：重跑 `sync_niushop --force`、删除图边、重建商品 section chunk。

### 2.3 写入字段与 chunk 模板

**SQLite** `knowledge_media_nodes`：


| 字段                | M2-2 写入                      |
| ----------------- | ---------------------------- |
| `vlm_description` | ✅ 主输出                        |
| `ocr_text`        | 可选（VLM 顺带读出图内大字，或后续 OCR）     |
| `use_cases`       | 可选（规则/LLM 标签：成分表 / 包装 / 步骤…） |


**Chroma** 媒体 chunk 文本（与 [知识库方案 §6.3](知识库-结构化入库方案.md) 对齐）：

```text
【全局媒体】图片
图片地址：https://yanpanji.com/upload/...
出现于：399白钻逆龄双效王炸套装、…
上下文摘录：
- …
场景描述：{vlm_description}
适用场景：{use_cases}
```

---

## 三、算力方案选型（基于自有算力）

> ⚠️ **本章为原 2B Int4 方案记录**；该路径已暂停，见 **§零**。勿再按本章在本地/2GB CVM 部署 2B GPTQ。

### 3.1 两档部署（原方案，已暂停）


| 档位          | 典型环境                     | 模型              | 运行窗口        | 说明                            |
| ----------- | ------------------------ | --------------- | ----------- | ----------------------------- |
| **A 生产/线上** | 2GB 独占 CVM + 2GB Swap    | **GPTQ Int4 仅** | 22:00–06:00 | `server.json` 默认；与 analyze 错峰 |
| **B 本地开发**  | Windows 16GB+ / 30GB 工作站 | I与线上一致          | 可放宽         | 验收 M2-2；**禁止**把 FP16 配置推到生产   |


### 3.2 资源占用（Int4 CPU）


| 阶段          | RSS 约                                  |
| ----------- | -------------------------------------- |
| 模型加载        | ~1.4 GB                                |
| 单图推理        | ~1.6–1.8 GB 峰值                         |
| 与 BGE-M3 同机 | **勿并发**；VLM 批处理期间避免全量 sync / 大批量 embed |


### 3.3 处理规模与耗时（beauty 303 图）


| 假设          | 值                                |
| ----------- | -------------------------------- |
| 待处理         | ~303 张（首次全补）                     |
| 单图 CPU Int4 | ~~15–40 s/张~~ **实测 15–40 min/张**（原估算错误；已停用） |
| nightly 限额  | `max_vlm_images_per_day: 50`（默认） |
| 首次跑完        | 约 **6–7 个夜间窗口**（50 张/夜）          |


开发机可临时提高限额或连续跑批，见 §7.3。

---

## 四、环境准备（逐步）

### 4.1 目录约定

```text
C:/work/salesagent/data/                    # SALESAGENT_DATA_ROOT（本地）
├── models/
│   └── Qwen2-VL-2B-Instruct-GPTQ-Int4/   # 模型权重
├── beauty/
│   └── chroma/                           # 向量库（勿在 VLM 高峰 bulk 写）
└── salesagent.db                         # knowledge_media_nodes

/www/wwwroot/salesagent/models/...          # Linux 生产（server.json 默认 path）
```

### 4.2 模型下载

**国内镜像（推荐）**：

```powershell
$env:HF_ENDPOINT = "https://hf-mirror.com"
pip install huggingface_hub

# Windows：Scripts 可能不在 PATH，任选其一
# 方式 A（推荐）：hf 新 CLI
$env:Path += ";$env:APPDATA\Python\Python314\Scripts"
hf download Qwen/Qwen2-VL-2B-Instruct-GPTQ-Int4 `
  --local-dir C:/work/salesagent/data/models/Qwen2-VL-2B-Instruct-GPTQ-Int4

# 方式 B：Python API（不依赖 PATH）
python -c "import os; os.environ['HF_ENDPOINT']='https://hf-mirror.com'; from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen2-VL-2B-Instruct-GPTQ-Int4', local_dir=r'C:/work/salesagent/data/models/Qwen2-VL-2B-Instruct-GPTQ-Int4')"
```

> **注意**：`huggingface_hub` ≥1.19 已弃用 `huggingface-cli`，请用 **`hf download`**。若提示找不到命令，用上面 `$env:Path += ...` 或方式 B。

**校验**：目录含 `config.json`、GPTQ 权重、`tokenizer`；`config.json` 内应有 `quantization_config`。

### 4.3 Python 依赖（VLM 专用 Python 3.11）

> **重要**：SalesAgent API 可继续用 Python 3.14；**VLM 推理必须 Python 3.11**（GPTQ 权重在 3.14/gptqmodel 下无法正确加载）。  
> 快捷脚本：`salesagent/scripts/run_vlm_py311.ps1`

在 **Python 3.11** 环境（`py -3.11` 或 `C:\Users\...\Python311\python.exe`）：

```powershell
cd C:\work\projects\wchat\salesagent

# 1) PyTorch CPU
py -3.11 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 2) 与 Qwen2-VL GPTQ 权重 key 对齐的 transformers 4.45.x
py -3.11 -m pip install "transformers==4.45.2" accelerate pillow qwen-vl-utils python-dotenv

# 3) auto-gptq + optimum 1.23.x（勿用 optimum 2.x + gptqmodel 混装）
py -3.11 -m pip install "peft==0.13.2" auto-gptq "optimum==1.23.3"

# 4) 批处理 / 验收还需（与 BGE 共用）
py -3.11 -m pip install chromadb FlagEmbedding pymysql
```

**Windows 常见报错与处理**：

| 报错 | 原因 | 处理 |
| --- | --- | --- |
| `No module named 'torch'`（装 auto-gptq 时） | pip 构建隔离环境里没有 torch | 先装 torch；`pip install auto-gptq --no-build-isolation` |
| `layer_type=Linear` / 输出乱码 | Py3.14 或 transformers 5.x / gptqmodel | **改用 Python 3.11 + transformers 4.45.2 + auto-gptq** |
| `cannot import name 'no_init_weights'` | transformers 5.x | `pip install transformers==4.45.2` |
| CPU 推理极慢（10–30 分钟/张） | GPTQ Int4 无 CUDA 内核 | 正常；缩小 `max_pixels`；本地 `--limit 1` 验收 |

**安装后自检**：

```powershell
py -3.11 scripts/_vlm_autogptq_test.py
# 期望：layer_type=QuantLinear has_qweight=True，RESULT 含中文
```

> 版本以 [Qwen2-VL 官方 README](https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct-GPTQ-Int4) 为准；安装后建议 `pip freeze > requirements-vlm.txt` 固化。

### 4.4 配置 `server.json`

VLM 相关配置分 **本地开发** 与 **线上生产** 两版；仓库内 `salesagent/config/server.json` 默认保留 **本地** 值，上线时在 CVM 上覆盖或改生产文件（**勿把 `night_batch_only: false` 推到生产**）。

#### 4.4.1 本地开发

`salesagent/config/server.json` 或 `config/profiles/local_dev.json` 覆盖：

```json
{
  "data_root": "C:/work/salesagent/data",
  "deployment": {
    "topology": "local_dev",
    "vlm_daytime_allowed": false,
    "embedding_device": "cpu"
  },
  "models": {
    "qwen_vl": {
      "path": "C:/work/salesagent/data/models/Qwen2-VL-2B-Instruct-GPTQ-Int4",
      "device": "cpu",
      "dtype": "float32",
      "loader": "gptqmodel"
    }
  },
  "vlm": {
    "enabled": true,
    "model": "Qwen2-VL-2B-Instruct-GPTQ-Int4",
    "model_path_ref": "models.qwen_vl.path",
    "loader_ref": "models.qwen_vl.loader",
    "quantization": "gptq-int4",
    "night_batch_only": false,
    "scope": "night_ingest_only"
  },
  "cost_guardrails": {
    "max_vlm_images_per_day": 50
  },
  "scheduler": {
    "heavy_tasks_window": {
      "start": "22:00",
      "end": "06:00",
      "timezone": "Asia/Shanghai"
    },
    "ingest_flush_cron": "0 22 * * *"
  },
  "knowledge_graph": {
    "vlm_enrich": {
      "enabled": true,
      "category": "beauty",
      "only_null_description": true,
      "max_images_per_run": 50,
      "max_images_per_goods": 5,
      "download_timeout_sec": 30,
      "prompt_template": "beauty_product_v1"
    }
  }
}
```

`.env`（本地，与 `data_root` 一致）：

```bash
SALESAGENT_DATA_ROOT=C:/work/salesagent/data
SALESAGENT_TOPOLOGY=local_dev
HF_ENDPOINT=https://hf-mirror.com
```

#### 4.4.2 线上生产（Linux 独立 CVM）

部署根目录 `/www/wwwroot/salesagent`；模型与数据分目录存放：

```text
/www/wwwroot/salesagent/
├── config/server.json          # 或生产专用 server.prod.json
├── .env                        # 密钥 + 路径覆盖
├── models/
│   └── Qwen2-VL-2B-Instruct-GPTQ-Int4/
└── data/
    ├── salesagent.db
    └── beauty/chroma/
```

**`server.json` 片段（VLM + 相关项）**：

```json
{
  "data_root": "/www/wwwroot/salesagent/data",
  "deployment": {
    "topology": "dedicated_sales_agent",
    "vlm_daytime_allowed": false,
    "embedding_device": "cpu"
  },
  "models": {
    "qwen_vl": {
      "path": "/www/wwwroot/salesagent/models/Qwen2-VL-2B-Instruct-GPTQ-Int4",
      "device": "cpu",
      "dtype": "float32",
      "loader": "gptqmodel"
    }
  },
  "vlm": {
    "enabled": true,
    "model": "Qwen2-VL-2B-Instruct-GPTQ-Int4",
    "model_path_ref": "models.qwen_vl.path",
    "loader_ref": "models.qwen_vl.loader",
    "quantization": "gptq-int4",
    "night_batch_only": true,
    "scope": "night_ingest_only"
  },
  "cost_guardrails": {
    "max_vlm_images_per_day": 50
  },
  "scheduler": {
    "heavy_tasks_window": {
      "start": "22:00",
      "end": "06:00",
      "timezone": "Asia/Shanghai"
    },
    "ingest_flush_cron": "0 22 * * *",
    "niushop_sync_cron": "0 2 * * *"
  },
  "niushop": {
    "mysql": {
      "active_profile": "production_dedicated"
    }
  },
  "knowledge_graph": {
    "vlm_enrich": {
      "enabled": true,
      "category": "beauty",
      "only_null_description": true,
      "max_images_per_run": 50,
      "max_images_per_goods": 5,
      "download_timeout_sec": 30,
      "prompt_template": "beauty_product_v1"
    }
  }
}
```

**`.env`（生产 CVM）**：

```bash
SALESAGENT_DATA_ROOT=/www/wwwroot/salesagent/data
SALESAGENT_TOPOLOGY=dedicated_sales_agent
DEEPSEEK_API_KEY=sk-...
NIUSHOP_MYSQL_HOST=10.x.x.x          # 商城 CVM 内网 IP
NIUSHOP_DB_USER=recommend_ro
NIUSHOP_DB_PASSWORD=...
# 可选：BGE 本地路径
BGE_MODEL_PATH=/www/wwwroot/salesagent/data/models/bge-m3
```

**Cron（与 §6.1 一致）**：

```cron
5 22 * * * cd /www/wwwroot/salesagent && PYTHONPATH=src \
  python -m com.yanpanji.agents.cli vlm_enrich --category beauty >> logs/vlm_enrich.log 2>&1
```

#### 4.4.3 本地 vs 生产差异速查

| 配置项 | 本地开发 | 线上生产 |
| --- | --- | --- |
| `data_root` | `C:/work/salesagent/data` | `/www/wwwroot/salesagent/data` |
| `deployment.topology` | `local_dev` | `dedicated_sales_agent` |
| `models.qwen_vl.path` | `C:/work/.../models/Qwen2-VL-...` | `/www/wwwroot/salesagent/models/Qwen2-VL-...` |
| `models.qwen_vl.loader` | `gptqmodel` | `gptqmodel`（Linux 亦推荐，勿用已弃用 auto-gptq） |
| `vlm.night_batch_only` | **`false`**（随时实验） | **`true`**（仅 22:00–06:00） |
| `niushop.mysql.active_profile` | `local_dev`（SSH 隧道 13306） | `production_dedicated`（内网 MySQL） |
| Python 依赖 | §4.3 Windows 顺序 | 同 §4.3；建议 **Python 3.11 venv**，`pip freeze` 固化 |

**上线自检**：

```bash
cd /www/wwwroot/salesagent && PYTHONPATH=src python -c "
from com.yanpanji.agents.core.config_loader import load_config
from pathlib import Path
c = load_config()
p = Path(c.server['models']['qwen_vl']['path'])
assert p.is_dir(), p
assert c.server['vlm']['night_batch_only'] is True
print('prod VLM config OK', c.data_root, c.topology)
"
```


| 配置项                                                | 含义                                                                                    |
| -------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `vlm.enabled`                                      | 总开关                                                                                   |
| `**vlm.night_batch_only**`                         | `**true`（默认/上线）**：仅 `heavy_tasks_window` 内可跑 `vlm_enrich`；`**false`（本地开发）**：不限时段，随时实验 |
| `scheduler.heavy_tasks_window`                     | 夜间窗口（默认 22:00–06:00 Asia/Shanghai）；仅 `night_batch_only=true` 时生效                      |
| `deployment.vlm_daytime_allowed`                   | 历史项；**禁止**实时 analyze 调 VLM；与批补开关无关                                                    |
| `cost_guardrails.max_vlm_images_per_day`           | 每日配额（SQLite 计数）                                                                       |
| `knowledge_graph.vlm_enrich.enabled`               | 媒体补描述任务总开关                                                                            |
| `knowledge_graph.vlm_enrich.only_null_description` | 只处理 `vlm_description IS NULL`                                                         |
| `max_images_per_goods`                             | 单商品最多 VLM 几张（优先主图+海报）                                                                 |
| `max_images_per_run`                               | 单次 CLI 上限                                                                             |


### 4.5 夜间批补开关（`vlm.night_batch_only`）


| 值           | 场景            | 行为                                                        |
| ----------- | ------------- | --------------------------------------------------------- |
| `**true`**  | **生产 / 上线默认** | Cron 仅在 22:00–06:00 内执行；白天手动跑 CLI 会报错并提示                  |
| `**false`** | **本地开发实验**    | 任意时间可跑 `vlm_enrich` / 单图测试；仍受 `max_vlm_images_per_day` 限额 |


代码入口：`com.yanpanji.agents.core.guardrails.assert_vlm_batch_allowed(config)`（`vlm_enrich` CLI 启动时调用）。

**本地开发**（改 `salesagent/config/server.json` 或复制一份本地配置，**勿提交生产**）：

```json
"vlm": {
  "night_batch_only": false
}
```

无需再改 `heavy_tasks_window` 或 `vlm_daytime_allowed`。

**上线恢复**：

```json
"vlm": {
  "night_batch_only": true
}
```

---

## 五、代码模块（M2-2 实现清单）

> **现状**：`cli ingest` 仍为 stub；`ingest/vlm.py` 待建。以下为 **定稿实现边界**，开发与验收按此执行。

```text
salesagent/src/com/yanpanji/agents/
├── ingest/
│   └── vlm.py                    # VLMPipeline：加载 Int4、单图 infer、guardrails
├── knowledge/
│   └── vlm_enrich.py             # 批处理：选节点 → 下载 → VLM → 更新 DB + Chroma
├── core/
│   └── guardrails.py             # in_heavy_tasks_window() / assert_vlm_allowed()
└── cli.py                        # 新增子命令 vlm_enrich

salesagent/scripts/
├── test_vlm_one_image.py         # 单图离线验收
└── verify_m22.py                 # 统计 vlm 覆盖率 + 抽测 chunk 文本
```

### 5.1 VLMPipeline 职责

- 懒加载模型（进程内单例，避免重复占 1.4GB）
- 输入：本地图片路径 + 可选 `context_before/after` 文本
- 输出：≤200 字中文 **场景描述**（成分/功效/包装/步骤/前后对比等）
- 硬校验：`assert_vlm_batch_allowed(config)`（`night_batch_only` 开关）

### 5.2 批处理 `vlm_enrich` 职责

1. `SELECT ... FROM knowledge_media_nodes WHERE category=? AND (vlm_description IS NULL OR vlm_description='') ORDER BY updated_at LIMIT ?`
2. 可选：按 `appears_in` 关联商品优先级（有 meta 标题的 doc 优先）
3. HTTP GET 图片（`User-Agent` + 超时）；失败写 `vlm_enrich_failures` 表或日志，**不**阻塞整批
4. `UPDATE knowledge_media_nodes SET vlm_description=?, updated_at=?`
5. 调用 `finalize_global_media_chunks` 逻辑 **仅更新该节点** 对应 chunk 文本 → `embed_texts_async` → Chroma upsert 单 id
6. 幂等：同一 `url_hash` 已有非空 `vlm_description` 则 skip

### 5.3 Prompt 要点（beauty_product_v1）

```text
你是美妆电商商品图分析助手。根据图片和下列上下文，用中文输出：
1）图片展示的内容（产品/包装/成分表/使用步骤等）；
2）适合回答哪类用户问题（功效、成分、用法、对比等）；
3）图内可见文字摘要（如有）。
控制在 200 字以内，不要编造图中没有的信息。

上下文：{context_excerpt}
```

---

## 六、运行方式

### 6.1 生产：Cron 夜间（推荐）

```cron
# 22:05 媒体 VLM 补描述（在 ingest_flush 之后、或与 sync 错开）
5 22 * * * cd /www/wwwroot/salesagent && PYTHONPATH=src \
  python -m com.yanpanji.agents.cli vlm_enrich --category beauty >> logs/vlm_enrich.log 2>&1
```

**与 Niushop sync 关系**：


| 任务             | 默认 cron | 关系                              |
| -------------- | ------- | ------------------------------- |
| `sync_niushop` | 02:00   | 新图入库 → 新 media_node（vlm 仍 null） |
| `vlm_enrich`   | 22:05   | **增量**补 null；不依赖当日是否 sync       |


建议：**sync 先跑完若干天也可**，VLM 只补现有 303 节点；之后每夜 sync 新增媒体 + vlm_enrich 补 null。

### 6.2 本地 Windows（开发验收）

```powershell
cd C:\work\projects\wchat\salesagent
$env:PYTHONPATH = "src"
$env:SALESAGENT_DATA_ROOT = "C:/work/salesagent/data"

# 1) 单图 smoke test
python scripts/test_vlm_one_image.py --url "https://yanpanji.com/upload/1/common/images/....jpg"

# 2) 小批量（5 张）
python -m com.yanpanji.agents.cli vlm_enrich --category beauty --limit 5

# 3) 验收
python scripts/verify_m22.py
```

### 6.3 与 SalesAgent API 并发


| 场景                          | 建议                                                                     |
| --------------------------- | ---------------------------------------------------------------------- |
| 白天谛听 + Analyze              | ✅ 正常；**不要**跑 vlm_enrich                                                |
| 夜间 vlm_enrich               | 可保持 uvicorn 运行；VLM 在 **线程池/子进程**，不阻塞 `/api/health`（与 M2-1 embed 改造同原则） |
| 夜间全量 `sync_niushop --force` | **避免与 vlm_enrich 同时**；内存叠加易 OOM                                        |


---

## 七、验收标准

### 7.1 单图离线

```powershell
python scripts/test_vlm_one_image.py --image .\sample.jpg
# 期望：stdout 一段中文描述；进程 RSS < 2GB；无 OOM
```

### 7.2 批处理

```powershell
python -m com.yanpanji.agents.cli vlm_enrich --category beauty --limit 10
python scripts/verify_m22.py
```

**verify_m22 检查项**：


| 检查                               | 期望                     |
| -------------------------------- | ---------------------- |
| `vlm_description` 非空节点数          | ≥ limit                |
| 随机抽 1 个 `knowledge_media_{hash}` | document 含「场景描述：」      |
| Chroma 条数                        | 不变（仍为 419，仅更新向量与文本）    |
| `knowledge_edges` 计数             | 不变                     |
| 技能集检索                            | 命中媒体 chunk 时文本含 VLM 描述 |


### 7.3 SQL 自查

```sql
-- 覆盖率
SELECT
  COUNT(*) AS total,
  SUM(CASE WHEN vlm_description IS NOT NULL AND vlm_description != '' THEN 1 ELSE 0 END) AS with_vlm
FROM knowledge_media_nodes WHERE category = 'beauty';

-- 待处理
SELECT media_node_id, media_url FROM knowledge_media_nodes
WHERE category = 'beauty' AND (vlm_description IS NULL OR vlm_description = '')
LIMIT 10;
```

---

## 八、故障排查


| 现象              | 原因                            | 处理                                                    |
| --------------- | ----------------------------- | ----------------------------------------------------- |
| `VLM 夜间批补已开启`   | `night_batch_only=true` 且白天运行 | 等到 22:00 后，或开发期设 `night_batch_only: false`            |
| OOM / Killed    | 2GB 无 Swap 或与 sync 并发         | 开 Swap；降 `max_images_per_run`；串行执行                    |
| GPTQ 加载失败       | 依赖/路径错误                       | 核对 `gptqmodel`（非 auto-gptq）、`transformers<5`、模型目录、`server.json#models.qwen_vl.path` |
| 图片下载 403/超时     | CDN 防盗链                       | 配置 `niushop.image_cdn_base`；Referer；重试队列              |
| Chroma upsert 慢 | 与 BGE 抢 CPU                   | VLM 批结束后再 embed；单条 upsert                             |
| 描述胡编            | Prompt 或图不清晰                  | 收紧 prompt；跳过过小缩略图；M2-3 概念边辅助                          |


---

## 九、安全与成本

- **不上传**图片到第三方 API；Qwen-VL **纯本地推理**
- 每日 `max_vlm_images_per_day` 防止失控电费/时间
- VLM **不接入** `POST /api/analyze` 实时链路
- 日志勿打印完整 CDN URL 中的 signed query（若未来有）

---

## 十、后续衔接


| 阶段            | 关系                                   |
| ------------- | ------------------------------------ |
| **M2-3 SPO**  | 概念边 `mentions`；与 VLM 独立，可并行开发        |
| **技能集·智能选图**  | 优先读 `vlm_description` + `appears_in` |
| **M3 用户上传图**  | 同一 `vlm_enrich` 管道，source 不同         |
| **Graph RAG** | 数据量 10 万+ 再评估                        |


---

## 十一、文档与配置索引


| 文档                                              | 内容                                                   |
| ----------------------------------------------- | ---------------------------------------------------- |
| [06-Qwen2-VL-Int4.md](环境准备/06-Qwen2-VL-Int4.md) | 依赖版本、HF 下载摘要                                         |
| [知识库-结构化入库方案.md](知识库-结构化入库方案.md) §6、§13.4       | 媒体模型、增量策略                                            |
| [scripts/dev-local.md](../scripts/dev-local.md) | 三终端启动；M2-2 命令将补入                                     |
| `salesagent/config/server.json`                 | `models.qwen_vl`、`vlm`、`scheduler`、`cost_guardrails` |


---

## 十二、变更记录


| 版本   | 日期         | 说明                                                               |
| ---- | ---------- | ---------------------------------------------------------------- |
| v1.2 | 2026-06-27 | **暂停 2B Int4 CPU 方案**；§零 记录停用原因与替代选型（2.5-VL / API 等） |
| v1.1 | 2026-06-26 | 新增 `vlm.night_batch_only` 开关；guardrails.assert_vlm_batch_allowed |
| v1.0 | 2026-06-26 | 初稿：M2-2 本地化部署 → 夜间批处理 → 验收；增量增强原则                                |


