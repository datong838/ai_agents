# 96 · Action 试跑校验 · 诚实口径微修

> **版本**：v1.0 · 2026-07-19  
> **状态**：✅ 已落地 · 自测通过  
> **上游**：[95](95-OT属性与Action编辑方案.md)  
> **Rules**：接已有 API · 禁止假口径 · 最小更改 · 不碰 89 后置

---

## 1. 范围

| # | 能力 | 做法 |
| --- | --- | --- |
| **A** | Action 试跑校验 | 编辑器接 `POST /v1/actions/validate`；样例 payload JSON；结果诚实展示 |
| **B** | 诚实口径微修 | Usage 去掉「近 30 天」假口径；Wiki CTA 无实例时不硬默认 `wo-1001` |

非目标：参数可视化设计器 · Wiki PUT · 三路冲突 · Draft 分叉 · Dataset 同步。

### A 注意

校验读的是 **库内已保存** 的 criteria / markings，不是表单草稿。UI 须明示：**先保存再试跑**。

---

## 2. 契约

```json
POST /v1/actions/validate
{ "actionTypeId": "CloseWorkOrder", "payload": { "reason": "ok" } }
→ 200 { "ok": true, "actionTypeId" }
→ 400 VALIDATION + details（criteria 失败）
```

后端已有 · 仅前端接线。

---

## 3. 文件

| 路径 | 变更 |
| --- | --- |
| `ActionTypeEditorPage.tsx` | A：payload + 试跑钮 |
| `objectTypeDetail.tsx` | B：Usage 文案 · Wiki CTA |
| 本文 + `00-技术方案索引.md` | 登记 v1.0.65 |

---

## 4. 自测

1. CloseWorkOrder · payload `{}` → 400 / 失败提示 ✅（`test_validate_endpoint_rejects`）  
2. payload `{"reason":"ok"}` → ok ✅  
3. 改 criteria 未保存就试跑 → 仍按旧规则（UI Banner 明示）  
4. Usage 文案无「近 30 天」；无实例时 Wiki 链无 `wo-1001` ✅  

pytest：`test_wave3_drafts` + `test_actions` → **8 passed**

---

## 5. 风险

| 风险 | 处理 |
| --- | --- |
| 用户以为草稿可验 | Banner + 按钮旁提示「基于已保存」 |
| markings 不足 | 透传 API 错误，不吞 |
