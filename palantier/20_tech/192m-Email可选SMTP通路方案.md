# 192m · Email 可选 SMTP 通路

> **版本**：v1.2 · 2026-07-20  
> **状态**：✅ **已编码**（M1-W4c）· 自测通过  
> **计划**：[180m](180m-M1后置闭环开发计划.md)  
> **对齐**：[101](101-通知通道运行时方案.md) · [182m](182m-成员邮箱手机OTP方案.md)  
> **落点**：`channel_runtime.py`（既有）· `tests/test_channel_runtime_101.py::test_channel_email_with_smtp_ok`

## 已决

| 项 | 行为 |
| --- | --- |
| `AOS_SMTP_HOST` 已配 | `channel-email` send → SMTP · health `smtpConfigured=true` |
| 未配 | 仍 501 `CHANNEL_STUB`（诚实） |
| SMS | 永久 501 |
| 实现 | `channel_runtime.py` 已有；本刀补 **绿路径单测**（mock smtplib） |

## 自检

- [x] mock SMTP → send 200 · mode=smtp  
- [x] health smtpConfigured  
- [x] SMS 仍 501（既有单测）  

---

*v1.2 · 192m · 已编码*
