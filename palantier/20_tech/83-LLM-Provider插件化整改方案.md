# 83 · LLM Provider 插件化整改（对齐 20 §3.1）

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 方案定稿 · 可编码  
> **强制对齐**：[20 §3.1](20-AOS整体技术方案.md) 插件化扩展 · [T07 §3](T07-AIP人工智能平台详细技术方案.md) · [23 军规](23-AOS开源引用与交付军规.md)  
> **Rules**：军规优先 · 先方案后编码 · `production-ui-no-temp` · 最小更改但须补齐插件落点

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 20 §3.1 | 每种模型供应商 = 插件包；核心只认契约；目录落在 `aos-platform/plugins/llm-providers/` |
| 不搬 Marketplace 全家桶 | 首批 **≥30** 常见插件（含 DeepSeek）；脚注提示可扩展；**在线定制发布**走自有工作室 |
| 保存即真持久化 | 安装态 / 自定义插件写 `meta_aip_kv`，禁止 sessionStorage 冒充安装 |

---

## 1. 军规检查结论（不合项 → 本刀必改）

| §3.1 要求 | 检查结果 | 处置 |
| --- | --- | --- |
| `plugins/llm-providers/<id>/` 落点 | ❌ 仓库无 `plugins/` | **新建** ≥30 个 `manifest.json` |
| 每种供应商 = 插件 · 非硬编码 if/else 丛林 | ❌ UI 仅 5 个 `PROVIDER_CATALOG` 常量 | 改为 **扫描注册表** |
| manifest：id/version/capabilities/configSchema | ❌ 无 | 补齐契约字段 |
| 生命周期 install→configure→health | ❌ Adapter disabled/假按钮已修，仍无 install API | `GET/POST` 插件安装态 |
| UI 配置端面 | 部分有 | 列表改「已安装 / 可安装」；工作室定制发布 |
| DeepSeek 必须有 | ❌ 未单列 | **必有** `deepseek` 插件 |
| 文本/图片/视频 · 免费/中端/高端 | ❌ 未覆盖 | modalities + tier 标注 |

**本刀不做（另刀）：** LiteLLM 边车按插件自动写 yaml 热加载全量；凭据 Vault 真轮换；sessionStorage 配置草稿债清理。

---

## 2. 首批插件清单（≥30 · 可滚动）

| # | id | 名称 | modalities | tier | formFamily |
| --- | --- | --- | --- | --- | --- |
| 1 | deepseek | DeepSeek 深度求索 | text | free | openai_compatible |
| 2 | openai | OpenAI | text,image | high | openai_compatible |
| 3 | azure-openai | Azure OpenAI | text | high | azure |
| 4 | anthropic | Anthropic Claude | text | high | anthropic |
| 5 | google-gemini | Google Gemini | text,image | mid | openai_compatible |
| 6 | google-vertex | Vertex AI | text | high | openai_compatible |
| 7 | groq | Groq | text | free | openai_compatible |
| 8 | mistral | Mistral | text | mid | openai_compatible |
| 9 | cohere | Cohere | text | mid | openai_compatible |
| 10 | together-ai | Together AI | text | mid | openai_compatible |
| 11 | fireworks | Fireworks | text | mid | openai_compatible |
| 12 | openrouter | OpenRouter | text | mid | openai_compatible |
| 13 | ollama | Ollama（本地） | text | free | local |
| 14 | vllm | vLLM（本地） | text | free | local |
| 15 | lmstudio | LM Studio | text | free | local |
| 16 | openai-compatible | OpenAI 兼容通用 | text | mid | openai_compatible |
| 17 | siliconflow | 硅基流动 | text,image | free | openai_compatible |
| 18 | moonshot | 月之暗面 Kimi | text | mid | openai_compatible |
| 19 | qwen-dashscope | 通义千问 | text,image | mid | openai_compatible |
| 20 | zhipu-glm | 智谱 GLM | text | mid | openai_compatible |
| 21 | baidu-ernie | 文心一言 | text | mid | openai_compatible |
| 22 | tencent-hunyuan | 腾讯混元 | text | mid | openai_compatible |
| 23 | volcengine-doubao | 火山豆包 | text | mid | openai_compatible |
| 24 | minimax | MiniMax | text | mid | openai_compatible |
| 25 | spark-xfyun | 讯飞星火 | text | mid | openai_compatible |
| 26 | yi-01ai | 零一万物 | text | mid | openai_compatible |
| 27 | xai-grok | xAI Grok | text | high | openai_compatible |
| 28 | perplexity | Perplexity | text | mid | openai_compatible |
| 29 | huggingface | Hugging Face Endpoint | text | free | openai_compatible |
| 30 | amazon-bedrock | Amazon Bedrock | text | high | openai_compatible |
| 31 | openai-image | OpenAI 图像 | image | high | image |
| 32 | stability-ai | Stability AI | image | mid | image |
| 33 | flux | Flux 图像 | image | mid | image |
| 34 | dashscope-wanx | 通义万相 | image | mid | image |
| 35 | kling-video | 可灵 Kling 视频 | video | high | video |
| 36 | luma-video | Luma 视频 | video | high | video |
| 37 | runway-video | Runway 视频 | video | high | video |
| 38 | volcengine-jimeng | 即梦（图/视频） | image,video | mid | video |
| 39 | agnes-text | Agnes Text（内网） | text | high | openai_compatible |
| 40 | agnes-image | Agnes Image（内网） | image | high | image |
| 41 | custom-adapter | 自定义 Adapter 包 | text | mid | adapter |

