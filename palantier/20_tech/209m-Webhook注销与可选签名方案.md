# 209m · Webhook 注销与可选签名

> **版本**：v1.1 · 2026-07-20 · **已编码**（M1-W10b）  
> **对齐**：[101](101-通知通道运行时方案.md)  
> **点名**：用户「继续」→ W10

## 已决

| 项 | 行为 |
| --- | --- |
| DELETE | `/v1/actions/webhooks/{id}` |
| 签名 | `AOS_WEBHOOK_SIGNING_SECRET` → `X-AOS-Signature: sha256=…` |
| dry-run | 默认不变 |

## 落地

| 路径 | 说明 |
| --- | --- |
| `channel_runtime.delete_webhook` / `_webhook_signature_headers` | 注销 · HMAC |
| `wave_ext` DELETE 路由 | 404 未找到 |
| `tests/test_w10_208_209m.py` | delete · signed header |

## 自检

- [x] 注册→删除→list 空  
- [x] secret 时 delivery 含签名头（非 dry-run）  

---

*v1.1 · 209m*
