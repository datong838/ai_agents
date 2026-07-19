# 104 Pipeline ↔ Embedding 接线方案

> 状态：✅ 已落地（方案先行）  
> 前置：[`103`](./103-Embedding运行时方案.md) · [`98`](./98-插件化剩余域收口方案.md) · [`20`](./20-AOS整体技术方案.md) §3.1 / T07  
> 索引：[`00`](./00-技术方案索引.md) v1.0.73

---

## 1. 目标

把 103 的 Host `embed` **接到 Pipeline 演示链**：文档 → 已安装 embedding 插件 → **本地向量索引** → 余弦检索。

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `POST` | `/v1/pipelines/{pipeline_id}/embed` | 按管道写入集合（默认 `collection=pipeline_id`） |
| `POST` | `/v1/aip/vector-index/upsert` | 直接 upsert（不绑管道） |
| `POST` | `/v1/aip/vector-index/search` | query embed + topK 余弦 |
| `GET` | `/v1/aip/vector-index/{collection}` | 集合统计（无假向量内容） |

**存储**：`meta_aip_kv`，key=`vector_index:{collection}`。  
**不是** Milvus/Qdrant；禁止把向量索引冒充 Ontology。

---

## 2. 规则

1. 调用 `embedding_runtime.dispatch_embed`；插件未装 / 无网关 → **原样 400/501**，**不**写入假向量。  
2. 单次最多 **32** 条文档；超限 400。  
3. Pipeline 不存在 → 404；`create_pipeline` **不**自动 embed。  
4. `documents` 为空时：用 ObjectSet `WorkOrder` 抽样标题（有则真数据，无则 400 要求显式 documents）。  
5. search 时 query 也走同一 `pluginId` embed。

---

## 3. 请求体摘要

### pipeline embed / upsert

```json
{
  "pluginId": "embed-openai-compatible",
  "collection": "optional",
  "documents": [{ "id": "opt", "text": "...", "meta": {} }],
  "replace": false
}
```

成功：`{ collection, pluginId, upserted, total, dimensions, mode: "local-kv" }`

### search

```json
{ "collection": "...", "query": "...", "pluginId": "embed-openai-compatible", "topK": 5 }
```

成功：`{ collection, results: [{ id, text, score, meta }] }`

---

## 4. UI（最小）

`PipelinesPage`：选中管道可「写入向量索引」与「检索试跑」；501 时展示诚实错误，不伪装成功。

---

## 5. 明确不做

- ~~不引入 Qdrant/Milvus 生产拓扑~~ → 见 [`105`](./105-Qdrant可选向量后端方案.md)（可选 Qdrant；默认仍 local-kv）  
- 不改 Ontology / Funnel / Insight Backfill  
- 不在 Pipeline create 时隐式 embed  
- 不做 Graph / Action Form 真组件（另刀）

---

## 6. 自测

- 未知 pipeline → 404  
- 无网关 → 501，KV 无新增向量  
- mock embed → upsert + search 命中  
- 超 32 条 → 400  
