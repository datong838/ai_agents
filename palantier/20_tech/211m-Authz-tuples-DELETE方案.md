# 211m · Authz tuples DELETE

> **版本**：v1.1 · 2026-07-20 · **已编码**（M1-W11a）  
> **对齐**：[207m](207m-OpenFGA-tuple列表API方案.md) · [55](55-OpenFGA与鉴权模型方案.md)  
> **点名**：用户「按你建议继续干完」→ W11

## 已决

`DELETE /v1/authz/tuples`（body: user?/relation/object）删本地行；有远程 URL 时尽力 deletes；删后 GET 无该行。

## 落地

| 路径 | 说明 |
| --- | --- |
| `openfga.delete_tuple` / `delete_tuple_remote` | 本地删 · 远程尽力 |
| `routers/authz.py` DELETE | 404 未命中 |
| `tests/test_w11_211_212_213m.py` | 写→删→list |

## 自检

- [x] 写→删→list 空  
- [x] 未命中 404  

---

*v1.1 · 211m*
