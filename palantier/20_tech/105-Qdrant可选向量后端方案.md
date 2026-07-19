# 105 Qdrant 可选向量后端方案

> 状态：✅ 已落地（方案先行）  
> 前置：[`104`](./104-Pipeline与Embedding接线方案.md) · [`103`](./103-Embedding运行时方案.md) · T07 §6.2  
> 索引：[`00`](./00-技术方案索引.md) v1.0.74

---

## 1. 目标

在 **不破坏** 104 `local-kv` 的前提下，为向量索引增加可选 **Qdrant** 后端（T07：RAG 优先 Qdrant Lite）。

| 环境 | 行为 |
| --- | --- |
| 默认 / `AOS_VECTOR_BACKEND=local-kv` | 与 104 完全一致 |
| `AOS_VECTOR_BACKEND=qdrant` + `AOS_QDRANT_URL` | upsert/search/stats 走 Qdrant REST |
| `qdrant` 但未配 URL | **501 `VECTOR_BACKEND_STUB`**，不写假点 |

API 路径不变（104 已定）；响应 `mode` 为 `local-kv` | `qdrant`。

新增：

| 方法 | 路径 |
| --- | --- |
| `GET` | `/v1/aip/vector-index/_backend` | 当前后端与配置态（不含密钥） |

---

## 2. 环境变量

| 变量 | 说明 |
| --- | --- |
| `AOS_VECTOR_BACKEND` | `local-kv`（默认）\| `qdrant` |
| `AOS_QDRANT_URL` | 如 `http://127.0.0.1:6333` |
| `AOS_QDRANT_API_KEY` | 可选；有则带 `api-key` 头 |

---

## 3. Qdrant 约定

- collection 名：sanitize 为 `[a-zA-Z0-9_-]`，前缀 `aos_`  
- point id：`uuid5(NAMESPACE_URL, "{collection}:{docId}")`  
- payload：`{ id, text, meta, pluginId }`  
- 距离：Cosine；维度以首次 upsert 向量长度为准  
- 不引入 Python `qdrant-client` 硬依赖；用 stdlib `urllib`（与 embed 同风格）  
- CI **不**要求真 Qdrant；单测 mock HTTP

---

## 4. 明确不做

- 不强制本机起 Qdrant / 不改 27 门禁为必装  
- 不接 Milvus  
- 不把向量当 Ontology  
- 不做 Graph / Action Form 真组件（另刀）

---

## 5. 自测（单元测试必过）

- 默认 backend = local-kv（104 回归仍绿）  
- `qdrant` 无 URL → 501  
- mock Qdrant：upsert + search 返回 `mode=qdrant`  
- `_backend` 反映 configured  
