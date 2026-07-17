# 环境准备 — DeepSeek API

> **角色**：服务端 **需求分析 LLM**（`POST /api/analyze` 后台流水线）  
> **阶段**：**POC 必须**  
> **配置**：`salesagent/config/server.json#llm.providers.deepseek`  
> **技术方案**：[服务端 §7.2](../技术方案-SalesAgent服务端.md)

---

## 1. 选型说明

> 官方文档：[DeepSeek 开放平台](https://platform.deepseek.com/usage)
>
> [首次调用 API](https://api-docs.deepseek.com/zh-cn/) · [模型 & 价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)


| 项              | 本项目定稿                                     | 官方（2026）                                           | 结论                   |
| -------------- | ----------------------------------------- | -------------------------------------------------- | -------------------- |
| Provider       | DeepSeek 官方 API                           | 同左                                                 | ✅                    |
| 协议             | **OpenAI-compatible**（`chat.completions`） | `base_url`: `https://api.deepseek.com`             | ✅                    |
| **模型（POC 默认）** | `**deepseek-v4-flash`**                   | V4 快速版；结构化 JSON 分析                                 | ✅ **推荐保持**           |
| 模型（可选升级）       | —                                         | `deepseek-v4-pro`                                  | 更强更贵；POC 不必换         |
| 旧模型名           | **不用**                                    | `deepseek-chat` → 等同 `deepseek-v4-flash` 非思考模式     | ⚠️ **2026/07/24 弃用** |
| 旧模型名           | **不用**                                    | `deepseek-reasoner` → 等同 `deepseek-v4-flash` 思考模式  | ⚠️ **2026/07/24 弃用** |
| Base URL       | `https://api.deepseek.com`                | 同左                                                 | ✅                    |
| 密钥环境变量         | `DEEPSEEK_API_KEY`                        | [API Keys](https://platform.deepseek.com/api_keys) | ✅                    |


`server.json` 当前配置（`salesagent/config/server.json#llm.providers.deepseek`）与上表一致。

**不用于**：客户端本地推理；微信 OCR（客户端 PaddleOCR）。

---

## 2. 注册与获取 API Key

1. 打开 [DeepSeek 开放平台](https://platform.deepseek.com/)（或官方最新控制台 URL）。
2. 注册账号 → **API Keys** → 创建 Key。
3. 充值 / 确认免费额度（政策以控制台为准）。
4. **禁止**将 Key 写入 `server.json` 或提交 Git。

### 本地 `.env` ✅ 路径定稿

**唯一位置**：`salesagent/.env`（与 `config/server.json` 同级）。

```bash
cd salesagent
cp .env.example .env
# 编辑 .env 填入 DEEPSEEK_API_KEY
```


| 环境                   | 路径                             | 说明                                         |
| -------------------- | ------------------------------ | ------------------------------------------ |
| Windows 开发（monorepo） | `wchat/salesagent/.env`        | 与 `config/server.json` 同级                  |
| Linux 生产             | `/www/wwwroot/salesagent/.env` | **部署根即服务端目录**，无 `salesagent/salesagent` 嵌套 |


**部署对应关系**：仓库内 `salesagent/` 目录的内容（含 `.env`）发布到线上 `/www/wwwroot/salesagent/`；monorepo 根目录（`ditingclient/`、`docs/` 等）**不上线**。

`config_loader` 从**当前工作目录**加载 `.env`（开发 `cd salesagent`；生产 `WorkingDirectory=/www/wwwroot/salesagent`）。

---

## 3. 对接方式（代码契约）

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

resp = client.chat.completions.create(
    model="deepseek-v4-flash",  # 与 server.json 一致
    messages=[
        {"role": "system", "content": "只输出 JSON"},
        {"role": "user", "content": "..."},
    ],
    temperature=0.3,
    timeout=30,
)
```

- 强制 JSON 输出：若 API 支持 `response_format={"type":"json_object"}` 则启用（见服务端 §7.2）。
- 超时 30s；失败重试 2 次 → 再降级混元或规则（`llm_fallback_on_quota`）。

---

## 4. 验收（开发前必做）

### 4.1 API 探活（可选）

> **Windows PowerShell**：`curl` 是 `Invoke-WebRequest` 别名，**不能**直接抄 Linux 的 `-H` 写法。请用下面任一方式。

**方式 A — 使用 `curl.exe`（推荐，与 Linux 一致）**

```powershell
cd C:\work\projects\wchat\salesagent
# 从 .env 加载 Key 到当前终端（仅本次会话）
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#][^=]+)=(.*)$') { Set-Item -Path "env:$($matches[1].Trim())" -Value $matches[2].Trim() }
}
curl.exe https://api.deepseek.com/v1/models -H "Authorization: Bearer $env:DEEPSEEK_API_KEY"
```

**方式 B — PowerShell 原生**

```powershell
$headers = @{ Authorization = "Bearer $env:DEEPSEEK_API_KEY" }
Invoke-RestMethod -Uri "https://api.deepseek.com/v1/models" -Headers $headers
```

**Linux / Git Bash**

```bash
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY"
```

期望：返回 JSON 模型列表，HTTP 200；401 表示 Key 无效或未加载。

### 4.2 Python 最小脚本（推荐验收）

**先升级 SDK**（避免 `proxies` 与 `httpx` 版本冲突）：

```powershell
pip install -U "openai>=1.55" python-dotenv
```

**方式 A — 独立脚本（推荐，避免 PowerShell 多行粘贴错乱）**

```powershell
cd C:\work\projects\wchat\salesagent
pip install -U "openai>=1.55" python-dotenv
python scripts\verify_deepseek.py
```

期望输出：`DeepSeek OK: Hello!`（或类似短句）。

**方式 B — 单行（PowerShell）**

```powershell
cd C:\work\projects\wchat\salesagent
python -c "import os; from dotenv import load_dotenv; from openai import OpenAI; load_dotenv(); c=OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'], base_url='https://api.deepseek.com'); r=c.chat.completions.create(model='deepseek-v4-flash', messages=[{'role':'user','content':'say hello'}], max_tokens=50, extra_body={'thinking':{'type':'disabled'}}); print(r.choices[0].message.content)"
```

> V4 默认 **thinking 开启**，小 `max_tokens` 会占满推理额度导致 `content` 为空；验收与 analyze 建议 `extra_body={"thinking":{"type":"disabled"}}`。

> 若 `deepseek-v4-flash` 报错，在控制台核对可用模型 id 并同步改 `server.json`。

### 4.3 接入 SalesAgent 后

`POST /api/analyze` → 202 → WS `demand_event` 中 `llm_meta.provider == "deepseek"`。

---

## 5. 费用与护栏

- POC 配额：客户端 + 服务端双侧 **500 次/日** 有效 analyze（见 PRD §8）。
- 开发调试：可用 mock LLM 跳过真实调用（仅 Phase 1 骨架阶段），**E2E 前必须切回真实 Key。
- 监控：记录 `llm_meta.latency_ms`；P95 目标 < 15s（POC）。

---

## 6. 常见问题


| 问题                                      | 处理                                                                                             |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- |
| 401 Invalid API Key                     | 检查 `salesagent/.env` 是否加载；Key 是否过期                                                             |
| `unexpected keyword argument 'proxies'` | `pip install -U "openai>=1.55"`（旧版 openai 1.12 + 新版 httpx 不兼容）                                 |
| 返回 `content` 为空                         | V4 默认 **thinking 开启**；analyze 用 `extra_body={"thinking":{"type":"disabled"}}`，或增大 `max_tokens` |
| 模型名不存在                                  | 控制台查可用 id，更新 `server.json#llm.providers.deepseek.model`                                        |
| 超时                                      | 客户端 60s WS 等待；服务端 BackgroundTasks 内重试                                                          |
| 国内网络                                    | 一般可直连；若失败检查代理/防火墙                                                                              |


---

## 7. 修订记录


| 版本   | 日期         | 说明                                                              |
| ---- | ---------- | --------------------------------------------------------------- |
| v1.0 | 2026-06-16 | 初稿                                                              |
| v1.1 | 2026-06-17 | §2 定稿 `.env` 路径；线上 `/www/wwwroot/salesagent/.env`（无嵌套）          |
| v1.2 | 2026-06-17 | §1 对照官方 V4 模型表；验收脚本改用 `deepseek-v4-flash`                       |
| v1.3 | 2026-06-17 | §4.2 增 `scripts/verify_deepseek.py`；openai 升级说明；`max_tokens` 修正 |
| v1.4 | 2026-06-17 | §4.2 验收脚本关闭 thinking；FAQ 补充 `content` 为空原因                      |


