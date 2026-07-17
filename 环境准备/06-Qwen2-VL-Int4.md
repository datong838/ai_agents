# 环境准备 — Qwen2-VL-2B-Instruct-GPTQ-Int4

> ⚠️ **已废弃 / 基本不可用**（2026-06-27 验证结论）：单图 CPU 推理 15–40 分钟、识图质量弱，**不再推进**。  
> **当前替代**：[M2-2-媒体图片描述-元宝技能方案.md](../M2-2-媒体图片描述-元宝技能方案.md)（谛听本机元宝 → `apply_yuanbao_vlm_result`）。  
> 下文保留作历史 Runbook；`server.json#vlm.enabled` 保持 **false**。

> **角色**：~~服务端 **图片理解 VLM**（夜间 ingest / 商品图描述）~~  
> **阶段**：~~**MVP**~~ → **已暂停**  
> **配置**：`server.json#models.qwen_vl`、`vlm`  
> **技术方案**：[服务端 §9.3](../技术方案-SalesAgent服务端.md)

---

## 1. 选型说明

| 项 | 值 |
|----|-----|
| 模型 | **Qwen2-VL-2B-Instruct-GPTQ-Int4** |
| 量化 | GPTQ **Int4**（2GB 机器唯一可行方案） |
| 设备 | **CPU**（`device: cpu`） |
| 峰值内存 | 加载 ~1.4GB，推理 ~1.8GB |
| 运行窗口 | **仅** `heavy_tasks_window` 22:00–06:00 |
| 禁止 | 白天运行；FP16/Int8 全精度；实时 analyze |

---

## 2. 硬件与系统前置

| 项 | 要求 |
|----|------|
| 内存 | 独占 CVM 2GB + **2GB Swap**（§8.4.3） |
| 与 Chroma 关系 | 夜间跑 VLM 时避免并发 bulk upsert / 高 analyze |
| 磁盘 | 模型约 **1.5–2GB**；路径见下 |

---

## 3. 模型下载

### 3.1 HuggingFace（推荐源）

模型 ID（以 HuggingFace 实际仓库为准，常见命名）：

```text
Qwen/Qwen2-VL-2B-Instruct-GPTQ-Int4
```

**国内镜像**：

```bash
export HF_ENDPOINT=https://hf-mirror.com
pip install huggingface_hub
huggingface-cli download Qwen/Qwen2-VL-2B-Instruct-GPTQ-Int4 \
  --local-dir C:/work/salesagent/data/models/Qwen2-VL-2B-Instruct-GPTQ-Int4
```

Linux 生产：

```text
/www/wwwroot/salesagent/models/Qwen2-VL-2B-Instruct-GPTQ-Int4/
```

同步 `server.json#models.qwen_vl.path`。

### 3.2 校验文件

目录内应含 `config.json`、`*.safetensors` 或 GPTQ 权重、`tokenizer` 等；`config.json` 中 `quantization_config` 含 GPTQ。

---

## 4. Python 依赖

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install transformers accelerate
pip install auto-gptq optimum  # GPTQ 加载，按模型卡说明选型
pip install qwen-vl-utils pillow
```

> **版本锁定**：以 Qwen2-VL 官方 README 为准；不同版本依赖可能不同，MVP 搭建时 `pip freeze` 固化。

---

## 5. 加载示例

```python
import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

MODEL_PATH = "/www/wwwroot/salesagent/models/Qwen2-VL-2B-Instruct-GPTQ-Int4"

processor = AutoProcessor.from_pretrained(MODEL_PATH, trust_remote_code=True)
model = Qwen2VLForConditionalGeneration.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="cpu",
    trust_remote_code=True,
)

def describe_image(image_path: str) -> str:
    # 按 Qwen2-VL 官方 chat template 构造 messages + vision inputs
    ...
```

封装于 `com.yanpanji.agents.ingest.vlm.VLMPipeline`。

### 5.1 硬校验

```python
def assert_vlm_allowed():
    if config.deployment.vlm_daytime_allowed:
        raise RuntimeError("VLM daytime forbidden")
    if not in_heavy_tasks_window():
        raise RuntimeError("VLM only in 22:00-06:00")
```

---

## 6. 与 ingest 集成

```bash
# 仅夜间 cron
python -m com.yanpanji.agents.cli ingest
```

流程：staging 图片 → VLM 转文字 → 切块 → BGE-M3 → Chroma upsert（batch=50）。

`max_vlm_images_per_day: 50`（`cost_guardrails`）。

---

## 7. 验收

### 7.1 离线单图

```bash
python scripts/test_vlm_one_image.py --image ./sample.jpg
# 输出一段中文描述，无 OOM
```

### 7.2 内存

```bash
free -m   # Linux，推理前后对比
```

### 7.3 API

上传含图片的 ingest batch，夜间跑完后 `GET /api/ingest/status` 中 chunk 增加。

---

## 8. 本地 Windows（30GB）vs 线上 2GB

| 环境 | 说明 |
|------|------|
| 开发机 | 可装 FP16 做对比，**生产配置仍以 Int4 为准** |
| 2GB CVM | **仅 Int4** + Swap；POC 阶段可跳过整个 VLM |

---

## 9. 常见问题

| 问题 | 处理 |
|------|------|
| OOM | 确保 Swap；减少并发；仅夜间单进程 |
| GPTQ 加载失败 | 核对 `auto-gptq` 与 CUDA 无关的 CPU 路径 |
| 模型路径错误 | Linux 大小写敏感（§开发计划 1.4） |
| POC 是否必须 | **否**；不阻塞主链路 E2E |

---

## 10. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-06-16 | 初稿 |
