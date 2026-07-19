# 174 · 桌面登录 CORS（Load failed）

> **版本**：v1.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 可编码  
> **对齐**：[20c](20c-AOS桌面端详细技术方案.md) · [173](173-桌面欢迎登录产品话术方案.md)  
> **点名**：用户桌面登录「Load failed」

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小 | 仅扩 CORS 白名单 + 登录失败人话提示 |
| 不破坏 | Web :5173 仍保留 |

## 1. 根因

| 项 | 值 |
| --- | --- |
| 桌面 devUrl | `http://localhost:1420`（tauri.conf） |
| API CORS 原白名单 | 仅 `127.0.0.1:5173` / `localhost:5173` |
| 结果 | 浏览器/WebView 拦跨域 → 文案常为 **Load failed** |
| API 本身 | `POST /v1/auth/token` 本机 curl **正常** |

## 2. 已决

CORS `allow_origins` 增加：

- `http://localhost:1420` · `http://127.0.0.1:1420`
- `tauri://localhost` · `https://tauri.localhost`（打包壳）

登录页：网络类错误改为「连不上平台，请确认平台已启动」类人话。

## 3. 落点

- `aos_api/main.py`
- `Login.tsx`
- 重启 aos-api 后生效

---

*v1.0*
