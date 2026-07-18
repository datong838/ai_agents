# 94 · W17 Agnes 默认接入与 LLM 回归方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[33](33-T3.9-LiteLLM边车去stub方案.md) · [93](93-W16-Data子页与Graph-Buddy与可演示DoD方案.md) · `aos-platform/.env`  
> **约束**：密钥不入库 · pytest 仍 mock · 真 LLM 仅 demo 脚本

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 先方案后代码 | 本文 → llm_gateway / web / scripts |
| 最小更改 | 不推翻 T3.9 路由优先级 Agnes→LiteLLM→mock |
| 安全 | API 只回 vault ref · 不回明文 key |
| 自测 | `run-pytest` + `run-demo-smoke` + **`run-agnes-smoke`** |

---

## 1. 背景

用户已在 `aos-platform/.env` 配置：

- `AGNES_API_KEY`
- `AGNES_BASE_URL`
- `AGNES_TEXT_MODEL`
- `AGNES_IMAGE_MODEL`

`aos-api` 启动时 `env_load.load_dotenv()` 加载；`llm_gateway.chat()` **优先走 Agnes**。

---

## 2. 范围

| 项 | 落点 | 动作 |
| --- | --- | --- |
| ensure-api 加载 .env | `scripts/demo/ensure-api.sh` | 启动前 export `AGNES_*` · 支持 `--restart` |
| providers 元数据 | `llm_gateway.providers_payload` | 增 `endpoint`（仅 base URL，无 key） |
| 供应商页 | `aip.tsx` · `ProvidersPage` | Agnes 已接入 Banner · endpoint 指标 |
| 路由页 | `aip.tsx` · `ModelRouterPage` | 默认选中 `defaultTextModel` · 路由表优先 Agnes |
| LLM 回归脚本 | `scripts/demo/run-agnes-smoke.sh` | providers/chat/buddy 断言 `route=agnes` |
| 单测 | `test_llm_gateway.py` | monkeypatch Agnes 配置 → providers 形态 |
| 手册 | [72](72-系统启停与健康检查手册.md) · [27](27-本机开发基础设施与工程门禁记录.md) | 挂 Agnes smoke 命令 |

---

## 3. 路由优先级（不变）

```text
Agnes (.env) → LiteLLM sidecar → mock fallback
```

pytest `conftest` 清空 `AGNES_*`，保持 **179+ passed** 离线绿。

---

## 4. 回归命令

```bash
# 1) 确保 API 在线（会加载 .env；改 .env 后须 --restart）
bash scripts/demo/ensure-api.sh --restart

# 2) 常规冒烟
bash scripts/demo/run-demo-smoke.sh

# 3) Agnes 真 LLM（需 .env 已填）
bash scripts/demo/run-agnes-smoke.sh

# 4) 离线单测
bash scripts/ci/run-pytest.sh
cd apps/web && npm test
```

### Agnes smoke 断言

| 检查 | 期望 |
| --- | --- |
| `GET /v1/aip/providers` | `sidecar=agnes-openai-compatible` · items ≥ 1 |
| `GET /v1/aip/models` | `defaultTextModel=AGNES_TEXT_MODEL` |
| `POST /v1/aip/chat` | `route=agnes` · answer 非 `[mock-llm]` |
| `POST /v1/buddy/ask` | sources[0].route=agnes |

---

## 5. 验收

1. `.env` 有 Agnes 时 providers/models 页展示 Agnes 模型 ✅  
2. Model Router 试聊默认选中 text 模型 ✅  
3. `run-agnes-smoke.sh` 绿 ✅  
4. pytest / npm test 仍绿 ✅  

---

## 变更日志

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-18 | W17 Agnes 默认 + LLM 回归 |

---

*v1.0*
