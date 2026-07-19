# 215m · OCR fallback mock boxes

> **版本**：v1.1 · 2026-07-20 · **已编码**（M1-W12b）  
> **对齐**：[185m](185m-Media元数据加深方案.md) · TC.4  
> **点名**：用户「按你建议继续干完」→ W12 · ≠ 生产 GPU Paddle

## 已决

`ocr_gateway._fallback`：按 `textHint` 切词生成假 `boxes` + `confidence>0`；无 hint 仍有默认文案与至少 1 box。

## 落地

| 路径 | 说明 |
| --- | --- |
| `ocr_gateway._fallback` | boxes · confidence |
| `tests/test_ocr_gateway.py` | 215m 断言 |

## 自检

- [x] pytest：boxes 非空 · confidence>0  

---

*v1.1 · 215m*
