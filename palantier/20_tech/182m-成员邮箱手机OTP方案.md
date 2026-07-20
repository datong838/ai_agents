# 182m · 成员邮箱/手机 OTP（验证码）最小方案

> **版本**：v1.1 · 2026-07-19  
> **状态**：✅ 方案定稿 · **已编码**（M1-W1b）  
> **分支**：`m1` · [180m](180m-M1后置闭环开发计划.md)  
> **对齐**：[168](168-成员自然人识别-邮箱手机号方案.md) · [41](41-TX.3-IdP-OIDC对接方案.md) · [181m](181m-TWA租户面PG迁库方案.md)  
> **消化**：179 ③ **168 验证码后置**  
> **实现**：`aos_api/otp.py` · `/v1/otp/send|verify` · `AOS_OTP_REQUIRED`（默认 0）· Web 成员页验证码 · `tests/test_otp_182m.py`

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小 | 只挡「加人 / 改本人联系方式」写路径；登录仍可走既有 Dev/OIDC |
| 诚实 | Dev 可用 **固定验证码 / 日志打印码**；生产须配置 SMS/Email 提供方 |
| 不破坏 | 无 OTP 开关时保持 168 现行为（可配 `AOS_OTP_REQUIRED=0`） |

## 1. 已决产品

| 场景 | 行为 |
| --- | --- |
| 管理员用邮箱/手机 **加人** | 先 `POST /v1/otp/send` → 用户/管理员提交码 → `POST …/members` 带 `otpId+code` 或服务端会话校验 |
| 本人改邮箱/手机（`/v1/me/profile`） | 改敏感字段须 OTP；仅改姓名/职务可不验 |
| 旧 subject 加人 | 不受影响 |

## 2. API（最小）

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/otp/send` | body: `{ channel: email\|phone, to, purpose: invite\|profile }` → `{ otpId, expiresIn }` |
| POST | `/v1/otp/verify` | `{ otpId, code }` → `{ ok, ticket }`（短时 ticket 供加人/改档） |

存储：PG 表 `twa_otp`（若 181m 已上）或内存+TTL（仅 Dev）。

## 3. 发送通道

| 环境 | 行为 |
| --- | --- |
| Dev | `AOS_OTP_DEV_CODE=6位` 或日志输出码；不真发信 |
| 配置了 SMTP/SMS | 真发（复用/扩展 101 Email；SMS 可后置接一家） |
| 未配置且 `AOS_OTP_REQUIRED=1` | send 返回 503 诚实错误 |

## 4. 非目标

- 强制 IdP account linking  
- 通讯录导入  
- 二维码邀请  
- 改登录 subject  

## 5. 落点

| 路径 | 变更 |
| --- | --- |
| `aos_api/otp.py` + router | send/verify |
| members / me profile | 门禁 |
| Web 加人表单 / 我的资料 | 验证码输入 |
| 168 / 179 | 回写 |

## 6. 自检

- [ ] Dev 固定码可加人  
- [ ] 错码 400  
- [ ] `AOS_OTP_REQUIRED=0` 回归 168 行为  

---

*v1.0 · 182m · M1-W1b*
