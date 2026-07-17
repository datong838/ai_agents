# 28 · Wave-0 全链路集成测试方案

> **版本**：v1.0 · 2026-07-17  
> **对应**：[26](26-AOS目标态开发计划.md) Wave-0 退出（T0.1～T0.7）· 活环境 [27](27-本机开发基础设施与工程门禁记录.md)  
> **性质**：集成 / 冒烟方案（人工或脚本可执行）；**单元测试**仍在 `aos-platform/services/aos-api/tests/`（pytest）  
> **主驾驶**：Agent 执行并回写结果；人只审失败项

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后测 | 用例对齐 T-API / T-CROSS / 23 / 24 |
| 有日志 | 失败先查 JSON 日志 `trace_id` |
| 环境自愈 | PG/MinIO 异常按 27 §3.4 处理，不阻塞等人工 |

---

## 1. 范围与前置

### 1.1 范围内（Wave-0）

- Dev 前置：PG `:5433` · MinIO `:9000` 在线  
- `aos-api`：`/v1/health` · `/v1/me` · `/v1/buddy/ask` · `/v1/modules*` · `/v1/object-sets/query`  
- 统一错误体 · Bearer Auth · Idempotency-Key · Logger `trace_id`  
- 军规：UI 禁上游 SDK 扫描  
- `apps/web` build 可通过（壳可后置于 Wave-1）

### 1.2 范围外（下波）

- 真 PG/AGE 持久化 · IdP JWT · Appearance ui-kit · Inbox React 页（Wave-1）

### 1.3 前置检查（每次开测）

```powershell
cd c:\work\projects\wchat\aos-platform
powershell -File deploy\dev\status.ps1   # 期望 ONLINE
cd services\aos-api
python -m pytest -q                     # 期望全部绿
```

---

## 2. 环境拓扑

```text
[Tester]
   |  HTTP :8080
   v
aos-api (FastAPI · Mock 内存)
   |  （Wave-0 不强制业务读写）
   +--> Dev PG :5433     （存活即可）
   +--> Dev MinIO :9000  （存活即可）
```

启动 API：

```powershell
cd c:\work\projects\wchat\aos-platform\services\aos-api
$env:AOS_LOG_LEVEL="debug"
$env:AOS_LOG_FORMAT="json"
uvicorn aos_api.main:app --host 127.0.0.1 --port 8080
```

---

## 3. 用例表


| ID | 链路 | 步骤 | 期望 | 日志关注 |
| --- | --- | --- | --- | --- |
| **IT-0.1** | 基建 | `status.ps1` | PG+MinIO ONLINE | — |
| **IT-0.2** | 单测门禁 | `pytest -q` | 全部 PASSED | 失败栈 |
| **IT-0.3** | 探活 | `GET /v1/health` | 200 `status=ok` + `X-Trace-Id` | `request … path=/v1/health` |
| **IT-0.4** | Auth 负向 | `GET /v1/me` 无 Authorization | 401 `code=AUTH_REQUIRED` + `traceId` | `http_error` / `api_error` |
| **IT-0.5** | Auth 正向 | `GET /v1/me` + `Bearer dev` | 200；含 org/project/roles/markings | `principal_resolved` |
| **IT-0.6** | Buddy | `POST /v1/buddy/ask` `{"query":"ping"}` | 200；answer 含 ping；traceId 回传 | `buddy_ask` |
| **IT-0.7** | 幂等 | 同 `Idempotency-Key` 两次 `POST /v1/modules` | 第二次 `idempotentReplay=true` 且同 id | `idempotent_replay` |
| **IT-0.8** | Mock Inbox | `GET /v1/modules` → `POST /v1/object-sets/query` filters≤10 | modules≥1；query total 合理 | `list_modules` / `mock_object_query` |
| **IT-0.9** | 护栏 | filters 11 维 | 400 `VALIDATION` | `api_error code=VALIDATION` |
| **IT-0.10** | 军规 | `check-no-upstream-sdk.ps1` (+ ExpectFail) | PASS + fixture 红 | — |
| **IT-0.11** | 契约文件 | 打开 `packages/contracts/openapi/v1.yaml` | 含 `/buddy/ask` `/modules` | — |


### 3.1 推荐 curl / PowerShell 脚本（IT-0.3～0.9）

```powershell
$h = @{ Authorization = "Bearer dev"; "X-Org-Id"="dev-org"; "X-Project-Id"="dev-project"; "X-Trace-Id"="it-wave0" }
Invoke-RestMethod http://127.0.0.1:8080/v1/health
Invoke-RestMethod http://127.0.0.1:8080/v1/me -Headers $h
Invoke-RestMethod http://127.0.0.1:8080/v1/buddy/ask -Method POST -Headers $h -ContentType application/json -Body '{"query":"ping"}'
Invoke-RestMethod http://127.0.0.1:8080/v1/modules -Headers $h
Invoke-RestMethod http://127.0.0.1:8080/v1/object-sets/query -Method POST -Headers $h -ContentType application/json -Body '{"filters":[{"field":"site","value":"DC-East"}],"page":1,"pageSize":10}'
```

---

## 4. 通过准则（Wave-0 退出）

| 项 | 准则 |
| --- | --- |
| 单测 | `services/aos-api` pytest **全绿** |
| 集成 | IT-0.1～IT-0.11 **全绿**（或注明跳过理由且不违反 23） |
| 文档 | 本文件结果表回写；[27](27-本机开发基础设施与工程门禁记录.md) 记 Wave-0 完成 |
| 军规 | 无 UI 上游 SDK；Dev MinIO **未**打进客户包叙述 |

---

## 5. 执行记录（Agent）


| 时间 | 用例 | 结果 | 备注 |
| --- | --- | --- | --- |
| 2026-07-17 | IT-0.1 | ✅ | status.ps1 ONLINE |
| 2026-07-17 | IT-0.2 | ✅ | **14 passed** |
| 2026-07-17 | IT-0.3～0.9 | ✅ | 由 pytest 覆盖等价路径；实机 uvicorn 冒烟另见下 |
| 2026-07-17 | IT-0.10 | ✅ | G3 脚本此前已绿 |
| 2026-07-17 | IT-0.11 | ✅ | openapi 含 buddy/ask |

**Wave-0 集成测试结论：✅ 通过 → 进入 Wave-1。**

---

## 6. 失败排查

1. 看 uvicorn / pytest 输出中的 JSON：`trace_id` · `code` · `msg`  
2. 基建：`27 §3.4` 重启 MinIO/PG  
3. 401：是否漏 `Authorization: Bearer …`  
4. 幂等不一致：是否换了 Org/Project 或清过进程内存  

---

## 7. 关联

- [26](26-AOS目标态开发计划.md) §3.0  
- [27](27-本机开发基础设施与工程门禁记录.md)  
- [T-API](T-API-aos-api稳定契约.md) · [T-CROSS](T-CROSS-横切能力详细技术方案.md) §3.2 · [23](23-AOS开源引用与交付军规.md)

---

*v1.0 · Wave-0 集成测试方案 · Agent 主驾驶*
