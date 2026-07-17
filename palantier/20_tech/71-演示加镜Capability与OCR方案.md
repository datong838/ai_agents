# 71 · 演示加镜：Capability + OCR/解析一页（TB 后可选）

> **版本**：v1.0 · 2026-07-18  
> **前提**：[70](70-业务平台可演示优先计划.md) §12 **自验收关闭**（冒烟绿 + 多次「继续直到完成」授权收口）  
> **范围**：70 已写明的 **可选穿插**（Capability 一镜 · MediaSet/OCR 一页）  
> **状态**：**✅ 完成**（2026-07-18）  
> **禁止**：Full Spoke / 生产 IdP / Ferry 加深 / 产品 1.3 Jupyter  
> **工程**：`aos-platform`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后改码 | 本文 → 再改 `demo_story` / DemoPage / smoke |
| 最小更改 | 复用既有 `/v1/aip/capabilities/*` · `/v1/parsers/extract` · OCR probe |
| 不进停车场 | 不宣称生产 OCR GPU / Full Capability SDK |

---

## 1. 目标（客户可见 DoD）

1. `/demo` 一键：**Capability Job → MediaSet rid** 可指  
2. 同响应内附：**解析 extract**（CSV 样例）+ **OCR sidecar probe**（有则 ok，无则 mock/unset 诚实）  
3. 冒烟覆盖 `POST /v1/demo/run-capability`  
4. 故事步骤增加 **TB.9（可选）**；不回头改 TB.0～8 DoD

---

## 2. 落点

| 项 | 路径 |
| --- | --- |
| API | `POST /v1/demo/run-capability` · `demo_story.run_capability_mirror` |
| UI | `DemoPage`「Capability/OCR 一镜」· 链 `/aip/capabilities` |
| 脚本 | `run-demo-smoke.ps1` · `CUSTOMER-DEMO.md` 加 1 分钟可选 |
| 测 | `tests/test_demo_story.py` |

---

## 3. 退出

- 单测绿 · smoke 含 run-capability · `/demo` 按钮可用  
- 回写 26/31/00；70 标注 §12 门禁已关、71 进行/完成  

**落地证据：** `POST /v1/demo/run-capability` · DemoPage「Capability/OCR 一镜」· `test_demo_run_capability_mirror` · smoke `run-capability` OK

---

*v1.0 · ✅*
