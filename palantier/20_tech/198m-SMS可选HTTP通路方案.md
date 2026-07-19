# 198m · SMS 可选 HTTP 通路

> **版本**：v1.1 · 2026-07-20  
> **状态**：✅ **已编码**（M1-W6c）· 自测通过  
> **计划**：[180m](180m-M1后置闭环开发计划.md)  
> **对齐**：[101](101-通知通道运行时方案.md) · [192m](192m-Email可选SMTP通路方案.md)  
> **落点**：`channel_runtime.py` · `tests/test_channel_runtime_101.py::test_198m_channel_sms_with_webhook_ok`

## 已决

| 项 | 行为 |
| --- | --- |
| 配置 | `AOS_SMS_WEBHOOK_URL` 或 `AOS_SMS_API_URL`+`AOS_SMS_API_KEY` |
| 未配 | 501 `CHANNEL_STUB` |
| 已配 | POST JSON → 200 · mode=http；health `smsConfigured` |

## 自检

- [x] 无配置 → 501  
- [x] mock urlopen → send 200  
- [x] health smsConfigured  

---

*v1.1 · 198m · 已编码*
