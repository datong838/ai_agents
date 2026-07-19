# 103 Embedding / Rerank 运行时方案

> 状态：✅ 已落地（方案先行）  
> 前置：[`98`](./98-插件化剩余域收口方案.md) · [`100`](./100-Connector运行时Host分发方案.md) · [`101`](./101-Channel运行时方案.md) · [`20`](./20-AOS整体技术方案.md) §3.1 / T07  
> 索引：[`00`](./00-技术文档索引.md) v1.0.72

---

## 1. 目标

为 `plugins/embeddings/{pluginId}/` 补 **Host 运行时**：

| 方法 | 路径 |
| --- | --- |
| `POST` | `/v1/embeddings/{plugin_id}/embed` |
| `POST` | `/v1/embeddings/{plugin_id}/rerank` |
| `GET` | `/v1/embeddings/{plugin_id}/health` |

规则与 100/101 一致：目录存在 → **已安装** → 按 `pluginId` 分发；未实现能力诚实 **501**。

---

## 2. 插件能力

| pluginId | embed | rerank | 条件 |
| --- | --- | --- | --- |
| `embed-openai-compatible` | ✅（有网关时） | ❌ 501 | `AOS_EMBED_*` 或复用 `AGNES_BASE_URL`+`AGNES_API_KEY`+`AOS_EMBED_MODEL` |
| `rerank-cohere` | ❌ 501 | ❌ 默认 501 | 未接 Cohere Key 前不假排序 |
| 其他目录插件 | 501 | 501 | stub |

未配置网关时 `embed` 返回 **501 `EMBEDDING_STUB`**（与 Email 无 SMTP 同口径），**不**返回假向量，避免检索链路被污染。

---

## 3. 请求体

### embed

```json
{ "texts": ["hello", "world"], "model": "optional-override" }
```

成功：`{ "pluginId", "model", "sidecar", "vectors": [[...], ...] }`（`vectors[i]` 与 `texts[i]` 对齐）。

### rerank

```json
{ "query": "...", "documents": ["a", "b"], "topN": 2 }
```

成功时：`{ "pluginId", "results": [{ "index", "score", "document" }] }`；当前默认 501。

---

## 4. 环境变量

| 变量 | 说明 |
| --- | --- |
| `AOS_EMBED_BASE_URL` | 优先；空则回退 `AGNES_BASE_URL` |
| `AOS_EMBED_API_KEY` | 优先；空则回退 `AGNES_API_KEY` |
| `AOS_EMBED_MODEL` | 默认 `text-embedding-3-small` |

调用 OpenAI 兼容：`POST {base}/v1/embeddings`，body `{ model, input }`。

---

## 5. 明确不做

- ~~不接生产向量库写入（仍属 Pipeline/检索刀）~~ → 见 [`104`](./104-Pipeline与Embedding接线方案.md)（本地 KV，非 Milvus）
- 不实现 Cohere Rerank 真调用（无 Key）
- 不改 Ontology / Connector / Channel 已有路径

---

## 6. 自测

- 未安装 / 未知插件 → 400（与 100/101 同口径）  
- 无网关 embed → 501 `EMBEDDING_STUB`  
- rerank-cohere → 501  
- health 反映 configured / stub  
- mock 上游时 embed 返回对齐 `vectors`  