脚注文案：**按需还可扩展接入更多供应商；使用「插件工作室」在线定制并发布。**

---

## 3. 契约与 API

### 3.1 Manifest（文件）

`aos-platform/plugins/llm-providers/<id>/manifest.json`

```json
{
  "id": "deepseek",
  "version": "0.1.0",
  "name": "DeepSeek",
  "nameZh": "深度求索",
  "description": "DeepSeek Chat / Reasoner · OpenAI 兼容",
  "tier": "free",
  "modalities": ["text"],
  "capabilities": ["llm", "chat"],
  "formFamily": "openai_compatible",
  "defaultModels": ["deepseek-chat", "deepseek-reasoner"],
  "litellmPrefix": "deepseek/",
  "author": "aos",
  "configSchema": {
    "type": "object",
    "required": ["apiKeyRef", "baseUrl"],
    "properties": {
      "baseUrl": { "type": "string", "default": "https://api.deepseek.com/v1" },
      "apiKeyRef": { "type": "string" },
      "models": { "type": "array", "items": { "type": "string" } }
    }
  }
}
```

### 3.2 API

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/llm-provider-plugins` | 目录 + 安装态 + 自定义 |
| POST | `/v1/aip/llm-provider-plugins/{id}/install` | 安装（写入 KV） |
| POST | `/v1/aip/llm-provider-plugins/{id}/uninstall` | 卸载 |
| PUT | `/v1/aip/llm-provider-plugins/custom` | 工作室发布/更新自定义插件 |
| GET | `/v1/plugins` | 聚合时并入 llm-provider 条目 |

### 3.3 UI（ProvidersPage）

```text
list
  ├─ 已安装：install 列表 ∪ 运行时 ready（Agnes 等）
  ├─ 可安装插件（折叠）：≥30 卡 · 安装 / 配置 · tier/modalities 徽标
  └─ 脚注：按需扩展 · 打开插件工作室
toolbar: 刷新 · 插件工作室 · Adapter 管理 · 路由策略
view=plugin-studio: 填 manifest 字段 → 发布 → 出现在可安装
```

---

## 4. 文件清单

| 路径 | 变更 |
| --- | --- |
| `docs/…/83-….md` | 本文 |
| `aos-platform/plugins/llm-providers/*/manifest.json` | 新建首批 |
| `aos_api/llm_provider_registry.py` | 扫描 + 安装态 + 自定义 |
| `wave_ext.py` | 注册 API；`/v1/plugins` 聚合 |
| `pages/s2/aip.tsx` | ProvidersPage 整改 |
| `styles.css` | 插件卡徽标 |
| `00-技术方案索引.md` | 挂 83 |

---

## 5. 自测

1. `GET /v1/aip/llm-provider-plugins` → items ≥ 30，含 `deepseek`  
2. 安装 deepseek → 刷新仍在「已安装」  
3. 工作室发布 `my-corp-llm` → 可安装列表出现  
4. `/v1/plugins` totals 含 llm-provider  
5. 既有 Agnes 已接入卡与测连通不回归  
