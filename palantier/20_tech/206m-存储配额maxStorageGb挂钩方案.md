# 206m · 存储配额 maxStorageGb 挂钩

> **版本**：v1.1 · 2026-07-20 · ✅ **已编码**（M1-W9b）  
> **落点**：`assert_storage_quota` · `POST /v1/media-sets` · `tests/test_w9_205_206_207m.py`

## 自检

- [x] 配额满 → 409  
- [x] 无租户无 env → 不拦（沿用）  

---

*v1.1 · 206m · 已编码*
