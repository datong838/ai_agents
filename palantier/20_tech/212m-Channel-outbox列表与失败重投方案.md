# 212m · Channel outbox 列表与失败重投

> **版本**：v1.1 · 2026-07-20 · **已编码**（M1-W11b）  
> **对齐**：[101](101-通知通道运行时方案.md) · [209m](209m-Webhook注销与可选签名方案.md)  
> **点名**：用户「按你建议继续干完」→ W11 · ≠ 全量 DLQ 产品

## 已决

| 项 | 行为 |
| --- | --- |
| GET | `/v1/channels/outbox` 最近投递 |
| POST | `/v1/channels/outbox/{id}/retry` 用存档 payload 再 dispatch |
| 存档 | send 时 outbox 行带 `payload` |

## 落地

| 路径 | 说明 |
| --- | --- |
| `channel_runtime.list_outbox` / `retry_outbox` | 列表 · 重投 |
| `wave_ext` GET/POST 路由 | 404 / 无 payload 400 |
| `tests/test_w11_211_212_213m.py` | list · retry · status=retried |

## 自检

- [x] send 后 list 有项  
- [x] retry 再出一条 / 原项标 retried  

---

*v1.1 · 212m*
