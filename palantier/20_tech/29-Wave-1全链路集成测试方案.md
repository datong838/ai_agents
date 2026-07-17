# 29 · Wave-1 全链路集成测试方案

> **版本**：v1.0 · 2026-07-17  
> **对应**：[26](26-AOS目标态开发计划.md) Wave-1 · 前置 [28](28-Wave-0全链路集成测试方案.md)  
> **主驾驶**：Agent

---

## 1. 范围

- AppShell / Appearance / 侧栏叙事  
- 概览 · 应用列表 · 运营台 Inbox · Selection≤10 · >1万护栏  
- 发布幂等 · Marking · 画布 · Buddy 芯片+Mock chat  
- 契约：`/v1/modules` · `/v1/object-sets/query` · `/v1/buddy/ask`

## 2. 前置

```powershell
powershell -File c:\work\projects\wchat\aos-platform\deploy\dev\status.ps1
cd c:\work\projects\wchat\aos-platform\services\aos-api; python -m pytest -q
cd c:\work\projects\wchat\aos-platform\apps\web; npm test; npm run build
# API :8080 + npm run dev :5173
```

## 3. 用例


| ID | 步骤 | 期望 |
| --- | --- | --- |
| IT-1.1 | 打开 `/` | 见 AOS 壳 + 侧栏分组 |
| IT-1.2 | 外观切换 light/dark | `html[data-aos-theme]` 变化 |
| IT-1.3 | `/workshop` | Module 列表来自 API |
| IT-1.4 | `/workshop/inbox` 添加 site=DC-East | 列表过滤；Selection 计数 |
| IT-1.5 | 模拟 total=12000 | 出现 >1万护栏横幅 |
| IT-1.6 | `/workshop/publish` 连点 | 幂等成功文案 |
| IT-1.7 | `/workshop/canvas` | Layout 树+预览 |
| IT-1.8 | `/workshop/buddy` | 芯片可见；询问返回 echo |
| IT-1.9 | 单测 | web vitest 全绿 · api pytest 全绿 |

## 4. 执行记录

| 时间 | 结果 |
| --- | --- |
| 2026-07-17 | ✅ web **9 passed** · api **19 passed**（含 Wave-2 ontology）· build 绿 |

**Wave-1 集成结论：✅ 通过（功能点见 26 进度看板）→ 继续 Wave-2。**

---

*v1.0 · Wave-1 集成测试*
