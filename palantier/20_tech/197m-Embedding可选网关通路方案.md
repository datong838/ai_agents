# 197m · Embedding/Rerank 可选网关通路

> **版本**：v1.1 · 2026-07-20  
> **状态**：✅ **已编码**（M1-W6b）· 自测通过  
> **计划**：[180m](180m-M1后置闭环开发计划.md)  
> **对齐**：[103](103-Embedding运行时方案.md)  
> **落点**：`embedding_runtime.py` · `tests/test_embedding_runtime_103.py::test_197m_rerank_with_key_mocked`

## 已决

| 项 | 行为 |
| --- | --- |
| embed | 既有 `AOS_EMBED_*` |
| rerank | `AOS_RERANK_API_KEY` / `AOS_COHERE_API_KEY`；可选 `AOS_RERANK_BASE_URL` |
| 未配 | 501 `EMBEDDING_STUB` |
| 已配 | 上游 → 200 `{ results }`；health `mode=cohere` |

## 自检

- [x] 无 Key → rerank 501  
- [x] mock Key → 200 + results  
- [x] health 翻转  

---

*v1.1 · 197m · 已编码*
